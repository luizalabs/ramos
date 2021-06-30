Backend Mixins
==============

As every backend needs a way to create itself, the `ramos.mixins` module
provides mixin classes for this task which might be repetitive otherwise.

Usage
-----

```python
from ramos.mixins import SingletonCreateMixin

class BaseBackend:

    def do_something(self):
        pass


class MyBackend(SingletonCreateMixin, BaseBackend):

    def do_something(self):
        # do something else
        pass


backend = MyBackend.create()
other = MyBackend.create()

assert backend is other  # True
```


SingletonCreateMixin
--------------------

The inherited class will return always the same instance of the backend in
every call of `create`.

**caveat**: When `SingletonCreateMixin` is used with args and kwargs,
every backend of the same type should use it as well, so that the backend pool
can create every backend instance using the exact same parameters. The args and kwargs
will be concatenated with class path and qualifier name to generate a unique identifier
to be used to find the instances previously created.


ThreadSafeCreateMixin
---------------------

The inherited class will return a new instance of itself in every call of
`create`.

**caveat**: When `ThreadSafeCreateMixin` is used with args and kwargs,
every backend of the same type should use it as well, so that the backend pool
can create every backend instance using the exact same parameters.


Pool Mixins
===========

DefaultBackendMixin
-------------------

The inherited class will have the option to return a default backend based on
the `SETTINGS_KEY` value that will exist in your `settings`.

```python
from ramos.mixins import DefaultBackendMixin
from ramos.pool import BackendPool

class MyBackendPool(DefaultBackendMixin, BackendPool):
    SETTINGS_KEY = 'DEFAULT_BACKEND_ID'

backend = MyBackendPool.get_default()
assert backend.id == 'DEFAULT_BACKEND_ID'
```
