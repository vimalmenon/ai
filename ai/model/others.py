from enum import Enum


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
