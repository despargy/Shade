import ADC as adc
import threading
from logger import InfoLogger, AdcsLogger, DataLogger


class Master:

    def __init__(self):

        self.adcslogger = AdcsLogger.get_instance()
        self.adc = adc.ADC().get_instance()
        #threading.Thread(target=self.create_s).start()


    def start(self):
        while True:
            thread_adc = threading.Thread(target=self.adc.start(self.adcslogger))
            print("ok")


