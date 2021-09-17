from tkinter import*
from Improc import ImProc
from cv2 import cv2 as cv


class Dashboard:
    def __init__(self):
        self.root=Tk()
        self.radioButtonVar=IntVar()
        self.canvasWidth=0
        self.canvasHeight=0
        self.marginWidth=0
        self.marginHeight=0
        self.fileWidth=0
        self.fileHeight=0

    def mainWindow(self):

        frame1=Frame(self.root)
        frame1.pack(side=TOP)
        label_Page_Size=Label(frame1,text='Page Size').pack(padx=12,pady=0, side=LEFT)
        self.pageSize_h=Entry(frame1,width=10)
        self.pageSize_h.pack(padx=5,pady=0,side=LEFT)
        label_pageSize_h=Label(frame1,text='H ').pack(padx=1, pady=0,side=LEFT)
        self.pageSize_w=Entry(frame1,width=10)
        self.pageSize_w.pack(padx=5, pady=0,side=LEFT)
        label_pageSize_w=Label(frame1,text='W ').pack(padx=1, pady=0,side=LEFT)

        frame2=Frame(self.root)
        frame2.pack(side=TOP)
        label_Margin_Size=Label(frame2,text='Margin Size').pack(padx=5,pady=10,side=LEFT)
        self.marginSize_h=Entry(frame2,width=10)
        self.marginSize_h.pack(padx=5,pady=0,side=LEFT)
        label_marginSize_h=Label(frame2,text='H ').pack(padx=1, pady=0,side=LEFT)
        self.marginSize_w=Entry(frame2,width=10)
        self.marginSize_w.pack(padx=5, pady=0,side=LEFT)
        label_marginSize_w=Label(frame2,text='W ').pack(padx=1, pady=0,side=LEFT)

        frame3=Frame(self.root)
        frame3.pack(side=TOP)
        label_file_Size=Label(frame3,text='File Size').pack(padx=15,pady=0,side=LEFT)
        self.fileSize_h=Entry(frame3,width=10)
        self.fileSize_h.pack(padx=5,pady=0,side=LEFT)
        label_fileSize_h=Label(frame3,text='H ').pack(padx=1, pady=0,side=LEFT)
        self.fileSize_w=Entry(frame3,width=10)
        self.fileSize_w.pack(padx=5, pady=0,side=LEFT)
        label_fileSize_w=Label(frame3,text='W ').pack(padx=1, pady=0,side=LEFT)

        frame4=Frame(self.root)
        frame4.pack(side=TOP)
        Radiobutton(frame4,text='Square',variable=self.radioButtonVar,value=1).pack(anchor=W)
        Radiobutton(frame4,text='Circle',variable=self.radioButtonVar,value=2).pack(anchor=W)
        Radiobutton(frame4,text='Outline',variable=self.radioButtonVar,value=3).pack(anchor=W)
        

        frame5=Frame(self.root)
        frame5.pack(side=TOP)
        label_Spacing_Size=Label(frame5,text='Spacing Size').pack(padx=15,pady=0,side=LEFT)
        self.spacingSize_h=Entry(frame5,width=10)
        self.spacingSize_h.pack(padx=5,pady=0,side=LEFT)
        label_spacingSize_h=Label(frame5,text='H ').pack(padx=1, pady=0,side=LEFT)
        self.spacingSize_w=Entry(frame5,width=10)
        self.spacingSize_w.pack(padx=5, pady=0,side=LEFT)
        label_spacingSize_w=Label(frame5,text='W ').pack(padx=1, pady=0,side=LEFT)




        submitButton= Button(self.root,text='Submit',command=self.submitButtonCallback)
        submitButton.pack(padx=0,pady=10,side=BOTTOM)

        self.root.mainloop()

        

    def submitButtonCallback(self):
        'get data from all windows and send it over'
        self.canvasWidth=float(self.pageSize_w.get())
        self.canvasHeight=float(self.pageSize_h.get())
        self.marginWidth=float(self.marginSize_w.get())
        self.marginHeight=float(self.marginSize_h.get())
        self.fileWidth=float(self.fileSize_w.get())
        self.fileHeight=float(self.fileSize_h.get())
        self.spacingHeight=float(self.spacingSize_h.get())
        self.spacingWidth=float(self.spacingSize_w.get())
        if( self.spacingWidth!='' and self.spacingHeight!='' and self.canvasWidth!='' and self.canvasHeight!='' and self.marginWidth!='' and self.marginHeight!='' and self.fileWidth!='' and self.fileHeight!=''):
            improc=ImProc()
            #set sheet Size  
            f = open("log.txt", "r")
            inpImg=f.read()
            print('file name: '+inpImg)
            improc.setInputFile(inpImg)
            # set page size
            improc.setCanvasSize(x=self.canvasWidth,y=self.canvasHeight)
            #setMargin
            improc.setMargin(x=self.marginWidth,y=self.marginHeight)
            improc.spacingHeight = self.spacingHeight
            improc.spacingWidth = self.spacingWidth
            if(self.radioButtonVar.get()==2):
                #img copies made after resizing
                improc.resetCanvas()
                improc.cricularCut(r=self.fileWidth)
                _=improc.saveImage(name=f'Circular_{self.fileWidth}x{self.fileHeight}',img=improc.canvas,ext='jpg')
                improc.makeCopies(newIm=improc.lineIm,x=improc.lineIm_X,y=improc.lineIm_Y)
                _Im=improc.saveImage(name=f'Circular_Diecut{self.fileWidth}x{self.fileHeight}',img=improc.canvas,ext='jpg')
                _=improc.saveImage(name=f'Circular_Diecut{self.fileWidth}x{self.fileHeight}',img=improc.canvas,ext='pdf',pickImg=_Im)
            elif(self.radioButtonVar.get()==3):
                improc.resetCanvas()
                improc.outlineImage(x=self.fileWidth,y=self.fileHeight,kernel=25)
                _=improc.saveImage(name=f'Outline_{self.fileWidth}x{self.fileHeight}',img=improc.canvas,ext='jpg')
                improc.makeCopies(newIm=improc.lineIm,x=improc.lineIm_X,y=improc.lineIm_Y)
                _Im=improc.saveImage(name=f'Outline_Diecut{self.fileWidth}x{self.fileHeight}',img=improc.canvas,ext='jpg')
                _=improc.saveImage(name=f'Outline_Diecut{self.fileWidth}x{self.fileHeight}',img=improc.canvas,ext='pdf',pickImg=_Im)
            else:
                improc.resetCanvas()
                improc.simpleImage(x=self.fileWidth,y=self.fileHeight)
                _=improc.saveImage(name=f'Square_{self.fileWidth}x{self.fileHeight}',img=improc.canvas,ext='jpg')
                improc.makeCopies(newIm=improc.lineIm,x=improc.lineIm_X,y=improc.lineIm_Y)
                _Im=improc.saveImage(name=f'Square_Diecut{self.fileWidth}x{self.fileHeight}',img=improc.canvas,ext='jpg')
                _=improc.saveImage(name=f'Square_Diecut{self.fileWidth}x{self.fileHeight}',img=improc.canvas,ext='pdf',pickImg=_Im)
            #save image with outline adjust kernel value to increase/decrease thickness must be an odd integer
        else:
            print('Enter All Values')


    


if __name__=='__main__':
    
    Db=Dashboard()
    Db.mainWindow()