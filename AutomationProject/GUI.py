from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLineEdit,QMainWindow, QPushButton, QVBoxLayout, QWidget,QLabel
import sys, os
from PyQt5.QtGui import QPixmap
from Improc import ImProc

class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n Drop Image Here \n\n')
        self.setStyleSheet('''QLabel{border: 4px dashed #aaa} ''')


    def setPixmap(self,image):
        super().setPixmap(image)



class ImgPicker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Atomate CM4')
        self.resize(400,400)
        self.filePath=''
        self.setAcceptDrops(True)
        mainLayout=QVBoxLayout()
        
        self.photoViewer=ImageLabel()
        mainLayout.addWidget(self.photoViewer)
        
        self.setLayout(mainLayout)

    def dragEnterEvent(self,event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self,event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self,event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            filePath=event.mimeData().urls()[0].toLocalFile()
            self.filePath=filePath
            f = open("log.txt", "w")
            f.write(filePath)
            f.close()
            self.setImage(filePath)
            event.accept()
        else:
            event.ignore()
    
    def setImage(self,filePath):
        self.photoViewer.setPixmap(QPixmap(filePath))
    



        