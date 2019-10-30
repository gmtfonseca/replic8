import pickle
from pathlib import Path

from replic8.core.schedule import Schedule
from replic8.core.copy import Copy


class Model(object):
    def __init__(self, path):
        self._path = Path(path)

    def initialize(self, emptyObject):
        if not self._path.exists() or self._path.stat().st_size == 0:
            self.saveToDisk(emptyObject)

        return self.loadFromDisk()

    def saveToDisk(self, obj):
        if not self._path.parent.exists():
            self._path.parent.mkdir(parents=True, exist_ok=True)

        with self._path.open('wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

    def loadFromDisk(self):
        with open(self._path, 'rb') as f:
            return pickle.load(f)

    def removeFromDisk(self):
        if self._path.exists():
            self._path.unlink()


class CopyModel(Model):
    def __init__(self, path):
        super().__init__(path)
        self._copy = self.initialize(Copy.empty())

    def setSources(self, paths):
        self._copy.sources = paths
        self.saveToDisk(self._copy)

    def setDestination(self, path):
        self._copy.destination = path
        self.saveToDisk(self._copy)

    def clear(self):
        self._copy = Copy.empty()
        self.saveToDisk(self._copy)

    @property
    def sources(self):
        return self._copy.sources

    @property
    def destination(self):
        return self._copy.destination


class ScheduleModel(Model):
    def __init__(self, path):
        self._path = Path(path)
        self._schedule = self.initialize(Schedule.empty())

    def setLastCopy(self, lastCopy):
        self._schedule.lastCopy = lastCopy
        self.saveToDisk(self._schedule)

    def setCopyInterval(self, copyInterval):
        self._schedule.copyInterval = int(copyInterval)
        self.saveToDisk(self._schedule)

    def clear(self):
        self._schedule = Schedule.empty()
        self.saveToDisk(self._schedule)

    @property
    def copyInterval(self):
        return self._schedule.copyInterval

    @property
    def lastCopy(self):
        return self._schedule.lastCopy
