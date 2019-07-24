import ADC as adc
import threading
from logger import InfoLogger, AdcsLogger, DataLogger


class Master:

    def __init__(self):

        self.adcslogger = AdcsLogger()
        self.adc = adc.ADC(self)
        self.isDeployed = True
        self.isManual = False

        #threading.Thread(target=self.create_s).start()


    def start(self):

        thread_adc = threading.Thread(target=self.adc.start())
        #self.isDeployed = True
        while True:
            print('ok')


if __name__ == '__main__':
    master = Master()
    master.start()