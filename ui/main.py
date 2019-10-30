import wx

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
        self._initialize()

    def _createTaskBarIcon(self):
        taskbarHandler = taskbar.TaskbarHandler(self.showSettings, self.quit)
        self._taskBarIcon = taskbar.create(self._view, taskbarHandler)

    def _initialize(self):
        if not self._app.ready():
            settings.show(self._view,
                          self._app.scheduleModel,
                          self._app.copyModel,
                          self._app.schedulerManager,
                          self._app.logger)
        else:
            self._app.schedulerManager.start()

    def updateChildrenState(self, syncState):
        self._taskBarIcon.updateState(syncState)

    def showSettings(self):
        settings.show(self._view, self._app.scheduleModel, self._app.copyModel, self._app.logger)

    def quit(self):
        self._taskBarIcon.destroy()
        self._view.destroy()


class MainInteractor:
    def Install(self, presenter, view):
        self._presenter = presenter
        self._view = view
