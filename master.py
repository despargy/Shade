import elinkmanager
import threading, time , sys
from logger import InfoLogger , AdcsLogger, DataLogger
import random


class Master:

    def __init__(self,ground_ip):
        self.ground_ip = ground_ip
        self.info_logger = InfoLogger.get_instance()
        self.data_logger = DataLogger.get_instance()
        self.adcs_logger = AdcsLogger.get_instance()
        self.vector_command = {}
        threading.Thread(target=self.create_dummy_data).start()



    def get_command(self,command):
        try:
            return vector_command[command]
        except:
            return 0


    def create_dummy_data(self):
        count = 0
        while True:
            time.sleep(0.5)

            ran1 = random.randint(-10,21)
            ran2 = random.randint(-10,21)
            self.data_logger.write_info('{},{}'.format(count,ran2))
            count += 1

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
        #Master(ground_ip).start()
        Master(ground_ip)