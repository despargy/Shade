from threading import Thread
from time import sleep
import queue
from statistics import mean
import random
#import RPi.GPIO as GPIO


class HEAT(object):


    __instance = None

    #, Master, DataManager
    def __init__(self):
        if HEAT.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.ison = False
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
            #self.master = Master
            #self.datamanager = DataManager
            HEAT.__instance = self


    def get_instance(self):
        if HEAT.__instance == None:
            HEAT()
        return HEAT.__instance


    def start(self):
        print("Start HEAT process")
        thread_data = Thread(target=self.threaded_function_data)
        thread_data.start()
        while True:
            self.need_heating = self.consider_data()
            if self.need_heating and not self.ison:
                self.open_heat()
                self.ison = True
            elif not self.need_heating and self.ison:
                self.pause_heat()
                self.ison = False
            sleep(3)


    def consider_data(self):
        if not self.data_queue.empty():
            l = list(self.data_queue.queue)
            self.mean_temp = mean(l)
            print("list = ", l)
            print(self.mean_temp)
            return self.mean_temp < self.temp_thresshold


    def open_heat(self):
        print("ON") #infologger on
        #GPIO.output(self.pin_heaterA, GPIO.HIGH)
        #GPIO.output(self.pin_heaterB, GPIO.HIGH)


    def pause_heat(self):
        print("OFF") #infologger of
        #GPIO.output(self.pin_heaterA, GPIO.LOW)
        #GPIO.output(self.pin_heaterB, GPIO.LOW)


    def threaded_function_data(self):
        while True:
            temp = random.randrange(15,30,1)
            #temp = self.datamanager.dictionary['ext_temp']
            if type(temp) in [int, float]:
                if self.data_queue.full():
                    self.data_queue.get()
                self.data_queue.put(temp) #put or put_nowait?
                sleep(1)

