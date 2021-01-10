import cv2

class Camera_Manager:
    def __init__(self):
        self.cap = cv2.VideoCapture()

    def get_camera_image(self):
        flag, image = self.cap.read()
        show = cv2.resize(image, (640, 480))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        return show
    
    def release(self):
        self.cap.release()

    def open(self, camera_number):
        self.cap.open(camera_number)

    def isOpened(self):
        return self.cap.isOpened()