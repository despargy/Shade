from pypylon import pylon
import platform
from pypylon import genicam
from time import sleep
import sys

class OBCS:

    __instance = None

    def __init__(self, master_):

        if OBCS.__instance is not None:

            raise Exception('This class is a singleton!')
        else:
            self.master = master_
            self.info_logger = self.master.info_logger
            # Number of images to be grabbed.
            self.countOfImagesToGrab = 1
            # The exit code of the sample application.
            self.exitCode = 0
            self.img_counter = 0
            OBCS.__instance = self

    @staticmethod
    def get_instance():

        if OBCS.__instance is None:
            OBCS(None)
        return OBCS.__instance

    def start(self):

        self.master.info_logger.write_info('START OBCS')
        print('START OBCS')
        try:
            img = pylon.PylonImage()
            tlf = pylon.TlFactory.GetInstance()
            # Create an instant camera object with the camera device found first.
            camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
            self.info_logger.write_info("Using device ", camera.GetDeviceInfo().GetModelName())
            print("Using device ", camera.GetDeviceInfo().GetModelName())
            camera.MaxNumBuffer = 5
            camera.Open()
            while not self.master.status_vector['CLOSE']:
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
                        filename = "/home/pi/Desktop/CameraFolder/Images/saved_pypylon_img_%d.png" % self.img_counter
                        img.Save(pylon.ImageFileFormat_Png, filename)
                    else:
                        print("Error: ", grabResult.ErrorCode, grabResult.ErrorDescription)

                    img.Release()
                    # check if m a tab
                    grabResult.Release()
                    sleep(5)
        except genicam.GenericException as e:
            # Error handling.
            self.info_logger.write_error("An exception occurred.")
            self.info_logger.write_error(e.GetDescription())
            print("An exception occurred.")
            print(e.GetDescription())
            self.exitCode = 1

#sys.exit(exitCode)
