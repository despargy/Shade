#!/usr/bin/python3
import socket, subprocess, platform
import threading
import json
import time

class ELinkManager:

    def __init__(self, master, ground_ip):
        self.master = master

        self.host = ''
        if ground_ip == 'local':
            self.ground_host = socket.gethostname()
        else:
            self.ground_host = ground_ip

        self.recv_port = 12345
        self.data_port = 12347
        self.logs_port = 12348
        self.BUFFER_SIZE = 1024
        self.recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.recv_socket.bind((self.host, self.recv_port))
        self.recv_socket.listen(5)

        threading.Thread(target=self.send_logs, args=('data.log',self.data_port,)).start()
        threading.Thread(target=self.send_logs, args=('info.log',self.logs_port,)).start()


    def ping_host(self,host):
        """
            Function that ecexutes ping (linux command) to check if
            ground IP exists into network.
            @carefull : this function dont cover the case where ground is on network
                        but is not available (bind to port etc)
        """
        try:
            output = subprocess.check_output("ping -{} 1 {}".format('n' if platform.system().lower()=="windows" else 'c', host), shell=True)
        except:
            return False

        return True

    def send_logs(self,file_name,port):


        while(True):
            time.sleep(5)
            ground_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                ground_socket.connect((self.ground_host, port))
                self.master.info_logger.write_info('Connect to ground to port {port} to send {filename}'.format(port=port, filename=file_name))
            except (socket.error , socket.timeout)  as e:
                print(e)
                self.master.info_logger.write_info('Socket Error when trying to connect to ground to send {filename}'.format(filename=file_name))
                time.sleep(2) #wait 2 seconds and retry
                continue


            #first send filename
            ground_socket.sendall(file_name.encode('utf-8'))


            if file_name == 'info.log':
                unsend_data, total_rows = self.master.info_logger.get_unsend_data()
            elif file_name == 'data.log':
                unsend_data, total_rows = self.master.data_logger.get_unsend_data()

            ground_socket.sendall(str(total_rows).encode('utf-8'))
            time.sleep(0.2)
            #TODOS: read file as chucks that have size BUFFER_SIZE
            for log in unsend_data:
                try:
                    ground_socket.sendall(log.encode('utf-8'))
                except (ConnectionResetError , ConnectionAbortedError) as e:
                    self.master.info_logger('Lost Connection. Unable to send log {log}'.format(log=log))
                    break
                time.sleep(0.2)

            ground_socket.close()





    def start(self):
        """Initialize ELinkManager. Bind him to await for a connection"""
        while True:
           #start listening
           ground_socket,addr = self.recv_socket.accept()
           self.master.info_logger.write_info('Got a connection from {addr}'.format(addr=addr))
           #Start Thread to serve client
           threading.Thread(target=self.open_connetion,
                            args=(ground_socket,addr, )).start()

    def show_prompt(self):
        """Prompt Message to inform about the
           actions ground software can do"""
        return """
                >> DMC Available Commands:
                    [+] DEP
                    [+] DEP_CONF
                    [+] DEP_AB
                    [+] DEP_SUCS
                    [+] RET
                    [+] RET_CONF
                    [+] RET_AB
                    [+] RET SUCS

                >> ADCS Available Commands
                    [+] SET
                    [+] SCAN
                    [+] ADC_MAN

                >> Heat Available Commands:
                    [+] HEAT_SLEEP

                >> Reboot Available Commands:
                    [+] REBOOT
                    [+] REBOOT_SLAVE
                """


    def open_connetion(self,ground_socket,addr):
        """
            @ground_socket : the connection socket between ground and elinkmanager
            @addr: the ground address
            Function to handle communication with ground software for manual commands
        """
        #send prompt
        try:
            ground_socket.send(self.show_prompt().encode('utf-8'))
            while(True):
                #get package as json string
                ground_package_json = ground_socket.recv(self.BUFFER_SIZE).decode('utf-8')
                if not ground_package_json:
                    self.master.info_logger.write_error('Lost connection unexpectedly from {addr}'.format(addr=addr))
                    break
                #handle the client package
                server_response = self.handle_package(ground_package_json)
                #send repsonse to client
                ground_socket.send(server_response.encode('utf-8'))

            ground_socket.close()
        except ConnectionResetError:
            #remove this , add log
            self.master.info_logger.write_error('Lost connection unexpectedly from {addr}'.format(addr=addr))

    def handle_package(self,ground_package_json):
        """
            @ground_package_json : the package received from ground
            Method to analyse ground's package
            and execute the appropriate actions
        """
        #json to list
        client_data = json.loads(ground_package_json)

        #get data
        action = client_data["action"]
        self.master.info_logger.write_info('Action {action} was received from ground.'.format(action=action))
        if action == 'SET':
            steps = client_data["steps"]
            values = {'status': 1 , 'steps' : steps}
            self.master.command_vector[action] = values
        else:
            self.master.command_vector[action] = 1

        return """
                 [+] Command {action} Successfuly
                 [+] changed command_vector
               """.format(action=action)


if __name__ == "__main__":
    ELinkManager().start()