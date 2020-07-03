## 0.2.1
* Fixes a bug with uncaught AttributeErrors if the `before_request` function did not run before `teardown_request`

## 0.2.0
* Makes basic auth optional

## 0.1.1
* Disabled caching for the metrics endpoint.
* Set the `prometheus_multiproc_dir` before importing prometheus client.
* Fixed duplicate metrics.
* Change the metrics path label to use the request route pattern rather than the actual path to cut down on the number of timeseries returned.
* Move metrics to separate file.
* Add authentication for metrics endpoint when deployed onto PaaS.
* Compress metrics response with gzip if provided in header.
* Labels without matching rule respond with `No endpoint`.
* Expose Counter, Gauge, Summary, Histogram to users without exposing the Prometheus client library.
* Add a `child_exit` hook for gunicorn multiprocessing support.
* Added flake8 support and tests for the code.
* Added a Makefile to make it easier to run tests and publish the library to PyPI.
* Updated the README.

## 0.1.0

### Changed
* First version of gds_metrics_python wrapper.
* Added Counter and Histogram stats based on metrics delivered by [GDS metrics Ruby][].
```http_server_request_duration_seconds_bucket, http_server_request_duration_seconds_count, http_server_request_duration_seconds_sum, http_server_exceptions_total```

[GDS metrics Python]: https://github.com/alphagov/gds_metrics_python