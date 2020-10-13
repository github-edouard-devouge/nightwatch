from .img import parse, enrichTags
from .kube import getAllClusterImages
from .cron import CronMethod
from .tags import getEligibleTags
from .metrics import updateImageMetrics

from datetime import datetime
import logging


class NightWatch():
    def __init__(self):
        self.images = []
        self.imagesToUpdate = []
        self.watchFrequency = 3600
        self.watch_ts = None
        self.status = "Stopped"
        self.watching = False
        self.__job = CronMethod(self.watchFrequency, self.watch)

    def watch(self):
        logging.info("Starting a new watch...")
        self.watching = True
        self.images = parse(getAllClusterImages())
        self.images = enrichTags(self.images)
        self.imagesToUpdate = []
        for image in self.images:
            if image.targetTag and getEligibleTags(image.registry, image.repository, [image.currentTag.dict()]):
                self.imagesToUpdate.append(image)
        self.watch_ts = datetime.now()
        self.watching = False
        updateImageMetrics(self.imagesToUpdate)
        logging.info("Watch complete.")

    def start(self):
        self.watch()
        self.__job.start()
        logging.info("NightWatch daemon started.")
        self.status = "Started"

    def stop(self):
        self.__job.stop()
        self.status = "Stopped"
