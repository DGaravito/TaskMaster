from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QGridLayout, QVBoxLayout, QGroupBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from Guis.Settings import discount, memory, reaction, beads, pbt, nact, gamble


class SelectWindow(QWidget):
    """
    This class is a window that has buttons for every task I have incorporated (or plan to incorporate) at the moment
    """

    def __init__(self):
        super().__init__()

        # Window title
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # setting the geometry of window
        self.setGeometry(0, 0, 500, 500)

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
        self.pdbutton = QPushButton('Probability Discounting')
        self.pdbutton.clicked.connect(lambda: self.selection('PD'))

        # CEDT button
        self.cedtbutton = QPushButton('CEDT')
        self.cedtbutton.clicked.connect(lambda: self.selection('CEDT'))

        # ARTT button
        self.arttbutton = QPushButton('ARTT (feat. ADOPy)')
        self.arttbutton.clicked.connect(lambda: self.selection('ARTT'))

        # Risk Aversion button
        self.rabutton = QPushButton('Risk Aversion')
        self.rabutton.clicked.connect(lambda: self.selection('RA'))

        # Framing button
        self.framebutton = QPushButton('Framing Task')
        self.framebutton.clicked.connect(lambda: self.selection('Framing'))

        # Beads Task button
        self.beadsbutton = QPushButton('Beads')
        self.beadsbutton.clicked.connect(lambda: self.selection('Beads'))

        # PBT button
        self.pbtbutton = QPushButton('PBT')
        self.pbtbutton.clicked.connect(lambda: self.selection('PBT'))

        # Negative Attentional Capture button
        self.nactbutton = QPushButton('NACT')
        self.nactbutton.clicked.connect(lambda: self.selection('NACT'))

        # Stop Signal button
        self.ssbutton = QPushButton('Stop Signal')
        self.ssbutton.clicked.connect(lambda: self.selection('SS'))

        # Emo Go-NoGo button
        self.egngbutton = QPushButton('Emo Go/No-Go')
        self.egngbutton.clicked.connect(lambda: self.selection('EGNG'))

        # Go-NoGo button
        self.gngbutton = QPushButton('Go/No-Go (WIP)')
        # self.gngbutton.clicked.connect(lambda: self.selection('GNG'))

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

        # Create a main layout and then separate grid layouts for the different categories of tasks
        mainlayout = QVBoxLayout()
        mainlayout.addWidget(self.header)

        risklayout = QGridLayout()
        discountlayout = QGridLayout()
        reactionlayout = QGridLayout()
        memorylayout = QGridLayout()
        misclayout = QGridLayout()

        # Create boxes around the category layouts
        riskbox = QGroupBox('Risk Taking')
        riskbox.setLayout(risklayout)

        discountbox = QGroupBox('Discounting')
        discountbox.setLayout(discountlayout)

        reactionbox = QGroupBox('Reaction')
        reactionbox.setLayout(reactionlayout)

        memorybox = QGroupBox('Memory')
        memorybox.setLayout(memorylayout)

        miscbox = QGroupBox('Misc')
        miscbox.setLayout(misclayout)

        # Add all the buttons to the appropriate layouts
        discountlayout.addWidget(self.ddbutton, 0, 0)
        discountlayout.addWidget(self.pdbutton, 0, 1)
        discountlayout.addWidget(self.cedtbutton, 0, 2)

        risklayout.addWidget(self.arttbutton, 0, 0)
        risklayout.addWidget(self.rabutton, 0, 1)
        risklayout.addWidget(self.framebutton, 0, 2)

        reactionlayout.addWidget(self.pbtbutton, 0, 0)
        reactionlayout.addWidget(self.nactbutton, 0, 1)
        reactionlayout.addWidget(self.ssbutton, 0, 2)
        reactionlayout.addWidget(self.egngbutton, 1, 0)
        reactionlayout.addWidget(self.gngbutton, 1, 1)

        memorylayout.addWidget(self.prbutton, 0, 0)
        memorylayout.addWidget(self.nbackbutton, 0, 1)

        misclayout.addWidget(self.beadsbutton, 0, 0)

        # add the boxes and the quit button to the main layout
        mainlayout.addWidget(riskbox)
        mainlayout.addWidget(discountbox)
        mainlayout.addWidget(reactionbox)
        mainlayout.addWidget(memorybox)
        mainlayout.addWidget(miscbox)

        mainlayout.addWidget(self.quitbutton)

        # set the layout as the window's layout
        self.setLayout(mainlayout)

    def centerscreen(self):
        """
        Finds the geometry of the comnputer screen and moves to the center of the screen
        """

        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def selection(self, choice=''):
        """
        Takes the choice value (determined by what button the user picked) and loads up the appropriate settingsguis
        window
        :param choice: a string corresponding to the button that the user clicked
        :return: Hides the selection window and opens up the corresponding settingsguis window
        """

        match choice:

            case str('DD'):
                self.w = discount.DdSettings('DD')

            case str('PD'):
                self.w = discount.PdSettings('PD')

            case str('CEDT'):
                self.w = discount.CEDTSettings('CEDT')

            case str('ARTT'):
                self.w = gamble.ARTTSettings('ARTT')

            case str('RA'):
                self.w = gamble.RASettings('RA')

            case str('Framing'):
                self.w = gamble.FrameSettings('Framing')

            case str('Beads'):
                self.w = beads.BeadsSettings('Beads')

            case str('PBT'):
                self.w = pbt.PBTSettings('PBT')

            case str('NACT'):
                self.w = nact.NACTSettings('NACT')

            case str('SS'):
                self.w = reaction.SSSettings('SS')

            case str('PR'):
                self.w = memory.PrSettings('PR')

            case str('NB'):
                self.w = memory.NBackSettings('1-back')

            case str('EGNG'):
                self.w = reaction.EGNGSettings('EGNG')

            case str('GNG'):
                self.w = reaction.GNGSettings('GNG')

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
