import wx
import wx.adv
import platform

from replic8.core.schedule import SchedulerState
from ui import assets


icon = assets.image('replic8_win.png')

if platform.system() != 'Windows':
    icon = assets.image('replic8.png')


def create(frame, taskbarHandler):
    return TaskBarPresenter(TaskBarIconView(frame, wx.Icon(icon)),
                            taskbarHandler)


class TaskbarHandler:
    def __init__(self, onSettings, onExit, onForceCopy):
        self.onSettings = onSettings
        self.onExit = onExit
        self.onForceCopy = onForceCopy


class TaskBarIconView(wx.adv.TaskBarIcon):
    def __init__(self, frame, icon):
        super().__init__()
        self.frame = frame

    def showPopupMenu(self):
        self.PopupMenu(self.popupMenu)

    def setIconAndTooltip(self, icon, tooltip):
        self.SetIcon(icon, tooltip)


class TaskBarPresenter:
    def __init__(self, view, taskbarHandler):
        self._view = view
        self._taskbarHandler = taskbarHandler
        self.initView()

    def initView(self):
        self._state = SchedulerState.UNINITIALIZED
        self._view.CreatePopupMenu = self._createPopupMenu
        self.loadViewFromModel()

    def updateState(self, state):
        self._state = state
        self.loadViewFromModel()

    def showPopupMenu(self):
        self._view.PopupMenu(self._view.popupMenu)

    def _createPopupMenu(self):
        popupMenu = wx.Menu()
        menuItemSettings = popupMenu.Append(-1, 'Configurações')
        menuItemForceCopy = popupMenu.Append(-1, 'Forçar cópia')
        popupMenu.AppendSeparator()
        menuItemExit = popupMenu.Append(wx.ID_EXIT, 'Sair')

        popupMenu.Bind(wx.EVT_MENU, self.OnShowSettings, menuItemSettings)
        popupMenu.Bind(wx.EVT_MENU, self.OnForceCopy, menuItemForceCopy)
        popupMenu.Bind(wx.EVT_MENU, self.OnExit, menuItemExit)

        return popupMenu

    def loadViewFromModel(self):
        if self._state == SchedulerState.UNINITIALIZED:
            self._view.SetIcon(wx.Icon(icon), 'Replic8\nNão inicializado')
        elif self._state == SchedulerState.ERROR:
            self._view.SetIcon(wx.Icon(icon), 'Replic8\nErro ao copiar arquivos')
        elif self._state == SchedulerState.COPYING:
            self._view.SetIcon(wx.Icon(icon), 'Replic8\nCopiando arquivos...')
        else:
            self._view.SetIcon(wx.Icon(icon), 'Replic8')

    def showBaloon(self, msg):
        self._view.ShowBalloon('Replic8', msg)

    def _showSettings(self):
        self._taskbarHandler.onSettings()

    def _forceCopy(self):
        self._taskbarHandler.onForceCopy()

    def exit(self):
        self._taskbarHandler.onExit()

    def destroy(self):
        self._view.Destroy()

    def OnShowSettings(self, evt):
        self._showSettings()

    def OnForceCopy(self, evt):
        self._forceCopy()

    def OnExit(self, evt):
        self.exit()
