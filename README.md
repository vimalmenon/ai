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
- [ ] Check if Workflow and execute can me made Parallel (Fetch takes lot of time)
- [ ] Can batch get from dynamo fetch in multiple table
- [ ] Need to move some business logic to service from manager
- [ ] Need to do set batch processes for scheduler
- [ ] Remove warning from test
- [ ] Workflow / Service to create nodes automatically from DB
- [ ] Add logger in all the Service and Manager class
- [ ] Run Celery Batch Job to run every 30 Minutes
- [ ] Automatically execute node unless there is human input required
- [ ] Move id from str to UUID
- [ ] Increase the test coverage to 80%
- [ ] Remove unwanted env values
- [ ] [fix] Google LLM not working
- [ ] Set up Backend for celery
- [ ] Create health endpoint
- [ ] Set up AWS Auth
- [ ] Change secondary key
- [ ] Add more tools
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
