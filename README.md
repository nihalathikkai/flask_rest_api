# flask_rest_api

Learn REST API development with Flask

## Docker Commands

```
docker build -t rest-apis-flask-python .

docker run -d -p 5000:5000 rest-apis-flask-python

docker run -d -p 5000:5000 -w /app -v "%cd%:/app" rest-apis-flask-python

docker run -d -p 5000:5000 -w /app -v "$(pwd):/app" rest-apis-flask-python

docker container ls

docker container stop <id>
docker container prune
```
