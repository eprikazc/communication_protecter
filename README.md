# Running the project
- Set `SLACK_OAUTH_ACCESS_TOKEN` environment variable. It can have some fake value if you only want to run tests:
```
export SLACK_OAUTH_ACCESS_TOKEN=abcde
```
- Project consists of database, redis, django development server and celery worker. We can run them all on development machine with single command:
```
docker-compose up
```
- Fill database:
```
make fill-db
```
- At this point you should be able to access application's admin interface at: `http://localhost:18000/admin/`.

# Running style check and tests
Unittests are written with `pytest`. We can run them in django docker container with single command (assuming that `docker-compose up` was run before):
```
make
```
By default, `all` target from Makefile is executed, which runs style check with `flake8` and then run tests.
It is also possible to run test(s) directly via pytest, for example
```
docker-compose exec django pytest dlp/tests.py::test_analyze_ok -v
```

# Running with real slack account
- Install, grok and setup tunnel: `ngrok http 18000`. In console output notice forwarding URL, it should look like `https://asdasdwe.ngrok.io`.
- Create slack account. Add following permissions/scopes: `channels:history, channels:read, chat:write:user, im:history, im:read`
Enable events and set ngrok URL from step#1: `https://asdasdwe.ngrok.io/slack-event`.
NOTE: we added `/slack-event` to the URL!
- Write message with following content in slack:
> This is bad message, because it contains companies email address - user@company.com

- When you send the message, following should happen:
    - Slack sends request to ngrok URL. You should be able to see this request in ngrok web interface at http://127.0.0.1:4040
    - Django should receive the request and create chain of celery tasks to process it
    - Celery tasks should detect data leakagei, record it to db, and block the message (change message text)
    - In django admin you should see new detection - http://localhost:18000/admin/slack_connector/dlpdetection/
    - In slack you should see the message text changed to:
> This message has been blocked

# TODO:
- Verify/confirm list of permissions/scopes in README. Perhaps some of them are not needed.
- Make request verification work
