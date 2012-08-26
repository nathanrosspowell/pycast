#!/usr/bin/python
import sys
import platform
 
import PySide
from PySide.QtGui import QApplication, QMainWindow, QTextEdit,\
                         QPushButton,  QMessageBox
 
__version__ = '0.0.1'
 
from ui_pycast import Ui_MainWindow
 
class MainWindow( QMainWindow, Ui_MainWindow ):
    def __init__( self, parent = None ):
        super( MainWindow, self ).__init__( parent )
        self.setupUi( self )
       
if __name__ == '__main__':
    app = QApplication( sys.argv )
    frame = MainWindow()
    frame.show()
    app.exec_()
