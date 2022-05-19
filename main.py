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
        self.header.move(0, 20)

        # center header

        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # DD button
        self.ddbutton = QPushButton('DD')
        self.ddbutton.clicked.connect(self.ddexp)

        # PD button
        self.pdbutton = QPushButton('PD')
        self.pdbutton.clicked.connect(self.pdexp)

        # CEDT button
        self.cedtbutton = QPushButton('CEDT (WIP)')
        self.cedtbutton.clicked.connect(self.cedtexp)

        # ARTT button
        self.arttbutton = QPushButton('ARTT (WIP)')
        self.arttbutton.clicked.connect(self.arttexp)

        # Risk Aversion button
        self.rabutton = QPushButton('RA (WIP)')
        self.rabutton.clicked.connect(self.raexp)

        # Framing button
        self.framebutton = QPushButton('Framing (WIP)')
        self.framebutton.clicked.connect(self.frameexp)

        # Beads Task button
        self.beadsbutton = QPushButton('Beads (WIP)')
        self.beadsbutton.clicked.connect(self.beadsexp)

        # PBT button
        self.pbtbutton = QPushButton('PBT (WIP)')
        self.pbtbutton.clicked.connect(self.pbtexp)

        # Negative Attentional Capture button
        self.nactbutton = QPushButton('NACT (WIP)')
        self.nactbutton.clicked.connect(self.nactexp)

        # Stop Signal button
        self.ssbutton = QPushButton('Stop Signal (WIP)')
        self.ssbutton.clicked.connect(self.ssexp)

        # Paired Recall button
        self.prbutton = QPushButton('Paired Recall')
        self.prbutton.clicked.connect(self.prexp)

        # n Back button
        self.nbackbutton = QPushButton('n-Back')
        self.nbackbutton.clicked.connect(self.nback)

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
        layout.addWidget(self.rabutton, 1, 1)
        layout.addWidget(self.framebutton, 1, 2)
        layout.addWidget(self.beadsbutton, 2, 0)
        layout.addWidget(self.pbtbutton, 2, 1)
        layout.addWidget(self.nactbutton, 2, 2)
        layout.addWidget(self.ssbutton, 3, 0)
        layout.addWidget(self.prbutton, 3, 1)
        layout.addWidget(self.nbackbutton, 3, 2)
        layout.addWidget(self.quitbutton, 4, 0, 1, 3)

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

    def raexp(self):
        self.w = settingsgui.RASettings()
        self.w.show()
        self.hide()

    def frameexp(self):
        self.w = settingsgui.FrameSettings()
        self.w.show()
        self.hide()

    def beadsexp(self):
        self.w = settingsgui.BeadsSettings()
        self.w.show()
        self.hide()

    def pbtexp(self):
        self.w = settingsgui.PBTSettings()
        self.w.show()
        self.hide()

    def nactexp(self):
        self.w = settingsgui.NACTSettings()
        self.w.show()
        self.hide()

    def ssexp(self):
        self.w = settingsgui.SSSettings()
        self.w.show()
        self.hide()

    def prexp(self):
        self.w = settingsgui.PrSettings()
        self.w.show()
        self.hide()

    def nback(self):
        self.w = settingsgui.NBackSettings()
        self.w.show()
        self.hide()


# Main function, which starts the application when called
def main():
    APP = QApplication([])
    APP.setStyle('Fusion')
    w = SelectWindow()
    APP.exec()


# Main loop
if __name__ == '__main__':

    main()
