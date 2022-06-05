from PyQt6.QtWidgets import QLabel, QSpinBox, QFormLayout, QVBoxLayout, QComboBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from settingsguis import settings

from participants import reactionp
from expguis import reactiongui


class SSSettings(settings.Settings):

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

        # Trials input
        self.trialsin = QSpinBox()
        self.trialsin.setSpecialValueText('30')

        # Reaction time input
        self.maxrtin = QSpinBox()
        self.maxrtin.setSpecialValueText('1500')

        # Blocks input
        self.blocksin = QSpinBox()
        self.blocksin.setSpecialValueText('3')

        # Make form layout for all the settingsguis
        layout = QFormLayout()

        layout.addRow(QLabel('Subject ID:'), self.idform)
        layout.addRow(QLabel('Number of trials:'), self.trialsin)
        layout.addRow(QLabel('Maximal reaction time (in milliseconds)?'), self.maxrtin)
        layout.addRow(QLabel('Number of blocks?'), self.blocksin)
        layout.addRow(QLabel('Where do you want to save the output?'), self.wdset)
        layout.addRow(self.submit, self.quitbutton)

        # Add form layout to overarching layout
        over_layout.addLayout(layout)

        self.setLayout(over_layout)

    def submitsettings(self):

        person = reactionp.SSParticipant(self.idform.text(),
                                         self.trialsin.text(),
                                         self.wdset.text(),
                                         'Stop-Signal Task',
                                         self.maxrtin.text(),
                                         self.blocksin.text())

        self.exp = reactiongui.SSExp(person)
        self.exp.show()
        self.hide()


class EGNGSettings(settings.Settings):

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

        # Trials input
        self.trialsin = QSpinBox()
        self.trialsin.setSpecialValueText('30')

        # Reaction time input
        self.maxrtin = QSpinBox()
        self.maxrtin.setSpecialValueText('1500')

        # Blocks input
        self.blocksin = QSpinBox()
        self.blocksin.setSpecialValueText('3')

        # Make form layout for all the settingsguis
        layout = QFormLayout()

        layout.addRow(QLabel('Subject ID:'), self.idform)
        layout.addRow(QLabel('Number of trials:'), self.trialsin)
        layout.addRow(QLabel('Maximal reaction time (in milliseconds)?'), self.maxrtin)
        layout.addRow(QLabel('Number of blocks?'), self.blocksin)
        layout.addRow(QLabel('Where do you want to save the output?'), self.wdset)
        layout.addRow(self.submit, self.quitbutton)

        # Add form layout to overarching layout
        over_layout.addLayout(layout)

        self.setLayout(over_layout)

    def submitsettings(self):

        person = reactionp.EGNGParticipant(self.idform.text(),
                                           self.trialsin.text(),
                                           self.wdset.text(),
                                           'Emo Go/No-Go',
                                           self.maxrtin.text(),
                                           self.blocksin.text())

        self.exp = reactiongui.EGNGExp(person)
        self.exp.show()
        self.hide()
