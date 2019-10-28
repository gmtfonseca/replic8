import time
import json
from threading import Thread
from enum import Enum
from datetime import date
from pathlib import Path


class SchedulerState(Enum):
    UNINITIALIZED = 0
    IDLE = 1
    COPYING = 2


class Schedule(object):
    def __init__(self, copyInterval, lastCopy):
        self.copyInterval = copyInterval
        self.lastCopy = lastCopy

    def toDict(self):
        return vars(self)

    @classmethod
    def fromJsonFile(cls, jsonFile):
        jsonDict = json.load(jsonFile)
        return cls(jsonDict['copyInterval'], jsonDict['lastCopy'])

    @classmethod
    def empty(cls):
        return cls('', '')


class ScheduleModel(object):
    def __init__(self, path):
        self._path = Path(path)
        self._schedule = self.load()

    def setLastCopy(self, lastCopy):
        self._schedule.lastCopy = lastCopy
        self.save()

    def setCopyInterval(self, copyInterval):
        self._schedule.copyInterval = copyInterval
        self.save()

    def save(self):
        if not self._path.parent.exists():
            self._path.parent.mkdir(parents=True, exist_ok=True)

        with self._path.open('w') as f:
            json.dump(self._schedule.toDict(), f, default=self._serializer)

    def load(self):
        if not self._path.exists():
            return Schedule.empty()

        with self._path.open() as f:
            schedule = Schedule.fromJsonFile(f)
            return schedule

    def _serializer(self, o):
        if isinstance(o, date):
            return o.__str__()

    @property
    def copyInterval(self):
        return self._schedule.copyInterval

    @property
    def lastCopy(self):
        return self._schedule.lastCopy


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
            self._logger.info('Copying')
            self._state = SchedulerState.COPYING
            self._copier.copy()
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
