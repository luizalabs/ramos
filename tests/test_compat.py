# -*- coding: utf-8 -*-
import pytest

from ramos.compat import import_string


class TestImportString(object):

    def test_should_raise_exception_when_path_has_no_dot(self):
        with pytest.raises(ImportError):
            import_string('no_dots_in_path')

    def test_should_raise_exceptions_when_module_has_no_attribute(self):
        with pytest.raises(ImportError) as exc:
            import_string('ramos.unexistent')

            message = 'Module "ramos" does not define a "unexistent" attribute'
            assert exc == message

    def test_should_import_module(self):
        cls = import_string('ramos.compat.import_string')

        assert cls == import_string
