from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QGridLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

import settingsgui


class SelectWindow(QWidget):

    def centerscreen(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def __init__(self):
        super().__init__()

        # Window title
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # setting  the geometry of window
        self.setGeometry(0, 0, 400, 400)

        # setting the minimum window size
        self.setMinimumSize(400, 400)

        # center window
        self.centerscreen()

        # Add in elements
        self.elements()

        # Show all elements
        self.show()

    def elements(self):

        # Make a label with instructions
        self.header = QLabel('Please select the appropriate design:', self)

        # setting font style and size
        self.header.setFont(QFont('Helvetica', 15))

        # resizing and moving
        self.header.resize(400, 25)
        self.header.move(0, 30)

        # center header

        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # DD button
        self.ddbutton = QPushButton('DD')
        self.ddbutton.clicked.connect(self.ddexp)

        # PD button
        self.pdbutton = QPushButton('PD (WIP)')
        self.pdbutton.clicked.connect(self.pdexp)

        # CEDT button
        self.cedtbutton = QPushButton('CEDT (WIP)')
        self.cedtbutton.clicked.connect(self.cedtexp)

        # ARTT button
        self.arttbutton = QPushButton('ARTT (WIP)')
        self.arttbutton.clicked.connect(self.arttexp)

        # Paired Recall button
        self.prbutton = QPushButton('Paired Recall')
        self.prbutton.clicked.connect(self.prexp)

        # Quit button
        self.quitbutton = QPushButton('Quit')
        self.quitbutton.clicked.connect(QApplication.instance().quit)
        self.quitbutton.resize(self.quitbutton.sizeHint())

        # Create layout for design options
        layout = QGridLayout()

        layout.addWidget(self.ddbutton, 0, 0)
        layout.addWidget(self.pdbutton, 0, 1)
        layout.addWidget(self.cedtbutton, 0, 2)
        layout.addWidget(self.arttbutton, 1, 0)
        layout.addWidget(QPushButton('Risk Aversion'), 1, 1)
        layout.addWidget(QPushButton('Framing'), 1, 2)
        layout.addWidget(self.prbutton, 2, 0)
        layout.addWidget(QPushButton('n-Back'), 2, 1)
        layout.addWidget(QPushButton('TBA'), 2, 2)
        layout.addWidget(self.quitbutton, 3, 0, 1, 3)

        self.setLayout(layout)

    def ddexp(self):
        self.w = settingsgui.DdSettings()
        self.w.show()
        self.hide()

    def pdexp(self):
        self.w = settingsgui.PdSettings()
        self.w.show()
        self.hide()

    def cedtexp(self):
        self.w = settingsgui.CEDTSettings()
        self.w.show()
        self.hide()

    def arttexp(self):
        self.w = settingsgui.ARTTSettings()
        self.w.show()
        self.hide()

    def prexp(self):
        self.w = settingsgui.PrSettings()
        self.w.show()
        self.hide()


def main():
    APP = QApplication([])
    APP.setStyle('Fusion')
    w = SelectWindow()
    APP.exec()


if __name__ == '__main__':

    main()
