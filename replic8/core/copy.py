from shutil import copyfile


class Copier(object):
    def __init__(self, pathSrc, pathDest):
        self._pathSrc = pathSrc
        self._pathDest = pathDest

    def copy(self):
        copyfile(self._pathSrc, self._pathDest)
