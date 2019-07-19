import elinkmanager , datamanager
import threading, time , sys
from logger import InfoLogger , AdcsLogger, DataLogger


class Master:

    def __init__(self,ground_ip):
        self.ground_ip = ground_ip


    def start(self):

        #Init ELinkManager
        #self.init_elink()
        
        #init_datamanager
        self.init_datamanager()
        
    def init_datamanager(self):
        data_manager = datamanager.DataManager(self,InfoLogger.get_instance(),DataLogger.get_instance())
        threading.Thread(target=data_manager.start).start()    


    def init_elink(self):
        elink = elinkmanager.ELinkManager(self.ground_ip)
        threading.Thread(target=elink.start).start()

    @staticmethod
    def get_datalogger_unsend_data():
        return DataLogger.get_instance().get_unsend_data()

    @staticmethod
    def get_infologger_unsend_data():
        return InfoLogger.get_instance().get_unsend_data()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("""
              [+] Run master program with one argument.
              [+] The argument indicates the ground IP
              [+] e.g python master.py 195.168.0.1

              [+] For Testing purposes use 'local' as argument
              [+] to simulate a connection locally
              [+] e.g python master.py local
              """)
    else:
        ground_ip = sys.argv[1]
        Master(ground_ip).start()
