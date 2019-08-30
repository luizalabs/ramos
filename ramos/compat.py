import threading

settings = None  # noqa
try:
    from django.conf import settings
except ImportError:
    try:
        from simple_settings import settings
    except ImportError:
        settings = threading.local()
        settings.POOL_OF_RAMOS = {}


def get_installed_pools():
    return settings.POOL_OF_RAMOS


def configure(pools):
    try:
        settings.configure(POOL_OF_RAMOS=pools)
    except (AttributeError, RuntimeError):
        settings.POOL_OF_RAMOS = dict(pools)


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
