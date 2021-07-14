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
        self.setWindowTitle("ShockForce")
        self.setWindowIcon(QtGui.QIcon("ui/img/icon.png"))
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
        #self.HLayout.setContentsMargins(0, 0, 0, 0)
        self.HLayout.setSpacing(2)
        self.HLayout.setObjectName("HLayout")
        self.layout.addLayout(self.HLayout)
        # simTypeLabel
        self.simTypelabel = QtWidgets.QLabel(Form)
        self.simTypelabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.simTypelabel.setText("Simulation Type:")
        self.HLayout.addWidget(self.simTypelabel)
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
        self.HLayout.addWidget(self.simTypeCBox)
        for text in [*Logic.simTypeCBoxDict.keys()]:
            self.simTypeCBox.addItem(text)
        self.simTypeCBox.currentIndexChanged.connect(lambda i: Logic.comboBoxLogic(self, i))
        # Stretch 0
        self.HLayout.addStretch(3)
        # Labels, LEdit box, units
        self.LEditDict = {"labels": ("Smallest:", "Largest:", "Animation Length:"),
                          "labelWidgets": [],
                          "LEditWidgets": [],
                          "unitWidgets": []
                          }
        for l in self.LEditDict["labels"]:
            label = QtWidgets.QLabel(Form)
            label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
            label.setMaximumSize(QtCore.QSize(120, 30))
            self.HLayout.addWidget(label)
            self.LEditDict["labelWidgets"].append(label)
            LEdit = QtWidgets.QLineEdit(Form)
            LEdit.setMaximumSize(QtCore.QSize(50, 30))
            LEdit.setAlignment(QtCore.Qt.AlignRight)
            self.HLayout.addWidget(LEdit)
            self.LEditDict["LEditWidgets"].append(LEdit)
            unit = QtWidgets.QLabel(Form)
            unit.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            unit.setMaximumSize(50,30)
            self.HLayout.addWidget(unit)
            self.LEditDict["unitWidgets"].append(unit)
            # Stretch 1: Between LEdit groups
            self.HLayout.addStretch(2)
        #stretch 2
        self.HLayout.addStretch(2)
        # Annotations?
        self.annotCkBox = QtWidgets.QCheckBox(Form)
        self.annotCkBox.setObjectName("annotCkBox")
        self.annotCkBox.setText("Annotations")
        self.HLayout.addWidget(self.annotCkBox)
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

    def refreshInputs(self, simType=False):
        if simType in Logic.simTypeDefaultValsDict.keys() :
            defaultVals = list(Logic.simTypeDefaultValsDict[simType])
            validatorRules = Logic.simTypeValMinMax[simType].values()
            AnnotationsState = defaultVals.pop() # This isn't super clean: default vals includes annotations state but has no min_,max_ or text so can't include in loop below
            self.annotCkBox.setChecked(AnnotationsState)
            widgets = self.LEditDict["LEditWidgets"]
            for (min_, max_), t, w in zip(validatorRules, defaultVals, widgets): #(validator min max), LEdit default text, LEdit widget
                validator = QtGui.QDoubleValidator(min_, max_, 2, notation=0)  # notation 0 sets to standard vs sci notation
                w.setValidator(validator)
                t = str(round(t,2))
                w.setText(t)
        elif simType == False:
            pass
        else:
            print("Error - refreshLEdits: unrecognized simType: %s" % str(simType))

    def LEditSetError(self, setError, index0, index1=None):
        widgets = [self.LEditDict["LEditWidgets"][index0]]
        args = [index0] #arguments to be passed onto LEditClearError
        if index1 != None: # this is for B > E scenarios where need to highlight both B and E
            args.append(index1)
            widgets.append(self.LEditDict["LEditWidgets"][index1])
        args.insert(0, False) # this adds setError argument so when this function is called it knows to clear the error
        if setError == True:
            for w in widgets:
                w.setStyleSheet("background-color: pink;")
                w.textChanged.connect(lambda: self.LEditSetError(*args))
        elif setError == False:
            for w in widgets:
                w.setStyleSheet("background-color: white;")
                w.disconnect() # remember to disconnect from textChanged.connect

    def annotationsCKState(self):
        state = self.annotCkBox.isChecked() #Returns True/False
        return state


    def goButtonClick(self):
        #Get text from LEdits
        simParams = [] #B, E, D
        widgets = self.LEditDict["LEditWidgets"]
        for w in widgets:
            validator = w.validator()
            val = (w.text())
            state, value, pos = validator.validate(val, 0) #value is return by validator but we aren't using,  pos is also return, unused by validator, unsure what it does
            if state != QtGui.QValidator.Acceptable:
                index = widgets.index(w)
                self.LEditSetError(True, index)
                return False
            val = float(val)
            simParams.append(val)
        B, E, D = simParams
        if B >= E:
            labels = self.LEditDict["labels"]
            indexB, indexE =  labels.index("Beginning:"), labels.index("End:")
            self.LEditSetError(True,indexB,indexE)
            return False
        annotations = self.annotationsCKState()
        fig, ims = Logic.SimulateWrapper(B, E, D, annotations)
        self.refreshAnimation(fig,ims)
        return True

    def setup(self):
        simType = Logic.simType
        self.refreshComboBox(simType)
        self.refreshLabels()
        self.refreshInputs(simType)
        self.goButtonClick()

if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    app = ApplicationWindow(Form)
    app.show()
    qapp.exec_()
