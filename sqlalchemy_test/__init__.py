import os
from sqlalchemy.sql.expression import _False, _True
from sqlalchemy.orm.properties import ColumnProperty


class ModelTestCase(object):
    model = None

    @property
    def columns(self):
        fields = set(self.model._sa_class_manager.values())
        columns = {}
        for field in fields:
            prop = field.property
            if isinstance(prop, ColumnProperty):
                column = prop.columns[0]
                columns[column.name] = column
        return columns

    @property
    def foreign_keys(self):
        foreign_keys = {}
        for name, column in self.columns.items():
            if column.foreign_keys:
                foreign_keys[name] = list(column.foreign_keys)
        return foreign_keys

    def test_has_primary_key(self):
        assert any(column.primary_key for column in self.columns.values())

    def assert_table_name(self, table_name):
        assert self.model.__tablename__ == table_name

    def assert_has(self, column_name):
        msg = (
            "Model %r does not have a column called %r. "
            "The model has the following columns: %s" % (
                self.model.__name__,
                column_name,
                [column for column in self.columns]
            )
        )
        assert column_name in self.columns, msg

    def assert_type(self, column_name, type_):
        assert isinstance(self.columns[column_name].type, type_)

    def assert_length(self, column_name, length):
        assert self.columns[column_name].type.length == length

    def assert_primary_key(self, column_name):
        assert self.columns[column_name].primary_key

    def assert_check_constraint(self, column_name, check_constraint):
        found = False
        for constraint in self.columns[column_name].constraints:
            if constraint.sqltext.text == check_constraint.sqltext.text:
                found = True

        if not found:
            assert False, "Column %s did not have check constraint %r" % (
                column_name, check_constraint
            )

    def assert_foreign_key(self, column_name, foreign_key):
        fks = self.foreign_keys[column_name]
        for fk in fks:
            if fk.target_fullname == foreign_key.target_fullname:
                assert fk.deferrable == foreign_key.deferrable
                assert fk.ondelete == foreign_key.ondelete
                assert fk.onupdate == foreign_key.onupdate
                assert fk.initially == foreign_key.initially
                assert fk.name == foreign_key.name

    def assert_unique(self, column_name):
        assert self.columns[column_name].unique

    def assert_index(self, column_name):
        assert self.columns[column_name].index

    def assert_default(self, column_name, default):
        assert self.columns[column_name].default.arg == default

    def assert_server_default(self, column_name, default):
        column_default = self.columns[column_name].server_default.arg
        if default.__class__ == column_default.__class__:
            if isinstance(default, _False) or isinstance(default, _True):
                return True

        assert column_default == default

    def assert_nullable(self, column_name):
        assert self.columns[column_name].nullable

    def assert_not_nullable(self, column_name):
        assert not self.columns[column_name].nullable

    def assert_autoincrement(self, column_name):
        assert self.columns[column_name].autoincrement

    def assert_not_autoincrement(self, column_name):
        assert not self.columns[column_name].autoincrement


def generate_test_case(model, path):
    fields = set(model._sa_class_manager.values())
    columns = {}
    for field in fields:
        prop = field.property
        if isinstance(prop, ColumnProperty):
            column = prop.columns[0]
            columns[column.name] = column

    file_ = open('%stest_%s.py' % (path, model.__name__.lower()), 'w+')
    lines = [
        'import sqlalchemy as sa',
        'from sqlalchemy_test import ModelTestCase',
        'from %s import %s' % (model.__module__, model.__name__),
        os.linesep,
        'class Test%s(ModelTestCase):' % model.__name__,
        '    model = %s%s' % (model.__name__, os.linesep)
    ]

    for name, column in columns.items():
        lines.extend(generate_has_column_test(name))
        lines.extend(generate_type_test(name, column.type))
        if column.nullable:
            lines.extend(generate_nullable_test(name))
        else:
            lines.extend(generate_not_nullable_test(name))
        if hasattr(column.type, 'length') and column.type.length:
            lines.extend(generate_length_test(name, column.type.length))
        if column.primary_key:
            lines.extend(generate_primary_key_test(name))
        if column.foreign_keys:
            counter = 1
            for fk in column.foreign_keys:
                lines.extend(generate_foreign_key_test(name, fk, counter))
                counter += 1
        if column.default:
            lines.extend(generate_default_test(name, column.default.arg))
        if column.server_default:
            lines.extend(
                generate_server_default_test(name, column.server_default.arg)
            )
        if column.autoincrement:
            lines.extend(generate_autoincrement_test(name))
        if column.unique:
            lines.extend(generate_unique_test(name))
    file_.writelines(map(lambda a: a + os.linesep, lines))


def generate_has_column_test(name):
    return [
        "    def test_has_%s(self):" % name.lower(),
        "        self.assert_has('%s')%s" % (name.lower(), os.linesep)
    ]


def generate_nullable_test(name):
    return [
        "    def test_%s_is_nullable(self):" % name.lower(),
        "        self.assert_nullable('%s')%s" % (name.lower(), os.linesep)
    ]


def generate_not_nullable_test(name):
    return [
        "    def test_%s_is_not_nullable(self):" % name.lower(),
        "        self.assert_not_nullable('%s')%s" % (name.lower(), os.linesep)
    ]


def generate_length_test(name, length):
    return [
        "    def test_%s_length_is_%d(self):" % (name.lower(), length),
        "        self.assert_length('%s', %d)%s" % (
            name.lower(), length, os.linesep
        )
    ]


def generate_type_test(name, type_):
    return [
        "    def test_%s_is_%s(self):" % (
            name.lower(), type_.__class__.__name__.lower()
        ),
        "        self.assert_type('%s', sa.%s)%s" % (
            name.lower(), type_.__class__.__name__, os.linesep
        )
    ]


def generate_primary_key_test(name):
    return [
        "    def test_%s_is_primary_key(self):" % name.lower(),
        "        self.assert_primary_key('%s')%s" % (name.lower(), os.linesep)
    ]


def generate_foreign_key_test(name, fk, counter):
    lines = [
        "    def test_%s_fk%d(self):" % (name.lower(), counter),
        "        self.assert_foreign_key(",
        "            '%s'," % name.lower(),
        "            sa.ForeignKey(",
        "                'Address.id',",
    ]
    if fk.deferrable:
        lines.append(
            "                deferrable=True,"
        )
    if fk.ondelete:
        lines.append(
            "                ondelete='%s'," % fk.ondelete
        )
    if fk.onupdate:
        lines.append(
            "                onupdate='%s'," % fk.onupdate
        )

    lines.extend([
        "            )",
        "        )" + os.linesep,
    ])
    return lines


def generate_autoincrement_test(name):
    return [
        "    def test_%s_is_autoincremented(self):" % name.lower(),
        "        self.assert_autoincrement('%s')%s" % (
            name.lower(), os.linesep
        )
    ]


def generate_default_test(name, default):
    if isinstance(default, basestring):
        default = "'%s'" % default
    elif callable(default):
        return []

    lines = [
        "    def test_default_of_%s(self):" % name.lower(),
        "        self.assert_default('%s', %s)%s" % (
            name.lower(), default, os.linesep
        )
    ]
    return lines


def generate_server_default_test(name, default):
    if isinstance(default, basestring):
        default = "'%s'" % default
    elif isinstance(default, _False):
        default = 'sa.sql.expression.false()'
    elif isinstance(default, _True):
        default = 'sa.sql.expression.true()'

    return [
        "    def test_server_default_of_%s(self):" % name.lower(),
        "        self.assert_server_default('%s', %s)%s" % (
            name.lower(), default, os.linesep
        )
    ]


def generate_unique_test(name):
    return [
        "    def test_%s_is_unique(self):" % name.lower(),
        "        self.assert_unique('%s')%s" % (name.lower(), os.linesep)
    ]
