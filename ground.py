#!/usr/bin/python3
import socket
import json
import threading
import sys
import time


class GroundClient:

    def __init__(self):
        self.host = socket.gethostname()
        self.port = 9999
        self.down_link_port = 8888
        self.BUFFER_SIZE = 1024
        self.timeout = 10
        threading.Thread(target=self.open_downlink_connetion).start()


    def open_downlink_connetion(self):
        down_link_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        down_link_socket.bind((self.host, self.down_link_port))
        while True:
            data, addr = down_link_socket.recvfrom(1024)
            if data:
                print ("File name:"+data.decode('utf-8'))
                file_name = data.strip()

            fh = open(file_name, "wb")
            while True:
                data, addr = down_link_socket.recvfrom(1024)
                fh.write(data)
                if not data: break

            fh.close()

        down_link_socket.close()


    def establish_connection(self):
        """Function to force connectio between client and server"""
        conn_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #connect to server
        try:
            conn_socket.connect((self.host, self.port))
        except socket.error as e:
            sys.exit("""
                    [+] Server is Unavailabe
                    [+] Exiting ...
                    """)

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
