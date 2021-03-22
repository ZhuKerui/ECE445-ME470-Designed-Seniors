
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2
import numpy as np

from camera import Camera_Manager
from graph import Coordinatograph
from live_demo import Live_Model
from mpii import MPII

def normalize(vecs:np.ndarray):
    normalizers = np.sqrt((vecs * vecs).sum(axis=1))
    normalizers[normalizers==0]=1
    return (vecs.T / normalizers).T


class Ui_MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        self.timer_camera = QtCore.QTimer()
        self.camera_manager = Camera_Manager()
        self.CAM_NUM = 0
        self.pose_model = Live_Model(self)
        self.pose_model.start()
        self.set_ui()
        self.x =0
        self.count = 0

    def set_ui(self):

        # Layout elements setup
        self.camera_open_button = QtWidgets.QPushButton(u'Camera On')
        close_button = QtWidgets.QPushButton(u'Exit')
        self.camera_display_label = QtWidgets.QLabel()
        self.camera_display_label.setFixedSize(641, 481)
        self.camera_display_label.setAutoFillBackground(False)
        coordinatograph = Coordinatograph('3D Skeleton Display', '', '', '', '')

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.camera_open_button)
        button_layout.addWidget(close_button)

        image_layout = QtWidgets.QHBoxLayout()
        image_layout.addWidget(self.camera_display_label)
        image_layout.addWidget(coordinatograph)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(image_layout)
        main_layout.addLayout(button_layout)
        
        # Signal connections setup
        self.camera_open_button.clicked.connect(self.camera_open_button_click)
        self.timer_camera.timeout.connect(self.show_camera)
        close_button.clicked.connect(self.close)
        self.pose_model.model_signal.connect(coordinatograph.update_value)
        self.pose_model.model_signal.connect(self.send_command)

        # Launch the layout
        self.setLayout(main_layout)
        self.setWindowTitle(u'Keebot Demo')

    def camera_open_button_click(self):
        if self.timer_camera.isActive() == False:
            flag = self.camera_manager.open(self.CAM_NUM)
            if flag == False:
                msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"Please check whether the camera is connected to the computer correctly", buttons=QtWidgets.QMessageBox.Ok,
                                            defaultButton=QtWidgets.QMessageBox.Ok)
            else:
                self.timer_camera.start(30)
                self.camera_open_button.setText(u'Camera off')
        else:
            self.timer_camera.stop()
            self.camera_manager.release()
            self.camera_display_label.clear()
            self.camera_open_button.setText(u'Camera on')

    def show_camera(self):
        camera_image = self.camera_manager.get_camera_image()
        image_h, image_w = camera_image.shape[0:2]
        showImage = QtGui.QImage(camera_image.data, camera_image.shape[1], camera_image.shape[0], QtGui.QImage.Format_RGB888)
        self.camera_display_label.setPixmap(QtGui.QPixmap.fromImage(showImage))
        short_edge = min(image_h, image_w)
        half_short_edge = int(short_edge / 2)
        center_h, center_w = int(image_h / 2), int(image_w / 2)
        camera_image = camera_image[(center_h-half_short_edge):(center_h+half_short_edge), (center_w-half_short_edge):(center_w+half_short_edge)]
        camera_image = cv2.resize(camera_image, (256, 256))
        self.pose_model.enqueue_image(camera_image)

    def send_command(self, points:np.ndarray):
        # Get vectors
        neck2r_shoulder = points[MPII.r_shoulder] - points[MPII.neck]
        neck2spine = points[MPII.spine] - points[MPII.neck]
        neck2l_shoulder = points[MPII.l_shoulder] - points[MPII.neck]
        r_shoulder2r_elbow = points[MPII.r_elbow] - points[MPII.r_shoulder]
        l_shoulder2l_elbow = points[MPII.l_elbow] - points[MPII.l_shoulder]
        r_elbow2r_wrist = points[MPII.r_wrist] - points[MPII.r_elbow]
        l_elbow2l_wrist = points[MPII.l_wrist] - points[MPII.l_elbow]
        pelvis2r_hip = points[MPII.r_hip] - points[MPII.pelvis]
        pelvis2l_hip = points[MPII.l_hip] - points[MPII.pelvis]
        r_hip2l_hip = points[MPII.l_hip] - points[MPII.r_hip]
        r_hip2r_knee = points[MPII.r_knee] - points[MPII.r_hip]
        r_knee2r_ankle = points[MPII.r_ankle] - points[MPII.r_knee]
        l_hip2l_knee = points[MPII.l_knee] - points[MPII.l_hip]
        l_knee2l_ankle = points[MPII.l_ankle] - points[MPII.l_knee]
        
        r_chest_plane = np.cross(neck2r_shoulder, neck2spine)
        l_chest_plane = np.cross(neck2spine, neck2l_shoulder)
        haunch_plane = np.cross(pelvis2r_hip, pelvis2l_hip)

        # Calculate angles
        v1 = np.vstack([r_elbow2r_wrist,    r_shoulder2r_elbow, l_elbow2l_wrist,    l_shoulder2l_elbow, r_knee2r_ankle, l_knee2l_ankle, -r_hip2l_hip,   r_hip2l_hip,    r_shoulder2r_elbow, l_shoulder2l_elbow, r_hip2r_knee,   l_hip2l_knee])
        v2 = np.vstack([r_shoulder2r_elbow, neck2r_shoulder,    l_shoulder2l_elbow, neck2l_shoulder,    r_hip2r_knee,   l_hip2l_knee,   r_hip2r_knee,   l_hip2l_knee,   r_chest_plane,      l_chest_plane,      haunch_plane,   haunch_plane])
        v1 = normalize(v1)
        v2 = normalize(v2)
        angles = (v1 * v2).sum(axis=1)
        angles[:8] = np.arccos(angles[:8])
        angles[8:] = np.arcsin(angles[8:])
        return angles.astype(np.int16)

    def closeEvent(self, event):
        ok = QtWidgets.QPushButton()
        cacel = QtWidgets.QPushButton()

        msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, u"Exit", u"Are you sure to exit?")

        msg.addButton(ok,QtWidgets.QMessageBox.ActionRole)
        msg.addButton(cacel, QtWidgets.QMessageBox.RejectRole)
        ok.setText(u'yes')
        cacel.setText(u'cancel')
        # msg.setDetailedText('sdfsdff')
        if msg.exec_() == QtWidgets.QMessageBox.RejectRole:
            event.ignore()
        else:
            if self.camera_manager.isOpened():
                self.camera_manager.release()
            if self.timer_camera.isActive():
                self.timer_camera.stop()
            self.pose_model.stop()
            event.accept()



if __name__ == "__main__":
    App = QApplication(sys.argv)
    ex = Ui_MainWindow()
    ex.show()
    sys.exit(App.exec_())