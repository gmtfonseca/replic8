import json
from pathlib import Path
from shutil import copyfile


class Source(object):
    '''
    Source is a list with multiple files path
    '''

    def __init__(self, paths=[]):
        self._paths = self.initPaths(paths)

    def initPaths(self, paths):
        paths = []
        for path in paths:
            paths.append(Path(path))

        return paths

    def add(self, path):
        self._paths.append(Path(path))

    @property
    def paths(self):
        return self._paths


class Destination(object):
    '''
    Destination is a single folder path
    '''

    def __init__(self, path):
        self._path = Path(path)

    @property
    def path(self):
        return self._path


class Copy(object):
    def __init__(self, source, destination):
        self._source = source
        self._destination = destination

    @classmethod
    def fromJsonFile(cls, jsonFile):
        # TODO - Implement
        jsonDict = json.load(jsonFile)
        return cls(jsonDict['pathSrc'], jsonDict['pathDest'])

    @classmethod
    def empty(cls):
        return cls('', '')


class CopyModel(object):
    def __init__(self, path):
        self._path = path
        self._copy = Copy.empty()


class Copier(object):
    def __init__(self, copyModel):
        self._copy = copyModel.load()

    def perform(self):
        for path in self._copy.paths:
            copyfile(self._pathSrc, self._pathDest)
