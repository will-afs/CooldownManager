import threading
import time

import toml
from singleton_decorator import singleton


@singleton
class CoolDownManager:
    def __init__(self):
        self._cooldown_lock = threading.Lock()
        self._get_token_lock = threading.Lock()
        project_config = toml.load("project_config.toml")
        self._cooldown_needed = False
        self._cooldown_delay = project_config["time"]["cooldown_delay"]
        self._time_step = project_config["time"]["time_step"]

    def _cooldown(self):
        with self._cooldown_lock:
            # print("Cooling down...")
            time.sleep(self._cooldown_delay)
            self._cooldown_needed = False
            # print("Refreshed !")

    def _run(self):
        while True:
            if self._cooldown_needed is True:
                # print("Cooldown needed")
                self._cooldown()
            else:
                time.sleep(self._time_step)

    def get_token(self) -> bool:
        with self._get_token_lock:
            if self._cooldown_needed is False:
                self._cooldown_needed = True
                
            else:
                while self._cooldown_needed is True:
                    # print("Waiting for cooldown to generate token...")
                    while self._cooldown_needed is True:
                        time.sleep(self._time_step)
        # print("Generated token")
        return True


if __name__ == "__main__":
    # Usage example
    cooldownmanager = CoolDownManager()
    print("\nInstanciated CoolDownManager\n")

    run_thread = threading.Thread(target=cooldownmanager._run, args=(), daemon=True)
    run_thread.start()
    print("Started run_thread\n")

    # First token is returned directly : no need to cooldown at first
    print("Asking for first token ...")
    request_time = time.time()
    cooldownmanager.get_token()
    response_time = time.time()
    print(
        "Obtained first token after {} s\n".format(
            round(response_time - request_time, 2)
        )
    )

    # Second token cannot be returned directly : need to respect cooldown delay
    print("Asking for second token ...")
    get_second_token_thread = threading.Thread(target=cooldownmanager.get_token, args=(), daemon=True)
    get_second_token_thread.start()
    print("Started run_thread\n")


    print("Asking for third token ...")
    request_time = time.time()
    cooldownmanager.get_token()
    response_time = time.time()
    print(
        "Obtained third token after {} s\n".format(
            round(response_time - request_time, 2)
        )
    )

    get_second_token_thread.join()
    
    print("Joining run thread")
    # Do not wait for run_thread to end (infinite while loop)
    run_thread.join(timeout=0)
    print("End of the program")
