import threading

_tls = threading.local()

_tls.INSTALLED_POOLS = {}


def configure(pools):
    _tls.INSTALLED_POOLS = dict(pools)


def get_installed_pools():
    return _tls.INSTALLED_POOLS


try:
    from django.conf import settings
    configure(pools=settings.POOL_OF_RAMOS)
except ImportError:
    try:
        from simple_settings import settings
        configure(pools=settings.POOL_OF_RAMOS)
    except ImportError:
        pass


try:
    from django.core.exceptions import ImproperlyConfigured
except ImportError:
    class ImproperlyConfigured(Exception):
        pass


try:
    from django.utils.module_loading import import_string
except ImportError:
    from importlib import import_module

    def import_string(dotted_path):
        """
        Import a dotted module path and return the attribute/class designated
        by the last name in the path. Raise ImportError if the import failed.
        """

        try:
            module_path, class_name = dotted_path.rsplit('.', 1)
        except ValueError:
            raise ImportError(
                "{} doesn't look like a module path".format(
                    dotted_path
                )
            )

        module = import_module(module_path)

        try:
            return getattr(module, class_name)
        except AttributeError:
            raise ImportError(
                'Module "{}" does not define a "{}" attribute/class'.format(
                    module_path,
                    class_name
                )
            )
