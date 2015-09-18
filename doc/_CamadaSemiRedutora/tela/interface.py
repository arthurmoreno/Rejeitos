# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tela.ui'
#
# Created: Sat Nov  2 22:05:06 2013
#      by: PyQt4 UI code generator 4.10.3
#

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

class Ui_Janela(QtGui.QWidget):
    def __init__(self, Janela):
        super(Ui_Janela, self).__init__()
        self.setupUi(Janela)
    
    def setupUi(self, Janela):
        Janela.setObjectName(_fromUtf8("Janela"))
        Janela.setEnabled(True)
        Janela.resize(363, 246)
        self.centralwidget = QtGui.QWidget(Janela)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        
        self.gridLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 341, 201))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        
        self.labelElemento = QtGui.QLabel(self.gridLayoutWidget)
        self.labelElemento.setObjectName(_fromUtf8("labelElemento"))
        self.gridLayout.addWidget(self.labelElemento, 0, 0, 1, 1)
        
        self.comboBoxElemento = QtGui.QComboBox(self.gridLayoutWidget)
        self.comboBoxElemento.setObjectName(_fromUtf8("comboBoxElemento"))
        self.gridLayout.addWidget(self.comboBoxElemento, 0, 1, 1, 1)
        
        self.labelEnergiaFoton = QtGui.QLabel(self.gridLayoutWidget)
        self.labelEnergiaFoton.setObjectName(_fromUtf8("labelEnergiaFoton"))
        self.gridLayout.addWidget(self.labelEnergiaFoton, 1, 0, 1, 1)
        
        self.comboBoxEnergiaFoton = QtGui.QComboBox(self.gridLayoutWidget)
        self.comboBoxEnergiaFoton.setObjectName(_fromUtf8("comboBoxEnergiaFoton"))
        self.gridLayout.addWidget(self.comboBoxEnergiaFoton, 1, 1, 1, 1)
        
        self.labelDoseInicial = QtGui.QLabel(self.gridLayoutWidget)
        self.labelDoseInicial.setObjectName(_fromUtf8("labelDoseInicial"))
        self.gridLayout.addWidget(self.labelDoseInicial, 2, 0, 1, 1)
        
        self.inputDoseInicial = QtGui.QLineEdit(self.gridLayoutWidget)
        self.inputDoseInicial.setObjectName(_fromUtf8("inputDoseInicial"))
        self.gridLayout.addWidget(self.inputDoseInicial, 2, 1, 1, 1)
        
        self.labelEspessura = QtGui.QLabel(self.gridLayoutWidget)
        self.labelEspessura.setObjectName(_fromUtf8("labelEspessura"))
        self.gridLayout.addWidget(self.labelEspessura, 3, 0, 1, 1)
        
        self.inputEspessura = QtGui.QLineEdit(self.gridLayoutWidget)
        self.inputEspessura.setEnabled(True)
        self.inputEspessura.setObjectName(_fromUtf8("inputEspessura"))
        self.gridLayout.addWidget(self.inputEspessura, 3, 1, 1, 1)
        
        self.ok_cancelar = QtGui.QDialogButtonBox(self.gridLayoutWidget)
        self.ok_cancelar.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.ok_cancelar.setObjectName(_fromUtf8("ok_cancelar"))
#        self.ok_cancelar.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.gridLayout.addWidget(self.ok_cancelar, 5, 1, 1, 1)
        
        Janela.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(Janela)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        Janela.setStatusBar(self.statusbar)

        self.retranslateUi(Janela)
        QtCore.QMetaObject.connectSlotsByName(Janela)
        Janela.setTabOrder(self.comboBoxElemento, self.comboBoxEnergiaFoton)
        Janela.setTabOrder(self.comboBoxEnergiaFoton, self.inputDoseInicial)
        Janela.setTabOrder(self.inputDoseInicial, self.inputEspessura)
        Janela.setTabOrder(self.inputEspessura, self.ok_cancelar)
    
    def retranslateUi(self, Janela):
        Janela.setWindowTitle(_translate("Janela", "Programa Feliz", None))
        
        self.labelElemento.setText(_translate("Janela", "Elemento", None))
        self.comboBoxElemento.setToolTip(_translate("Janela", "Escolha o elemento químico", None))
        
        self.labelEnergiaFoton.setText(_translate("Janela", "Energia do Fóton", None))
        self.comboBoxEnergiaFoton.setToolTip(_translate("Janela", "Escolha a energia do fóton em MeV", None))
        
        self.labelDoseInicial.setText(_translate("Janela", "Dose Inicial", None))
        self.inputDoseInicial.setToolTip(_translate("Janela", "Informe a dose inicial em xx", None))
        
        self.labelEspessura.setText(_translate("Janela", "Espessura", None))
        self.inputEspessura.setToolTip(_translate("Janela", "Informe a expessura em cm do material de blindagem", None))
    
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message', "Are you sure to quit?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Janela = QtGui.QMainWindow()
    ui = Ui_Janela(Janela)
#    ui.setupUi(Janela)
    Janela.show()
    sys.exit(app.exec_())