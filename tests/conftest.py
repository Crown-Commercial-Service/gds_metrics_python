import os
import pytest
import time
from flask import Flask

from gds_metrics import GDSMetrics


FAKE_APP_ID = "123"
SLOW_REQUEST_DURATION = 0.1


@pytest.fixture
def app(mocker):
    flask_app = Flask(__name__)
    ctx = flask_app.app_context()
    ctx.push()

    mocker.patch.dict(
        os.environ,
        {'VCAP_APPLICATION': '{"application_id": "' + FAKE_APP_ID + '"}'}
    )
    mocker.patch('prometheus_client.generate_latest', return_value='Prometheus metrics response')

    @flask_app.route('/')
    def index():
        return 'index'

    @flask_app.route('/slow_request')
    def slow_request():
        time.sleep(SLOW_REQUEST_DURATION)
        return 'slow request'

    @flask_app.route('/exception')
    def exception():
        raise Exception()

    yield flask_app

    ctx.pop()


@pytest.fixture(scope='function')
def client(app):
    with app.test_request_context(), app.test_client() as client:
        metrics = GDSMetrics()
        metrics.init_app(app)

        yield client


@pytest.fixture(scope='function')
def client_without_basic_auth(app, mocker):
    with app.test_request_context(), app.test_client() as client:
        mocker.patch.dict(
            os.environ,
            {
                'VCAP_APPLICATION': '{"application_id": "' + FAKE_APP_ID + '"}',
                'METRICS_BASIC_AUTH': 'false'
            }
        )

        metrics = GDSMetrics()
        metrics.init_app(app)

        yield client


@pytest.fixture(scope='function')
def client_without_env_app_id(app, mocker):
    with app.test_request_context(), app.test_client() as client:
        mocker.patch.dict(os.environ, {'VCAP_APPLICATION': '{}'})

        metrics = GDSMetrics()
        metrics.init_app(app)

        yield client
