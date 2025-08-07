# Elara (Ela)

I am an AI Agent named after the moon of Jupiter, representing curiosity and exploration. I work along with Vimal Menon to help with his work.

## Details

<b>Name</b>: Elara
<br/>
<b>Email</b>: elara.ai@proton.me
<br/>

## To Do

- [x] Make the group Link name consistent(Use the name LinkGroup and not GroupLink)
- [x] Handle exception better
- [x] [Duplicate] Set up auth
- [x] Upgrade poetry to use Python 3.13
- [x] [Test] Mock LLM service
- [x] Add interactive development shell with FastAPI context
- [ ] Check if Workflow and execute can me made Parallel (Fetch takes lot of time)
- [ ] Can batch get from dynamo fetch in multiple table
- [ ] Need to move some business logic to service from manager
- [ ] Need to do set batch processes for scheduler
- [ ] Remove warning from test
- [ ] Workflow / Service to create nodes automatically from DB
- [ ] Add logger in all the Service and Manager class
- [ ] Run Celery Batch Job to run every 30 Minutes
- [ ] Automatically execute node unless there is human input required
- [ ] Increase the test coverage to 80%
- [ ] Remove unwanted env values
- [ ] [fix] Google LLM not working
- [ ] Set up Backend for celery
- [ ] Create health endpoint
- [ ] Set up AWS Auth
- [ ] Change secondary key
- [ ] Add more tools
- [ ] [Low] Move id from str to UUID
- [ ] [Low] Node can connect to multiple node
- [ ] [LongTerm] [AI] Write Content
- [ ] [LongTerm] [AI] Write Code
- [ ] [LongTerm] [AI] Review Code

## Links

- [Sonar](https://sonarcloud.io/project/overview?id=vimalmenon_ai)

## Command

```sh
poetry run fastapi dev main.py
```

## Development Shell

This project provides several ways to interact with the FastAPI application in a shell environment for development and debugging.

### Interactive Shell

Start an interactive Python shell with pre-loaded FastAPI context:

```sh
# Basic Python shell with FastAPI context
poetry run python shell.py

# Enhanced IPython shell (if IPython is installed)
poetry run python ishell.py
```

Available objects in the shell:
- `app` - FastAPI application instance
- `wm` - Pre-created WorkflowManager instance  
- `db` - Pre-created DbManager instance
- `WorkflowManager`, `DbManager` - Manager classes
- `WorkflowModel`, `WorkflowSlimModel`, `UpdateWorkflowRequest` - Model classes
- `DbKeys` - Database key enums
- `generate_uuid`, `created_date` - Utility functions

### Management Commands

Use Django-style management commands for common tasks:

```sh
# Show available commands
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

### Quick Shell Examples

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

### One-liner Commands

```sh
# Quick access to specific functionality
poetry run python -c "
from ai.managers.workflow_manager.workflow_manager import WorkflowManager
wm = WorkflowManager()
print('Workflows:', len(wm.get_workflows()))
"

# Interactive session with preloaded context
poetry run python -i -c "
from main import app
from ai.managers.workflow_manager.workflow_manager import WorkflowManager
wm = WorkflowManager()
print('Ready! Use wm, app objects')
"
```

```sh
poetry run ruff check --fix
```

Run poetry test in watch mode

```sh
poetry run ptw
```

Clean up Remote branch

```sh
git remote update origin --prune
```

Find the process running in 8000

```sh
sudo lsof -i :8000
```

Run Celery

```sh
poetry run celery -A tasks worker -l info
```

Remove old branch

```sh
git branch | grep -v "$(git branch --show-current)" | xargs git branch -D
```
