import time
import serial
import math
import decimal


class DataManager:
    # constructor
    def __init__(self):
        self.gps_port = "/dev/ttyACM3"
        self.ser_gps = serial.Serial(self.gps_port, baudrate=9600, timeout=0.5)
        self.dictionary = dict()

    def start(self):
        while True:
            self.read_gps()
            time.sleep(3)

    def read_gps(self):
        pass

def dmm_to_dd(x):
    s1 = math.floor(x / 100)
    s11 = (x - s1 * 100) / 60
    x = s1 + s11
    print(x)
    return x


if __name__ == '__main__':
    #data_obj = DataManager()
    #D = decimal.Decimal
    #data_obj.start()
    lat = 4037.63876
# dirLat = s[3]
    lon = 02257.63252
    lat = dmm_to_dd(lat)
    lon = dmm_to_dd(lon)