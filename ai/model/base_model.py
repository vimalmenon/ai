from humps import camelize
from pydantic import BaseModel, ConfigDict


def to_camel_case(string) -> str:
    return camelize(string)


class Base(BaseModel):

    model_config = ConfigDict(
        alias_generator=to_camel_case,
        validate_by_name=True,
        use_enum_values=True,
        extra="forbid",
    )
