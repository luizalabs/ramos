Ramos
=====

.. image:: https://readthedocs.org/projects/ramos/badge/?version=latest&style=flat
    :target: https://ramos.readthedocs.io/en/latest/

.. image:: https://travis-ci.org/luizalabs/ramos.svg?branch=master
    :target: https://travis-ci.org/luizalabs/ramos

.. image:: https://codecov.io/gh/luizalabs/ramos/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/luizalabs/ramos


Generic backend pool


Setup
-----

.. code:: bash

    pip install ramos


Development setup
-----------------

.. code:: bash

    make install


Usage
-----

.. code:: python

    import ramos

    ramos.configure(pools={
        'backend_type': [
            'path.to.backend_a',
            'path.to.backend_b',
        ]
    })


Integrations
~~~~~~~~~~~~

Ramos can uses `Django`_ or `Simple Settings`_ to get backends
configurations if set settings.POOL_OF_RAMOS:

.. code:: python

    POOL_OF_RAMOS = {
        'backend_type': [
            'path.to.backend_a',
            'path.to.backend_b',
        ]
    }


Backend Implementations
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from ramos.mixins import ThreadSafeCreateMixin


    class BackendA(ThreadSafeCreateMixin):
        id = 'backend_a'
        def say(self):
            return 'A'


    class BackendB(ThreadSafeCreateMixin):
        id = 'backend_b'
        def say(self):
            return 'B'


Backend Pool
~~~~~~~~~~~~

.. code:: python

    from ramos.pool import BackendPool


    class BackendTypePool(BackendPool)
        backend_type = 'backend_type'


    backends = BackendTypePool.all()

    for backend in backends:
        print(backend.say())


    # backend_a = BackendTypePool.get('backend_a')
    # backend_b = BackendTypePool.get('backend_b')

.. _Django: https://github.com/django/django
.. _Simple Settings: https://github.com/drgarcia1986/simple-settings
