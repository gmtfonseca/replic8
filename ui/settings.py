import wx
from pathlib import Path


def show(parent, scheduleModel, copyModel, schedulerManager, logger):
    return SettingsPresenter(SettingsDialog(parent, 'Configurações'),
                             SettingsInteractor(),
                             scheduleModel,
                             copyModel,
                             schedulerManager,
                             logger)


class SettingsDialog(wx.Dialog):

    def __init__(self, parent, title):
        super().__init__(parent=parent, title=title, size=(500, 360))
        self._initLayout()

    def _initLayout(self):
        panel = wx.Panel(self)

        lblInterval = wx.StaticText(panel, -1, 'Intervalo (dias)', size=(100, -1))
        self.txtInterval = wx.TextCtrl(panel, -1, '', size=(50, -1))

        lblDest = wx.StaticText(panel, -1, 'Pasta de destino', size=(100, -1))
        self.txtDest = wx.TextCtrl(panel, -1, '')
        self.btnDest = wx.Button(panel, -1, 'Selecionar', (50, 50))

        sourceBox = wx.StaticBox(panel, wx.ID_ANY, 'Arquivos a serem copiados')

        self.btnAddSource = wx.Button(sourceBox, -1, 'Adicionar', (50, 50))
        self.btnRemoveSource = wx.Button(sourceBox, -1, 'Remover', (50, 50))
        self.listSources = wx.ListCtrl(sourceBox, -1,
                                       style=wx.LC_REPORT
                                       | wx.LC_EDIT_LABELS
                                       )

        self.listSources.InsertColumn(0, 'Caminho')
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

        sourceBoxSizer = wx.BoxSizer(wx.VERTICAL)
        sourceBoxSizer.Add(sourceSizer)
        sourceBoxSizer.Add(self.listSources, wx.SizerFlags(0).Border(wx.TOP, 5))

        sourceBoxSizerOuter = wx.BoxSizer(wx.VERTICAL)
        sourceBoxSizerOuter.Add(sourceBoxSizer, wx.SizerFlags(0).Border(wx.ALL, 5))
        sourceBox.SetSizer(sourceBoxSizerOuter)

        footerSizer = wx.BoxSizer(wx.HORIZONTAL)
        footerSizer.Add(self.btnOk)
        footerSizer.Add(self.btnCancel, wx.SizerFlags(0).Border(wx.LEFT, 5))

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(intervalSizer)
        mainSizer.Add(destSizer, wx.SizerFlags(0).Expand().Border(wx.TOP, 10))
        mainSizer.Add(sourceBox, wx.SizerFlags(0).Border(wx.TOP, 10))
        mainSizer.Add(footerSizer, wx.SizerFlags(0).Right().Border(wx.TOP, 10))

        panelSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer.Add(mainSizer, wx.SizerFlags(0).Expand().Border(wx.ALL, 10))

        panel.SetSizer(panelSizer)
        panel.Fit()
        self.Fit()

    def createDestDialog(self):
        dlg = wx.DirDialog(self, "Selecione uma pasta",
                           style=wx.DD_DEFAULT_STYLE
                           | wx.DD_DIR_MUST_EXIST
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

    def showInvalidIntervalDialog(self):
        wx.MessageDialog(self, 'Selecione um intervalo válido', 'Intervalo inválido').ShowModal()

    def showInvalidDestDialog(self):
        wx.MessageDialog(self, 'Selecione uma pasta de destino válida', 'Pasta de destino inválida').ShowModal()

    def showInvalidSourceDialog(self):
        wx.MessageDialog(self, 'Selecione ao menos um arquivo para ser copiado', 'Arquivos inválidos').ShowModal()

    def showConfirmChangesErrorDialog(self):
        wx.MessageDialog(self, 'Não foi possível salvar os dados', 'Error inesperado').ShowModal()

    def destroy(self):
        self.Destroy()

    def start(self):
        self.CenterOnScreen()
        self.Raise()
        self.ShowModal()


class SettingsPresenter:
    def __init__(self, view, interactor, scheduleModel, copyModel, schedulerManager, logger):
        self._view = view
        interactor.Install(self, self._view)
        self._scheduleModel = scheduleModel
        self._copyModel = copyModel
        self._schedulerManager = schedulerManager
        self._logger = logger
        self._loadViewFromModel()
        self._view.start()

    def _loadViewFromModel(self):
        if self._scheduleModel.copyInterval:
            self._view.txtInterval.SetValue(self._scheduleModel.copyInterval)

        if self._copyModel.destination:
            self._view.txtDest.SetValue(self._copyModel.destination.as_posix())

        for source in self._copyModel.sources:
            self._view.listSources.InsertItem(self._view.listSources.GetItemCount(), source.as_posix())

    def selectDest(self):
        dialog = self._view.createDestDialog()
        if dialog.ShowModal() == wx.ID_OK:
            self._view.txtDest.SetValue(dialog.GetPath())

    def selectSource(self):
        dialog = self._view.createSourceDialog()
        if dialog.ShowModal() == wx.ID_OK:
            self.insertSource(dialog.GetPath())

    def insertSource(self, path):
        if path:
            self._view.listSources.InsertItem(self._view.listSources.GetItemCount(), path)

    def removeSource(self):
        selectedItem = self._view.listSources.GetFirstSelected()
        if selectedItem != -1:
            self._view.listSources.DeleteItem(selectedItem)

    def quit(self):
        self._view.destroy()

    def confirmChanges(self):
        if not self._view.txtInterval.GetValue():
            self._view.showInvalidIntervalDialog()
            self._logger.debug('Intervalo inválido')
            return

        if not self._view.txtDest.GetValue() or not Path(self._view.txtDest.GetValue()).exists():
            self._view.showInvalidDestDialog()
            self._logger.debug('Destino inválido')
            return

        if not self._view.listSources.ItemCount:
            self._view.showInvalidSourceDialog()
            self._logger.debug('Origem inválida')
            return

        self._updateModel()

    def _updateModel(self):
        try:
            self._scheduleModel.setCopyInterval(self._view.txtInterval.GetValue())
            self._copyModel.setDestination(self._view.txtDest.GetValue())
            sources = [self._view.listSources.GetItem(i, 0).GetText() for i in range(self._view.listSources.ItemCount)]
            self._copyModel.setSources(sources)
            self._schedulerManager.start()
            self.quit()
        except Exception as err:
            self._view.showConfirmChangesErrorDialog()
            self._logger.exception(err)


class SettingsInteractor:
    def Install(self, presenter, view):
        self._presenter = presenter
        self._view = view

        self._view.btnDest.Bind(wx.EVT_BUTTON, self.OnSelectDest)
        self._view.btnAddSource.Bind(wx.EVT_BUTTON, self.OnSelectSource)
        self._view.btnRemoveSource.Bind(wx.EVT_BUTTON, self.OnRemoveSource)
        self._view.btnCancel.Bind(wx.EVT_BUTTON, self.OnCancel)
        self._view.btnOk.Bind(wx.EVT_BUTTON, self.OnOk)

    def OnSelectDest(self, evt):
        self._presenter.selectDest()

    def OnSelectSource(self, evt):
        self._presenter.selectSource()

    def OnRemoveSource(self, evt):
        self._presenter.removeSource()

    def OnCancel(self, evt):
        self._presenter.quit()

    def OnOk(self, evt):
        self._presenter.confirmChanges()
