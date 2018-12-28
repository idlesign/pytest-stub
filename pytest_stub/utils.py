# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys

_UNSET = set()


class StubProxy(object):

    def __init__(self):
        self._moules = sys.modules
        self._overridden = {}

    def _set(self, path, attrs):

        modules = self._moules
        overridden = self._overridden

        if not isinstance(attrs, dict):  # actual value
            path, attr = path.rsplit('.', 1)
            attrs = {attr: attrs}

        path = str(path)

        val_current = getattr(modules, path, _UNSET)

        if path not in overridden:
            overridden[path] = val_current

        modules[path] = Stub(path, attrs=attrs or {})

    def apply(self, rules):
        """Apply stubbing rules.

        :param dict rules:

        """
        for path, attrs in rules.items():
            self._set(path, attrs)

    def restore_initial(self):
        """Restore initial modules."""

        modules = self._moules
        unset = _UNSET

        for key, val in self._overridden.items():

            if val is unset:
                # wipe
                del modules[key]

            else:
                # restore
                modules[key] = val


class Stub(object):

    def __init__(self, path, attrs):
        self.path = path
        self.attrs = attrs

    def __getattr__(self, name):
        attr = self.attrs.get(name, None)

        if attr is None:
            raise AttributeError('Path %s contain no %s attribute' % (self.path, name))

        if attr == '[cls]':
            return type(str('%sStub' % name), (object,), {})

        elif attr == '[func]':
            return lambda *args, **kwargs: None

        return attr
