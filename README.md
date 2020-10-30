# msg_queue

Message Bus Implementation with Django and ApScheduler


#### Get Started

Install deps
```pip install -r reqs.txt```

Migrate ``` python manage.py makemigrations```

Start server ```python manage.py runsever```


#### How it works


Post a json message to `/event`

From there django puts that message into a queue * max size is determined by env var

The ApScheduler picks up that event with a worker then posts said event to your specified endpoint after x amount of time.

