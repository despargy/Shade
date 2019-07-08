#!/usr/bin/python3
import socket
import json
import threading
import sys
import time


class GroundClient:

    def __init__(self):
        self.uplink_host = '192.168.0.104'
        self.up_link_port = 12345
        self.down_link_port = 12346
        self.BUFFER_SIZE = 1024
        #set timeout 10 seconds
        self.timeout = 10
        # bind ground to down_link_port , to receive images
        threading.Thread(target=self.open_downlink_connetion).start()



    #TODO: maybe need better error handling
    def open_downlink_connetion(self):
        """
            Function to bind ground software to down_link_port
            and await for downlink manager to send image.
        """
        downlink_host = ''
        down_link_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        down_link_socket.bind((downlink_host, self.down_link_port))
        while True:
            #wait for connection from downlinkmanager
            data, addr = down_link_socket.recvfrom(self.BUFFER_SIZE)
            if data:
                file_name = data.strip().decode('utf-8')
                print ("File name:"+file_name)
            else:
                #received bad package
                continue
            #TODO : check if dir exists. if not create it
            fh = open('images/'+ file_name, "wb")
            #read buffer by BUFFER_SIZE chunks
            while True:
                data, addr = down_link_socket.recvfrom(self.BUFFER_SIZE)
                fh.write(data)
                if not data: break

            fh.close()

        down_link_socket.close()



    def onClose():
        """Function to handle properly the shutdown of the Ground Software"""
        pass



    def establish_connection(self):
        """Main Function to send manual commands to elinkmanager"""
        conn_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        #connect to server
        while(True):
            try:
                conn_socket.connect((self.uplink_host, self.up_link_port))
                print("""
                        [+] Success!
                        [+] Establish Connection
                        """)
                break
            except socket.error as e:
                print(e)
                print("""
                        [+] Server is Unavailabe
                        [+] Try again to connect.
                        [+] Reconecting ...
                        """)
                time.sleep(2) #wait 2 seconds and retry
                continue

        #receive prompt
        prompt = conn_socket.recv(self.BUFFER_SIZE).decode('utf-8')
        print(prompt)

        while(True):
            action = input("Action: ")
            if action == "EXIT" or action =="":
                conn_socket.close()
                break

            #save data into dictionary
            subsystem = input("Subsystem: ")
            package = {"action": action , "subsystem":subsystem }

            #send data as json string
            conn_socket.sendall(json.dumps(package).encode('utf-8'))

            #get response and print it
            response = conn_socket.recv(self.BUFFER_SIZE).decode('utf-8')
            print(f"{str(response)}")



def main():
    GroundClient().establish_connection()

if __name__ == "__main__":
    main()
