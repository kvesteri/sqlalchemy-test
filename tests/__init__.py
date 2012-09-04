import sqlalchemy as sa
from sqlalchemy.sql.expression import false
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
    is_active = sa.Column(sa.Boolean, default=False, server_default='FALSE')
    is_confirmed = sa.Column(sa.Boolean, server_default=false())
    age = sa.Column(sa.Integer, index=True)
    description = sa.Column(sa.Unicode(255))
