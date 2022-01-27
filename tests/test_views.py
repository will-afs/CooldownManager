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
ref_cooldown_delay = project_config["time"]["countdown_delay"]
network_related_tolerance = project_config["time"]["network_related_tolerance"]


def get_token(client, path, i, request_times, responses, response_times):
    request_times[i] = time.time()
    responses[i] = client.get(path)
    response_times[i] = time.time()

    # Snippet in case found a way to "app.run(threaded=True)" with pytest

    # thread = threading.Thread(target=client.get, args=(path,), daemon=True)
    # request_times[i] = time.time()
    # thread.start()
    # thread.join()
    # response_times[i] = time.time()
    # responses[i].status = "200 OK" # fake, to remove


def test_get_token_view(app):
    threads = [None] * 3
    request_times = [None] * 3
    responses = [None] * 3
    response_times = [None] * 3
    clients = [None] * 3

    for i in range(0, 3):
        clients[i] = app.test_client()
        threads[i] = threading.Thread(
            target=get_token,
            args=(clients[i], "/", i, request_times, responses, response_times),
            daemon=True,
        )

    for i in range(0, 3):
        # Dedicated loop in order to start the threads approximately at the same time
        threads[i].start()
        print("thread n°{} started at : {}".format(i, datetime.now()))

    for i in range(0, 3):
        # Dedicated loop in order to end the threads approximately at the same time
        threads[i].join()
        print("thread n°{} ended at : {}".format(i, datetime.now()))

    for i in range(0, 3):
        assert responses[i].status == "200 OK"
        expected_time_delta = i * ref_cooldown_delay
        # Unfortunately, the server can only handle requests one by one
        assert response_times[i] - request_times[i] >= expected_time_delta
        assert response_times[i] - request_times[i] == pytest.approx(
            expected_time_delta, abs=(i + 1) * network_related_tolerance
        )

        # Snippet in case found a way to "app.run(threaded=True)" with pytest

        # if i == 0:
        #     # no cooldown needed : token should be returned directly
        #     assert response_times[i] - request_times[i] == pytest.approx(0, abs=network_related_tolerance)
        # else:
        #     # cooldown needed : token should only be returned after cooldown delay
        #     assert response_times[i] - request_times[i] >= ref_cooldown_delay
        #     assert response_times[i] - request_times[i] == pytest.approx(ref_cooldown_delay, abs=network_related_tolerance)
