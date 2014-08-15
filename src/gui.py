import PyQt4
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.runText = ""
        self.scriptText = ""
        self.changeText = ""
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(580, 200)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.Run = QtGui.QPushButton(self.centralwidget)
        self.Run.setGeometry(QtCore.QRect(250, 150, 75, 23))
        self.Run.setObjectName(_fromUtf8("Run"))
        self.Script = QtGui.QLabel(self.centralwidget)
        self.Script.setGeometry(QtCore.QRect(70, 10, 46, 13))
        self.Script.setObjectName(_fromUtf8("Script"))
        self.Hosts = QtGui.QLabel(self.centralwidget)
        self.Hosts.setGeometry(QtCore.QRect(270, 10, 46, 13))
        self.Hosts.setObjectName(_fromUtf8("Hosts"))
        self.CHange = QtGui.QLabel(self.centralwidget)
        self.CHange.setGeometry(QtCore.QRect(470, 10, 46, 13))
        self.CHange.setObjectName(_fromUtf8("CHange"))
        self.ScriptLine = QtGui.QLineEdit(self.centralwidget)
        self.ScriptLine.setGeometry(QtCore.QRect(30, 30, 113, 20))
        self.ScriptLine.setObjectName(_fromUtf8("ScriptLine"))
        self.HostLine = QtGui.QLineEdit(self.centralwidget)
        self.HostLine.setGeometry(QtCore.QRect(230, 30, 113, 20))
        self.HostLine.setObjectName(_fromUtf8("HostLine"))
        self.ChangeLine = QtGui.QLineEdit(self.centralwidget)
        self.ChangeLine.setGeometry(QtCore.QRect(430, 30, 113, 20))
        self.ChangeLine.setText(_fromUtf8(""))
        self.ChangeLine.setObjectName(_fromUtf8("ChangeLine"))
        self.Cla = QtGui.QLabel(self.centralwidget)
        self.Cla.setGeometry(QtCore.QRect(260, 80, 211, 16))
        self.Cla.setText(_fromUtf8(""))
        self.Cla.setObjectName(_fromUtf8("Cla"))
        self.Sla = QtGui.QLabel(self.centralwidget)
        self.Sla.setGeometry(QtCore.QRect(260, 100, 211, 16))
        self.Sla.setText(_fromUtf8(""))
        self.Sla.setObjectName(_fromUtf8("Sla"))
        self.Hla = QtGui.QLabel(self.centralwidget)
        self.Hla.setGeometry(QtCore.QRect(260, 120, 201, 16))
        self.Hla.setText(_fromUtf8(""))
        self.Hla.setObjectName(_fromUtf8("Hla"))
        self.Cla_2 = QtGui.QLabel(self.centralwidget)
        self.Cla_2.setGeometry(QtCore.QRect(250, 60, 111, 16))
        self.Cla_2.setObjectName(_fromUtf8("Cla_2"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(210, 100, 46, 13))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(210, 120, 46, 13))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(200, 80, 46, 13))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(30, 80, 113, 20))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.lineEdit_2 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(430, 80, 113, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Wingdings 2"))
        font.setPointSize(1)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setAutoFillBackground(False)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(60, 60, 81, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(460, 60, 46, 13))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.ScriptLine, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.Sla.setText)
        QtCore.QObject.connect(self.HostLine, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.Hla.setText)
        QtCore.QObject.connect(self.ChangeLine, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.Cla.setText)
        QtCore.QObject.connect(self.Run, QtCore.SIGNAL(_fromUtf8("released()")), self.ScriptLine.clear)
        QtCore.QObject.connect(self.Run, QtCore.SIGNAL(_fromUtf8("released()")), self.HostLine.clear)
        QtCore.QObject.connect(self.Run, QtCore.SIGNAL(_fromUtf8("released()")), self.ChangeLine.clear)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.Run.setText(_translate("MainWindow", "Run", None))
        self.Script.setText(_translate("MainWindow", "Script", None))
        self.Hosts.setText(_translate("MainWindow", "Hosts", None))
        self.CHange.setText(_translate("MainWindow", "Change", None))
        self.ScriptLine.setPlaceholderText(_translate("MainWindow", "Enter script file name", None))
        self.HostLine.setPlaceholderText(_translate("MainWindow", "Enter Host file name", None))
        self.ChangeLine.setPlaceholderText(_translate("MainWindow", "Enter Change file name", None))
        self.Cla_2.setText(_translate("MainWindow", "Files to be used:", None))
        self.label.setText(_translate("MainWindow", "Script:", None))
        self.label_2.setText(_translate("MainWindow", "Hosts:", None))
        self.label_3.setText(_translate("MainWindow", "Change:", None))
        self.label_4.setText(_translate("MainWindow", "User Name", None))
        self.label_5.setText(_translate("MainWindow", "Password", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())