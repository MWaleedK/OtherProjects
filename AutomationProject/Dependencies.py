import subprocess
import sys
#run this file only once

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def installAll():
    install('numpy')
    install('opencv-python')
    install('pyqt5')
    install('PIL-Tools')
    install('img2pdf')


if __name__=='__main__':
    installAll()   