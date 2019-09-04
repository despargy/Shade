import HEAT_HAI as heat
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


class Master:

    __instance = None

    def __init__(self):

        self.status_vector = dict()
        self.command_vector = dict()
        self.info_logger = InfoLogger()
        self.data_logger = DataLogger()
        self.data_manager = DataManager(self, self.info_logger, self.data_logger)
        self.thread_data_manager = None
        self.heat = heat.HEAT_HAI(self)
        self.thread_heat = None
        self.counterdown = CounterDown(self)
        self.paths = paths.Paths()
        self.pin_powerB = pins.Pins().pin_powerB # @TODO change it in boot/config.txt
        GPIO.setmode(GPIO.BOARD)
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
            sleep(2)
            print('FROM HAI EXT: PASS')
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
        self.init_data_manager()
        self.init_subsystems()

    def init_data_manager(self):
        #pass
        self.thread_data_manager = threading.Thread(target=self.data_manager.start).start()

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

        Master().start()

