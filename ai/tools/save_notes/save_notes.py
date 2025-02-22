from ai.config import env


def save_to_notes(notes: str):
    """Save the notes to the file when requested. Use this tool only when requested. Do not use this tool unless asked to save notes."""
    with open(env.notes_path, "a") as f:
        f.write(notes)
        f.write("\n")
