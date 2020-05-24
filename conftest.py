import pytest

POOL_OF_RAMOS = {'backend_type': ['path.to.backend']}


_SETTINGS = None


@pytest.fixture(autouse=True)
def reset_pools():
    import ramos

    ramos.configure(pools=POOL_OF_RAMOS)


@pytest.fixture(autouse=True)
def reset_settings():
    if _SETTINGS:
        try:
            _SETTINGS.configure(POOL_OF_RAMOS=POOL_OF_RAMOS)
        except RuntimeError:
            _SETTINGS.POOL_OF_RAMOS = POOL_OF_RAMOS


@pytest.fixture
def settings():
    if _SETTINGS is None:
        pytest.skip('The django or simple_settings are not installed.')

    return _SETTINGS


def pytest_configure():
    global _SETTINGS

    try:
        import django
        from django.conf import settings

        settings.configure(POOL_OF_RAMOS=POOL_OF_RAMOS)
        django.setup()

        _SETTINGS = settings
    except ImportError:
        try:
            import os

            os.environ.setdefault('SIMPLE_SETTINGS', 'conftest')

            from simple_settings import settings

            settings.configure(POOL_OF_RAMOS=POOL_OF_RAMOS)

            _SETTINGS = settings
        except ImportError:
            import ramos

            ramos.configure(pools=POOL_OF_RAMOS)
