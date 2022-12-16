from PyQt5 import uic,QtCore
from PyQt5.QtWidgets import QDialog 

class Main(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('ui/main.ui', self)
        self.show()
    
    