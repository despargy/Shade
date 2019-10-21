from time import sleep
import math
from Antenna import Antenna
from Motor import MotorADC, MotorDMC
from counterdown import CounterDown
from threading import Thread
import random

class ADC:

    __instance = None

    def __init__(self, master_):

        if ADC.__instance is not None:

            raise Exception('This class is a singleton!')
        else:
            """
                GS: x- axis y-axis of SHADE Ground Station - static
                gps: x- axis y-axis of Gondola's  current x,y-axis
                compass: data received from compass, degrees btwn North and Gondola 0,0
                antenna_adc: object of antenna instance
                direction: clockwise (1) or anti-clockwise(0) for antenna base rotation
                difference: degrees which are needed for antenna base rotation
            """
            self.master = master_
            self.antenna_adc = Antenna()
            self.motor_adc = MotorADC.get_instance()
            self.motor_dmc = MotorDMC.get_instance()
            self.data_manager = self.master.data_manager
            self.info_logger = self.master.info_logger
            self.adcs_logger = self.master.adcs_logger
            self.counterdown = CounterDown(master_)
            self.info_logger.write_info('antenna at {}'.format(self.antenna_adc.position))
            #@TODO GS gps data
            self.GS = [210631.24000000002, 678785.42]
            self.compass = 0
            self.gps = self.GS
            self.direction = 1
            self.difference = 0
            self.valid_data = True
            ###color
            self.color_string = None
            self.stop_turn = False
            self.dir_init = 0
            self.counter_done = 0
            ###
            ADC.__instance = self


    @staticmethod
    def get_instance():

        if ADC.__instance is None:
            ADC(None)
        return ADC.__instance

    def start(self):

        self.info_logger.write_info('ADC: START ADC PROCESS')
        while not self.master.status_vector['DEP_SUCS'] and not self.master.status_vector['KILL']:

            self.info_logger.write_info('ADC: WAIT FOR DEP')
            sleep(self.counterdown.adc_time_checks_deploy)

        while not self.master.status_vector['KILL']:
            self.run_ADC_auto()
            self.run_ADC_manual()

        self.info_logger.write_info('ADC: END OF ADC PROCESS')


    #Auto mode of ADC
    def run_ADC_auto(self):

        self.info_logger.write_info('ADC: AUTO ADC')
        self.master.status_vector['ADC_MAN'] = 0   # 0
        self.master.command_vector['ADC_MAN'] = 0
        while not self.master.get_command('ADC_MAN') and not self.master.status_vector['KILL']:

            self.valid_data = True
            self.get_compass_data()
            self.get_gps_data()

            if self.valid_data:

                self.calc_new_position()
                c_step = self.convert_to_steps(self.difference)
                self.log_last_position_before(c_step)
                self.move_ADC_motor(c_step, self.direction)
                self.antenna_adc.update_position(self.difference, self.direction)
                self.log_last_position_after()
            else:
                self.info_logger.write_warning('ADC: NON ACTION: INVALID DATA')
            sleep(self.counterdown.adc_auto_time_runs) #time to run ADC algorithm


    def run_ADC_manual(self):

        while self.master.get_command('ADC_MAN') and not self.master.status_vector['KILL']:
            self.master.info_logger.write_info('ADC: IN ADC MAN')
            self.master.status_vector['ADC_MAN'] = 1
            self.master.command_vector['ADC_AUTO'] = 0   # re-init
            self.master.command_vector['SET'] = 0  # re-init
            self.master.command_vector['SCAN'] = 0  # re-init
            self.master.command_vector['INIT'] = 0  # re-init
            choice = self.counterdown.countdown3(self.counterdown.adc_man_timeout_to_set_or_scan, 'SET', 'SCAN', 'INIT')
            if choice == 1:
                self.info_logger.write_info('ADC: IN SET')
                sleep(self.counterdown.adc_wait_auto_ends)
                try:
                    steps = int(self.master.command_vector['SET']['steps'])
                    self.go_to_zero()
                    sleep(1)
                    self.set_position(steps)
                except:
                    self.info_logger.write_warning('ADC: INVALID STEP INPUT')
            elif choice == 2:
                self.info_logger.write_info('ADC: IN SCAN')
                self.go_to_zero()
                sleep(1)
                self.scan()
            elif choice == 3:
                self.info_logger.write_info('ADC: IN INIT')
                self.init_position()
            self.master.command_vector['SET'] = 0  # re-init
            self.master.command_vector['SCAN'] = 0  # re-init
            self.master.command_vector['INIT'] = 0  # re-init
            self.master.command_vector['ADC_AUTO'] = 0  # re-init
            self.master.command_vector['ADC_MAN'] = 0  # re-init
            self.info_logger.write_info('ADC: WAITING FOR ADC MAN OR AUTO')
            choice = self.counterdown.countdown2(self.counterdown.adc_man_time_breaks, 'ADC_AUTO', 'ADC_MAN')
            if choice == 2:
                self.info_logger.write_info('ADC: CONT ADC MAN')
            else:
                self.master.command_vector['ADC_MAN'] = 0 # re-init
                self.master.status_vector['ADC_MAN'] = 0 # re-init
                self.info_logger.write_info('ADC: BREAK ADC MAN')
        sleep(self.counterdown.adc_man_time_runs)

    def get_compass_data(self):

        if self.master.status_vector['COMPASS'] == 0:
            self.info_logger.write_warning('ADC: Invalid compass data')
            self.valid_data = False
        else:
            self.compass = float(self.data_manager.get_data("angle_c"))

    def get_gps_data(self):

        if self.master.status_vector["GPS"] == 0:
            self.info_logger.write_warning('ADC: Invalid gps data')
            self.valid_data = False
        else:
            x = self.data_manager.get_data("gps_x") * 10000
            y = self.data_manager.get_data("gps_y") * 10000
            self.gps = [x, y]

    def log_last_position_before(self, c_step):
        self.info_logger.write_info('ADC: STEPS\t {} TO DO'.format(c_step))
        self.info_logger.write_info('ADC: DEGREES {} TO DO'.format(self.difference))
        self.info_logger.write_info('ADC: ACT FROM: {} WITH {}'.format(self.antenna_adc.counter_for_overlap, self.direction))

    def log_last_position_after(self):
        self.info_logger.write_info('ADC: DONE: {}'.format(self.antenna_adc.counter_for_overlap))
        self.adcs_logger.write_info(' {}, {}, {}, {} '.format(self.antenna_adc.position, self.antenna_adc.counter_for_overlap, self.antenna_adc.theta_antenna_pointing, self.antenna_adc.theta))
        self.antenna_adc.angle_plot = self.antenna_adc.theta_antenna_pointing

    def push_DMC_motor(self):
        self.motor_dmc.motor_push()
        self.info_logger.write_info('ADC: DMC MOTOR PUSH')

    def move_ADC_motor(self,counter_step,direction):
        self.motor_adc.act(counter_step, direction)
        self.info_logger.write_info('ADC: ADC MOTOR ROTATED')

    def pull_DMC_motor(self):
        self.motor_dmc.motor_pull()
        self.info_logger.write_info('ADC: DMC MOTOR PULL')

    def convert_to_steps(self, dif):
        if self.motor_adc.step_size != 0:
            c_step = int(dif * self.motor_adc.step_size)
            return c_step
        else:
            self.info_logger.write_warning('ADC: TRY division /0: check step size')
            return 0

    def set_position(self, set_step):

        if 0 <= set_step <= (360*self.motor_adc.step_size):
            direction = 1
            self.motor_adc.act(set_step, direction)
            self.antenna_adc.update_position(set_step/self.motor_adc.step_size, direction)
            self.info_logger.write_info('ADC: SET: ANTENNA AT {}'.format(self.antenna_adc.position))
            self.adcs_logger.write_info(' {}, {}, {}, {} '.format(self.antenna_adc.position, self.antenna_adc.counter_for_overlap, self.antenna_adc.position + self.compass, self.antenna_adc.theta))
            self.antenna_adc.angle_plot = self.antenna_adc.position + self.compass

        else:
            self.info_logger.write_warning('ADC: Invalid SET_STEP')

    def scan(self):
        direction = 1
        steps_per_time = 70 # 70steps - 20 degress
        times_per_scan = 18
        for x in range(0,times_per_scan):
            self.motor_adc.act(steps_per_time, direction)
            self.antenna_adc.update_position(20, direction)
            self.info_logger.write_info('ADC: SCAN: ANTENNA AT {}'.format(self.antenna_adc.position))
            self.log_last_position_after()
        direction = 0
        for x in range(0,times_per_scan):
            self.motor_adc.act(steps_per_time, direction)
            self.antenna_adc.update_position(20, direction)
            self.info_logger.write_info('ADC: SCAN: ANTENNA AT {}'.format(self.antenna_adc.position))
            self.log_last_position_after()

    def go_to_zero(self):
        if self.antenna_adc.counter_for_overlap > 0:
            direction = 0
        else:
            direction = 1
        c_steps = self.convert_to_steps(self.antenna_adc.counter_for_overlap)
        self.motor_adc.act(c_steps, direction)
        self.antenna_adc.position = 0
        self.antenna_adc.counter_for_overlap = 0
        self.adcs_logger.write_info(
            ' {}, {}, {}, {} '.format(self.antenna_adc.position, self.antenna_adc.counter_for_overlap,
                                      self.antenna_adc.theta_antenna_pointing, self.antenna_adc.theta))
        self.antenna_adc.angle_plot = self.antenna_adc.theta_antenna_pointing

    def calc_new_position(self):
    #calc GEOMETRY
        thresshold = 0.001
        dx = abs(self.GS[0] - self.gps[0])
        dy = abs(self.gps[1] - self.GS[1])
        if dx < thresshold:
            # in same yy' axis
            if self.GS[1] < self.gps[1]:
                theta = 180
            else:
                theta = 0
        else:
            if dy == 0:
                dy = thresshold
            fi = math.atan(dx/dy) * 180 / math.pi
            if self.GS[0] < self.gps[0] and self.GS[1] < self.gps[1]:
                theta = 180 + fi #quartile = 1
            elif self.GS[0] < self.gps[0] and self.GS[1] > self.gps[1]:
                #OLD theta = 180 - fi #quartile = 2
                theta = 360 - fi #quartile = 2
            elif self.GS[0] > self.gps[0] and self.GS[1] > self.gps[1]:
                theta = fi #quartile = 3
            else:
               #OLD theta = 360 - fi # quartile = 4
               theta = 180 - fi # quartile = 4
     # end calc GEOMETRY
        self.antenna_adc.theta = theta
        self.antenna_adc.theta_antenna_pointing = (self.antenna_adc.position + self.compass) % 360
        self.adcs_logger.write_info(' {}, {}, {}, {} '.format(self.antenna_adc.position, self.antenna_adc.counter_for_overlap, self.antenna_adc.theta_antenna_pointing, self.antenna_adc.theta))
        self.antenna_adc.angle_plot = self.antenna_adc.theta_antenna_pointing
    if self.antenna_adc.theta_antenna_pointing < self.antenna_adc.theta:
            dif1 = self.antenna_adc.theta - self.antenna_adc.theta_antenna_pointing
            dif2 = 360 - dif1
            if dif1 <= dif2:
                if self.antenna_adc.check_isinoverlap(dif1, +1):  # clockwise
                    self.difference = dif2
                    self.direction = 0  # ani-clockwise
                else:
                    self.difference = dif1
                    self.direction = 1  # clockwise
            else:
                if self.antenna_adc.check_isinoverlap(dif2, -1):  # anti-clockwise
                    self.difference = dif1
                    self.direction = 1  # clockwise
                else:
                    self.difference = dif2
                    self.direction = 0  # anti-clockwise
        else:
            dif2 = self.antenna_adc.theta_antenna_pointing - self.antenna_adc.theta
            dif1 = 360 - dif2
            if dif1 <= dif2:
                if self.antenna_adc.check_isinoverlap(dif1, +1):  # clockwise
                    self.difference = dif2
                    self.direction = 0  # ani-clockwise
                else:
                    self.difference = dif1
                    self.direction = 1  # clockwise
            else:
                if self.antenna_adc.check_isinoverlap(dif2, -1):  # anti-clockwise
                    self.difference = dif1
                    self.direction = 1  # clockwise
                else:
                    self.difference = dif2
                    self.direction = 0  # anti-clockwise

        self.info_logger.write_info('ADC: Difference {} Direction {}'.format( self.difference, self.direction))


    def get_color_data(self):

        if self.master.status_vector["INFRARED"] == 0 :
            self.info_logger.write_warning('ADC: Invalid color data')
        else:
            self.color_string = self.data_manager.get_data("color")

    #@TODO mod it to work
    def init_position(self):

        #clean overlaps
        if self.antenna_adc.counter_for_overlap > 360:
            self.motor_adc.act(315, 0)  # anti-clockwise
            self.antenna_adc.update_position(315 / self.motor_adc.step_size, 0)  # anti-clockwise
        elif self.antenna_adc.counter_for_overlap < -360:
            self.motor_adc.act(315, 1)  # clockwise
            self.antenna_adc.update_position(315 / self.motor_adc.step_size, 1)  # clockwise

        # find direction
        if self.antenna_adc.counter_for_overlap < 0:
            self.dir_init = 1
        else:
            self.dir_init = 0

        self.stop_turn = False
        self.counter_done = 0
        to_act_one = False

        #thread_act = Thread(target=self.threaded_function_act)
        #thread_act.start()


        while not self.stop_turn and not self.master.status_vector['KILL'] and self.master.status_vector['INFRARED']:

            self.get_color_data()
            if (self.color_string == "WHITE"):
                self.info_logger.write_info("ADC: WHITE")
                self.info_logger.write_info("ADC: ZERO POSITION IS SET")
                if to_act_one:
                    self.stop_turn = True
                to_act_one = True
            elif (self.color_string == "RED"):
                self.info_logger.write_info("ADC: SAW RED")
                to_act_one = False
            elif (self.color_string == "BLUE"):
                self.info_logger.write_info("ADC: SAW BLUE")
                to_act_one = False
            elif (self.color_string == "BLACK"):
                self.info_logger.write_info("ADC: SAW BLACK")
                to_act_one = False
            if not self.stop_turn and not to_act_one:
                self.counter_done += 1
                self.motor_adc.act_smooth(self.dir_init)
            elif to_act_one:
                sleep(4)
                self.motor_adc.act(1, self.dir_init)
                self.info_logger.write_info("ADC: NEXT STEP OF WHITE")
            if self.counter_done > 190:
                self.info_logger.write_info("ADC: CHANGE DIR_INIT")
                if self.dir_init == 0:
                    self.dir_init = 1
                else:
                    self.dir_init = 0
                self.counter_done = 0
            sleep(2)

        if self.stop_turn:
            self.motor_adc.act(10,self.dir_init)
            self.antenna_adc.position = 0
            self.antenna_adc.counter_for_overlap = 0
        else:
            self.antenna_adc.update_position(self.counter_done*self.motor_adc.smooth_steps / self.motor_adc.step_size,self.dir_init)
        self.get_compass_data()
        self.adcs_logger.write_info(' {}, {}, {}, {} '.format(self.antenna_adc.position, self.antenna_adc.counter_for_overlap, self.antenna_adc.position + self.compass, self.antenna_adc.theta))
        self.antenna_adc.angle_plot = self.antenna_adc.position + self.compass

    #def threaded_function_act(self):

        #while not self.stop_turn:
            #self.counter_done += 1
            #self.motor_adc.act_smooth(self.dir_init)