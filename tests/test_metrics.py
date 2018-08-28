import pytest
from tests.conftest import FAKE_APP_ID, SLOW_REQUEST_DURATION

VALID_AUTH_HEADER = 'Authorization', 'Bearer {}'.format(FAKE_APP_ID)


@pytest.mark.parametrize('auth_header,expected_status', [
    (None, 401),
    ([VALID_AUTH_HEADER], 200),
    ([('Authorization', 'Bearer invalid-token')], 403),
])
def test_auth_header_returns_expected_response(client, auth_header, expected_status, mocker):
    response = client.get(
        '/metrics',
        headers=auth_header
    )
    assert response.status_code == expected_status


def test_no_basic_auth_env_flag_returns_200(client_without_basic_auth):
    response = client_without_basic_auth.get('/metrics')
    assert response.status_code == 200


def test_metrics_path_without_app_id_env_does_not_need_auth(client_without_env_app_id):
    response = client_without_env_app_id.get('/metrics')
    assert response.status_code == 200


def test_app_path_does_not_need_auth(client):
    response = client.get('/')
    assert response.status_code == 200


def test_compresses_response_with_gzip_header(client):
    response = client.get(
        '/metrics',
        headers=[('Accept-Encoding', 'gzip'), (VALID_AUTH_HEADER)]
    )
    assert response.headers['Content-Encoding'] == 'gzip'


def test_does_not_compress_response_without_gzip_header(client):
    response = client.get(
        '/metrics',
        headers=[VALID_AUTH_HEADER]
    )
    assert response.headers.get('Content-Encoding') is None


def test_gzip_request_header_does_not_affect_other_paths(app, client):
    response = client.get(
        '/',
        headers=[('Accept-Encoding', 'gzip'), (VALID_AUTH_HEADER)]
    )
    assert response.headers.get('Content-Encoding') is None


def test_calls_histogram_observe(client, mocker):
    histogram_observe = mocker.patch(
        'gds_metrics.metrics.HTTP_SERVER_REQUEST_DURATION_SECONDS._wrappedClass.observe')

    client.get(
        '/slow_request',
        headers=[(VALID_AUTH_HEADER)]
    )
    assert histogram_observe.called
    # cannot define exact duration so expect at least the specified duration for the slow_request
    assert histogram_observe.call_args_list[0][0][0] > SLOW_REQUEST_DURATION and \
        histogram_observe.call_args_list[0][0][0] < SLOW_REQUEST_DURATION + 0.05


def test_requests_increases_request_counter(client, mocker):
    counter_inc = mocker.patch(
        'gds_metrics.metrics.HTTP_SERVER_REQUESTS_TOTAL._wrappedClass.inc')
    client.get(
        '/',
        headers=[(VALID_AUTH_HEADER)]
    )
    assert counter_inc.called


def test_exception_increases_exception_counter(client, mocker):
    counter_inc = mocker.patch(
        'gds_metrics.metrics.HTTP_SERVER_EXCEPTIONS_TOTAL._wrappedClass.inc')

    response = client.get(
        '/exception',
        headers=[(VALID_AUTH_HEADER)]
    )
    assert response.status_code == 500
    assert counter_inc.called
