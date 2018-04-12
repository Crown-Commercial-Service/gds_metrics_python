import os
from flask import request, Response

import prometheus_client
from prometheus_client import Counter, Histogram
from prometheus_client import multiprocess, CollectorRegistry


class GDSMetrics(object):

    def __init__(self):
        self.metrics_path = os.environ.get('PROMETHEUS_METRICS_PATH', '/metrics')

        # set multiprocess temp directory
        os.environ.setdefault('prometheus_multiproc_dir', '/tmp')

        self.registry = CollectorRegistry()
        multiprocess.MultiProcessCollector(self.registry)

    def init_app(self, app):
        app.add_url_rule(self.metrics_path, 'metrics', self.metrics)

    def metrics(self):
        return Response(
            prometheus_client.generate_latest(self.registry),
            mimetype='text/plain; version=0.0.4; charset=utf-8'
        )
