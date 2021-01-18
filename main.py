
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from camera import Camera_Manager
from graph import Coordinatograph

class Ui_MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        self.timer_camera = QtCore.QTimer()
        self.camera_manager = Camera_Manager()
        self.CAM_NUM = 0
        self.set_ui()
        self.x =0
        self.count = 0

    def set_ui(self):

        # Layout elements setup
        camera_open_button = QtWidgets.QPushButton(u'Camera On')
        close_button = QtWidgets.QPushButton(u'Exit')
        camera_display_label = QtWidgets.QLabel()
        camera_display_label.setFixedSize(641, 481)
        camera_display_label.setAutoFillBackground(False)
        coordinatograph = Coordinatograph('3D Skeleton Display', '', '', '', '')

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(camera_open_button)
        button_layout.addWidget(close_button)

        image_layout = QtWidgets.QHBoxLayout()
        image_layout.addWidget(camera_display_label)
        image_layout.addWidget(coordinatograph)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(image_layout)
        main_layout.addLayout(button_layout)
        
        # Signal connections setup
        def camera_open_button_click():
            if self.timer_camera.isActive() == False:
                flag = self.camera_manager.open(self.CAM_NUM)
                if flag == False:
                    msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"Please check whether the camera is connected to the computer correctly", buttons=QtWidgets.QMessageBox.Ok,
                                                defaultButton=QtWidgets.QMessageBox.Ok)
                else:
                    self.timer_camera.start(30)
                    camera_open_button.setText(u'Camera off')
            else:
                self.timer_camera.stop()
                self.camera_manager.release()
                camera_display_label.clear()
                camera_open_button.setText(u'Camera on')
    
        camera_open_button.clicked.connect(camera_open_button_click)

        def show_camera():
            camera_image = self.camera_manager.get_camera_image()
            showImage = QtGui.QImage(camera_image.data, camera_image.shape[1], camera_image.shape[0], QtGui.QImage.Format_RGB888)
            camera_display_label.setPixmap(QtGui.QPixmap.fromImage(showImage))

        self.timer_camera.timeout.connect(show_camera)
        close_button.clicked.connect(self.close)

        # Launch the layout
        self.setLayout(main_layout)
        self.setWindowTitle(u'Keebot Demo')


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
            event.accept()



if __name__ == "__main__":
    App = QApplication(sys.argv)
    ex = Ui_MainWindow()
    ex.show()
    sys.exit(App.exec_())