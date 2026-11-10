from typing import Generator

import pytest

from .utils import StubProxy


@pytest.fixture
def stub() -> Generator[StubProxy, None, None]:
    """Fixture allowing to temporarily override stub packages, modules and attributes.

    Example::

        def test_django_related(stub):

            stub.apply({
                'cv2': '[mock]',
                'django.dummy': '[mock]',
                'django.core.management.call_command': '[func]',
                'django.core.management.base.BaseCommand': '[cls]',
                'django.conf': {
                    'settings': object(),
                    'some': True,
                }
            })

    """
    proxy = StubProxy()

    yield proxy

    proxy.restore_initial()
