from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QGridLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

import settingsguis


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
        self.ddbutton.clicked.connect(lambda: self.selection('DD'))

        # PD button
        self.pdbutton = QPushButton('PD')
        self.pdbutton.clicked.connect(lambda: self.selection('PD'))

        # CEDT button
        self.cedtbutton = QPushButton('CEDT (WIP)')
        self.cedtbutton.clicked.connect(lambda: self.selection('CEDT'))

        # ARTT button
        self.arttbutton = QPushButton('ARTT (feat. ADOPy)')
        self.arttbutton.clicked.connect(lambda: self.selection('ARTT'))

        # Risk Aversion button
        self.rabutton = QPushButton('RA')
        self.rabutton.clicked.connect(lambda: self.selection('RA'))

        # Framing button
        self.framebutton = QPushButton('Framing')
        self.framebutton.clicked.connect(lambda: self.selection('Framing'))

        # Beads Task button
        self.beadsbutton = QPushButton('Beads')
        self.beadsbutton.clicked.connect(lambda: self.selection('Beads'))

        # PBT button
        self.pbtbutton = QPushButton('PBT')
        self.pbtbutton.clicked.connect(lambda: self.selection('PBT'))

        # Negative Attentional Capture button
        self.nactbutton = QPushButton('NACT (WIP)')
        self.nactbutton.clicked.connect(lambda: self.selection('NACT'))

        # Stop Signal button
        self.ssbutton = QPushButton('Stop Signal')
        self.ssbutton.clicked.connect(lambda: self.selection('SS'))

        # Emo Go-NoGo button
        self.egngbutton = QPushButton('Emo Go/No-Go (WIP)')
        self.egngbutton.clicked.connect(lambda: self.selection('EGNG'))

        # Go-NoGo button
        self.gngbutton = QPushButton('Go/No-Go (WIP)')
        self.gngbutton.clicked.connect(lambda: self.selection('GNG'))

        # Paired Recall button
        self.prbutton = QPushButton('Paired Recall')
        self.prbutton.clicked.connect(lambda: self.selection('PR'))

        # n Back button
        self.nbackbutton = QPushButton('n-Back')
        self.nbackbutton.clicked.connect(lambda: self.selection('NB'))

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
        layout.addWidget(self.gngbutton, 3, 2)
        layout.addWidget(self.prbutton, 4, 0)
        layout.addWidget(self.nbackbutton, 4, 1)
        layout.addWidget(self.quitbutton, 5, 0, 1, 3)

        self.setLayout(layout)

    def selection(self, choice=''):
        """
        Takes the choice value (determined by what button the user picked) and loads up the appropriate settingsguis
        window
        :param choice: a string corresponding to the button that the user clicked
        :return: Hides the selection window and opens up the corresponding settingsguis window
        """

        match choice:

            case str('DD'):
                self.w = settingsguis.discount.DdSettings()

            case str('PD'):
                self.w = settingsguis.discount.PdSettings()

            case str('CEDT'):
                self.w = settingsguis.discount.CEDTSettings()

            case str('ARTT'):
                self.w = settingsguis.gamble.ARTTSettings()

            case str('RA'):
                self.w = settingsguis.gamble.RASettings()

            case str('Framing'):
                self.w = settingsguis.gamble.FrameSettings()

            case str('Beads'):
                self.w = settingsguis.beads.BeadsSettings()

            case str('PBT'):
                self.w = settingsguis.pbt.PBTSettings()

            case str('NACT'):
                self.w = settingsguis.nact.NACTSettings()

            case str('SS'):
                self.w = settingsguis.reaction.SSSettings()

            case str('PR'):
                self.w = settingsguis.memory.PrSettings()

            case str('NB'):
                self.w = settingsguis.memory.NBackSettings()

            case str('EGNG'):
                self.w = settingsguis.reaction.EGNGSettings()

            case _:
                self.w = QLabel('Panic')

        self.w.show()
        self.hide()


# Main function, which starts the application when called
def main():
    app = QApplication([])
    app.setStyle('Fusion')
    SelectWindow()
    app.exec()


# Main loop
if __name__ == '__main__':

    main()
