# -*- coding: utf-8 -*-

from .compat import settings


class ThreadSafeCreateMixin(object):
    """
    ThreadSafeCreateMixin can be used as an inheritance
    of thread safe backend implementations
    """

    @classmethod
    def create(cls):
        """
        Return always a new instance of the backend class
        """
        return cls()


class SingletonCreateMixin(object):
    """
    SingletonCreateMixin can be used as an inheritance
    of singleton backend implementations
    """

    _instances = {}

    @classmethod
    def create(cls):
        """
        Return always the same instance of the backend class
        """
        if cls not in cls._instances:
            cls._instances[cls] = cls()

        return cls._instances[cls]


class DefaultBackendMixin(object):
    """
    Creates the method 'get_default' that will return the backend with the
    `SETTINGS_KEY` key value
    """
    SETTINGS_KEY = None

    @classmethod
    def get_default(cls):
        if cls.SETTINGS_KEY is None:
            raise AttributeError(
                'You must set a `SETTINGS_KEY` to the Pool.'
            )

        try:
            backend_id = getattr(settings, cls.SETTINGS_KEY)
        except AttributeError:
            raise AttributeError(
                'Key {key} not found on settings.'.format(key=cls.SETTINGS_KEY)
            )

        return cls.get(backend_id=backend_id)
