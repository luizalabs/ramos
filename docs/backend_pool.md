Backend Pool
============

The `BackendPool` is the component which locates and instantiates your _backend_
classes. In orther to use it you should subclass it and set a `backend_type`.
(see [the example](/#example))

`BackendPool` class
-------------------

### `get`

Returns returns an instance of the backend which has the given `backend_id`

#### arguments

`backend_id` - The `id` of the backend you are looking for


### `all`

Returns a list of instances of all backends configured with the pool's backend
type
