from pypylon import pylon
import platform
from pypylon import genicam
from time import sleep
import sys
import Paths as paths
from pathlib import Path
import os

class OBCS:

    __instance = None

    def __init__(self,image_lock):

        if OBCS.__instance is not None:

            raise Exception('This class is a singleton!')
        else:
            self.image_dir = Path("Images")
            # Number of images to be grabbed.
            self.countOfImagesToGrab = 1
            # The exit code of the sample application.
            self.exitCode = 0
            self.img_counter = 0
            self.image_lock = image_lock
            self.stop_taking_images = False
            OBCS.__instance = self

    @staticmethod
    def get_instance():

        if OBCS.__instance is None:
            OBCS(None) #Bad bad bad
        return OBCS.__instance


    def close_camera(self):
        self.stop_taking_images = True

    def start(self):
        
        print('START OBCS')
        try:
            img = pylon.PylonImage()
            tlf = pylon.TlFactory.GetInstance()
            # Create an instant camera object with the camera device found first.
            camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
    
            print("Using device ", camera.GetDeviceInfo().GetModelName())
            camera.MaxNumBuffer = 5
            camera.Open()
            while True:

                if self.stop_taking_images : break

                self.img_counter += 1
                camera.StartGrabbingMax(self.countOfImagesToGrab)

                # Camera.StopGrabbing() is called automatically by the RetrieveResult() method
                # when c_countOfImagesToGrab images have been retrieved.
                while camera.IsGrabbing():
                    # Wait for an image and then retrieve it. A timeout of 5000 ms is used.
                    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

                    # Image grabbed successfully?
                    if grabResult.GrabSucceeded():
                        # Calling AttachGrabResultBuffer creates another reference to the
                        # grab result buffer. This prevents the buffer's reuse for grabbing.
                        img.AttachGrabResultBuffer(grabResult)
                        filename = os.path.join(self.image_dir, "image_%d.png" % self.img_counter)
                        self.image_lock.acquire()
                        img.Save(pylon.ImageFileFormat_Png, filename)
                        self.image_lock.release()
                    else:
                        print("Error: ", grabResult.ErrorCode, grabResult.ErrorDescription)

                    img.Release()
                    # check if m a tab
                    grabResult.Release()
                    sleep(20)
        except genicam.GenericException as e:
            # Error handling.
            print("An exception occurred.")
            print(e.GetDescription())
            self.exitCode = 1

#sys.exit(exitCode)
