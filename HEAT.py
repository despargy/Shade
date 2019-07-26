from threading import Thread
from time import sleep
import queue
from statistics import mean
import random
from logger import InfoLogger
#import RPi.GPIO as GPIO


class HEAT(object):

    __instance = None

    def __init__(self, master_):

        if HEAT.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
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
            self.master = master_
            self.infologger = self.master.infologger
            HEAT.__instance = self
            self.infologger.write_info('HEAT PROCESS START')

    def get_instance(self):

        if HEAT.__instance is None:
            HEAT(None)
        return HEAT.__instance

    def start(self):

        self.infologger.write_info('START HEAT PROCESS')
        thread_data = Thread(target=self.threaded_function_data)
        thread_data.start()
        while True:

            while self.master.get_command('HEAT_SLEEP'):
                self.infologger.write_info('Reinforce CLOSE HEAT')
                self.pause_heat()
                sleep(5)

            self.need_heating = self.consider_data()
            if self.need_heating and not self.master.status_vector['HEAT_ON']:
                self.open_heat()
            elif not self.need_heating and self.master.status_vector['HEAT_ON']:
                self.pause_heat()
            sleep(3)

    def consider_data(self):

        if not self.data_queue.empty():
            l = list(self.data_queue.queue)
            self.mean_temp = mean(l)
            #print("list = ", l)
            self.infologger.write_info('MEAN TEMP {}'.format(self.mean_temp))
            return self.mean_temp < self.temp_thresshold

    def open_heat(self):

        self.infologger.write_info('HEAT ON')
        #GPIO.output(self.pin_heaterA, GPIO.HIGH)
        #GPIO.output(self.pin_heaterB, GPIO.HIGH)
        self.master.status_vector['HEAT_ON'] = 1

    def pause_heat(self):

        self.infologger.write_info('HEAT OFF')
        #GPIO.output(self.pin_heaterA, GPIO.LOW)
        #GPIO.output(self.pin_heaterB, GPIO.LOW)
        self.master.status_vector['HEAT_ON'] = 0

    def threaded_function_data(self):

        while True:
            temp = random.randrange(-14,20,1)
            #temp = self.datamanager.dictionary['ext_temp']
            if temp is None:
                self.infologger.write_warning('Invalid temperature data HEAT')
            else:
                if self.data_queue.full():
                    self.data_queue.get()
                self.data_queue.put(temp) #put or put_nowait?
                sleep(1)

