# -*- coding: utf-8 -*-


class ThreadSafeCreateMixin(object):

    @classmethod
    def create(cls):
        return cls()


class SingletonCreateMixin(object):
    _instances = {}

    @classmethod
    def create(cls):
        if cls not in cls._instances:
            cls._instances[cls] = cls()

        return cls._instances[cls]
