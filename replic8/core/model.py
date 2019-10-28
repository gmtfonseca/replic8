import json
from datetime import datetime
from pathlib import Path


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
        self._schedule._copyInterval = copyInterval
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
        if isinstance(o, datetime):
            return o.__str__()

    @property
    def lastCopy(self):
        return self._schedule.lastCopy

    @property
    def copyInterval(self):
        return self._schedule.copyInterval


class CopyModel(object):
    def __init__(self, path):
        pass
