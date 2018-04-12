import os
from time import monotonic
from flask import g, request, Response
from flask.signals import got_request_exception, request_finished

# set multiprocess temp directory before we import prometheus_client
os.environ.setdefault('prometheus_multiproc_dir', '/tmp') # noqa

import prometheus_client
from prometheus_client import Counter, Histogram
from prometheus_client import multiprocess, CollectorRegistry


class GDSMetrics(object):

    def __init__(self):
        self.metrics_path = os.environ.get('PROMETHEUS_METRICS_PATH', '/metrics')

        self.registry = CollectorRegistry()
        multiprocess.MultiProcessCollector(self.registry)

        self.HTTP_SERVER_REQUESTS_TOTAL = Counter(
            'http_server_requests_total',
            'Total requests',
            ['method', 'host', 'path', 'code'],
        )

        self.HTTP_SERVER_EXCEPTIONS_TOTAL = Counter(
            'http_server_exceptions_total',
            'Total number of exceptions',
            ['error'],
        )

        self.HTTP_SERVER_REQUEST_DURATION_SECONDS = Histogram(
            'http_server_request_duration_seconds', 'Server request duration in seconds',
            ['method', 'host', 'path', 'code'],
        )

    def init_app(self, app):
        app.add_url_rule(self.metrics_path, 'metrics', self.metrics_endpoint)

        app.before_request(self.before_request)
        request_finished.connect(self.teardown_request, sender=app)
        got_request_exception.connect(self.handle_exception, sender=app)

    def metrics_endpoint(self):
        return Response(
            prometheus_client.generate_latest(self.registry),
            mimetype='text/plain; version=0.0.4; charset=utf-8',
            headers={
                'Cache-Control': 'no-cache, no-store, max-age=0, must-revalidate',
            }
        )

    def before_request(self, *args, **kwargs):
        g._gds_metrics_start_time = monotonic()

    def teardown_request(self, sender, response, *args, **kwargs):
        resp_time = monotonic() - g._gds_metrics_start_time
        self.HTTP_SERVER_REQUEST_DURATION_SECONDS.labels(
            request.method,
            request.host,
            request.path,
            response.status_code
        ).observe(resp_time)

        self.HTTP_SERVER_REQUESTS_TOTAL.labels(
            request.method,
            request.host,
            request.path,
            response.status_code
        ).inc()

        return response

    def handle_exception(self, sender, response, *args, **kwargs):
        self.HTTP_SERVER_EXCEPTIONS_TOTAL.labels(kwargs.get('exc_info', [None])[0]).inc()
