import logging
from abc import ABC, abstractmethod
from file_read_backwards import FileReadBackwards
import threading
import os


class Logger(ABC):


    def __init__(self,filename):
        self.lock = threading.Lock()
        self.dir = "Logs"
        if(not os.path.isdir(self.dir)):
            os.mkdir(self.dir)

        self.file_name = "{dir}/{filename}".format(dir=self.dir,filename=filename)
        last_index = self.get_last_index()
        self.last_sended_index = str(last_index) 
        self.log_id = 0 if last_index == 1 else last_index
            
    

    def set_up_logger(self,formatter,name):
        """Set formmater and name of logge
        
        Arguments:
            formatter {string} -- The message formatter
            name {string} -- The name of logger
        """
        self.formatter = logging.Formatter(formatter)
        self.handler = logging.FileHandler(self.file_name)
        self.handler.setFormatter(self.formatter)
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(self.handler)

    @abstractmethod
    def get_instance(self): 
        """Return the singleton instance
           of logger. Every logger must
           override.
        """
        pass

    def set_last_sended_index(self,index):
        """Set value of variable last_sended_index
        
        Arguments:
            index {int} -- The last index that ground station received
        """
        self.last_sended_index = index

    def get_last_index(self):
        """Get index from last row
        
        Returns:
            [int] -- The index from last row or
                      1 if there is no file.
        """
        if(self.isSafeToRead()):
            with FileReadBackwards(self.file_name, encoding="utf-8") as log_file:
                for line in log_file:
                    try:
                        return int(line.split(',')[0])
                    except:
                        break
        return 1


    def isSafeToRead(self):
        """Checks if is safe to read the log file
        
        Returns:
            [boolean] -- True: dir and filename exists
                         False: the dir or the filename doesn't exists
        """
        return os.path.isdir(self.dir) and os.path.exists(self.file_name)

    def get_unsend_data(self):
        """Get the logs that haven't been send to ground station
        
        Returns:
            [list: unsend_logs] -- The unsend logs
            [int: total_logs] -- The total count of unsend logs
        """
        unsend_logs = []
        total_logs = 0
        with FileReadBackwards(self.file_name, encoding="utf-8") as log_file:
            for line in log_file:
                line_id = line.split(',')[0]
                if line_id == self.last_sended_index:
                    if line_id == 1 :
                        total_logs += 1
                        unsend_logs.insert(0, line)
                    break

                total_logs += 1
                unsend_logs.insert(0, line)

        return unsend_logs, total_logs

    def inc_log_id(self):
        """Safely increases log id
        """
        self.lock.acquire()
        self.log_id += 1
        self.lock.release()

    def write_info(self,message):
        """Logs info message
        
        Arguments:
            message {string} -- the log message
        """
        self.inc_log_id()
        self.logger.info(message,
                            extra={'log_id':self.log_id})

    def write_error(self,message):
        """Logs error message
        
        Arguments:
            message {string} -- the log message
        """
        self.inc_log_id()
        self.logger.error(message,
                            extra={'log_id':self.log_id})

    def write_warning(self,message):
        """Logs warning message
        
        Arguments:
            message {string} -- the log message
        """
        self.inc_log_id()
        self.logger.warning(message,
                            extra={'log_id':self.log_id})

    def write_debug(self,message):
        """Logs debug message
        
        Arguments:
            message {string} -- the log message
        """
        self.inc_log_id()
        self.logger.debug(message,
                            extra={'log_id':self.log_id})

    def write_critical(self,message):
        """Logs critical message
        
        Arguments:
            message {string} -- the log message
        """
        self.inc_log_id()
        self.logger.critical(message,
                            extra={'log_id':self.log_id})

    def write_exception(self,message):
        """Logs exception message
        
        Arguments:
            message {string} -- the log message
        """
        self.inc_log_id()
        self.logger.exception(message,
                            extra={'log_id':self.log_id})



"""
 Class for Logging ADCS action so you can
 recover your system.
"""
class AdcsLogger(Logger):

    __instance = None

    def __init__(self, filename = 'adcs.log'):
      if AdcsLogger.__instance != None:
         raise Exception("This class is a singleton!")
      else:
         super(AdcsLogger, self).__init__(filename)
         formatter = '%(log_id)s,%(asctime)s %(levelname)s %(message)s'
         self.set_up_logger(formatter,'adcs_logger')
         AdcsLogger.__instance = self



    def get_instance(self):
        if AdcsLogger.__instance == None:
            AdcsLogger()
        return AdcsLogger.__instance




class InfoLogger(Logger):

    __instance = None

    def __init__(self, filename = 'info.log'):
        if InfoLogger.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            super(InfoLogger, self).__init__(filename)
            formatter = '%(log_id)s,%(asctime)s %(levelname)s %(message)s'
            self.set_up_logger(formatter,'info_logger')
            InfoLogger.__instance = self


    def get_instance(self):
        if InfoLogger.__instance == None:
            InfoLogger()
        return InfoLogger.__instance


class DataLogger(Logger):

    __instance = None

    def __init__(self, filename = 'data.log'):
        if DataLogger.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            super(DataLogger, self).__init__(filename)
            formatter = '%(log_id)s,%(message)s'
            self.set_up_logger(formatter,'data_logger')
            DataLogger.__instance = self


    def get_instance():
        if DataLogger.__instance == None:
            DataLogger()
        return DataLogger.__instance


class GroundLogger(Logger):


    def __init__(self, filename = 'elink.info.log'):
        super(GroundLogger, self).__init__(filename)
        formatter = '%(message)s'
        self.set_up_logger(formatter,'logger_{filename}'.format(filename=filename))

    def get_instance():
        pass

