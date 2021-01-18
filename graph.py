
import sys
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
 
import pyqtgraph.opengl as gl


class Coordinatograph(QWidget):
    def __init__(self, title:str, xLabel:str, xUnit:str, yLabel:str, yUnit:str):
        super(Coordinatograph, self).__init__()
        self.setFixedSize(300, 150)
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        self.gw = gl.GLViewWidget()
        ## create three grids, add each to the view
        xgrid = gl.GLGridItem()
        ygrid = gl.GLGridItem()
        zgrid = gl.GLGridItem()
        self.gw.addItem(xgrid)
        self.gw.addItem(ygrid)
        self.gw.addItem(zgrid)

        self.pause = False
 
        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.gw)
        self.setLayout(self.v_layout)
 
    def pause_plot(self):
        self.pause = True

    def start_plot(self):
        self.pause = False

    def update_value(self, new_data:float=0, new_target:float=0):
        if self.pause:
            return
        pass
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Coordinatograph('test', 'time', 's', 'value', 'A')
    demo.update_value()
    demo.show()
    sys.exit(app.exec_())