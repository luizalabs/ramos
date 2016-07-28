# -*- coding: utf-8 -*-


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
