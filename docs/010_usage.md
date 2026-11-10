# Usage

Use `stub` fixture in your test functions:

```python
def test_django_related(stub):

    stub.apply({
        # Replace `call_command` with a generated function.
        'django.core.management.call_command': '[func]',

        # Replace `BaseCommand` with a generated class.
        'django.core.management.base.BaseCommand': '[cls]',

        # Replace `dummy` with generated MagicMock.
        'django.dummy': '[mock]',

        # Replace entire `cv2` module.
        'cv2': '[mock]',

        # Sometimes we need just a persistent (always the same) magic mock.
        'numpy': '[mock_persist]',

        # Stub multiple attributes in the same module with custom objects.
        'django.conf': {
            'settings': object(),
            'some': True,
        },

    })
```

If we want to replace some dependency with a stub not in a fixture but globally, we can use `stub_global()` function
in root `conftest.py` (this code will apply patch before tests, so tests will be safe to import code using dependencies).

```python
from pytest_stub.toolbox import stub_global

stub_global({
    'cv2': '[mock_persist]',
})
```
