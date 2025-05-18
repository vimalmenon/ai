from enum import Enum


class WorkflowType(Enum):
    Agent = "Agent"
    LLM = "LLM"
    Tool = "Tool"
    HumanInput = "HumanInput"
    Service = "Service"


class Tool(Enum):
    SaveToNotes = "SaveToNotes"
    SaveToDB = "SaveToDB"
    SaveToS3 = "SaveToS3"
    TextToSpeech = "TextToSpeech"


class Service(Enum):
    GetFromDB = "GetFromDB"
    GetFromS3 = "GetFromS3"


class WorkflowStatus(Enum):
    NEW = "NEW"
    RUNNING = "RUNNING"
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    IN_PROGRESS = "IN_PROGRESS"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
