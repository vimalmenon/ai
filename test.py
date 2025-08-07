#!/usr/bin/env python3
"""
Test runner script for the AI project.
This script provides a convenient way to run tests with different options.
"""

import argparse
import subprocess
import sys
from pathlib import Path


def get_python_path():
    """Get the correct Python path for the project."""
    base_path = Path(__file__).parent
    python_path = base_path / ".tox" / "py313" / "bin" / "python"

    if python_path.exists():
        return str(python_path)

    # Fallback to system python
    return "python"


def run_tests(args):
    """Run pytest with the given arguments."""
    python_path = get_python_path()

    cmd = [python_path, "-m", "pytest"]

    if args.verbose:
        cmd.append("-v")

    if args.coverage:
        cmd.extend(["--cov=ai", "--cov-report=term-missing", "--cov-report=html"])

    if args.parallel:
        cmd.extend(["-n", "auto"])

    if args.fast:
        cmd.extend(["-x", "--tb=line"])

    if args.markers:
        cmd.extend(["-m", args.markers])

    if args.path:
        cmd.append(args.path)

    if args.keyword:
        cmd.extend(["-k", args.keyword])

    if args.extra:
        cmd.extend(args.extra)

    print(f"Running: {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=Path(__file__).parent)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Test runner for AI project")

    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    parser.add_argument(
        "-c", "--coverage", action="store_true", help="Run with coverage report"
    )

    parser.add_argument(
        "-p", "--parallel", action="store_true", help="Run tests in parallel"
    )

    parser.add_argument(
        "-f",
        "--fast",
        action="store_true",
        help="Fast mode: stop on first failure, short traceback",
    )

    parser.add_argument(
        "-m",
        "--markers",
        type=str,
        help="Run tests with specific markers (e.g., 'unit', 'integration')",
    )

    parser.add_argument(
        "-k", "--keyword", type=str, help="Run tests matching keyword expression"
    )

    parser.add_argument(
        "path", nargs="?", help="Specific test file or directory to run"
    )

    parser.add_argument("extra", nargs="*", help="Extra arguments to pass to pytest")

    args = parser.parse_args()

    result = run_tests(args)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
