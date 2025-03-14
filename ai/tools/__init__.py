from ai.tools.multiply.multiply import multiply
from ai.tools.save_notes.save_notes import save_to_notes
from ai.tools.save_to_s3.save_to_s3 import save_to_s3

tools = [save_to_notes, multiply, save_to_s3]

__all__ = [
    "multiply",
    "save_to_notes",
    "save_to_s3",
]
