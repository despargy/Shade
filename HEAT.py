from threading import Thread
from time import sleep
import queue
from statistics import mean
from counterdown import CounterDown
import random
#import RPi.GPIO as GPIO


class HEAT(object):

    __instance = None

    def __init__(self, master_):

        if HEAT.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.master = master_
            #self.data_manager = self.master.data_manager
            self.info_logger = self.master.info_logger
            self.counterdown = CounterDown(master_)
            self.need_heating = False
            self.temp_thresshold = 10
            self.mean_temp = self.temp_thresshold
            self.max_size = 5
            self.data_queue = queue.Queue(self.max_size)
            self.pin_heaterA = 24 #pin for Heater A
            self.pin_heaterB = 25 #pin for Heater B
            #GPIO.setmode(GPIO.BOARD)
            #GPIO.setup(self.pin_heaterA, GPIO.OUT)
            #GPIO.setup(self.pin_heaterB, GPIO.OUT)
            HEAT.__instance = self

    @staticmethod
    def get_instance():

        if HEAT.__instance is None:
            HEAT(None)
        return HEAT.__instance

    def start(self):

        self.info_logger.write_info("START HEAT PROCESS")
        thread_data = Thread(target=self.threaded_function_data)
        thread_data.start()
        while not self.master.status_vector['RET_SUCS']:

            while self.master.get_command("HEAT_SLEEP") and not self.master.get_command('HEAT_AWAKE'):
                self.master.status_vector['HEAT_SLEEP'] = 1
                self.info_logger.write_info("Reinforce CLOSE HEAT")
                self.pause_heat()
                sleep(self.counterdown.heat_time_check_awake)

            self.master.status_vector['HEAT_SLEEP'] = 0
            self.master.command_vector['HEAT_SLEEP'] = 0
            self.master.command_vector['HEAT_AWAKE'] = 0

            self.need_heating = self.consider_data()
            if self.need_heating and not self.master.status_vector["HEAT_ON"]:
                self.open_heat()
            elif not self.need_heating and self.master.status_vector["HEAT_ON"]:
                self.pause_heat()
            sleep(self.counterdown.heat_time_runs)

    def consider_data(self):

        if not self.data_queue.empty():
            self.mean_temp = mean(list(self.data_queue.queue))
            self.info_logger.write_info("MEAN TEMP {}".format(self.mean_temp))
            return self.mean_temp < self.temp_thresshold

    def open_heat(self):

        #GPIO.output(self.pin_heaterA, GPIO.HIGH)
        #GPIO.output(self.pin_heaterB, GPIO.HIGH)
        self.info_logger.write_info("HEAT ON")
        self.master.status_vector["HEAT_ON"] = 1

    def pause_heat(self):

        #GPIO.output(self.pin_heaterA, GPIO.LOW)
        #GPIO.output(self.pin_heaterB, GPIO.LOW)
        self.info_logger.write_info("HEAT OFF")
        self.master.status_vector["HEAT_ON"] = 0

    def threaded_function_data(self):

        while not self.master.status_vector['RET_SUCS']:
            temp = random.randrange(-14,20,1)
            #temp = self.data_manager.get_data("ext_temp")
            if temp is None:
                self.info_logger.write_warning("Invalid temperature data HEAT")
            else:
                if self.data_queue.full():
                    self.data_queue.get()
                self.data_queue.put(temp) #put or put_nowait?
                sleep(self.counterdown.heat_time_updates_data)
                #self.counterdown.countdown0(self.counterdown.time_heat_updates_data)

