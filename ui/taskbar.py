import wx
import wx.adv
import platform

from ui import assets


def create(frame, taskbarHandler):
    icon = wx.Icon(assets.image('replic8_win.png'))
    if platform.system() != 'Windows':
        icon = wx.Icon(assets.image('replic8.png'))
    return TaskBarPresenter(TaskBarIconView(frame, icon),
                            TaskBarInteractor(),
                            taskbarHandler)


class TaskbarHandler:
    def __init__(self, onSettings, onExit):
        self.onSettings = onSettings
        self.onExit = onExit


class TaskBarIconView(wx.adv.TaskBarIcon):
    def __init__(self, frame, icon):
        super().__init__()
        self.SetIcon(icon, 'Replic8')
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
        self.loadViewFromModel()

    def updateState(self, state):
        self._state = state
        self.loadViewFromModel()

    def showPopupMenu(self):
        self._view.PopupMenu(self._view.popupMenu)

    def loadViewFromModel(self):
        # self._view.setIconAndTooltip(icon, 'Replic8')
        pass

    def handleSingleLeftClick(self):
        self._view.showPopupMenu()

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

        self._view.Bind(wx.adv.EVT_TASKBAR_LEFT_UP,
                        self.OnLeftClickTaskBarIcon)
        self._view.Bind(wx.adv.EVT_TASKBAR_RIGHT_UP,
                        self.OnRightClickTaskBarIcon)
        view.popupMenu.Bind(wx.EVT_MENU, self.OnSettings,
                            view.menuItemSettings)
        view.popupMenu.Bind(wx.EVT_MENU, self.OnExit, view.menuItemExit)

    def OnLeftClickTaskBarIcon(self, evt):
        self._presenter.handleSingleLeftClick()

    def OnRightClickTaskBarIcon(self, evt):
        self._presenter.handleSingleRightClick()

    def OnSettings(self, evt):
        self._presenter.showSettings()

    def OnExit(self, evt):
        self._presenter.exit()
