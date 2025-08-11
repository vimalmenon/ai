from enum import Enum

from ai.model.output import TestStructuredOutput


class WorkflowType(Enum):
    LLM = "LLM"
    Agent = "Agent"
    Service = "Service"
    Workflow = "Workflow"
    ExecuteWorkflowCreator = "ExecuteWorkflowCreator"


class Tool(Enum):
    # SaveToNotes = "SaveToNotes"
    SaveToDB = "SaveToDB"
    SaveToS3 = "SaveToS3"
    InternetSearch = "InternetSearch"


class Service(Enum):
    GetFromDB = "GetFromDB"
    SaveToDB = "SaveToDB"
    GetFromS3 = "GetFromS3"
    SaveToS3 = "SaveToS3"
    HumanInput = "HumanInput"
    ManualConfirmation = "ManualConfirmation"
    InternetSearch = "InternetSearch"
    TextToSpeech = "TextToSpeech"
    AddToScheduler = "AddToScheduler"
    GetFromScheduler = "GetFromScheduler"
    ExecuteWorkflowCreator = "ExecuteWorkflowCreator"


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


class AiMessageType(Enum):
    Human = "Human"
    AI = "AI"
    System = "System"
    Tool = "Tool"


class HealthStatus(Enum):
    OK = "OK"
    NOK = "NOK"


class DbKeys(Enum):
    Primary = "table"
    Secondary = "app_id"


class DbTable(Enum):
    AI_SCHEDULER = "AI#SCHEDULER"
    AI_EXECUTE = "AI#EXECUTE"
    AI_WORKFLOWS = "AI#WORKFLOWS"
    AI_LINKS = "AI#LINKS"
