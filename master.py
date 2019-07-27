import ADC as adc
import HEAT as heat
import DMC as dmc
from datamanager import DataManager
from counterdown import CounterDown
import threading
from logger import InfoLogger, DataLogger
from time import sleep

class Master:

    def __init__(self):

        self.status_vector = dict()
        self.command_vector = dict()
        self.infologger = InfoLogger()
        self.datalogger = DataLogger()
        self.datamanager = DataManager(self, self.infologger, self.datalogger)
        self.dmc = dmc.DMC(self)
        self.heat = heat.HEAT(self)
        self.adc = adc.ADC(self)
        #self.tx = tx.TX(self)
        self.counterdown = CounterDown(self)

    def init_status_vector(self):
        #Data
        self.status_vector['GPS'] = 1       #1
        self.status_vector['COMPASS'] = 1   #1
        self.status_vector['IMU'] = 1       #1
        self.status_vector['ALTIMETER'] = 1 #1
        self.status_vector['TEMP'] = 1      #1
        #Heat
        self.status_vector['HEAT_ON'] = 0   #0
        #Transmition
        self.status_vector['AMP_ON'] = 0    #0
        self.status_vector['TX_ON'] = 0     #0
        #ADC
        self.status_vector['ADC_MAN'] = 0   #0
        #DMC
        self.status_vector['DEP_READY'] = 0 #0
        self.status_vector['DEP_CONF'] = 0  #0
        self.status_vector['DEP_AB'] = 0    #0
        self.status_vector['DEP_SUCS'] = 0  #0
        self.status_vector['RET_READY'] = 0 #0
        self.status_vector['RET_CONF'] = 0  #0
        self.status_vector['RET_AB'] = 0    #0
        self.status_vector['RET_SUCS'] = 0  #0

        #ONLY FOR TESTING
        #self.command_vector['DEP'] = 1
        #self.command_vector['DEP_AB'] = 1
        #self.command_vector['DEP_CONF'] = 0
        #self.command_vector['DEP_RETRY'] = 0
        #self.command_vector['RET'] = 0
        #self.command_vector['RET_AB'] = 1

        #

    def start(self):
        self.init_experiment()

        while True:

            if self.status_vector['DEP_SUCS']:
                self.handle_manual_adc()

    def init_experiment(self):
        self.init_status_vector()
        # self.init_elink()
        self.init_datamanager()
        self.init_subsystems()

    def init_datamanager(self):
        thread_datamanager = threading.Thread(target=self.datamanager.start).start()

    def init_subsystems(self):
        # thread_adc = threading.Thread(target=self.adc.start).start()
        thread_dmc = threading.Thread(target=self.dmc.start).start()
        # thread_heat = threading.Thread(target=self.heat.start).start()
        # thread_tx =

    def handle_manual_adc(self):
        if self.status_vector['ADC_MAN']:
            choice = self.counterdown.countdown2(self.counterdown.timeout_cmd, 'SET', 'SCAN')
            if choice == 2:
                pass

    def get_command(self, command):
        try:
            return self.command_vector[command]
        except:
            return 0


if __name__ == '__main__':
    master = Master()
    master.start()