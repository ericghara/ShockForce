# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Qtlayout.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class ApplicationWindow(QtWidgets.QMainWindow):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1112, 700)
        font = QtGui.QFont()
        font.setPointSize(10)
        Form.setFont(font)
        Form.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        Form.setAutoFillBackground(False)
        #Holder for canvas
        self.annimGBox = QtWidgets.QGroupBox(Form)
        self.annimGBox.setGeometry(QtCore.QRect(11, 11, 1090, 624))
        self.annimGBox.setObjectName("annimGBox")
        #Form
        self.Form = QtWidgets.QWidget(Form)
        self.Form.setGeometry(QtCore.QRect(10, 640, 1091, 35))
        self.Form.setObjectName("widget")
        #hlayout for bundles of hlayouts and simTypeCBox
        self.parentHLayout = QtWidgets.QHBoxLayout(self.Form)
        self.parentHLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.parentHLayout.setContentsMargins(0, 0, 0, 0)
        self.parentHLayout.setSpacing(0)
        self.parentHLayout.setObjectName("parentHLayout")
        #simTypeCBox
        self.simTypeCBox = QtWidgets.QComboBox(self.Form)
        self.simTypeCBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.simTypeCBox.setFrame(True)
        self.simTypeCBox.setObjectName("simTypeCBox")
        self.simTypeCBox.addItem("")
        self.simTypeCBox.addItem("")
        self.simTypeCBox.addItem("")
        self.parentHLayout.addWidget(self.simTypeCBox)
        #"Beginning" HLayout
        self.childHLayout0 = QtWidgets.QHBoxLayout()
        self.childHLayout0.setObjectName("horizontalLayout")
        # Label text
        self.LEditLabel0 = QtWidgets.QLabel(self.Form)
        self.LEditLabel0.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.LEditLabel0.setObjectName("LEditLabel1")
        self.childHLayout0.addWidget(self.LEditLabel0)
        # Input box
        self.lineEdit0 = QtWidgets.QLineEdit(self.Form)
        self.lineEdit0.setMaximumSize(QtCore.QSize(50, 30))
        self.lineEdit0.setObjectName("lineEdit1")
        self.childHLayout0.addWidget(self.lineEdit0)
        #Unit label
        self.LEditUnit0 = QtWidgets.QLabel(self.Form)
        self.LEditUnit0.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.LEditUnit0.setObjectName("LEditUnit1")
        self.childHLayout0.addWidget(self.LEditUnit0)
        self.parentHLayout.addLayout(self.childHLayout0)
        # Loop to make All
        #------>Add me
        # Annotations?
        self.annotCkBox = QtWidgets.QCheckBox(self.Form)
        self.annotCkBox.setObjectName("annotCkBox")
        self.parentHLayout.addWidget(self.annotCkBox)
        #Go Button
        self.goButton = QtWidgets.QPushButton(self.Form)
        self.goButton.setObjectName("goButton")
        self.parentHLayout.addWidget(self.goButton)
        self.simTypeCBox.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def setup(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.annimGBox.setTitle(_translate("Form", "Animation"))
        self.simTypeCBox.setItemText(0, _translate("Form", "Spring Rate"))
        self.simTypeCBox.setItemText(1, _translate("Form", "Spring Preload"))
        self.simTypeCBox.setItemText(2, _translate("Form", "Airgap"))
        self.LEditLabel0.setText(_translate("Form", "Beginning"))
        self.LEditUnit0.setText(_translate("Form", "UNITS"))
        self.annotCkBox.setText(_translate("Form", "Annotations"))
        self.goButton.setText(_translate("Form", "Render"))

