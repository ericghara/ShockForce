from matplotlib import animation
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from matplotlib.backends.backend_qt5agg import (FigureCanvas)
from src import ShockForce


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self, Form):
        ##Matplotlib Vars
        self.fig = None
        self.canvas = None
        self.ims = None
        self.FPS = 60
        self.simType = "s"
        # UI Setup Constants
        self.simTypeCBoxDict = {
            "Spring Rate": "s",
            "Spring Preload": "p",
            "Airgap": "a"
        }
        self.simTypeUnitsDict = {
            "s": "kg/mm",
            "p": "cm",
            "a": "cm"
        }
        self.simTypeDefaultValsDict = {
            "s": (0.00, 1.30, 4),
            "p": (0.00, 10.5, 4),
            "a": (0.05, 10.5, 4)
        }  # Format: simType : (B, E, Animation Length (s)
        self.simTypeValMinMax = {
            "s": {"BE" : (0.00, 9.99), "D" : (0,20)},
            "p": {"BE" : (0.00, 10.5), "D" : (0, 20)},
            "a": {"BE" : (0.01, 10.5), "D" : (0, 20)}
        }
        self.Q__init__(Form)

    def Q__init__(self, Form):
        super().__init__()
        self.setCentralWidget(Form)
        self.layout = QtWidgets.QVBoxLayout(Form)
        # hlayout
        self.HLayout = QtWidgets.QHBoxLayout(Form)
        self.HLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.HLayout.setContentsMargins(0, 0, 0, 0)
        self.HLayout.setSpacing(0)
        self.HLayout.setObjectName("HLayout")
        # simTypeCBox
        self.simTypeCBox = QtWidgets.QComboBox(Form)
        #self.simTypeCBox.setSizeAdjustPolicy(0)
        #self.simTypeCBox.resize(self.simTypeCBox.sizeHint())
        #self.simTypeCBox.resize(50, 25)
        self.simTypeCBox.setMaximumSize(QtCore.QSize(125, 30))
        self.simTypeCBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.simTypeCBox.setFrame(True)
        self.simTypeCBox.setObjectName("simTypeCBox")
        for text in [*self.simTypeCBoxDict.keys()]:
            self.simTypeCBox.addItem(text)
        self.simTypeCBox.currentIndexChanged.connect(self.comboBoxLogic)
        # Label text
        self.LEditLabel0 = QtWidgets.QLabel(Form)
        self.LEditLabel0.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.LEditLabel0.setObjectName("LEditLabel1")
        self.HLayout.addWidget(self.LEditLabel0)
        # Input box
        self.LEdit0 = QtWidgets.QLineEdit(Form)
        self.LEdit0.setMaximumSize(QtCore.QSize(50, 30))
        self.LEdit0.setObjectName("lineEdit1")
        self.HLayout.addWidget(self.LEdit0)
        #Unit label
        self.LEditUnit0 = QtWidgets.QLabel(Form)
        self.LEditUnit0.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.LEditUnit0.setObjectName("LEditUnit1")
        self.HLayout.addWidget(self.LEditUnit0)
        self.LEditLabel0.setText("Beginning")
        self.LEditUnit0.setText("UNITS")
        # Loop to make All
        #------>Add me
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.layout.addLayout(self.HLayout)


        self.HLayout.addWidget(self.simTypeCBox)
        self.HLayout.addWidget(self.LEditLabel0)
        self.HLayout.addWidget(self.LEdit0)
        self.HLayout.addWidget(self.LEditUnit0)

        self.setup()

    def comboBoxLogic(self, index):
        dictKey = [*self.simTypeCBoxDict.keys()][index]
        simType = self.simTypeCBoxDict[dictKey]
        #Remove this conditional check once changing sweep feature implemented
        if simType in self.simTypeCBoxDict.values():
            B, E, D = self.simTypeDefaultValsDict[simType]
            fig, ims = self.SimulateWrapper(simType, B, E, D)
        else:
            print('Error comboBoxLogic received unrecognized SimType: "%s' % simType)
            return -1
        self.refreshAnimation(fig, ims)

    def SimulateWrapper(self, simType, B, E, duration):
        step = self.durationLogic(B, E, duration)
        sim = ShockForce.Simulate()
        fig, ims = sim.get_data(simType, B, E, step)
        ims += ims[-2:0:-1]  # Reversed ims minus first and last frame (to allow reflection like loop)
        return fig, ims

    def durationLogic(self, B, E, duration):
        #Returns step size to fit duration based on FPS
        frames = duration*self.FPS
        step = (E-B)/frames
        return step

    def goButtonLogic(self):
        #get combobox value
        #get B
        #get E
        #get duration
        #Check for input errors
        # B < E
        # BED policy from dicts
        #get annotation True/False
        pass

    def refreshAnimation(self,fig, ims):
        try:
            self.layout.removeWidget(self.canvas)  # Removing, then adding is a hack, attempts to refresh didn work
            #self.canvas.deleteLater()  #This is how you should delete the canvas
            self.fig.clf()
            self.fig.canvas.draw_idle()
            self.layout.update()
        except:
            print("Refresh Animation starting up")


        self.fig = fig
        self.ims = ims
        self.canvas = FigureCanvas(self.fig)
        self.layout.insertWidget(0, self.canvas)  # Animation
        self.anim = animation.ArtistAnimation(self.fig, self.ims, interval=10, blit=True)
        self.fig.canvas.draw_idle()


    def setup(self):
        B, E, D =  self.simTypeDefaultValsDict[self.simType]
        fig, ims = self.SimulateWrapper(self.simType, B, E, D)
        self.canvas = FigureCanvas(fig)
        self.refreshAnimation(fig, ims)




if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    app = ApplicationWindow(Form)
    app.show()
    print("x: %d, y: %d" % (app.canvas.x(), app.canvas.y()))
    print(app.canvas.geometry())
    qapp.exec_()
