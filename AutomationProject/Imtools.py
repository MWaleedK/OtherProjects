import os 
from PIL import Image
from numpy import *
import sys
from PyQt5.QtWidgets import QApplication
import img2pdf
import numpy as np

class Imtools:
    def __init__(self):
        self.inchtoCm=2.54
        self.dpis=[]

    def get_imlist(self,path):
        return [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.jpg')]

    def imresize(self,im,sz_x,sz_y):
        img=Image.fromarray(np.uint8(im))
        return array(img.resize([sz_x,sz_y]))

    def getDPI(self,screens=1):
        app=QApplication(sys.argv)
        for screen in range(0,screens):
            scr=app.screens()[screen]
            self.dpis.append(scr.physicalDotsPerInch())
            app.quit()

    def getPixels(self,x, y):
        self.getDPI()
        newX=x*self.dpis[0]/self.inchtoCm
        newY=y*self.dpis[0]/self.inchtoCm
        return int(newX),int(newY)

    def toPdf(self,imgPath,newNameWithPath):
        image=Image.open(imgPath)
        pdf_bytes=img2pdf.convert(image.filename)
        file=open(newNameWithPath,"wb")
        file.write(pdf_bytes)
        image.close()
        file.close()

    
