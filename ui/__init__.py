import os
from pathlib import Path

import wx

from ui import main
from replic8.core.app import App


APPDATA_PATH = Path(os.getenv('LOCALAPPDATA')) / 'Replic8'

config = {
}


def run():
    wxApp = wx.App()

    app = App(config)
    main.start(app)

    wxApp.MainLoop()
