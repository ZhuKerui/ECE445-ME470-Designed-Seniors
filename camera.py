import cv2

class Camera_Manager:
    def __init__(self):
        self.cap = cv2.VideoCapture()
        self.file_valid = False

    def get_camera_image(self):
        self.file_valid, image = self.cap.read()
        if not self.file_valid:
            return None
        return image
    
    def release(self):
        self.cap.release()

    def open(self, camera_number):
        self.cap.open(camera_number)
        self.file_valid = True

    def isOpened(self):
        return self.cap.isOpened()