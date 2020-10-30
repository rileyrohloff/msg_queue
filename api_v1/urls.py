from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path("index", views.index, name="index"),
    path("message", csrf_exempt(views.add_to_queue), name="queue_message"),
    path("currentQueue", views.check_queue, name="check_queue"),
]
