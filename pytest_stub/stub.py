# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from .utils import StubProxy


@pytest.fixture
def stub():
    """Fixture allowing to temporarily override stub packages, modules and attributes.

    Example::

        def test_django_related(stub):

            stub.apply({
                'django.core.management.call_command': '[func]',
                'django.core.management.base.BaseCommand': '[cls]',
                'django.sub': {
                    'settings': object(),
                    'some': True,
                }
            })

    :rtype: SettingsProxy

    """
    proxy = StubProxy()

    yield proxy

    proxy.restore_initial()
