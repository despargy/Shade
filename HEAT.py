from threading import Thread
from time import sleep
import queue
from statistics import mean
from counterdown import CounterDown
import random
import Pins as pins
import RPi.GPIO as GPIO


class HEAT(object):

    __instance = None

    def __init__(self, master_):

        if HEAT.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.master = master_
            self.data_manager = self.master.data_manager
            self.info_logger = self.master.info_logger
            self.counterdown = CounterDown(master_)
            self.need_heating_A = False
            self.need_heating_B = False
            self.temp_thresshold = -20
            self.mean_temp_A = self.temp_thresshold
            self.mean_temp_B = self.temp_thresshold
            self.max_size = 10
            self.data_queue_A = queue.Queue(self.max_size)
            self.data_queue_B = queue.Queue(self.max_size)
            self.pin_heaterA = pins.Pins().pin_heaterA #pin for Heater A
            self.pin_heaterB = pins.Pins().pin_heaterB #pin for Heater B
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.pin_heaterA, GPIO.OUT)
            GPIO.output(self.pin_heaterA, GPIO.LOW)
            GPIO.setup(self.pin_heaterB, GPIO.OUT)
            GPIO.output(self.pin_heaterB, GPIO.LOW)
            HEAT.__instance = self

    @staticmethod
    def get_instance():

        if HEAT.__instance is None:
            HEAT(None)
        return HEAT.__instance

    def start(self):

        self.info_logger.write_info("HEAT: START HEAT PROCESS")
        thread_data = Thread(target=self.threaded_function_data)
        thread_data.start()
        while not self.master.status_vector['RET_SUCS'] and not self.master.status_vector['KILL']:

            while self.master.get_command("HEAT_SLEEP") and not self.master.get_command('HEAT_AWAKE'):
                self.master.status_vector['HEAT_SLEEP'] = 1
                self.info_logger.write_info("HEAT: R-CLOSE HEAT")
                self.pause_heat_A()
                self.pause_heat_B()
                sleep(self.counterdown.heat_time_check_awake)

            self.master.status_vector['HEAT_SLEEP'] = 0
            self.master.command_vector['HEAT_SLEEP'] = 0
            self.master.command_vector['HEAT_AWAKE'] = 0

            self.need_heating_A = self.consider_data_A()
            self.need_heating_B = self.consider_data_B()

            if self.need_heating_A and not self.master.status_vector["HEAT_A_ON"]:
                self.open_heat_A()
            elif not self.need_heating_A and self.master.status_vector["HEAT_A_ON"]:
                self.pause_heat_A()

            if self.need_heating_B and not self.master.status_vector["HEAT_B_ON"]:
                self.open_heat_B()
            elif not self.need_heating_B and self.master.status_vector["HEAT_B_ON"]:
                self.pause_heat_B()

            if self.master.get_command('HEAT_OPEN'):
                self.info_logger.write_info("HEAT: OPEN MANUAL")
                self.master.command_vector['HEAT_OPEN'] = 0
                self.open_heat_A()
                self.open_heat_B()

            sleep(self.counterdown.heat_time_runs)

        return 0

    def consider_data_A(self):

        if not self.data_queue_A.empty():
            self.mean_temp = mean(list(self.data_queue_A.queue))
            self.info_logger.write_info("HEAT : MEAN TEMP A {}".format(self.mean_temp))
            return self.mean_temp < self.temp_thresshold
        else:
            return False

    def consider_data_B(self):

        if not self.data_queue_B.empty():
            self.mean_temp = mean(list(self.data_queue_B.queue))
            self.info_logger.write_info("HEAT : MEAN TEMP B {}".format(self.mean_temp))
            return self.mean_temp < self.temp_thresshold
        else:
            return False


    def open_heat_A(self):

        GPIO.output(self.pin_heaterA, GPIO.HIGH)
        self.info_logger.write_info("HEAT: A HEAT ON")
        self.master.status_vector["HEAT_A_ON"] = 1

    def open_heat_B(self):

        GPIO.output(self.pin_heaterB, GPIO.HIGH)
        self.info_logger.write_info("HEAT: B HEAT ON")
        self.master.status_vector["HEAT_B_ON"] = 1

    def pause_heat_A(self):

        GPIO.output(self.pin_heaterA, GPIO.LOW)
        self.info_logger.write_info("HEAT: A HEAT OFF")
        self.master.status_vector["HEAT_A_ON"] = 0

    def pause_heat_B(self):

        GPIO.output(self.pin_heaterB, GPIO.LOW)
        self.info_logger.write_info("HEAT: B HEAT OFF")
        self.master.status_vector["HEAT_B_ON"] = 0

    def threaded_function_data(self):

        while not self.master.status_vector['RET_SUCS'] and not self.master.status_vector['KILL']:

            temp_A = self.data_manager.get_data("temp_A")
            temp_B = self.data_manager.get_data("temp_B")

            if self.master.status_vector['TEMP_A'] == 0 or temp_A is None:
                self.info_logger.write_warning("HEAT: Invalid temperature A data HEAT")
            else:
                if self.data_queue_A.full():
                    self.data_queue_A.get()
                self.data_queue_A.put(temp_A)

            if self.master.status_vector['TEMP_B'] == 0 or temp_B is None:
                self.info_logger.write_warning("HEAT: Invalid temperature B data HEAT")
            else:
                if self.data_queue_B.full():
                    self.data_queue_B.get()
                self.data_queue_B.put(temp_B)

            sleep(self.counterdown.heat_time_updates_data)

