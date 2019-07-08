#!/usr/bin/python3
import socket
import time
import sys


class DownLinkManager:

    def __init__(self):
        self.host = '192.168.0.103' #host name changes when change network
        self.port = 12346
        self.BUFFER_SIZE = 1024
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    def send_photo(self, file_name):
        """
            @file_name : the filename of image to send.
            Function to send photo to ground software.
        """
        #first send filename
        self.socket.sendto(file_name.encode('utf-8'), (self.host, self.port))
        print ("Sending "+file_name+" ...")

        with open(file_name, "rb") as imageFile:
            while True:
                #read image by BUFFER_SIZE
                data = imageFile.read(self.BUFFER_SIZE)
                self.socket.sendto(data, (self.host, self.port))
                time.sleep(0.02) #await 0.2 seconds so ground receive data
                if not data: break

        self.socket.close()

if __name__ == "__main__":
    DownLinkManager().send_photo('test.png')
