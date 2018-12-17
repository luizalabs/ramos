Settings
--------

In orther to locate backends, **Ramos** needs to know where to look for
and which pools can use which classes.


`ramos.configure`
-----------------

Out-of-the-box **Ramos** can use the `configure` method to setup the
path and type of all backends available.

#### arguments

`pools` - A dictionary with the backend type as a key and a list of
available backend paths as value. The list of backends given will be
available for the [BackendPool][backend_pool] with the `backend_type`
given in the key.

#### example

```python
import ramos

ramos.configure(pools={
    'print': [
        'path.to.backend_a',
        'path.to.backend_b',
    ]
})
```

Django Settings
---------------

If you are using [Django][https://www.djangoproject.com/], you can use a
variable `POLL_OF_RAMOS` in your settings file instead of `ramos.configure`.

#### example
```python
# settings.py

POOL_OF_RAMOS = {
    'backend_type': [
        'path.to.backend_a',
        'path.to.backend_b',
    ]
}
```

Simple Settings
---------------

**Ramos** also supports [Simple Settings](https://github.com/drgarcia1986/simple-settings)
which can setup a `POLL_OF_RAMOS` variable, like Django's settings.
