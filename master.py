import ADC as adc
import HEAT as heat
import DMC as dmc
import threading
from logger import InfoLogger
from time import sleep
from Motor import MotorADC, MotorDMC

class Master:

    def __init__(self):

        self.status_vector = dict()
        self.command_vector = dict()
        self.infologger = InfoLogger()
        self.dmc = dmc.DMC(self)
        self.heat = heat.HEAT(self)
        self.adc = adc.ADC(self)
        #self.tx = tx.TX(self)

    def init_status_vector(self):
        #Data
        self.status_vector['GPS'] = 1
        self.status_vector['COMPASS'] = 1
        self.status_vector['IMU'] = 1
        self.status_vector['ALTIMETER'] = 1
        self.status_vector['TEMP'] = 1
        #Heat
        self.status_vector['HEAT_ON'] = 0
        #Transmition
        self.status_vector['AMP_ON'] = 0
        self.status_vector['TX_ON'] = 0
        #ADC
        self.status_vector['ADC_MAN'] = 0
        #DMC
        self.status_vector['DEP_READY'] = 0
        self.status_vector['DEP_CONF'] = 0
        self.status_vector['DEP_AB'] = 0
        self.status_vector['DEP_SUCS'] = 1
        self.status_vector['RET_READY'] = 0
        self.status_vector['RET_CONF'] = 0
        self.status_vector['RET_AB'] = 0
        self.status_vector['RET_SUCS'] = 0

    def get_command(self, command):
        try:
            return self.command_vector[command]
        except:
            return 0

    def init_subsystems(self):
        thread_adc = threading.Thread(target=self.adc.start).start()
        #thread_dmc = threading.Thread(target=self.dmc.start).start()
        thread_heat = threading.Thread(target=self.heat.start).start()
        #thread_tx =

    def start(self):

        self.init_status_vector()
        self.init_subsystems()
        #self.init_elink()
        #self.init_datamanager()



if __name__ == '__main__':
    master = Master()
    master.start()