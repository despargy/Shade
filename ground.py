#!/usr/bin/python3
import socket
import json
import threading
import sys
import time


class GroundClient:

    def __init__(self):
        #self.host = socket.gethostname()
        #self.host = '192.168.43.15'
        self.host = '192.168.0.104'
        self.port = 12345
        self.down_link_port = 12346
        self.BUFFER_SIZE = 1024
        self.timeout = 10
        threading.Thread(target=self.open_downlink_connetion).start()


    def open_downlink_connetion(self):
        host = ''
        down_link_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        down_link_socket.bind((host, self.down_link_port))
        while True:
            data, addr = down_link_socket.recvfrom(1024)
            if data:
                file_name = data.strip().decode('utf-8')
                print ("File name:"+file_name)

            fh = open('images/'+ file_name, "wb")
            while True:
                data, addr = down_link_socket.recvfrom(1024)
                fh.write(data)
                if not data: break

            #print('Received Image '+file_name)
            fh.close()

        down_link_socket.close()


    def onClose():
        pass

    def establish_connection(self):
        """Function to force connectio between client and server"""
        conn_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #connect to server
        while(True):
            try:
                conn_socket.connect((self.host, self.port))
                print("""
                        [+] Success!
                        [+] Establish Connection
                        """)
                break
            except socket.error as e:
                print(e)
                print("""
                        [+] Server is Unavailabe
                        [+] Try again to connect ...
                        """)
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
    print(socket.gethostname())
    GroundClient().establish_connection()

if __name__ == "__main__":
    main()
