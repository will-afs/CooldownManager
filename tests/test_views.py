import json
import threading
import time
from datetime import datetime
from venv import create

import pytest
import toml

from flaskapp import create_app
from tests.conftest import client  # ,create_app_for_tc, test_client

project_config = toml.load("project_config.toml")
ref_cooldown_delay = project_config["time"]["cooldown_delay"]
network_related_tolerance = project_config["time"]["network_related_tolerance"]


def get_token(client, path, i, request_times, responses, response_times):
    request_times[i] = time.time()
    responses[i] = client.get(path)
    response_times[i] = time.time()
    return

def test_get_token_view(client): #app, 
    n_requests = 2
    threads = [None] * n_requests
    request_times = [None] * n_requests
    responses = [None] * n_requests
    response_times = [None] * n_requests
    # clients = [None] * n_requests
    for i in range(0, n_requests):
        # clients[i] = app.test_client()
        threads[i] = threading.Thread(
            target=get_token,
            args=(client, "/", i, request_times, responses, response_times), #clients[i]
            daemon=True,
        )

    for i in range(0, n_requests):
        # Dedicated loop in order to start the threads approximately at the same time
        threads[i].start()
        time.sleep(0.5) # to make sure clients send their request in the right order

    for i in range(0, n_requests):
        # Dedicated loop in order to end the threads approximately at the same time
        threads[i].join()

    for i in range(0, n_requests):
        assert responses[i].status == "200 OK"

    # Unfortunately, the server can only handle requests one by one
    assert abs(response_times[1] - response_times[0]) >= ref_cooldown_delay
    assert abs(response_times[1] - response_times[0]) == pytest.approx(
            ref_cooldown_delay, abs=network_related_tolerance
        )

        # if i == 0:
        #     # no cooldown needed : response received directly
        #     assert response_times[i] - request_times[i] == pytest.approx(
        #         i * ref_cooldown_delay, abs=(i + 1) * network_related_tolerance
        #     )
        # else:
        #     # cooldown needed : time delta between two tokens must be superior to ref_cooldown_delay
        #     assert response_times[i] - response_times[i-1] >= ref_cooldown_delay
        #     # and time delta between two tokens must be approximately ref_cooldown_delay
        #     assert response_times[i] - response_times[i-1] == pytest.approx(
        #     ref_cooldown_delay, abs=(i + 1) * network_related_tolerance
        # )
