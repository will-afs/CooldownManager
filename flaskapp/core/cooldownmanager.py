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
        self._stopping = False
        self._cooldown_delay = project_config["time"]["cooldown_delay"]
        self._time_step = project_config["time"]["time_step"]
        self._run_thread = None

    def _cooldown(self):
        with self._cooldown_lock:
            # print("Cooling down...")
            time.sleep(self._cooldown_delay)
            self._cooldown_needed = False
            # print("Refreshed !")

    def _run(self):
        while not self._stopping:
            if self._cooldown_needed:
                # print("Cooldown needed")
                if not self._cooldown_lock.locked():
                    self._cooldown()
            else:
                time.sleep(self._time_step)
        if self._cooldown_needed:
            self._cooldown()
        
    def start(self) :
        if not self._run_thread:
            self._run_thread = threading.Thread(
                target=self._run, args=(), daemon=True
            )
            self._run_thread.start()

    def stop(self) :
        if self._run_thread and self._run_thread.is_alive():
            self._stopping = True
            self._run_thread.join()
            self._run_thread = None
            self._stopping = False

    def get_token(self) -> bool:
        with self._get_token_lock:
            if self._run_thread and not self._stopping:
                if self._cooldown_needed is False:
                    self._cooldown_needed = True
                else:
                    while self._run_thread and self._cooldown_needed :
                        time.sleep(self._time_step)
                    self._cooldown_needed = True
                # print("Generated token")
                return True
            else:
                return False            


if __name__ == "__main__":
    # Usage example
    cooldownmanager = CoolDownManager()
    print("\nInstanciated CoolDownManager\n")

    cooldownmanager.start()
    print("Started run_thread\n")

    # First token is returned directly : no need to cooldown at first
    get_token_threads = []
    request_times = [None]*2
    response_times = [None]*2
    for i in range(0,2):
        get_token_threads.append(threading.Thread(target=cooldownmanager.get_token, args=()))

    for i in range(0,2):
        print("Asking for token n°{}...".format(i))
        request_times[i] = time.time()
        get_token_threads[i].start()

    for i in range(0,2):
        get_token_threads[i].join()
        response_times[i] = time.time()
        print("Obtained token n°{} after {} s ...".format(
                i,
                round(response_times[i] - request_times[i], 2)
            )
        )
    
    cooldownmanager.stop()

