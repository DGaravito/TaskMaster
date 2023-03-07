from PyQt6.QtWidgets import QLabel, QSpinBox, QComboBox, QCheckBox

# from adopy.tasks.dd import TaskDD

from Participants import discountp

from Guis.Settings import settings
from Guis.Experiments import discountexp


class DdSettings(settings.Settings):

    def __init__(self, task):
        super().__init__(task)

        # Smaller Sooner Delay input
        self.imdin = QSpinBox()
        self.imdin.setRange(0, 10000)
        self.imdin.setValue(0)

        # Larger Later smallest Delay input
        self.sdin = QSpinBox()
        self.sdin.setRange(0, 10000)
        self.sdin.setValue(1)

        # Larger Later largest Delay input
        self.ldin = QSpinBox()
        self.ldin.setRange(0, 10000)
        self.ldin.setValue(52)

        # Smallest reward input
        self.srewin = QSpinBox()
        self.srewin.setRange(0, 100000000)
        self.srewin.setValue(1)

        # Largest reward input
        self.lrewin = QSpinBox()
        self.lrewin.setRange(0, 100000000)
        self.lrewin.setValue(250)

        # Make form layout for all the settingsguis
        self.layout.addRow(QLabel('Number of trials per block:'), self.trialsin)
        self.layout.addRow(QLabel('Number of blocks:'), self.blocksin)
        self.layout.addRow(QLabel('Shortest delay in immediate option (weeks):'), self.imdin)
        self.layout.addRow(QLabel('Shortest delay in delayed option (weeks):'), self.sdin)
        self.layout.addRow(QLabel('Longest delay in delayed option (weeks):'), self.ldin)
        self.layout.addRow(QLabel('Smallest reward in immediate option:'), self.srewin)
        self.layout.addRow(QLabel('Biggest reward in delayed option:'), self.lrewin)
        # self.layout.addRow(QLabel('Do you want to use ADOPy?'), self.adopytoggle)
        self.layout.addRow(QLabel('Are you using a button-box instead of the keyboard?'), self.buttontoggle)
        # self.layout.addRow(QLabel('Are you using an eyetracker?'), self.eyetrackingtoggle)
        self.layout.addRow(QLabel('Run in fMRI mode?'), self.fmritoggle)
        self.layout.addRow(QLabel('Current output directory:'), self.wdlabel)
        self.layout.addRow(QLabel('Click to choose where to save your output:'), self.wdset)
        self.layout.addRow(self.quitbutton, self.submit)

        # Add form layout to overarching layout
        self.over_layout.addLayout(self.layout)

        self.setLayout(self.over_layout)

    def submitsettings(self):
        person = discountp.DdParticipant(self.idform.text(),
                                         self.trialsin.text(),
                                         self.sessionin.text(),
                                         self.wd.text(),
                                         'Delay Discounting',
                                         self.imdin.text(),
                                         self.sdin.text(),
                                         self.ldin.text(),
                                         self.srewin.text(),
                                         self.lrewin.text(),
                                         self.blocksin.text(),
                                         self.adopystate,
                                         self.buttonboxstate,
                                         self.eyetracking,
                                         self.fmri)

        self.exp = discountexp.DDiscountExp(person)
        self.exp.show()
        self.hide()


class PdSettings(settings.Settings):

    def __init__(self, task):
        super().__init__(task)

        # Minimum input
        self.rewmin = QSpinBox()
        self.rewmin.setRange(0, 10000000)
        self.rewmin.setValue(1)

        # Maximum input
        self.rewmax = QSpinBox()
        self.rewmax.setRange(0, 10000000)
        self.rewmax.setValue(250)

        # Dropdown box for gains, losses, or both
        self.design = QComboBox()
        self.design.addItems(['Gains only', 'Losses only', 'Gains and Losses'])

        # checkbox for getting a random reward/loss
        self.outcometoggle = QCheckBox('', self)
        self.outcometoggle.stateChanged.connect(self.clickbox)

        self.layout.addRow(QLabel('Number of trials per block:'), self.trialsin)
        self.layout.addRow(QLabel('Number of blocks:'), self.blocksin)
        self.layout.addRow(QLabel('Smallest amount of money:'), self.rewmin)
        self.layout.addRow(QLabel('Biggest amount of money:'), self.rewmax)
        self.layout.addRow(QLabel('What type of questions do you want?'), self.design)
        self.layout.addRow(QLabel('Do you want to have an outcome randomly chosen?'), self.outcometoggle)
        self.layout.addRow(QLabel('Participant starting money (only used if above is checked):'), self.smoneyin)
        self.layout.addRow(QLabel('Are you using a button-box instead of the keyboard?'), self.buttontoggle)
        # self.layout.addRow(QLabel('Are you using an eyetracker?'), self.eyetrackingtoggle)
        self.layout.addRow(QLabel('Run in fMRI mode?'), self.fmritoggle)
        self.layout.addRow(QLabel('Current output directory:'), self.wdlabel)
        self.layout.addRow(QLabel('Click to choose where to save your output:'), self.wdset)
        self.layout.addRow(self.quitbutton, self.submit)

        # Add form layout to overarching layout
        self.over_layout.addLayout(self.layout)

        self.setLayout(self.over_layout)

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
                                             self.wd.text(),
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

            self.exp = discountexp.PDiscountExp(person)
            self.exp.show()
            self.hide()

        else:
            self.matherrordialog(2)


class CEDTSettings(settings.Settings):

    def __init__(self, task):
        super().__init__(task)

        # reward max input
        self.maxrewin = QSpinBox()
        self.maxrewin.setRange(0, 100000000)
        self.maxrewin.setValue(5)

        # Dropdown box for stim names
        self.names = QComboBox()
        self.names.addItems(['a, e, i, u', 'Black, Red, Blue, Purple'])

        # Dropdown box for stim names
        self.version = QComboBox()
        self.version.addItems(['Original', 'Alternate'])

        self.layout.addRow(QLabel('Number of trials per block:'), self.trialsin)
        self.layout.addRow(QLabel('Number of blocks:'), self.blocksin)
        self.layout.addRow(QLabel('Largest reward amount:'), self.maxrewin)
        self.layout.addRow(QLabel('Do you want to have an outcome randomly chosen?'), self.outcometoggle)
        self.layout.addRow(QLabel('What names would you like to use for the stimuli?'), self.names)
        self.layout.addRow(QLabel('Would you like the original or alternate version?'), self.version)
        self.layout.addRow(QLabel('Are you using a button-box instead of the keyboard?'), self.buttontoggle)
        # self.layout.addRow(QLabel('Are you using an eyetracker?'), self.eyetrackingtoggle)
        self.layout.addRow(QLabel('Run in fMRI mode?'), self.fmritoggle)
        self.layout.addRow(QLabel('Current output directory:'), self.wdlabel)
        self.layout.addRow(QLabel('Click to choose where to save your output:'), self.wdset)
        self.layout.addRow(self.quitbutton, self.submit)

        # Add form layout to overarching layout
        self.over_layout.addLayout(self.layout)

        self.setLayout(self.over_layout)

    def submitsettings(self):

        if (
                ((int(self.trialsin.text()) % 6 == 0) & (self.version.currentText() == 'Alternate')) |
                ((int(self.trialsin.text()) % 3 == 0) & (self.version.currentText() == 'Original'))
        ):

            person = discountp.CEDParticipant(self.idform.text(),
                                              self.trialsin.text(),
                                              self.sessionin.text(),
                                              self.wd.text(),
                                              'CogED Task',
                                              self.maxrewin.text(),
                                              self.outcome,
                                              self.names.currentText(),
                                              self.version.currentText(),
                                              self.blocksin.text(),
                                              self.buttonboxstate,
                                              self.eyetracking,
                                              self.fmri)

            self.exp = discountexp.CEDiscountExp(person)
            self.exp.show()
            self.hide()

        else:

            if self.version.currentText() == "Original":
                self.matherrordialog(5)

            else:
                self.matherrordialog(6)
