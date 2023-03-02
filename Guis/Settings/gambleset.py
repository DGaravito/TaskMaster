from PyQt6.QtWidgets import QLabel, QSpinBox, QComboBox

from adopy.tasks.cra import TaskCRA

from Participants import gamblep

from Guis.Settings import settings
from Guis.Experiments import gambleexp


class ARTTSettings(settings.Settings):

    def __init__(self, task):
        super().__init__(task)

        # probability input
        # self.probriskin = QLineEdit()
        # self.probriskin.setText('.13, .25, .38, .5, .75')
        self.probabilities = [.13, .25, .38, .5, .62, .75, .87]

        # proportion input
        # self.probambin = QLineEdit()
        # self.probambin.setText('.25, .5, .75')
        self.proportions = [.25, .5, .75]

        # Smallest reward input
        self.srewin = QSpinBox()
        self.srewin.setRange(0, 1000000)
        self.srewin.setValue(5)

        # Largest reward input
        self.lrewin = QSpinBox()
        self.lrewin.setRange(0, 1000000)
        self.lrewin.setValue(50)

        # Dropdown box for gains, losses, or both
        self.design = QComboBox()
        self.design.addItems(['Gains only', 'Losses only', 'Gains and Losses'])

        # Make form layout for all the settingsguis
        self.layout.addRow(QLabel('Number of trials per block:'), self.trialsin)
        self.layout.addRow(QLabel('Number of blocks:'), self.blocksin)
        # layout.addRow(QLabel('Enter the probablities for risky trials:'), self.probriskin)
        # layout.addRow(QLabel('Enter the proportions covered for ambiguous trials:'), self.probambin)
        self.layout.addRow(QLabel('Fixed reward/loss magnitude:'), self.srewin)
        self.layout.addRow(QLabel('Largest reward/loss possible:'), self.lrewin)
        self.layout.addRow(QLabel('What type of questions do you want?'), self.design)
        self.layout.addRow(QLabel('Do you want to use ADOPy?'), self.adopytoggle)
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
        """
        Checks to make sure the math works out for the submitted settings. If Gains and Losses is selected, then the
        number of trials should be divisible by 2. If only gains or losses is selected, then you can just be good to go.
        If the math fails, through the respective math error. If the user is good to go, make an ARTT participants with
        the user's settings and then replace the settings window with an ARTT window using the ARTT participants.
        """

        # riskstring = self.probriskin.text()
        # risklist = list(riskstring.split(", "))

        # ambstring = self.probambin.text()
        # amblist = list(ambstring.split(", "))

        if (
                (
                        (
                                int(
                                    self.trialsin.text()
                                ) % 2
                        ) == 0
                ) & (self.design.currentText() == 'Gains and Losses')
        ) | (self.design.currentText() in ['Gains only', 'Losses only']):
            person = gamblep.ARTTParticipant(self.idform.text(),
                                             self.trialsin.text(),
                                             self.sessionin.text(),
                                             self.wd.text(),
                                             TaskCRA(),
                                             self.probabilities,
                                             self.proportions,
                                             self.srewin.text(),
                                             self.lrewin.text(),
                                             self.design.currentText(),
                                             self.outcome,
                                             self.smoneyin.text(),
                                             self.blocksin.text(),
                                             self.adopystate,
                                             self.buttonboxstate,
                                             self.eyetracking,
                                             self.fmri)

            self.exp = gambleexp.ARTTExp(person)
            self.exp.show()
            self.hide()

        else:
            self.matherrordialog(2)


class RASettings(settings.Settings):

    def __init__(self, task):
        super().__init__(task)

        # Minimum input
        self.minin = QSpinBox()
        self.minin.setRange(0, 1000000)
        self.minin.setValue(1)

        # Maximum input
        self.maxin = QSpinBox()
        self.maxin.setRange(0, 1000000)
        self.maxin.setValue(30)

        # Make form layout for all the settingsguis
        self.layout.addRow(QLabel('Number of trials per block:'), self.trialsin)
        self.layout.addRow(QLabel('Number of blocks:'), self.blocksin)
        self.layout.addRow(QLabel('Smallest possible gain:'), self.minin)
        self.layout.addRow(QLabel('Largest possible gain:'), self.maxin)
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

        person = gamblep.RAParticipant(self.idform.text(),
                                       self.trialsin.text(),
                                       self.sessionin.text(),
                                       self.wd.text(),
                                       'Risk Aversion',
                                       self.minin.text(),
                                       self.maxin.text(),
                                       self.outcome,
                                       self.smoneyin.text(),
                                       self.blocksin.text(),
                                       self.buttonboxstate,
                                       self.eyetracking,
                                       self.fmri)

        self.exp = gambleexp.RAExp(person)
        self.exp.show()
        self.hide()


class FrameSettings(settings.Settings):

    def __init__(self, task):
        super().__init__(task)

        # min EV input
        self.minin = QSpinBox()
        self.minin.setRange(0, 1000000)
        self.minin.setValue(1)

        # max EV input
        self.maxin = QSpinBox()
        self.maxin.setRange(0, 1000000)
        self.maxin.setValue(50)

        # Dropdown box for gains, losses, or both
        self.design = QComboBox()
        self.design.addItems(['Gains only', 'Losses only', 'Gains and Losses'])

        # Make form layout for all the settingsguis
        self.layout.addRow(QLabel('Number of trials per block:'), self.trialsin)
        self.layout.addRow(QLabel('Number of blocks:'), self.blocksin)
        self.layout.addRow(QLabel('Minimum expected value:'), self.minin)
        self.layout.addRow(QLabel('Maximum expected value:'), self.maxin)
        self.layout.addRow(QLabel('What type of questions do you want?'), self.design)
        self.layout.addRow(QLabel('Do you want FTT truncations (i.e., Gist, Mixed, Verbatim)?'), self.ftttoggle)
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
                (self.design.currentText() == 'Gains and Losses') &
                (self.ftt == 'Yes') &
                int(self.trialsin.text()) % 6 != 0
        ):

            self.matherrordialog(4)

        elif (self.ftt == 'Yes') & (int(self.trialsin.text()) % 3 != 0):

            self.matherrordialog(3)

        elif (self.design.currentText() == 'Gains and Losses') & (int(self.trialsin.text()) % 2 != 0):

            self.matherrordialog(2)

        else:

            person = gamblep.FrameParticipant(self.idform.text(),
                                              self.trialsin.text(),
                                              self.sessionin.text(),
                                              self.wd.text(),
                                              'Framing Task',
                                              self.minin.text(),
                                              self.maxin.text(),
                                              self.design.currentText(),
                                              self.ftt,
                                              self.outcome,
                                              self.smoneyin.text(),
                                              self.blocksin.text(),
                                              self.buttonboxstate,
                                              self.eyetracking,
                                              self.fmri)

            self.exp = gambleexp.FrameExp(person)
            self.exp.show()
            self.hide()
