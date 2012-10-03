import sqlalchemy as sa
from sqlalchemy_test import ModelTestCase
from tests import Address
from tests import CustomType


class TestAddress(ModelTestCase):
    model = Address

    def test_has_id(self):
        self.assert_has('id')

    def test_id_is_integer(self):
        self.assert_type('id', sa.Integer)

    def test_id_is_not_nullable(self):
        self.assert_not_nullable('id')

    def test_id_is_primary_key(self):
        self.assert_primary_key('id')

    def test_has_name(self):
        self.assert_has('name')

    def test_name_is_customtype(self):
        self.assert_type('name', CustomType)

    def test_name_is_nullable(self):
        self.assert_nullable('name')

