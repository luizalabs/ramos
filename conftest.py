# -*- coding: utf-8 -*-
def pytest_configure():
    """ pytest setup. """

    import django
    from django.conf import settings

    settings.configure(
        DEBUG=False,
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
            }
        },
        SECRET_KEY='fake',
        USE_I18N=True,
        USE_L10N=True,
        STATIC_URL='/static/',
        MIDDLEWARE_CLASSES=(
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
        ),
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
        ),
        CACHES={
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
            }
        },
        POOL_OF_RAMOS={
            'backend_type': [
                'path.to.backend'
            ]
        }
    )

    if django.get_version() >= '1.7':
        django.setup()
