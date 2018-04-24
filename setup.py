"""
Library for Prometheus instrumentation in Python/Flask based apps
"""

import re
import ast
from setuptools import setup, find_packages


_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('gds_metrics/version.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='gds-metrics',
    version=version,
    url='https://github.com/alphagov/gds_metrics_python',
    license='MIT',
    author='Government Digital Service',
    description='Library for Prometheus instrumentation in Python/Flask based apps',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "prometheus_client==0.2.0",
        "Flask>=0.10",
        "blinker>=1.4",
    ],
    # for running pytest as `python setup.py test`, see
    # http://doc.pytest.org/en/latest/goodpractices.html#integrating-with-setuptools-python-setup-py-test-pytest-runner
    setup_requires=[
        'pytest-runner'
    ],
    test_suite="tests",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: System :: Monitoring",
        "License :: OSI Approved :: MIT License",
    ],
    keywords='gds reliability engineering metrics',
)
