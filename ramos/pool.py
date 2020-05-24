from .compat import ImproperlyConfigured, get_installed_pools, import_string
from .exceptions import InvalidBackendError


class BackendPool:
    """
    BackendPool is an interface to get instances of backend types
    """

    backend_type = None

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
            get_installed_pools()[cls.backend_type],
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

    @classmethod
    def classes_iterator(cls):
        """
        Return an iterator with all classed of backend type
        """
        try:
            backend_list = get_installed_pools()[cls.backend_type]
        except KeyError:
            raise ImproperlyConfigured(
                'Backend type "{}" config not found'.format(cls.backend_type)
            )

        return (import_string(backend_path) for backend_path in backend_list)
