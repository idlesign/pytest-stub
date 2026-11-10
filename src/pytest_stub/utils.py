import sys
from typing import Union, Dict, Any
from unittest.mock import MagicMock

_UNSET = set()


def stub_global(rules: Dict[str, Any]):
    """Applies stubs globally (not in fixture).

    Useful in root conftest.py to patch dependencies before tests run.

    :param rules:

    """
    proxy = StubProxy()
    proxy.apply(rules=rules)


class StubProxy:

    def __init__(self):
        self._modules = sys.modules
        self._overridden = {}

    def _set(self, path: str, attrs: Union[Dict[str, Any], Any]):

        modules = self._modules
        overridden = self._overridden

        if not isinstance(attrs, dict):  # actual value
            try:
                path, attr = path.rsplit('.', 1)

            except ValueError:
                attr = '__module__'

            attrs = {attr: attrs}

        path = str(path)

        val_current = getattr(modules, path, _UNSET)

        if path not in overridden:
            overridden[path] = val_current

        modules[path] = Stub(path, attrs=attrs or {})

    def apply(self, rules: Dict[str, Any]):
        """Apply stubbing rules.

        :param rules:

        """
        for path, attrs in rules.items():
            self._set(path, attrs)

    def restore_initial(self):
        """Restore initial modules."""

        modules = self._modules
        unset = _UNSET

        for key, val in self._overridden.items():

            if val is unset:
                # wipe
                del modules[key]

            else:
                # restore
                modules[key] = val


class Stub:

    def __init__(self, path: str, attrs: Dict[str, Any]):
        self.path = path
        self.attrs = attrs

    def __getattr__(self, name: str):
        attr = self.attrs.get(name, None)

        if attr is None:
            module_mock = self.attrs.get('__module__')

            if module_mock is not None:
                attr = module_mock

            else:
                raise AttributeError('Path %s contains no %s attribute' % (self.path, name))

        if attr == '[cls]':
            return type(str('%sStub' % name), (object,), {})

        elif attr == '[func]':
            return lambda *args, **kwargs: None

        elif attr == '[mock]':
            return MagicMock()

        elif attr == '[mock_persist]':
            mock = MagicMock()
            self.attrs[name] = mock
            return mock

        return attr
