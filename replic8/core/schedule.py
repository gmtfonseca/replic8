import time
from threading import Thread
from enum import Enum


class SchedulerState(Enum):
    UNINITIALIZED = 0
    IDLE = 1
    COPYING = 2


class Scheduler(Thread):
    def __init__(self, copier, delay):
        super().__init__()
        # super().setDaemon(True)
        self._copier = copier
        self._delay = delay
        self._state = SchedulerState.UNINITIALIZED
        self._abort = False

    def run(self):
        while True:
            if self._abort:
                return
            self._checkSchedule()
            time.sleep(self._delay)

    def _checkSchedule(self):
        if self._state == SchedulerState.IDLE and self._timeToCopy():
            self._copyFiles()

    def _copyFiles(self):
        try:
            self._state = SchedulerState.COPYING
            self._copier.copy()
        except Exception as err:
            print(err)

    def _timeToCopy(self):
        return True

    def start(self):
        self._state = SchedulerState.IDLE
        super().start()

    def abort(self):
        self._abort = True
