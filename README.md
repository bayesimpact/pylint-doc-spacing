# Pylint Doc Spacing Checker

[![Latest Version](https://img.shields.io/pypi/v/pylint-doc-spacing.svg)](https://pypi.python.org/pypi/pylint-doc-spacing)

A Pylint plugin to check for the presence/absence of spacing after documentation strings.

## Installation

Installing with `pip`:

```sh
pip install pylint-doc-spacing
```

## Usage

To use pylint-doc-spacing, it must be loaded as a plugin when running pylint:

```sh
pylint --load-plugins pylint_doc_spacing <module-or-package>
```

## Configuration

The consistency of doc spacing can be configured:

* `one-line`: enforces having exactly one empty line after the documentation (the default).
* `none`: enforces no blank line after the documentation.
* `any`: does not enforce anything.

You can decide on different spacing for different kind of documentation by changing the following
Pylint configs:

* `module-doc-spacing` for the modules' documentation.
* `class-doc-spacing` for the classes' documentation.
* `function-doc-spacing` for the functions and methods documentation.

Example of configuration in `.pylintrc`:

```ini
[MISCELLANEOUS]
function-doc-spacing=none
class-doc-spacing=only-one
module-doc-spacing=any
```
