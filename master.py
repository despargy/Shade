import elinkmanager
import threading, time
from logger import InfoLogger , AdcsLogger, DataLogger


class Master:

    def __init__(self):
        threading.Thread(target=self.create_dummy_data).start()


    def create_dummy_data(self):
        while True:
            time.sleep(3)
            DataLogger.get_instance().write_info('Data1 , Data2 , Data3 , Data 4')
            InfoLogger.get_instance().write_info('Data1 , Data2 , Data3 , Data 4')

    def start(self):

        #Init ELinkManager
        self.init_elink()


    def init_elink(self):
        elink = elinkmanager.ELinkManager()
        threading.Thread(target=elink.start).start()

    @staticmethod
    def get_datalogger_unsend_data():
        return DataLogger.get_instance().get_unsend_data()

    @staticmethod
    def get_infologger_unsend_data():
        return InfoLogger.get_instance().get_unsend_data()


if __name__ == "__main__":
    Master().start()
