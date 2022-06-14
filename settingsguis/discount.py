from PyQt6.QtWidgets import QLabel, QSpinBox, QFormLayout, QVBoxLayout, QComboBox, QCheckBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from adopy.tasks.dd import TaskDD

from settingsguis import settings
from participants import discountp
from expguis import discountgui


class DdSettings(settings.Settings):

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

        # Make form layout for all the settingsguis
        layout = QFormLayout()

        layout.addRow(QLabel('Subject ID:'), self.idform)
        layout.addRow(QLabel('Session name/number (enter \'Practice\' to not have output):'), self.sessionin)
        layout.addRow(QLabel('Number of trials per block:'), self.trialsin)
        layout.addRow(QLabel('Number of blocks:'), self.blocksin)
        layout.addRow(QLabel('Shortest delay in immediate option (weeks):'), self.imdin)
        layout.addRow(QLabel('Shortest delay in delayed option (weeks):'), self.sdin)
        layout.addRow(QLabel('Longest delay in delayed option (weeks):'), self.ldin)
        layout.addRow(QLabel('Smallest reward in immediate option:'), self.ssrewin)
        layout.addRow(QLabel('Biggest reward in delayed option:'), self.llrewin)
        layout.addRow(QLabel('Are you using a button-box instead of the keyboard?'), self.buttontoggle)
        layout.addRow(QLabel('Are you using an eyetracker?'), self.eyetrackingtoggle)
        layout.addRow(QLabel('Run in fMRI mode?'), self.fmritoggle)
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

        if self.fmritoggle.isChecked():
            self.fmri = 'Yes'
        else:
            self.fmri = 'No'

    def submitsettings(self):
        person = discountp.DdParticipant(self.idform.text(),
                                         self.trialsin.text(),
                                         self.sessionin.text(),
                                         self.wd,
                                         TaskDD(),
                                         self.imdin.text(),
                                         self.sdin.text(),
                                         self.ldin.text(),
                                         self.ssrewin.text(),
                                         self.llrewin.text(),
                                         self.blocksin.text(),
                                         self.buttonboxstate,
                                         self.eyetracking,
                                         self.fmri)

        self.exp = discountgui.DDiscountExp(person)
        self.exp.show()
        self.hide()


class PdSettings(settings.Settings):

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
        self.trialsin.setSpecialValueText('10')

        # Minimum input
        self.rewmin = QSpinBox()
        self.rewmin.setSpecialValueText('1')

        # Maximum input
        self.rewmax = QSpinBox()
        self.rewmax.setSpecialValueText('250')

        # Dropdown box for gains, losses, or both
        self.design = QComboBox()
        self.design.addItems(['Gains only', 'Losses only', 'Gains and Losses'])

        # checkbox for getting a random reward/loss
        self.outcometoggle = QCheckBox('', self)
        self.outcometoggle.stateChanged.connect(self.clickbox)

        # Starting money input
        self.smoneyin = QSpinBox()
        self.smoneyin.setSpecialValueText('25')

        # Make form layout for all the settingsguis
        layout = QFormLayout()

        layout.addRow(QLabel('Subject ID:'), self.idform)
        layout.addRow(QLabel('Session name/number (enter \'Practice\' to not have output):'), self.sessionin)
        layout.addRow(QLabel('Number of trials per block:'), self.trialsin)
        layout.addRow(QLabel('Number of blocks:'), self.blocksin)
        layout.addRow(QLabel('Smallest amount of money:'), self.rewmin)
        layout.addRow(QLabel('Biggest amount of money:'), self.rewmax)
        layout.addRow(QLabel('What type of questions do you want?'), self.design)
        layout.addRow(QLabel('Do you want to have an outcome randomly chosen?'), self.outcometoggle)
        layout.addRow(QLabel('Participant starting money (only used if above is checked):'), self.smoneyin)
        layout.addRow(QLabel('Are you using a button-box instead of the keyboard?'), self.buttontoggle)
        layout.addRow(QLabel('Are you using an eyetracker?'), self.eyetrackingtoggle)
        layout.addRow(QLabel('Run in fMRI mode?'), self.fmritoggle)
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

        if self.outcometoggle.isChecked():
            self.outcome = 'Yes'
        else:
            self.outcome = 'No'

        if self.eyetrackingtoggle.isChecked():
            self.eyetracking = 'Yes'
        else:
            self.eyetracking = 'No'

        if self.fmritoggle.isChecked():
            self.fmri = 'Yes'
        else:
            self.fmri = 'No'

    def submitsettings(self):

        if (
                (
                        (
                                int(
                                    self.trialsin.text()
                                ) % 2
                        ) == 0
                ) & (self.design.currentText() in ['Gains and Losses'])
        ) | (self.design.currentText() in ['Gains only', 'Losses only']):
            person = discountp.PdParticipant(self.idform.text(),
                                             self.trialsin.text(),
                                             self.sessionin.text(),
                                             self.wd,
                                             'Probability Discounting',
                                             self.design.currentText(),
                                             self.rewmin.text(),
                                             self.rewmax.text(),
                                             self.outcome,
                                             self.smoneyin.text(),
                                             self.blocksin.text(),
                                             self.buttonboxstate,
                                             self.eyetracking,
                                             self.fmri)

            self.exp = discountgui.PDiscountExp(person)
            self.exp.show()
            self.hide()

        else:
            self.matherrordialog(2)


class CEDTSettings(settings.Settings):

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
        self.trialsin.setSpecialValueText('12')

        # reward max input
        self.maxrewin = QSpinBox()
        self.maxrewin.setSpecialValueText('5')

        # checkbox for getting a random outcome
        self.outcometoggle = QCheckBox('', self)
        self.outcometoggle.stateChanged.connect(self.clickbox)

        # Dropdown box for stim names
        self.names = QComboBox()
        self.names.addItems(['a, e, i, u', 'Black, Red, Blue, Purple'])

        # Dropdown box for stim names
        self.version = QComboBox()
        self.version.addItems(['Original', 'Alternate'])

        # Make form layout for all the settingsguis
        layout = QFormLayout()

        layout.addRow(QLabel('Subject ID:'), self.idform)
        layout.addRow(QLabel('Session name/number (enter \'Practice\' to not have output):'), self.sessionin)
        layout.addRow(QLabel('Number of trials per block:'), self.trialsin)
        layout.addRow(QLabel('Number of blocks:'), self.blocksin)
        layout.addRow(QLabel('Largest reward amount:'), self.maxrewin)
        layout.addRow(QLabel('Do you want to have an outcome randomly chosen?'), self.outcometoggle)
        layout.addRow(QLabel('What names would you like to use for the stimuli?'), self.names)
        layout.addRow(QLabel('Would you like the original or alternate version?'), self.version)
        layout.addRow(QLabel('Are you using a button-box instead of the keyboard?'), self.buttontoggle)
        layout.addRow(QLabel('Are you using an eyetracker?'), self.eyetrackingtoggle)
        layout.addRow(QLabel('Run in fMRI mode?'), self.fmritoggle)
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

        if self.outcometoggle.isChecked():
            self.outcome = 'Yes'
        else:
            self.outcome = 'No'

        if self.eyetrackingtoggle.isChecked():
            self.eyetracking = 'Yes'
        else:
            self.eyetracking = 'No'

        if self.fmritoggle.isChecked():
            self.fmri = 'Yes'
        else:
            self.fmri = 'No'

    def submitsettings(self):

        if (
                ((int(self.trialsin.text()) % 6 == 0) & (self.version.currentText() == 'Alternate')) |
                ((int(self.trialsin.text()) % 3 == 0) & (self.version.currentText() == 'Original'))
        ):

            person = discountp.CEDParticipant(self.idform.text(),
                                              self.trialsin.text(),
                                              self.sessionin.text(),
                                              self.wd,
                                              'CogED Task',
                                              self.maxrewin.text(),
                                              self.outcome,
                                              self.names.currentText(),
                                              self.version.currentText(),
                                              self.blocksin.text(),
                                              self.buttonboxstate,
                                              self.eyetracking,
                                              self.fmri)

            self.exp = discountgui.CEDiscountExp(person)
            self.exp.show()
            self.hide()

        else:

            if self.version.currentText() == "Original":
                self.matherrordialog(5)

            else:
                self.matherrordialog(6)
