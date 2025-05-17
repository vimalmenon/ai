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
