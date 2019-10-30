""" from replic8.core.schedule import Scheduler
from replic8.core.copy import Copier
from replic8.core.model import ScheduleModel, CopyModel
from replic8.core.logger import LoggerFactory
from datetime import date, timedelta

scheduleModel = ScheduleModel('./fixture/schedule.config')
scheduleModel.clear()
scheduleModel.setCopyInterval(7)

lastCopy = date.today() - timedelta(days=8)
scheduleModel.setLastCopy(lastCopy)

copyModel = CopyModel('./fixture/copy.config')
copyModel.clear()
copyModel.addSource('./fixture/src/dumb.js')
copyModel.addSource('./fixture/src/dumb2.js')
copyModel.setDestination('./fixture/dest/')

copier = Copier(copyModel)

schedule = Scheduler(copier, 30, scheduleModel,
                     LoggerFactory.getDevLogger())
schedule.start()

while True:
    pass
 """
