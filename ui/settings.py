import wx


def show(parent):
    return SettingsPresenter(SettingsDialog(parent, 'Replic8'),
                             SettingsInteractor())


class SettingsDialog(wx.Dialog):

    def __init__(self, parent, title):
        super().__init__(parent=parent, title=title, size=(600, 500))
        self._initLayout()

    def _initLayout(self):
        self.SetAutoLayout(True)

    def quit(self):
        self.Destroy()

    def start(self):
        self.CenterOnScreen()
        self.Raise()
        self.ShowModal()


class SettingsPresenter:
    def __init__(self, view, interactor):
        self._view = view
        interactor.Install(self, self._view)
        self._view.start()


class SettingsInteractor:
    def Install(self, presenter, view):
        self._presenter = presenter
        self._view = view
