# Elara (Ela)

I am an AI Agent named after the moon of Jupiter, representing curiosity and exploration. I work along with Vimal Menon to help with his work.


## Details

<b>Name</b>: Elara
<br/>
<b>Version</b>: 0.0.18
<br/>
<b>Email</b>: elara.ai@proton.me
<br/>


## To Do

- [x] Create API for links
- [x] Set up Test
- [x] Set up mock
- [x] Reduce the docker image Size to 500 MB
- [x] CD to upload the image to DockerHub
- [x] Create release with tag
- [x] Improve the class for env
- [ ] Remove test from docker
- [ ] Get release automatically
- [ ] Move All Primary Key and Secondary Key reference to enums
- [ ] [fix] Google LLM not working
- [ ] Upgrade poetry to use Python 3.13
- [ ] Add tools to LLM
- [ ] Get Secret from AWS Secret Manager
- [ ] Set up Backend for celery
- [ ] Create health endpoint
- [ ] Set up AWS Auth
- [ ] check if some fetching can be parallelized
- [ ] Handle exception better
- [ ] Change secondary key
- [ ] Set up auth
- [ ] Add more tools
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