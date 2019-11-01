import gzip
import shutil


class Compression:

    @staticmethod
    def copyCompressed(fileInPath, fileOutPath):
        with open(str(fileInPath), 'rb') as fileIn:
            with gzip.open(str(fileOutPath) + '.gz', 'wb') as fileOut:
                shutil.copyfileobj(fileIn, fileOut)
