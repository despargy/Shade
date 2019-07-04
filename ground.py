#!/usr/bin/python3
import socket
import json
import random
import threading
import sys

class GroundClient:

    def __init__(self):
        self.host = socket.gethostname()
        self.port = 9999
        self.BUFFER_SIZE = 1024

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
