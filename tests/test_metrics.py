import pytest
from tests.conftest import FAKE_APP_ID, FAKE_BASIC_AUTH_TOKEN, SLOW_REQUEST_DURATION

VALID_AUTH_HEADER = 'Authorization', 'Bearer {}'.format(FAKE_APP_ID)
VALID_AUTH_HEADER_TOKEN = 'Authorization', 'Bearer {}'.format(FAKE_BASIC_AUTH_TOKEN)


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


@pytest.mark.parametrize('auth_header,expected_status', [
    (None, 401),
    ([VALID_AUTH_HEADER_TOKEN], 200),
    ([VALID_AUTH_HEADER], 403),
    ([('Authorization', 'Bearer invalid-token')], 403),
])
def test_auth_token_takes_precedence_over_application_id(client_with_auth_token, auth_header, expected_status):
    response = client_with_auth_token.get('/metrics', headers=auth_header)
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
    histogram_labels = mocker.patch('gds_metrics.HTTP_SERVER_REQUEST_DURATION_SECONDS.labels')
    client.get(
        '/slow_request',
        headers=[(VALID_AUTH_HEADER)]
    )
    assert histogram_labels.called
    observe_mock = histogram_labels.return_value.observe
    assert observe_mock.called
    # cannot define exact duration so expect at least the specified duration for the slow_request
    assert observe_mock.call_args_list[0][0][0] > SLOW_REQUEST_DURATION and \
        observe_mock.call_args_list[0][0][0] < SLOW_REQUEST_DURATION + 0.05


def test_requests_increases_request_counter(client, mocker):
    counter_labels = mocker.patch(
        'gds_metrics.HTTP_SERVER_REQUESTS_TOTAL.labels')
    client.get(
        '/',
        headers=[(VALID_AUTH_HEADER)]
    )
    assert counter_labels.called
    assert counter_labels.return_value.inc.called


def test_exception_increases_exception_counter(client, mocker):
    counter_labels = mocker.patch(
        'gds_metrics.HTTP_SERVER_EXCEPTIONS_TOTAL.labels')

    response = client.get(
        '/exception',
        headers=[(VALID_AUTH_HEADER)]
    )
    assert response.status_code == 500
    assert counter_labels.called
    assert counter_labels.return_value.inc.called
