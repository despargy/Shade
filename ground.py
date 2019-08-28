#!/usr/bin/python3
import socket , requests
import json
import threading
import sys , time
from logger import InfoLogger


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


        self.info_logger = InfoLogger('groud.info.log')
        # bind ground to down_link_port , to receive images
        self.stop_log_threads = False
        self.start_log_threads()
        threading.Thread(target=self.open_image_connection, args=(self.images_port, )).start()


    def start_log_threads(self):
        self.data_log_thread  = threading.Thread(target=self.open_connection, args=(self.logs_port, ))
        self.data_log_thread.start()
        self.info_log_thread = threading.Thread(target=self.open_connection, args=(self.data_port, ))
        self.info_log_thread.start()
        
    def print_lost_connection(self):
        print("""
                  [+] Lost Internet Connection
                  [+] Trying to reconnect...
             """)


    def open_connection(self,port):

        while True:

            #force thread to stop
            if self.stop_log_threads : break

            host = ''
            log_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            log_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            log_socket.bind((host, port))
            log_socket.listen(5)

            while(not self.has_internet_connection()): time.sleep(3)
            try:
                log_socket,addr = log_socket.accept()
            except (OSError) as e:
                self.print_lost_connection()
                continue

            self.info_logger.write_info('Got a connection from {addr}'.format(addr=addr))

            while(True):

                try:
                    data = log_socket.recv(self.BUFFER_SIZE).decode('utf-8')
                except (ConnectionAbortedError, ConnectionResetError) as e:
                    self.print_lost_connection()
                    log_socket.close()
                    break

                if not data:
                    self.info_logger.write_error('Lost connection unexpectedly from {addr}'.format(addr=addr))
                    break

                file_name = data
                try:
                    data = log_socket.recv(self.BUFFER_SIZE).decode('utf-8')
                except (ConnectionAbortedError, ConnectionResetError) as e:
                    self.print_lost_connection()
                    log_socket.close()
                    break

                try:
                    total_rows = int(data)
                except:
                    self.info_logger.write_error('Exception on type casting for total rows. Data : {data}'.format(data=data))

                    continue

                time.sleep(0.2)

                for i in range(total_rows):
                    with open('elink.'+file_name , 'a') as f:
                        try:
                            data = log_socket.recv(self.BUFFER_SIZE).decode('utf-8')
                            log_socket.sendall("Received".encode('utf-8'))
                        except (ConnectionAbortedError, ConnectionResetError) as e:
                            self.info_logger.write_error('Lost connection when reading log :  {log}'.format(log=data))
                            self.print_lost_connection()
                            break

                        f.write(data)
                    #f.close()
                    time.sleep(0.2)
        log_socket.close()


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
            #wait for connection from downlinkmanager
            data, addr = image_downlink_socket.recvfrom(self.BUFFER_SIZE)
            if data:
                file_name = data.strip().decode('utf-8')
            else:
                #self.info_logger.write_error('Received bad package from elink. Ignoring.. ')
                continue
            #TODO : check if dir exists. if not create it
            fh = open('images/elink.'+ file_name, "ab")
            #read buffer by BUFFER_SIZE chunks
            while True:
                data, addr = image_downlink_socket.recvfrom(self.BUFFER_SIZE)
                fh.write(data)
                if not data: break

            fh.close()

        image_downlink_socket.close()



    def onClose(self):
        """Function to handle properly the shutdown of the Ground Software"""
        pass


    def has_internet_connection(self):
        """
            Function to check internet connection.
        """
        try:
            _ = requests.get('http://www.google.com/', timeout=5)
            return True
        except:
            self.info_logger.write_warning('Lost internet connection.')
            self.print_lost_connection()
        return False

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
                print("""
                        [+] Server is Unavailabe
                        [+] or there is no internet connection.
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
            if action == "EXIT":
                conn_socket.close()
                sys.exit(0)
            elif action =="":
                continue
            elif action == "RESTART_GROUND_LOGS":
                self.stop_log_threads = True
                if self.data_log_thread.isAlive():
                    self.data_log_thread.join()
                if self.info_log_thread.isAlive():
                    self.info_log_thread.join()
                self.stop_log_threads = False
                self.start_log_threads()
                continue


            #save data into dictionary
            package = {"action": action }

            if action == "SET":
                package['steps'] = input('Steps: ')


            while(not self.has_internet_connection()): time.sleep(3)

            #send data as json string
            try:
                conn_socket.sendall(json.dumps(package).encode('utf-8'))
                #get response and print it
                response = conn_socket.recv(self.BUFFER_SIZE).decode('utf-8')
            except ConnectionAbortedError as e:
                print("""
                    [+] Lost Connection.
                    [+] Unable to send action {action}.
                    [+] Initialize connection.
                    [+] Please wait....
                    """.format(action=action))
                break
            except ConnectionResetError as e:
                print("""
                  [+] Unable to send action {action}.
                  [+] Initialize connection.
                  [+] Please wait....
                    """.format(action=action))
                break
            except TimeoutError as e:
                print("""
                  [+] ElinkManager is unreachable
                  [+] Something went wrong!
                  [+] Try to reconnect...
                    """)
                break
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
        ground = GroundClient(elinkmanager_ip)
        while(True):
            ground.establish_connection()
