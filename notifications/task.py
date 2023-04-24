from celery import Celery

app = Celery("tasks", broker="pyamqp://redis@localhost//")


@app.task
def add(x, y):
    return x + y
