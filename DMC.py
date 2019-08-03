import time
from Motor import MotorDMC
from counterdown import CounterDown


class DMC:

    __instance = None

    def __init__(self, master_):

        if DMC.__instance is not None:

            raise Exception('This class is a singleton!')
        else:
            self.master = master_
            self.motor_dmc = MotorDMC.get_instance()
            #self.data_manager = self.master.data_manager
            self.info_logger = self.master.info_logger
            self.counterdown = CounterDown(master_)
            self.alti_thresshold = 1000  # 1km
            DMC.__instance = self

    @staticmethod
    def get_instance():

        if DMC.__instance is None:
            DMC(None)
        return DMC.__instance

    def start(self):
        self.master.info_logger.write_info('START DMC  PROCESS')
        print('START DMC  PROCESS')

        while not self.master.status_vector['DEP_CONF']:
            self.phase_zero()
            self.phase_ready_for_deploy()

        while not self.master.status_vector['DEP_SUCS']:
            self.phase_deploy()
        self.phase_sleep()
        self.master.status_vector['DMC_SLEEP'] = 0

        while not self.master.status_vector['RET_CONF']:
            self.phase_check()
        self.phase_kill_before_retrieve()

        while not self.master.status_vector['RET_SUCS']:
            self.phase_retrieve()
        self.master.info_logger.write_info('END DMC PROCESS')
        print('end dmc process')

    def phase_zero(self):
        self.master.command_vector['DEP'] = 0  # re-init if a new cmd come
        self.info_logger.write_info('PHASE ZERO')
        print('phase zero')
        self.counterdown.countdown1(self.counterdown.dmc_time_left_auto_deploy, 'DEP')
        self.master.status_vector['DEP_READY'] = 1

    def phase_ready_for_deploy(self):
        self.master.command_vector['DEP_CONF'] = 0  # re-init if a new cmd come
        self.master.command_vector['DEP_AB'] = 0  # re-init if a new cmd come
        self.info_logger.write_info('PHASE READY DEP')
        print('phase ready dep')
        choice = self.counterdown.countdown2(self.counterdown.dmc_timeout_cmd, 'DEP_CONF', 'DEP_AB')
        if choice == 2:
            self.master.command_vector['DEP'] = 0  # re-init if a new cmd come
            self.master.status_vector['DEP_READY'] = 0
            self.counterdown.dmc_time_left_auto_deploy = 5  # ex. 5min
        else:
            self.master.status_vector['DEP_CONF'] = 1

    def phase_deploy(self):
        self.info_logger.write_info('PHASE DEPLOY')
        print('phase deploy')
        # in that phase status_vector DEP_READY = 1 & DEP_CONF = 1
        self.motor_dmc.motor_deploy()
        self.master.command_vector['DEP_SUCS'] = 0  # re-init if a new cmd come
        self.master.command_vector['DEP_RETRY'] = 0  # re-init if a new cmd come
        choice = self.counterdown.countdown2(self.counterdown.dmc_timeout_cmd, 'DEP_SUCS', 'DEP_RETRY')
        if choice == 2:
            print('retry')
            self.motor_dmc.motor_retrieve()
            time.sleep(2)
        else:
            self.master.status_vector['DEP_SUCS'] = 1

    def phase_sleep(self):
        self.info_logger.write_info('PHASE SLEEP')
        print('phase sleep')
        self.master.status_vector['DMC_SLEEP'] = 1
        self.master.command_vector['DMC_AWAKE'] = 0  # re-init if a new cmd come
        self.counterdown.countdown1(self.counterdown.dmc_time_to_sleep, 'DMC_AWAKE')
        self.master.command_vector['RET'] = 0  # re-init if a new cmd come

    def phase_check(self):
        self.info_logger.write_info('PHASE CHECK')
        print('phase check')
        time.sleep(self.counterdown.dmc_time_checks_altitude)
        altitude = 100000000
        #altitude = self.data_manager.get_data('alti')
        self.master.command_vector['RET_CONF'] = 0  # re-init if a new cmd come
        self.master.command_vector['RET_AB'] = 0  # re-init if a new cmd come
        if self.master.status_vector['ALTIMETER'] and (altitude < self.alti_thresshold) or self.master.get_command('RET'):
            self.master.status_vector['RET_READY'] = 1
            print('ready to retrieve')
            choice = self.counterdown.countdown2(self.counterdown.dmc_timeout_cmd, 'RET_CONF', 'RET_AB')
            if choice == 2:
                self.master.command_vector['RET'] = 0  # re-init if a new cmd come
                self.master.status_vector['RET_AB'] = 1
                self.master.status_vector['RET_READY'] = 0
                self.info_logger.write_info('RETRIEVE ABORT ')
                print('retrieve abort')
            else:
                self.master.status_vector['RET_CONF'] = 1
                self.info_logger.write_info(' RETRIEVE CONFIRMED')
                print('retrieve confirmed')

    def phase_kill_before_retrieve(self):
        self.info_logger.write_warning('PHASE KILLING')
        print('kill status true')
        self.master.status_vector['KILL'] = 1
        time.sleep(self.counterdown.dmc_wait_others_to_killed)  # wait master to kill or dmc kills

    def phase_retrieve(self):
        self.info_logger.write_info('PHASE RETRIEVE')
        print('phase retrieve')
        self.motor_dmc.motor_retrieve()
        self.master.command_vector['RET_SUCS'] = 0  # re-init if a new cmd come
        self.master.command_vector['RET_RETRY'] = 0  # re-init if a new cmd come
        choice = self.counterdown.countdown2(self.counterdown.dmc_timeout_cmd, 'RET_SUCS', 'RET_RETRY')
        print('choice = '.format(choice))
        if choice == 2:
            print('ret_retry')
            self.motor_dmc.motor_deploy()
        else:
            self.master.status_vector['RET_SUCS'] = 1
            print('ret_sucs')
