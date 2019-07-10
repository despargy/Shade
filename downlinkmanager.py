#!/usr/bin/python3
import socket
import time
import sys


class DownLinkManager:

    def __init__(self,ground_ip):
        if(ground_ip == 'local'):
            self.host = socket.gethostname()
        else:
            self.host = ground_ip

        self.port = 12346
        self.BUFFER_SIZE = 1024
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    def start(self):
        while(True):
            image = self.get_image()
            #for testing purposes
            if image == "":
                self.send_image('test.jpg')
            else:
                pass #send real image

            #break here to send only one image (testing)
            break

        self.socket.close()

    def get_image(self):
        return ""

    def send_image(self, file_name):
        """
            @file_name : the filename of image to send.
            Function to send image to ground software.
        """
        #first send filename
        self.socket.sendto(file_name.encode('utf-8'), (self.host, self.port))
        print ("Begin sending "+file_name+" ...")

        try:
            with open(file_name, "rb") as imageFile:
                while True:
                    #read image by BUFFER_SIZE
                    data = imageFile.read(self.BUFFER_SIZE)
                    self.socket.sendto(data, (self.host, self.port))
                    time.sleep(0.02) #await 0.2 seconds so ground receive data
                    if not data: break
        except FileNotFoundError:
            print('File not found')



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("""
              [+] Run ground program with one argument.
              [+] The argument indicates the ELinkManager IP
              [+] e.g python ground.py 195.168.0.1

              [+] For Testing purposes use 'local' as argument
              [+] to simulate a connection locally
              [+] e.g python ground.py local
              """)

    else:
        ground_ip = sys.argv[1]
        DownLinkManager(ground_ip).start()
