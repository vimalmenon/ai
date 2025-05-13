from langchain_core.tools import tool

from ai.config.env import env


@tool("save_to_notes")
def save_to_notes(notes: str) -> None:
    """Save the notes to the file only when requested.
    Use this tool only on request.
    Do not use this tool unless asked to save notes.
    """
    with open(env.notes_path, "a") as f:
        f.write(notes)
        f.write("\n")
