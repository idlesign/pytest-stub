import sys
from unittest.mock import MagicMock


def test_basic(stub):

    from pytest_stub.utils import Stub

    class Settings(object):
        pass

    modules = sys.modules

    assert 'django.core.management.call_command' not in modules
    assert 'django.core.management.base.BaseCommand' not in modules
    assert 'django.conf.settings' not in modules

    stub.apply({
        'virtualfakedlib': '[mock]',
        'django.faked': '[mock]',
        'django.core.management.call_command': '[func]',
        'django.core.management.base.BaseCommand': '[cls]',
        'django.conf': {
            'settings': Settings(),
            'some': True,
        }
    })
    
    assert isinstance(modules['django.core.management'], Stub)
    assert isinstance(modules['django.core.management.base'], Stub)
    assert isinstance(modules['django.conf'], Stub)

    assert 'django.core.management' in modules
    assert 'django.core.management.base' in modules
    assert 'django.conf' in modules

    from django.conf import settings, some
    from django.core.management import call_command
    from django.core.management.base import BaseCommand

    assert some
    assert isinstance(settings, Settings)
    assert callable(call_command)
    assert isinstance(BaseCommand, object)

    # Test mocking.
    from django import faked
    faked.dummy = 1
    assert faked.dummy == 1

    # Test entire module stub.
    import virtualfakedlib as vl
    some = vl.virtual
    assert isinstance(some, MagicMock)
