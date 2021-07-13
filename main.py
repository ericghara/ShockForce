from matplotlib import animation
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from matplotlib.backends.backend_qt5agg import (FigureCanvas)
from src import Wrapper


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self, Form):
        global Logic
        Logic = Wrapper.Wrapper()
        super().__init__()
        ##Matplotlib Vars
        self.fig = None
        self.ims = None
        # UI Setup Constants
        self.canvas = None
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
        for text in [*Logic.simTypeCBoxDict.keys()]:
            self.simTypeCBox.addItem(text)
        self.simTypeCBox.currentIndexChanged.connect(lambda i: Logic.comboBoxLogic(self, i))
        # Labels, LEdit box, units
        self.LEditDict = {"labels": ("Beginning:", "End:", "Animation Length:"),
                          "labelWidgets": [],
                          "LEditWidgets": [],
                          "unitWidgets": []
                          }
        for l in self.LEditDict["labels"]:
            label = QtWidgets.QLabel(Form)
            label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
            self.HLayout.addWidget(label)
            self.LEditDict["labelWidgets"].append(label)
            LEdit = QtWidgets.QLineEdit(Form)
            LEdit.setMaximumSize(QtCore.QSize(50, 30))
            self.HLayout.addWidget(LEdit)
            self.LEditDict["LEditWidgets"].append(LEdit)
            unit = QtWidgets.QLabel(Form)
            unit.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            self.HLayout.addWidget(unit)
            self.LEditDict["unitWidgets"].append(unit)
        """
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
        """
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.layout.addLayout(self.HLayout)
        self.HLayout.insertWidget(0, self.simTypeCBox)
        #self.HLayout.addWidget(self.LEditLabel0)
        #self.HLayout.addWidget(self.LEdit0)
        #self.HLayout.addWidget(self.LEditUnit0)
        self.setup()

    def refreshAnimation(self, fig, ims):
        try:
            self.layout.removeWidget(self.canvas)  # Removing, then adding is a hack, attempts to refresh didn work
            # self.canvas.deleteLater()  #This is how you should delete the canvas
            self.fig.clf()
            self.fig.canvas.draw_idle()
            self.layout.update()
        except:
            print("Refresh Animation starting up")
        self.canvas = FigureCanvas(fig)
        self.layout.insertWidget(0, self.canvas)  # Animation
        Logic.anim = animation.ArtistAnimation(fig, ims, interval=10, blit=True)
        fig.canvas.draw_idle()
        self.fig = fig
        self.ims = ims

    def refreshLabels(self, setup=False):
        units = list(Logic.simTypeUnitsDict[Logic.simType])  #returns list of all units required by simType B,E,D
        uWidgets = self.LEditDict["unitWidgets"]
        if setup == True:
            lText = list(self.LEditDict["labels"])
            units.extend(lText)
            lWidgets = self.LEditDict["labelWidgets"]
            uWidgets.extend(lWidgets)
        for text, widget in zip(units, uWidgets):
            widget.setText(text)

    def setup(self):
        #Note default Logic.simType value sets simType on startup
        B, E, D = Logic.simTypeDefaultValsDict[Logic.simType]
        fig, ims = Logic.SimulateWrapper(Logic.simType, B, E, D)
        self.canvas = FigureCanvas(fig)
        self.refreshAnimation(fig, ims)
        self.refreshLabels(True)

if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    app = ApplicationWindow(Form)
    app.show()
    print("x: %d, y: %d" % (app.canvas.x(), app.canvas.y()))
    print(app.canvas.geometry())
    qapp.exec_()
