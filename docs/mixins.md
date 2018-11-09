Mixins
======

As every backend needs a way to create itself, the `ramos.mixins` module
provides mixin classes for this task which might be repetitive otherwise.

Usage
-----

```python
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

Then inherited class will return always the same instance of the backend in
every call of `create`.


ThreadSafeCreateMixin
---------------------

The inherited class will return a new instance of itself in every call of
`create`.
