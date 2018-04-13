# GDS metrics for Python apps

GDS Metrics are in Alpha and these instructions are subject to change.

GDS Python metrics enables your [Python][] web app to export performance data to [Prometheus][], you can add metrics to your app using this [Python package][].

This package is a thin wrapper around [the Python Prometheus client][] that:

* T
* B
* C

Once you’ve added this package, metrics data is served from your app's metrics endpoint and is scraped by Prometheus. This data can be turned into performance dashboards using [Grafana][].

You can read more about the Reliability Engineering monitoring solution [here][].

## Before using GDS metrics

Before using GDS metrics you should have:

* created a [Python][] or [Flask][] app
* deployed it to [GOV.UK Platform as a Service (PaaS)][]

## How to install metrics for Flask apps

To use GDS metrics you must:

1. Add the [latest version of the package][] to your requirements.txt, for example:

    ```TBC```

2. Run the following command to install the package:

    ```pip install -r requirements.tt```

3. Restart your server by running:

    ```python run.py```

4. Visit any page of your app (for example [the index page][]) to generate some site traffic

5. Visit the metrics endpoint at `/metrics` to check if the package was set up correctly. If it's set up correctly, you will see a page containing some metrics (for example `http_req_duration_seconds`).

If you're not using Flask, you'll also need to ...

## Running on GOV.UK Platform as a Service (PaaS)

When running on PaaS, citizens won’t see your metrics in production as this endpoint is automatically protected with authentication.

The PaaS documentation has information on how you can [deploy a basic Python app][]. You can also read the official Cloud Foundry guide which has detailed information on [deploying Python apps][].

## Optional configuration

You can change the path for serving metrics (by default `/metrics`) by setting the `PROMETHEUS_METRICS_PATH` [environment variable][].

## How to setup extended metrics

While common metrics are recorded by default, you can also:

* record your own metrics such as how many users are signed up for your service, or how many emails it's sent
* use the Prometheus interface to set your own metrics as the metrics Python package is built on top of [the Python Prometheus client][]

You can read more about the different types of metrics available in the [Prometheus documentation][].

## Contributing

GDS Reliability Engineering welcome contributions. We'd appreciate it if you write tests with your changes and document them where appropriate, this will help us review them quickly.

## Licence

This project is licensed under the [MIT License][].

[Python]: https://www.python.org/
[Prometheus]: https://prometheus.io/
[Python package]: TBC
[the Python Prometheus client]: https://pypi.python.org/pypi/prometheus_client
[Grafana]: https://grafana.com/
[here]: https://reliability-engineering.cloudapps.digital/#reliability-engineering
[Flask]: http://flask.pocoo.org/
[GOV.UK Platform as a Service (PaaS)]: https://www.cloud.service.gov.uk/
[latest version of the package]: TBC
[the index page]: http://localhost:5000/
[PaaS]: https://www.cloud.service.gov.uk/
[deploy a basic Python app]: TBC
[deploying Python apps]: TBC
[environment variable]: https://docs.cloud.service.gov.uk/#environment-variables
[Prometheus documentation]: https://prometheus.io/docs/concepts/metric_types/
[MIT License]: https://github.com/alphagov/gds_metrics_python/blob/master/LICENSE
