import ADC as adc
import HEAT as heat
import DMC as dmc
from datamanager import DataManager
from counterdown import CounterDown
import threading
from logger import InfoLogger, DataLogger
from time import sleep

class Master:

    __instance = None

    def __init__(self):

        self.status_vector = dict()
        self.command_vector = dict()
        self.infologger = InfoLogger()
        self.datalogger = DataLogger()
        self.datamanager = DataManager(self, self.infologger, self.datalogger)
        self.dmc = dmc.DMC(self)
        self.thread_dmc = None
        self.heat = heat.HEAT(self)
        self.thread_heat = None
        self.adc = adc.ADC(self)
        self.thread_adc = None
        #self.tx = tx.TX()
        #self.thread_tx = None
        self.counterdown = CounterDown(self)
        self.step_of_set = 1234
        Master.__instance = self

    @staticmethod
    def get_instance():

        if Master.__instance is None:
            Master()
        return Master.__instance


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
        self.status_vector['DEP_CONF'] = 0  #0
        self.status_vector['DEP_AB'] = 0    #0
        self.status_vector['DEP_SUCS'] = 0  #0
        self.status_vector['DEP_READY'] = 0 #0
        self.status_vector['RET_READY'] = 0 #0
        self.status_vector['RET_CONF'] = 0  #0
        self.status_vector['RET_AB'] = 0    #0
        self.status_vector['RET_SUCS'] = 0  #0
        #Experiment
        self.status_vector['CLOSE'] = 0

    def init_command_vector(self):
        #ADC
        self.command_vector['ADC_MAN'] = 0
        self.command_vector['ADC_AUTO'] = 0
        self.command_vector['SET'] = 0
        self.command_vector['SCAN'] = 0
        #HEAT
        self.command_vector['HEAT_SLEEP'] = 0
        #DMC
        self.command_vector['DEP'] = 0
        self.command_vector['DEP_CONF'] = 0
        self.command_vector['DEP_AB'] = 0
        self.command_vector['DEP_SUCS'] = 0
        self.command_vector['DEP_RETRY'] = 0
        self.command_vector['DMC_AWAKE'] = 0
        self.command_vector['RET_CONF'] = 0
        self.command_vector['RET_AB'] = 0
        self.command_vector['RET'] = 0
        self.command_vector['RET_SUCS'] = 0
        self.command_vector['RET_RETRY'] = 0
        #Experiment
        self.command_vector['STOP'] = 0
        self.command_vector['SHADE'] = 0
        self.command_vector['CLOSE'] = 0



        #ONLY FOR TESTING
        #self.command_vector['DEP'] = 1
        #self.command_vector['DEP_AB'] = 1
        #self.command_vector['DEP_CONF'] = 0
        #self.command_vector['DEP_RETRY'] = 0
        #self.command_vector['RET'] = 0
        #self.command_vector['RET_AB'] = 1

        #

    def start(self):

        while self.status_vector['CLOSE']:
            self.init_experiment()

            while self.get_command('STOP'):
                sleep(self.counterdown.master_checks_dep_sucs)
                if self.status_vector['DEP_SUCS']:
                    self.handle_manual_adc()

            if self.thread_adc is not None:
                self.thread_adc.join()
            #if self.thread_tx is not None:
                #self.thread_tx.join()
            if self.thread_dmc is not None:
                self.thread_dmc.join()

            choice = self.counterdown.countdown2(self.counterdown.timeout_cmd, 'CLOSE', 'SHADE')
            if choice == 1:
                self.status_vector['CLOSE'] = 1
                self.infologger.write_warning('SHADE IS TERMINATED')



    def init_experiment(self):
        self.init_status_vector()
        self.init_command_vector()
        # self.init_elink()
        self.init_datamanager()
        self.init_subsystems()

    def init_datamanager(self):
        thread_datamanager = threading.Thread(target=self.datamanager.start).start()

    def init_subsystems(self):
        # self.thread_adc = threading.Thread(target=self.adc.start).start()
        self.thread_dmc = threading.Thread(target=self.dmc.start).start()
        # self.thread_heat = threading.Thread(target=self.heat.start).start()
        # self.thread_tx =

    def handle_manual_adc(self):
        while self.get_command('ADC_MAN'):
            sleep(self.counterdown.master_time_checks_adc_man_cmd)
            self.status_vector['ADC_MAN'] = 1
            self.command_vector['ADC_AUTO'] = 0  # re-init
            choice = self.counterdown.countdown2(self.counterdown.timeout_cmd, 'SET', 'SCAN')
            if choice == 1:
                self.adc.adcslogger.write_info('FROM MASTER IN SET')
                self.counterdown.countdown0(self.counterdown.timeout_cmd)
                #@TOCHECK INT SET - RIGHT INTERRUPT GET CMD
                self.step_of_set = self.get_step()
                if type(self.step_of_set) in int and self.step_of_set != 1234:
                    self.adc.set_position(self.step_of_set)
                else:
                    self.adc.adcslogger.write_warning('FROM MASTER INVALID STEP OF SET')
            elif choice == 2:
                self.adc.adcslogger.write_info('FROM MASTER IN SCAN')
                self.adc.scan()
            self.command_vector['SET'] = 0 #re-init
            self.step_of_set = 1234 #re-init
            self.command_vector['SCAN'] = 0 #re-init
            choice = self.counterdown.countdown3(self.counterdown.master_time_breaks_adc_man, 'SET', 'SCAN', 'ADC_AUTO')
            if choice == 1 or choice == 2:
                self.adc.adcslogger.write_info('FROM MASTER CONT ADC MAN')
            else:
                self.command_vector['ADC_MAN'] = 0 #re-init
                self.status_vector['ADC_MAN'] = 0 #re-init
                self.adc.adcslogger.write_info('FROM MASTER BREAK ADC MAN')



    def get_command(self, command):
        try:
            return self.command_vector[command]
        except:
            return 0

    def get_step(self):
        return self.step_of_set

if __name__ == '__main__':
    master = Master()
    master.start()