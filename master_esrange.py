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
#import RPi.GPIO as GPIO


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
        self.pin_powerB = 12 # @TODO change it in boot/config.txt
        # GPIO.setmode(GPIO.BOARD)
        # GPIO.setup(self.pin_powerB, GPIO.OUT)
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
        self.status_vector['DEP_SUCS'] = 0  # 0
        self.status_vector['DEP_READY'] = 0 # 0
        self.status_vector['RET_READY'] = 0 # 0
        self.status_vector['RET_CONF'] = 0  # 0
        self.status_vector['RET_AB'] = 0    # 0
        self.status_vector['RET_SUCS'] = 0  # 0
        # Experiment
        self.status_vector['KILL'] = 0

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
        self.command_vector['DEP_SUCS'] = 0
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
        #REBOOT
        self.command_vector['REBOOT_SLAVE'] = 0

    def start(self):

        self.init_experiment()

        while not self.status_vector['RET_CONF'] and not self.get_command('KILL'):
            sleep(self.counterdown.master_time_runs)
            if self.get_command('REBOOT_SLAVE'):
                self.command_vector['REBOOT_SLAVE'] = 0
                self.reboot_slave()
            if self.get_command('REBOOT'):
                pass

        # kill threads
        self.status_vector['KILL'] = 1
        self.info_logger.write_info('KILLED ADC + TX')
        print('killed adc + tx')

        # @ TODO wait DMC and then kill DMC n' HEAT n' ?Elink n' ?Data
        if self.thread_dmc is not None:
            self.thread_dmc.join()

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
        self.thread_adc = threading.Thread(target=self.adc.start).start()
        self.thread_dmc = threading.Thread(target=self.dmc.start).start()
        self.thread_heat = threading.Thread(target=self.heat.start).start()
        #self.thread_tx = threading.Thread(target=self.tx.start).start()

    def get_command(self, command):
        try:
            return self.command_vector[command]
        except:
            return 0

    def reboot_slave(self):
        pass
        #power off and power on the other ras
        # GPIO.output(self.pin_powerB, GPIO.LOW)
        # GPIO.output(self.pin_powerB, GPIO.HIGH)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("""
              [+] Run master program with one argument.
              [+] The argument indicates the ground IP
              [+] e.g python master_esrange.py 195.168.0.1

              [+] For Testing purposes use 'local' as argument
              [+] to simulate a connection locally
              [+] e.g python master_esrange.py local
              """)
    else:
        ground_ip = sys.argv[1]
        Master(ground_ip).start()

