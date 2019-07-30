import ADC as adc
import HEAT as heat
import DMC as dmc
import TX as tx
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
        self.dmc = dmc.DMC(self)
        self.thread_dmc = None
        self.heat = heat.HEAT(self)
        self.thread_heat = None
        self.adc = adc.ADC(self)
        self.thread_adc = None
        self.tx = tx.TX(self)
        self.thread_tx = None
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
        # Transmition
        self.status_vector['AMP_ON'] = 0    # 0
        self.status_vector['TX_ON'] = 0     # 0
        # ADC
        self.status_vector['ADC_MAN'] = 0   # 0
        # DMC
        self.status_vector['DMC_SLEEP'] = 0 # 0
        self.status_vector['DEP_CONF'] = 0  # 0
        self.status_vector['DEP_SUCS'] = 1  # 0
        self.status_vector['DEP_READY'] = 0 # 0
        self.status_vector['RET_READY'] = 0 # 0
        self.status_vector['RET_CONF'] = 0  # 0
        self.status_vector['RET_AB'] = 0    # 0
        self.status_vector['RET_SUCS'] = 0  # 0
        # Experiment
        self.status_vector['KILL'] = 0
        self.status_vector['AGAIN'] = 0

    def init_command_vector(self):
        # ADC
        self.command_vector['ADC_MAN'] = 0
        self.command_vector['ADC_AUTO'] = 0
        self.command_vector['SET'] = 0
        self.command_vector['SCAN'] = 0
        # HEAT
        self.command_vector['HEAT_SLEEP'] = 0
        self.command_vector['HEAT_AWAKE'] = 0
        # DMC
        self.command_vector['DMC_AWAKE'] = 0
        self.command_vector['DEP'] = 0
        self.command_vector['DEP_CONF'] = 0
        self.command_vector['DEP_AB'] = 0
        self.command_vector['DEP_SUCS'] = 1
        self.command_vector['DEP_RETRY'] = 0
        self.command_vector['RET_CONF'] = 0
        self.command_vector['RET_AB'] = 0
        self.command_vector['RET'] = 0
        self.command_vector['RET_SUCS'] = 0
        self.command_vector['RET_RETRY'] = 0
        # TX
        self.command_vector['TX_SLEEP'] = 0
        self.command_vector['TX_AWAKE'] = 0
        self.command_vector['PRE'] = 0

        # Experiment
        self.command_vector['AGAIN'] = 0
        self.command_vector['EXIT'] = 0

        # ONLY FOR TESTING
        # self.command_vector['DEP'] = 1
        # self.command_vector['DEP_AB'] = 1
        # self.command_vector['DEP_CONF'] = 0
        # self.command_vector['DEP_RETRY'] = 0
        # self.command_vector['RET'] = 0
        # self.command_vector['RET_AB'] = 1
        #

    def create_dummy_data(self):
        while True:
            sleep(3)
            DataLogger.get_instance().write_info('Data1 , Data2 , Data3 , Data 4')

    def start(self):

        self.init_experiment()

        # threading.Thread(target=self.create_dummy_data).start()
        while not self.status_vector['RET_CONF']:
            sleep(self.counterdown.master_checks_dep_sucs)
            if self.status_vector['DEP_SUCS']:
                while not self.status_vector['KILL']:
                    self.handle_manual_adc()

        #self.status_vector['KILL'] = 1
        # wait for threads before kill them
        if self.thread_adc is not None:
            self.thread_adc.join()
        if self.thread_tx is not None:
            self.thread_tx.join()
        if self.thread_dmc is not None:
            self.thread_dmc.join()

        self.info_logger.write_info('KILLED ALL')
        print('killed all')
        #self.status_vector['KILL'] = 0

        choice = self.counterdown.countdown2(self.counterdown.timeout_cmd, 'EXIT', 'AGAIN')
        if choice == 2:
            self.status_vector['AGAIN'] = 1
        else:
            self.info_logger.write_warning('SHADE IS TERMINATED')
            print('shade is terminated')
            # @TODO RESTART SHADE n REBOOT

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
        #self.thread_adc = threading.Thread(target=self.adc.start).start()
        #self.thread_dmc = threading.Thread(target=self.dmc.start).start()
        #self.thread_heat = threading.Thread(target=self.heat.start).start()
        self.thread_tx = threading.Thread(target=self.tx.start).start()

    def handle_manual_adc(self):
        while self.get_command('ADC_MAN') and not self.status_vector['KILL']:
            self.info_logger.write_info('IN ADC MAN: SET OR SCAN')
            print('in adc man: set or scan')
            self.status_vector['ADC_MAN'] = 1
            self.command_vector['ADC_AUTO'] = 0   # re-init
            self.command_vector['SET'] = 0  # re-init
            self.command_vector['SCAN'] = 0  # re-init
            choice = self.counterdown.countdown2(self.counterdown.master_timeout_to_set_or_scan, 'SET', 'SCAN')
            if choice == 1:
                self.adc.adcs_logger.write_info('FROM MASTER IN SET')
                print('from master in set')
                #@TODO AUTO ADC WAIT
                steps = int(self.command_vector['SET']['steps'])
                self.adc.set_position(steps)
            elif choice == 2:
                self.adc.adcs_logger.write_info('FROM MASTER IN SCAN')
                print('from master in scan')
                self.adc.scan()
            self.command_vector['SET'] = 0  # re-init
            self.command_vector['SCAN'] = 0  # re-init
            self.command_vector['ADC_AUTO'] = 0  # re-init
            self.command_vector['ADC_MAN'] = 0  # re-init
            self.info_logger.write_info('WAITING FOR ADC MAN OR AUTO')
            print('waiting for adc man or auto')
            choice = self.counterdown.countdown2(self.counterdown.master_time_breaks_adc_man, 'ADC_AUTO', 'ADC_MAN')
            if choice == 2:
                self.adc.adcs_logger.write_info('FROM MASTER CONT ADC MAN')
                print('from master cont adc man')
            else:
                self.command_vector['ADC_MAN'] = 0 # re-init
                self.status_vector['ADC_MAN'] = 0 # re-init
                self.adc.adcs_logger.write_info('FROM MASTER BREAK ADC MAN')
                print('from master break adc man')
        sleep(self.counterdown.master_time_adc_man_runs)

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
              [+] e.g python master.py 195.168.0.1

              [+] For Testing purposes use 'local' as argument
              [+] to simulate a connection locally
              [+] e.g python master.py local
              """)
    else:
        ground_ip = sys.argv[1]
        while __again:
            Master(ground_ip).start()
            __again = Master.get_instance().status_vector['AGAIN']

