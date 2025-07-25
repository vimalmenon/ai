from collections.abc import Callable

from ai.model.enums import StructuredOutputType
from ai.model.output import TestStructuredOutput


class StructuredOutputService:
    def get_structured_output(self, type=StructuredOutputType) -> Callable | None:
        if type == StructuredOutputType.TestStructuredOutput:
            return TestStructuredOutput
        else:
            return None
