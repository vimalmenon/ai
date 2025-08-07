#!/usr/bin/env python3
"""
FastAPI Management Commands
Usage: poetry run python manage.py <command>

Available commands:
  shell    - Interactive shell with FastAPI context
  test     - Run specific method tests
  workflow - Workflow-specific commands
"""

import argparse
import sys
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))


def shell_command():
    """Start interactive shell"""
    print("Starting FastAPI shell...")
    with open("shell.py") as f:
        exec(f.read())


def test_command(args):
    """Run tests"""
    import subprocess

    if args.method:
        # Test specific method
        cmd = f"poetry run pytest ai/tests/managers/test_workflow_manager.py::{args.method} -v"
        print(f"Running: {cmd}")
        subprocess.run(cmd, shell=True)
    else:
        # Run all tests
        cmd = "poetry run pytest ai/tests/ -v"
        print(f"Running: {cmd}")
        subprocess.run(cmd, shell=True)


def workflow_command(args):
    """Workflow management commands"""
    from ai.managers.workflow_manager.workflow_manager import WorkflowManager

    wm = WorkflowManager()

    if args.action == "list":
        workflows = wm.get_workflows()
        print(f"Found {len(workflows)} workflows:")
        for wf in workflows:
            print(f"  - {wf.id}: {wf.name}")

    elif args.action == "get-with-executed":
        # Since get_workflow_with_executed_workflow doesn't exist, let's use available methods
        workflows = wm.get_workflows()
        print(f"Workflows: {len(workflows)}")

        for wf in workflows:
            print(f"  Workflow: {wf.id} - {wf.name}")

        # You can add logic here to get executed workflows from DbManager if needed
        from boto3.dynamodb.conditions import Key

        from ai.managers.db_manager.db_manager import DbManager
        from ai.model.enums import DbKeys

        db = DbManager()
        executed_items = db.query_items(Key(DbKeys.Primary.value).eq("AI#EXECUTE"))
        print(f"Executed workflows: {len(executed_items)}")

        for ew in executed_items:
            print(
                f"  Executed: {ew.get('workflow_id', 'N/A')} - {ew.get('status', 'N/A')}"
            )

    elif args.action == "create":
        from ai.model import WorkflowSlimModel

        if not args.name:
            print("Error: --name is required for create action")
            return

        data = WorkflowSlimModel(name=args.name)
        workflow = wm.create_workflow(data)
        print(f"Created workflow: {workflow.id} - {workflow.name}")


def main():
    parser = argparse.ArgumentParser(description="FastAPI Management Commands")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Shell command
    subparsers.add_parser("shell", help="Start interactive shell")

    # Test command
    test_parser = subparsers.add_parser("test", help="Run tests")
    test_parser.add_argument("--method", help="Specific test method to run")

    # Workflow command
    workflow_parser = subparsers.add_parser("workflow", help="Workflow management")
    workflow_parser.add_argument(
        "action",
        choices=["list", "get-with-executed", "create"],
        help="Action to perform",
    )
    workflow_parser.add_argument("--name", help="Workflow name (for create action)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == "shell":
        shell_command()
    elif args.command == "test":
        test_command(args)
    elif args.command == "workflow":
        workflow_command(args)


if __name__ == "__main__":
    main()
