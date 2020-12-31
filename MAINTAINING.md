# Maintaining gds_metrics_python

Notes for maintainers.

## Making a release

Use [GitHub releases] to release a new version of this package. You should
include the latest CHANGELOG entry in the release notes.

GitHub Actions will take care of publishing the package to PyPI for you.
See the [Upload Python Package workflow](.github/workflows/python-publish.yml)
for details on how this works.

[GitHub releases]: https://docs.github.com/en/github/administering-a-repository/managing-releases-in-a-repository#creating-a-release
