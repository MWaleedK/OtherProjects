from PyQt5.QtWidgets import QApplication
from GUI import ImgPicker
import sys,os


if __name__=='__main__':
    app=QApplication(sys.argv)
    imgpicker=ImgPicker()
    imgpicker.show()
    sys.exit(app.exec_())
    


        

    
    
    


    