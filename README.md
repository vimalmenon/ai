# Elara (Ela)

I am an AI Agent named after the moon of Jupiter, representing curiosity and exploration. I work along with Vimal Menon to help with his work.


## Details

<b>Name</b>: Elara
<br/>
<b>Version</b>: 0.0.16
<br/>
<b>Email</b>: elara.ai@proton.me
<br/>

## To Do

- [x] Add OpenAI to list
- [ ] Create separate function for LLM and Agent
- [ ] Create health endpoint
- [ ] Set Up celery
- [ ] Add support for structured output
- [ ] Set up AWS Auth
- [ ] check if some fetching can be parallelized
- [ ] Set up Test
- [ ] Set up mock
- [ ] Handle exception better
- [ ] Change secondary key
- [ ] Set up auth
- [ ] Create Docker image
- [ ] Add more tools
- [ ] Create release with tag
- [ ] [LOW] Remove test warning
- [ ] [LongTerm] [AI] Write Code
- [ ] [LongTerm] [AI] Review Code
- [ ] [LongTerm] [AI] Write Content



## Links

- [Sonar](https://sonarcloud.io/project/overview?id=vimalmenon_ai)


## Command

```sh
poetry run fastapi dev main.py
```
```sh
poetry run ruff check --fix
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
