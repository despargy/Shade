from counterdown import CounterDown
from time import sleep
import subprocess, sys, os, threading
import Paths as paths


class TX:

    __instance = None

    def __init__(self, master_):

        if TX.__instance is not None:

            raise Exception('This class is a singleton!')
        else:

            self.master = master_
            self.info_logger = self.master.info_logger
            self.counterdown = CounterDown(master_)
            self.sdr_process = None
            self.file_name_temperature = paths.Paths().tx_file
            self.file_name_predefined_data = paths.Paths().tx_file_pre_data
            self.TX_code_file = 'sdr_TX.py'

    @staticmethod
    def get_instance():

        if TX.__instance is None:
            TX(None)
        return TX.__instance

    def start(self):
        self.info_logger.write_info('TX PROCESS START')
        self.tx_phase_zero()
        self.tx_phase_available()


    def tx_phase_zero(self):
        while not self.master.status_vector['DEP_SUCS'] and not self.master.status_vector['KILL']:
            self.info_logger.write_info('TX WAIT')
            print('tx wait')
            sleep(self.counterdown.tx_time_checks_deploy)

    def tx_phase_available(self):
        #while not self.master.status_vector['KILL']:

        #self.master.command_vector['PRE'] = 0
        #while self.master.get_command('TX_SLEEP'):
            #self.phase_tx_sleep()
        print('tx phase av')
        self.open_amplifier()

        threading.Thread(target=self.start_tx, args=(self.TX_code_file,)).start()
        print('sdt start tx')
            #self.transmit(self.file_name_temperature)

            #while or sleep

            #while not self.master.get_command('PRE') and not self.master.get_command('TX_SLEEP'):
                #print('wait transmition')
                #sleep(self.counterdown.tx_check_to_stop_transmition)

            #if self.master.get_command('PRE'):
                #self.transmit(self.file_name_predefined_data)
                #wait to send data
                # kill sdr process
                #self.sdr_process.kill()

        sleep(10)

            # kill sdr process
        self.kill_tx(self.TX_code_file)

    def transmit(self, file):
        self.info_logger.write_info('TX: TX TRANSMIT'.format(file))
        self.master.status_vector['TX_ON'] = 1
        print('TX TRANSMIT'.format(file))
        try:
            #self.sdr_process = subprocess.call([sys.executable, os.path.join(get_script_dir(), 'sdr_code.py')])
            cmd = 'python3 sdr_code.py'
            self.sdr_process = subprocess.Popen(cmd, stdout=subprocess.PIPE,shell=True, preexec_fn=os.setsid)
            #subprocess.call("/home/despina/Dropbox/BEAM/Software/Shade/sdr_simulation.py", shell=True)
        #@TODO FILE RUN
        except:
            self.info_logger.write_error('TX: SDR PROCESS COULD BE CALLED')
        pass

    def open_amplifier(self):
        self.master.status_vector['AMP_ON'] = 1
        # led amplifier on
        # gpio amp on
        pass

    def close_amplifier(self):
        self.master.status_vector['AMP_ON'] = 0
        # led amplifier off
        # gpio amp off
        pass

    def phase_tx_sleep(self):
        self.close_amplifier()
        self.master.status_vector['TX_ON'] = 0
        self.info_logger.write_warning('TX: FORCE_TX_CLOSED')
        print('FORCE_TX_CLOSED')
        if self.master.get_command('TX_AWAKE'):
            self.master.command_vector['TX_SLEEP'] = 0
            self.master.command_vector['TX_AWAKE'] = 0
            self.master.status_vector['TX_ON'] = 1

    def start_tx(self, name):
        os.system('python2 {name} {file}'.format(name=name, file = self.file_name_temperature))

    def kill_tx(self, name):
        temp_filename = 'tmp_pid'
        os.system('ps -ef | grep {name} > {temp_filename}'.format(name=name, temp_filename=temp_filename))
        with open(temp_filename, 'r') as tmp:
            lines = tmp.readlines()
            for line in lines:
                compoments = line.split()
                curr_name = compoments[-1]
                curr_command = compoments[-2]

                if curr_name == name and curr_command == 'python3':
                    pid = compoments[1]
                    os.system('kill -9 {pid}'.format(pid=pid))
                    os.system('rm -f {temp_filename}'.format(temp_filename=temp_filename))
