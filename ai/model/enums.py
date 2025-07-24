from enum import Enum

from ai.model.output import TestStructuredOutput


class WorkflowType(Enum):
    Agent = "Agent"
    LLM = "LLM"
    HumanInput = "HumanInput"
    Service = "Service"
    ManualConfirmation = "ManualConfirmation"


class Tool(Enum):
    SaveToNotes = "SaveToNotes"
    SaveToDB = "SaveToDB"
    SaveToS3 = "SaveToS3"
    InternetSearch = "InternetSearch"
    TextToSpeech = "TextToSpeech"


class Service(Enum):
    GetFromDB = "GetFromDB"
    GetFromS3 = "GetFromS3"
    SaveToDB = "SaveToDB"
    SaveToS3 = "SaveToS3"
    InternetSearch = "InternetSearch"


class WorkflowStatus(Enum):
    NEW = "NEW"
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class WorkflowNodeStatus(Enum):
    NEW = "NEW"
    READY = "READY"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class StructuredOutputType(Enum):
    TestStructuredOutput = TestStructuredOutput.__name__
