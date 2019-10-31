import sys
from pathlib import Path

import wx

from ui import assets


def create(parent, scheduleModel, copyModel, schedulerManager, logger):
    return SettingsPresenter(SettingsFrame(parent, 'Configurações'),
                             SettingsInteractor(),
                             scheduleModel,
                             copyModel,
                             schedulerManager,
                             logger)


class SettingsFrame(wx.Frame):

    def __init__(self, parent, title):
        height = 390 if sys.platform == 'win32' else 325
        super().__init__(parent=parent, title=title,
                         style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.FRAME_NO_TASKBAR,
                         size=(500, height))
        self._initLayout()

    def _initLayout(self):
        panel = wx.Panel(self)

        widthLabel = 95 if sys.platform == 'win32' else 100

        lblInterval = wx.StaticText(panel, -1, 'Intervalo (dias)', size=(widthLabel, -1))
        self.txtInterval = wx.TextCtrl(panel, -1, '', size=(50, -1))

        lblDest = wx.StaticText(panel, -1, 'Pasta de destino', size=(widthLabel, -1))
        self.txtDest = wx.TextCtrl(panel, -1, '')
        self.txtDest.Disable()

        bmpFolder = wx.Bitmap(assets.image('folder.png'), wx.BITMAP_TYPE_PNG)
        self.btnSelectDest = wx.BitmapButton(panel, -1, bmpFolder, (50, 50))

        sourceBox = wx.StaticBox(panel, -1, 'Arquivos a serem copiados')

        bmpAdd = wx.Bitmap(assets.image('add.png'), wx.BITMAP_TYPE_PNG)
        self.btnAddSource = wx.BitmapButton(sourceBox, -1, bmpAdd, (50, 50))

        bmpRemove = wx.Bitmap(assets.image('remove.png'), wx.BITMAP_TYPE_PNG)
        self.btnRemoveSource = wx.BitmapButton(sourceBox, -1, bmpRemove, (50, 50))
        self.listSources = wx.ListCtrl(sourceBox, -1,
                                       style=wx.LC_REPORT
                                       )

        self.listSources.InsertColumn(0, 'Arquivo')
        self.listSources.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)

        self.btnOk = wx.Button(panel, -1, 'OK', (50, -1))
        self.btnCancel = wx.Button(panel, -1, 'Cancelar', (50, -1))

        intervalSizer = wx.BoxSizer(wx.HORIZONTAL)
        intervalSizer.Add(lblInterval)
        intervalSizer.Add(self.txtInterval, wx.SizerFlags(1).Border(wx.LEFT, 5))

        destSizer = wx.BoxSizer(wx.HORIZONTAL)
        destSizer.Add(lblDest)
        destSizer.Add(self.txtDest, wx.SizerFlags(1).Border(wx.LEFT, 5))
        destSizer.Add(self.btnSelectDest, wx.SizerFlags(0).Border(wx.LEFT, 5))

        sourceSizer = wx.BoxSizer(wx.HORIZONTAL)
        sourceSizer.Add(self.btnAddSource)
        sourceSizer.Add(self.btnRemoveSource, wx.SizerFlags(0).Border(wx.LEFT, 5))

        sourceBoxSizer = wx.BoxSizer(wx.VERTICAL)
        borderTop = 15 if sys.platform == 'win32' else 0
        sourceBoxSizer.Add(sourceSizer, wx.SizerFlags(0).Expand().Border(wx.TOP, borderTop))
        sourceBoxSizer.Add(self.listSources, wx.SizerFlags(0).Expand().Border(wx.TOP, 5))

        sourceBoxSizerOuter = wx.BoxSizer(wx.VERTICAL)
        sourceBoxSizerOuter.Add(sourceBoxSizer, wx.SizerFlags(0).Expand().Border(wx.ALL, 10))
        sourceBox.SetSizer(sourceBoxSizerOuter)

        footerSizer = wx.BoxSizer(wx.HORIZONTAL)
        footerSizer.Add(self.btnOk)
        footerSizer.Add(self.btnCancel, wx.SizerFlags(0).Border(wx.LEFT, 5))

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(intervalSizer)
        mainSizer.Add(destSizer, wx.SizerFlags(0).Expand().Border(wx.TOP, 10))
        mainSizer.Add(sourceBox, wx.SizerFlags(0).Expand().Border(wx.TOP, 10))
        mainSizer.Add(footerSizer, wx.SizerFlags(0).Right().Border(wx.TOP, 10))

        panelSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer.Add(mainSizer, wx.SizerFlags(0).Expand().Border(wx.ALL, 10))

        panel.SetSizer(panelSizer)

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
        self.Raise()
        self.Show()


class SettingsPresenter:
    def __init__(self, view, interactor, scheduleModel, copyModel, schedulerManager, logger):
        self._view = view
        self._view.CenterOnScreen()
        interactor.Install(self, self._view)
        self._scheduleModel = scheduleModel
        self._copyModel = copyModel
        self._schedulerManager = schedulerManager
        self._logger = logger
        self._loadViewFromModel()

    def _loadViewFromModel(self):
        if self._scheduleModel.copyInterval:
            self._view.txtInterval.SetValue(str(self._scheduleModel.copyInterval))

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
            self.insertSource(Path(dialog.GetPath()).as_posix())

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

    def show(self):
        self._view.start()

    def isActive(self):
        return bool(self._view)


class SettingsInteractor:
    def Install(self, presenter, view):
        self._presenter = presenter
        self._view = view

        self._view.btnSelectDest.Bind(wx.EVT_BUTTON, self.OnSelectDest)
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
