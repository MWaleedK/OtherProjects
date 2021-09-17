from numpy.core.fromnumeric import prod
from Imtools import Imtools
from cv2 import cv2 as cv
import numpy as np
import random

class ImProc:
    def __init__(self):
        self.tools=Imtools()
        self.canv_x,self.canv_y=self.tools.getPixels(33,44.8)# Plotter paper size
        self.canvas=np.ones((self.canv_y,self.canv_x,3), np.uint8)*255
        self.offset_x,self.offset_y=self.tools.getPixels(1.5,3)

        self.spacingHeight=0
        self.spacingWidth=0
    
    def setCanvasSize(self,x=33,y=44.8):
        self.canv_x,self.canv_y=self.tools.getPixels(x,y)
        self.canvas=np.ones((self.canv_y,self.canv_x,3), np.uint8)*255
        self.createMarkings()

    def setMargin(self,x=2.5,y=2.5):
        self.offset_x,self.offset_y=self.tools.getPixels(x,y)

    def setInputFile(self,path):
        self.inputPath=cv.imread(path,cv.IMREAD_COLOR)

    def simpleImage(self,x=4,y=4):
        x,y=self.tools.getPixels(x,y)
        newIm=np.array(self.tools.imresize(self.getInputPath(),x,y))
        imgGray=cv.cvtColor(newIm,cv.COLOR_BGR2GRAY)
        ret,thresh=cv.threshold(imgGray,127,255,0)
        contours,_=cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_NONE)
        
        contours = sorted(contours, key=lambda l: cv.contourArea(l), reverse=True)
        #cv.drawContours(newIm,contours,0,(0,0,255),2)
        #newIm2=np.array(self.tools.imresize(newIm,x,y))
        lineIm2=np.ones(newIm.shape,dtype=np.uint8)*255
        lineIm2=self.drawCountorusDahed(contours,lineIm2,0,x,y)
        #lineIm2=self.addRoundedRectangleBorder(newIm)
        #cv.drawContours(lineIm2,contours,0,(0,0,255),2)
        self.lineIm=np.array(self.tools.imresize(lineIm2,x,y))
        self.makeCopies(newIm,x,y)
        self.lineIm_X=x
        self.lineIm_Y=y

    def drawCountorusDahed(self,contours,img,contNum=0,x=3,y=3):
        currCont=(contours[contNum])
        contlen=len(currCont)
        newX=contlen/x
        newY=contlen/y
        lineDrawLen = (int)(newX*newY)
        if(lineDrawLen>contlen):
            lineDrawLen=(int)(min(newY,newX)*(lineDrawLen/contlen))
        count=0
        currCont=np.array(currCont)
        drawBool=False
        for i in range(lineDrawLen,currCont.shape[0],lineDrawLen):
                conts=currCont[count:i]
                if(drawBool):
                    cv.drawContours(img,conts,-1,(0,0,255),2)
                    drawBool=False
                else:
                    drawBool=True
                if(count>currCont.shape[0]):
                    count=currCont.shape[0]
                count+=lineDrawLen
        return img
        
    def addRoundedRectangleBorder(self,img2):
        height, width, channels = img2.shape

        border_radius = int(width * 10/100.0)
        line_thickness = int(max(width, height) * 2/100.0)
        edge_shift = int(line_thickness/2.0)

        red = 255 
        green = 0
        blue = 0
        color = (blue, green, red)

        img=np.ones(img2.shape,dtype=np.uint8)*255
        #might need fine tuning in the end

        
        #draw lines
        #top
        cv.line(img, (0, 0), 
        (width, 0), (blue, green, red), line_thickness)
        #bottom
        cv.line(img, (border_radius, height-line_thickness), 
        (width - border_radius, height-line_thickness), (blue, green, red), line_thickness)
        #left
        cv.line(img, (0, 0), 
        (edge_shift, height  - border_radius), (blue, green, red), line_thickness)
        #right
        cv.line(img, (width, 0), 
        (width - line_thickness, height  - border_radius), (blue, green, red), line_thickness)

        #corners
        #cv.ellipse(img, (border_radius+ edge_shift, border_radius+edge_shift), 
        #(border_radius, border_radius), 180, 0, 90, color, line_thickness)
        #cv.ellipse(img, (width-(border_radius+line_thickness), border_radius), 
        #(border_radius, border_radius), 270, 0, 90, color, line_thickness)
        cv.ellipse(img, (width-(border_radius+line_thickness), height-(border_radius + line_thickness)), 
        (border_radius, border_radius), 10, 0, 90, color, line_thickness)
        cv.ellipse(img, (border_radius+edge_shift, height-(border_radius + line_thickness)), 
        (border_radius, border_radius), 90, 0, 90, color, line_thickness)
        return img

    def makeCopies(self,newIm,x,y):
        test_col,test_row = self.tools.getPixels(self.spacingWidth,self.spacingHeight)
        mid_x_y=[((self.rowEnd+self.rowStart)/2),((self.colStart+self.colEnd)/2)]
        rowImgs=(int)((mid_x_y[0]-self.rowStart)/y)
        colImgs=(int)((mid_x_y[1]-self.colStart)/x)

        rowSpaceOffset=mid_x_y[0]-(rowImgs-1)*test_row
        colSpaceOffset=mid_x_y[1]-(colImgs-1)*test_col

        rowImgs = (int)((rowSpaceOffset - self.rowStart) / y)
        colImgs = (int)((colSpaceOffset - self.colStart) / x)

        rowStart = (int)(rowSpaceOffset - ((rowImgs) * (y)))
        colStart = int(colSpaceOffset - ((colImgs) * (x)))


        rowImgs=((rowImgs)*2)
        colImgs=((colImgs)*2)
        rowEnd=int(rowSpaceOffset+rowImgs*(y))
        colEnd=int(colSpaceOffset+colImgs*(x))
        print(rowImgs,colImgs)
        totalX=0
        totalY=0
        print('Where it starts from: '+ f'({rowStart},{colStart})')
        '''
        _x=0
        for canv_x in range(rowStart,rowEnd):
            _y=0
            if (_x>=y):
                _x=0
                totalY+=1
            for canv_y in range(colStart,colEnd):
                if(totalX==colImgs):
                    totalX=0
                    break
                if(_y>=x):
                    _y=0
                    totalX+=1
                for i in range(0,3):
                    self.canvas[canv_x][canv_y][i]=newIm[_x][_y][i]
                _y+=1
            if(rowImgs==totalY):
                break
            _x+=1
            '''


        canv_x=rowStart
        _x=0
        while(canv_x < rowEnd):
            canv_y=colStart
            _y=0
            if (_x>=y):
                _x=0
                canv_x+=test_row
                totalY+=1
            if(canv_x>=rowEnd):
                    break
            while (canv_y <colEnd):
                if(totalX==colImgs):
                    totalX=0
                    break
                if(_y>=x):
                    _y=0
                    canv_y+=test_col
                    totalX+=1
                if canv_y>=colEnd:
                        break
                for i in range(0,3):
                    self.canvas[canv_x][canv_y][i]=newIm[_x][_y][i]
                _y+=1
                canv_y+=1
            if(rowImgs==totalY):
                break
            _x+=1
            canv_x+=1

    def arbiter(self,a,b,c):
        if a>=b:
            return c
        else:
            return 1


    def getInputPath(self):
        return self.inputPath
    
    def createMarkings(self, value=True):
        rowStart=self.offset_y+(int(self.canv_y*0.005))
        colStart=self.offset_x+(int(self.canv_x*0.008))
        rowEnd=self.canv_y-self.offset_y-(int(self.canv_y*0.005))
        colEnd=self.canv_x-self.offset_x-(int(self.canv_x*0.008))
        m1=0.008
        m2=0.1
        
        condition_1=rowStart+(int)((m1)*(rowEnd))
        condition_2=(int)(((m2)*(colEnd))+colStart)
        condition_3=colEnd-(int)((((m2)*(colEnd))))
        condition_4=rowStart+(int)((m2)*(rowEnd))
        condition_5=((m1)*(colEnd))+colStart
        condition_6=colEnd-(int)((((m1)*(colEnd))))
        condition_7=rowEnd-(int)((((m2)*(rowEnd))))
        condition_8=colStart+(int)((m2)*(colEnd))
        condition_9=rowEnd-(int)((((m1)*(rowEnd))))

        for i in range(rowStart,rowEnd):
            for j in range(colStart,colEnd):
                if(i<condition_1):
                    if((j<condition_2)  or (j>(condition_3))):
                        if value==True:
                            self.canvas[i][j]=(0,0,0)
                
                elif(i<condition_4):
                    if((j<(condition_5))  or (j>(condition_6))):
                        if value==True:
                            self.canvas[i][j]=(0,0,0)
                
                elif((j<condition_5) or (j>(condition_6))):
                    if((i>(condition_7))):
                        if value==True:
                            self.canvas[i][j]=(0,0,0)

                elif((j<condition_8) or (j>(condition_3))):
                    if((i>(condition_9))):
                        if value==True:
                            self.canvas[i][j]=(0,0,0)
                else:
                    self.canvas[i][j]=(255,255,255)
        print('To start from: '+f'({condition_1},{condition_3})')

        self.rowStart=condition_1
        self.rowEnd=condition_9
        self.colStart=condition_5
        self.colEnd=condition_6

                
        
    
    def cricularCut(self,r=3):
        radius_x,radius_y=self.tools.getPixels(r,r)
        newIm=self.getInputPath()
        center=int(newIm.shape[0]/2),int(newIm.shape[1]/2)
        mask=np.zeros(newIm.shape,dtype=np.uint8)
        cv.circle(mask,center,radius_y,(255,255,255),-1)
        regionOfInterest=cv.bitwise_and(newIm,mask)
        mask = cv.cvtColor(mask, cv.COLOR_BGR2GRAY)
        x,y,w,h = cv.boundingRect(mask)
        result = regionOfInterest[y:y+h,x:x+w]
        mask = mask[y:y+h,x:x+w]
        result[mask==0] = (255,255,255)
        imgGray=mask
        ret,thresh=cv.threshold(imgGray,127,255,0)
        contours,_=cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_NONE)
        
        contours = sorted(contours, key=lambda l: cv.contourArea(l), reverse=True)
        cv.drawContours(result,contours,0,(0,0,255),2)
        lineIm2=np.ones(result.shape,dtype=np.uint8)*255
        #cv.drawContours(lineIm2,contours,0,(0,0,255),2)
        lineIm2=self.drawCountorusDahed(contours,lineIm2,0,x,y)
        newIm2=np.array(self.tools.imresize(result,radius_x,radius_y))
        self.makeCopies(newIm2,radius_x,radius_y)
       
        self.lineIm=np.array(self.tools.imresize(lineIm2,radius_x,radius_y))
        self.lineIm_X=radius_x
        self.lineIm_Y=radius_y
    
    def outlineImage(self,x=4,y=4,kernel=5):
        x,y=self.tools.getPixels(x,y)
        newImg=self.getInputPath()
        kernel = np.ones((kernel,kernel), 'uint8')
        erodedIm=newImg.copy()
        cv.erode(newImg,kernel,erodedIm)
        imgGray=cv.cvtColor(erodedIm,cv.COLOR_BGR2GRAY)
        ret,thresh=cv.threshold(imgGray,127,255,0)
        contours,_=cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_NONE)
        
        contours = sorted(contours, key=lambda l: cv.contourArea(l), reverse=True)
        cv.drawContours(newImg,contours,1,(0,0,255),2)
        newIm2=np.array(self.tools.imresize(newImg,x,y))
        lineIm2=np.ones(newImg.shape,dtype=np.uint8)*255
        lineIm2=self.drawCountorusDahed(contours,lineIm2,1,x,y)
        #cv.drawContours(lineIm2,contours,1,(0,0,255),2)
        self.lineIm=np.array(self.tools.imresize(lineIm2,x,y))
        self.makeCopies(newIm2,x,y)
        self.lineIm_X=x
        self.lineIm_Y=y


    def resetCanvas(self,value=True):
        self.canvas=np.ones((self.canv_y,self.canv_x,3), np.uint8)*255
        self.createMarkings(value)


    def saveImage(self,img,name,ext,pickImg=''):
        newName='toBePrinted/'+name+'.'+ext
        print(newName)
        if(ext=='jpg'):
            cv.imwrite(newName,img)
        else:
            self.tools.toPdf(imgPath=pickImg,newNameWithPath=newName)
        self.resetCanvas(True)
        return newName

                

