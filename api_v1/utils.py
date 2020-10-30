import os
import json
import requests
import queue
from dotenv import load_dotenv

load_dotenv()


class MsgPublisher:
    def __init__(self):
        self.session = requests.Session()
        self.endpoint = os.getenv("EVENT_URL")
        self.queue_maxsize = int(os.environ["QUEUE_SIZE"])
        self.queue = queue.Queue(maxsize=self.queue_maxsize)

    def publish_event(self, event: dict):
        resp = self.session.post(url=f"{self.endpoint}/api/event", json=event)
        data = resp.json()
        print("\nRESPONSE FROM ENDPOINT: ", json.dumps(data, indent=2))

    def event_worker(self):
        while self.queue.qsize() > 0:
            item = self.queue.get()
            print(f"{item} ------- sending payload to ==> {os.environ['EVENT_URL']}")
            self.publish_event(item)
            self.queue.task_done()

    def trigger_queue(self):
        if self.queue.qsize() > 0:
            self.event_worker()
        else:
            pass

    def read_queue(self) -> list:
        return list(self.queue.queue)
