# -*- coding: utf-8 -*-

from .exceptions import MisconfiguredBackendError


class ThreadSafeCreateMixin(object):
    """
    ThreadSafeCreateMixin can be used as an inheritance
    of thread safe backend implementations
    """

    @classmethod
    def create(cls, *args, **kwargs):
        """
        Return always a new instance of the backend class
        """
        return cls(*args, **kwargs)


class SingletonCreateMixin(object):
    """
    SingletonCreateMixin can be used as an inheritance
    of singleton backend implementations
    """

    _instances = {}

    @classmethod
    def create(cls, *args, **kwargs):
        """
        Return always the same instance of the backend class
        """
        if args or kwargs:
            raise MisconfiguredBackendError(
                "Singletons can't be initialized with extra arguments"
            )

        if cls not in cls._instances:
            cls._instances[cls] = cls()

        return cls._instances[cls]
