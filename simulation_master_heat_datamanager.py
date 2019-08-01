import HEAT as heat
import elinkmanager
# from datamanager import DataManager
from counterdown import CounterDown
import threading
from logger import InfoLogger, DataLogger, AdcsLogger
import sys

class Master:

    __instance = None

    def __init__(self, ground_ip):

        self.status_vector = dict()
        self.command_vector = dict()
        self.ground_ip = ground_ip
        self.info_logger = InfoLogger()
        self.data_logger = DataLogger()
        self.elink = elinkmanager.ELinkManager(self,self.ground_ip)
        self.thread_elink = None
        # self.data_manager = DataManager(self, self.info_logger, self.data_logger)
        # self.thread_data_manager = None
        self.heat = heat.HEAT(self)
        self.thread_heat = None
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
        # Heat
        self.status_vector['HEAT_ON'] = 0   # 0
        self.status_vector['HEAT_SLEEP'] = 0
        # DMC
        self.status_vector['RET_SUCS'] = 0  # 0
        # Experiment
        self.status_vector['KILL'] = 0

    def init_command_vector(self):
        # HEAT
        self.command_vector['HEAT_SLEEP'] = 0
        self.command_vector['HEAT_AWAKE'] = 0
        # DMC
        self.command_vector['RET_RETRY'] = 0

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
        self.thread_heat = threading.Thread(target=self.heat.start).start()

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
              [+] e.g python simulation_master_heat_datamanager.py 195.168.0.1

              [+] For Testing purposes use 'local' as argument
              [+] to simulate a connection locally
              [+] e.g python simulation_master_heat_datamanager.py local
              """)
    else:
        print("""
            This is a program to test only heating control.
            Use commands:
            [+] HEAT_SLEEP #to force close the heating control
            [+] HEAT_AWAKE #to recall auto mode of heating control
            [+] KILL #to kill program 
            Choose where to collect data (random or from data_manager) via the HEAT class 
                - threaded_function_data()
            """)
        ground_ip = sys.argv[1]
        Master(ground_ip).start()
