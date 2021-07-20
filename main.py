from matplotlib import animation
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvas
from src import Wrapper

class ApplicationWindow(QtWidgets.QMainWindow):

    def __init__(self, Form):
        super().__init__()
        QtCore.QMetaObject.connectSlotsByName(Form)
        global Logic
        Logic = Wrapper.Wrapper()
        # MainWindow
        self.setWindowTitle("ShockForce")
        self.setWindowIcon(QtGui.QIcon("ui/img/main.png"))
        self.resize(1088, 681)  # MainWindow size on startup
        self.setMinimumSize(895, 579) # determined empirically
        self.font_= QtGui.QFont("Arial", 8, QtGui.QFont.StyleNormal)
        self.setFont(self.font_)
        self.setCentralWidget(Form)
        # Matplotlib Vars
        self.fig = None
        self.ims = None
        # UI Setup Vars
        self.canvas = None
        # parent layout
        self.layout = QtWidgets.QVBoxLayout(Form)
        # hlayout - child layout
        self.HLayout = QtWidgets.QHBoxLayout(Form)
        self.HLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
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
            LEdit.setMaximumSize(QtCore.QSize(40, 30))
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
        self.annotCkBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.HLayout.addWidget(self.annotCkBox)
        # goButton
        self.goButton = QtWidgets.QPushButton(Form)
        self.goButton.setObjectName("goButton")
        self.goButton.clicked.connect(self.goButtonClick)
        self.goButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.HLayout.addWidget(self.goButton)
        self.goButton.setText("Render")
        # saveButton
        self.saveButton = QtWidgets.QPushButton(Form)
        self.saveButton.clicked.connect(lambda: Logic.saveLogic(self, self.fig, self.ims))
        self.saveButton.setIcon(QtGui.QIcon("ui/img/save.png"))
        self.saveButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.HLayout.addWidget(self.saveButton)
        # loadingLabel
        self.loadingLabel = QtWidgets.QLabel()
        self.loadingLabel.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)
        self.loadingLabel.setStyleSheet("""QWidget {background-color: rgb(255, 255, 255);
                                        font-size: 36px;
                                        font-family: "Arial";
                                        padding: 86;
                                        image: url(ui/img/icon.png);
                                        color: rgb(0, 0, 255);
                                        }""")


    def delAnimation(self):
        if self.fig != None: # if true we aren't in startup
            self.canvas.setVisible(False)
            self.layout.removeWidget(self.canvas)  # Removing, then adding is a hack, attempts to refresh didn't work
            Logic.anim._stop()
            self.canvas.deleteLater()  #This is how you should delete the canvas
            self.fig.clf()
            return True
        return False # We're at startup

    def refreshAnimation(self, fig, ims):
        self.canvas = FigureCanvas(fig)
        self.layout.insertWidget(0, self.canvas)  # Animation
        Logic.anim = animation.ArtistAnimation(fig, ims, interval=10, blit=True)
        fig.canvas.draw_idle()
        self.fig = fig
        self.ims = ims

    def delLoadingMessage(self):
        if self.loadingLabel.isVisible():
            self.loadingLabel.setVisible(False)
            self.layout.removeWidget(self.loadingLabel)


    def loadingMessage(self,preset,message=None):
        messageDict = {"r" : "   Rendering...",
                       "s" : "   Saving please stand by..."}
        geo = QtCore.QRect(11, 11, 1066, 600) # default geometry of self.canvas on startup
        if preset in messageDict.keys() and message==None: #: #select preset message
            message = messageDict[preset]
        elif not preset and message: #Custom Message
            if type(message) != str:
                print("Error loadingMessage: loading message type is not a string")
                return False
        else:
            print("Error loadingMessage: unrecognized preset")
            return False
        if self.fig: #Not at startup, get canvas geometry (user may have resized window)
            geo = self.canvas.geometry()
        self.loadingLabel.setText(message)
        self.loadingLabel.setGeometry(geo)
        self.loadingLabel.setVisible(True)
        self.layout.insertWidget(0, self.loadingLabel)
        qapp.processEvents()  # Force qapp to process all events in queue

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
            state, value, pos = validator.validate(val, 0) # value and pos unused but validate returns these too
            if state != QtGui.QValidator.Acceptable: # Aceeptable are fields that got through validator's input mask, but are also invalid
                index = widgets.index(w)
                self.LEditSetError(True, index)
                return False
            val = float(val)
            simParams.append(val)
        B, E, D = simParams
        if B >= E:
            labels = self.LEditDict["labels"]
            indexB, indexE =  labels.index("Smallest:"), labels.index("Largest:")
            self.LEditSetError(True,indexB,indexE)
            return False
        annotations = self.annotationsCKState()
        #print("Rendering Type: %s, B: %d, E: %d, D: %d, Annot: %r." % (Logic.simType, B, E, D, annotations)) # Enable for debug
        print("Rendering")
        self.delAnimation()
        self.loadingMessage("r")
        fig, ims = Logic.SimulateWrapper(B, E, D, annotations)
        self.refreshAnimation(fig,ims)
        self.delLoadingMessage()
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
    app.setup() # prepare MainWindow and render first animation
    qapp.exec_()