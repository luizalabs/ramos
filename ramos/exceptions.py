# -*- coding: utf-8 -*-
class InvalidBackendError(Exception):
    """
    InvalidBackendError is raised when instances of BackendPool
    can't get a backend implementation
    """

    def __init__(self, backend_type, backend_id, available_backends):
        self.backend_type = backend_type
        self.backend_id = backend_id
        self.available_backends = available_backends
        self.error_message = u'Invalid {} backend: {}'.format(
            self.backend_type, self.backend_id
        )

        super(InvalidBackendError, self).__init__(
            self.backend_type,
            self.backend_id,
            self.error_message,
            self.available_backends,
        )
