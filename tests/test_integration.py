import pytest

from ramos.compat import get_installed_pools

skip_django = False
try:
    import django  # noqa
except ImportError:
    skip_django = True

skip_simple_settings = False
try:
    from simple_settings.utils import settings_stub
except ImportError:
    skip_simple_settings = True


@pytest.mark.skipif(skip_django, reason='The django is not installed')
def test_should_configure_if_django_settings_is_installed(settings):
    settings.POOL_OF_RAMOS = {
        'backend_a': [
            'path.to.backend'
        ],
        'backend_b': [
            'path.to.backend'
        ],
    }

    assert get_installed_pools() == settings.POOL_OF_RAMOS


@pytest.mark.skipif(
    skip_simple_settings,
    reason='The simple_settings is not installed'
)
def test_should_configure_if_simple_settings_is_installed():
    POOL_OF_RAMOS = {
        'backend_a': [
            'path.to.backend'
        ],
        'backend_b': [
            'path.to.backend'
        ],
    }

    assert get_installed_pools() != POOL_OF_RAMOS
    with settings_stub(POOL_OF_RAMOS=POOL_OF_RAMOS):
        assert get_installed_pools() == POOL_OF_RAMOS
