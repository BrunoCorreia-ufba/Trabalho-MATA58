import sys
from PyQt5 import QtTest
from PyQt5.QtCore import Qt, QTime, QSize
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QIcon, QBrush, QPalette
from escalonator import Escalonator
import time

class Window_Gantt(QWidget):
    def __init__(self, n, cpu, escalonator, io, processes, SOWindow):
        super().__init__()
        self.timer = QTime()
        self.SO = SOWindow
        self.tickClock = 0
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(len(processes))
        self.tableWidget.setColumnCount(1)

        nameMem = QTableWidgetItem()
        nameMem.setText("RAM")

        nameDisk = QTableWidgetItem()
        nameDisk.setText("Disco")

        self.tableMem = QTableWidget()
        self.tableMem.setRowCount(50)
        self.tableMem.setColumnCount(1)
        self.tableMem.setHorizontalHeaderItem(0, nameMem)
        self.tableMem.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.tableDisk = QTableWidget()
        self.tableDisk.setRowCount(len(cpu.disk.memory))
        self.tableDisk.setColumnCount(1)
        self.tableDisk.setHorizontalHeaderItem(0, nameDisk)
        self.tableDisk.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.dicionary = {}
        index = 0
        for i in processes:
            self.dicionary[i.id] = index
            index+=1

        self.setWindowTitle("Gantt")
        self.layout = QVBoxLayout()
        self.tickRun = QPushButton( "Tick", self)
        self.tickRun.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.layout2 = QHBoxLayout()
        self.tickRun.clicked.connect(self.tick)
        self.ticksQuant = QSpinBox()
        self.ticksQuant.setMinimum(1)
        self.ticksQuant.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.AutoTickQuant = QSpinBox()
        self.AutoTickQuant.setMinimum(1)
        self.AutoTickQuant.setMaximum(2000)
        self.AutoTickQuant.setValue(1000)
        self.AutoTickQuant.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.checkAutoTick = QCheckBox("Auto Tick")
        self.checkAutoTick.setChecked(False)
        self.checkAutoTick.stateChanged.connect(self.autoTick)
        self.checkAutoTick.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.Info = QLabel("Algoritmo CPU: " + self.SO.type + "\n Algoritmo Mem: " + self.SO.typeMMU +  "\n Quantum: " + str(self.SO.quantum) + "\n Sobrecarga: "
                           + str(self.SO.override))
        self.Info.setStyleSheet("color: red;")
        self.Info.setAlignment(Qt.AlignCenter)

        self.layout3 = QVBoxLayout()
        labelCheck =  QLabel("Marque para rodar automaticamente")
        self.layout3.addWidget(labelCheck)
        self.layout3.addWidget(self.checkAutoTick)
        C = QWidget()
        C.setLayout(self.layout3)
        self.layout2.addWidget(C)

        self.layout3 = QVBoxLayout()
        labelCheck = QLabel("Tempo em msec para modo automático")
        self.layout3.addWidget(labelCheck)
        self.layout3.addWidget(self.AutoTickQuant)
        D = QWidget()
        D.setLayout(self.layout3)
        self.layout2.addWidget(D)

        self.layout3 = QVBoxLayout()
        self.labelCheck1 = QLabel("Clique para rodar " + str(self.ticksQuant.value()) + " ticks")
        self.layout3.addWidget(self.labelCheck1)
        self.layout3.addWidget(self.tickRun)
        E = QWidget()
        E.setLayout(self.layout3)
        self.layout2.addWidget(E)

        self.layout3 = QVBoxLayout()
        labelCheck = QLabel("Ticks para rodar")
        self.layout3.addWidget(labelCheck)
        self.layout3.addWidget(self.ticksQuant)
        self.ticksQuant.valueChanged.connect(self.ticksQuantUpdate)
        F = QWidget()
        F.setLayout(self.layout3)
        self.layout2.addWidget(F)

        A = QWidget()
        A.setLayout(self.layout2)
        self.layout.addWidget(self.Info)
        self.layout.addWidget(A)
        layoutTables = QHBoxLayout()
        layoutTables.addWidget(self.tableWidget)
        layoutTables.addWidget(self.tableMem)
        layoutTables.addWidget(self.tableDisk)
        B = QWidget()
        B.setLayout(layoutTables)
        self.layout.addWidget(B)
        self.LastLabel = QLabel("Rodando")
        G = QWidget()
        layoutLegenda = QHBoxLayout()
        tableLegenda = QTableWidget()
        tableLegenda.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        tableLegenda.setRowCount(1)
        tableLegenda.setColumnCount(7)

        teste = QTableWidgetItem()
        teste.setText("na lista de IO")
        tableLegenda.setItem(0, 0, QTableWidgetItem())
        tableLegenda.item(0, 0).setBackground(QColor(139,0,0))
        tableLegenda.item(0, 0).setFlags(Qt.NoItemFlags)
        tableLegenda.setHorizontalHeaderItem(0, teste)

        teste1 = QTableWidgetItem()
        teste1.setText("Sobrecarga")
        tableLegenda.setItem(0, 1, QTableWidgetItem())
        tableLegenda.item(0, 1).setBackground(Qt.red)
        tableLegenda.item(0, 1).setFlags(Qt.NoItemFlags)
        tableLegenda.setHorizontalHeaderItem(1, teste1)

        teste2 = QTableWidgetItem()
        teste2.setText("Execução")
        tableLegenda.setItem(0, 2, QTableWidgetItem())
        tableLegenda.item(0, 2).setBackground(Qt.green)
        tableLegenda.item(0, 2).setFlags(Qt.NoItemFlags)
        tableLegenda.setHorizontalHeaderItem(2, teste2)

        teste3 = QTableWidgetItem()
        teste3.setText("Executando, dead")
        tableLegenda.setItem(0, 3, QTableWidgetItem())
        tableLegenda.item(0, 3).setBackground(QColor(0,100,0))
        tableLegenda.item(0, 3).setFlags(Qt.NoItemFlags)
        tableLegenda.setHorizontalHeaderItem(3, teste3)

        teste4 = QTableWidgetItem()
        teste4.setText("Em prontos")
        tableLegenda.setItem(0, 4, QTableWidgetItem())
        tableLegenda.item(0, 4).setBackground(Qt.yellow)
        tableLegenda.item(0, 4).setFlags(Qt.NoItemFlags)
        tableLegenda.setHorizontalHeaderItem(4, teste4)

        teste5 = QTableWidgetItem()
        teste5.setText("Em prontos, dead")
        tableLegenda.setItem(0, 5, QTableWidgetItem())
        tableLegenda.item(0, 5).setBackground(QColor(189,183,107))
        tableLegenda.item(0, 5).setFlags(Qt.NoItemFlags)
        tableLegenda.setHorizontalHeaderItem(5, teste5)

        teste6 = QTableWidgetItem()
        teste6.setText("Não começou/ Acabou")
        tableLegenda.setItem(0, 6, QTableWidgetItem())
        tableLegenda.item(0, 6).setBackground(Qt.gray)
        tableLegenda.item(0, 6).setFlags(Qt.NoItemFlags)
        tableLegenda.setColumnWidth(6, 240)
        tableLegenda.setHorizontalHeaderItem(6, teste6)

        self.tableDisk.setColumnWidth(0, 100)
        self.tableDisk.setFixedWidth(180)
        self.tableMem.setColumnWidth(0, 100)
        self.tableMem.setFixedWidth(180)

        layoutLegenda.addWidget(tableLegenda)
        G.setLayout(layoutLegenda)
        self.layout.addWidget(G)
        self.layout.addWidget(self.LastLabel)
        self.setGeometry(300, 300, 1400, 1000)
        self.setLayout(self.layout)
        self.setWindowIcon(QIcon('edit-image.png'))
        self.show()

        self.cpu = cpu
        self.escalonator = escalonator
        self.io = io
        self.n = n

    def ticksQuantUpdate(self):
        self.labelCheck1.setText("Clique para rodar " + str(self.ticksQuant.value()) + " ticks")



    def updategantt(self, tick, escalonator, io, cpu):

        for i in range(self.tableWidget.rowCount()):
            self.tableWidget.setItem(i, tick, QTableWidgetItem())
            self.tableWidget.item(i, tick,).setBackground(Qt.gray)
            self.tableWidget.item(i, tick).setFlags(Qt.NoItemFlags)

        for i in escalonator.ready_queue:
            if i.deadline <= 0 and escalonator.algorithm == "EDF":
                self.tableWidget.setItem(self.dicionary[i.id], tick, QTableWidgetItem())
                self.tableWidget.item(self.dicionary[i.id], tick).setBackground(QColor(189,183,107))
                self.tableWidget.item(self.dicionary[i.id], tick).setFlags(Qt.NoItemFlags)
            else:
                self.tableWidget.setItem(self.dicionary[i.id], tick, QTableWidgetItem())
                self.tableWidget.item(self.dicionary[i.id], tick).setBackground(Qt.yellow)
                self.tableWidget.item(self.dicionary[i.id], tick).setFlags(Qt.NoItemFlags)
        for i in io.queue:
            self.tableWidget.setItem(self.dicionary[i.id], tick, QTableWidgetItem())
            self.tableWidget.item(self.dicionary[i.id], tick).setBackground(QColor(139,0,0))
            self.tableWidget.item(self.dicionary[i.id], tick).setFlags(Qt.NoItemFlags)

        if cpu.state == "Executando" or cpu.state == "PreSobrecarga" or cpu.state == "Pronto" :
            if cpu.process.deadline <= 0 and escalonator.algorithm == "EDF":
                self.tableWidget.setItem(self.dicionary[cpu.process.id], tick, QTableWidgetItem())
                self.tableWidget.item(self.dicionary[cpu.process.id], tick).setBackground(QColor(0,100,0))
                self.tableWidget.item(self.dicionary[cpu.process.id], tick).setFlags(Qt.NoItemFlags)
            else:
                self.tableWidget.setItem(self.dicionary[cpu.process.id], tick, QTableWidgetItem())
                self.tableWidget.item(self.dicionary[cpu.process.id], tick).setBackground(Qt.green)
                self.tableWidget.item(self.dicionary[cpu.process.id], tick).setFlags(Qt.NoItemFlags)
        if cpu.state == "PosSobrecarga"  or cpu.state == "Sobrecarga":
            self.tableWidget.setItem(self.dicionary[cpu.process.id], tick, QTableWidgetItem())
            self.tableWidget.item(self.dicionary[cpu.process.id], tick).setBackground(Qt.red)
            self.tableWidget.item(self.dicionary[cpu.process.id], tick).setFlags(Qt.NoItemFlags)
        if self.n != len(self.cpu.concluded_process_time):
            self.tableWidget.setColumnCount(self.tableWidget.columnCount()+1)

    def updateMem(self):

        index = 0
        for i in self.cpu.mmu.vm.mem_ram.queue:
            if self.cpu.mmu.vm.mem_ram.isAllocated(i):
                self.tableMem.setItem(index, 0, QTableWidgetItem())
                self.tableMem.item(index, 0).setBackground(QColor(30,144,255))
                self.tableMem.item(index, 0).setForeground(Qt.yellow)
                self.tableMem.item(index, 0).setTextAlignment(Qt.AlignHCenter)
                self.tableMem.item(index, 0).setText(str(i.num))
                self.tableMem.item(index, 0).setFlags(Qt.NoItemFlags)
            else:
                self.tableMem.setItem(index, 0, QTableWidgetItem())
                self.tableMem.item(index, 0).setBackground(Qt.gray)
                self.tableMem.item(index, 0).setFlags(Qt.NoItemFlags)
            index+=1

    def updateDisk(self):
        index = 0

        for i in self.cpu.disk.memory:
            if i.isAllocated:
                self.tableDisk.setItem(index, 0, QTableWidgetItem())
                self.tableDisk.item(index, 0).setBackground(QColor(30, 144, 255))
                self.tableDisk.item(index, 0).setForeground(Qt.yellow)
                self.tableDisk.item(index, 0).setTextAlignment(Qt.AlignHCenter)
                self.tableDisk.item(index, 0).setText(str(i.proc_id))
                self.tableDisk.item(index, 0).setFlags(Qt.NoItemFlags)
            else:
                self.tableDisk.setItem(index, 0, QTableWidgetItem())
                self.tableDisk.item(index, 0).setBackground(Qt.gray)
                self.tableDisk.item(index, 0).setFlags(Qt.NoItemFlags)
            index += 1



    def tick(self):
        if self.n == len(self.cpu.concluded_process_time):
            self.cpu.mmu.vm.mem_ram.clear()
            self.cpu.mmu.vm.clear()
            if self.ticksQuant.value() > 1:
                self.ticksQuant.setValue(1)
            self.checkAutoTick.setChecked(False)
            turnaround = sum(self.cpu.concluded_process_time) / self.n
            self.LastLabel.setText("TURNAROUND: " + str(turnaround))
            text = " Algoritmo CPU: " + self.SO.type + "\n Algoritmo Mem: " + self.SO.typeMMU +  "\n Quantum: " + str(self.SO.quantum) + "\n Sobrecarga: " + str(self.SO.override) + "\n TURNAROUND: "+ str(turnaround)
            reply = QMessageBox.information(self, 'TERMINOU', text, QMessageBox.Ok)

            return
        self.escalonator.nextProcess()
        self.io.wait_for_resource(self.cpu)
        self.cpu.runClock()

        self.updategantt(self.cpu.clock, self.escalonator, self.io, self.cpu)
        self.updateMem()
        self.updateDisk()
        print(self.cpu.clock)
        self.cpu.clock += 1
        self.tickClock = self.cpu.clock

        if self.ticksQuant.value()>1:
            self.ticksQuant.setValue(self.ticksQuant.value()-1)
            self.tick()

    def autoTick(self):
        while self.checkAutoTick.isChecked():
            self.tick()
            QtTest.QTest.qWait(self.AutoTickQuant.value())


    def closeEvent(self, e):
        self.SO.file_open(True)
        self.SO.show()
        self.close()
