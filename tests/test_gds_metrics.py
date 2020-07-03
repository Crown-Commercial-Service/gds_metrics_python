from unittest.mock import Mock

from gds_metrics import GDSMetrics

from flask import Flask, g


def test_teardown_requests_doesnt_record_duration_metric_if_gds_metrics_start_time_not_set(mocker):
    app = Flask(__name__)
    with app.test_request_context():
        assert not hasattr(g, "_gds_metrics_start_time")
        duration_metric = mocker.patch('gds_metrics.HTTP_SERVER_REQUEST_DURATION_SECONDS.labels')
        count_metric = mocker.patch('gds_metrics.HTTP_SERVER_REQUESTS_TOTAL.labels')
        gds_metrics = GDSMetrics()

        gds_metrics.teardown_request(sender=Mock(), response=Mock())

        assert not duration_metric.called
        assert count_metric.called
