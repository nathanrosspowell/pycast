#!/usr/bin/python
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PyCast. Authored by Nathan Ross Powell.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import PySide classes
import sys
from PySide.QtCore import *
from PySide.QtGui import *
 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Create a Qt application
class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        # Create widgets
        self.edit = QLineEdit("Write my name here")
        self.button = QPushButton("Show Greetings")        
        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.button)
        layoutMiddle = QVBoxLayout()
        layoutMiddle.addWidget(self.edit)
        layoutMiddle.addWidget(self.button)
        layoutRight = QVBoxLayout()
        layoutRight.addWidget(self.edit)
        layoutRight.addWidget(self.button)
        layoutMaster = QVBoxLayout()
        layoutMaster.addWidget( layout )
        layoutMaster.addWidget( layoutMiddle )
        layoutMiddle.addWidget( layoutRight )
        # Set dialog layout
        self.setLayout(layoutMaster)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.greetings)
       
    # Greets the user
    def greetings(self):
        print ("Hello %s" % self.edit.text())        
 
 
if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())

