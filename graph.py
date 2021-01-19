
import sys
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
 
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

        self.edges = [[0, 1], [1, 2], [2, 6], [6, 3], [3, 4], [4, 5], 
              [10, 11], [11, 12], [12, 8], [8, 13], [13, 14], [14, 15], 
              [6, 8], [8, 9]]
        self.arm_edges = np.array([10, 11, 12, 8, 13, 14, 15], dtype=np.int)
        self.back_edges = np.array([9, 8, 7, 6], dtype=np.int)
        self.leg_edges = np.array([0, 1, 2, 6, 3, 4, 5], dtype=np.int)
        self.transform_matrix = np.array([[1, 0, 0],
                                          [0, 0,-1],
                                          [0, 1, 0]])
    def pause_plot(self):
        self.pause = True

    def start_plot(self):
        self.pause = False

    def update_value(self, points):
        if self.pause:
            return
        points = np.matmul(points.reshape(-1, 3), self.transform_matrix)
        self.arm.setData(pos=points[self.arm_edges])
        self.back.setData(pos=points[self.back_edges])
        self.leg.setData(pos=points[self.leg_edges])
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Coordinatograph('test', 'time', 's', 'value', 'A')
    demo.update_value()
    demo.show()
    sys.exit(app.exec_())