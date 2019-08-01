import ADC as adc
import elinkmanager
# from datamanager import DataManager
from counterdown import CounterDown
import threading
from logger import InfoLogger, DataLogger, AdcsLogger
from time import sleep
import sys


class Master:

    __instance = None

    def __init__(self, ground_ip):

        self.status_vector = dict()
        self.command_vector = dict()
        self.ground_ip = ground_ip
        self.info_logger = InfoLogger()
        self.data_logger = DataLogger()
        self.adcs_logger = AdcsLogger()
        self.elink = elinkmanager.ELinkManager(self,self.ground_ip)
        self.thread_elink = None
        # self.data_manager = DataManager(self, self.info_logger, self.data_logger)
        # self.thread_data_manager = None
        self.adc = adc.ADC(self)
        self.thread_adc = None
        self.counterdown = CounterDown(self)
        Master.__instance = self

    @staticmethod
    def get_instance():

        if Master.__instance is None:
            Master()
        return Master.__instance

    def init_status_vector(self):
        # Data
        self.status_vector['GPS'] = 1       # 1
        self.status_vector['COMPASS'] = 1   # 1
        self.status_vector['IMU'] = 1       # 1
        self.status_vector['ALTIMETER'] = 1 # 1
        self.status_vector['TEMP'] = 1      # 1
        # ADC
        self.status_vector['ADC_MAN'] = 0   # 0
        # DMC

        self.status_vector['DEP_SUCS'] = 1  # 0

        # Experiment
        self.status_vector['KILL'] = 0

    def init_command_vector(self):
        # ADC
        self.command_vector['ADC_MAN'] = 0
        self.command_vector['ADC_AUTO'] = 0
        self.command_vector['SET'] = 0
        self.command_vector['SCAN'] = 0

    def start(self):

        self.init_experiment()
        while not self.get_command('KILL'):
            pass
        self.status_vector['KILL'] = 1
        print('end')

    def init_experiment(self):
        self.init_status_vector()
        self.init_command_vector()
        self.init_elink()
        # self.init_data_manager()
        self.init_subsystems()

    def init_elink(self):
        self.thread_elink = threading.Thread(target=self.elink.start).start()

    def init_data_manager(self):
        pass
        # self.thread_data_manager = threading.Thread(target=self.data_manager.start).start()

    def init_subsystems(self):
        self.thread_adc = threading.Thread(target=self.adc.start).start()

    def get_command(self, command):
        try:
            return self.command_vector[command]
        except:
            return 0


if __name__ == "__main__":

    __again = True

    if len(sys.argv) != 2:
        print("""
              [+] Run master program with one argument.
              [+] The argument indicates the ground IP
              [+] e.g python simulation_master_adc_datamanager.py 195.168.0.1

              [+] For Testing purposes use 'local' as argument
              [+] to simulate a connection locally
              [+] e.g python simulation_master_adc_datamanager.py local
              """)
    else:
        print("""
        This is a program to test only ADC control.
            Use commands:
            [+] ADC_MAN #to change in manual ADC control
            [+] SET # set antenna's base in a specific step - operation of manual ADC only
            [+] SCAN # antenna's base turn 360 n back - operation of manual ADC only
            [+] ADC_AUTO #to recall auto mode of ADC control
            [+] KILL #to kill program 
            Choose where to collect data (random or from data_manager) via the ADC class 
                - get_compass_data()
                - get_gps_data()
        """)
        ground_ip = sys.argv[1]
        Master(ground_ip).start()
