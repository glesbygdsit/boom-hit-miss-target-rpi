# boom-hit-miss-target-rpi
## Running tests with Docker
TDB: Dev. Docker images coming soon...

Clone repo and run:
```
docker run --rm -it -v ${PWD}:/app python:3.7.0a4-alpine
```

In running Docker container:
```
pip install pipenv
cd /app
pipenv install -d
pipenv run ptw -p
```
Files can now be edited on host and will automatically trigger tests to be run upon modification.
