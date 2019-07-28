import time
from master import Master
from Motor import MotorDMC
from counterdown import CounterDown
from logger import InfoLogger

class DMC:

    __instance = None

    def __init__(self):

        if DMC.__instance is not None:

            raise Exception('This class is a singleton!')
        else:
            self.master = Master.get_instance()
            self.motor_dmc = MotorDMC.get_instance()
            self.datamanager = self.master.datamanager
            self.infologger = self.master.infologger
            self.counterdown = CounterDown()
            self.alti_thresshold = 1000 #1km
            DMC.__instance = self

    @staticmethod
    def get_instance():

        if DMC.__instance is None:
            DMC()
        return DMC.__instance

    def start(self):
        self.master.infologger.write_info('START DMC  PROCESS')

        while not self.master.status_vector['DEP_CONF'] and not self.master.get_command('STOP'):
            self.phase_zero()
            self.phase_ready_for_deploy()

        while not self.master.status_vector['DEP_SUCS'] and not self.master.get_command('STOP'):
            self.phase_deploy()
        self.phase_sleep()

        while not self.master.status_vector['RET_READY'] and not self.master.get_command('STOP'):
            self.phase_check()
        self.phase_warn_retrieve()

        while not self.master.get_command('RET_SUCS') and not self.master.get_command('STOP'):
            self.phase_retrieve()
        self.master.infologger.write_info('END DMC PROCESS')


    def phase_zero(self):
        self.infologger.write_info('PHASE ZERO')
        self.counterdown.countdown1(self.time_left_auto_deploy, 'DEP')
        self.master.status_vector['DEP_READY'] = 1

    def phase_ready_for_deploy(self):
        self.infologger.write_info('PHASE READY DEP')
        choice = self.counterdown.countdown2(self.counterdown.timeout_cmd, 'DEP_CONF', 'DEP_AB')
        if choice == 2:
            self.master.command_vector['DEP_AB'] = 0  # re-init if a new cmd come
            self.master.command_vector['DEP'] = 0  # re-init if a new cmd come
            self.master.status_vector['DEP_READY'] = 0
            self.time_left_auto_deploy = 5 #ex. 5min
        else:
            self.master.status_vector['DEP_CONF'] = 1

    def phase_deploy(self):
        self.infologger.write_info('PHASE DEPLOY')
        # in that phase status_vector DEP_READY = 1 & DEP_CONF = 1
        if self.master.status_vector['DEP_READY'] != 1 or self.master.status_vector['DEP_CONF'] != 1 :
            self.infologger.write_error('CHECK CONDITIONS FOR DEP')
        self.motor_dmc.motor_deploy()
        choice = self.counterdown.countdown2(self.counterdown.timeout_cmd, 'DEP_SUCS', 'DEP_RETRY')
        if choice == 2:
            self.master.command_vector['DEP_RETRY'] = 0  # re-init if a new cmd come
            self.motor_dmc.motor_retrieve()
            time.sleep(2)
        else:
            self.master.status_vector['DEP_SUCS'] = 1

    def phase_sleep(self):
        self.infologger.write_info('PHASE SLEEP')
        self.counterdown.countdown1(self.counterdown.dmc_time_to_sleep, 'DMC_AWAKE')

    def phase_check(self):
        self.infologger.write_info('PHASE CHECK')
        time.sleep(1)
        altitude = self.datamanager.get_data('alti')
        if self.master.status_vector['ALTIMETER'] and (altitude < self.alti_thresshold) :
            self.master.status_vector['RET_READY'] = 1
            choice = self.counterdown.countdown2(self.counterdown.timeout_cmd, 'RET_CONF', 'RET_AB')
            if choice == 2:
                self.master.command_vector['RET_AB'] = 0  # re-init if a new cmd come
                self.master.status_vector['RET_READY'] = 0
                self.infologger.write_info('PHASE ABORT RETRIEVE')
            else:
                self.master.status_vector['RET_CONF'] = 1
        elif self.master.get_command('RET'):
            self.master.status_vector['RET_READY'] = 1
            self.master.status_vector['RET_CONF'] = 1

    def phase_warn_retrieve(self):
        self.infologger.write_warning('PHASE RET READY')
        self.master.command_vector['STOP'] = 1
        time.sleep(self.counterdown.dmc_wait_others_to_killed) #wait master to kill or dmc kills


    def phase_retrieve(self):
        self.infologger.write_info('PHASE TO RETRIEVE')
        self.motor_dmc.motor_retrieve()
        choice = self.counterdown.countdown2(self.counterdown.timeout_cmd, 'RET_SUCS', 'RET_RETRY')
        if choice == 2:
            self.master.command_vector['RET_RETRY'] = 0  # re-init if a new cmd come
            self.motor_dmc.motor_deploy()
        else:
            self.master.command_vector['RET_SUCS'] = 1
