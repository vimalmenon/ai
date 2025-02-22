from ai.config import env


def save_to_notes(notes: str):
    """This save notes to the file in the disk. Use this tools for saving notes."""
    with open(env.notes_path, "a") as f:
        f.write(notes)
        f.write("\n")
