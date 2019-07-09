import logging
from abc import ABC, abstractmethod

class Logger(ABC):

    @abstractmethod
    def get_instance(self): pass

    def write_info(self,message):
        self.logger.info(message)

    def write_error(self,message):
        self.logger.error(message)

    def write_warning(self,message):
        self.logger.warning(message)

    def write_debug(self,message):
        self.logger.debug(message)

    def write_critical(self,message):
        self.logger.critical(message)

    def write_exception(self,message):
        self.logger.exception(message)


class AdcsLogger(Logger):

    __instance = None

    def get_instance():
        if AdcsLogger.__instance == None:
            AdcsLogger()
        return AdcsLogger.__instance


    def __init__(self):
      if AdcsLogger.__instance != None:
         raise Exception("This class is a singleton!")
      else:
         self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
         self.handler = logging.FileHandler('adcs.log')
         self.handler.setFormatter(self.formatter)

         self.logger = logging.getLogger('adcs_logger')
         self.logger.setLevel(logging.INFO)
         self.logger.addHandler(self.handler)
         AdcsLogger.__instance = self


class InfoLogger(Logger):

    __instance = None

    def get_instance():
        if InfoLogger.__instance == None:
            InfoLogger()
        return InfoLogger.__instance


    def __init__(self):
      if InfoLogger.__instance != None:
         raise Exception("This class is a singleton!")
      else:
         self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
         self.handler = logging.FileHandler('info.log')
         self.handler.setFormatter(self.formatter)

         self.logger = logging.getLogger('info_logger')
         self.logger.setLevel(logging.INFO)
         self.logger.addHandler(self.handler)
         InfoLogger.__instance = self
