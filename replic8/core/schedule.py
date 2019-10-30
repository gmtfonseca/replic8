import time
from pathlib import Path
from threading import Thread
from enum import Enum
from datetime import date

import wx

EVT_TYPE_SCHEDULER = wx.NewEventType()
EVT_SCHEDULER = wx.PyEventBinder(EVT_TYPE_SCHEDULER, 2)


class SchedulerEvent(wx.PyCommandEvent):
    def __init__(self, type, id, state, msg):
        super().__init__(type, id)
        self.state = state
        self.msg = msg


class NotInitializedError(Exception):
    pass


class SchedulerState(Enum):
    UNINITIALIZED = 0
    IDLE = 1
    COPYING = 2
    ERROR = 3


class Schedule(object):
    def __init__(self, copyInterval, lastCopy):
        self.copyInterval = copyInterval
        self.lastCopy = lastCopy

    @classmethod
    def empty(cls):
        return cls(None, None)


class SchedulerManager:
    def __init__(self, schedulerFactory):
        self._schedulerFactory = schedulerFactory
        self._scheduler = None

    def start(self):
        self._scheduler = self._schedulerFactory()
        self._scheduler.start()

    def restart(self):
        self.stop()
        self.start()

    def stop(self):
        self._scheduler.abort()


class Scheduler(Thread):
    def __init__(self, view, copier, delay, scheduleModel, logger):
        super().__init__()
        super().setDaemon(True)
        self._view = view
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
            fileNames = ','.join([Path(f).name for f in self._copier.sources])
            self._setStateAndPostEvent(SchedulerState.COPYING, f'Copiando o(s) arquivo(s) { fileNames } para a pasta { self._copier.destination }')
            self._copier.perform()
            self._scheduleModel.setLastCopy(date.today())
            self._setStateAndPostEvent(SchedulerState.IDLE, 'Arquivos copiados com sucesso.')
            self._logger.info('Copy succeeded')
        except Exception as err:
            self._setStateAndPostEvent(SchedulerState.ERROR)
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

    def _setStateAndPostEvent(self, state, msg=''):
        self._state = state
        evt = SchedulerEvent(EVT_TYPE_SCHEDULER, -1, self._state, msg)
        wx.PostEvent(self._view, evt)

    def start(self):
        self._state = SchedulerState.IDLE
        super().start()

    def abort(self):
        self._abort = True
