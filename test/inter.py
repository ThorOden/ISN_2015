# Créé par levyfalk, le 16/03/2015 en Python 3.2
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file
#
# Created: Thu Jun 13 20:47:12 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(333, 285)
        Form.setMouseTracking(True)
        self.labelImage = QtGui.QLabel(Form)
        self.labelImage.setGeometry(QtCore.QRect(5, 10, 320, 240))
        self.labelImage.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.labelImage.setText(_fromUtf8(""))
        self.labelImage.setObjectName(_fromUtf8("labelImage"))
        self.pushButtonEffacer = QtGui.QPushButton(Form)
        self.pushButtonEffacer.setGeometry(QtCore.QRect(5, 255, 85, 27))
        self.pushButtonEffacer.setObjectName(_fromUtf8("pushButtonEffacer"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Pyqt : Clic souris dessine pixel", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonEffacer.setText(QtGui.QApplication.translate("Form", "Effacer", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
