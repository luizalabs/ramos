from unittest.mock import Mock, patch

import pytest

from ramos.mixins import (
    DefaultBackendMixin,
    SingletonCreateMixin,
    ThreadSafeCreateMixin
)


class SingletonDerived(SingletonCreateMixin):
    pass


class AnotherSingletonDerived(SingletonCreateMixin):
    pass


class TestSingletonCreateMixin:

    def setup(self):
        SingletonCreateMixin._instances = {}
        AnotherSingletonDerived._instances = {}
        SingletonDerived._instances = {}

    def test_create_should_return_the_same_instance(self):
        assert SingletonDerived.create()
        assert SingletonDerived.create() is SingletonDerived.create()

    def test_singleton_instance_should_be_different_for_child_classes_defined_after_instance_creation(  # noqa
        self
    ):
        instance_base = SingletonCreateMixin.create()

        class DynamicDerived(SingletonCreateMixin):
            pass

        instance_child = DynamicDerived.create()

        assert instance_base is not instance_child

    def test_create_should_return_different_instances_for_different_classes(
        self
    ):
        assert (
            AnotherSingletonDerived.create() is not SingletonDerived.create()
        )


class TestThreadSafeCreateMixin:

    def test_create_should_return_a_new_instance(self):
        instance_1 = ThreadSafeCreateMixin.create()
        instance_2 = ThreadSafeCreateMixin.create()

        assert instance_1
        assert instance_2
        assert instance_1 is not instance_2

    def test_create_should_pass_args_to_create_a_new_instance(self):
        class Fake(ThreadSafeCreateMixin):
            def __init__(self, arg1, arg2, arg3):
                self.arg1 = arg1
                self.arg2 = arg2
                self.arg3 = arg3

        instance = Fake.create(1, 2, arg3=3)

        assert instance.arg1 == 1
        assert instance.arg2 == 2
        assert instance.arg3 == 3


class TestDefaultBackendMixin:

    @pytest.fixture
    def backend_id(self):
        return 'my-backend-id'

    @pytest.fixture
    def mocked_settings(self, backend_id):
        with patch('ramos.mixins.settings') as mocked_settings:
            settings_obj = Mock()
            settings_obj.DEFAULT_BACKEND_ID = backend_id

            mocked_settings.return_value = settings_obj

            yield mocked_settings

    def test_should_raise_attribute_error_if_settings_key_is_none(self):
        with pytest.raises(AttributeError):
            DefaultBackendMixin.get_default()

    def test_should_raise_attribute_error_if_key_not_found_on_settings(self):
        invalid_key = 'four-o-four'
        mixin_class = DefaultBackendMixin
        mixin_class.SETTINGS_KEY = invalid_key

        with pytest.raises(AttributeError) as exc:
            mixin_class.get_default()

        assert invalid_key in str(exc.value)

    def test_should_call_get_with_correct_backend_id(
        self,
        mocked_settings,
        backend_id
    ):
        mixin_class = DefaultBackendMixin
        mixin_class.SETTINGS_KEY = backend_id
        mixin_class.get = None

        with patch.object(mixin_class, 'get') as mocked_class:
            mixin_class.get_default()

        assert mocked_class.get.called_with('backend_id')
