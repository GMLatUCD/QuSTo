#---------------------------------------------------------------------------------------------------------------------------------------------
# QuSTo ver 1.0
# Damon Nguyen, Mandeep Basson
# CREATED: JUNE 2020
# LAST UPDATE: 05/11/2021
#---------------------------------------------------------------------------------------------------------------------------------------------
# Please see the file "README_QuSTo.txt" for both an overview an instructions of how to use this program
# Note: As this code was originally designed with the purpose of analyzing scales of snakes, structures in the code are referred to as "scales."
#---------------------------------------------------------------------------------------------------------------------------------------------
# Import Modules

import csv
import re
import pandas as pd
import numpy as np 
from scipy.signal import argrelmax, argrelmin 
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import scipy as scipy
from scipy.signal.signaltools import residue
import math as mt

# Modules used for debugging 

import cProfile
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
#---------------------------------------------------------------------------------------------------------------------------------------------
# Generate UI
class FileDialog(QtWidgets.QFileDialog):
    def __init__(self, *args, **kwargs):
        QtWidgets.QFileDialog.__init__(self, *args)
        self.setOption(self.DontUseNativeDialog, False)    

    def accept(self):
        super(FileDialog, self).accept()

class Ui_QuSTo(QtWidgets.QWidget):
    def setupUi(self, QuSTo):
        QuSTo.setObjectName("QuSTo")
        QuSTo.resize(1224, 817)
        QuSTo.setWindowFlags(
            QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        font = QtGui.QFont()
        font.setPointSize(10)
        QuSTo.setFont(font)
        self.centralwidget = QtWidgets.QWidget(QuSTo)
        self.centralwidget.setObjectName("centralwidget")
        self.openButton = QtWidgets.QPushButton(self.centralwidget)
        self.openButton.setGeometry(QtCore.QRect(10, 30, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.openButton.setFont(font)
        self.openButton.setObjectName("openButton")
        self.fileBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.fileBrowser.setGeometry(QtCore.QRect(120, 30, 311, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.fileBrowser.setFont(font)
        self.fileBrowser.setObjectName("fileBrowser")
        self.loadButton = QtWidgets.QPushButton(self.centralwidget)
        self.loadButton.setGeometry(QtCore.QRect(10, 80, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.loadButton.setFont(font)
        self.loadButton.setObjectName("loadButton")
        self.flipBox = QtWidgets.QCheckBox(self.centralwidget)
        self.flipBox.setGeometry(QtCore.QRect(120, 70, 61, 61))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setUnderline(True)
        self.flipBox.setFont(font)
        self.flipBox.setObjectName("flipBox")
        self.mainProfile = QtWidgets.QGraphicsView(self.centralwidget)
        self.mainProfile.setGeometry(QtCore.QRect(40, 160, 1141, 341))
        self.mainProfile.setObjectName("mainProfile")
        self.scene = QtWidgets.QGraphicsScene(self.centralwidget)
        self.mainProfile.setScene(self.scene)
        self.mainProfileLabel = QtWidgets.QLabel(self.centralwidget)
        self.mainProfileLabel.setGeometry(QtCore.QRect(40, 140, 1141, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.mainProfileLabel.setFont(font)
        self.mainProfileLabel.setObjectName("mainProfileLabel")
        self.numOfScalesLabel = QtWidgets.QLabel(self.centralwidget)
        self.numOfScalesLabel.setGeometry(QtCore.QRect(500, 110, 131, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.numOfScalesLabel.setFont(font)
        self.numOfScalesLabel.setObjectName("numOfScalesLabel")
        self.numOfScalesBox = QtWidgets.QTextBrowser(self.centralwidget)
        self.numOfScalesBox.setGeometry(QtCore.QRect(640, 100, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.numOfScalesBox.setFont(font)
        self.numOfScalesBox.setObjectName("numOfScalesBox")
        self.scaleLabel = QtWidgets.QLabel(self.centralwidget)
        self.scaleLabel.setGeometry(QtCore.QRect(20, 530, 131, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.scaleLabel.setFont(font)
        self.scaleLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scaleLabel.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scaleLabel.setObjectName("scaleLabel")
        self.fullScale = QtWidgets.QGraphicsView(self.centralwidget)
        self.fullScale.setGeometry(QtCore.QRect(20, 580, 211, 191))
        self.fullScale.setObjectName("fullScale")
        self.scene1 = QtWidgets.QGraphicsScene(self.centralwidget)
        self.fullScale.setScene(self.scene1)
        self.fullScaleLabel = QtWidgets.QLabel(self.centralwidget)
        self.fullScaleLabel.setGeometry(QtCore.QRect(20, 560, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setUnderline(True)
        self.fullScaleLabel.setFont(font)
        self.fullScaleLabel.setObjectName("fullScaleLabel")
        self.halfScale = QtWidgets.QGraphicsView(self.centralwidget)
        self.halfScale.setGeometry(QtCore.QRect(250, 580, 211, 191))
        self.halfScale.setObjectName("halfScale")
        self.scene2 = QtWidgets.QGraphicsScene(self.centralwidget)
        self.halfScale.setScene(self.scene2)
        self.halfScaleLabel = QtWidgets.QLabel(self.centralwidget)
        self.halfScaleLabel.setGeometry(QtCore.QRect(250, 560, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setUnderline(True)
        self.halfScaleLabel.setFont(font)
        self.halfScaleLabel.setObjectName("halfScaleLabel")
        self.scaleBox = QtWidgets.QTextBrowser(self.centralwidget)
        self.scaleBox.setGeometry(QtCore.QRect(150, 520, 41, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.scaleBox.setFont(font)
        self.scaleBox.setObjectName("scaleBox")
        self.scaleDropdown = QtWidgets.QComboBox(self.centralwidget)
        self.scaleDropdown.setGeometry(QtCore.QRect(210, 520, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.scaleDropdown.setFont(font)
        self.scaleDropdown.setObjectName("scaleDropdown")
        self.kurtosisLabel = QtWidgets.QLabel(self.centralwidget)
        self.kurtosisLabel.setGeometry(QtCore.QRect(666, 580, 51, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.kurtosisLabel.setFont(font)
        self.kurtosisLabel.setObjectName("kurtosisLabel")
        self.jump = QtWidgets.QTextBrowser(self.centralwidget)
        self.jump.setGeometry(QtCore.QRect(556, 740, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.jump.setFont(font)
        self.jump.setObjectName("jump")
        self.lengthLabel = QtWidgets.QLabel(self.centralwidget)
        self.lengthLabel.setGeometry(QtCore.QRect(476, 530, 47, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lengthLabel.setFont(font)
        self.lengthLabel.setObjectName("lengthLabel")
        self.height = QtWidgets.QTextBrowser(self.centralwidget)
        self.height.setGeometry(QtCore.QRect(736, 520, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.height.setFont(font)
        self.height.setObjectName("height")
        self.QRCoeffLabel = QtWidgets.QLabel(self.centralwidget)
        self.QRCoeffLabel.setGeometry(QtCore.QRect(476, 630, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.QRCoeffLabel.setFont(font)
        self.QRCoeffLabel.setObjectName("QRCoeffLabel")
        self.skew = QtWidgets.QTextBrowser(self.centralwidget)
        self.skew.setGeometry(QtCore.QRect(556, 570, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.skew.setFont(font)
        self.skew.setObjectName("skew")
        self.length = QtWidgets.QTextBrowser(self.centralwidget)
        self.length.setGeometry(QtCore.QRect(556, 520, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.length.setFont(font)
        self.length.setObjectName("length")
        self.skewLabel = QtWidgets.QLabel(self.centralwidget)
        self.skewLabel.setGeometry(QtCore.QRect(476, 580, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.skewLabel.setFont(font)
        self.skewLabel.setObjectName("skewLabel")
        self.convConst = QtWidgets.QTextBrowser(self.centralwidget)
        self.convConst.setGeometry(QtCore.QRect(556, 690, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.convConst.setFont(font)
        self.convConst.setObjectName("convConst")
        self.QRCoeff = QtWidgets.QTextBrowser(self.centralwidget)
        self.QRCoeff.setGeometry(QtCore.QRect(556, 620, 271, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.QRCoeff.setFont(font)
        self.QRCoeff.setObjectName("QRCoeff")
        self.kurtosis = QtWidgets.QTextBrowser(self.centralwidget)
        self.kurtosis.setGeometry(QtCore.QRect(736, 570, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.kurtosis.setFont(font)
        self.kurtosis.setObjectName("kurtosis")
        self.R2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.R2.setGeometry(QtCore.QRect(736, 690, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.R2.setFont(font)
        self.R2.setObjectName("R2")
        self.jumpLabel = QtWidgets.QLabel(self.centralwidget)
        self.jumpLabel.setGeometry(QtCore.QRect(476, 750, 47, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.jumpLabel.setFont(font)
        self.jumpLabel.setObjectName("jumpLabel")
        self.R2Label = QtWidgets.QLabel(self.centralwidget)
        self.R2Label.setGeometry(QtCore.QRect(676, 700, 47, 13))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.R2Label.setFont(font)
        self.R2Label.setObjectName("R2Label")
        self.heightLabel = QtWidgets.QLabel(self.centralwidget)
        self.heightLabel.setGeometry(QtCore.QRect(666, 530, 47, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.heightLabel.setFont(font)
        self.heightLabel.setObjectName("heightLabel")
        self.convConstLabel = QtWidgets.QLabel(self.centralwidget)
        self.convConstLabel.setGeometry(QtCore.QRect(476, 700, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.convConstLabel.setFont(font)
        self.convConstLabel.setObjectName("convConstLabel")
        self.table = QtWidgets.QTableWidget(self.centralwidget)
        self.table.setGeometry(QtCore.QRect(840, 520, 361, 191))
        self.table.setObjectName("table")
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.calculateButton = QtWidgets.QPushButton(self.centralwidget)
        self.calculateButton.setGeometry(QtCore.QRect(1040, 90, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.calculateButton.setFont(font)
        self.calculateButton.setObjectName("calculateButton")
        self.jumpRangeLabel = QtWidgets.QLabel(self.centralwidget)
        self.jumpRangeLabel.setGeometry(QtCore.QRect(860, 40, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.jumpRangeLabel.setFont(font)
        self.jumpRangeLabel.setObjectName("jumpRangeLabel")
        self.toLabel = QtWidgets.QLabel(self.centralwidget)
        self.toLabel.setGeometry(QtCore.QRect(1090, 40, 47, 13))
        self.toLabel.setObjectName("toLabel")
        self.jumpTextEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.jumpTextEdit.setGeometry(QtCore.QRect(1010, 30, 71, 31))
        self.jumpTextEdit.setObjectName("jumpTextEdit")
        self.jumpTextEdit2 = QtWidgets.QTextEdit(self.centralwidget)
        self.jumpTextEdit2.setGeometry(QtCore.QRect(1110, 30, 71, 31))
        self.jumpTextEdit2.setObjectName("jumpTextEdit2")
        self.roughness = QtWidgets.QTextBrowser(self.centralwidget)
        self.roughness.setGeometry(QtCore.QRect(350, 80, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.roughness.setFont(font)
        self.roughness.setObjectName("roughness")
        self.roughnessLabel = QtWidgets.QLabel(self.centralwidget)
        self.roughnessLabel.setGeometry(QtCore.QRect(270, 90, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.roughnessLabel.setFont(font)
        self.roughnessLabel.setObjectName("roughnessLabel")
        # Export Scale Button currently turned off (unused)
        # self.exportScaleButton = QtWidgets.QPushButton(self.centralwidget)
        # self.exportScaleButton.setGeometry(QtCore.QRect(680, 740, 151, 31))
        # self.exportScaleButton.setObjectName("exportScaleButton")
        self.exportTableButton = QtWidgets.QPushButton(self.centralwidget)
        self.exportTableButton.setGeometry(QtCore.QRect(1080, 720, 121, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.exportTableButton.setFont(font)
        self.exportTableButton.setObjectName("exportTableButton")
        self.recommendedRangeLabel = QtWidgets.QLabel(self.centralwidget)
        self.recommendedRangeLabel.setGeometry(QtCore.QRect(960, 70, 301, 16))
        self.recommendedRangeLabel.setObjectName("recommendedRangeLabel")
        self.autoSliceButton = QtWidgets.QPushButton(self.centralwidget)
        self.autoSliceButton.setGeometry(QtCore.QRect(480, 30, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.autoSliceButton.setFont(font)
        self.autoSliceButton.setObjectName("autoSliceButton")
        self.sliceOptionsLabel = QtWidgets.QLabel(self.centralwidget)
        self.sliceOptionsLabel.setGeometry(QtCore.QRect(540, 10, 161, 16))
        self.sliceOptionsLabel.setObjectName("sliceOptionsLabel")
        self.loadFileLabel = QtWidgets.QLabel(self.centralwidget)
        self.loadFileLabel.setGeometry(QtCore.QRect(230, 10, 231, 16))
        self.loadFileLabel.setObjectName("loadFileLabel")
        self.calculateLabel = QtWidgets.QLabel(self.centralwidget)
        self.calculateLabel.setGeometry(QtCore.QRect(960, 10, 101, 16))
        self.calculateLabel.setObjectName("calculateLabel")
        self.comingSoonLabel = QtWidgets.QLabel(self.centralwidget)
        self.comingSoonLabel.setGeometry(QtCore.QRect(710, 90, 171, 41))
        self.comingSoonLabel.setObjectName("comingSoonLabel")
        self.selectStructureButton = QtWidgets.QPushButton(self.centralwidget)
        self.selectStructureButton.setGeometry(QtCore.QRect(340, 520, 121, 31))
        self.selectStructureButton.setObjectName("selectStructureButton")
        QuSTo.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(QuSTo)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1224, 21))
        self.menubar.setObjectName("menubar")
        QuSTo.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(QuSTo)
        self.statusbar.setObjectName("statusbar")
        QuSTo.setStatusBar(self.statusbar)
        self.flipNote = QtWidgets.QLabel(self.centralwidget)
        self.flipNote.setGeometry(QtCore.QRect(10, 110, 421, 41))
        self.flipNote.setObjectName("flipNote")
        self.creditNote = QtWidgets.QLabel(self.centralwidget)
        self.creditNote.setGeometry(QtCore.QRect(700, 775, 521, 20))
        self.creditNote.setObjectName("creditNote")
        self.sensTextEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.sensTextEdit.setGeometry(QtCore.QRect(670, 30, 71, 31))
        self.sensTextEdit.setObjectName("sensTextEdit")
        self.sensLabel = QtWidgets.QLabel(self.centralwidget)
        self.sensLabel.setGeometry(QtCore.QRect(600, 30, 61, 16))
        self.sensLabel.setObjectName("sensLabel")
        self.note1 = QtWidgets.QLabel(self.centralwidget)
        self.note1.setGeometry(QtCore.QRect(600, 70, 281, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.note1.setFont(font)
        self.note1.setObjectName("note1")
        self.note2 = QtWidgets.QLabel(self.centralwidget)
        self.note2.setGeometry(QtCore.QRect(600, 80, 191, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.note2.setFont(font)
        self.note2.setObjectName("note2")
        self.recommendedSensitivity = QtWidgets.QLabel(self.centralwidget)
        self.recommendedSensitivity.setGeometry(QtCore.QRect(600, 60, 301, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.recommendedSensitivity.setFont(font)
        self.recommendedSensitivity.setObjectName("recommendedSensitivity")

        self.retranslateUi(QuSTo)
        QtCore.QMetaObject.connectSlotsByName(QuSTo)

    def retranslateUi(self, QuSTo):
        _translate = QtCore.QCoreApplication.translate
        QuSTo.setWindowTitle(_translate("QuSTo", "QuSTo 1.0"))
        self.openButton.setText(_translate("QuSTo", "Open File"))
        self.loadButton.setText(_translate("QuSTo", "Load"))
        self.flipBox.setText(_translate("QuSTo", "Flip"))
        self.mainProfileLabel.setText(_translate("QuSTo", "                                                                                                        Main Profile                                                                                                                                                                                                                                                 "))
        self.numOfScalesLabel.setText(_translate("QuSTo", "Number of Structures:"))
        self.scaleLabel.setText(_translate("QuSTo", "Individual Structure:"))
        self.fullScaleLabel.setText(_translate("QuSTo", "Full Structure"))
        self.halfScaleLabel.setText(_translate("QuSTo", "Half Structure"))
        self.kurtosisLabel.setText(_translate("QuSTo", "Kurtosis:"))
        self.lengthLabel.setText(_translate("QuSTo", "Length:"))
        self.QRCoeffLabel.setText(_translate("QuSTo", "QR Coeffs:"))
        self.skewLabel.setText(_translate("QuSTo", "Skewness:"))
        self.jumpLabel.setText(_translate("QuSTo", "Jump:"))
        self.R2Label.setText(_translate("QuSTo", "R2:"))
        self.heightLabel.setText(_translate("QuSTo", "Height:"))
        self.convConstLabel.setText(_translate("QuSTo", "Conv Const:"))
        self.calculateButton.setText(_translate("QuSTo", "Calculate"))
        self.jumpRangeLabel.setText(_translate("QuSTo", "Acceptable Jump Range:"))
        self.toLabel.setText(_translate("QuSTo", "to"))
        self.jumpTextEdit.setHtml(_translate("QuSTo", "0"))
        self.jumpTextEdit2.setHtml(_translate("QuSTo", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"0.3"))
        self.roughnessLabel.setText(_translate("QuSTo", "Roughness:"))
        # self.exportScaleButton.setText(_translate("QuSTo", "Export Structure Data"))
        self.exportTableButton.setText(_translate("QuSTo", "Export Table"))
        self.recommendedRangeLabel.setText(_translate("QuSTo", "(Recommended Jump Range: 0 to 0.3)"))
        self.autoSliceButton.setText(_translate("QuSTo", "Auto"))
        self.sliceOptionsLabel.setText(_translate("QuSTo", "2) Structure Slice Options"))
        self.loadFileLabel.setText(_translate("QuSTo", "1) Load a File"))
        self.calculateLabel.setText(_translate("QuSTo", "3) Calculate"))
        self.comingSoonLabel.setText(_translate("QuSTo", "Custom Option Coming Soon"))
        self.selectStructureButton.setText(_translate("QuSTo", "Select Structure"))
        self.flipNote.setText(_translate("QuSTo", "(The left side of a structure is used to calculate the convexity constant)"))
        self.creditNote.setText(_translate("QuSTo", "Ver. 1.0    Created by UCD Granular Materials Lab; Damon Nguyen and Mandeep Basson"))
        self.sensTextEdit.setHtml(_translate("QuSTo", "1.5"))
        self.sensLabel.setText(_translate("QuSTo", "Sensitivity"))
        self.note1.setText(_translate("QuSTo", "Increase if mult. strucs are grouped together"))
        self.note2.setText(_translate("QuSTo", "Decrease if structs are incomplete"))
        self.recommendedSensitivity.setText(_translate("QuSTo", "(Recommended: 1.5)"))

#---------------------------------------------------------------------------------------------------------------------------------------------
# Click Commands for Buttons

        self.openButton.clicked.connect(self.open)
        self.loadButton.clicked.connect(self.load)
        self.autoSliceButton.clicked.connect(self.autoSlice) 
        self.calculateButton.clicked.connect(self.calculate)
        self.selectStructureButton.clicked.connect(self.getValues)
        self.exportTableButton.clicked.connect(self.handleSave)

#---------------------------------------------------------------------------------------------------------------------------------------------
    # Open Button
    def open(self):
        dialog = FileDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.sourcefileNames = dialog.selectedFiles()
            for i in dialog.selectedFiles():
                self.fileBrowser.setText(i)

#---------------------------------------------------------------------------------------------------------------------------------------------
    # Load Button
    def load(self):

        # Load File
        fileToOpen = self.sourcefileNames[0]
        # Preallocate 'results.'
        results = [] 


        # Open the csv file. Data goes to 'results.'
        with open(fileToOpen) as csvfile: 
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                results.append(row)

        # Construct a data matrix from results. Eliminate the first row ('X um','Z um') and convert string elements to float elements.
        data = np.array(results)
        data = np.delete(data, 0, 0)
        data = data.astype(np.float)

        # Calculate
        # Sepperate the data into two arrays, X and Z
        # Also create a third array, flipZ, which is the Z data in reverse order
        X = data[:,0]
        Z = data[:,1]
        flipZ = np.flip(Z)

        # If the flip box is checked, flipZ will be used. If not, Z is used.
        if self.flipBox.isChecked():
            Z = flipZ
        else:
            Z = Z

        self.X = X
        self.Z = Z

        # Calculate the roughness of the profile
        # Roughness = (1/Length) * [sum of (|zi| * delta xi)]

        # Calculate the length of the profile
        length = X[-1] - X[0]

        # Set up to calculate sum part of the roughness equation
        numPoints = np.size(X)
        currentSum = 0

        # Update current sum (zi * delta xi) for each i
        for i in range(0,numPoints-1):
            currentSum = currentSum + abs(Z[i]) * (X[i+1]-X[i])

        # Calculate roughness
        roughnessValue = currentSum / length

        # Round to 4 digits
        roughnessValue = np.round(roughnessValue, 4) 

        # Place roughness value in the text box
        self.roughness.setText(str(roughnessValue))

        #*****************************************************************************************************************************************
        # Plotting (Main Profile)

        figure = Figure(figsize=(12,3.25))
        axes = figure.gca()
        axes.plot(self.X, self.Z,c='black',lw=2)
        
        canvas = FigureCanvas(figure)
        self.scene.addWidget(canvas)
        self.mainProfile.setScene(self.scene)

        #*****************************************************************************************************************************************
        # Clear stuff in the sepereate scale boxes

        self.scaleBox.setText('')       
        self.jump.setText('')
        self.length.setText('')
        self.height.setText('')
        self.skew.setText('')
        self.kurtosis.setText('')
        self.QRCoeff.setText('')
        self.convConst.setText('')
        self.R2.setText('')

#---------------------------------------------------------------------------------------------------------------------------------------------
    # Auto Slice Button

    def autoSlice(self):

        # Determine Maxima and Minima Points

        # Create indexing array for the X and Z arrays. (Length of X should be equal to length of Z)
        length = np.size(self.Z)
        index = np.arange(0, length-1, 1)

        # Find max and min by comparing points next to each other
        self.Imax = argrelmax(self.Z)
        self.Imin = argrelmin(self.Z)

        # Find flat peaks and valleys. If there is a flat or valley peak, place an extreme point in the center of the flat area.
        # Difference between subsequent elements
        dz = np.diff(self.Z)

        # Indexes where Z does not change
        flats = np.where(dz == 0)
        flats = flats[0]
        numFlats = np.size(flats)

        if numFlats != 0:

            # Find flat area with more than one point (three or four points make up the flat area)
            df = np.diff(flats)
            ldf = np.where(df == 1)
            ldf = ldf[0]
            numRep = np.size(ldf)
            repeats = []
            for i in range(numRep):
                currEl = ldf[i]
                repeats.append(flats[currEl])
            #The number of flat areas = numFlats - repeating points in the flat area
            numFlatAreas = numFlats - numRep

            # Construct an array that contains the points of each flat area
            flatAreas=[]
            # single area
            area = []
            j=0

            for i in range(numFlatAreas):
                # Create a new array strting with a flat point at our current value of j
                area.append(flats[j])
                currFlat = flats[j]
                # If there are repeats, put those flat points into the current area
                while True:
                    if currFlat in repeats:
                        j=j+1
                        currFlat = flats[j]
                        area.append(currFlat)
                    else:
                        break
                # Include the last point of the flat area
                area.append(flats[j]+1)
                j=j+1
                # Put the area into flatAreas
                flatAreas.append(area)
                # Reset area
                area = []

            # Now, for each flat area, check if it is a max or min.
            for i in range(numFlatAreas):
                firstFlat = flatAreas[i][0]
                lastFlat = flatAreas[i][-1]
                lenFlat = np.size(flatAreas[i])
                # Make sure the flat area isn't at the ends of the profile
                if firstFlat != 0:
                    if lastFlat != length - 1:
                        # Max if both points next to flat area are smaller
                        if self.Z[firstFlat] > self.Z[firstFlat - 1]:
                            if self.Z[lastFlat] > self.Z[lastFlat + 1]:
                                # Take point around the center of the flat area
                                mid = mt.ceil(lenFlat/2)-1
                                maxflat = flatAreas[i][mid]
                                # Add this point to the max index array
                                self.Imax = np.append(self.Imax, maxflat)
                                # Resort the array
                                self.Imax = np.sort(self.Imax)
                        # Min if both points next to flat area are larger
                        if self.Z[firstFlat] < self.Z[firstFlat - 1]:
                            if self.Z[lastFlat] < self.Z[lastFlat + 1]:
                                # Take point around the center of the flat area
                                mid = mt.ceil(lenFlat/2)-1
                                minflat = flatAreas[i][mid]
                                # Add this point to the min index array
                                self.Imin = np.append(self.Imin, minflat)
                                # Resort the array
                                self.Imin = np.sort(self.Imin)           

        # Index arrays for extrema points
        self.Imax = index[self.Imax]
        self.Imin = index[self.Imin]

        # Get the number of extrema points in data set
        numMax = np.size(self.Imax)
        numMin = np.size(self.Imin)

        # Make the starting and ending points maxima or minima based of the type of extrema point next to it
        # Example: If the first minima comes before the first maximum, than the first point on the profile is a maximum
        if numMin != 0:
            if self.Imax[0] > self.Imin[0]:
                self.Imax = np.insert(self.Imax, 0, 0)
            else:
                self.Imin = np.insert(self.Imin, 0, 0)

        # Get the number of extrema points in data set
        numMax = np.size(self.Imax)
        numMin = np.size(self.Imin) 

        if numMin != 0:
            if self.Imax[numMax-1] < self.Imin[numMin-1]: 
                self.Imax = np.append(self.Imax, length-1)
            else:
                self.Imin = np.append(self.Imin, length-1)  

        # If there is only one extreme point (profile looks like a parabola), put extrema at the ends
        if numMax == 1:
            self.Imin = np.insert(self.Imin, 0, 0)
            self.Imin = np.append(self.Imin, length-1)
        if numMin == 1:
            self.Imax = np.insert(self.Imax, 0, 0)
            self.Imax = np.append(self.Imax, length-1)

        # Update the number of extrema points in the dataset
        numMax = np.size(self.Imax)
        numMin = np.size(self.Imin)

        # Put the extrema points in their own arrays: "self.Zmax" and "self.Zmin"
        self.Zmax = self.Z[self.Imax]
        self.Zmin = self.Z[self.Imin]

        #*****************************************************************************************************************************************
        # Auto-Pick Extrema Points for Scale Separation

        # Upon loading the file, maximum and minimum points will be selected by the program for scale separation to it's best ability. 

        # Surface scans tend to have noise, deteriorations, anomalies, and other distortions in thier profile that will cause maximum or minimum points
        # to appear in the middle of a scale. The goal is to select maximum and minimum points that will be used to divide the profile into full
        # scales. By selecting the "Auto" Slice option, the program will pick maximum and minimum values it thinks is best for scale seperation through
        # the process below. 

        # Important: A scale is defined as starting with a minimum, going to a maximum, and ending with another minimum. 
      
        # If only one scale is present (i.e. one max), ignore this whole process.

        if numMax != 1: 

            # If a maximum comes before a minimum, eliminate it from the Zmax and Imax arrays. This way, we always start with a minimum.
            if self.Imax[0] < self.Imin[0]:
                self.Zmax = np.delete(self.Zmax, 0)
                self.Imax = np.delete(self.Imax, 0)
            
            # Simillarly we always want to end with a minimum point. 
            if self.Imax[-1] > self.Imin[-1]:
                self.Zmax = np.delete(self.Zmax, -1)
                self.Imax = np.delete(self.Imax, -1)

            # Update the number of maximums and minimums
            numMax = np.size(self.Imax)
            numMin = np.size(self.Imin)

            # The next step is to eliminate the maximum and minimum values that could be a result of noise / distortion.

            # There are two types of noise: noise on the way down (from tip of scale to bottom of next scale) and noise on the way up (from bottom of 
            # scale to tip of scale). 

            # The max-min pairs due to noise can be defined by the "Sensitivity" value selected by the user (default = 1.5). To find which pairs are
            # the result of noise, first take the difference between the max and min values. This is the height of the scales. Then, average the 
            # heights. Heights that are less then 1/"the Sensitivity value" of the average value are considered to be the result of noise. 

            # Preallocate dif
            dif = []

            for i in range(0,numMax):
                dif.append(self.Zmax[i] - self.Zmin[i+1])

            avg = np.mean(dif)
            
            # Preallocate a logic matrix that detects the indexes of which heights are less than the average value divided by the sensitivity.
            deleteMax = np.zeros(numMax)
            deleteMin = np.zeros(numMin)
            sensitivity = float(self.sensTextEdit.toPlainText())
            # Find which heights are considered noise.
            for i in range(0,numMax-1):
                if dif[i] < avg/sensitivity: 
                    # Once we find a shorter height, see which pair of max and mins is causing the noise 
                    difLeft = self.Zmax[i]-self.Zmin[i]
                    difRight = self.Zmax[i]-self.Zmin[i+1]
                    if difLeft < difRight:
                        deleteMax[i] = True
                        deleteMin[i] = True
                    else:
                        deleteMax[i] = True 
                        deleteMin[i+1] = True
                else:
                    pass

            # Next, eliminate the min and max pair that makes up the noise-heights. Note that this does not actually alter the shape of the scales at all, 
            # it just refines the points that are considered to be maxes and mins.
            dmax1 = np.where(deleteMax)
            dmax1 = np.array(dmax1)
            dmin1 = np.where(deleteMin)
            dmin1 = np.array(dmin1)
            self.Zmax = np.delete(self.Zmax, dmax1)
            self.Imax = np.delete(self.Imax, dmax1)
            self.Zmin = np.delete(self.Zmin, dmin1)
            self.Imin = np.delete(self.Imin, dmin1)

            # Update the number of maximums and minimums
            numMax = np.size(self.Imax)
            numMin = np.size(self.Imin)

            # Check if there are scales with no max.
            noMax = 0
            for i in range (0,numMin-1):
                if self.Imin[i+1] < self.Imax[i]:
                    noMax = noMax + 1
                    mid = mt.ceil((self.Imin[i] + self.Imin[i+1]) / 2)
                    # Insert a false max
                    self.Imax = np.append(self.Imax, mid)
                    self.Imax = np.sort(self.Imax)

            if noMax != 0:
                self.Zmax = self.Z[self.Imax]

                # Update the number of maximums and minimums
                numMax = np.size(self.Imax)
                numMin = np.size(self.Imin)
                
        #*****************************************************************************************************************************************
        # Scale Sepperation (Make New Arrays for Each Individual Scale)

        # Important: A scale is defined as starting with a minimum, going to a maximum, and ending with another minimum. 

        # Scales are divided by sepperating the full profile into multiple arrays, with each array containing the data of an indivudal scale. 

        # Calculate how many scales are present. This should be equal to the number of maximums currently on the profile.
        self.numScales = numMax

        # First, arrays containing FULL scales are made by taking all the points inbetween two minimums. The first scale is from minimum
        # 0 to minimum 1. The second is from minimum 1 to minimum 2 and so forth. These full scales are used to calculate length, height, 
        # skewness, and kurtosis of individual scales.

        # Preallocate the arrays that contain the data for each full scale
        self.fScaleX = [] # Contains arrays with the X data for each full scale
        self.fScaleZ = [] # Contains arrays with the Z data for each full scale
        
        # Dividing the profile into full scales 
        # If one scale is present, use all the data points

        for i in range (0,self.numScales):
            if self.Imin[i+1] == np.size(index):
                scale = np.arange(index[self.Imin[i]],index[self.Imin[i+1]-1],1)
            else:
                scale = np.arange(index[self.Imin[i]],index[self.Imin[i+1]+1],1)

                self.fScaleX.append(self.X[scale])
                self.fScaleZ.append(self.Z[scale]) 

        self.fScaleX = np.array(self.fScaleX)
        self.fScaleZ = np.array(self.fScaleZ)

        # Next, arrays containing HALF scales are made by taking all the points inbetween a minimum and a maximum. The first scale is from 
        # minimum 0 to maximum 0. The second is from minim 1 to maximum 1 and so forth. These half scales are used to calculate the 
        # "convexity constant" of individual scales

        # Preallocate the arrays that contain the data for each half scale
        self.hScaleX = [] # Contains arrays with the X data for each half scale
        self.hScaleZ = [] # Contains arrays with the Z data for each half scale
        # Dividing the profile into half scales 
        # If one scale is present, use data points from the first minimum to the maximum

        for i in range (0,self.numScales):
            scale = np.arange(index[self.Imin[i]],index[self.Imax[i]],1)
            self.hScaleX.append(self.X[scale])
            self.hScaleZ.append(self.Z[scale])

        self.hScaleX = np.array(self.hScaleX)
        self.hScaleZ = np.array(self.hScaleZ)

        # Report how many scales are present in the UI
        self.numScales = np.size(self.fScaleZ)
        self.numOfScalesBox.setText(str(self.numScales))  

        #*****************************************************************************************************************************************
        # Plotting (Max and Min Points)

        # Color each individual scale. List of colors:
        colors = ['firebrick','midnightblue','darkmagenta','green']
        #colors = ['#762a83','#9970ab','#c2a5cf','#e7d4e8','#d9f0d3','#a6dba0','#5aae61','#1b7837']
        # Save a new list of colors to be used for the sepperated scale figures
        self.scaleColors = []

        # Calculate how many times the color sequence needs to be repeated 
        numColorLoops = mt.ceil(self.numScales/len(colors))
        # Set j to zero. J will be compared to the number of scales on the profile
        j = 0

        # Create an array of colors where the number of colors = the number of scales
        for i in range(numColorLoops):
            self.scaleColors.append(colors[0])
            if self.numScales > j+1:
                self.scaleColors.append(colors[1])
            if self.numScales > j+2:
                self.scaleColors.append(colors[2])
            if self.numScales > j+3:
                self.scaleColors.append(colors[3])
            # Add 4 to j for the next loop
            j = j + 4

        # Set up the plot
        #plt.style.use('dark_background')
        figure = Figure(figsize=(12,3.25))
        axes = figure.gca()
        
        axes.plot(self.X,self.Z,c='black',lw=1.9)

        # Plot w/ colored scales
        for i in range(self.numScales):
            axes.plot(self.fScaleX[i],self.fScaleZ[i],c=str(self.scaleColors[i]),lw=2)

        # Plot max and min points
        axes.plot(self.X[self.Imax], self.Z[self.Imax], "X", c='red') 
        axes.plot(self.X[self.Imin], self.Z[self.Imin], "X", c='orange')
        
        canvas = FigureCanvas(figure)
        self.scene.addWidget(canvas)
        self.mainProfile.setScene(self.scene)

        #*****************************************************************************************************************************************
        # Set Combo Box 1

        # Clear
        self.scaleDropdown.clear()

        # Add
        for i in range (0,self.numScales):
            self.scaleDropdown.addItem(str(i+1))

        self.scaleDropdown.setCurrentIndex(0)
      
#---------------------------------------------------------------------------------------------------------------------------------------------
    # Calculate Button  
    def calculate(self):

        # Calculate Length and Height of Each Indidual Scale
        scaleLengths = [] # Contains lengths of each full scale
        scaleHeights = [] # Contains heights of each full scale

        # The length of each scale is calculated by subtracting the starting X value from the final X value of each scale.

        # Calculating length
        for i in range (0,self.numScales):
            lengths = self.fScaleX[i][-1] - self.fScaleX[i][0]
            scaleLengths.append(lengths)

        scaleLengths = np.array(scaleLengths) 

        # The height of each scale is calculated by first averaging the first and last Z values of each scale (base elevation), and subtracting it
        # from that scale's maximum point (top elevation).

        # Calculating Height
        for i in range (0,self.numScales):
            baseHeight = (self.fScaleZ[i][-1] + self.fScaleZ[i][0]) / 2
            heights = self.Zmax[i] - baseHeight
            scaleHeights.append(heights)

        scaleHeights = np.array(scaleHeights) 

        #*****************************************************************************************************************************************
        # Calculate Skewness and Kurtosis of Each Indidual Scale

        scaleSkewness = [] # Contains Skewness values for each scale
        scaleKurtosis = [] # Contains Kurtosis values for each scale

        # Skewness and Kurtosis are properties of a statistical data set, or one where the frequency of occurence xi happens yi times. In order 
        # to obtain skewness and kurtosis values of significance, the data needs to be altered so that an xi value repeats itself yi times.
        # (For example, if x1 is 5 and y1  is 3, then our new x array contains 3 5's. y is the Z data in this case). By doing this, the data for
        # each scale, which was represented by two arrays ('X' and 'Z'), is now represented by one array (dubbed 'u'). 

        U = [] # Contains the arrays of the scale data transfromed for skewness and kurtosis calculations
        tempScaleZ = np.copy(self.fScaleZ) # Makes new data set containing altered Z data for each scale, tempScaleZ
        posScaleZ = [] # Contains unrounded, positive Z values for each scale. For use in calulating 'jump'. NOT USED FOR SKEW OR KURT.
        multipliers = [] # Will contain the number of times X should be repeated

        # This is accomplished in three steps:

        # 1. First, the profile must be grounded, or, the profile's minimum point is put at Z = 0. To do this, Subtract the lowest negative Z 
        # value from every number in the Z array. If negative Z values are present, this bumps the profile up so that it's minimum value is always zero.
        # If there are no negative Z values, this brings the profile down so that once again, it's minimum values is always zero.

        for i in range (0,self.numScales):
            tempScaleZ[i] = tempScaleZ[i] + -1 * min(tempScaleZ[i])

        # Set aside the positive scales for later use. (Will be used to calculate jump values).
            posScaleZ.append(tempScaleZ[i])

        # 2. Round Z values to a full number. 
            tempScaleZ[i] = np.round(tempScaleZ[i])
            multipliers = tempScaleZ[i].astype(np.int)

        # 3. Construct the new 'u' arrays with repeated X values. 'u' arrays are stored in 'U'. 
            u = np.repeat(self.fScaleX[i],multipliers)
            U.append(u)

        # Now, the skewness and kurtosis of each scale can be calculated by using the newly created 'U' array

        # Calculating Skewness
            s = scipy.stats.skew(U[i])
            scaleSkewness.append(s)

        # Calculating Kurtosis
            # scipy.stats calculates "excess kurtosis" for the kurtosis function. "Excess kurtosis" is the kurtosis value - 3. 
            # So, 3 is added back to each kurtosis value.
            k = scipy.stats.kurtosis(U[i]) + 3
            scaleKurtosis.append(k)

        # Turn posScaleZ to an array for calculating 'jump' values.
        posScaleZ = np.array(posScaleZ)

        #*****************************************************************************************************************************************
        # Calculate the "Convexity Constant" of Each Indidual Scale

        coefficients = [] # Contains arrays with the coefficents of the quadratic regression equation for each scale
        QuadRegEqs = [] # Contains the equations of the quadratic regressions
        scaleR2Values = [] # Contains the R2 value for each scale
        scaleConvConsts = [] # Contains Convexity Constants for each scale

        # First, a quadratic regression is fit over each half scale. Then, the second derivative of the reqression is taken, yielding the 
        # "Convexity Constant". The second derivative of a quadratic function is simply twice the leading coefficent.

        # Get the Coefficents for the quadratic regression equation:
        for i in range (0,self.numScales):
            c = np.polyfit(self.hScaleX[i], self.hScaleZ[i], 2)
            coefficients.append(c)

            # Get the equation of the regression from the coefficents
            p = np.poly1d(coefficients[i])
            QuadRegEqs.append(p)

            # Calculate the R Squared values:
            # R squared is the regression sum of squares (ssreg) divided by the total sum of squares (sstot)

            # zhat: the value when the X value is plugged into the regression equation 
            zhat = p(self.hScaleX[i])
            # zbar: the average of the (real) z values
            zbar = np.sum(self.hScaleZ[i])/len(self.hScaleZ[i])
            # ssreg: the regression sum of squares
            ssreg = np.sum((zhat-zbar)**2)
            # sstot: the total sum of squares
            sstot = np.sum((self.hScaleZ[i] - zbar)**2)
            r2 = (ssreg / sstot)
            scaleR2Values.append(r2)

        # Calculate the Convexity Constant:
            cc = coefficients[i][0] * 2
            scaleConvConsts.append(cc)

        #*****************************************************************************************************************************************
        # Calculate the "Jump" of Each Indidual Scale

        scaleJumpValues = [] # Contains Jump values for each scale

        # The vertical "jump" between the two endpoints is usefull in selecting scales for analysis. The "jump" is the vertical distance between 
        # the two endpoints of a scale divided by the scale's maximum value. The larger this value is, the more the skew and kurtosis of the scale 
        # will be altered. This "jump" value should be compared to a pre-set error range to ensure that the "jump" is not altering the skew and 
        # kurtosis too much. 

        for i in range (0,self.numScales):
            maxZ = max(posScaleZ[i])
            if posScaleZ[i][-1] > posScaleZ[i][0]:
                gap = posScaleZ[i][-1] - posScaleZ[i][0]
            else:
                gap = posScaleZ[i][0] - posScaleZ[i][-1]
            jump = gap / maxZ
            scaleJumpValues.append(jump)

        #*****************************************************************************************************************************************
        # Round Everything

        self.scaleJumpValues = np.round(scaleJumpValues, 5)
        self.scaleLengths = np.round(scaleLengths, 5)
        self.scaleHeights = np.round(scaleHeights, 5)
        self.scaleSkewness = np.round(scaleSkewness, 5)
        self.scaleKurtosis = np.round(scaleKurtosis, 5)
        self.coefficients = coefficients
        self.scaleConvConsts = np.round(scaleConvConsts, 5)
        self.scaleR2Values = np.round(scaleR2Values, 5)

        #*****************************************************************************************************************************************
        # Table Creation

        self.table.setColumnCount(self.numScales) 
        self.table.setRowCount(5) # Length, Height, Skewness, Kurtosis, and Convexity Constant
        
        rowNames = ["Length", "Height", "Skewness", "Kurtosis", "Convexity Constant"]

        for i in range (0,5):
            text = rowNames[i]
            item = QtWidgets.QTableWidgetItem()
            item.setText(text)
            self.table.setVerticalHeaderItem(i, item)

        for i in range (0,self.numScales):
            text = "Scale "
            number = str(i+1)
            fullText = text + number
            item = QtWidgets.QTableWidgetItem()
            item.setText(fullText)
            self.table.setHorizontalHeaderItem(i, item)

        _translate = QtCore.QCoreApplication.translate
        jumpMin = float(self.jumpTextEdit.toPlainText())
        jumpMax = float(self.jumpTextEdit2.toPlainText())

        for i in range (0,self.numScales):

            if self.scaleJumpValues[i] >= jumpMin and self.scaleJumpValues[i] <= jumpMax:

                item = QtWidgets.QTableWidgetItem()
                item.setText(_translate("QuSTo", str(self.scaleLengths[i])))
                self.table.setItem(0, i, item)

                item = QtWidgets.QTableWidgetItem()  
                item.setText(_translate("QuSTo", str(self.scaleHeights[i])))
                self.table.setItem(1, i, item)

                item = QtWidgets.QTableWidgetItem()   
                item.setText(_translate("QuSTo", str(self.scaleSkewness[i])))
                self.table.setItem(2, i, item)

                item = QtWidgets.QTableWidgetItem()  
                item.setText(_translate("QuSTo", str(self.scaleKurtosis[i])))
                self.table.setItem(3, i, item)

                item = QtWidgets.QTableWidgetItem()
                item.setText(_translate("QuSTo", str(self.scaleConvConsts[i])))
                self.table.setItem(4, i, item)

            else:

                item = QtWidgets.QTableWidgetItem()
                item.setText("-")
                self.table.setItem(0, i, item)

                item = QtWidgets.QTableWidgetItem()  
                item.setText("-")
                self.table.setItem(1, i, item)

                item = QtWidgets.QTableWidgetItem()   
                item.setText("-")
                self.table.setItem(2, i, item)

                item = QtWidgets.QTableWidgetItem()  
                item.setText("-")
                self.table.setItem(3, i, item)

                item = QtWidgets.QTableWidgetItem()
                item.setText("-")
                self.table.setItem(4, i, item)         
#--------------------------------------------------------------------------------------------------------------------------------------------- 
    # Select Structure Button   
            
    def getValues(self):
        # Fill in the values to the text boxes based on the scale selected from the dropdown menu
        scale1 = int(self.scaleDropdown.currentText())
        self.scaleBox.setText(str(scale1))       
        self.jump.setText(str(self.scaleJumpValues[scale1-1]))
        self.length.setText(str(self.scaleLengths[scale1-1]))
        self.height.setText(str(self.scaleHeights[scale1-1]))
        self.skew.setText(str(self.scaleSkewness[scale1-1]))
        self.kurtosis.setText(str(self.scaleKurtosis[scale1-1]))
        self.QRCoeff.setText(str(self.coefficients[scale1-1]))
        self.convConst.setText(str(self.scaleConvConsts[scale1-1]))
        self.R2.setText(str(self.scaleR2Values[scale1-1]))

        # Full Scale Plot
        #plt.style.use('dark_background')
        figure = Figure(figsize=(2,1.5))
        axes = figure.gca()
        plt.rc('xtick',labelsize=1)
        plt.rc('ytick',labelsize=1)
        # Plot figure of the full scale. Color is saved when making the full profile after pressing a 'slice' button.
        axes.plot(self.fScaleX[scale1-1], self.fScaleZ[scale1-1],c=self.scaleColors[scale1-1],lw=2)
        canvas = FigureCanvas(figure)
        self.scene1.addWidget(canvas)
        self.fullScale.setScene(self.scene1)

        # Half Scale Plot
        #plt.style.use('dark_background')
        figure = Figure(figsize=(2,1.5))
        axes = figure.gca()
        plt.rc('xtick',labelsize=1)
        plt.rc('ytick',labelsize=1)
        # Plot figure of the half scale. Color is saved when making the full profile after pressing a 'slice' button.
        axes.plot(self.hScaleX[scale1-1], self.hScaleZ[scale1-1],c=self.scaleColors[scale1-1],lw=2)
        canvas = FigureCanvas(figure)
        self.scene2.addWidget(canvas)
        self.halfScale.setScene(self.scene2)

#---------------------------------------------------------------------------------------------------------------------------------------------
# Saving file to csv or txt

    def handleSave(self):
        dialog = FileDialog()

        self.savefileNames,_ = dialog.getSaveFileName(dialog, 'Save File', '', 'csv(*.csv);;txt(*.txt)')

        if self.savefileNames:
            with open(self.savefileNames, 'w', encoding='utf8', newline='') as stream:
                writer = csv.writer(stream)
                
                firstrow=['']
                for i in range(1, self.numScales+1):
                    firstrow.append(str('Scale ')+str(i))
                writer.writerow(firstrow)

                rowname = ['Length','Height','Skewness','Kurtosis','Convexity Constant']
                for row in range(self.table.rowCount()):
                    rowdata = [rowname[row]]
                    for column in range(self.table.columnCount()):
                        item = self.table.item(row, column)
                        if item is not None:
                            rowdata.append(item.text())
                        else:
                            rowdata.append('')
                    writer.writerow(rowdata)

#---------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    QuSTo = QtWidgets.QMainWindow()
    ui = Ui_QuSTo()
    ui.setupUi(QuSTo)
    QuSTo.show()
    sys.exit(app.exec_())

#*********************************************************************************************************************************************
# EoC
#*********************************************************************************************************************************************