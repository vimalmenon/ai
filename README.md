# Elara (Ela)

I am an AI Agent named after the moon of Jupiter, representing curiosity and exploration. I work along with Vimal Menon to help with his work.

## Details

<b>Name</b>: Elara
<br/>
<b>Version</b>: 0.0.19
<br/>
<b>Email</b>: elara.ai@proton.me
<br/>

## To Do

- [x] Run test in parallel
- [x] Make all AiMessage Consistent
- [x] [LOW] Remove test warning
- [ ] Make the group Link name consistent
- [ ] Add args for env in Docker build
- [ ] Get and update release version automatically
- [ ] Increase the test coverage to 80%
- [ ] Check for errors / exception in test
- [ ] Remove unwanted env values
- [ ] [fix] Google LLM not working
- [ ] Upgrade poetry to use Python 3.13
- [ ] Add tools to LLM
- [ ] Set up Backend for celery
- [ ] Create health endpoint
- [ ] Set up AWS Auth
- [ ] Handle exception better
- [ ] Change secondary key
- [ ] Set up auth
- [ ] Add more tools
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
