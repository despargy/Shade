from counterdown import CounterDown
from time import sleep

class TX:

    __instance = None

    def __init__(self, master_):

        if TX.__instance is not None:

            raise Exception('This class is a singleton!')
        else:

            self.master = master_
            self.info_logger = self.master.info_logger
            self.counterdown = CounterDown(master_)
            self.file_name_temperature = 'tx_temperature_file.txt'
            self.file_name_predefined_data = 'tx_predefined_data.txt'


    @staticmethod
    def get_instance():

        if TX.__instance is None:
            TX(None)
        return TX.__instance

    def start(self):

        self.info_logger.write_info('TX PROCESS START')
        while not self.master.status_vector['DEP_SUCS']:

            self.info_logger.write_info('TX WAIT')
            print('TX WAIT DEP SUCS')
            sleep(self.counterdown.tx_time_checks_deploy)

        if self.master.status_vector['FORCE_TX_CLOSE']:
            self.info_logger.write_warning('FORCE_TX_CLOSE')
        else:
            while not self.master.status_vector['RET_CONF']:

                while not self.master.get_command('PRE'):
                    self.transmite(self.file_name_temperature)

                self.transmite(self.file_name_predefined_data)
                self.master.command_vector['PRE'] = 0

    def transmite(self, file):
        self.info_logger.write_info('TX TRANSMITE')
        print('TX TRANSMITE')
        pass