#!/usr/bin/python3
import socket
import threading
import json
import time


class ELinkManager:

    def __init__(self):
        self.host = ''
        self.recv_port = 12345
        self.BUFFER_SIZE = 1024
        self.recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.recv_socket.bind((self.host, self.recv_port))
        self.recv_socket.listen(5)


    def start(self):
        """Initialize ELinkManager. Bind him to await for a connection"""
        while True:
           #start listening
           ground_socket,addr = self.recv_socket.accept()
           print("Got a connection from %s" % str(addr))
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
            Function to handle communication with ground software
        """
        #send prompt
        try:
            ground_socket.send(self.show_prompt().encode('utf-8'))
            while(True):
                #get package as json string
                ground_package_json = ground_socket.recv(self.BUFFER_SIZE).decode('utf-8')
                if not ground_package_json:
                    print("Lost connection with %s" % str(addr))
                    break
                #handle the client package
                server_response = self.handle_package(ground_package_json)
                #send repsonse to client
                ground_socket.send(server_response.encode('utf-8'))

            ground_socket.close()
        except ConnectionResetError:
            #remove this , add log
            print('Lost Connection unexpected')

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
        print("Command is deploy")
        # Call master to make the actions
        return """
                  [+] Deployed Successfuly
                """

    def dep_abort(self):
        print("Command is dep_abort")
        # Call master to make the actions
        return """
                  [+] Deployment Aborted
                """

    def dep_again(self):
        print("Command is dep_again")
        # Call master to make the actions
        return """
                  [+] Try Again to deploy
                """

    def dep_confirm(self):
        print("Command is dep_confirm")
        # Call master to make the actions
        return """
                  [+] Deployment Confirmed
                """

    def dep_cutoff(self):
        print("Command is dep_cutoff")
        # Call master to make the actions
        return """
                  [+]Deployment Cutted Off
                """

    def dep_abort_cutoff(self):
        print("Command is dep_abort_cutoff")
        # Call master to make the actions
        return """
                  [+]Deployment Cut Off Aborted
                """

    def dep_retrieve(self):
        print("Command is dep_retrieve")
        # Call master to make the actions
        return """
                  [+]Retrieved Successfuly
                """

    def dep_retrieve_again(self):
        print("Command is dep_retrieve_again")
        # Call master to make the actions
        return """
                  [+]Try to Retrieved Again
                """

    def adcs_set_auto(self):
        print("Command is adcs_set_auto")
        # Call master to make the actions
        return """
                  [+]ADCS in auto mode
                """

    def adcs_set_manual(self):
        print("Command is adcs_set_manual")
        # Call master to make the actions
        return """
                  [+]ADCS in manual mode
                """

    def adcs_scan(self):
        print("Command is adcs_scan")
        # Call master to make the actions
        return """
                  [+]Scanned Successfuly
                """

    def adcs_set_pos(self):
        print("Command is adcs_set_pos")
        # Call master to make the actions
        return """
                  [+]Possition setted Successfuly
                """

    def tx_stop_emmision(self):
        print("Command is tx_stop_emmision")
        # Call master to make the actions
        return """
                  [+] Emmision Stopped
                """


if __name__ == "__main__":
    ELinkManager().start()