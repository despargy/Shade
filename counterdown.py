from time import sleep

class CounterDown:

    def __init__(self, master_):

        self.master = master_
        self.heat_time_check_awake = 10
        self.heat_time_runs = 5
        self.heat_time_updates_data = 5

        self.adc_time_checks_deploy = 10
        self.adc_wait_manual_ends = 5
        self.adc_wait_auto_ends = 10
        self.adc_auto_time_runs = 5
        self.adc_man_time_runs = 5
        self.adc_man_timeout_to_set_or_scan = 60
        self.adc_man_time_breaks = 60
        self.adc_fake_runs = 20

        self.dmc_time_left_auto_deploy = 2*60*60  # 2*60*60 #ex. 2hours
        self.dmc_timeout_cmd = 3*60  # ex. 3 mins
        self.dmc_time_to_sleep = 2*60*60  # ex. 2 hour
        self.dmc_wait_others_to_killed = 30
        self.dmc_time_checks_altitude = 10

        self.master_time_runs = 5
        self.master_wait_self_reboot = 10
        self.master_wait_others_to_die = 30
        self.timeout_cmd = 2*60
        self.timeout_cmd_steps = 60
        self.tx_time_checks_deploy = 10
        self.tx_check_to_stop_transmition = 3
        self.tx_duration_sin = 60

        self.reboot_low_wait = 10

    def countdown0(self, t):
        while t:
            mins, secs = divmod(t, 60)
            timeformat = 'COUNTER: {:02d}:{:02d}'.format(mins, secs)
            self.master.info_logger.write_info('{}'.format(timeformat, end='\r'))
            sleep(1)
            t -= 1

    def countdown1(self, t, cmd):
        while t:
            mins, secs = divmod(t, 60)
            timeformat = 'COUNTER: {:02d}:{:02d}'.format(mins, secs)
            self.master.info_logger.write_info('{} break {}'.format(timeformat, cmd, end='\r'))
            sleep(1)
            t -= 1
            if self.master.get_command(cmd):
                break

    def countdown2(self, t, cmd1, cmd2):
        ret = 0
        while t:
            mins, secs = divmod(t, 60)
            timeformat = 'COUNTER: {:02d}:{:02d}'.format(mins, secs)
            self.master.info_logger.write_info('{} break {} or {}'.format(timeformat, cmd1, cmd2, end='\r'))
            sleep(1)
            t -= 1
            if self.master.get_command(cmd1):
                ret = 1
                break
            elif self.master.get_command(cmd2):
                ret = 2
                break
        return ret

    def countdown3(self, t, cmd1, cmd2, cmd3):
        ret = 0
        while t:
            mins, secs = divmod(t, 60)
            timeformat = 'COUNTER: {:02d}:{:02d}'.format(mins, secs)
            self.master.info_logger.write_info('COUNTER: {}'.format(timeformat, end='\r'))
            sleep(1)
            t -= 1
            if self.master.get_command(cmd1):
                ret = 1
                break
            elif self.master.get_command(cmd2):
                ret = 2
                break
            elif self.master.get_command(cmd3):
                ret = 3
                break
        return ret