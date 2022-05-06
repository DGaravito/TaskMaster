from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QSpinBox, QLineEdit,\
    QFormLayout, QVBoxLayout, QCheckBox, QComboBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from adopy.tasks.dd import TaskDD
from adopy.tasks.cra import TaskCRA
import participant
import gui


class Settings(QWidget):
    def centerscreen(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def __init__(self):
        super().__init__()

        # Window title
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # setting the minimum window size
        self.setMinimumSize(500, 350)

        # center window
        self.centerscreen()

        # Quit button
        self.quitbutton = QPushButton('Quit')
        self.quitbutton.clicked.connect(QApplication.instance().quit)
        self.quitbutton.resize(self.quitbutton.sizeHint())


class DdSettings(Settings):

    def __init__(self):
        super().__init__()

        # setting  the geometry of window
        self.setGeometry(0, 0, 650, 350)

        # center window
        self.centerscreen()

        # Add in elements
        self.elements()

        # Show all elements
        self.show()

    def elements(self):
        # Make overarching layout
        over_layout = QVBoxLayout()

        # Make a label with instructions
        self.header = QLabel('Enter the appropriate values:', self)

        # setting font style and size
        self.header.setFont(QFont('Helvetica', 30))

        # center header
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add header to overarching layout

        over_layout.addWidget(self.header)

        # ID form
        self.idform = QLineEdit()
        self.idform.setText('9999')

        # Trials input
        self.trialsin = QSpinBox()
        self.trialsin.setSpecialValueText('10')

        # Immediate Delay input
        self.imdin = QSpinBox()
        self.imdin.setSpecialValueText('0')

        # Short Delay input
        self.sdin = QSpinBox()
        self.sdin.setSpecialValueText('1')

        # Long Delay input
        self.ldin = QSpinBox()
        self.ldin.setSpecialValueText('52')

        # SS reward input
        self.ssrewin = QSpinBox()
        self.ssrewin.setSpecialValueText('1')

        # LL reward input
        self.llrewin = QSpinBox()
        self.llrewin.setSpecialValueText('250')

        # WD input
        self.wdset = QLineEdit()
        self.wdset.setText('/Users/DGaravito/Desktop')

        # Submit button
        self.submit = QPushButton('Submit')
        self.submit.clicked.connect(self.submitsettings)

        # Make form layout for all the settings
        layout = QFormLayout()

        layout.addRow(QLabel('Subject ID:'), self.idform)
        layout.addRow(QLabel('Number of trials:'), self.trialsin)
        layout.addRow(QLabel('Shortest delay in immediate option (weeks):'), self.imdin)
        layout.addRow(QLabel('Shortest delay in delayed option (weeks):'), self.sdin)
        layout.addRow(QLabel('Longest delay in delayed option (weeks):'), self.ldin)
        layout.addRow(QLabel('Smallest reward in immediate option:'), self.ssrewin)
        layout.addRow(QLabel('Biggest reward in delayed option:'), self.llrewin)
        layout.addRow(QLabel('Where do you want to save the output?'), self.wdset)
        layout.addRow(self.submit, self.quitbutton)

        # Add form layout to overarching layout
        over_layout.addLayout(layout)

        self.setLayout(over_layout)

    def submitsettings(self):
        person = participant.DdParticipant(self.idform.text(),
                                           self.trialsin.text(),
                                           self.wdset.text(),
                                           TaskDD(),
                                           self.imdin.text(),
                                           self.sdin.text(),
                                           self.ldin.text(),
                                           self.ssrewin.text(),
                                           self.llrewin.text())

        self.exp = gui.DDiscountExp(person)
        self.exp.show()
        self.hide()


class PdSettings(Settings): # TODO Change to probability discounting things

    def __init__(self):
        super().__init__()

        # setting  the geometry of window
        self.setGeometry(0, 0, 650, 350)

        # center window
        self.centerscreen()

        # Add in elements
        self.elements()

        # Show all elements
        self.show()

    def elements(self):
        # Make overarching layout
        over_layout = QVBoxLayout()

        # Make a label with instructions
        self.header = QLabel('Enter the appropriate values:', self)

        # setting font style and size
        self.header.setFont(QFont('Helvetica', 30))

        # center header
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add header to overarching layout

        over_layout.addWidget(self.header)

        # ID form
        self.idform = QLineEdit()
        self.idform.setText('9999')

        # Trials input
        self.trialsin = QSpinBox()
        self.trialsin.setSpecialValueText('10')

        # Minimum input
        self.rewmin = QSpinBox()
        self.rewmin.setSpecialValueText('1')

        # Maximum input
        self.rewmax = QSpinBox()
        self.rewmax.setSpecialValueText('250')

        # Dropdown box for gains, losses, or both
        self.design = QComboBox()
        self.design.addItems(['Gains only', 'Losses only', 'Gains and losses'])

        # WD input
        self.wdset = QLineEdit()
        self.wdset.setText('/Users/DGaravito/Desktop')

        # Submit button
        self.submit = QPushButton('Submit')
        self.submit.clicked.connect(self.submitsettings)

        # Make form layout for all the settings
        layout = QFormLayout()

        layout.addRow(QLabel('Subject ID:'), self.idform)
        layout.addRow(QLabel('Number of trials:'), self.trialsin)
        layout.addRow(QLabel('Smallest amount of money:'), self.rewmin)
        layout.addRow(QLabel('Biggest amount of money:'), self.rewmax)
        layout.addRow(QLabel('Where do you want to save the output?'), self.wdset)
        layout.addRow(self.submit, self.quitbutton)

        # Add form layout to overarching layout
        over_layout.addLayout(layout)

        self.setLayout(over_layout)

    def submitsettings(self):
        person = participant.PdParticipant(self.idform.text(),
                                           self.trialsin.text(),
                                           self.wdset.text(),
                                           'Probability Discounting',
                                           self.design.currentText(),
                                           self.rewmin.text(),
                                           self.rewmax.text())

        self.exp = gui.PDiscountExp(person)
        self.exp.show()
        self.hide()


class CEDTSettings(Settings): # TODO Review CEDT for proper variables

    def __init__(self):
        super().__init__()

        # setting  the geometry of window
        self.setGeometry(0, 0, 650, 350)

        # center window
        self.centerscreen()

        # Add in elements
        self.elements()

        # Show all elements
        self.show()

    def elements(self):
        # Make overarching layout
        over_layout = QVBoxLayout()

        # Make a label with instructions
        self.header = QLabel('Enter the appropriate values:', self)

        # setting font style and size
        self.header.setFont(QFont('Helvetica', 30))

        # center header
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add header to overarching layout

        over_layout.addWidget(self.header)

        # ID form
        self.idform = QLineEdit()
        self.idform.setText('9999')

        # Trials input
        self.trialsin = QSpinBox()
        self.trialsin.setSpecialValueText('10')

        # Immediate Delay input
        self.imdin = QSpinBox()
        self.imdin.setSpecialValueText('0')

        # Short Delay input
        self.sdin = QSpinBox()
        self.sdin.setSpecialValueText('1')

        # Long Delay input
        self.ldin = QSpinBox()
        self.ldin.setSpecialValueText('52')

        # SS reward input
        self.ssrewin = QSpinBox()
        self.ssrewin.setSpecialValueText('1')

        # LL reward input
        self.llrewin = QSpinBox()
        self.llrewin.setSpecialValueText('250')

        # WD input
        self.wdset = QLineEdit()
        self.wdset.setText('/Users/DGaravito/Desktop')

        # Submit button
        self.submit = QPushButton('Submit')
        self.submit.clicked.connect(self.submitsettings)

        # Make form layout for all the settings
        layout = QFormLayout()

        layout.addRow(QLabel('Subject ID:'), self.idform)
        layout.addRow(QLabel('Number of trials:'), self.trialsin)
        layout.addRow(QLabel('Shortest delay in immediate option (weeks):'), self.imdin)
        layout.addRow(QLabel('Shortest delay in delayed option (weeks):'), self.sdin)
        layout.addRow(QLabel('Longest delay in delayed option (weeks):'), self.ldin)
        layout.addRow(QLabel('Smallest reward in immediate option:'), self.ssrewin)
        layout.addRow(QLabel('Where do you want to save the output?'), self.wdset)
        layout.addRow(self.submit, self.quitbutton)

        # Add form layout to overarching layout
        over_layout.addLayout(layout)

        self.setLayout(over_layout)

    def submitsettings(self):
        person = participant.DdParticipant(self.idform.text(),
                                           self.trialsin.text(),
                                           self.wdset.text(),
                                           TaskDD(),
                                           self.imdin.text(),
                                           self.sdin.text(),
                                           self.ldin.text(),
                                           self.ssrewin.text(),
                                           self.llrewin.text())

        self.exp = gui.DiscountExp(person)
        self.exp.show()
        self.hide()


class ARTTSettings(Settings):  # TODO Review ADOPy for required stuff - progress bar?

    def __init__(self):
        super().__init__()

        # setting  the geometry of window
        self.setGeometry(0, 0, 650, 350)

        # center window
        self.centerscreen()

        # Add in elements
        self.elements()

        # Show all elements
        self.show()

    def elements(self):
        # Make overarching layout
        over_layout = QVBoxLayout()

        # Make a label with instructions
        self.header = QLabel('Enter the appropriate values:', self)

        # setting font style and size
        self.header.setFont(QFont('Helvetica', 30))

        # center header
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add header to overarching layout

        over_layout.addWidget(self.header)

        # ID form
        self.idform = QLineEdit()
        self.idform.setText('9999')

        # Trials input
        self.trialsin = QSpinBox()
        self.trialsin.setSpecialValueText('10')

        # Short Delay input
        self.probriskin = QLineEdit()
        self.probriskin.setText('.13, .25, .38')

        # Long Delay input
        self.probambin = QLineEdit()
        self.probambin.setText('.25, .5, .75')

        # Smallest reward input
        self.srewin = QSpinBox()
        self.srewin.setSpecialValueText('5')

        # Largest reward input
        self.lrewin = QSpinBox()
        self.lrewin.setSpecialValueText('50')

        # WD input
        self.wdset = QLineEdit()
        self.wdset.setText('/Users/DGaravito/Desktop')

        # Submit button
        self.submit = QPushButton('Submit')
        self.submit.clicked.connect(self.submitsettings)

        # Make form layout for all the settings
        layout = QFormLayout()

        layout.addRow(QLabel('Subject ID:'), self.idform)
        layout.addRow(QLabel('Number of trials:'), self.trialsin)
        layout.addRow(QLabel('Enter the probablities for risky trials:'), self.probriskin)
        layout.addRow(QLabel('Enter the probablities for ambiguous trials:'), self.probambin)
        layout.addRow(QLabel('Smallest reward possible:'), self.srewin)
        layout.addRow(QLabel('Biggest reward possible:'), self.lrewin)
        layout.addRow(QLabel('Where do you want to save the output?'), self.wdset)
        layout.addRow(self.submit, self.quitbutton)

        # Add form layout to overarching layout
        over_layout.addLayout(layout)

        self.setLayout(over_layout)

    def submitsettings(self):

        riskstring = self.probriskin.text()

        risklist = list(riskstring.split(", "))

        ambstring = self.probambin.text()

        amblist = list(ambstring.split(", "))

        person = participant.ARTTParticipant(self.idform.text(),
                                             self.trialsin.text(),
                                             self.wdset.text(),
                                             TaskCRA(),
                                             risklist,
                                             amblist,
                                             self.srewin.text(),
                                             self.lrewin.text())

        self.exp = gui.ARTTExp(person)
        self.exp.show()
        self.hide()


class PrSettings(Settings):

    def __init__(self):
        super().__init__()

        # setting  the geometry of window
        self.setGeometry(0, 0, 650, 350)

        # center window
        self.centerscreen()

        # STT default
        self.stt = 0

        # Add in elements
        self.elements()

        # Show all elements
        self.show()

    def elements(self):
        # Make overarching layout
        over_layout = QVBoxLayout()

        # Make a label with instructions
        self.header = QLabel('Enter the appropriate values:', self)

        # setting font style and size
        self.header.setFont(QFont('Helvetica', 30))

        # center header
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add header to overarching layout

        over_layout.addWidget(self.header)

        # ID form
        self.idform = QLineEdit()
        self.idform.setText('9999')

        # Pairs input
        self.pairsin = QSpinBox()
        self.pairsin.setSpecialValueText('30')

        # ST Trials input
        self.trialsin = QSpinBox()
        self.trialsin.setSpecialValueText('3')

        # ST Trials input
        self.stttoggle = QCheckBox('STT?', self)
        self.stttoggle.stateChanged.connect(self.clickBox)

        # WD input
        self.wdset = QLineEdit()
        self.wdset.setText('/Users/DGaravito/Desktop')

        # Submit button
        self.submit = QPushButton('Submit')
        self.submit.clicked.connect(self.submitsettings)

        # Make form layout for all the settings
        layout = QFormLayout()

        layout.addRow(QLabel('Subject ID:'), self.idform)
        layout.addRow(QLabel('Number of word pairs (Max: 30):'), self.pairsin)
        layout.addRow(QLabel('Number of study-test trials:'), self.trialsin)
        layout.addRow(QLabel('Do you want an STT trial?:'), self.stttoggle)
        layout.addRow(QLabel('Where do you want to save the output?'), self.wdset)
        layout.addRow(self.submit, self.quitbutton)

        # Add form layout to overarching layout
        over_layout.addLayout(layout)

        self.setLayout(over_layout)

    def clickBox(self):

        if self.stttoggle.isChecked():
            self.stt = 1
        else:
            self.stt = 0

    def submitsettings(self):
        person = participant.PrParticipant(self.idform.text(),
                                           self.pairsin.text(),
                                           self.wdset.text(),
                                           'Pair Recall Memory',
                                           self.trialsin.text(),
                                           self.stt)

        self.exp = gui.MemoryExp(person)
        self.exp.show()
        self.hide()
