
import sys
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2
import numpy as np
import pandas as pd

from camera import Camera_Manager
from graph import Coordinatograph
from live_demo import Live_Model
from mpii import MPII
from ble import BLE_Driver, device_addr, read_uuid, write_uuid
from time import sleep, time
import pdb

class Ui_MainWindow(QWidget):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        # Initialize device managers and main components
        self.timer_camera = QtCore.QTimer()
        self.camera_manager = Camera_Manager()
        self.ble_manager = BLE_Driver(device_addr=device_addr, read_uuid=read_uuid, write_uuid=write_uuid, read_handler=print, parent=self)
        self.ble_manager.start()
        self.mpii = MPII()
        self.CAM_NUM = 0
        self.pose_model = Live_Model(self)
        self.pose_model.start()
        self.set_ui()
        self.imitation_enable = True
        # Debug and Param Adjust stuffs
        self.is_record = False                  # Whether it is recording
        self.is_record_video = False            # Whether it is recording video
        self.video_writer = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        self.vw = None
        self.pose_data_raw = np.array([])       # The pose data calculated by the neural network model
        self.pose_data_denoise = np.array([])   # The pose data reconstructed from denoised data
        self.angle_data = np.array([])          # The angle data for each servo
        self.record_start_time = time()         # The starting time of the recording
        self.record_list = pd.DataFrame(columns=['time']+MPII.angle_labels)   # The recorded angle data

    def set_ui(self):
        '''
        Layout elements setup
        '''
        # User operations group
        user_group = QGroupBox('User', self)
        user_layout = QHBoxLayout()
        self.camera_open_button = QPushButton(u'Camera On')
        choose_image_button = QPushButton('Choose Image')
        self.choose_video_button = QPushButton('Choose Video')
        self.record_video_button = QPushButton('Record Video')
        show_std_pose_button = QPushButton('Show Standard')
        user_layout.addWidget(self.camera_open_button)
        user_layout.addWidget(choose_image_button)
        user_layout.addWidget(self.choose_video_button)
        user_layout.addWidget(show_std_pose_button)
        user_layout.addWidget(self.record_video_button)
        user_group.setLayout(user_layout)

        # Debug operations group
        debug_group = QGroupBox('Debug', self)
        debug_layout = QHBoxLayout()
        self.denoise_button = QPushButton(u'Denoise On')
        test_button = QPushButton(u'Test Command')
        print_data_button = QPushButton(u'Print Data')
        self.record_button = QPushButton(u'Record On')
        show_axis_button = QPushButton(u'Show Axis')
        self.axis_id_input = QLineEdit()
        debug_layout.addWidget(self.denoise_button)
        debug_layout.addWidget(test_button)
        debug_layout.addWidget(print_data_button)
        debug_layout.addWidget(self.record_button)
        debug_layout.addWidget(show_axis_button)
        debug_layout.addWidget(self.axis_id_input)
        debug_group.setLayout(debug_layout)

        # Parameter adjustment operations group
        param_group = QGroupBox('Param', self)
        param_layout = QHBoxLayout()
        self.threshold_input = QLineEdit()
        set_threshold_button = QPushButton('Set Threshold')
        self.v_lim_input = QLineEdit()
        set_v_lim_button = QPushButton('Set Velocity Lim')
        param_layout.addWidget(set_threshold_button)
        param_layout.addWidget(self.threshold_input)
        param_layout.addWidget(set_v_lim_button)
        param_layout.addWidget(self.v_lim_input)
        param_group.setLayout(param_layout)

        # General operations layout
        operation_layout = QVBoxLayout()
        operation_layout.addWidget(user_group)
        operation_layout.addWidget(debug_group)
        operation_layout.addWidget(param_group)
        
        # Visual demostration layout
        image_layout = QHBoxLayout()
        self.camera_display_label = QLabel()
        self.camera_display_label.setFixedSize(641, 481)
        self.camera_display_label.setAutoFillBackground(False)
        self.coordinatograph = Coordinatograph('3D Skeleton Display', '', '', '', '')
        self.debug_graph = Coordinatograph('3D Skeleton Display', '', '', '', '')
        image_layout.addWidget(self.camera_display_label)
        image_layout.addWidget(self.coordinatograph)
        image_layout.addWidget(self.debug_graph)

        # Main layout of the UI
        main_layout = QVBoxLayout()
        main_layout.addLayout(image_layout)
        main_layout.addLayout(operation_layout)
        
        # Signal connections setup
        self.camera_open_button.clicked.connect(self.camera_open_button_click)
        choose_image_button.clicked.connect(self.analyze_image_file)
        self.choose_video_button.clicked.connect(self.analyze_video_file)
        show_std_pose_button.clicked.connect(self.show_std_pose)
        self.record_video_button.clicked.connect(self.record_video_button_click)
        self.denoise_button.clicked.connect(self.denoise_button_click)
        test_button.clicked.connect(self.send_test_command)
        print_data_button.clicked.connect(self.print_data)
        self.record_button.clicked.connect(self.record_button_click)
        show_axis_button.clicked.connect(self.show_axis_button_click)
        set_threshold_button.clicked.connect(self.set_threshold_button_click)
        set_v_lim_button.clicked.connect(self.set_v_lim_button_click)
        self.timer_camera.timeout.connect(self.show_camera)
        self.pose_model.model_signal.connect(self.process_pose_data)

        # Launch the layout
        self.setLayout(main_layout)
        self.setWindowTitle(u'Keebot Demo')

    def camera_open_button_click(self):
        '''
        Turn on/off the camera
        '''
        if self.timer_camera.isActive() == False:
            self.__start_flow_analysis(self.CAM_NUM)
            self.camera_open_button.setText(u'Camera off')
        else:
            self.__stop_flow_analysis()
            self.camera_open_button.setText(u'Camera on')

    def __start_flow_analysis(self, input_stream):
        flag = self.camera_manager.open(input_stream)
        if flag == False:
            msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"Please check whether the camera is connected to the computer correctly", buttons=QtWidgets.QMessageBox.Ok,
                                        defaultButton=QtWidgets.QMessageBox.Ok)
        else:
            self.timer_camera.start(40)
            self.imitation_enable = True    # Enable the imitation

    def __stop_flow_analysis(self):
        self.timer_camera.stop()
        self.camera_manager.release()
        self.camera_display_label.clear()

    def analyze_image_file(self):
        fileName,fileType = QFileDialog.getOpenFileName(None, "choose file", os.getcwd(), "All Files(*)")
        if not fileName:
            return
        temp_image = cv2.imread(fileName)
        self.analyze_image(temp_image)

    def analyze_video_file(self):
        if self.timer_camera.isActive() == False:
            fileName,fileType = QFileDialog.getOpenFileName(None, "choose file", os.getcwd(), "All Files(*)")
            if not fileName:
                return
            self.__start_flow_analysis(fileName)
            self.choose_video_button.setText(u'Stop Video')
        else:
            self.__stop_flow_analysis()
            self.choose_video_button.setText(u'Choose Video')

    def show_std_pose(self):
        self.coordinatograph.update_value(self.mpii.std_pose)

    def record_video_button_click(self):
        if not self.is_record_video:
            fileName,fileType = QFileDialog.getSaveFileName(None, "choose file", os.getcwd(), "All Files(*)")
            if not fileName:
                return
            self.vw = cv2.VideoWriter(fileName, self.video_writer, 25, (640, 480))
        else:
            self.vw.release()
        self.is_record_video = not self.is_record_video
        self.record_video_button.setText('Stop Recording' if self.is_record_video else 'Record Video')

    def denoise_button_click(self):
        '''
        Turn on/off the denoise
        '''
        self.mpii.is_denoise = not self.mpii.is_denoise
        self.denoise_button.setText('Denoise Off' if self.mpii.is_denoise else 'Denoise On')

    def send_test_command(self):
        '''
        Send pre-defined test command
        '''
        # test_data = np.array([90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 10], dtype=np.uint8)
        test_data = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 10], dtype=np.uint8)
        self.ble_manager.write(b'\x00%b' % test_data.tobytes())
        print('Send')

    def print_data(self):
        '''
        Print the present raw pose data and the denoised angle data to the terminal
        '''
        # print('Raw Pose Data:')
        # for i in range(len(self.pose_data_raw)):
        #     print(self.pose_data_raw[i])
        print('Denoised Angle Data:')
        for i in range(len(self.angle_data)):
            print('%s: %d' % (MPII.angle_labels[i], self.angle_data[i]))
        print(self.mpii.div)

    def record_button_click(self):
        '''
        Turn on/off the recording
        '''
        self.is_record = not self.is_record
        if self.is_record:
            self.record_button.setText('Record Off')
            self.record_start_time = time()
            self.record_list.drop(self.record_list.index, inplace=True)
        else:
            self.record_button.setText('Record On')
            self.record_list.to_csv('temp.csv', index=False)

    def show_axis_button_click(self):
        axis_id = int(self.axis_id_input.text())
        if axis_id == 0:
            self.coordinatograph.show_axis(self.pose_data_raw[MPII.r_shoulder], self.mpii.r_shoulder_axis)
        elif axis_id == 1:
            self.coordinatograph.show_axis(self.pose_data_raw[MPII.l_shoulder], self.mpii.l_shoulder_axis)
        elif axis_id == 2:
            self.coordinatograph.show_axis(self.pose_data_raw[MPII.r_hip], self.mpii.r_hip_axis)
        elif axis_id == 3:
            self.coordinatograph.show_axis(self.pose_data_raw[MPII.l_hip], self.mpii.l_hip_axis)
        else:
            self.coordinatograph.clear_axis()
            
    def set_threshold_button_click(self):
        self.mpii.div_lim = float(self.threshold_input.text())
        print(self.mpii.div_lim)

    def set_v_lim_button_click(self):
        self.mpii.v_lim = float(self.v_lim_input.text()) * np.ones(16)

    def show_camera(self):
        camera_image = self.camera_manager.get_camera_image()
        if self.camera_manager.file_valid:
            self.analyze_image(camera_image)
        else:
            self.__stop_flow_analysis()
            self.choose_video_button.setText('Choose Video')
            self.camera_open_button.setText('Camera On')

    def analyze_image(self, camera_image:np.ndarray):
        show = cv2.resize(camera_image, (640, 480))
        if self.is_record_video:
            self.vw.write(show)
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        image_h, image_w = show.shape[0:2]
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.camera_display_label.setPixmap(QtGui.QPixmap.fromImage(showImage))
        short_edge = min(image_h, image_w)
        half_short_edge = int(short_edge / 2)
        center_h, center_w = int(image_h / 2), int(image_w / 2)
        show = show[(center_h-half_short_edge):(center_h+half_short_edge), (center_w-half_short_edge):(center_w+half_short_edge)]
        show = cv2.resize(show, (256, 256))
        self.pose_model.enqueue_image(show)

    def process_pose_data(self, points:np.ndarray):
        self.pose_data_raw = points
        self.process_angle_data(self.mpii.handle_pose_data(points))

    def process_angle_data(self, angles:np.ndarray):
        self.angle_data = angles
        # Calculate the reconstructed pose data
        self.pose_data_denoise = self.mpii.reconstruct_pose_data(angles)

        if self.is_record:
            # Record the time stamp and angle data
            new_data = {MPII.angle_labels[i] : angles[i] for i in range(16)}
            new_data['time'] = self.mpii.interval
            self.record_list.append(pd.DataFrame(new_data), ignore_index=True)

        target_time = np.uint8(self.mpii.interval * 10) if self.mpii.interval < 5 else 50

        if self.imitation_enable:
            # Send command if imitation is enabled
            self.ble_manager.write(b'\x00%b' % np.append(self.angle_data, target_time).astype(np.uint8).tobytes())

        # Update graphic display
        self.coordinatograph.update_value(self.pose_data_raw)
        self.debug_graph.update_value(self.pose_data_denoise)

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
            self.ble_manager.stop()
            event.accept()



if __name__ == "__main__":
    App = QApplication(sys.argv)
    ex = Ui_MainWindow()
    ex.show()
    sys.exit(App.exec_())