# Elara (Ela) - AI Agent

An AI Agent named after the moon of Jupiter, representing curiosity and exploration. Elara works alongside Vimal Menon to assist with various development and automation tasks.

## About

**Name**: Elara  
**Email**: elara.ai@proton.me  
**Python**: 3.13+

## Features

- 🤖 AI-powered workflow automation
- 🔗 Link management and organization
- 📝 Blog content generation
- 🌐 FastAPI-based REST API with modern lifespan management
- 📊 Comprehensive testing and quality assurance (76% coverage)
- 🔄 Celery-based background task processing
- 🔍 Interactive development environment
- 🛡️ Enhanced error handling and logging
- ⚡ Request timing and performance monitoring
- 🔧 Developer-friendly testing tools and scripts

## Quick Start

### Prerequisites

- Python 3.13+
- Poetry for dependency management
- AWS credentials (for DynamoDB and S3)
- Docker and Docker Compose (optional, for containerized deployment)

### Installation

#### Local Development

```sh
# Clone the repository
git clone <repository-url>
cd ai

# Install dependencies
poetry install

# Start the development server
poetry run fastapi dev main.py
# or using the poetry script
poetry run app
```

The API will be available at:
- Main API: `http://localhost:8000`
- Health Check: `http://localhost:8000/health`
- API Documentation: `http://localhost:8000/docs`
- ReDoc Documentation: `http://localhost:8000/redoc`

#### Docker Development

```sh
# Build and run with Docker Compose
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build

# View logs
docker-compose logs -f app

# Stop services
docker-compose down
```

#### Production Deployment

```sh
# Production deployment with optimized settings
docker-compose -f docker-compose.prod.yml up -d --build

# With Nginx reverse proxy
docker-compose -f docker-compose.prod.yml --profile with-nginx up -d --build
```

## Development Roadmap

### Completed ✅
- [x] Make the group Link name consistent (Use the name LinkGroup and not GroupLink)
- [x] Handle exception better
- [x] Set up auth
- [x] Upgrade poetry to use Python 3.13
- [x] Mock LLM service for testing
- [x] Add interactive development shell with FastAPI context
- [x] Enhanced main.py with improved logging and error handling
- [x] Modern FastAPI lifespan event handlers (replaced deprecated @app.on_event)
- [x] Comprehensive pytest configuration with coverage reporting
- [x] Developer-friendly testing tools and Makefile commands
- [x] Request timing middleware for performance monitoring
- [x] Health check and root endpoints
- [x] Environment-based CORS configuration

### In Progress 🔄
- [ ] Optimize workflow execution (make Workflow and execute parallel - fetch optimization)
- [ ] Implement batch operations for DynamoDB
- [ ] Move business logic from managers to services
- [ ] Set up batch processes for scheduler

### Planned 📋
- [ ] Optimize workflow execution (make Workflow and execute parallel - fetch optimization)
- [ ] Auto-generate workflow nodes from database
- [ ] Add comprehensive logging to Service and Manager classes
- [ ] Implement Celery batch jobs (30-minute intervals)
- [ ] Auto-execute nodes (except human input required)
- [ ] Increase test coverage to 85%+ (currently at 76%)
- [ ] Clean up environment variables
- [ ] Fix Google LLM integration
- [ ] Set up Celery backend
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

## API Features

### Enhanced FastAPI Application

The main application (`main.py`) includes several production-ready features:

#### 🔧 **Robust Error Handling**
- Custom exception handlers for validation errors, HTTP exceptions, and general errors
- Backward-compatible error responses with enhanced detail structure
- Request URL context in error logs
- Debug-conditional error message exposure

#### 📊 **Comprehensive Logging**
- Console and file logging with structured format
- Request/response timing middleware
- Error logging with stack traces
- Configurable log levels

#### ⚡ **Performance Monitoring**
- Request timing middleware
- Response time logging
- Performance metrics tracking

#### 🛡️ **Modern Patterns**
- FastAPI lifespan event handlers (replaces deprecated `@app.on_event`)
- Type-safe request/response handling
- Proper middleware implementation

#### 🌐 **API Endpoints**
- `GET /` - Root endpoint with API information
- `GET /health` - Health check with environment details
- `GET /docs` - Interactive API documentation
- `GET /redoc` - ReDoc API documentation

#### 🔄 **Middleware Features**
- CamelCase to snake_case request body conversion
- Environment-based CORS configuration
- Request logging and timing

### Environment Configuration

The application supports flexible environment-based configuration:

```python
# Environment variables
ALLOWED_ORIGINS=http://localhost:3000,https://example.com
DEBUG=true
HOST=0.0.0.0
PORT=8000
```

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

This project features a comprehensive testing setup with pytest, coverage reporting, and developer-friendly tools.

### Quick Testing Commands

```sh
# Run all tests with coverage
make test

# Fast mode (stop on first failure)
make test-fast

# Run with detailed coverage report
make test-cov

# Run tests by category (directory-based)
make test-units      # Manager and service tests (30 tests)
make test-apis       # API endpoint tests (20 tests)

# Run tests in parallel
make test-parallel

# Run specific test file
make test-file FILE=ai/tests/api/test_error_handling.py

# Run tests matching a pattern
make test-pattern PATTERN="validation"

# Run tests in watch mode
make test-watch

# Clean test artifacts
make clean
```

### Using the Test Script

The project includes a custom test runner (`test.py`) with additional options:

```sh
# Basic usage
python test.py

# With coverage and verbose output
python test.py --coverage --verbose

# Fast mode with parallel execution
python test.py --fast --parallel

# Run specific test markers
python test.py --markers unit

# Run tests matching keywords
python test.py --keyword "error_handling"

# Run specific test path
python test.py ai/tests/api/test_links.py
```

### Pytest Configuration

The project uses a comprehensive pytest configuration in `pyproject.toml`:

- **Coverage**: Automatic coverage reporting with 76% current coverage
- **Markers**: Support for `unit`, `integration`, and `slow` test markers
- **Strict Mode**: Strict marker and config validation
- **Multiple Reports**: Terminal and HTML coverage reports
- **Branch Coverage**: Tracks code branch coverage

### Test Structure

```
ai/tests/
├── api/           # API endpoint tests
├── conftest.py    # Shared fixtures and test configuration
├── factory/       # Test data factories
├── managers/      # Manager layer tests  
└── services/      # Service layer tests
```

### Available Test Fixtures

- `client` - FastAPI test client
- `dynamodb_mock` - Mocked DynamoDB for testing
- `mock_llm_execute_service` - Mocked LLM service
- `mock_ai_message_manager` - Mocked AI message manager
- `setup_env` - Automatic environment setup for tests

### Tox Integration

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
# Makefile commands for development workflow
make help           # Show all available commands
make install        # Install dependencies
make dev            # Start development server
make test           # Run all tests
make test-fast      # Fast test mode
make test-cov       # Tests with coverage
make lint           # Run all linting tools
make format         # Auto-format code
make type-check     # Run type checking
make clean          # Clean build artifacts

# Manual commands
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

## Docker Commands

### Development

```sh
# Build the Docker image
docker build -t elara-ai .

# Run the container
docker run -p 8000:8000 --env-file .env elara-ai

# Build and run with Docker Compose
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop and remove containers
docker-compose down
```

### Production

```sh
# Production deployment
docker-compose -f docker-compose.prod.yml up -d --build

# Scale the application
docker-compose -f docker-compose.prod.yml up -d --scale app=3

# Update application
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d --build

# View production logs
docker-compose -f docker-compose.prod.yml logs -f app
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run quality checks:
   ```sh
   # Run tests
   make test-cov
   
   # Run linting
   make lint
   
   # Run type checking  
   make type-check
   
   # Or run everything with tox
   tox
   ```
5. Ensure tests pass and coverage is maintained
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Development Guidelines

- Write tests for new features (aim for 80%+ coverage)
- Use type hints throughout the codebase
- Follow existing code style (enforced by ruff and black)
- Add docstrings for public functions and classes
- Update README for significant changes

### Pre-Push Quality Checks

This project has several mechanisms to ensure code quality before pushing:

#### Automatic Git Hook
A pre-push git hook is installed that automatically runs all quality checks before allowing a push. The hook will prevent pushing if any checks fail.

#### Manual Quality Checks
You can manually run quality checks using any of these methods:

```bash
# Using make (recommended)
make pre-push

# Using the dedicated script
./scripts/pre-push-check.sh

# Using tox for comprehensive testing
tox
```

#### What Gets Checked
- **Code Formatting**: Black formatting compliance
- **Linting**: Ruff and Flake8 code quality checks  
- **Type Checking**: MyPy static type analysis
- **Tests**: Full test suite with coverage reporting

#### GitHub Actions CI/CD
The repository includes GitHub Actions workflows that run the same checks on every push and pull request to the main branches.

## License

This project is private and proprietary.
