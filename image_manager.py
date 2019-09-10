#!/usr/bin/python3
import socket
import time
import sys, os
import glob
import threading
import json
import OBCS
import RPi.GPIO as GPIO
import Pins as pins

"""TODO:
        - Internet Lost handle
        - Merge it with OBCS
        - Add some more annotiations
        - Make it sexy :)
"""
class ImageManager:

    def __init__(self,ground_ip):
        if(ground_ip == 'local'):
            self.host = socket.gethostname()
        else:
            self.host = ground_ip
        
        self.image_dir = "Images"
        self.log_dir = 'Logs'
        self.last_image = '' 
        self.image_lock = threading.Lock()
        
        #start OBCS to taking and saving images
        self.obcs = OBCS.OBCS(self.image_lock)
        self.obcs_thread = threading.Thread(target=self.obcs.start)
        self.obcs_thread.start()

        self.command_port = 12654
        self.command_host = ''
        self.command_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.command_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.command_socket.bind((self.command_host, self.command_port))
        self.command_socket.listen(5)
        threading.Thread(target=self.start).start()

        self.port = 12346
        self.BUFFER_SIZE = 1024
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.pin_powerA = pins.Pins().pin_powerA
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin_powerA, GPIO.OUT)
        GPIO.output(self.pin_powerA, GPIO.HIGH)



    def start_server(self):
        """Initialize Image Manager. Bind him to await for a connection"""
        while True:
           #start listening
           ground_socket,addr = self.command_socket.accept()
           print('Got a connection from {addr}'.format(addr=addr))
           #Start Thread to serve client
           threading.Thread(target=self.open_connetion,
                            args=(ground_socket,addr, )).start()
                            

    
    def open_connetion(self,ground_socket,addr):
        """
            @ground_socket : the connection socket between ground and ImageManager
            @addr: the ground address
            Function to handle communication with ground software for manual commands
        """
        #send prompt
        try:
            while(True):
                #get package as json string
                ground_package_json = ground_socket.recv(self.BUFFER_SIZE).decode('utf-8')
                if not ground_package_json:
                    print('Lost connection unexpectedly from {addr}'.format(addr=addr))
                    break

                #handle the client package
                server_response = self.handle_package(ground_package_json)
                #send repsonse to client
                ground_socket.send(server_response.encode('utf-8'))

            ground_socket.close()
        except ConnectionResetError:
            #remove this , add log
            print('Lost connection unexpectedly from {addr}'.format(addr=addr))

    
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
        
        if action == 'GET_IMAGE':
            index = client_data["index"]
            image_filename = "image_{index}.png".format(index=index)
            if(self.imageExists(image_filename)):
                self.image_lock.acquire()
                self.send_image(image_filename)
                self.image_lock.release()
                response = "Image {image_filename} successfuly sended".format(image_filename=image_filename)
            else:
                response = "Image {image_filename} doesn't exists".format(image_filename=image_filename)
        elif action == 'REBOOT':
            GPIO.output(self.pin_powerA, GPIO.LOW)
            time.sleep(5)
            GPIO.output(self.pin_powerA, GPIO.HIGH)
            response = "Successfuly Reboot"
        elif action == 'CLOSE':
            self.obcs.close_camera()
            self.obcs_thread.join()
            response = "Successfuly closed camera."
        else:
            response = "Unknown command {action}".format(action=action)

        return response


    def get_last_image(self):
        """Returns the filename of the latests image. 
           Checks if the latest image is the same with 
           previous sended to avoid sending same image
           twice.
        
        Returns:
            [string] latest_image -- the filename of latest image
        """
        latest_image = ""
        if not os.path.isdir(self.image_dir):
            os.mkdir(self.image_dir)
            return latest_image #empty

        list_of_images = glob.glob('Images/*')
        
        if not list_of_images: return ""
            
        latest_image = max(list_of_images, key=os.path.getctime)
        latest_image = os.path.basename(os.path.normpath(latest_image))
        
        if latest_image != self.last_image:
            self.last_image = latest_image
            return latest_image

        return "" #empty

      
    def imageExists(self,filename):
        return os.path.isdir(self.image_dir) and os.path.exists(self.image_dir+"/"+filename)

    def isSafeToRead(self):
        """Checks if is safe to read the image file
        
        Returns:
            [boolean] -- True: dir and filename exists
                         False: the dir or the filename doesn't exists
        """
        return os.path.isdir(self.image_dir)


    def start(self):
        
        while(True):
            #get latest image
            image_name = self.get_last_image()
            if image_name == "":
                time.sleep(3)
                continue
            
            #send image
            self.image_lock.acquire()
            self.send_image(image_name)
            self.image_lock.release()

        self.socket.close()


    def send_image(self, image_name):
        """
            @image_name : the filename of image to send.
            Function to send image to ground software.
        """
    
        #first send filename
        self.socket.sendto(image_name.encode('utf-8'), (self.host, self.port))
        print ("Begin sending "+image_name+" ...")
             
        if not self.isSafeToRead():
            os.mkdir(self.image_dir)

        try:
            with open(self.image_dir+'/'+image_name, "rb") as imageFile:
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
        ImageManager(ground_ip).start_server()