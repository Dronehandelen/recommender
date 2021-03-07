import threading
import time

import schedule


class Crons(schedule.Scheduler):
    def __init__(self):
        super().__init__()

    def run(self, interval=1):
        cease_continuous_run = threading.Event()

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not cease_continuous_run.is_set():
                    self.run_pending()
                    time.sleep(interval)

        continuous_thread = ScheduleThread(daemon=True)
        continuous_thread.start()

        return cease_continuous_run
