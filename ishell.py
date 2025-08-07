#!/usr/bin/env python3
"""
FastAPI IPython Shell with auto-completion and syntax highlighting
Run with: poetry run python ishell.py
"""

import sys
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from IPython import embed
    from IPython.terminal.prompts import Prompts, Token

    # Custom prompt
    class FastAPIPrompts(Prompts):
        def in_prompt_tokens(self, cli=None):
            return [
                (Token.Prompt, "FastAPI"),
                (Token.Prompt, "["),
                (Token.PromptNum, str(self.shell.execution_count)),
                (Token.Prompt, "]: "),
            ]

    # Import FastAPI app and modules
    from ai.managers.db_manager.db_manager import DbManager
    from ai.managers.workflow_manager.workflow_manager import WorkflowManager
    from ai.model import UpdateWorkflowRequest, WorkflowModel, WorkflowSlimModel
    from ai.model.enums import DbKeys
    from ai.utilities import created_date, generate_uuid
    from main import app

    # Pre-create instances
    wm = WorkflowManager()
    db = DbManager()

    print("🚀 FastAPI IPython Shell")
    print("=" * 50)
    print("Available objects:")
    print("  app, wm, db, WorkflowManager, DbManager, etc.")
    print("=" * 50)

    # Start IPython with enhanced features
    embed(
        header="",
        prompts_class=FastAPIPrompts,
        colors="Linux",  # Better colors for terminal
        # Make these available in the IPython shell
        user_ns={
            "app": app,
            "WorkflowManager": WorkflowManager,
            "DbManager": DbManager,
            "WorkflowModel": WorkflowModel,
            "WorkflowSlimModel": WorkflowSlimModel,
            "UpdateWorkflowRequest": UpdateWorkflowRequest,
            "DbKeys": DbKeys,
            "generate_uuid": generate_uuid,
            "created_date": created_date,
            "wm": wm,
            "db": db,
        },
    )

except ImportError:
    print("IPython not installed. Installing it would provide better shell experience.")
    print("Run: poetry add ipython")
    print("Falling back to regular Python shell...")

    # Fallback to regular shell
    with open("shell.py") as f:
        exec(f.read())
