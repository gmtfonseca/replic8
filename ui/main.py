import wx

from ui import taskbar, settings


def start(app):
    return MainPresenter(MainFrame(), MainInteractor(), app)


class MainFrame(wx.Frame):

    def __init__(self):
        super(MainFrame, self).__init__(None)

    def destroy(self):
        self.Destroy()


class MainPresenter:
    def __init__(self, view, interactor, app):
        self._view = view
        interactor.Install(self, self._view)
        self._app = app
        self._createTaskBarIcon()

    def _createTaskBarIcon(self):
        taskbarHandler = taskbar.TaskbarHandler(self.showSettings, self.quit)
        self._taskBarIcon = taskbar.create(self._view, taskbarHandler)

    def updateChildrenState(self, syncState):
        self._taskBarIcon.updateState(syncState)

    def showSettings(self):
        settings.show(self._view)

    def quit(self):
        self._taskBarIcon.destroy()
        self._view.destroy()


class MainInteractor:
    def Install(self, presenter, view):
        self._presenter = presenter
        self._view = view
