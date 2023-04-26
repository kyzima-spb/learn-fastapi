"""
Setup: pip install locust
Run: Save as locustfile.py and run locust in terminal. Open http://localhost:8089 and run with 100, 100, http://localhost.
"""
from locust import HttpUser, task


class User(HttpUser):
    @task
    def test(self):
        self.client.get('/users/test')
        self.client.get('/users/')
