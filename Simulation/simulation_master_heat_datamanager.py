import HEAT as heat
import elinkmanager
#from datamanager import DataManager
from counterdown import CounterDown
import threading
from logger import InfoLogger, DataLogger, AdcsLogger
from time import sleep
import sys
#import RPi.GPIO as GPIO
import json
import  Paths as paths
import Pins as pins

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
        #self.data_manager = DataManager(self, self.info_logger, self.data_logger)
        #self.thread_data_manager = None
        self.heat = heat.HEAT(self)
        self.thread_heat = None
        self.counterdown = CounterDown(self)
        self.paths = paths.Paths()
        self.pin_powerB = pins.Pins().pin_powerB # @TODO change it in boot/config.txt
        #GPIO.setmode(GPIO.BOARD)
        #GPIO.setup(self.pin_powerB, GPIO.OUT)
        Master.__instance = self

    @staticmethod
    def get_instance():

        if Master.__instance is None:
            Master()
        return Master.__instance

    def start(self):

        self.init_experiment()

        while  not self.get_command('KILL'):
            sleep(self.counterdown.master_time_runs)
            if self.get_command('REBOOT_SLAVE'):
                self.command_vector['REBOOT_SLAVE'] = 0
                self.reboot_slave()
            if self.get_command('REBOOT'):
                pass
            json.dump(self.status_vector, open(self.paths.file_status_vector, 'w'))

        # kill threads
        self.status_vector['KILL'] = 1
        self.info_logger.write_warning('MASTER_ESRANGE: SHADE IS TERMINATED')
        print('shade is terminated')
        # @TODO RESTART SHADE n REBOOT

    def init_experiment(self):
        self.status_vector = json.load(open(self.paths.file_status_vector))
        self.command_vector = json.load(open(self.paths.file_command_vector))
        self.init_elink()
        #self.init_data_manager()
        self.init_subsystems()

    def init_elink(self):
        self.thread_elink = threading.Thread(target=self.elink.start).start()

#    def init_data_manager(self):
#        pass
#        self.thread_data_manager = threading.Thread(target=self.data_manager.start).start()

    def init_subsystems(self):
        self.thread_heat = threading.Thread(target=self.heat.start).start()

    def get_command(self, command):
        try:
            return self.command_vector[command]
        except:
            return 0

    def reboot_slave(self):
        pass
        #power off and power on the other ras
        #GPIO.output(self.pin_powerB, GPIO.LOW)
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

