import elinkmanager
import threading, time , sys
from logger import InfoLogger , AdcsLogger, DataLogger


class Master:

    def __init__(self,ground_ip):
        self.ground_ip = ground_ip
        self.info_logger = InfoLogger.get_instance()
        self.data_logger = DataLogger.get_instance()
        self.adcs_logger = AdcsLogger.get_instance()
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
        elink = elinkmanager.ELinkManager(self,self.ground_ip)
        threading.Thread(target=elink.start).start()


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
