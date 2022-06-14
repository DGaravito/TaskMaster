from PyQt6.QtWidgets import QLabel, QSpinBox, QFormLayout, QVBoxLayout, QCheckBox, QComboBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from settingsguis import settings

from participants import memoryp
from expguis import memorygui


class PrSettings(settings.Settings):

    def __init__(self):
        super().__init__()

        # setting  the geometry of window
        self.setGeometry(0, 0, 650, 350)

        # Default for whether to use STT trial
        self.stt = 'No'

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

        # Pairs input
        self.pairsin = QSpinBox()
        self.pairsin.setSpecialValueText('30')

        # ST Trials input
        self.trialsin = QSpinBox()
        self.trialsin.setSpecialValueText('3')

        # ST Trials input
        self.stttoggle = QCheckBox(self)
        self.stttoggle.stateChanged.connect(self.clickbox)

        # Make form layout for all the settingsguis
        layout = QFormLayout()

        layout.addRow(QLabel('Subject ID:'), self.idform)
        layout.addRow(QLabel('Session name/number (enter \'Practice\' to not have output):'), self.sessionin)
        layout.addRow(QLabel('Number of word pairs (Max: 30):'), self.pairsin)
        layout.addRow(QLabel('Number of study-test trials:'), self.trialsin)
        layout.addRow(QLabel('Do you want an STT trial?'), self.stttoggle)
        layout.addRow(QLabel('Are you using an eyetracker?'), self.eyetrackingtoggle)
        layout.addRow(QLabel('Current output directory:'), self.wdlabel)
        layout.addRow(QLabel('Click to choose where to save your output:'), self.wdset)
        layout.addRow(self.quitbutton, self.submit)

        # Add form layout to overarching layout
        over_layout.addLayout(layout)

        self.setLayout(over_layout)

    def clickbox(self):

        if self.stttoggle.isChecked():
            self.stt = 'Yes'
        else:
            self.stt = 'No'

        if self.eyetrackingtoggle.isChecked():
            self.eyetracking = 'Yes'
        else:
            self.eyetracking = 'No'

    def submitsettings(self):

        person = memoryp.PrParticipant(self.idform.text(),
                                       self.pairsin.text(),
                                       self.sessionin.text(),
                                       self.wd,
                                       'Pair Recall Memory',
                                       self.trialsin.text(),
                                       self.stt,
                                       self.eyetracking)

        self.exp = memorygui.PrExp(person)
        self.exp.show()
        self.hide()


class NBackSettings(settings.Settings):

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

        # Trials input
        self.trialsin = QSpinBox()
        self.trialsin.setSpecialValueText('30')

        # Dropdown box for gains, losses, or both
        self.design = QComboBox()
        self.design.addItems(['1-back', '2-back', '3-back', '4-back'])

        # Make form layout for all the settingsguis
        layout = QFormLayout()

        layout.addRow(QLabel('Subject ID:'), self.idform)
        layout.addRow(QLabel('Session name/number (enter \'Practice\' to not have output):'), self.sessionin)
        layout.addRow(QLabel('Number of trials per block:'), self.trialsin)
        layout.addRow(QLabel('Number of blocks:'), self.blocksin)
        layout.addRow(QLabel('Type of n-Back:'), self.design)
        layout.addRow(QLabel('Are you using a button-box instead of the keyboard?'), self.buttontoggle)
        layout.addRow(QLabel('Are you using an eyetracker?'), self.eyetrackingtoggle)
        layout.addRow(QLabel('Current output directory:'), self.wdlabel)
        layout.addRow(QLabel('Click to choose where to save your output:'), self.wdset)
        layout.addRow(self.quitbutton, self.submit)

        # Add form layout to overarching layout
        over_layout.addLayout(layout)

        self.setLayout(over_layout)

    def clickbox(self):

        if self.buttontoggle.isChecked():
            self.buttonboxstate = 'Yes'
        else:
            self.buttonboxstate = 'No'

        if self.eyetrackingtoggle.isChecked():
            self.eyetracking = 'Yes'
        else:
            self.eyetracking = 'No'

    def submitsettings(self):

        person = memoryp.NbParticipant(self.idform.text(),
                                       self.trialsin.text(),
                                       self.sessionin.text(),
                                       self.wd,
                                       self.design.currentText(),
                                       self.blocksin.text(),
                                       self.buttonboxstate,
                                       self.eyetracking)

        self.exp = memorygui.NbExp(person)
        self.exp.show()
        self.hide()
