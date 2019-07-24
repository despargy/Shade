#!/usr/bin/python3
import socket
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


    def send_logs(self,file_name,port):
        while(True):
            time.sleep(10)
            #first send filename

            ground_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ground_socket.sendto(file_name.encode('utf-8'), (self.ground_host, port))

            #self.master.info_logger.write_info('Start sending {filename}'.format(filename=file_name))

            if file_name == 'info.log':
                unsend_data, total_rows = self.master.info_logger.get_unsend_data()
            elif file_name == 'data.log':
                unsend_data, total_rows = self.master.data_logger.get_unsend_data()

            ground_socket.sendto(str(total_rows).encode('utf-8'), (self.ground_host, port))

            #TODOS: read file as chucks that have size BUFFER_SIZE
            for log in unsend_data:
                #print(len(log.encode('utf-8')))
                ground_socket.sendto(log.encode('utf-8'), (self.ground_host, port))
                time.sleep(0.02)

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
                    [+] dep
                    [+] dep_abort
                    [+] deb_again
                    [+] dep_confirm
                    [+] dep_cutoff
                    [+] dep_abort_cutoff
                    [+] dep_retrieve
                    [+] dep_retrieve_again

                >> ADCS Available Commands
                    [+] adcs_set_auto
                    [+] adcs_set_manual
                    [+] adcs_scan
                    [+] adcs_set_pos

                >> TX Available Commands
                    [+] tx_stop_emmision
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
                    self.master.info_logger.write_error('Lost connection unexpected from {addr}'.format(addr=addr))
                    break
                #handle the client package
                server_response = self.handle_package(ground_package_json)
                #send repsonse to client
                ground_socket.send(server_response.encode('utf-8'))

            ground_socket.close()
        except ConnectionResetError:
            #remove this , add log
            self.master.info_logger.write_error('Lost connection unexpected from {addr}'.format(addr=addr))

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
        subsystem = client_data["subsystem"]

        #check action and make the actions
        if action == "dep":
            return self.dep()
        elif action == "dep_abort":
            return self.dep_abort()
        elif action == "dep_again":
            return self.dep_again()
        elif action == "dep_confirm":
            return self.dep_confirm()
        elif action == "dep_cutoff":
            return self.dep_cutoff()
        elif action == "dep_abort_cutoff":
            return self.dep_abort_cutoff()
        elif action == "dep_retrieve":
            return self.dep_retrieve()
        elif action == "dep_retrieve_again":
            return self.dep_retrieve_again()
        elif action == "adcs_set_auto":
            return self.adcs_set_auto()
        elif action == "adcs_set_manual":
            return self.adcs_set_manual()
        elif action == "adcs_scan":
            return self.adcs_scan()
        elif action == "adcs_set_pos":
            return self.adcs_set_pos()
        elif action == "tx_stop_emmision":
            return self.tx_stop_emmision()
        else:
            #unrecognised or unavailabe action
            return "Unrecognised or Unavailabe action"



    def dep(self):
        self.master.info_logger.write_info('Received manual command: dep ')
        # Call master to make the actions
        return """
                  [+] Deployed Successfuly
                """

    def dep_abort(self):
        self.master.info_logger.write_info('Received manual command: dep_abort ')
        # Call master to make the actions
        return """
                  [+] Deployment Aborted
                """

    def dep_again(self):
        self.master.info_logger.write_info('Received manual command: dep_again ')
        # Call master to make the actions
        return """
                  [+] Try Again to deploy
                """

    def dep_confirm(self):
        self.master.info_logger.write_info('Received manual command: dep_confirm ')
        # Call master to make the actions
        return """
                  [+] Deployment Confirmed
                """

    def dep_cutoff(self):
        self.master.info_logger.write_info('Received manual command: dep_cutoff ')
        # Call master to make the actions
        return """
                  [+]Deployment Cutted Off
                """

    def dep_abort_cutoff(self):
        self.master.info_logger.write_info('Received manual command: dep_abort_cutoff ')
        # Call master to make the actions
        return """
                  [+]Deployment Cut Off Aborted
                """

    def dep_retrieve(self):
        self.master.info_logger.write_info('Received manual command: dep_retrieve ')
        # Call master to make the actions
        return """
                  [+]Retrieved Successfuly
                """

    def dep_retrieve_again(self):
        self.master.info_logger.write_info('Received manual command: dep_retrieve_again ')
        # Call master to make the actions
        return """
                  [+]Try to Retrieved Again
                """

    def adcs_set_auto(self):
        self.master.info_logger.write_info('Received manual command: adcs_set_auto ')
        # Call master to make the actions
        return """
                  [+]ADCS in auto mode
                """

    def adcs_set_manual(self):
        self.master.info_logger.write_info('Received manual command: adcs_set_manual ')
        # Call master to make the actions
        return """
                  [+]ADCS in manual mode
                """

    def adcs_scan(self):
        self.master.info_logger.write_info('Received manual command: adcs_scan ')
        # Call master to make the actions
        return """
                  [+]Scanned Successfuly
                """

    def adcs_set_pos(self):
        self.master.info_logger.write_info('Received manual command: adcs_set_pos ')
        # Call master to make the actions
        return """
                  [+]Possition setted Successfuly
                """

    def tx_stop_emmision(self):
        self.master.info_logger.write_info('Received manual command: tx_stop_emmision')
        # Call master to make the actions
        return """
                  [+] Emmision Stopped
                """


if __name__ == "__main__":
    ELinkManager().start()
