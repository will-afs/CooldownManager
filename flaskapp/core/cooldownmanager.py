import threading
import time

import toml
from singleton_decorator import singleton


@singleton
class CoolDownManager:
    def __init__(self):
        project_config = toml.load("project_config.toml")
        self._cooldown_needed = False
        self._cooldown_delay = project_config["time"]["countdown_delay"]
        self._time_step = project_config["time"]["time_step"]

    def _cooldown(self):
        print("Cooling down...")
        time.sleep(self._cooldown_delay)
        self._cooldown_needed = False
        print("Refreshed !")

    def _run(self):
        while True:
            if self._cooldown_needed is True:
                print("Cooldown needed")
                self._cooldown()
            else:
                time.sleep(self._time_step)

    def get_token(self) -> bool:
        if self._cooldown_needed is False:
            self._cooldown_needed = True
            print("Generated token")
            return True
        else:
            while self._cooldown_needed is True:
                print("Waiting for cooldown to generate token...")
                while self._cooldown_needed is True:
                    time.sleep(self._time_step)
            return self.get_token()


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
    request_time = time.time()
    cooldownmanager.get_token()
    response_time = time.time()
    print(
        "Obtained first token after {} s\n".format(
            round(response_time - request_time, 2)
        )
    )

    print("Joining run thread")
    # Do not wait for run_thread to end (infinite while loop)
    run_thread.join(timeout=0)
    print("End of the program")
