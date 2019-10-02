import ADC as adc
import HEAT as heat
import DMC as dmc
import TX as tx
import elinkmanager
from datamanager import DataManager
from counterdown import CounterDown
import threading
from logger import InfoLogger, DataLogger, AdcsLogger
from time import sleep
import sys
import RPi.GPIO as GPIO
import json
import  Paths as paths
import Pins as pins
#@TODO mv import of motors
from Motor import MotorADC

class Master:

    __instance = None

    def __init__(self, ground_ip):

        self.status_vector = dict()
        self.command_vector = dict()
        self.ground_ip = ground_ip
        self.info_logger = InfoLogger()
        self.data_logger = DataLogger()
        self.adcs_logger = AdcsLogger()
        #@TODO where antenna to start
        self.adcs_logger.write_info(' {}, {} '.format(0, 0))
        self.elink = elinkmanager.ELinkManager(self,self.ground_ip)
        self.thread_elink = None
        self.data_manager = DataManager(self, self.info_logger, self.data_logger)
        self.thread_data_manager = None
        self.dmc = dmc.DMC(self)
        self.thread_dmc = None
        self.heat = heat.HEAT(self)
        self.thread_heat = None
        #@TODO uncomment next line
        #self.adc = adc.ADC(self)
        self.thread_adc = None
        self.tx = tx.TX(self)
        self.thread_tx = None
        self.counterdown = CounterDown(self)
        self.paths = paths.Paths()
        #self.pin_powerB = pins.Pins().pin_powerB # @TODO change it in boot/config.txt
        GPIO.setmode(GPIO.BOARD)
        #GPIO.setup(self.pin_powerB, GPIO.OUT)
        #GPIO.output(self.pin_powerB, GPIO.HIGH)
        Master.__instance = self

    @staticmethod
    def get_instance():

        if Master.__instance is None:
            Master()
        return Master.__instance

    def start(self):

        self.init_experiment()

        while not self.status_vector['RET_CONF'] and not self.get_command('KILL'):
            sleep(self.counterdown.master_time_runs)
            if self.get_command('REBOOT_SLAVE'):
                self.info_logger.write_info('MASTER ESRANGE: REBOOT SLAVE')
                self.command_vector['REBOOT_SLAVE'] = 0
                self.reboot_slave()
            if self.get_command('REBOOT'):
                self.command_vector['REBOOT'] = 0
                self.status_vector['KILL'] = 1
                self.info_logger.write_info('MASTER ESRANGE: SELF - REBOOT IN 10 secs')
                sleep(self.counterdown.master_wait_self_reboot)
                pass
            #@TODO uncomment to keep the exp status
            #json.dump(self.status_vector, open(self.paths.file_status_vector, 'w'))

        # kill threads
        self.status_vector['KILL'] = 1
        sleep(self.counterdown.master_wait_others_to_die)
        self.info_logger.write_info('MASTER ESRANGE: KILLED ADC + TX')

        if self.thread_dmc is not None:
            self.thread_dmc.join()

        self.info_logger.write_warning('MASTER ESRANGE: SHADE IS TERMINATED')

    def init_experiment(self):
        self.status_vector = json.load(open(self.paths.file_status_vector))
        self.command_vector = json.load(open(self.paths.file_command_vector))
        self.init_elink()
        self.init_data_manager()
        self.init_subsystems()
        self.info_logger.write_info('MASTER ESRANGE: INIT EXP DONE')

    def init_elink(self):
        self.thread_elink = threading.Thread(target=self.elink.start).start()
        self.info_logger.write_info('MASTER ESRANGE: ELINK THREADED')

    def init_data_manager(self):
        self.thread_data_manager = threading.Thread(target=self.data_manager.start).start()
        self.info_logger.write_info('MASTER ESRANGE: DATAMANAGER THREADED')

    def init_subsystems(self):
        #@TODO RM FAKE - START ADC ORIGINAL
        #self.thread_adc = threading.Thread(target=self.adc.start).start()
        self.thread_adc = threading.Thread(target=self.adc_FAKE).start()
        self.thread_dmc = threading.Thread(target=self.dmc.start).start()
        self.thread_heat = threading.Thread(target=self.heat.start).start()
        self.thread_tx = threading.Thread(target=self.tx.start).start()
        self.info_logger.write_info('MASTER ESRANGE: SUBSYSTEMS THREADED')

    #@TODO rm adc_FAKE
    def adc_FAKE(self):
        self.info_logger.write_warning('MASTER ESRANGE: FAKE ADC THREADED')
        motor_ADC = MotorADC()
        while not self.status_vector['KILL']:
            self.info_logger.write_info('MASTER ESRANGE: FAKE ADC ACTION')
            motor_ADC.act(100,1)
            motor_ADC.act(100,1)
            motor_ADC.act(200,0)
            sleep(self.counterdown.adc_fake_runs)

    def get_command(self, command):
        try:
            return self.command_vector[command]
        except:
            return 0

    def reboot_slave(self):
        #power off and power on the other ras
        pass
        #GPIO.output(self.pin_powerB, GPIO.LOW)
        #sleep(self.counterdown.reboot_low_wait)
        #GPIO.output(self.pin_powerB, GPIO.HIGH)


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

