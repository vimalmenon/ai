#!/usr/bin/env python3
"""
FastAPI Interactive Shell
Run with: poetry run python shell.py
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import FastAPI app and commonly used modules
try:
    from main import app
    from ai.managers.workflow_manager.workflow_manager import WorkflowManager
    from ai.managers.db_manager.db_manager import DbManager
    from ai.model import WorkflowModel, WorkflowSlimModel, UpdateWorkflowRequest
    from ai.model.enums import DbKeys
    from ai.utilities import generate_uuid, created_date
    
    print("🚀 FastAPI Interactive Shell")
    print("=" * 50)
    print("Available objects:")
    print("  app          - FastAPI application instance")
    print("  WorkflowManager - Workflow management class")
    print("  DbManager    - Database management class")
    print("  WorkflowModel, WorkflowSlimModel, UpdateWorkflowRequest - Model classes")
    print("  DbKeys       - Database key enums")
    print("  generate_uuid, created_date - Utility functions")
    print()
    print("Quick examples:")
    print("  wm = WorkflowManager()")
    print("  workflows = wm.get_workflows()")
    print("  result = wm.get_workflow_with_executed_workflow()")
    print("  db = DbManager()")
    print()
    print("Type 'help()' for Python help, or 'exit()' to quit")
    print("=" * 50)
    
    # Pre-create some common instances for convenience
    wm = WorkflowManager()
    db = DbManager()
    
    print("Pre-created instances:")
    print("  wm = WorkflowManager()")
    print("  db = DbManager()")
    print()
    
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure you're in the correct directory and dependencies are installed.")
    sys.exit(1)

# Start interactive shell
if __name__ == "__main__":
    import code
    
    # Create a dictionary of local variables to make available in the shell
    local_vars = {
        'app': app,
        'WorkflowManager': WorkflowManager,
        'DbManager': DbManager,
        'WorkflowModel': WorkflowModel,
        'WorkflowSlimModel': WorkflowSlimModel,
        'UpdateWorkflowRequest': UpdateWorkflowRequest,
        'DbKeys': DbKeys,
        'generate_uuid': generate_uuid,
        'created_date': created_date,
        'wm': wm,
        'db': db,
    }
    
    # Start the interactive console
    console = code.InteractiveConsole(locals=local_vars)
    console.interact(banner="")
