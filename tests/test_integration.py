from ramos.compat import get_installed_pools

try:
    from importlib import reload
except ImportError:
    pass


def test_should_configure_if_settings(settings):
    settings.POOL_OF_RAMOS = {
        'backend_a': [
            'path.to.backend'
        ],
        'backend_b': [
            'path.to.backend'
        ],
    }

    from ramos import compat

    reload(compat)

    assert get_installed_pools() == settings.POOL_OF_RAMOS
