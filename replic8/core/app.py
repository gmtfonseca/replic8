from functools import partial

from replic8.core.schedule import Scheduler, SchedulerManager, NotInitializedError
from replic8.core.copy import Copier
from replic8.core.model import ScheduleModel, CopyModel
from replic8.core.logger import LoggerFactory


class App(object):
    def __init__(self, config):
        self._config = config
        self._scheduleModel = ScheduleModel(self._config['storage']['schedule_data_path'])
        self._copyModel = CopyModel(self._config['storage']['copy_data_path'])
        self._logger = self._createLogger()
        self._schedulerManager = None

    def _createLogger(self):
        if self._config['env'] == 'dev':
            logger = LoggerFactory.getDevLogger()
        elif self._config['env'] == 'prod':
            logger = LoggerFactory.getProdLogger(self._config['storage']['log_path'])
        else:
            logger = LoggerFactory.getRootLogger()
        return logger

    def createSchedulerManager(self, view):
        self._schedulerManager = SchedulerManager(partial(self._schedulerFactory, view))

    def _schedulerFactory(self, view):
        delay = self._config['scheduler']['delay']
        copier = Copier(self._copyModel)
        return Scheduler(view, copier, delay, self._scheduleModel, self._logger)

    def ready(self):
        return self._scheduleModel.copyInterval and self._copyModel.destination and len(self._copyModel.sources) > 0

    @property
    def schedulerManager(self):
        if not self._schedulerManager:
            raise NotInitializedError()

        return self._schedulerManager

    @property
    def scheduleModel(self):
        return self._scheduleModel

    @property
    def copyModel(self):
        return self._copyModel

    @property
    def logger(self):
        return self._logger
