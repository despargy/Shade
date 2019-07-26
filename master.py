import datamanager
import threading, time , sys
from logger import InfoLogger , AdcsLogger, DataLogger


class Master:
    
     def __init__(self):

        self.status_vector = dict()
        #self.command_vector = dict()
        self.infologger = InfoLogger()
        #self.dmc = dmc.DMC(self)
        #self.heat = heat.HEAT(self)
        #self.adc = adc.ADC(self)
        #self.tx = tx.TX(self)
        self.datalogger = DataLogger()
        self.datamanager = datamanager.DataManager(self,self.infologger,self.datalogger)
        
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
        self.status_vector['DEP_SUCS'] = 1  #1
        self.status_vector['RET_READY'] = 0 #0
        self.status_vector['RET_CONF'] = 0  #0
        self.status_vector['RET_AB'] = 0    #0
        self.status_vector['RET_SUCS'] = 0  #0    

     def start(self):

        #Init ELinkManager
        #self.init_elink()
        
        #init_datamanager
        self.init_status_vector()
        self.init_datamanager()
        
     def init_datamanager(self):
        threading.Thread(target=self.datamanager.start).start()    


     @staticmethod
     def get_datalogger_unsend_data():
        return DataLogger.get_instance().get_unsend_data()

     @staticmethod
     def get_infologger_unsend_data():
        return InfoLogger.get_instance().get_unsend_data()


if __name__ == "__main__":
       Master().start()
