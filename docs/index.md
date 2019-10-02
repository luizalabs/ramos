Ramos - Generic Backend Pool
============================

**Ramos** is a library to create, locate, instantiate and control the lifecyle of
generic _backends_.


What is a backend?
------------------

_Plugable Backend_ (or _backend_ for short) is a term [borrowed from Django](http://charlesleifer.com/blog/django-patterns-pluggable-backends/).
It is a standard interface to a resource, so that it can be _plugged_ at the
developer's will. In order to instantiate a backend, **Ramos** requires the
class to have a _classmethod_ `create`, which usually does not accept any parameter
([but it can, if you need](mixins.md#ThreadSafeCreateMixin)) and must return
your backend's instance. **Ramos** does not verify if the classes configured
in a backend type really have a common interface, it is up to you
([Abstract Base Classes](https://docs.python.org/3/library/abc.html) can help).


Installation
------------

install using `pip`.
```
pip install ramos
```

Example
-------

This is a quick step-by-step example of what you can do with **Ramos**. We will
create 2 simple and interchangeable backends which only print a greeting.

Create the backends.
```python
class PrintHiBackend:

    id = 'hi'

    @classmethod
    def create(cls):
        return cls()

    def print(self):
        print('hi')


class PrintByeBackend:

    id = 'bye'

    @classmethod
    def create(cls):
        return cls()

    def print(self):
        print('bye')
```

Setup the path for your backends.
```python
import ramos

ramos.configure(pools={
    'print': (
        '__main__.PrintHiBackend',
        '__main__.PrintByeBackend',
    )
})
```

Setup the backend pool to load your backends.
```python
from ramos.pool import BackendPool

class PrintBackendPool(BackendPool):
    backend_type = 'print'
```

Instantiate the pool and use your backends!
```python
pool = PrintBackendPool()

# iterate over all of them
for backend in pool.all():
    backend.print()

# get a backend by id
backend = pool.get('bye')
backend.print()
```

See also
--------

* [Mixins](mixins)
* [Backend Pool](backend_pool)
* [Settings](settings)
