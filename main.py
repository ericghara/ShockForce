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
        # Matplotlib Vars
        self.fig = None
        self.ims = None
        # UI Setup Vars
        self.canvas = None
        self.setCentralWidget(Form)
        self.layout = QtWidgets.QVBoxLayout(Form)
        # hlayout
        self.HLayout = QtWidgets.QHBoxLayout(Form)
        self.HLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.HLayout.setContentsMargins(0, 0, 0, 0)
        self.HLayout.setSpacing(0)
        self.HLayout.setObjectName("HLayout")
        self.layout.addLayout(self.HLayout)
        # simTypeCBox
        self.simTypeCBox = QtWidgets.QComboBox(Form)
        #self.simTypeCBox.setSizeAdjustPolicy(0)
        #self.simTypeCBox.resize(self.simTypeCBox.sizeHint())
        #self.simTypeCBox.resize(50, 25)
        self.simTypeCBox.setMaximumSize(QtCore.QSize(125, 30))
        self.simTypeCBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.simTypeCBox.setFrame(True)
        self.simTypeCBox.setObjectName("simTypeCBox")
        self.simTypeCBox.raise_()
        self.HLayout.insertWidget(0, self.simTypeCBox)
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
            LEdit.setAlignment(QtCore.Qt.AlignRight)
            self.HLayout.addWidget(LEdit)
            self.LEditDict["LEditWidgets"].append(LEdit)
            unit = QtWidgets.QLabel(Form)
            unit.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            self.HLayout.addWidget(unit)
            self.LEditDict["unitWidgets"].append(unit)
        # Annotations?
        self.annotCkBox = QtWidgets.QCheckBox(Form)
        self.annotCkBox.setObjectName("annotCkBox")
        self.HLayout.addWidget(self.annotCkBox)
        self.annotCkBox.setText("Annotations")
        # Go Button
        self.goButton = QtWidgets.QPushButton(Form)
        self.goButton.setObjectName("goButton")
        self.goButton.clicked.connect(self.goButtonClick)
        self.HLayout.addWidget(self.goButton)
        self.goButton.setText("Render")
        #
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.setup()

    def refreshAnimation(self, fig, ims):
        if self.fig != None: # if true we aren't in startup
            self.layout.removeWidget(self.canvas)  # Removing, then adding is a hack, attempts to refresh didn't work
            # self.canvas.deleteLater()  #This is how you should delete the canvas
            self.fig.clf()
            self.fig.canvas.draw_idle()
            self.layout.update()
        else:
            print("Refresh Animation starting up")
        self.canvas = FigureCanvas(fig)
        self.layout.insertWidget(0, self.canvas)  # Animation
        Logic.anim = animation.ArtistAnimation(fig, ims, interval=10, blit=True)
        fig.canvas.draw_idle()
        self.fig = fig
        self.ims = ims

    def refreshComboBox(self, simType):
        list = [*Logic.simTypeCBoxDict.values()]
        index = list.index(simType)
        self.simTypeCBox.setCurrentIndex(index)

    def refreshLabels(self):
        # Units
        text = list(Logic.simTypeUnitsDict[Logic.simType])  #returns list of all units required by simType B,E,D
        widgets = self.LEditDict["unitWidgets"]
        if self.fig == None: # first run, perform setup
            # Labels; on setup only
            lText = list(self.LEditDict["labels"])
            text.extend(lText)
            lWidgets = self.LEditDict["labelWidgets"]
            widgets.extend(lWidgets)
        for t, w in zip(text, widgets):
            w.setText(t)

    def refreshLEdits(self, simType=False):
        if simType in Logic.simTypeDefaultValsDict.keys() :
            defaultVals = Logic.simTypeDefaultValsDict[simType]
            for t, w in zip(defaultVals, self.LEditDict["LEditWidgets"]):
                t = str(round(t,2))
                w.setText(t)
        elif simType == False:
            pass
        else:
            print("Error - refreshLEdits: unrecognized simType: %s" % str(simType))

    def goButtonClick(self):
        #Get text from LEdits
        simParams = [] #B, E, D
        for w in self.LEditDict["LEditWidgets"]:
            val = float(w.text())
            simParams.append(val)
        B, E, D = simParams
        fig, ims = Logic.SimulateWrapper(B, E, D)
        self.refreshAnimation(fig,ims)

    def setup(self):
        simType = Logic.simType
        self.refreshComboBox(simType)
        self.refreshLabels()
        self.refreshLEdits(simType)
        self.goButtonClick()

if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    app = ApplicationWindow(Form)
    app.show()
    qapp.exec_()
