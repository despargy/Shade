import DMC as dmc
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
        self.dmc = dmc.DMC(self)
        self.thread_dmc = None
        self.counterdown = CounterDown(self)
        Master.__instance = self

    @staticmethod
    def get_instance():

        if Master.__instance is None:
            Master()
        return Master.__instance


    def init_status_vector(self):
        # Data
        self.status_vector['GPS'] = 1  # 1
        self.status_vector['COMPASS'] = 1  # 1
        self.status_vector['IMU'] = 1  # 1
        self.status_vector['ALTIMETER'] = 1  # 1
        self.status_vector['TEMP'] = 1  # 1
        # DMC
        self.status_vector['DMC_SLEEP'] = 0  # 0
        self.status_vector['DEP_CONF'] = 0  # 0
        self.status_vector['DEP_SUCS'] = 0  # 0
        self.status_vector['DEP_READY'] = 0  # 0
        self.status_vector['RET_READY'] = 0  # 0
        self.status_vector['RET_CONF'] = 0  # 0
        self.status_vector['RET_AB'] = 0  # 0
        self.status_vector['RET_SUCS'] = 0  # 0
        # Experiment
        self.status_vector['KILL'] = 0

    def init_command_vector(self):
        # DMC
        self.command_vector['DMC_AWAKE'] = 0
        self.command_vector['DEP'] = 0
        self.command_vector['DEP_CONF'] = 0
        self.command_vector['DEP_AB'] = 0
        self.command_vector['DEP_SUCS'] = 0
        self.command_vector['DEP_RETRY'] = 0
        self.command_vector['RET_CONF'] = 0
        self.command_vector['RET_AB'] = 0
        self.command_vector['RET'] = 0
        self.command_vector['RET_SUCS'] = 0
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
        self.thread_dmc = threading.Thread(target=self.dmc.start).start()

    def get_command(self, command):
        try:
            return self.command_vector[command]
        except:
            return 0


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("""
              [+] Run master program with one argument.
              [+] The argument indicates the ground IP
              [+] e.g python simulation_master_dmc_datamanager.py 195.168.0.1

              [+] For Testing purposes use 'local' as argument
              [+] to simulate a connection locally
              [+] e.g python simulation_master_dmc_datamanager.py local
              """)
    else:
        print("""
            This is a program to test only DMC control.
            Use commands:
            [+] DEP # to ask for deploy
            [+] DEP_CONF # to confirm for deploy - after DEP
            [+] DEP_AB # to abort deployment - after DEP
            [+] DEP_SUCS # to declare the successful deployment
            [+] DEP_RETRY #to retry the deployment
            [+] DMC_AWAKE # to wake up DMC
            [+] RET # to ask for retrieve
            [+] RET_CONF # to confirm for retrieve - after RET
            [+] RET_AB # to abort retrieve - after RET            
            [+] RET_SUCS # to declare the successful retrieve
            [+] RET_RETRY #to retry the retrieve
            [+] KILL #to kill program 
            Choose where to collect data (random or from data_manager) via the DMC class 
                - phase_check()
            """)
        ground_ip = sys.argv[1]
        Master(ground_ip).start()
