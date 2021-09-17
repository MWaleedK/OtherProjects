import pyautogui
from Imtools import Imtools



class Automate:
    def __init__(self):
        self.AssetsList=[]
        printList=[]
        self.auto=pyautogui

    def getAssetsPath(self,path):
        self.AssetsList=Imtools.get_imlist(Imtools,path)

    def doItAll(self,btCount=0):
        print('printing now:'+self.AssetsList[btCount])
        #myFiles=self.getAssetsPath('ToBePrinted')
        print(self.auto.locateCenterOnScreen(self.AssetsList[btCount]))
        

