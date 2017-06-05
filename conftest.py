# -*- coding: utf-8 -*-

POOL_OF_RAMOS = {
    'backend_type': [
        'path.to.backend'
    ]
}


def pytest_configure():
    """ pytest setup. """
    try:
        import django
        from django.conf import settings

        settings.configure(
            POOL_OF_RAMOS=POOL_OF_RAMOS
        )

        django.setup()
    except ImportError:
        from simple_settings.core import LazySettings
        settings = LazySettings('conftest')
        settings.configure()
