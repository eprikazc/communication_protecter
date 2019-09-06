# Running the project
Project consists of database, redis, django development server and celery worker. You can run them all on your development machine with single command:
```
docker-compose up
```

# Running tests
Unittests are written with pytest. You can run them in django docker container (assuming that `docker-compose up` was run before):
```
docker-compose exec django pytest
```

# Trying things in browser
To check things in browser, you need to fill database:
```
docker-compose exec django python manage.py migrate
docker-compose exec django python manage.py createsuperuser
docker-compose exec django python manage.py loaddata dlp/fixtures/filter_rules.json
```
Now we can do simple in-browser test:
Open browser at `http://localhost:18000/admin/slack_connector/dlpdetection/`.
Make http request similar to Slack event. Like this:
```
curl http://127.0.0.1:18000/slack-event -H 'Content-Type: application/json' --data '{"event": {"type": "message", "text": "this is bad message user@company.com"}}'
```
Refresh browser and make sure that new `DLPDetection` record has been added.
