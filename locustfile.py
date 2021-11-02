import logging
from http import HTTPStatus
from json import dumps
from random import choice

from locust import HttpUser, TaskSet, constant, task

from plugins.utils import url_for
from handlers.get_city import GetUserCity


class AnalyzerTaskSet(TaskSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.round = 0

    @staticmethod
    def create_id():
        return choice([123, 356, 678])

    def request(self, method, path, expected_status, user_id,  **kwargs):
        payload = {'message_name': 'GET_CITY', 'user_id': user_id}
        headers = {'content-type': 'application/json'}

        with self.client.request(
                method, path,
                data=dumps(payload),
                headers=headers,
                catch_response=True, **kwargs
        ) as resp:
            if resp.status_code != expected_status:
                resp.failure(f'expected status {expected_status}, '
                             f'got {resp.status_code}')
            logging.info(
                'round %r: %s %s, http status %d (expected %d), took %rs',
                self.round, method, path, resp.status_code, expected_status,
                resp.elapsed.total_seconds()
            )
            return resp

    def get_city(self, user_id):
        url = url_for(GetUserCity.URL_PATH)
        self.request('POST', url, HTTPStatus.OK, user_id,
                     name='/get_city/')

    @task
    def workflow(self):
        self.round += 1
        import_id = self.create_id()
        self.get_city(import_id)


class WebsiteUser(HttpUser):
    tasks = [AnalyzerTaskSet]
    wait_time = constant(1)
