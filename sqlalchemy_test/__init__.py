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

    def assert_autoincrement(self, column_name):
        assert self.columns[column_name].autoincrement

    def assert_not_autoincrement(self, column_name):
        assert not self.columns[column_name].autoincrement
