from pathlib import Path
from shutil import copyfile

from replic8.lib.compression import Compression


class Source(object):
    '''
    Source is a list with multiple files path
    '''

    def __init__(self, paths=[]):
        self._paths = self._initialize(paths)

    def _initialize(self, paths):
        return [Path(path) for path in paths]

    @property
    def paths(self):
        return self._paths

    @paths.setter
    def paths(self, paths):
        self._paths = self._initialize(paths)

    @classmethod
    def empty(cls):
        return cls([])


class Destination(object):
    '''
    Destination is a single folder path
    '''

    def __init__(self, path):
        self._path = Path(path) if path else ''

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        self._path = Path(path)

    @classmethod
    def empty(cls):
        return cls('')


class Copy(object):
    def __init__(self, source, destination):
        self._source = source
        self._destination = destination

    @property
    def sources(self):
        return self._source.paths

    @sources.setter
    def sources(self, paths):
        self._source.paths = paths

    @property
    def destination(self):
        return self._destination.path

    @destination.setter
    def destination(self, path):
        self._destination.path = path

    @classmethod
    def empty(cls):
        return cls(Source.empty(), Destination.empty())


class Copier(object):
    def __init__(self, copyModel):
        self._copyModel = copyModel

    def perform(self):
        destFolder = self._copyModel.destination
        sources = self._copyModel.sources
        for source in sources:
            destFile = destFolder / source.name
            Compression.copyCompressed(source, destFile)

    @property
    def sources(self):
        return [source.as_posix() for source in self._copyModel.sources]

    @property
    def destination(self):
        return self._copyModel.destination.as_posix()
