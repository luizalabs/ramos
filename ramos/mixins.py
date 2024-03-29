from .compat import settings


class ThreadSafeCreateMixin:
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


class SingletonCreateMixin:
    """
    SingletonCreateMixin can be used as an inheritance
    of singleton backend implementations
    """

    _instances = {}

    @classmethod
    def _get_instance_key(cls, *args, **kwargs):
        class_path = f'{cls.__module__}.{cls.__qualname__}'
        kwargs_tuple = tuple(sorted(kwargs.items()))

        return f'{class_path}|{hash(args)}|{hash(kwargs_tuple)}'

    @classmethod
    def create(cls, *args, **kwargs):
        """
        Return always the same instance of the backend class
        """
        key = cls._get_instance_key(*args, **kwargs)

        if key not in cls._instances:
            cls._instances[key] = cls(*args, **kwargs)

        return cls._instances[key]


class DefaultBackendMixin:
    """
    Creates the method 'get_default' that will return the backend with the
    `SETTINGS_KEY` key value
    """

    SETTINGS_KEY = None

    @classmethod
    def get_default(cls):
        if cls.SETTINGS_KEY is None:
            raise AttributeError('You must set a `SETTINGS_KEY` to the Pool.')

        try:
            backend_id = getattr(settings, cls.SETTINGS_KEY)
        except AttributeError:
            raise AttributeError(
                'Key {key} not found on settings.'.format(key=cls.SETTINGS_KEY)
            )

        return cls.get(backend_id=backend_id)
