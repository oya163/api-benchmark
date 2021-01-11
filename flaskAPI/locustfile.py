import time
from locust import HttpUser, task

class QuickstartUser(HttpUser):
    @task
    def hello_world(self):
        self.client.post("http://127.0.0.1:5000/magic/imageurl")
        self.client.get("/world")