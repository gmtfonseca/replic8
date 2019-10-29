import time
from threading import Thread
from enum import Enum
from datetime import date


class SchedulerState(Enum):
    UNINITIALIZED = 0
    IDLE = 1
    COPYING = 2


class Schedule(object):
    def __init__(self, copyInterval, lastCopy):
        self.copyInterval = copyInterval
        self.lastCopy = lastCopy

    @classmethod
    def empty(cls):
        return cls(None, None)


class Scheduler(Thread):
    def __init__(self, copier, delay, scheduleModel, logger):
        super().__init__()
        super().setDaemon(True)
        self._copier = copier
        self._delay = delay
        self._scheduleModel = scheduleModel
        self._logger = logger
        self._state = SchedulerState.UNINITIALIZED
        self._abort = False

    def run(self):
        while True:
            if self._abort:
                return
            self._checkSchedule()
            time.sleep(self._delay)

    def _checkSchedule(self):
        if self._timeToCopy():
            self._copyFiles()

    def _copyFiles(self):
        try:
            self._logger.info(f'Copying files { self._copier.sources } to folder { self._copier.destination }')
            self._state = SchedulerState.COPYING
            self._copier.perform()
            self._scheduleModel.setLastCopy(date.today())
            self._logger.info('Copy succeeded')
            self._state = SchedulerState.IDLE
        except Exception as err:
            self._logger.exception(err)
            self.abort()

    def _timeToCopy(self):
        if not self._scheduleModel.lastCopy:
            return True

        if not self._scheduleModel.copyInterval:
            return False

        today = date.today()
        interval = today - self._scheduleModel.lastCopy
        return interval.days >= self._scheduleModel.copyInterval

    def start(self):
        self._state = SchedulerState.IDLE
        super().start()

    def abort(self):
        self._abort = True
