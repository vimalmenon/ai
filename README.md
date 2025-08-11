# Elara (Ela) - AI Agent

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)
![Coverage](https://img.shields.io/badge/Coverage-76%25-orange.svg)

An AI Agent named after the moon of Jupiter, representing curiosity and exploration. Elara is a comprehensive AI workflow automation system built with FastAPI, featuring intelligent task processing, link management, and content generation capabilities.

## Table of Contents

- [About](#about)
- [Features](#features)
- [Quick Start](#quick-start)
- [Development Environment](#development-environment)
- [Testing and Quality Assurance](#testing-and-quality-assurance)
- [API Features](#api-features)
- [Docker Deployment](#docker-deployment)
- [Development Roadmap](#development-roadmap)
- [Contributing](#contributing)
- [Links](#links)

## About

**Project**: Elara AI Agent  
**Contact**: elara.ai@proton.me  
**Python Version**: 3.13+  
**Architecture**: FastAPI + Celery + DynamoDB + AWS Integration

## Features

- 🤖 AI-powered workflow automation
- 🔗 Link management and organization
- 📝 Blog content generation
- 🌐 FastAPI-based REST API with modern lifespan management
- 📊 Comprehensive testing and quality assurance (76% coverage)
- 🔄 Celery-based background task processing with scheduled tasks
- 🔍 Interactive development environment
- 🛡️ Enhanced error handling and logging
- ⚡ Request timing and performance monitoring
- 🔧 Developer-friendly testing tools and scripts
- 🚀 Production-ready deployment script with service orchestration

## Quick Start

### Prerequisites

- **Python 3.13+** - Latest Python version
- **Poetry** - For dependency management ([Install Poetry](https://python-poetry.org/docs/#installation))
- **AWS Account** - For DynamoDB and S3 services
- **Docker & Docker Compose** (optional) - For containerized deployment

### Environment Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai
   ```

2. **Configure environment variables**
   ```bash
   # Copy example environment file
   cp .env.example .env
   
   # Edit .env with your configuration
   nano .env
   ```

   Required environment variables:
   ```env
   # AWS Configuration
   AWS_ACCESS_KEY_ID=your_access_key
   AWS_SECRET_ACCESS_KEY=your_secret_key
   AWS_DEFAULT_REGION=us-east-1
   
   # Application Settings
   DEBUG=true
   HOST=0.0.0.0
   PORT=8000
   ALLOWED_ORIGINS=http://localhost:3000,https://example.com
   
   # Database
   DYNAMODB_TABLE_NAME=your_table_name
   ```

3. **Install dependencies**
   ```bash
   poetry install
   ```

### Development Server

Choose your preferred method to start the development environment:

#### Option 1: FastAPI Only
```bash
# Start the FastAPI development server
poetry run fastapi dev main.py
# or use the poetry script shortcut
poetry run app
```

#### Option 2: Full Stack (Recommended)
```bash
# Start all services (FastAPI + Celery + Celery Beat)
./start-local.sh
```

This will start:
- **FastAPI server** at `http://localhost:8000`
- **Celery worker** for background tasks
- **Celery beat** for scheduled tasks

### API Endpoints

Once running, access these endpoints:

| Endpoint | Description |
|----------|-------------|
| [`http://localhost:8000`](http://localhost:8000) | Root API information |
| [`http://localhost:8000/health`](http://localhost:8000/health) | Health check |
| [`http://localhost:8000/docs`](http://localhost:8000/docs) | Interactive API docs (Swagger) |
| [`http://localhost:8000/redoc`](http://localhost:8000/redoc) | ReDoc documentation |

## Docker Deployment

### Development with Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Run in detached mode
docker-compose up -d --build

# View logs
docker-compose logs -f app

# Stop services
docker-compose down
```

### Production Deployment

```bash
# Production deployment with optimized settings
docker-compose -f docker-compose.prod.yml up -d --build

# With Nginx reverse proxy
docker-compose -f docker-compose.prod.yml --profile with-nginx up -d --build

# Scale the application
docker-compose -f docker-compose.prod.yml up -d --scale app=3
```

### Service Management Scripts

The project includes environment-specific startup scripts:

#### Local Development (`start-local.sh`)
- Uses Poetry and local paths
- Logs to `logs/` directory
- Designed for development environments

#### Production (`start.sh`)
- Uses containerized paths (`/app/.venv/bin/`)
- Optimized for Docker containers
- Production-ready configuration

Both scripts provide:
- **Graceful shutdown** with SIGTERM/SIGINT handling
- **Process monitoring** and automatic restart
- **Separate log files** for each service:
  - `logs/app.log` (FastAPI)
  - `logs/celery.log` (Celery worker)  
  - `logs/celery-beat.log` (Celery scheduler)

## Development Roadmap

### ✅ Completed Features

- [x] Mock LLM service for comprehensive testing
- [x] Interactive development shell with FastAPI context
- [x] Improved main.py with robust logging and error handling
- [x] Developer-friendly testing tools and Makefile commands
- [x] Request timing middleware for performance monitoring
- [x] Health check and root API endpoints
- [x] Environment-based CORS configuration
- [x] Production-ready deployment scripts
- [x] [Not possible] Optimize workflow execution with parallel processing
- [x] Set up batch processes for scheduler
- [x] Refactor HumanInput & HumanConfirm to Service layer

### 🔄 In Progress

- [ ] Implement DynamoDB batch operations
- [ ] Migrate business logic from managers to services
- [ ] DynamdoDB fetch is very slow, Need to check singapore region.
- [ ] Update secondary key name (Check with copilot)
- [ ] Implement Celery batch jobs (30-minute intervals)

### 📋 Planned Features

- [ ] **Performance**: Parallel workflow execution and fetch optimization
- [ ] **Automation**: Auto-generate workflow nodes from database
- [ ] **Monitoring**: Comprehensive logging for Service and Manager classes
- [ ] **Auto-execution**: Auto-execute nodes (except human input required)
- [ ] **Testing**: Increase test coverage to 85%+ (currently 76%)
- [ ] **Environment**: Clean up and document environment variables
- [ ] **Integrations**: Fix Google LLM integration and AWS authentication

### 🚀 Future Enhancements

- [ ] **[Low Priority]** Migrate from string IDs to UUID
- [ ] **[Low Priority]** Multi-node workflow connections
- [ ] **[AI Features]** Advanced content generation capabilities
- [ ] **[AI Features]** Automated code generation and review
- [ ] **[AI Features]** Enhanced AI tool integration

### 🎯 Immediate Actions

- [ ] Review workflow_node_service.py implementation
- [ ] Update environment variable documentation
- [ ] Add error handling examples to API documentation
- [ ] Create comprehensive deployment guide
- [ ] Add performance benchmarking tests

### 🔧 Code Quality & Maintenance

- [ ] Refactor long functions in workflow services
- [ ] Add missing docstrings to public methods
- [ ] Improve error messages for debugging
- [ ] Create troubleshooting guide
- [ ] Add input validation examples

### 📖 Documentation & Examples

- [ ] Create comprehensive API usage examples
- [ ] Add step-by-step workflow creation tutorial
- [ ] Document environment setup variations
- [ ] Create contributor onboarding guide
- [ ] Add architecture decision records

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
## Contributing

We welcome contributions to improve Elara! Please follow these guidelines:

### Development Workflow

1. **Fork the repository**
   ```bash
   git fork https://github.com/vimalmenon/ai
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes**
   - Write clean, well-documented code
   - Follow existing code style and patterns
   - Add tests for new functionality

4. **Run quality checks**
   ```bash
   # Run all quality checks
   make pre-push
   
   # Or run individual checks
   make test-cov      # Tests with coverage
   make lint          # Code linting
   make type-check    # Type checking
   ```

5. **Commit and push**
   ```bash
   git commit -m 'feat: add amazing feature'
   git push origin feature/amazing-feature
   ```

6. **Open a Pull Request**
   - Provide a clear description of changes
   - Link any related issues
   - Ensure all CI checks pass

### Development Guidelines

- **Testing**: Write tests for new features (maintain 80%+ coverage)
- **Type Hints**: Use type hints throughout the codebase
- **Code Style**: Follow existing patterns (enforced by ruff and black)
- **Documentation**: Add docstrings for public functions and classes
- **Commits**: Use conventional commit format (`feat:`, `fix:`, `docs:`, etc.)

### Code Quality Standards

- **Linting**: Code must pass ruff and flake8 checks
- **Formatting**: Use black for consistent code formatting
- **Type Checking**: All code must pass mypy type checking
- **Testing**: Maintain or improve test coverage
- **Security**: Follow security best practices

### Pre-Push Quality Checks

A pre-push git hook automatically runs quality checks:

```bash
# Manual pre-push check
make pre-push

# Individual quality tools
tox -e lint        # Linting
tox -e type-check  # Type checking
tox -e py313       # Tests with coverage
```

## Utility Commands

### Git and Repository Management

```bash
# Clean up remote branches
git remote update origin --prune

# Remove old local branches  
git branch | grep -v "$(git branch --show-current)" | xargs git branch -D

# Find process on port
sudo lsof -i :8000
```

### Docker Commands Reference

```bash
# Development
docker build -t elara-ai .
docker run -p 8000:8000 --env-file .env elara-ai

# Production scaling
docker-compose -f docker-compose.prod.yml up -d --scale app=3

# Update production deployment
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d --build
```

## Links

- **[SonarCloud Analysis](https://sonarcloud.io/project/overview?id=vimalmenon_ai)** - Code quality metrics
- **[GitHub Repository](https://github.com/vimalmenon/ai)** - Source code
- **[FastAPI Documentation](https://fastapi.tiangolo.com/)** - Framework documentation
- **[Celery Documentation](https://docs.celeryproject.org/)** - Task queue documentation

## License

This project is private and proprietary. All rights reserved.
```

## Development Environment

Multiple interfaces for interacting with the FastAPI application during development.

### Interactive Development Shell

Access enhanced Python shells with pre-loaded FastAPI context:

```bash
# Enhanced IPython shell (recommended)
poetry run python ishell.py

# Basic Python shell with FastAPI context
poetry run python shell.py
```

**Pre-loaded objects**:
- `app` - FastAPI application instance
- `wm` - WorkflowManager instance
- `db` - DbManager instance  
- Model classes: `WorkflowModel`, `WorkflowSlimModel`, `UpdateWorkflowRequest`
- Utilities: `generate_uuid`, `created_date`, `DbKeys`

### Management Commands

Django-style management interface for development tasks:

```bash
# Show all available commands
poetry run python manage.py

# Interactive shell
poetry run python manage.py shell

# Workflow management
poetry run python manage.py workflow list
poetry run python manage.py workflow get-with-executed
poetry run python manage.py workflow create --name "My New Workflow"

# Testing
poetry run python manage.py test --method test_get_workflows
poetry run python manage.py test  # Run all tests
```

### Development Examples

```python
# Interactive shell examples:

# Get all workflows
workflows = wm.get_workflows()

# Get workflow by ID
workflow = wm.get_workflow_by_id("some-id")

# Create new workflow
from ai.model import WorkflowSlimModel
new_wf = wm.create_workflow(WorkflowSlimModel(name="Test Workflow"))

# Database operations
from boto3.dynamodb.conditions import Key
items = db.query_items(Key(DbKeys.Primary.value).eq("AI#WORKFLOWS"))
```

### Development Commands

```bash
# Makefile shortcuts
make help           # Show all available commands
make install        # Install dependencies
make dev            # Start development server
make lint           # Run all linting tools
make format         # Auto-format code
make type-check     # Run type checking

# Manual commands
poetry run ruff check --fix    # Fix linting issues
poetry run black .             # Format code
poetry run ptw                 # Test watch mode

# Celery commands
poetry run celery -A tasks worker -l info    # Start worker
poetry run celery -A tasks beat -l info      # Start scheduler
```

## Testing and Quality Assurance

This project features comprehensive testing with pytest, coverage reporting, and multiple quality assurance tools.

### Quick Testing Commands

```bash
# Run all tests with coverage
make test

# Fast mode (stop on first failure)
make test-fast

# Detailed coverage report
make test-cov

# Run tests by category
make test-units      # Manager and service tests (30 tests)
make test-apis       # API endpoint tests (20 tests)

# Run tests in parallel
make test-parallel

# Run specific test file
make test-file FILE=ai/tests/api/test_error_handling.py

# Run tests matching a pattern
make test-pattern PATTERN="validation"

# Watch mode for continuous testing
make test-watch

# Clean test artifacts
make clean
```

### Test Coverage

- **Current Coverage**: 76%
- **Target Coverage**: 85%+
- **Coverage Reports**: Terminal and HTML formats
- **Branch Coverage**: Enabled for comprehensive analysis

### Test Structure

```
ai/tests/
├── api/           # API endpoint tests (20 tests)
├── managers/      # Manager layer tests (30 tests)
├── services/      # Service layer tests
├── conftest.py    # Shared fixtures and configuration
└── factory/       # Test data factories
```

### Quality Assurance with Tox

Run comprehensive quality checks across multiple environments:

```bash
# Run all environments (tests, linting, type checking)
tox

# Run specific environments
tox -e py313        # Tests with coverage
tox -e lint         # Linting checks
tox -e type-check   # Type checking with mypy
tox -e format       # Auto-format code
```

### Pre-Push Quality Checks

Automated quality checks prevent code issues before pushing:

```bash
# Manual quality check (recommended before pushing)
make pre-push

# Or use the dedicated script
./scripts/pre-push-check.sh
```

**Quality checks include**:
- Code formatting (Black)
- Linting (Ruff, Flake8)
- Type checking (MyPy)
- Full test suite with coverage

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
