# -*- coding: utf-8 -*-
from django_ramos.mixins import SingletonCreateMixin, ThreadSafeCreateMixin


class SingletonDerived(SingletonCreateMixin):
    pass


class AnotherSingletonDerived(SingletonCreateMixin):
    pass


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


class TestThreadSafeCreateMixin(object):

    def test_create_should_return_a_new_instance(self):
        instance_1 = ThreadSafeCreateMixin.create()
        instance_2 = ThreadSafeCreateMixin.create()

        assert instance_1
        assert instance_2
        assert instance_1 is not instance_2
