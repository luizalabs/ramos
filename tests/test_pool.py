# -*- coding: utf-8 -*-
import pytest

from ramos import configure
from ramos.compat import ImproperlyConfigured
from ramos.exceptions import InvalidBackendError
from ramos.mixins import ThreadSafeCreateMixin
from ramos.pool import BackendPool


class FakeABCBackend(ThreadSafeCreateMixin):
    id = 'fake_abc'


class FakeXYZBackend(ThreadSafeCreateMixin):
    id = 'fake_xyz'


class TestBackendPool(object):

    def test_get_backends_should_return_all_backends_instances(self):
        configure(pools={
            BackendPool.backend_type: (
                u'{module}.{cls}'.format(
                    module=__name__,
                    cls=FakeXYZBackend.__name__
                ),
                u'{module}.{cls}'.format(
                    module=__name__,
                    cls=FakeABCBackend.__name__
                ),
            )
        })

        backends = BackendPool.all()

        assert isinstance(backends[0], FakeXYZBackend)
        assert isinstance(backends[1], FakeABCBackend)

    def test_get_backends_without_config_should_raise(self):
        configure(pools={})

        with pytest.raises(ImproperlyConfigured):
            BackendPool.all()

    def test_get_backends_with_zero_backends_should_return_empty_list(self):
        configure(pools={
            BackendPool.backend_type: {}
        })

        assert BackendPool.all() == []

    def test_get_should_return_the_backend_instance(self):
        configure(pools={
            BackendPool.backend_type: (
                u'{module}.{cls}'.format(
                    module=__name__,
                    cls=FakeXYZBackend.__name__
                ),
                u'{module}.{cls}'.format(
                    module=__name__,
                    cls=FakeABCBackend.__name__
                ),
            )
        })

        backend = BackendPool.get('fake_abc')

        assert isinstance(backend, FakeABCBackend)

    def test_get_with_nonexistent_backend_should_raise(self):
        configure(pools={
            BackendPool.backend_type: (
                u'{module}.{cls}'.format(
                    module=__name__,
                    cls=FakeXYZBackend.__name__
                ),
                u'{module}.{cls}'.format(
                    module=__name__,
                    cls=FakeABCBackend.__name__
                ),
            )
        })

        with pytest.raises(InvalidBackendError):
            BackendPool.get('fake_fake')
