from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
import json
import uuid

from apscheduler.schedulers.background import BackgroundScheduler

from . import utils

msg_queue = utils.MsgPublisher()
scheduler = BackgroundScheduler()


# Create your views here.


def start_queue_proccessing():
    msg_queue.trigger_queue()


scheduler.start()
scheduler.add_job(start_queue_proccessing, "interval", seconds=2, max_instances=1)


@require_GET
def index(request):
    response: dict = {"msg": "success"}
    return JsonResponse(response, status=200, content_type="application/json")


@require_POST
def add_to_queue(request):
    data = json.loads(request.body)
    data["guid"] = str(uuid.uuid4())
    if msg_queue.queue.qsize() >= msg_queue.queue_maxsize:
        print(f"Current: {msg_queue.queue.qsize()} of {msg_queue.queue.maxsize}")
        return JsonResponse(
            {"error": "queue is full"}, status=400, content_type="application/json"
        )
    msg_queue.queue.put(data)
    return JsonResponse(
        {"success": f"{data} added to the queue"},
        status=200,
        content_type="application/json",
    )


@require_GET
def check_queue(request):
    data = msg_queue.read_queue()
    return JsonResponse({"queue": f"{data}"}, status=200)
