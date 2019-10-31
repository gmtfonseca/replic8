import wx

from replic8.core.schedule import EVT_SCHEDULER, SchedulerState
from ui import taskbar, settings


def start(app):
    return MainPresenter(MainFrame(), MainInteractor(), app)


class MainFrame(wx.Frame):

    def __init__(self):
        super().__init__(None)

    def destroy(self):
        self.Destroy()


class MainPresenter:
    def __init__(self, view, interactor, app):
        self._view = view
        interactor.Install(self, self._view)
        self._app = app
        self._createTaskBarIcon()
        self._app.createSchedulerManager(self._view)
        self._activeWindow = None
        self._initialize()

    def _createTaskBarIcon(self):
        taskbarHandler = taskbar.TaskbarHandler(self.showSettings, self.quit, self.forceCopy)
        self._taskBarIcon = taskbar.create(self._view, taskbarHandler)

    def _initialize(self):
        if not self._app.ready():
            self.showSettings()
        else:
            self._app.schedulerManager.start()

    def _setActiveWindowAndShow(self, window):
        self._activeWindow = window
        self._activeWindow.show()

    def _hasActiveWindow(self):
        return self._activeWindow and self._activeWindow.isActive()

    def handleSchedulerStateUpdate(self, evt):
        self.updateChildren(evt)

    def updateChildren(self, evt):
        self.updateTaskBarIcon(evt.state, evt.title, evt.text)

    def updateTaskBarIcon(self, state, title, text):
        self._taskBarIcon.updateState(state)
        if title:
            flags = wx.ICON_ERROR if state == SchedulerState.ERROR else wx.ICON_INFORMATION
            self._taskBarIcon.showBaloon(title, text, flags)

    def showSettings(self):
        if not self._hasActiveWindow():
            self._activeWindow = settings.create(None,
                                                 self._app.scheduleModel,
                                                 self._app.copyModel,
                                                 self._app.schedulerManager,
                                                 self._app.logger)
        self._activeWindow.show()

    def forceCopy(self):
        self._app.schedulerManager.forceCopy()

    def quit(self):
        self._taskBarIcon.destroy()
        self._view.destroy()


class MainInteractor:
    def Install(self, presenter, view):
        self._presenter = presenter
        self._view = view

        self._view.Bind(EVT_SCHEDULER, self.OnUpdateSchedulerState)

    def OnUpdateSchedulerState(self, evt):
        self._presenter.handleSchedulerStateUpdate(evt)
