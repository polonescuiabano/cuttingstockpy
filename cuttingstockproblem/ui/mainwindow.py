# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.vboxlayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.vboxlayout.setObjectName("vboxlayout")
        self.label_barras_disponiveis = QtWidgets.QLabel(self.centralwidget)
        self.label_barras_disponiveis.setObjectName("label_barras_disponiveis")
        self.vboxlayout.addWidget(self.label_barras_disponiveis)
        self.label_instrucao = QtWidgets.QLabel(self.centralwidget)
        self.label_instrucao.setObjectName("label_instrucao")
        self.vboxlayout.addWidget(self.label_instrucao)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit_tamanho = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_tamanho.setObjectName("lineEdit_tamanho")
        self.horizontalLayout.addWidget(self.lineEdit_tamanho)
        self.lineEdit_quantidade = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_quantidade.setObjectName("lineEdit_quantidade")
        self.horizontalLayout.addWidget(self.lineEdit_quantidade)
        self.btn_adicionar = QtWidgets.QPushButton(self.centralwidget)
        self.btn_adicionar.setObjectName("btn_adicionar")
        self.horizontalLayout.addWidget(self.btn_adicionar)
        self.vboxlayout.addLayout(self.horizontalLayout)
        self.tableWidget_barras_desejadas = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_barras_desejadas.setObjectName("tableWidget_barras_desejadas")
        self.tableWidget_barras_desejadas.setColumnCount(2)
        self.tableWidget_barras_desejadas.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_barras_desejadas.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_barras_desejadas.setHorizontalHeaderItem(1, item)
        self.vboxlayout.addWidget(self.tableWidget_barras_desejadas)
        self.btn_resolver = QtWidgets.QPushButton(self.centralwidget)
        self.btn_resolver.setObjectName("btn_resolver")
        self.vboxlayout.addWidget(self.btn_resolver)
        self.label_barras_digitadas = QtWidgets.QLabel(self.centralwidget)
        self.label_barras_digitadas.setObjectName("label_barras_digitadas")
        self.vboxlayout.addWidget(self.label_barras_digitadas)
        self.label_resultado = QtWidgets.QLabel(self.centralwidget)
        self.label_resultado.setObjectName("label_resultado")
        self.vboxlayout.addWidget(self.label_resultado)
        self.textEdit_combinacoes = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_combinacoes.setObjectName("textEdit_combinacoes")
        self.vboxlayout.addWidget(self.textEdit_combinacoes)
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setObjectName("graphicsView")
        self.vboxlayout.addWidget(self.graphicsView)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Cutting Stock Application"))
        self.label_barras_disponiveis.setText(_translate("MainWindow", "Barras disponíveis: 7, 8, 9, 10, 11, 12, 13, 15 metros"))
        self.label_instrucao.setText(_translate("MainWindow", "Digite os comprimentos das barras:"))
        self.lineEdit_tamanho.setPlaceholderText(_translate("MainWindow", "Comprimento"))
        self.lineEdit_quantidade.setPlaceholderText(_translate("MainWindow", "Quantidade"))
        self.btn_adicionar.setText(_translate("MainWindow", "Adicionar"))
        item = self.tableWidget_barras_desejadas.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Tamanho"))
        item = self.tableWidget_barras_desejadas.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Quantidade"))
        self.btn_resolver.setText(_translate("MainWindow", "Resolver"))
        self.label_barras_digitadas.setText(_translate("MainWindow", "Barras digitadas:"))
        self.label_resultado.setText(_translate("MainWindow", "Melhor combinação:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
