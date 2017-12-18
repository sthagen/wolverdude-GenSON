from copy import copy
from warnings import warn


class SchemaGenerator(object):
    KEYWORDS = ('type')

    @classmethod
    def match_schema(cls, schema):
        raise NotImplementedError("'match_schema' not implemented")

    @classmethod
    def match_object(cls, obj):
        raise NotImplementedError("'match_object' not implemented")

    def __init__(self, parent_node):
        self._extra_keywords = {}

    def add_schema(self, schema):
        self.add_extra_keywords(schema)

    def add_extra_keywords(self, schema):
        for keyword, value in schema.items():
            if keyword in self.KEYWORDS:
                continue
            elif keyword not in self._extra_keywords:
                self._extra_keywords[keyword] = value
            elif self._extra_keywords[keyword] != value:
                warn(('Schema incompatible. Keyword {0!r} has conflicting '
                      'values ({1!r} vs. {2!r}). Using {1!r}').format(
                          keyword, self._extra_keywords[keyword], value))

    def add_object(self, obj):
        pass

    def to_schema(self):
        return copy(self._extra_keywords)


class TypedSchemaGenerator(SchemaGenerator):
    # JS_TYPE =
    # PYTHON_TYPE =

    @classmethod
    def match_schema(cls, schema):
        return schema.get('type') == cls.JS_TYPE

    @classmethod
    def match_object(cls, obj):
        return isinstance(obj, cls.PYTHON_TYPE)

    def to_schema(self):
        schema = super().to_schema()
        schema['type'] = self.JS_TYPE
        return schema
