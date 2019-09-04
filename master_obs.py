#import elinkmanager
import OBCS as obcs
import threading
from time import sleep
import sys
from logger import InfoLogger
import RPi.GPIO as GPIO
import Pins as pins

class Master_Obs:

    __instance = None

    def __init__(self, ground_ip):

        self.master_time_runs = 3
        self.master_waits_camera_close = 2
        self.status_vector = dict()
        self.command_vector = dict()
        self.ground_ip = ground_ip
        self.info_logger = InfoLogger()
        #self.elink = elinkmanager.ELinkManager(self,self.ground_ip)
        #self.thread_elink = None
        self.obcs = obcs.OBCS(self)
        self.thread_obcs = None
        self.pin_powerA = pins.Pins().pin_powerA # @TODO change it in boot/config.txt
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin_powerA, GPIO.OUT)
        Master_Obs.__instance = self


    @staticmethod
    def get_instance():

        if Master_Obs.__instance is None:
            Master_Obs()
        return Master_Obs.__instance


    def init_status_vector(self):
        # Camera
        self.status_vector['REC'] = 0       # 0
        #Experiment
        self.status_vector['CLOSE'] = 1       # 1

    def init_command_vector(self):
        #REBOOT
        self.command_vector['REBOOT_SLAVE'] = 0
        self.command_vector['CLOSE'] = 0


    def start(self):

        self.init_experiment()
        self.status_vector['REC'] = 1
        while not self.get_command('CLOSE'):
            sleep(self.master_time_runs)
            if self.get_command('REBOOT_SLAVE'):
                self.command_vector['REBOOT_SLAVE'] = 0
                self.reboot_slave()
                print('on reboot slave')
                self.info_logger.write_info('MASTER_OBCS: reboot slave')
            if self.get_command('CLOSE'):
                self.status_vector['CLOSE'] = 1
                self.info_logger.write_info('MASTER_OBCS: wait camera to close')
                sleep(self.master_waits_camera_close)
                print('on wait camera')
                pass
                # waits to close camera
        self.status_vector['REC'] = 0
        self.info_logger.write_info('MASTER_OBCS: Obs on close')
        print('Obs on close')

    def init_experiment(self):
        self.init_status_vector()
        self.init_command_vector()
        self.init_elink()
        self.init_obcs()

    def init_elink(self):
        pass
        #self.thread_elink = threading.Thread(target=self.elink.start).start()

    def init_obcs(self):
        self.thread_obcs = threading.Thread(target=self.obcs.start).start()

    def get_command(self, command):
        try:
            return self.command_vector[command]
        except:
            return 0

    def reboot_slave(self):
        pass
        #power off and power on the other ras
        GPIO.output(self.pin_powerA, GPIO.LOW)
        GPIO.output(self.pin_powerA, GPIO.HIGH)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("""
              [+] Run master program with one argument.
              [+] The argument indicates the ground IP
              [+] e.g python master_obs.py 195.168.0.1

              [+] For Testing purposes use 'local' as argument
              [+] to simulate a connection locally
              [+] e.g python master_obs.py local
              """)
    else:
        ground_ip = sys.argv[1]
        Master_Obs(ground_ip).start()
