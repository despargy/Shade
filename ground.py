#!/usr/bin/python3
import socket
import json
import threading
import sys
import time


class GroundClient:

    def __init__(self, elinkmanager_ip):
        if elinkmanager_ip == 'local':
            self.uplink_host = socket.gethostname()
        else:
            self.uplink_host = elinkmanager_ip

        self.up_link_port = 12345
        self.images_port = 12346
        self.data_port = 12347
        self.logs_port = 12348
        self.BUFFER_SIZE = 1024
        #set timeout 10 seconds
        self.timeout = 10
        # bind ground to down_link_port , to receive images
        threading.Thread(target=self.open_connection, args=(self.logs_port, )).start()
        threading.Thread(target=self.open_connection, args=(self.data_port, )).start()
        threading.Thread(target=self.open_image_connection, args=(self.images_port, )).start()


    def open_connection(self,port):
        host = ''
        elink_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        elink_socket.bind((host, port))

        while True:
            print('Awaiting data')
            data, addr = elink_socket.recvfrom(self.BUFFER_SIZE)

            if data:
                file_name = data.strip().decode('utf-8')
                print ("File name:"+file_name)
            else:
                #received bad package
                continue

            data, addr = elink_socket.recvfrom(self.BUFFER_SIZE)
            total_rows = int(data.decode('utf-8'))

            for i in range(total_rows):
                f = open('test.'+file_name, "a")
                data, addr = elink_socket.recvfrom(self.BUFFER_SIZE)
                f.write(data.decode('utf-8')+'\n')
                f.close()
                time.sleep(0.2)


    #TODO: maybe need better error handling
    def open_image_connection(self,port):
        """
            Function to bind ground software to down_link_port
            and await for downlink manager to send image.
        """
        image_downlink_host = ''
        image_downlink_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        image_downlink_socket.bind((image_downlink_host, port))
        while True:
            print('awaiting image')
            #wait for connection from downlinkmanager
            data, addr = image_downlink_socket.recvfrom(self.BUFFER_SIZE)
            if data:
                file_name = data.strip().decode('utf-8')
                print ("File name:"+file_name)
            else:
                #received bad package
                continue
            #TODO : check if dir exists. if not create it
            fh = open('images/test.'+ file_name, "ab")
            #read buffer by BUFFER_SIZE chunks
            while True:
                data, addr = image_downlink_socket.recvfrom(self.BUFFER_SIZE)
                fh.write(data)
                if not data: break

            fh.close()

        image_downlink_socket.close()



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
        elinkmanager_ip = sys.argv[1]
        GroundClient(elinkmanager_ip).establish_connection()
