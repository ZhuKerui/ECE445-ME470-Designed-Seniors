
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
from ble import BLE_Driver, device_addr, read_uuid, write_uuid
from time import time

class Ui_MainWindow(QWidget):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        self.timer_camera = QtCore.QTimer()
        self.camera_manager = Camera_Manager()
        self.ble_manager = BLE_Driver(device_addr=device_addr, read_uuid=read_uuid, write_uuid=write_uuid, read_handler=print)
        # self.ble_manager.start()
        self.mpii = MPII(self.process_angle_data)
        self.CAM_NUM = 0
        self.pose_model = Live_Model(self)
        self.pose_model.start()
        self.set_ui()
        self.imitation_enable = False
        # Debug and Param Adjust stuffs
        self.count = 0
        self.denoise = False
        self.record = False
        self.threshold = 0
        self.pose_data_raw = np.array([])
        self.pose_data_denoise = np.array([])
        self.angle_data = np.array([])
        self.record_start_time = time()
        self.record_list = []

    def set_ui(self):

        # Layout elements setup
        user_group = QGroupBox('User', self)
        user_layout = QHBoxLayout()
        self.camera_open_button = QPushButton(u'Camera On')
        user_layout.addWidget(self.camera_open_button)
        user_group.setLayout(user_layout)

        debug_group = QGroupBox('Debug', self)
        debug_layout = QHBoxLayout()
        self.denoise_button = QPushButton(u'Denoise On')
        test_button = QPushButton(u'Test Command')
        print_data_button = QPushButton(u'Print Data')
        self.record_button = QPushButton(u'Record On')
        debug_layout.addWidget(self.denoise_button)
        debug_layout.addWidget(test_button)
        debug_layout.addWidget(print_data_button)
        debug_layout.addWidget(self.record_button)
        debug_group.setLayout(debug_layout)

        param_group = QGroupBox('Param', self)
        param_layout = QHBoxLayout()
        self.threshold_input = QLineEdit()
        set_threshold_button = QPushButton('Set Threshold')
        param_layout.addWidget(set_threshold_button)
        param_layout.addWidget(self.threshold_input)
        param_group.setLayout(param_layout)

        operation_layout = QVBoxLayout()
        operation_layout.addWidget(user_group)
        operation_layout.addWidget(debug_group)
        operation_layout.addWidget(param_group)
        
        image_layout = QHBoxLayout()
        self.camera_display_label = QLabel()
        self.camera_display_label.setFixedSize(641, 481)
        self.camera_display_label.setAutoFillBackground(False)
        self.coordinatograph = Coordinatograph('3D Skeleton Display', '', '', '', '')
        image_layout.addWidget(self.camera_display_label)
        image_layout.addWidget(self.coordinatograph)

        main_layout = QVBoxLayout()
        main_layout.addLayout(image_layout)
        main_layout.addLayout(operation_layout)
        
        # Signal connections setup
        self.camera_open_button.clicked.connect(self.camera_open_button_click)
        self.denoise_button.clicked.connect(self.denoise_button_click)
        test_button.clicked.connect(self.send_test_command)
        print_data_button.clicked.connect(self.print_data)
        self.record_button.clicked.connect(self.record_button_click)
        set_threshold_button.clicked.connect(self.set_threshold_button_click)
        self.timer_camera.timeout.connect(self.show_camera)
        self.pose_model.model_signal.connect(self.process_pose_data)

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

    def denoise_button_click(self):
        self.denoise = not self.denoise
        self.denoise_button.setText('Denoise Off' if self.denoise else 'Denoise On')

    def send_test_command(self):
        test_data = np.array([90, 90, 90, 90, 45, 45, 45, 45, 30, 30, 30, 30, 1, 1, 1, 1], dtype=np.uint8)
        self.ble_manager.write(b'\x00%b' % test_data.tobytes())

    def print_data(self):
        print('Raw Pose Data:')
        for i in range(len(self.pose_data_raw)):
            print('%s: %d' % (MPII.point_labels[i], self.pose_data_raw[i]))
        print('Denoised Angle Data:')
        for i in range(len(self.angle_data)):
            print('%s: %d' % (MPII.angle_labels[i], self.angle_data[i]))

    def record_button_click(self):
        self.record = not self.record
        if self.record:
            self.record_button.setText('Record Off')
            self.record_start_time = time()
            self.record_list = []
        else:
            print(time() - self.record_start_time)
            self.record_button.setText('Record On')
            print(len(self.record_list))

    def set_threshold_button_click(self):
        self.threshold = float(self.threshold_input.text())
        print(self.threshold)

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

    def process_pose_data(self, points:np.ndarray):
        self.pose_data_raw = points
        self.mpii.handle_pose_data(points)

    def process_angle_data(self, angles:np.ndarray):
        if self.record:
            # Record the time stamp and angle data
            self.record_list.append((time() - self.record_start_time, angles))

        if self.denoise:
            # Calculate the reconstructed pose data
            self.pose_data_denoise = self.mpii.reconstruct_pose_data(angles)

        if self.imitation_enable:
            # Send command if imitation is enabled
            self.ble_manager.write(b'\x00%b' % angles.tobytes())

        # Update graphic display
        self.coordinatograph.update_value(self.pose_data_denoise if self.denoise else self.pose_data_raw)

    def closeEvent(self, event):
        ok = QtWidgets.QPushButton()
        cacel = QtWidgets.QPushButton()

        msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, u"Exit", u"Are you sure to exit?")

        msg.addButton(ok,QtWidgets.QMessageBox.ActionRole)
        msg.addButton(cacel, QtWidgets.QMessageBox.RejectRole)
        ok.setText(u'yes')
        cacel.setText(u'cancel')
        if msg.exec_() == QtWidgets.QMessageBox.RejectRole:
            event.ignore()
        else:
            if self.camera_manager.isOpened():
                self.camera_manager.release()
            if self.timer_camera.isActive():
                self.timer_camera.stop()
            self.pose_model.stop()
            # self.ble_manager.stop()
            event.accept()



if __name__ == "__main__":
    App = QApplication(sys.argv)
    ex = Ui_MainWindow()
    ex.show()
    sys.exit(App.exec_())