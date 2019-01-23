# -*- coding: utf-8 -*-
import pytest

from ramos.exceptions import MisconfiguredBackendError
from ramos.mixins import SingletonCreateMixin, ThreadSafeCreateMixin


class SingletonDerived(SingletonCreateMixin):
    pass


class AnotherSingletonDerived(SingletonCreateMixin):
    pass


class BackendWithInit(ThreadSafeCreateMixin):
    def __init__(self, a, b):
        self.a = a
        self.b = b


class TestSingletonCreateMixin(object):

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

    def test_create_singleton_with_custom_parameters_should_raise_error(self):
        with pytest.raises(MisconfiguredBackendError):
            SingletonDerived.create(1)

        with pytest.raises(MisconfiguredBackendError):
            SingletonDerived.create(a=2)

        with pytest.raises(MisconfiguredBackendError):
            SingletonDerived.create(3, b=4)


class TestThreadSafeCreateMixin(object):

    def test_create_should_return_a_new_instance(self):
        instance_1 = ThreadSafeCreateMixin.create()
        instance_2 = ThreadSafeCreateMixin.create()

        assert instance_1
        assert instance_2
        assert instance_1 is not instance_2

    def test_create_with_parameters_forwards_arguments(self):
        instance = BackendWithInit.create(a=2, b=3)

        assert instance.a == 2
        assert instance.b == 3
