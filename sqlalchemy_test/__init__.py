import os
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

    def assert_unique(self, column_name):
        assert self.columns[column_name].unique

    def assert_index(self, column_name):
        assert self.columns[column_name].index

    def assert_default(self, column_name, default):
        assert self.columns[column_name].default.arg == default

    def assert_server_default(self, column_name, default):
        assert self.columns[column_name].server_default.arg == default

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
        if hasattr(column.type, 'length'):
            lines.extend(generate_length_test(name, column.type.length))
        if column.primary_key:
            lines.extend(generate_primary_key_test(name))
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


def generate_autoincrement_test(name):
    return [
        "    def test_%s_is_autoincremented(self):" % name.lower(),
        "        self.assert_autoincrement('%s')%s" % (
            name.lower(), os.linesep
        )
    ]


def generate_default_test(name, default):
    lines = ["    def test_default_of_%s(self):" % name.lower()]

    if isinstance(default, basestring):
        lines.append(
            "        self.assert_default('%s', '%s')%s" % (
                name.lower(), default, os.linesep
            )
        )
    else:
        lines.append(
            "        self.assert_default('%s', %s)%s" % (
                name.lower(), default, os.linesep
            )
        )
    return lines


def generate_server_default_test(name, default):
    lines = ["    def test_server_default_of_%s(self):" % name.lower()]

    if isinstance(default, basestring):
        lines.append(
            "        self.assert_server_default('%s', '%s')%s" % (
                name.lower(), default, os.linesep
            )
        )
    else:
        lines.append(
            "        self.assert_server_default('%s', %s)%s" % (
                name.lower(), default, os.linesep
            )
        )
    return lines


def generate_unique_test(name):
    return [
        "    def test_%s_is_unique(self):" % name.lower(),
        "        self.assert_unique('%s')%s" % (name.lower(), os.linesep)
    ]
