from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QGridLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

import settingsgui


class SelectWindow(QWidget):
    """
    This class is a window that has buttons for every task I have incorporated (or plan to incorporate) at the moment
    """

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
        self.header = QLabel('Please select the appropriate task:', self)

        # setting font style and size
        self.header.setFont(QFont('Helvetica', 15))

        # resizing and moving
        self.header.resize(400, 25)
        self.header.move(0, 10)

        # center header

        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # DD button
        self.ddbutton = QPushButton('DD (feat. ADOPy)')
        self.ddbutton.clicked.connect(lambda: self.selection(1))

        # PD button
        self.pdbutton = QPushButton('PD')
        self.pdbutton.clicked.connect(lambda: self.selection(2))

        # CEDT button
        self.cedtbutton = QPushButton('CEDT (WIP)')
        self.cedtbutton.clicked.connect(lambda: self.selection(3))

        # ARTT button
        self.arttbutton = QPushButton('ARTT (feat. ADOPy)')
        self.arttbutton.clicked.connect(lambda: self.selection(4))

        # Risk Aversion button
        self.rabutton = QPushButton('RA')
        self.rabutton.clicked.connect(lambda: self.selection(5))

        # Framing button
        self.framebutton = QPushButton('Framing')
        self.framebutton.clicked.connect(lambda: self.selection(6))

        # Beads Task button
        self.beadsbutton = QPushButton('Beads')
        self.beadsbutton.clicked.connect(lambda: self.selection(7))

        # PBT button
        self.pbtbutton = QPushButton('PBT')
        self.pbtbutton.clicked.connect(lambda: self.selection(8))

        # Negative Attentional Capture button
        self.nactbutton = QPushButton('NACT (WIP)')
        self.nactbutton.clicked.connect(lambda: self.selection(9))

        # Stop Signal button
        self.ssbutton = QPushButton('Stop Signal (WIP)')
        self.ssbutton.clicked.connect(lambda: self.selection(10))

        # Emo Go-NoGo button
        self.egngbutton = QPushButton('Emo Go/No-Go (WIP)')
        self.egngbutton.clicked.connect(lambda: self.selection(13))

        # Paired Recall button
        self.prbutton = QPushButton('Paired Recall')
        self.prbutton.clicked.connect(lambda: self.selection(11))

        # n Back button
        self.nbackbutton = QPushButton('n-Back')
        self.nbackbutton.clicked.connect(lambda: self.selection(12))

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
        layout.addWidget(self.egngbutton, 3, 1)
        layout.addWidget(self.prbutton, 3, 2)
        layout.addWidget(self.nbackbutton, 4, 0)
        layout.addWidget(self.quitbutton, 5, 0, 1, 3)

        self.setLayout(layout)

    def selection(self, choice):
        """
        Takes the choice value (determined by what button the user picked) and loads up the appropriate settings window
        :param choice: an integer corresponding to the button that the user clicked
        :return: Hides the selection window and opens up the corresponding settings window
        """

        match choice:

            case 1:
                self.w = settingsgui.DdSettings()

            case 2:
                self.w = settingsgui.PdSettings()

            case 3:
                self.w = settingsgui.CEDTSettings()

            case 4:
                self.w = settingsgui.ARTTSettings()

            case 5:
                self.w = settingsgui.RASettings()

            case 6:
                self.w = settingsgui.FrameSettings()

            case 7:
                self.w = settingsgui.BeadsSettings()

            case 8:
                self.w = settingsgui.PBTSettings()

            case 9:
                self.w = settingsgui.NACTSettings()

            case 10:
                self.w = settingsgui.SSSettings()

            case 11:
                self.w = settingsgui.PrSettings()

            case 12:
                self.w = settingsgui.NBackSettings()

            case 13:
                self.w = settingsgui.EGNGSettings()

            case _:
                print("not sure how you got this...")

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
