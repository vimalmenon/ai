from enum import Enum

from ai.model.output import TestStructuredOutput


class WorkflowType(Enum):
    LLM = "LLM"
    Agent = "Agent"
    Workflow = "Workflow"
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


class LLMs(Enum):
    DEEPSEEK = "DEEPSEEK"
    GOOGLE = "GOOGLE"
    OLLAMA = "OLLAMA"
    OpenAI = "OpenAI"


class AIMessageType(Enum):
    Human = "Human"
    AI = "AI"
    System = "System"
    Tool = "Tool"


class HealthStatus(Enum):
    OK = "OK"
    NOK = "NOK"
