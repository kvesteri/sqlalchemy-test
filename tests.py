from pytest import raises
import sqlalchemy as sa
from sqlalchemy_test import ModelTestCase


from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Entity(Base):
    __tablename__ = 'entity'
    id = sa.Column(sa.BigInteger, autoincrement=True, primary_key=True)
    name = sa.Column(sa.Unicode(255), index=True, nullable=False, default=u'')


class User(Entity):
    __tablename__ = 'user'
    STATUSES = ('status1', 'status2')
    query = None

    id = sa.Column(sa.BigInteger, sa.ForeignKey(Entity.id), primary_key=True)
    email = sa.Column(sa.Unicode(255), unique=True, nullable=False)
    status = sa.Column(sa.Enum(*STATUSES))
    is_active = sa.Column(sa.Boolean, default=False)
    age = sa.Column(sa.Integer, index=True)
    description = sa.Column(sa.Unicode(255))


class TestEntity(ModelTestCase):
    model = Entity

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
