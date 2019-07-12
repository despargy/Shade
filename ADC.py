import time
import math
import Antenna as antenna
from threading import Timer
import signal

class ADC(object):
    def __init__(self):
        self.bscan = False
        self.bset = False
        self.man_adc = False
        self.auto_adc = True
        self.angle_to_set = 0
        self.GS = [1, 1]
        self.antenna_adc = antenna.Antenna("antenna-ADC", 1.8)
        self.rot = 1
        self.dif = 0
        self.received = False

    def run_init(self):
        print("ADC run init")
        inp = input("Press any key and >Enter to move in auto-ADC")

    def run_auto(self, x, y, c):
        #!! need to add cases !!
        print("ADC run auto")
        comp = c  # Data.compass()
        gps = [x, y]  # Data.gps()
        at = math.atan((gps[1] - self.GS[1]) / (gps[0] - self.GS[0]))
        theta_global = at*180/math.pi
        print(theta_global)
        theta_global_sup = 90 - theta_global
        theta_cur_point = self.antenna_adc.set_by_motor_in + comp
        angle_goal = 180 - theta_cur_point + theta_global_sup
        print(angle_goal)
        if angle_goal > theta_cur_point :
            sing = 1
        else:
            sing = -1
        dif1 = sing*(angle_goal - theta_cur_point)
        dif2 = 360 - dif1
        if dif1 < dif2:
            self.dif = dif1
            self.rot = 1 #clockwise
            if sing == -1:
                self.rot = 0
        else:
            self.dif = dif2
            self.rot = 0 #anti-clockwise
            if sing == -1:
                self.rot = 1
        print("dif = ", self.dif,"\nrotation = ", self.rot)
        #motor action(self.dif, self.rot)
        if self.rot == 1:
            update_a = self.dif + self.antenna_adc.set_by_motor_in
        else:
            update_a = self.antenna_adc.set_by_motor_in - self.dif
        self.antenna_adc.update_set_by_motor(update_a)
        print("updated = ",self.antenna_adc.set_by_motor_in)
    def manual_adc(self):
        print("ADC in Manual Mode")
        self.man_adc = True
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
            an = int(an)
            if an < 360 and an > 0:
                self.set(an)
            else:
                print("Wrong angle input")
        else:
            print("Wrong input")
        #self.man_adc = False
    def scan(self):
        print("Manual in Scan Mode")
        self.bscan = True
        #from current point of motor driver go to 0 degrees
        self.dif = self.antenna_adc.set_by_motor_in
        self.rot = 0 #anti-clockwise
        #motor act(self.dif, self.rot)
        self.antenna_adc.update_set_by_motor(0)
        #turn 360 degrees
        self.dif = 360
        self.rot = 1 #clockwise
        #motor act(self.dif, self.rot)
        self.antenna_adc.update_set_by_motor(360)
        #return to 0 degrees
        self.dif = 360
        self.rot = 0 #anti-clockwise
        #motor act(self.dif, self.rot)
        self.bscan = False
    def set(self, ang):
        print("Manual in Set Mode")
        self.bset = True
        if ang > self.antenna_adc.set_by_motor_in:
            self.dif = ang - self.antenna_adc.set_by_motor_in
            self.rot = 0
        else:
            self.dif = self.antenna_adc.set_by_motor_in - ang
            self.rot = 1
        #motor act(self.dif, self.rot)
        print("dif = ", self.dif, "\nrotation = ", self.rot)
        print("Antenna is set to", ang)
        self.bset = False
    def close(self):
        print("Close ADC")


def main():
    adc = ADC()
    adc.run_init()
    while True:
        print("Enter 'manual' to change in Manual ADC mode\n Or x , y, comp for Auto ADC")
        inp = input("Wait for manual or x of gondola: \n")
        if inp == "manual":
            adc.manual_adc()
        else:
            x = int(inp)
            y = int(input("wait for y of gondola"))
            c = int(input("wait for compass degrees"))
            adc.run_auto(x, y, c)
    adc.close()
    print("DONE")


main()
