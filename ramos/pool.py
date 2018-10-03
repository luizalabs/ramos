# -*- coding: utf-8 -*-

from .compat import ImproperlyConfigured, get_installed_pools, import_string
from .exceptions import InvalidBackendError


class BackendPool(object):
    """
    BackendPool is an interface to get instances of backend types
    """

    backend_type = None

    @classmethod
    def get(cls, backend_id):
        """
        Return an instance of backend type
        """

        for backend_class in cls._get_backends_classes():
            if backend_class.id == backend_id:
                return backend_class.create()

        raise InvalidBackendError(
            cls.backend_type,
            backend_id,
            get_installed_pools()[cls.backend_type]
        )

    @classmethod
    def all(cls):
        """
        Return a list of instances of backend type
        """

        return [
            backend_class.create()
            for backend_class in cls._get_backends_classes()
        ]

    @classmethod
    def _get_backends_classes(cls):
        try:
            backend_list = get_installed_pools()[cls.backend_type]
        except KeyError:
            raise ImproperlyConfigured(
                u'Backend type "{}" config not found'.format(cls.backend_type)
            )

        return [
            cls._get_backend_class(backend_path)
            for backend_path in backend_list
        ]

    @classmethod
    def _get_backend_class(cls, backend_path):
        backend_class = import_string(backend_path)

        return backend_class
