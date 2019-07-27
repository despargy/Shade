import logging
from abc import ABC, abstractmethod
from file_read_backwards import FileReadBackwards


class Logger(ABC):


    def __init__(self):
        self.log_id = 0
        self.last_sended_index = 1

    @abstractmethod
    def get_instance(self): pass


    def get_unsend_data(self):
        unread_logs = []
        total_rows = 0
        with FileReadBackwards(self.file_name, encoding="utf-8") as BigFile:
            for line in BigFile:
                line_id = int(line.split(',')[0])
                if line_id == self.last_sended_index:
                    if line_id == 1 :
                        total_rows += 1
                        unread_logs.insert(0, line)
                    self.last_sended_index = self.log_id
                    break

                total_rows += 1
                unread_logs.insert(0, line)

        return unread_logs, total_rows

    def write_info(self,message):
        self.log_id += 1
        self.logger.info(message,
                            extra={'log_id':self.log_id})

    def write_error(self,message):
        self.log_id += 1
        self.logger.error(message,
                            extra={'log_id':self.log_id})

    def write_warning(self,message):
        self.log_id += 1
        self.logger.warning(message,
                            extra={'log_id':self.log_id})

    def write_debug(self,message):
        self.log_id += 1
        self.logger.debug(message,
                            extra={'log_id':self.log_id})

    def write_critical(self,message):
        self.log_id += 1
        self.logger.critical(message,
                            extra={'log_id':self.log_id})

    def write_exception(self,message):
        self.log_id += 1
        self.logger.exception(message,
                            extra={'log_id':self.log_id})



"""
 Class for Logging ADCS action so you can
 recover your system.
"""
class AdcsLogger(Logger):

    __instance = None

    def __init__(self):
      if AdcsLogger.__instance != None:
         raise Exception("This class is a singleton!")
      else:
         super(AdcsLogger, self).__init__()
         self.file_name = 'adcs.log'
         self.formatter = logging.Formatter('%(log_id)s,%(asctime)s %(levelname)s %(message)s')
         self.handler = logging.FileHandler(self.file_name)
         self.handler.setFormatter(self.formatter)

         self.logger = logging.getLogger('adcs_logger')
         self.logger.setLevel(logging.INFO)
         self.logger.addHandler(self.handler)
         AdcsLogger.__instance = self


    def get_instance(self):
        if AdcsLogger.__instance == None:
            AdcsLogger()
        return AdcsLogger.__instance




class InfoLogger(Logger):

    __instance = None

    def __init__(self):
        if InfoLogger.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            super(InfoLogger, self).__init__()
            self.file_name = 'info.log'
            self.formatter = logging.Formatter('%(log_id)s,%(asctime)s %(levelname)s %(message)s')
            self.handler = logging.FileHandler(self.file_name)
            self.handler.setFormatter(self.formatter)

            self.logger = logging.getLogger('info_logger')
            self.logger.setLevel(logging.INFO)
            self.logger.addHandler(self.handler)
            InfoLogger.__instance = self


    def get_instance(self):
        if InfoLogger.__instance == None:
            InfoLogger()
        return InfoLogger.__instance


class DataLogger(Logger):

    __instance = None

    def __init__(self):
        if DataLogger.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            super(DataLogger, self).__init__()
            self.file_name = 'data.log'
            self.formatter = logging.Formatter('%(log_id)s,%(message)s')
            self.handler = logging.FileHandler(self.file_name)
            self.handler.setFormatter(self.formatter)

            self.logger = logging.getLogger('data_logger')
            self.logger.setLevel(logging.INFO)
            self.logger.addHandler(self.handler)
            DataLogger.__instance = self


    def get_instance():
        if DataLogger.__instance == None:
            DataLogger()
        return DataLogger.__instance
