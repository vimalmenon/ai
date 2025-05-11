from enum import Enum


class WorkflowType(Enum):
    Agent = "Agent"
    LLM = "LLM"
    Tool = "Tool"
    HumanInput = "HumanInput"
    Service = "Service"


class Tool(Enum):
    save_to_notes = "Save To Notes"
    save_to_db = "Save To DB"
    save_to_s3 = "Save To S3"
