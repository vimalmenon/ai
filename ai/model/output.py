from pydantic import BaseModel, Field


class TestStructuredOutput(BaseModel):
    """List countries detail."""

    name: str = Field(description="The name of the topic")
