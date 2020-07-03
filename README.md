# GDS metrics for Python apps [![Build Status](https://travis-ci.org/alphagov/gds_metrics_python.svg?branch=master)](https://travis-ci.org/alphagov/gds_metrics_python)
[![Coverage Status](https://coveralls.io/repos/github/alphagov/gds_metrics_python/badge.svg?branch=master)](https://coveralls.io/github/alphagov/gds_metrics_python?branch=master)

This project is currently maintained by the [Digital Marketplace team](https://github.com/orgs/alphagov/teams/digitalmarketplace).

GDS Metrics are in Alpha and these instructions are subject to change.

GDS Python metrics enables your [Python Flask][] web app to export performance data to [Prometheus][], you can add metrics to your app using this [GDS Python Package][].

This package is a thin wrapper around [the Python Prometheus client][] that:

* protects your `/metrics` endpoint with basic HTTP authentication for apps deployed to GOV.UK PaaS
* exposes standard metrics to be used in Grafana
```http_server_request_duration_seconds_bucket, http_server_request_duration_seconds_count, http_server_request_duration_seconds_sum, http_server_exceptions_total```

Once you’ve added this package, metrics data is served from your app's metrics endpoint and is scraped by Prometheus. This data can be turned into performance dashboards using [Grafana][].

You can read more about the Reliability Engineering monitoring solution [here][].

## Before using GDS metrics

Before using GDS metrics you should have:

* created a [Python Flask][] app running on a [Gunicorn][] HTTP Server
* deployed it to [GOV.UK Platform as a Service (PaaS)][]

## How to install metrics for Flask apps served on a Gunicorn server

To use GDS metrics you must:

1. Add the [latest version of the package][] to your `requirements.txt`, for example:

    `gds-metrics==0.1.1`

2. Run the following command to install the package:

    `pip install -r requirements.txt`

3. In your application file, usually `application.py`, create the GDSMetrics object and pass the Flask app object to the `init_app` function:

    ```python
    ...
    from gds_metrics import GDSMetrics

    app = Flask(__name__)

    metrics = GDSMetrics()
    metrics.init_app(app)
    ...
    ```

    You want to run `metrics.init_app` before any other `init_app` functions and as early in your request processing as possible to get the most accurate and reliable response timings.

4. Add/Update your Gunicorn config to import `child_exit` from the library:

    ```python
    from gds_metrics.gunicorn import child_exit
    ```

    More information about [Prometheus Gunicorn setup][].

5. Restart your server by running:

    `gunicorn -c <config file>.py <application file>:<app variable>`

    For example -

    `gunicorn -c gunicorn_config.py application:app`

6. Visit any page of your app (for example [the index page][]) to generate some site traffic

7. Visit the metrics endpoint at `/metrics` to check if the package was set up correctly. If it's set up correctly, you will see a page containing some metrics (for example `http_server_request_duration_seconds_bucket`).

## Running on GOV.UK Platform as a Service (PaaS)

When running on PaaS, citizens won’t see your metrics in production as this endpoint is automatically protected with authentication.

You can also read the official Cloud Foundry guide which has detailed information on [deploying Python apps][].

## Optional configuration

You can change the path for serving metrics (by default `/metrics`) by setting the `PROMETHEUS_METRICS_PATH` [environment variable][].

If you are running `blue-green` deployments through a cf plugin like [autopilot][] you should disable basic auth on the `\metrics` endpoint and use [IP whitelisting][] by setting the `METRICS_BASIC_AUTH` [environment variable][] to `false`. This will minimise gaps in metrics during deployment.

## How to setup extended metrics

While common metrics are recorded by default, you can also:

* record your own metrics such as how many users are signed up for your service, or how many emails it's sent
* use the Prometheus interface to set your own metrics as the metrics Python package is built on top of [the Python Prometheus client][]

You can read more about the different types of metrics available in the [Prometheus documentation][].

## Contributing

We welcome contributions. We'd appreciate it if you write tests with your changes and document them where appropriate, this will help us review them quickly.

## Licence

This project is licensed under the [MIT License][].

[Prometheus]: https://prometheus.io/
[GDS Python package]: https://pypi.org/project/gds-metrics/
[the Python Prometheus client]: https://pypi.python.org/pypi/prometheus_client
[Grafana]: https://grafana.com/
[here]: https://reliability-engineering.cloudapps.digital/#reliability-engineering
[Gunicorn]: http://gunicorn.org/
[Prometheus Gunicorn setup]: https://github.com/prometheus/client_python#multiprocess-mode-gunicorn
[Python Flask]: http://flask.pocoo.org/
[GOV.UK Platform as a Service (PaaS)]: https://www.cloud.service.gov.uk/
[latest version of the package]: https://pypi.org/project/gds-metrics/
[the index page]: http://localhost:5000/
[PaaS]: https://www.cloud.service.gov.uk/
[deploy a basic Python app]: https://docs.cloud.service.gov.uk/#deploy-a-django-app
[deploying Python apps]: https://docs.cloudfoundry.org/buildpacks/python/index.html
[environment variable]: https://docs.cloud.service.gov.uk/#environment-variables
[Prometheus documentation]: https://prometheus.io/docs/concepts/metric_types/
[MIT License]: https://github.com/alphagov/gds_metrics_python/blob/master/LICENSE
[IP whitelisting]: https://reliability-engineering.cloudapps.digital/manuals/monitor-paas-app-with-prometheus.html#ip-whitelist-your-app-metrics-endpoint
