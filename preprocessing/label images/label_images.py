#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Creating GUI

Author: Syed Sheece Raza Gardezi
Last edited: 22 September 2017
"""
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from utils import *

import xml.etree.cElementTree as ET
from xml.etree import ElementTree
from xml.dom import minidom
import xml.etree.ElementTree as ETIMPORT

import cv2

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.imgWidget = QLabel()

        # self.root = str(QFileDialog.getExistingDirectory(self, "Select Data Directory"))
        self.rootDirectory = 'C:\\Users\\U5752631\\Desktop\\SSRLot'
        ignoreParkinglots = ['BIAR-Akureyri-Flight-School', '30-Years-Of-Great-Victory-Square', 'Borgarfjarðar-College',
                             'Hauptplatz-from-Stadt-Cafe', 'Hiruzen-Bear-Valley-Ski-Area', 'Libra-&-Långnäsvägen',
                             'Lotus-Square', 'Monino-Central Airforce-Museum', 'Nakabiraki-Car-Park',
                             'Place-Centrale-Monthey']

        # self.rootDirectory = 'C:\\Users\\U5752631\\Desktop\\csproj17s2\\artefacts\\preprocessing\\example_video\\video'

        self.listOfPathsOfParkingLots = get_listOfFolders(self.rootDirectory)
        self.currentParkinglotPath = os.path.join(self.rootDirectory, self.listOfPathsOfParkingLots.pop())
        self.listOfPathsOfPicture = get_listOfPictures(self.currentParkinglotPath)
        self.pathToCurrentPicture=''
        self.pathToLastPicture=''
        self.parkinglots=[]
        self.revisionState=True

        self.initUI()

    #define the GUI elements
    def initUI(self):

        # create menu item
        exitAct = QAction(QIcon('images\exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        helpAct = QAction(QIcon('images\exit.png'), '&Help', self)
        helpAct.setShortcut('Ctrl+H')
        helpAct.setStatusTip('Get Help')
        helpAct.triggered.connect(self.showdialog)

        menubar = self.menuBar()

        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)

        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction(helpAct)

        #create tool bar
        exitAct = QAction(QIcon('images\exit.png'), 'Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(qApp.quit)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAct)

        #create grid of widgets
        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(QLineEdit(), 1, 1)

        btn1 = QPushButton("Next Picture", self)
        btn1.clicked.connect(self.buttonClickedNextPicture)
        grid.addWidget(btn1, 0, 1)

        btn1 = QPushButton("Previous Picture", self)
        btn1.clicked.connect(self.buttonClickedPreviousPicture)
        grid.addWidget(btn1, 1, 1)


        btn1 = QPushButton("Next Parking Lot", self)
        btn1.clicked.connect(self.buttonClickedNextParkingLot)
        grid.addWidget(btn1, 2, 1)

        btn1 = QPushButton("Save Progress", self)
        btn1.clicked.connect(self.buttonClickedSaveProgress)
        grid.addWidget(btn1, 3, 1)

        btn1 = QPushButton("Delete Picture", self)
        btn1.clicked.connect(self.buttonClickedDeletePicture)
        grid.addWidget(btn1, 4, 1)

        self.RevisionCheckbox = QCheckBox("Activate Revision")
        self.RevisionCheckbox.setChecked(self.revisionState)
        self.RevisionCheckbox.stateChanged.connect(lambda: self.checkboxUpdateRevisionState(self.RevisionCheckbox))
        grid.addWidget(self.RevisionCheckbox,5,1)

        logOutput = QTextEdit('Click on the parking spot with car in it. Red mean car is present. Green mean its a vacant spot. You can toggle the color by clicking again in the parking spot. Pictures left: '+str(len(self.listOfPathsOfPicture)))
        logOutput.setReadOnly(True)
        # logOutput.setLineWrapMode(QTextEdit.NoWrap)
        font = logOutput.font()
        font.setFamily("Courier")
        font.setPointSize(10)
        grid.addWidget(logOutput, 6, 1, 1, 1, Qt.AlignTop)

        ###Add radio buttons
        # Create an array of radio buttons
        moods = [QRadioButton("Cloudy"), QRadioButton("Rainy"), QRadioButton("Sunny")]
        # Set a radio button to be checked by default
        moods[0].setChecked(True)
        # Radio buttons usually are in a vertical layout
        # Create a button group for radio buttons
        self.mood_button_group = QButtonGroup()
        for i in range(len(moods)):
            # Add each radio button to the button layout
            grid.addWidget(moods[i], 7+i, 1, 1, 1, Qt.AlignTop)

            # Add each radio button to the button group & give it an ID of i
            self.mood_button_group.addButton(moods[i], i)
            # Connect each radio button to a method to run when it's clicked
            moods[i].clicked.connect(self.radio_button_clicked)
        # update picture
        self.imgWidget.setObjectName("imgWidget")
        self.imgWidget.mousePressEvent = self.clickedImage
        self.buttonClickedNextPicture()
        grid.addWidget(self.imgWidget, 0, 0,10,1, Qt.AlignTop)


        centralWidget = QWidget()
        centralWidget.setLayout(grid)
        self.setCentralWidget(centralWidget)

        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon('images\icon.png'))
        self.setWindowTitle('Toolbar')

        self.statusBar().showMessage('Edit Picture')
        self.show()

    def radio_button_clicked(self):
        # print(self.mood_button_group.checkedId())
        return self.mood_button_group.checkedButton().text()

    def buttonClickedPreviousPicture(self):
        print("")

    def buttonClickedNextPicture(self):

        self.pathToCurrentPicture=''
        self.parkinglots=[]
        unlabeledPictureNotFound=True

        if not self.revisionState:
            while unlabeledPictureNotFound and len(self.listOfPathsOfPicture) > 0:

                self.pathToCurrentPicture = self.listOfPathsOfPicture.pop()
                pathOfWireFrame = self.getGenericWireframeForParkingLot(self.pathToCurrentPicture)

                if not os.path.exists(pathOfWireFrame):
                    print('Wireframe Dose not Exist!')
                    sys.exit(0)

                if not os.path.exists(self.getSpecificWireframeForPicture(self.pathToCurrentPicture)):
                    unlabeledPictureNotFound=True



        else:
            PictureNotFound=True
            while PictureNotFound and len(self.listOfPathsOfPicture) > 0:
                self.pathToCurrentPicture = self.listOfPathsOfPicture.pop()
                pathOfWireFrame = self.getSpecificWireframeForPicture(self.pathToCurrentPicture)

                if not os.path.exists(pathOfWireFrame):
                    pathOfWireFrame = self.getGenericWireframeForParkingLot(self.pathToCurrentPicture)

                    if not os.path.exists(pathOfWireFrame):
                        print('Wireframe Dose not Exist!')
                        sys.exit(0)


                if os.path.exists(self.pathToCurrentPicture):
                    PictureNotFound=False

        if os.path.exists(self.pathToCurrentPicture):

            currentframe = cv2.imread(self.pathToCurrentPicture)
            height, width, channels = currentframe.shape
            self.parkinglots = self.import_wireframe_xml(pathOfWireFrame)

            for space in self.parkinglots:
                pts = np.array(space[0], np.int32)
                pts = pts.reshape((-1, 1, 2))
                if space[1]:
                    cv2.polylines(currentframe, [pts], True, (0, 0, 255))
                else:
                    cv2.polylines(currentframe, [pts], True, (0, 255, 0))

            cvRGBImg = cv2.cvtColor(currentframe, cv2.COLOR_BGR2RGB)
            qimg = QImage(cvRGBImg.data, cvRGBImg.shape[1], cvRGBImg.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimg)
            self.imgWidget.setPixmap(pixmap)


        else:
            self.buttonClickedNextParkingLot()
        self.pathToLastPicture=self.pathToCurrentPicture
        self.statusBar().showMessage('Next Picture')

    def checkboxUpdateRevisionState(self, checkbox):
            if checkbox.isChecked() == True:
                self.revisionState= True
            else:
                self.revisionState = False

    def buttonClickedNextParkingLot(self):

        if len(self.listOfPathsOfParkingLots)>0 :
            self.currentParkinglotPath=os.path.join(self.rootDirectory, self.listOfPathsOfParkingLots.pop())
            self.listOfPathsOfPicture=get_listOfPictures(self.currentParkinglotPath)
            self.buttonClickedNextPicture()
            self.statusBar().showMessage('Next Parkinglot')

        else:
            self.statusBar().showMessage('No more parking lots')

    def buttonClickedSaveProgress(self):
        pathForXML=self.pathToCurrentPicture.split('.')[0]+'.xml'
        self.export_wireframe_xml(self.parkinglots, pathForXML)
        self.statusBar().showMessage('Progress Saved')

    def buttonClickedDeletePicture(self):
        if os.path.isfile(self.pathToCurrentPicture):
            os.remove(self.pathToCurrentPicture)
        self.buttonClickedNextPicture()
        self.statusBar().showMessage('Picture Deleted')

    #help box
    def showdialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("This is a message box")
        msg.setInformativeText("This is additional information")
        msg.setWindowTitle("MessageBox demo")
        msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.Ok )
        msg.exec_()

    def clickedImage(self, event):
        ix = event.pos().x()
        iy = event.pos().y()

        #toggle space
        for i in range(len(self.parkinglots)):
            space=self.parkinglots[i][0]
            if point_inside_polygon(ix, iy ,space):
                if self.parkinglots[i][1]:
                    self.parkinglots[i][1]=False
                else:
                    self.parkinglots[i][1]=True

        currentframe = cv2.imread(self.pathToCurrentPicture)

        for space in self.parkinglots:
            pts = np.array(space[0], np.int32)
            pts = pts.reshape((-1, 1, 2))
            if space[1]:
                cv2.polylines(currentframe, [pts], True, (0, 0, 255))
            else:
                cv2.polylines(currentframe, [pts], True, (0, 255, 0))

        cvRGBImg = cv2.cvtColor(currentframe, cv2.COLOR_BGR2RGB)
        qimg = QImage(cvRGBImg.data, cvRGBImg.shape[1], cvRGBImg.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        self.imgWidget.setPixmap(pixmap)

        pathOfWireFrame = self.getSpecificWireframeForPicture(self.pathToCurrentPicture)
        self.export_wireframe_xml(self.parkinglots, pathOfWireFrame)
        self.statusBar().showMessage('Progress Saved')

    def export_wireframe_xml(self,spaces, filepath):
        root = ET.Element("parking", id=spaces[0][2],weather=self.radio_button_clicked())

        for i in range(len(spaces)):
            space = spaces[i]
            spacexmltag = ET.SubElement(root, "space", id=str(i + 1), occupied=str(space[1]))
            contour = ET.SubElement(spacexmltag, "contour")

            for point in space[0]:
                point = ET.SubElement(contour, "point", x=str(point[0]), y=str(point[1]))

        xmlfile = open(filepath, "w")
        xmlfile.write(prettify(root))
        xmlfile.close()


    def import_wireframe_xml(self,filename):
        pathOfRootFolderOfParkinglot=os.path.split(os.path.abspath(filename))[0]
        pathToWireframe=os.path.join(pathOfRootFolderOfParkinglot,'wireframe.xml')
        pathToImageWireframe=filename.split('.')[0]+'.xml'
        parkinglots = []

        #Exact wireframe if it exists else load that generic wireframe
        if os.path.exists(pathToImageWireframe) :

            tree = ET.parse(pathToImageWireframe)
            spaces = tree.getroot()
            # print('name of parkinglot: ',spaces.attrib['id'])
            parkinglotName=spaces.attrib['id']
            for space in spaces:
                # print( space.attrib['id'],space.attrib['occupied'])
                occupied = space.attrib['occupied'] == 'True'
                parkinglot = []
                for point in space.iter('point'):
                    x = int(point.attrib['x'])
                    y = int(point.attrib['y'])
                    parkinglot.append([x, y])
                parkinglots.append([parkinglot,occupied,parkinglotName])

        elif os.path.exists(pathToWireframe):
            parkinglots = []
            tree = ET.parse(pathToWireframe)
            spaces = tree.getroot()
            nameOfParkinglot=spaces.attrib['id']

            for space in spaces:
                    # print( space.attrib['id'],space.attrib['occupied'])
                occupied = space.attrib['occupied'] == 'True'
                parkinglot = []
                for point in space.iter('point'):
                    x = int(point.attrib['x'])
                    y = int(point.attrib['y'])
                    parkinglot.append([x, y])
                parkinglots.append([parkinglot, occupied, nameOfParkinglot])
        else:
            print('Wireframe Dose not Exist!')
            sys.exit(0)

        return parkinglots

    def getGenericWireframeForParkingLot(self, pathToPicture):
        pathForGenericWireframe = os.path.join(os.path.split(pathToPicture)[0], 'wireframe.xml')
        return pathForGenericWireframe

    def getSpecificWireframeForPicture(self, pathToPicture):
        pathForPictureWireframe = pathToPicture.split('.')[0] + '.xml'
        return pathForPictureWireframe

    def keyPressEvent(self, e):

        if e.key() == Qt.Key_Z:
            self.buttonClickedNextPicture()

def main():
  app = QApplication(sys.argv)
  win = Window()
  exit(app.exec_())

if __name__ == '__main__':
    main()