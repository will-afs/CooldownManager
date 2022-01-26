import time
from datetime import datetime, timedelta
import time
import toml
import threading
from singleton_decorator import singleton


@singleton
class CoolDownManager():
    def __init__(self):
        self._cooldown_needed = False
        project_config = toml.load('project_config.toml')
        self._cooldown_delay = project_config['time']['countdown_delay']
        self._time_step = project_config['time']['time_step']

    def _cooldown(self):
        print('Cooling down...')
        time.sleep(self._cooldown_delay)
        self._cooldown_needed = False
        print('Refreshed !')

    def get_token(self) -> bool:
        if self._cooldown_needed == False:
            self._cooldown_needed = True
            print('Generated token')
            return True            
        else:
            while self._cooldown_needed == True:
                print('Waiting for cooldown to generate token...')
                while self._cooldown_needed == True:
                    time.sleep(self._time_step)
            return self.get_token()
            
    def _run(self):
        while True:
            if self._cooldown_needed == True:
                print('Cooldown needed')
                self._cooldown()
            else:
                time.sleep(self._time_step)

if __name__ == '__main__':
    # Usage example
    cooldownmanager = CoolDownManager()
    print('\nInstanciated CoolDownManager\n')

    run_thread = threading.Thread(target=cooldownmanager._run, args=(), daemon=True)
    run_thread.start()
    print('Started run_thread\n')

    start_date = time.time()

    # First token is returned directly : no need to cooldown at first
    print('Asking for first token at {} s'.format(round(time.time()-start_date, 2)))
    cooldownmanager.get_token()
    print('Obtained first token at {} s\n'.format(round(time.time()-start_date, 2)))

    # Second token cannot be returned directly : need to respect cooldown delay
    print('Asking for second token at {} s'.format(round(time.time()-start_date, 2)))
    cooldownmanager.get_token()
    print('Obtained second token at {} s\n'.format(round(time.time()-start_date, 2)))

    print('Joining run thread')
    run_thread.join(timeout=0) # Do not wait for run_thread to end before destroying it (infinite while loop)
    print('End of the program')  
