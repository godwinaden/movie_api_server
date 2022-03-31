import time
import tracemalloc

import pytest
from starlette.testclient import TestClient
from main import app

tracemalloc.start()
client = TestClient(app)
durations: list = []


def timed(func):
    """
    records approximate durations of test function calls
    """

    def wrapper(*args, **kwargs):
        start = time.time()
        print('{name:<30} started'.format(name=func.__name__))
        result = func(*args, **kwargs)
        duration = "{name:<30} finished in {elapsed:.2f} seconds".format(
            name=func.__name__, elapsed=time.time() - start
        )
        print(duration)
        durations.append(duration)
        return result

    return wrapper


class TestAPIs:
    my_api_public_key: str = ""
    my_api_secret_key: str = ""

    @pytest.fixture
    def create_new_movie(self):
        return dict(title="Mission Impossible", subtitle="Beyond Missions", price=345.00, description="This is")

    @pytest.fixture
    def create_new_key(self):
        return dict(secret="", public="", domain="http://localhost:4600")

    def test_check_unauthorized_cannot_create_movies(self, create_new_movie):
        response = client.post("/movies", json=create_new_movie)
        assert response.status_code == 401 or response.status_code == 403

    def test_create_api_key(self, create_new_key):
        response = client.post("/keys", json=create_new_key)
        assert response.status_code == 201
        json_resp = response.json()
        assert 'secret' in json_resp
        assert 'public' in json_resp
        self.my_api_secret_key = json_resp['secret']
        self.my_api_public_key = json_resp['public']
        print(f"Bearer {self.my_api_public_key}")
        assert len(self.my_api_public_key) >= 50
        assert len(self.my_api_secret_key) >= 50

    def test_create_movie(self, create_new_movie):
        headers = {
            "Content-Type": "application/json",
            "authorization": "Bearer " + self.my_api_public_key,
        }
        response = client.post("/movies", json=create_new_movie, headers=headers)
        assert response.status_code == 201
        json_resp = response.json()
        print(f"Movie Response: {json_resp}")

    def test_movies_retriever(self):
        response = client.get("/movies")
        assert response.status_code == 200
        json_resp = response.json()
        assert isinstance(json_resp, list)
        assert len(json_resp) > 0
        print(f"Movie Response: {json_resp}")
