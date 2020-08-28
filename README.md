# Embiq task

To run debug flask app on port ```5000```.
```
$ docker-compose up web
```

To run tests. 
```
$ docker-compose up tests
```

## API example (/api)

### register (/auth/register) POST
```
{
    "username": "testuser",
    "password": "password",
    "slack_api": "https://hooks.slack.com/services/.../.../..."
}
```
Response 200
```
{
    "data": {
        "id": "5f48ac017fc73750d044f933",
        "slack_api": "https://hooks.slack.com/services/.../.../...",
        "tasks": [],
        "username": "testuser"
    },
    "success": true
}
```

### login (/auth/login) POST
Return bearer token (JWT)
```
{
    "username": "testuser",
    "password": "password"
}
```
Response 200
```
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTg1OTgyNDQsIm5iZiI6MTU5ODU5ODI0NCwianRpIjoiNTkxNzVhNWItMjNiMy00MmU2LTlmOTAtMzIwYmI0Yzc2NDJmIiwiZXhwIjoxNTk4Njg0NjQ0LCJpZGVudGl0eSI6InRlc3R1c2VyIiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.cR2vGdSpOSwsKNSaQODSlB25-7SViRF_WGuJV5ULuh8"
}
```

### Get Tasks (/task) GET
Add token to headers 

Example Response 200
```
{
    "data": [
        {
            "_id": "5f4817b0409d1d3bc6ddccb6",
            "date_created": "2020-08-27T20:29:36.173000",
            "date_schedule": "2020-08-26T16:11:00.132000",
            "message": "test message",
            "name": "test"
        },
        {
            "_id": "5f4817b1409d1d3bc6ddccb7",
            "date_created": "2020-08-27T20:29:37.459000",
            "date_schedule": "2020-08-26T16:11:00.132000",
            "message": "message",
            "name": "test second"
        }
    ],
    "success": true
}
```

### New Task (/task) POST
Add token to headers 
```
{
    "name": "test",
    "message": "my message",
    "date_schedule": "2020-08-26T16:11:00.132000"
}
```

Example Response 200
```
{
    "data": [
        {
            "_id": "5f4817b0409d1d3bc6ddccb6",
            "date_created": "2020-08-27T20:29:36.173000",
            "date_schedule": "2020-08-26T16:11:00.132000",
            "message": "test message",
            "name": "test"
        },
        {
            "_id": "5f4817b1409d1d3bc6ddccb7",
            "date_created": "2020-08-27T20:29:37.459000",
            "date_schedule": "2020-08-26T16:11:00.132000",
            "message": "message",
            "name": "test second"
        }
    ],
    "success": true
}
```

### Edit Task (/task) PATCH
Add token to headers 
```
{
    "id": "5f4817b0409d1d3bc6ddccb6",
    "data": {
        "name": "test",
        "message": "test"
    }
}
```

Example Response 200
```
{
    "data": {
        "_id": "5f4817b0409d1d3bc6ddccb6",
        "date_created": "2020-08-27T20:29:36.173000",
        "date_schedule": "2020-08-26T16:11:00.132000",
        "message": "test",
        "name": "test"
    },
    "success": true
}
```

### Delete Task (/task) DELETE
Add token to headers 
```
{
    "id": "5f4817b0409d1d3bc6ddccb6"
}
```

Example Response 200
```
{
    "data": {
        "id": "5f468955f5ea3fc43c2b4229",
        "slack_api": "https://hooks.slack.com/services/.../.../...",
        "tasks": [
            {
                "_id": "5f4817b0409d1d3bc6ddccb6",
                "date_created": "2020-08-27T20:29:36.173000",
                "date_schedule": "2020-08-26T16:11:00.132000",
                "message": "test",
                "name": "test"
            }
        ],
        "username": "testuser"
    },
    "success": true
}
```

### Get tasks in one week back (/task/week) GET

### Get tasks in one month back (/task/month) GET


## Todo:
- week, month as filters on /task GET
- get week, month tasks in a more elegant way 
- fix clear up in tests, data stays in db
- add validators for adding date_schedule for task
- on app.run(): add to schedular all not finished tasks and with date > nowdate
- on app.run(): all tasks with date <= nowdate, send notification and check as finished
- more tests on auth
- more tests on task
- test schedular