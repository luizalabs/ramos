# -*- coding: utf-8 -*-
import pytest
from mock import Mock, patch

from ramos.compat import configure, get_installed_pools, import_string

try:
    from importlib import reload
except ImportError:
    pass


def assert_pools_is_equals_settings(pools, modules):
    with patch.dict('sys.modules', modules):
        from ramos import compat

        reload(compat)

        assert get_installed_pools() == pools


class TestImportString(object):

    def test_should_raise_exception_when_path_has_no_dot(self):
        with pytest.raises(ImportError):
            import_string('no_dots_in_path')

    def test_should_raise_exceptions_when_module_has_no_attribute(self):
        with pytest.raises(ImportError) as exc:
            import_string('ramos.unexistent')

            message = 'Module "ramos" does not define a "unexistent" attribute'
            assert exc == message

    def test_should_import_module(self):
        cls = import_string('ramos.compat.import_string')

        assert cls == import_string


class TestConfiguration:

    def test_should_configure_pools(self):
        pools = {
            'backend_a': [
                'path.to.backend'
            ],
            'backend_b': [
                'path.to.backend'
            ]
        }

        configure(pools=pools)

        assert get_installed_pools() == pools

    def test_should_configure_pools_from_django_settings(self):
        pools = {
            'backend-from-django-settings': [
                'path.to.backend'
            ]
        }

        django = Mock()
        django.conf.settings.POOL_OF_RAMOS = pools

        assert_pools_is_equals_settings(
            pools=pools,
            modules={
                'django': django,
                'django.conf': django.conf,
                'simple_settings': None
            }
        )

    def test_should_configure_pools_from_simple_settings(self):
        pools = {
            'backend-from-simple-settings': [
                'path.to.backend'
            ]
        }

        simple_settings = Mock()
        simple_settings.settings.POOL_OF_RAMOS = pools

        assert_pools_is_equals_settings(
            pools=pools,
            modules={
                'django': None,
                'django.conf': None,
                'simple_settings': simple_settings
            }
        )
