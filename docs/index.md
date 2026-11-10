# pytest-stub

<https://github.com/idlesign/pytest-stub>

*Stub packages, modules and attributes.*

This pytest plugin allows you to replace dependencies with stubs.

It can be useful if you want to test some code using a dependency without actually having this dependency,
for example if you're testing your library, which uses some parts of another library.

## Requirements

1. Python 3.10+
2. pytest >= 2.9.0

## Install

```shell
$ python -m pip install pytest-stub
```

See [Usage](010_usage.md) for the details.
