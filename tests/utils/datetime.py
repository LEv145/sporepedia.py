# pragma: no cover
from typing import Any, _SpecialForm
from dataclasses import is_dataclass, Field


def get_actual_type(type_: Any):
    try:
        actual_type = type_.__origin__
    except AttributeError:
        actual_type = type_

    if isinstance(actual_type, _SpecialForm):
        # Case of typing.Union[...] or typing.ClassVar[...] and more
        actual_type = tuple(
            get_actual_type(i)
            for i in type_.__args__
        )

    return actual_type


def validate_dataclass(obj: object):
    if not is_dataclass(obj):
        raise Exception("Object is not dataclass")

    dataclass_fields: dict[str, Field] = obj.__dataclass_fields__  # type: ignore

    for name, field in dataclass_fields.items():
        if isinstance(field.type, _SpecialForm):
            # No check for typing.Any; typing.Union, typing.ClassVar (without parameters)
            continue

        actual_value = getattr(obj, name)

        if is_dataclass(actual_value):
            validate_dataclass(actual_value)

        actual_type = get_actual_type(field.type)

        if not isinstance(actual_value, actual_type):
            raise ValueError(
                f"{type(obj).__name__}[{name}]: '{actual_value}' instead of '{field.type}'"
            )
