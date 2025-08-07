#!/bin/bash

# Pre-push quality checks script
# Run this manually before pushing to ensure all checks pass

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_header() {
    echo -e "${BLUE}===========================================${NC}"
    echo -e "${BLUE} $1 ${NC}"
    echo -e "${BLUE}===========================================${NC}"
}

print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check if poetry is available
if ! command -v poetry &> /dev/null; then
    print_error "Poetry is not installed. Please install poetry first."
    exit 1
fi

print_header "Running Pre-Push Quality Checks"

# Install dependencies if needed
echo "📦 Ensuring dependencies are installed..."
poetry install --quiet
print_status "Dependencies are up to date"

echo ""
print_header "Code Formatting (Black)"
if poetry run black --check --diff .; then
    print_status "Code formatting is correct"
else
    print_error "Code formatting issues found. Run 'poetry run black .' to fix"
    exit 1
fi

echo ""
print_header "Linting (Ruff)"
if poetry run ruff check; then
    print_status "Ruff linting passed"
else
    print_error "Ruff linting failed. Run 'poetry run ruff check --fix' to fix issues"
    exit 1
fi

echo ""
print_header "Linting (Flake8)"
if poetry run flake8 .; then
    print_status "Flake8 linting passed"
else
    print_error "Flake8 linting failed"
    exit 1
fi

echo ""
print_header "Type Checking (MyPy)"
if poetry run mypy ai; then
    print_status "Type checking passed"
else
    print_error "Type checking failed"
    exit 1
fi

echo ""
print_header "Running Tests"
if poetry run pytest -n auto --cov=ai --cov-report=term-missing; then
    print_status "All tests passed"
else
    print_error "Some tests failed"
    exit 1
fi

echo ""
print_header "All Checks Passed! 🎉"
echo -e "${GREEN}Your code is ready to be pushed!${NC}"
echo ""
echo "To push your changes:"
echo "  git push origin <branch-name>"
echo ""
