from pathlib import Path

import wx
from appdirs import AppDirs

from ui import main
from replic8.core.app import App

APPNAME = "Replic8"
AUTHOR = 'gmtfonseca'

appDataPath = Path(AppDirs('Replic8', 'gmtfonseca').user_data_dir)


config = {
    'storage': {
        'schedule_data_path': appDataPath / 'schedule.config',
        'copy_data_path': appDataPath / 'copy.config',
        'log_path': appDataPath / 'log.txt'
    },
    'scheduler': {
        'delay': 5
    },
    'env': 'dev'
}


def run():
    wxApp = wx.App()

    app = App(config)
    main.start(app)

    wxApp.MainLoop()
