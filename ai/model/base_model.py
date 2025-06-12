from humps import camelize
from pydantic import BaseModel


def to_camel_case(string) -> str:
    return camelize(string)


class Base(BaseModel):
    class Config:
        alias_generator = to_camel_case
        validate_by_name = True
        use_enum_values = True
        json_encoders = {
            str: lambda v: v,
            int: lambda v: v,
            float: lambda v: v,
            bool: lambda v: v,
        }
        extra = "forbid"
