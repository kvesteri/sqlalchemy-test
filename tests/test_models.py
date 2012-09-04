from pytest import raises
import sqlalchemy as sa
from sqlalchemy_test import ModelTestCase, generate_test_case
from tests import Entity, User


class TestEntity(ModelTestCase):
    model = Entity

    def test_name_is_not_nullable(self):
        self.assert_not_nullable('name')

    def test_has_name(self):
        self.assert_has('name')

    def test_assert_primary_key(self):
        self.assert_primary_key('id')

    def test_assert_autoincrement(self):
        self.assert_autoincrement('id')


class TestUser(TestEntity):
    model = User

    def test_assert_table_name(self):
        self.assert_table_name('user')

    def test_assert_name_is_nullable(self):
        self.assert_nullable('age')

    def test_assert_length(self):
        self.assert_length('description', 255)

    def test_assert_has_for_existing_column(self):
        self.assert_has('age')

    def test_assert_default(self):
        self.assert_default('is_active', False)

    def test_assert_has_for_non_existing_column_raises_exception(self):
        with raises(AssertionError):
            self.assert_has('unknown_column')

    def test_assert_type(self):
        self.assert_type('age', sa.Integer)

    def test_assert_unique(self):
        self.assert_unique('email')

    def test_assert_index(self):
        self.assert_index('age')


class TestTestCaseGeneration(object):
    def test_something(self):
        generate_test_case(User, 'tests/')
