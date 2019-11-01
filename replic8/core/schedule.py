import time
from pathlib import Path
from threading import Thread
from enum import Enum
from datetime import date

import wx

EVT_TYPE_SCHEDULER = wx.NewEventType()
EVT_SCHEDULER = wx.PyEventBinder(EVT_TYPE_SCHEDULER, 2)


class SchedulerEvent(wx.PyCommandEvent):
    def __init__(self, type, id, state, title, text):
        super().__init__(type, id)
        self.state = state
        self.title = title
        self.text = text


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

    def forceCopy(self):
        if not self._scheduler.isRunning():
            self.restart()

        self._scheduler.forceCopy()


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
        self._forceCopy = False

    def run(self):
        while True:
            if self._abort:
                break
            self._checkSchedule()
            time.sleep(self._delay)

    def _checkSchedule(self):
        if self._timeToCopy() or self._forceCopy:
            self._copyFiles()
            self._forceCopy = False

    def _copyFiles(self):
        try:
            self._logger.info(f'Copying files { self._copier.sources } to folder { self._copier.destination }')
            fileNames = ', '.join([Path(f).name for f in self._copier.sources])
            self._setStateAndPostEvent(SchedulerState.COPYING,
                                       'Aviso',
                                       f'Copiando o(s) arquivo(s) "{ fileNames }" para a pasta "{ self._copier.destination }".')
            self._copier.perform()
            self._scheduleModel.setLastCopy(date.today())
            self._setStateAndPostEvent(SchedulerState.IDLE,
                                       'Sucesso',
                                       'Arquivo(s) copiado(s) com sucesso.')
            self._logger.info('Copy succeeded')
        except Exception as e:
            if isinstance(e, FileNotFoundError):
                self._setStateAndPostEvent(SchedulerState.ERROR,
                                           'Erro',
                                           f'Arquivo "{ e.filename }" não foi encontrado.')
            else:
                self._setStateAndPostEvent(SchedulerState.ERROR,
                                           'Erro',
                                           'Ocorreu um erro inesperado ao copiar os arquivos.')
            self._logger.exception(e)
            self.abort()

    def _timeToCopy(self):
        if not self._scheduleModel.lastCopy:
            return True

        if not self._scheduleModel.copyInterval:
            return False

        today = date.today()
        interval = today - self._scheduleModel.lastCopy
        return interval.days >= self._scheduleModel.copyInterval

    def _setStateAndPostEvent(self, state, title='', text=''):
        self._state = state
        evt = SchedulerEvent(EVT_TYPE_SCHEDULER, -1, self._state, title, text)
        wx.PostEvent(self._view, evt)

    def start(self):
        self._setStateAndPostEvent(SchedulerState.IDLE)
        super().start()

    def abort(self):
        self._abort = True

    def forceCopy(self):
        self._forceCopy = True

    def isRunning(self):
        return not self._abort and self.is_alive()
