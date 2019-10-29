import wx


def show(parent):
    return SettingsPresenter(SettingsDialog(parent, 'Configurações'),
                             SettingsInteractor())


class SettingsDialog(wx.Dialog):

    def __init__(self, parent, title):
        super().__init__(parent=parent, title=title, size=(500, 360))
        self._initLayout()

    def _initLayout(self):
        panel = wx.Panel(self)
        # panel.SetBackgroundColour(wx.YELLOW)

        lblInterval = wx.StaticText(panel, -1, 'Intervalo (dias)', size=(90, -1))
        self.txtInterval = wx.TextCtrl(panel, -1, '', size=(50, -1))

        lblDest = wx.StaticText(panel, -1, 'Pasta de destino', size=(90, -1))
        self.txtDest = wx.TextCtrl(panel, -1, '')
        self.btnDest = wx.Button(panel, -1, 'Selecionar', (50, 50))

        self.btnAddSource = wx.Button(panel, -1, 'Adicionar', (50, 50))
        self.btnRemoveSource = wx.Button(panel, -1, 'Remover', (50, 50))
        self.listSources = wx.ListCtrl(panel, -1,
                                       style=wx.LC_REPORT
                                       | wx.LC_EDIT_LABELS
                                       )

        self.listSources.InsertColumn(0, "Caminho")
        self.listSources.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)

        self.btnOk = wx.Button(panel, -1, 'OK', (50, -1))
        self.btnCancel = wx.Button(panel, -1, 'Cancelar', (50, -1))

        intervalSizer = wx.BoxSizer(wx.HORIZONTAL)
        intervalSizer.Add(lblInterval)
        intervalSizer.Add(self.txtInterval, wx.SizerFlags(1).Border(wx.LEFT, 5))

        destSizer = wx.BoxSizer(wx.HORIZONTAL)
        destSizer.Add(lblDest)
        destSizer.Add(self.txtDest, wx.SizerFlags(1).Border(wx.LEFT, 5))
        destSizer.Add(self.btnDest, wx.SizerFlags(0).Border(wx.LEFT, 5))

        sourceSizer = wx.BoxSizer(wx.HORIZONTAL)
        sourceSizer.Add(self.btnAddSource)
        sourceSizer.Add(self.btnRemoveSource, wx.SizerFlags(0).Border(wx.LEFT, 5))

        footerSizer = wx.BoxSizer(wx.HORIZONTAL)
        footerSizer.Add(self.btnOk)
        footerSizer.Add(self.btnCancel, wx.SizerFlags(0).Border(wx.LEFT, 5))

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(intervalSizer)
        mainSizer.Add(destSizer, wx.SizerFlags(0).Expand().Border(wx.TOP, 10))
        mainSizer.Add(sourceSizer, wx.SizerFlags(0).Border(wx.TOP, 10))
        mainSizer.Add(self.listSources, wx.SizerFlags(0).Expand().Border(wx.TOP, 10))
        mainSizer.Add(footerSizer, wx.SizerFlags(0).Right().Border(wx.TOP, 10))

        panelSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer.Add(mainSizer, wx.SizerFlags(0).Expand().Border(wx.ALL, 10))

        panel.SetSizer(panelSizer)

    def createDestDialog(self):
        dlg = wx.DirDialog(self, "Selecione uma pasta:",
                           style=wx.DD_DEFAULT_STYLE
                           # | wx.DD_DIR_MUST_EXIST
                           # | wx.DD_CHANGE_DIR
                           )
        return dlg

    def createSourceDialog(self):
        dlg = wx.FileDialog(
            self, message="Selecione um arquivo",
            style=wx.FD_OPEN | wx.FD_MULTIPLE |
            wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST |
            wx.FD_PREVIEW
        )
        return dlg

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

    def selectDest(self):
        dialog = self._view.createDestDialog()
        if dialog.ShowModal() == wx.ID_OK:
            self._view.txtDest.SetValue(dialog.GetPath())

    def selectSource(self):
        dialog = self._view.createSourceDialog()
        if dialog.ShowModal() == wx.ID_OK:
            self.insertSource(dialog.GetPath())

    def insertSource(self, path):
        self._view.listSources.InsertItem(self._view.listSources.GetItemCount(), path)

    def removeSource(self):
        idx = self._view.listSources.GetFirstSelected()
        print(idx)


class SettingsInteractor:
    def Install(self, presenter, view):
        self._presenter = presenter
        self._view = view

        self._view.btnDest.Bind(wx.EVT_BUTTON, self.OnSelectDest)
        self._view.btnAddSource.Bind(wx.EVT_BUTTON, self.OnSelectSource)
        self._view.btnRemoveSource.Bind(wx.EVT_BUTTON, self.OnRemoveSource)

    def OnSelectDest(self, evt):
        self._presenter.selectDest()

    def OnSelectSource(self, evt):
        self._presenter.selectSource()

    def OnRemoveSource(self, evt):
        self._presenter.removeSource()
