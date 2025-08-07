# Elara (Ela) - AI Agent

An AI Agent named after the moon of Jupiter, representing curiosity and exploration. Elara works alongside Vimal Menon to assist with various development and automation tasks.

## About

**Name**: Elara  
**Email**: elara.ai@proton.me  
**Version**: 0.0.19  
**Python**: 3.13+

## Features

- 🤖 AI-powered workflow automation
- 🔗 Link management and organization
- 📝 Blog content generation
- 🌐 FastAPI-based REST API
- 📊 Comprehensive testing and quality assurance
- 🔄 Celery-based background task processing
- 🔍 Interactive development environment

## Quick Start

### Prerequisites

- Python 3.13+
- Poetry for dependency management
- AWS credentials (for DynamoDB and S3)

### Installation

```sh
# Clone the repository
git clone <repository-url>
cd ai

# Install dependencies
poetry install

# Start the development server
poetry run fastapi dev main.py
```

The API will be available at `http://localhost:8000`

## Development Roadmap

### Completed ✅
- [x] Make the group Link name consistent (Use the name LinkGroup and not GroupLink)
- [x] Handle exception better
- [x] Set up auth
- [x] Upgrade poetry to use Python 3.13
- [x] Mock LLM service for testing
- [x] Add interactive development shell with FastAPI context

### In Progress 🔄
- [ ] Optimize workflow execution (make Workflow and execute parallel - fetch optimization)
- [ ] Implement batch operations for DynamoDB
- [ ] Move business logic from managers to services
- [ ] Set up batch processes for scheduler

### Planned 📋
- [ ] Remove warnings from tests
- [ ] Auto-generate workflow nodes from database
- [ ] Add comprehensive logging to Service and Manager classes
- [ ] Implement Celery batch jobs (30-minute intervals)
- [ ] Auto-execute nodes (except human input required)
- [ ] Increase test coverage to 80%
- [ ] Clean up environment variables
- [ ] Fix Google LLM integration
- [ ] Set up Celery backend
- [ ] Create health endpoint
- [ ] Implement AWS authentication
- [ ] Update secondary key structure
- [ ] Add more AI tools

### Future Enhancements 🚀
- [ ] **[Low Priority]** Migrate from string IDs to UUID
- [ ] **[Low Priority]** Multi-node connections
- [ ] **[AI Features]** Content generation
- [ ] **[AI Features]** Code generation
- [ ] **[AI Features]** Code review automation

## Links

- [SonarCloud Analysis](https://sonarcloud.io/project/overview?id=vimalmenon_ai)

## Development Environment

This project provides multiple ways to interact with the FastAPI application for development, debugging, and testing.

### Interactive Development Shell

Start an enhanced Python shell with pre-loaded FastAPI context:

```sh
# Basic Python shell with FastAPI context
poetry run python shell.py

# Enhanced IPython shell (recommended - if IPython is installed)
poetry run python ishell.py
```

**Available objects in the shell:**
- `app` - FastAPI application instance
- `wm` - Pre-configured WorkflowManager instance  
- `db` - Pre-configured DbManager instance
- `WorkflowManager`, `DbManager` - Manager classes
- `WorkflowModel`, `WorkflowSlimModel`, `UpdateWorkflowRequest` - Model classes
- `DbKeys` - Database key enumerations
- `generate_uuid`, `created_date` - Utility functions

### Management Commands

Django-style management interface for common development tasks:

```sh
# Show all available commands
poetry run python manage.py

# Start interactive shell
poetry run python manage.py shell

# Workflow management
poetry run python manage.py workflow list
poetry run python manage.py workflow get-with-executed
poetry run python manage.py workflow create --name "My New Workflow"

# Run specific tests
poetry run python manage.py test --method test_get_workflows
poetry run python manage.py test  # Run all tests
```

### Development Examples

```python
# In the shell, you can:

# Get all workflows
workflows = wm.get_workflows()

# Get workflow by ID
workflow = wm.get_workflow_by_id("some-id")

# Create a new workflow
from ai.model import WorkflowSlimModel
new_wf = wm.create_workflow(WorkflowSlimModel(name="Test Workflow"))

# Test database operations
from boto3.dynamodb.conditions import Key
items = db.query_items(Key(DbKeys.Primary.value).eq("AI#WORKFLOWS"))

# Access FastAPI routes
print([route.path for route in app.routes])
```

### Quick Access Commands

```sh
# Quick functionality access
poetry run python -c "
from ai.managers.workflow_manager.workflow_manager import WorkflowManager
wm = WorkflowManager()
print('Total Workflows:', len(wm.get_workflows()))
"

# Interactive session with preloaded context
poetry run python -i -c "
from main import app
from ai.managers.workflow_manager.workflow_manager import WorkflowManager
wm = WorkflowManager()
print('Ready! Use wm and app objects for interaction')
"
```

## Testing and Quality Assurance

This project uses **tox** for comprehensive testing and quality assurance across different environments.

### Tox Environments

```sh
# Run all environments (tests, linting, type checking)
tox

# Run only tests with coverage
tox -e py313

# Run only linting checks
tox -e lint

# Run only type checking
tox -e type-check

# Auto-format code (black + ruff fix)
tox -e format

# Documentation environment (placeholder)
tox -e docs
```

### Individual Quality Checks

```sh
# Test coverage with detailed reporting
tox -e py313

# Check code formatting and style
tox -e lint

# Type checking with mypy
tox -e type-check

# Format code automatically
tox -e format
```

### Additional Development Commands

```sh
# Code formatting and linting
poetry run ruff check --fix
poetry run black .

# Test in watch mode
poetry run ptw

# Run Celery worker
poetry run celery -A tasks worker -l info
```

## Utility Commands

### Git and Branch Management

```sh
# Clean up remote branches
git remote update origin --prune

# Remove old local branches
git branch | grep -v "$(git branch --show-current)" | xargs git branch -D
```

### System Utilities

```sh
# Find process running on port 8000
sudo lsof -i :8000
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and quality checks (`tox`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is private and proprietary.
