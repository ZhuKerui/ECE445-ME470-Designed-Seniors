import cv2

class Camera_Manager:
    def __init__(self):
        self.cap = cv2.VideoCapture()
        self.file_valid = False

    def get_camera_image(self):
        self.file_valid, image = self.cap.read()
        if not self.file_valid:
            return None
        show = cv2.resize(image, (640, 480))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        return show
    
    def release(self):
        self.cap.release()

    def open(self, camera_number):
        self.cap.open(camera_number)
        self.file_valid = True

    def isOpened(self):
        return self.cap.isOpened()