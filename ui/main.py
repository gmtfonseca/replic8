import wx

from ui import taskbar


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
        self._taskBarIcon = taskbar.create(self._view)
        print(self._taskBarIcon)

    def updateChildrenState(self, syncState):
        self._taskBarIcon.updateState(syncState)

    def _removeTaskBarIcon(self):
        if self._taskBarIcon:
            self._taskBarIcon.quit()

    def quit(self):
        self._removeTaskBarIcon()
        self._view.destroy()


class MainInteractor:
    def Install(self, presenter, view):
        self._presenter = presenter
        self._view = view
