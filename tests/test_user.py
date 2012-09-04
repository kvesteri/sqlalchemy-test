import sqlalchemy as sa
from sqlalchemy_test import ModelTestCase
from tests import User


class TestUser(ModelTestCase):
    model = User

    def test_has_status(self):
        self.assert_has('status')

    def test_status_is_enum(self):
        self.assert_type('status', sa.Enum)

    def test_status_is_nullable(self):
        self.assert_nullable('status')

    def test_status_length_is_7(self):
        self.assert_length('status', 7)

    def test_status_is_autoincrement(self):
        self.assert_autoincrement('status')

    def test_has_description(self):
        self.assert_has('description')

    def test_description_is_unicode(self):
        self.assert_type('description', sa.Unicode)

    def test_description_is_nullable(self):
        self.assert_nullable('description')

    def test_description_length_is_255(self):
        self.assert_length('description', 255)

    def test_description_is_autoincrement(self):
        self.assert_autoincrement('description')

    def test_has_age(self):
        self.assert_has('age')

    def test_age_is_integer(self):
        self.assert_type('age', sa.Integer)

    def test_age_is_nullable(self):
        self.assert_nullable('age')

    def test_age_is_autoincrement(self):
        self.assert_autoincrement('age')

    def test_has_is_active(self):
        self.assert_has('is_active')

    def test_is_active_is_boolean(self):
        self.assert_type('is_active', sa.Boolean)

    def test_is_active_is_nullable(self):
        self.assert_nullable('is_active')

    def test_default_value_of_is_active(self):
        self.assert_default('is_active', False)

    def test_is_active_is_autoincrement(self):
        self.assert_autoincrement('is_active')

    def test_has_email(self):
        self.assert_has('email')

    def test_email_is_unicode(self):
        self.assert_type('email', sa.Unicode)

    def test_email_is_not_nullable(self):
        self.assert_not_nullable('email')

    def test_email_length_is_255(self):
        self.assert_length('email', 255)

    def test_email_is_autoincrement(self):
        self.assert_autoincrement('email')

    def test_email_is_unique(self):
        self.assert_unique('email')

    def test_has_id(self):
        self.assert_has('id')

    def test_id_is_biginteger(self):
        self.assert_type('id', sa.BigInteger)

    def test_id_is_not_nullable(self):
        self.assert_not_nullable('id')

    def test_id_is_primary_key(self):
        self.assert_primary_key('id')

    def test_id_is_autoincrement(self):
        self.assert_autoincrement('id')

    def test_has_name(self):
        self.assert_has('name')

    def test_name_is_unicode(self):
        self.assert_type('name', sa.Unicode)

    def test_name_is_not_nullable(self):
        self.assert_not_nullable('name')

    def test_name_length_is_255(self):
        self.assert_length('name', 255)

    def test_default_value_of_name(self):
        self.assert_default('name', '')

    def test_name_is_autoincrement(self):
        self.assert_autoincrement('name')

