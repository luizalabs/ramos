import abc

from .compat import ImproperlyConfigured, get_installed_pools, import_string
from .exceptions import InvalidBackendError


class AbstractPool(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def classes_iterator(cls):
        ...

    @classmethod
    def get(cls, backend_id, *args, **kwargs):
        """
        Return an instance of backend type
        """
        backend_class = cls.get_class(backend_id)
        return backend_class.create(*args, **kwargs)

    @classmethod
    def all(cls, *args, **kwargs):
        """
        Return a list of instances of backend type
        """
        return list(cls.iterator(*args, **kwargs))

    @classmethod
    def get_class(cls, backend_id):
        """
        Return a class of backend type
        """
        for backend_class in cls.classes_iterator():
            if backend_class.id == backend_id:
                return backend_class

        raise InvalidBackendError(
            cls.backend_type,
            backend_id,
            get_installed_pools()[cls.backend_type]
        )

    @classmethod
    def all_classes(cls):
        """
        Return a list of class of backend type
        """
        return list(cls.classes_iterator())

    @classmethod
    def iterator(cls, *args, **kwargs):
        """
        Return an iterator of instances of backend type
        """
        return (
            backend_class.create(*args, **kwargs)
            for backend_class in cls.classes_iterator()
        )


class BackendPool(AbstractPool):
    """
    BackendPool is an interface to get instances of backend types
    """

    backend_type = None

    @classmethod
    def classes_iterator(cls):
        """
        Return an iterator with all classed of backend type
        """
        try:
            backend_list = get_installed_pools()[cls.backend_type]
        except KeyError:
            raise ImproperlyConfigured(
                u'Backend type "{}" config not found'.format(cls.backend_type)
            )

        return (
            import_string(backend_path)
            for backend_path in backend_list
        )


class IndependentPool(AbstractPool):
    """
    The independent pool allows you to configure through the `backends`
    property, without having to run ramos.configure() or install in your
    settings (django.conf.settings or simple_settings).

    Example:

        caches
          |___ pool.py
          |___ backends
            |____ file.py
            |____ locmem.py
            |____ redis.py

        >>> from ramos.pool import IndendentPool
        >>> from caches.backends.locmem import LocmemBackend

        >>> class CachePool(IndependentPool):
        >>>     backends = [
        >>>         LocmemBackend,
        >>>         'caches.backends.file.FileCacheBackend',
        >>>         'caches.backends.redis.RedisCacheBackend',
        >>>     ]

        >>> CachePool.get('locmem')

        OR

        >>> CachePool.get('redis')

        This always return backends instances
    """

    backends = []

    @classmethod
    def classes_iterator(cls):
        """
        Return an iterator with all classed of backends in this pool
        """
        for backend in cls.backends:
            if isinstance(backend, str):
                yield import_string(backend)
            else:
                yield backend
