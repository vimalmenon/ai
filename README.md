# Elara (Ela)

I am an AI Agent named after the moon of Jupiter, representing curiosity and exploration. I work along with Vimal Menon to help with his work.


## Details

<b>Name</b>: Elara
<br/>
<b>Version</b>: 0.0.13
<br/>
<b>Email</b>: elara.ai@proton.me
<br/>

## To Do

- [ ] Save executed workflow in DB
- [ ] Create a job to run the workflow
- [ ] Resume workflow
- [ ] Show trimmed WF in list page
- [ ] Handle exception better
- [ ] Remove test warning
- [ ] Set up mock
- [ ] Change secondary key
- [ ] Set up auth
- [ ] Create Docker image
- [ ] Add more tools
- [ ] Create release with tag
- [ ] Create advanced workflows
- [ ] [Endpoints] Add test
- [ ] [Managers] Add test
- [ ] [Services] Add test
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