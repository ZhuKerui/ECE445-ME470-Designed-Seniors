
import sys
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from mpii import MPII
 
import pyqtgraph.opengl as gl


class Coordinatograph(QWidget):
    def __init__(self, title:str='', xLabel:str='', xUnit:str='', yLabel:str='', yUnit:str=''):
        super(Coordinatograph, self).__init__()
        self.setFixedSize(641, 481)
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        self.gw = gl.GLViewWidget()
        ## create three grids, add each to the view
        xgrid = gl.GLGridItem()
        xgrid.rotate(90, 0, 1, 0)
        xgrid.translate(-10, 0, 0)
        self.gw.addItem(xgrid)
        ygrid = gl.GLGridItem()
        ygrid.rotate(90, 1, 0, 0)
        ygrid.translate(0, -10, 0)
        self.gw.addItem(ygrid)
        zgrid = gl.GLGridItem()
        zgrid.translate(0,0,-10)
        self.gw.addItem(zgrid)

        self.arm = gl.GLLinePlotItem(color=pg.glColor('r'), width=10., antialias=True)
        self.back = gl.GLLinePlotItem(color=pg.glColor('r'), width=10., antialias=True)
        self.leg = gl.GLLinePlotItem(color=pg.glColor('r'), width=10., antialias=True)
        self.gw.addItem(self.arm)
        self.gw.addItem(self.back)
        self.gw.addItem(self.leg)

        self.pause = False
 
        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.gw)
        self.setLayout(self.v_layout)

        self.arm_edges = np.array([MPII.r_wrist, MPII.r_elbow, MPII.r_shoulder, MPII.neck, MPII.l_shoulder, MPII.l_elbow, MPII.l_wrist], dtype=np.int)
        self.back_edges = np.array([MPII.head, MPII.head, MPII.spine, MPII.pelvis], dtype=np.int)
        self.leg_edges = np.array([MPII.r_ankle, MPII.r_knee, MPII.r_hip, MPII.pelvis, MPII.l_hip, MPII.l_knee, MPII.l_ankle], dtype=np.int)
        
    def pause_plot(self):
        self.pause = True

    def start_plot(self):
        self.pause = False

    def update_value(self, points):
        if self.pause:
            return
        self.arm.setData(pos=points[self.arm_edges])
        self.back.setData(pos=points[self.back_edges])
        self.leg.setData(pos=points[self.leg_edges])
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Coordinatograph('test', 'time', 's', 'value', 'A')
    demo.update_value()
    demo.show()
    sys.exit(app.exec_())