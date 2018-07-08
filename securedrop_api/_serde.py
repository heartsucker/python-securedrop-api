from datetime import datetime

'''Helpers for de/serializing JSON
'''


class SerdeError(Exception):
    '''Generic error for de/serialization failures.
    '''

    pass


class Field:
    '''Marker for attributes that should be de/serialized.
       :param serde: Serde for de/serializing JSON
       :param is_optional: Whether the field is required or not
       :param validator: Function that is run when the field is set
    '''

    def __init__(self, serde, is_optional: bool=False, validator=None) -> None:
        if isinstance(serde, JsonSerde):
            serde = serde.as_serde()
        self.serde = serde
        self.is_optional = is_optional
        self.validator = validator


class Serde:

    @classmethod
    def to_json(cls, value):
        raise NotImplementedError

    @classmethod
    def from_json(cls, value):
        raise NotImplementedError

    @classmethod
    def validate(cls, value) -> None:
        raise NotImplementedError


class String(Serde):

    @classmethod
    def to_json(cls, value) -> str:
        return value

    @classmethod
    def from_json(cls, value) -> str:
        return value

    @classmethod
    def validate(cls, value) -> None:
        if not isinstance(value, str):
            raise SerdeError('Not a string: {}'.format(value))


class Boolean(Serde):

    @classmethod
    def to_json(cls, value) -> bool:
        return value

    @classmethod
    def from_json(cls, value) -> bool:
        return value

    @classmethod
    def validate(cls, value) -> None:
        if not isinstance(value, bool):
            raise SerdeError('Not a bool: {}'.format(value))


class Integer(Serde):

    @classmethod
    def to_json(cls, value) -> int:
        return value

    @classmethod
    def from_json(cls, value) -> int:
        return value

    @classmethod
    def validate(cls, value) -> None:
        if not isinstance(value, int):
            raise SerdeError('Not an int: {}'.format(value))


class IsoDateTime(Serde):

    __FMT_STRS = ['{}{}{}'.format('%Y-%m-%dT%H:%M:%S', m, z)
                  for m in ('', '.%f')
                  for z in ('Z', '%z')]

    @classmethod
    def to_json(cls, value) -> str:
        return value

    @classmethod
    def from_json(cls, value) -> datetime:
        for fmt_str in cls.__FMT_STRS:
            try:
                return datetime.strptime(value, fmt_str)
            except ValueError:
                pass
        if value is not None:
            raise SerdeError('Date had bad format: {}'.format(value))

    @classmethod
    def validate(cls, value) -> None:
        if not isinstance(value, datetime):
            raise SerdeError('Not a datetime: {}'.format(value))


class List(Serde):

    def __init__(self, typ) -> None:
        self.__typ = typ

    def to_json(self, value) -> list:
        if value is not None:
            return [v.to_json() for v in value]
        return None

    def from_json(self, value) -> list:
        if value is not None:
            return [self.__typ.from_json(v) for v in value]
        return None

    @classmethod
    def validate(cls, value) -> None:
        if not isinstance(value, list):
            raise SerdeError('Not a datetime: {}'.format(value))


class JsonSerdeMeta(type):

    def __new__(cls, name, bases, attrs):
        __serde_fields__ = {}

        for field_name, field in attrs.items():
            if isinstance(field, Field):
                __serde_fields__[field_name] = field

        attrs['__serde_fields__'] = __serde_fields__
        attrs['__init__'] = JsonSerdeMeta.init
        attrs['__eq__'] = JsonSerdeMeta.eq
        attrs['__ne__'] = lambda s, o: not s.__eq__(o)
        attrs['__hash__'] = JsonSerdeMeta.hash

        return type.__new__(cls, name, bases, attrs)

    @staticmethod
    def init(self, *nargs, **kwargs) -> None:
        for name, field in self.__serde_fields__.items():
            try:
                value = kwargs.pop(name)
            except KeyError:
                if not field.is_optional:
                    raise SerdeError('Missing kwarg {}'.format(name))
                value = None

            if value is not None and hasattr(field.serde, 'validate'):
                field.serde.validate(value)

            if field.validator is not None:
                try:
                    field.validator(value)
                except ValueError as e:
                    raise SerdeError(str(e))
            setattr(self, name, value)

    @staticmethod
    def eq(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False

        for name, field in self.__serde_fields__.items():
            if not hasattr(other, name):
                return False
            if getattr(self, name) != getattr(other, name):
                return False

        return True

    @staticmethod
    def hash(self) -> int:
        out = 0
        for name in sorted(self.__serde_fields__.keys()):
            out ^= hash(getattr(self, name))
        return out


class JsonSerde(Field, metaclass=JsonSerdeMeta):

    @classmethod
    def as_serde(cls) -> Serde:
        return type('{}AsField'.format(cls.__class__.__name__),
                    (Field,),
                    {'to_json': cls.to_json,
                     'from_json': cls.from_json})

    @classmethod
    def from_json(cls, value):
        if not isinstance(value, dict):
            raise SerdeError('Was not a dict: {}'.format(value))

        kwargs = {}
        for key, val in value.items():
            try:
                field = cls.__serde_fields__[key]
            except KeyError:
                continue
            kwargs[key] = field.serde.from_json(val)
        return cls(**kwargs)

    def to_json(self):
        out = {}
        for name, field in self.__serde_fields__.items():
            value = getattr(self, name, None)
            if value is None and field.is_optional:
                continue
            out[name] = field.serde.to_json(value)
        return out
