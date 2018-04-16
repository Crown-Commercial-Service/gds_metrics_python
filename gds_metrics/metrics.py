from prometheus_client import Counter, Gauge, Summary, Histogram # noqa


HTTP_SERVER_REQUESTS_TOTAL = Counter(
    'http_server_requests_total',
    'Total requests',
    ['method', 'host', 'path', 'code']
)

HTTP_SERVER_EXCEPTIONS_TOTAL = Counter(
    'http_server_exceptions_total',
    'Total number of exceptions',
    ['error']
)

HTTP_SERVER_REQUEST_DURATION_SECONDS = Histogram(
    'http_server_request_duration_seconds', 'Server request duration in seconds',
    ['method', 'host', 'path', 'code']
)
