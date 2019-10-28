import time
from threading import Thread


class Scheduler(Thread):
    def __init__(self, copier, delay):
        super().__init__()
        # super().setDaemon(True)
        self._copier = copier
        self._delay = delay
        self._abort = False

    def run(self):
        while True:
            if self._abort:
                return
            self._checkSchedule()
            time.sleep(self._delay)

    def _checkSchedule(self):
        if self._hasToCopy():
            self._copier.copy()

    def _hasToCopy(self):
        return True

    def start(self):
        super().start()

    def abort(self):
        self._abort = True
