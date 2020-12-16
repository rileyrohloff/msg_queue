from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
import json
import uuid
from random import randint

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


@require_POST
def mock_reporting_service(request, event_ID):
    data = json.loads(request.body)
    print(data, event_ID)
    possible_status = [200, 503, 429, 300]
    key_status = possible_status[randint(0, len(possible_status) - 1)]
    return JsonResponse(
            {"status": "recieved"}, status=key_status, content_type="application/json"
        )

@require_GET
def health_check(request):
    bools = [True, False]
    which_bool = bools[randint(0, 1)]

    if which_bool:
        return JsonResponse({"healthy": True}, status=200)
    return JsonResponse({"healthy": False}, status=500)
