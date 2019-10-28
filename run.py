from replic8.core.schedule import Scheduler
from replic8.core.copy import Copier
from replic8.core.model import ScheduleModel
from replic8.core.logger import LoggerFactory
from pathlib import Path
from datetime import date, timedelta

modelPath = Path('F:/Projetos/trash/src/model.json')
scheduleModel = ScheduleModel(modelPath)


scheduleModel.setCopyInterval(7)

lastCopy = date.today() - timedelta(days=8)
scheduleModel.setLastCopy(lastCopy)


src = Path('F:/Projetos/trash/src/bigiso.iso')
dest = Path('F:/Projetos/trash/dest/bigiso_backup.iso')
copier = Copier(src, dest)

schedule = Scheduler(copier, 30, scheduleModel,
                     LoggerFactory.getDevLogger())
schedule.start()

while True:
    pass
