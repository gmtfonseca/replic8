import wx


def show(parent):
    return SettingsPresenter(SettingsDialog(parent, 'Configurações'),
                             SettingsInteractor())


class SettingsDialog(wx.Dialog):

    def __init__(self, parent, title):
        super().__init__(parent=parent, title=title, size=(500, 350))
        self._initLayout()

    def _initLayout(self):
        panel = wx.Panel(self)
        # panel.SetBackgroundColour(wx.YELLOW)

        lblInterval = wx.StaticText(panel, -1, 'Intervalo (dias)')
        self.txtInterval = wx.TextCtrl(panel, -1, '')

        lblDest = wx.StaticText(panel, -1, 'Pasta de destino')
        self.txtDest = wx.TextCtrl(panel, -1, '')
        self.btnDest = wx.Button(panel, -1, 'Selecionar', (50, 50))

        lblSource = wx.StaticText(panel, -1, 'Origem')
        self.txtSource = wx.TextCtrl(panel, -1, '')
        self.btnSource = wx.Button(panel, -1, 'Adicionar arquivo', (50, 50))
        self.listSources = wx.ListCtrl(panel, -1,
                                       style=wx.LC_REPORT
                                       | wx.BORDER_NONE
                                       | wx.LC_EDIT_LABELS
                                       )

        self.listSources.InsertColumn(0, "Caminho")
        self.listSources.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)

        self.btnOk = wx.Button(panel, -1, 'OK', (50, 50))
        self.btnCancel = wx.Button(panel, -1, 'Cancelar', (50, 50))

        intervalSizer = wx.BoxSizer(wx.HORIZONTAL)
        intervalSizer.Add(lblInterval)
        intervalSizer.Add(self.txtInterval, wx.SizerFlags(1).Border(wx.LEFT, 5))

        destSizer = wx.BoxSizer(wx.HORIZONTAL)
        destSizer.Add(lblDest)
        destSizer.Add(self.txtDest, wx.SizerFlags(0).Expand().Border(wx.LEFT, 5))
        destSizer.Add(self.btnDest, wx.SizerFlags(0).Border(wx.LEFT, 5))

        sourceSizer = wx.BoxSizer(wx.HORIZONTAL)
        sourceSizer.Add(lblSource)
        sourceSizer.Add(self.txtSource, wx.SizerFlags(0).Border(wx.LEFT, 5))
        sourceSizer.Add(self.btnSource, wx.SizerFlags(0).Border(wx.LEFT, 5))

        footerSizer = wx.BoxSizer(wx.HORIZONTAL)
        footerSizer.Add(self.btnOk)
        footerSizer.Add(self.btnCancel, wx.SizerFlags(0).Border(wx.LEFT, 5))

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(intervalSizer, wx.SizerFlags(0).Expand())
        mainSizer.Add(destSizer, wx.SizerFlags(0).Expand().Border(wx.TOP, 10))
        mainSizer.Add(sourceSizer, wx.SizerFlags(0).Expand().Border(wx.TOP, 10))
        mainSizer.Add(self.listSources, wx.SizerFlags(0).Expand().Border(wx.TOP, 10))
        mainSizer.Add(footerSizer, wx.SizerFlags(0).Right().Border(wx.TOP, 10))

        panelSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer.Add(mainSizer, wx.SizerFlags(0).Expand().Border(wx.ALL, 10))

        panel.SetSizer(panelSizer)

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
