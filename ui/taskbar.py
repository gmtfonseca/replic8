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
                            TaskBarInteractor(),
                            taskbarHandler)


class TaskbarHandler:
    def __init__(self, onSettings, onExit):
        self.onSettings = onSettings
        self.onExit = onExit


class TaskBarIconView(wx.adv.TaskBarIcon):
    def __init__(self, frame, icon):
        super().__init__()
        self.frame = frame
        self._createPopupMenu()

    def _createPopupMenu(self):
        self.popupMenu = wx.Menu()
        self.menuItemSettings = self.popupMenu.Append(-1, 'Configurações')
        self.popupMenu.AppendSeparator()
        self.menuItemExit = self.popupMenu.Append(wx.ID_EXIT, 'Sair')

    def showPopupMenu(self):
        self.PopupMenu(self.popupMenu)

    def setIconAndTooltip(self, icon, tooltip):
        self.SetIcon(icon, tooltip)


class TaskBarPresenter:
    def __init__(self, view, interactor, taskbarHandler):
        self._view = view
        interactor.Install(self, self._view)
        self._taskbarHandler = taskbarHandler
        self.initView()

    def initView(self):
        self._state = SchedulerState.UNINITIALIZED
        self.loadViewFromModel()

    def updateState(self, state):
        self._state = state
        self.loadViewFromModel()

    def showPopupMenu(self):
        self._view.PopupMenu(self._view.popupMenu)

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

    def handleSingleRightClick(self):
        self._view.showPopupMenu()

    def showSettings(self):
        self._taskbarHandler.onSettings()

    def exit(self):
        self._taskbarHandler.onExit()

    def destroy(self):
        self._view.Destroy()


class TaskBarInteractor:

    def Install(self, presenter, view):
        self._presenter = presenter
        self._view = view

        self._view.Bind(wx.adv.EVT_TASKBAR_RIGHT_UP, self.OnRightClickTaskBarIcon)
        self._view.popupMenu.Bind(wx.EVT_MENU, self.OnSettings, self._view.menuItemSettings)
        self._view.popupMenu.Bind(wx.EVT_MENU, self.OnExit, self._view.menuItemExit)

    def OnRightClickTaskBarIcon(self, evt):
        self._presenter.handleSingleRightClick()

    def OnSettings(self, evt):
        self._presenter.showSettings()

    def OnExit(self, evt):
        self._presenter.exit()
