import gzip
import hmac
import json
import os
from time import monotonic

from flask import abort, g, request, Response
from flask.signals import got_request_exception, request_finished

# set multiprocess temp directory before we import prometheus_client
os.environ.setdefault('prometheus_multiproc_dir', '/tmp') # noqa

import prometheus_client
from prometheus_client import multiprocess, CollectorRegistry

from .metrics import ( # noqa proxy metric types imports
    Counter,
    Gauge,
    Summary,
    Histogram,
    HTTP_SERVER_EXCEPTIONS_TOTAL,
    HTTP_SERVER_REQUEST_DURATION_SECONDS,
    HTTP_SERVER_REQUESTS_TOTAL,
)


class GDSMetrics(object):

    def __init__(self):
        self.metrics_path = os.environ.get('PROMETHEUS_METRICS_PATH', '/metrics')
        if os.environ.get("METRICS_BASIC_AUTH", "true") == "true":
            self.auth_token = json.loads(os.environ.get("VCAP_APPLICATION", "{}")).get("application_id")
        else:
            self.auth_token = False

        self.registry = CollectorRegistry()
        multiprocess.MultiProcessCollector(self.registry)

    def init_app(self, app):
        app.add_url_rule(self.metrics_path, 'metrics', self.metrics_endpoint)

        app.before_request(self.before_request)
        request_finished.connect(self.teardown_request, sender=app)
        got_request_exception.connect(self.handle_exception, sender=app)

    def metrics_endpoint(self):
        if self.auth_token:
            auth_header = request.headers.get('Authorization', '')
            if not auth_header:
                abort(401)
            elif not hmac.compare_digest(auth_header, 'Bearer {}'.format(self.auth_token)):
                abort(403)

        response = Response(
            prometheus_client.generate_latest(self.registry),
            mimetype='text/plain; version=0.0.4; charset=utf-8',
            headers={
                'Cache-Control': 'no-cache, no-store, max-age=0, must-revalidate',
            }
        )

        accept_encoding = request.headers.get('Accept-Encoding', '')

        if 'gzip' not in accept_encoding.lower():
            return response

        response.data = gzip.compress(response.data)
        response.headers['Content-Encoding'] = 'gzip'
        response.headers['Content-Length'] = len(response.data)
        response.headers['Vary'] = 'Accept-Encoding'

        return response

    def before_request(self, *args, **kwargs):
        g._gds_metrics_start_time = monotonic()

    def teardown_request(self, sender, response, *args, **kwargs):
        resp_time = monotonic() - g._gds_metrics_start_time
        HTTP_SERVER_REQUEST_DURATION_SECONDS.labels(
            request.method,
            request.host,
            request.url_rule.rule if request.url_rule else 'No endpoint',
            response.status_code
        ).observe(resp_time)

        HTTP_SERVER_REQUESTS_TOTAL.labels(
            request.method,
            request.host,
            request.url_rule.rule if request.url_rule else 'No endpoint',
            response.status_code
        ).inc()

        return response

    def handle_exception(self, sender, exception, *args, **kwargs):
        HTTP_SERVER_EXCEPTIONS_TOTAL.labels(type(exception)).inc()
