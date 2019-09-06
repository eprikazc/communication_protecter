# Running the project
Project consists of database, redis, django development server and celery worker. We can run them all on development machine with single command:
```
docker-compose up
```

# Running style check and tests
Unittests are written with pytest. We can run them in django docker container (assuming that `docker-compose up` was run before):
```
make
```
By default, `all` target is executed, which runs style check with `flake8` and if then run tests.
It is also possible to run tests directly via pytest, for example
```
docker-compose exec django pytest dlp/tests.py::test_analyze_ok -v
```

# Trying things in browser
To check things in browser, we need to fill database:
```
make fill-db
```
Now, we can do simple in-browser test:
Open browser at `http://localhost:18000/admin/slack_connector/dlpdetection/`.
Make http request similar to Slack event. Like this:
```
curl http://127.0.0.1:18000/slack-event -H 'Content-Type: application/json' --data '{"event": {"type": "message", "text": "this is bad message user@company.com"}}'
```
Refresh browser and make sure that new `DLPDetection` record has been added.
