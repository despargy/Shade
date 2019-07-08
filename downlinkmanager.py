#!/usr/bin/python3
import socket
import time
import sys


class DownLinkManager:

    def __init__(self):
        self.host = '192.168.0.103'
        self.port = 12346
        self.BUFFER_SIZE = 1024
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    def send_photo(self, file_name):
        #send first filename so client can open file via filename
        self.socket.sendto(file_name.encode('utf-8'), (self.host, self.port))
        print ("Sending "+file_name+" ...")
        with open(file_name, "rb") as imageFile:
            while True:
                data = imageFile.read(self.BUFFER_SIZE)
                self.socket.sendto(data, (self.host, self.port))
                time.sleep(0.02)
                if not data: break

        self.socket.close()

if __name__ == "__main__":
    DownLinkManager().send_photo('test.png')
