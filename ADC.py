import time
import math
import Antenna as antenna
from threading import Timer
import signal

#class to represent subsystem's proccess of ADC
class ADC():
    #constructor
    def __init__(self):
        """ inauto_adc: bool to define mode
            inman_auto: bool to define mode
            inscan: bool to define mode
            inset: bool to define mode
            GS: x- axis y-axis of SHADE Ground Station - static
            gps: x- axis y-axis of Gondola's  current x,y-axis
            compass: data received from compass, degrees btwn North and Gondola 0,0
            antenna_adc: object of antenna instance
            direction: clockwise (1) or anti-clockwise(0) for antenna base rotation
            difference: degrees which are needed for antenna base rotation

        """
        self.inauto_adc = False
        self.inman_adc = False
        self.inscan = False
        self.inset = False
        self.GS = [1, 1]
        self.compass = 0
        self.gps = self.GS
        self.antenna_adc = antenna.Antenna("antenna-ADC", 1.8)
        self.direction = 1
        self.difference = 0
        self.received = False
        self.new_angle = 0

    #ADC before deployment
    def run_init(self):
        print("ADC run init")
        inp = input("Press any key to move in auto-ADC\n")

    #Auto mode of ADC
    def run_auto(self, x_axis, y_axis, compass_data_):
        print("ADC run auto\n")
        self.compass = compass_data_  # Data.compass()
        self.gps = [x_axis, y_axis]  # Data.gps()
        #find quartile GS n' gps
        quartile = self.find_quartile()
        print("quartile= ", quartile, "\n")
        #find the angle goal based on global degrees
        theta_global_bear = self.find_bear(quartile)
        print("bearing tha gondola sees GS= ", theta_global_bear, "\n")
        #find where the antenna is pointing right now based on motor diver set and the rotation of gondola
        theta_current_antenna_pointing = (self.antenna_adc.set_by_motor_in + self.compass) % 360
        print("cur ant point = ", theta_current_antenna_pointing)
        self.rotation_with_cases(theta_current_antenna_pointing, theta_global_bear)
        print("base will be rotated = ", self.difference,"\n with direction = ", self.direction)
        #motor action(self.difference, self.direction)
        self.antenna_adc.update_set_by_motor(self.new_angle)
        self.antenna_adc.update_counter_for_overlap()
        print("antenna is = ", self.antenna_adc.set_by_motor_in)

    def find_quartile(self):
        same_ax = 0
        thresshold = 0.1
        if self.GS[0] < self.gps[0] and self.GS[1] < self.gps[1]:
            quartile = 1
        elif self.GS[0] < self.gps[0] and self.GS[1] > self.gps[1]:
            quartile = 2
        elif self.GS[0] > self.gps[0] and self.GS[1] > self.gps[1]:
            quartile = 3
        elif self.GS[0] > self.gps[0] and self.GS[1] < self.gps[1]:
            quartile = 4
        else:
            print("almost in same axis")
            if abs(self.GS[0] - self.gps[0]) < thresshold :
                #in same y' axis
                if abs(self.GS[1] - self.gps[1]) < thresshold :
                    print("almost the same point")
                    quartile = 5
                elif self.GS[1] < self.gps[1]:
                    quartile = 6
                else:
                    quartile = 7
            else:
                #in same y' axis
                if abs(self.GS[0] - self.gps[0]) < thresshold :
                    print("almost the same point")
                    quartile = 5
                elif self.GS[0] < self.gps[0]:
                    quartile = 8
                else:
                    quartile = 9
        return quartile

    def find_bear(self, quartile_):
        quartile = quartile_
        if quartile == 1:
            theta_global_bear = self.case_quartile_1()
        elif quartile == 2:
            theta_global_bear = self.case_quartile_2()
        elif quartile == 3:
            theta_global_bear = self.case_quartile_3()
        elif quartile == 4:
            theta_global_bear = self.case_quartile_4()
        elif quartile == 5:
            theta_global_bear = 0
        elif quartile == 6:
            theta_global_bear = 180
        elif quartile == 7:
            theta_global_bear = 0
        elif quartile == 8:
            theta_global_bear = 270
        elif quartile == 9:
            theta_global_bear = 90
        return theta_global_bear

    def case_quartile_1(self):
        #find the angle that GS sees the gondola
        theta_global = math.atan((self.gps[0] - self.GS[0]) / (self.gps[1] - self.GS[1]))*180/math.pi
        print("theta global = ",theta_global,"\n")
        #angle that gondola sees GS
        theta_global_bear = theta_global + 180
        #180
        return theta_global_bear

    def case_quartile_2(self):
        # find the angle that GS sees the gondola
        theta_global = math.atan(( self.gps[0] - self.GS[0]) / (self.GS[1] - self.gps[1])) * 180 / math.pi
        print("theta global = ", theta_global, "\n")
        #angle that gondola sees GS
        theta_global_bear = 360 - theta_global
        return theta_global_bear

    def case_quartile_3(self):
        # find the angle that GS sees the gondola
        theta_global = math.atan(( self.GS[0] - self.gps[0] ) / (self.GS[1] - self.gps[1])) * 180 / math.pi
        print("theta global = ", theta_global, "\n")
        #angle that gondola sees GS
        theta_global_bear = theta_global
        return theta_global_bear

    def case_quartile_4(self):
        # find the angle that GS sees the gondola
        theta_global = math.atan((self.GS[0] - self.gps[0]) / (self.gps[1] - self.GS[1])) * 180 / math.pi
        print("theta global = ", theta_global, "\n")
        # find the supplementary of that angle
        # angle that gondola sees GS
        theta_global_bear = 180 - theta_global
        return theta_global_bear

    def rotation_with_cases(self, theta_current_antenna_pointing, theta_global_bear):
        #case a of clockwise rotation
        if theta_current_antenna_pointing < theta_global_bear:
            dif1 = theta_global_bear - theta_current_antenna_pointing
            dif2 = 360 - dif1
            if dif1 <= dif2:
                if self.antenna_adc.check_isinoverlap(dif1, +1):  # clockwise
                    self.difference = dif2
                    self.direction = 0 #ani-clockwise
                    new_angle = self.antenna_adc.set_by_motor_in + 360 - self.difference
                    if self.new_angle < 0:
                        self.new_angle = 360 - abs(self.new_angle)
                    else:
                        self.new_angle = new_angle % 360
                    self.antenna_adc.sign_for_counter_overlap = -1
                    self.antenna_adc.next_plus_angle = self.difference
                else:
                    self.difference = dif1
                    self.direction = 1 #clockwise
                    new_angle = self.antenna_adc.set_by_motor_in + self.difference
                    if self.new_angle < 0:
                        self.new_angle = 360 - abs(self.new_angle)
                    else:
                        self.new_angle = new_angle % 360
                    self.antenna_adc.sign_for_counter_overlap = +1
                    self.antenna_adc.next_plus_angle = self.difference
            else:
                if self.antenna_adc.check_isinoverlap(dif2, -1):  # anti-clockwise
                    self.difference = dif1
                    self.direction = 1 #clockwise
                    new_angle = self.antenna_adc.set_by_motor_in +self.difference
                    if self.new_angle < 0:
                        self.new_angle = 360 - abs(self.new_angle)
                    else:
                        self.new_angle = new_angle % 360
                    self.antenna_adc.sign_for_counter_overlap = +1
                    self.antenna_adc.next_plus_angle = self.difference
                else:
                    self.difference = dif2
                    self.direction = 0 #anti-clockwise
                    new_angle = self.antenna_adc.set_by_motor_in + 360 - self.difference
                    if self.new_angle < 0:
                        self.new_angle = 360 - abs(self.new_angle)
                    else:
                        self.new_angle = new_angle % 360
                    self.antenna_adc.sign_for_counter_overlap = -1
                    self.antenna_adc.next_plus_angle = self.difference
        else:
            dif2 = theta_current_antenna_pointing - theta_global_bear
            dif1 = 360 - dif2
            if dif1 <= dif2:
                if self.antenna_adc.check_isinoverlap(dif1, +1):  # clockwise
                    self.difference = dif2
                    self.direction = 0 #ani-clockwise
                    new_angle = self.antenna_adc.set_by_motor_in - self.difference
                    if self.new_angle < 0:
                        self.new_angle = 360 - abs(self.new_angle)
                    else:
                        self.new_angle = new_angle % 360
                    self.antenna_adc.sign_for_counter_overlap =  -1
                    self.antenna_adc.next_plus_angle = self.difference
                else:
                    self.difference = dif1
                    self.direction = 1 #clockwise
                    new_angle = self.antenna_adc.set_by_motor_in + self.difference
                    if self.new_angle < 0:
                        self.new_angle = 360 - abs(self.new_angle)
                    else:
                        self.new_angle = new_angle % 360
                    self.antenna_adc.sign_for_counter_overlap = +1
                    self.antenna_adc.next_plus_angle = self.difference
            else:
                if self.antenna_adc.check_isinoverlap(dif2, -1):  # anti-clockwise
                    self.difference = dif1
                    self.direction = 1 #clockwise
                    new_angle = self.antenna_adc.set_by_motor_in +self.difference
                    if self.new_angle < 0:
                        self.new_angle = 360 - abs(self.new_angle)
                    else:
                        self.new_angle = new_angle % 360
                    self.antenna_adc.sign_for_counter_overlap = +1
                    self.antenna_adc.next_plus_angle = self.difference
                else:
                    self.difference = dif2
                    self.direction = 0 #anti-clockwise
                    new_angle = self.antenna_adc.set_by_motor_in + 360 - self.difference
                    if self.new_angle < 0:
                        self.new_angle = 360 - abs(self.new_angle)
                    else:
                        self.new_angle = new_angle % 360
                    self.antenna_adc.sign_for_counter_overlap = -1
                    self.antenna_adc.next_plus_angle = self.difference

    #Manual mode of ADC
    def manual_adc(self):
        print("ADC in Manual Mode")
        self.inman_adc = True
        #timeout = 1*10
        #def timeout_error(* _):
            #raise TimeoutError
        #signal.signal(signal.SIGALRM, timeout_error())
        #signal.alarm(timeout)
        #t = Timer(timeout, print, ['in timer: 1 minute'])
        #try:
        ch = input("Choose: Scan or Set Mode \n $$ scan \t$$ set\n")
        #except TimeoutError:
            #print("Times up")
            #ch = "TimerOut"
        if ch == "scan":
            print("input scan")
            self.scan()
        elif ch == "set":
            print("input set")
            an = input("Enter desired angle in degrees: \n angle 0-360\n")
            an = float(an)
            if an < 360 and an > 0:
                self.set(an)
            else:
                print("Wrong angle input")
        else:
            print("Wrong input")
        #self.inman_adc = False
    #Scan mode of Manual ADC
    def scan(self):
        print("Manual in Scan Mode")
        self.inscan = True
        #from current point of motor driver go to 0 degrees
        self.difference = abs(self.antenna_adc.counter_for_overlap)
        if self.antenna_adc.counter_for_overlap < 0:
            self.direction = 1
        else:
            self.direction = 0
        #motor act(self.difference, self.direction)
        self.antenna_adc.update_set_by_motor(0)
        #turn 360 degrees
        self.difference = 360
        self.direction = 1 #clockwise
        #motor act(self.difference, self.direction)
        self.antenna_adc.update_set_by_motor(360)
        #return to 0 degrees
        self.difference = 360
        self.direction = 0 #anti-clockwise
        #motor act(self.difference, self.direction)
        self.antenna_adc.update_set_by_motor(0)
        self.inscan = False

    #Set mode of Manual ADC
    def set(self, ang):
        print("Manual in Set Mode")
        self.inset = True
        theta_current_antenna_pointing = self.antenna_adc.set_by_motor_in
        theta_global_bear = ang
        self.cases_for_rotation(theta_current_antenna_pointing, theta_global_bear)
        print("Antenna is set to", self.antenna_adc.set_by_motor_in)
        self.inset = False

    #function to close the ADC process
    def onClose(self):
        print("Close ADC")


if __name__ == '__main__':
    adc = ADC()
    adc.run_init()
    while True:
        print("Enter 'manual' to change in Manual ADC mode\n Or x , y, comp for Auto ADC")
        inp = input("Wait for manual or x of gondola: \n")
        if inp == "manual":
            adc.manual_adc()
        else:
            x = float(inp)
            y = float(input("wait for y of gondola\n"))
            c = float(input("wait for compass degrees\n"))
            adc.run_auto(x, y, c)
    adc.onClose()
    print("DONE")


main()
