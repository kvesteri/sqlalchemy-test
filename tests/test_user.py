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

    def test_status_is_autoincremented(self):
        self.assert_autoincrement('status')

    def test_has_address_id(self):
        self.assert_has('address_id')

    def test_address_id_is_integer(self):
        self.assert_type('address_id', sa.Integer)

    def test_address_id_is_nullable(self):
        self.assert_nullable('address_id')

    def test_address_id_fk1(self):
        self.assert_foreign_key(
            'address_id',
            sa.ForeignKey(
                'Address.id',
                deferrable=True,
                ondelete='CASCADE',
                onupdate='CASCADE',
            )
        )

    def test_address_id_is_autoincremented(self):
        self.assert_autoincrement('address_id')

    def test_has_name(self):
        self.assert_has('name')

    def test_name_is_unicode(self):
        self.assert_type('name', sa.Unicode)

    def test_name_is_not_nullable(self):
        self.assert_not_nullable('name')

    def test_name_length_is_255(self):
        self.assert_length('name', 255)

    def test_default_of_name(self):
        self.assert_default('name', '')

    def test_has_is_confirmed(self):
        self.assert_has('is_confirmed')

    def test_is_confirmed_is_boolean(self):
        self.assert_type('is_confirmed', sa.Boolean)

    def test_is_confirmed_is_nullable(self):
        self.assert_nullable('is_confirmed')

    def test_server_default_of_is_confirmed(self):
        self.assert_server_default('is_confirmed', sa.sql.expression.false())

    def test_is_confirmed_is_autoincremented(self):
        self.assert_autoincrement('is_confirmed')

    def test_has_created_at(self):
        self.assert_has('created_at')

    def test_created_at_is_datetime(self):
        self.assert_type('created_at', sa.DateTime)

    def test_created_at_is_nullable(self):
        self.assert_nullable('created_at')

    def test_created_at_is_autoincremented(self):
        self.assert_autoincrement('created_at')

    def test_has_is_active(self):
        self.assert_has('is_active')

    def test_is_active_is_boolean(self):
        self.assert_type('is_active', sa.Boolean)

    def test_is_active_is_nullable(self):
        self.assert_nullable('is_active')

    def test_default_of_is_active(self):
        self.assert_default('is_active', False)

    def test_server_default_of_is_active(self):
        self.assert_server_default('is_active', 'FALSE')

    def test_is_active_is_autoincremented(self):
        self.assert_autoincrement('is_active')

    def test_has_id(self):
        self.assert_has('id')

    def test_id_is_biginteger(self):
        self.assert_type('id', sa.BigInteger)

    def test_id_is_not_nullable(self):
        self.assert_not_nullable('id')

    def test_id_is_primary_key(self):
        self.assert_primary_key('id')

    def test_id_fk1(self):
        self.assert_foreign_key(
            'id',
            sa.ForeignKey(
                'Address.id',
            )
        )

    def test_id_is_autoincremented(self):
        self.assert_autoincrement('id')

    def test_has_age(self):
        self.assert_has('age')

    def test_age_is_integer(self):
        self.assert_type('age', sa.Integer)

    def test_age_is_nullable(self):
        self.assert_nullable('age')

    def test_age_is_autoincremented(self):
        self.assert_autoincrement('age')

    def test_has_email(self):
        self.assert_has('email')

    def test_email_is_unicode(self):
        self.assert_type('email', sa.Unicode)

    def test_email_is_not_nullable(self):
        self.assert_not_nullable('email')

    def test_email_length_is_255(self):
        self.assert_length('email', 255)

    def test_email_is_autoincremented(self):
        self.assert_autoincrement('email')

    def test_email_is_unique(self):
        self.assert_unique('email')

    def test_has_description(self):
        self.assert_has('description')

    def test_description_is_unicodetext(self):
        self.assert_type('description', sa.UnicodeText)

    def test_description_is_nullable(self):
        self.assert_nullable('description')

    def test_description_is_autoincremented(self):
        self.assert_autoincrement('description')

