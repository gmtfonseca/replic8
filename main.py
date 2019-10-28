from datetime import datetime
from replic8.core.schedule import Scheduler
from replic8.core.copy import Copier
from replic8.core.model import ScheduleModel

scheduleModel = ScheduleModel(
    '/Users/gustavo.fonseca/Projetos/experimentos/copy_files/src/model.json')

scheduleModel.setCopyInterval(15)


copier = Copier(
    '/Users/gustavo.fonseca/Projetos/experimentos/copy_files/src/auction.js',
    '/Users/gustavo.fonseca/Projetos/experimentos/copy_files/dest/auction_backup.js')
schedule = Scheduler(copier, 30)
schedule.start()
