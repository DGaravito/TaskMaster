from PyQt6.QtWidgets import QLabel, QSpinBox, QComboBox

from Participants import memoryp

from Guis.Settings import settings
from Guis.Experiments import memoryexp


class PrSettings(settings.Settings):

    def __init__(self, task):
        super().__init__(task)

        # Pairs input
        self.pairsin = QSpinBox()
        self.pairsin.setValue(30)
        self.pairsin.setRange(10, 30)

        # Make form layout for all the settingsguis
        self.layout.addRow(QLabel('Number of word pairs (Max: 30):'), self.pairsin)
        self.layout.addRow(QLabel('Number of study-test trials:'), self.trialsin)
        self.layout.addRow(QLabel('Do you want an STT trial?'), self.stttoggle)
        # self.layout.addRow(QLabel('Are you using an eyetracker?'), self.eyetrackingtoggle)
        self.layout.addRow(QLabel('Current output directory:'), self.wdlabel)
        self.layout.addRow(QLabel('Click to choose where to save your output:'), self.wdset)
        self.layout.addRow(self.quitbutton, self.submit)

        # Add form layout to overarching layout
        self.over_layout.addLayout(self.layout)

        self.setLayout(self.over_layout)

    def submitsettings(self):

        person = memoryp.PrParticipant(self.idform.text(),
                                       self.pairsin.text(),
                                       self.sessionin.text(),
                                       self.wd,
                                       'Pair Recall Memory',
                                       self.trialsin.text(),
                                       self.stt,
                                       self.eyetracking)

        self.exp = memoryexp.PrExp(person)
        self.exp.show()
        self.hide()


class NBackSettings(settings.Settings):

    def __init__(self, task):
        super().__init__(task)

        # Dropdown box for gains, losses, or both
        self.design = QComboBox()
        self.design.addItems(['1-back', '2-back', '3-back', '4-back'])
        self.design.currentIndexChanged.connect(self.taskchange)

        # Make form layout for all the settingsguis
        self.layout.addRow(QLabel('Number of trials per block:'), self.trialsin)
        self.layout.addRow(QLabel('Number of blocks:'), self.blocksin)
        self.layout.addRow(QLabel('Type of n-Back:'), self.design)
        self.layout.addRow(QLabel('Do you want feedback on participant performance?'), self.feedtoggle)
        # self.layout.addRow(QLabel('Are you using an eyetracker?'), self.eyetrackingtoggle)
        self.layout.addRow(QLabel('Current output directory:'), self.wdlabel)
        self.layout.addRow(QLabel('Click to choose where to save your output:'), self.wdset)
        self.layout.addRow(self.quitbutton, self.submit)

        # Add form layout to overarching layout
        self.over_layout.addLayout(self.layout)

        self.setLayout(self.over_layout)

    def taskchange(self):

        self.task = self.design.currentText()

    def submitsettings(self):

        person = memoryp.NbParticipant(self.idform.text(),
                                       self.trialsin.text(),
                                       self.sessionin.text(),
                                       self.wd,
                                       self.design.currentText(),
                                       self.feedback,
                                       self.blocksin.text(),
                                       self.eyetracking,
                                       self.controls.currentText())

        self.exp = memoryexp.NbExp(person)
        self.exp.show()
        self.hide()


class DSSettings(settings.Settings):

    def __init__(self, task):
        super().__init__(task)

        # Dropdown box for forwards/backwards testing
        self.testorder = QComboBox()
        self.testorder.addItems(['Forwards', 'Backwards'])

        # Dropdown box for increasing/static difficulty
        self.testdiff = QComboBox()
        self.testdiff.addItems(['Static', 'Increasing'])

        # Number entry for time limit to enter numbers
        self.timelimit = QSpinBox()
        self.timelimit.setValue(5000)
        self.timelimit.setRange(1000, 100000)

        # Make form layout for all the settingsguis
        self.layout.addRow(QLabel('Number of numbers per test:'), self.trialsin)
        self.layout.addRow(QLabel('Should difficulty increase (by one) with each test or stay static?'), self.testdiff)
        self.layout.addRow(QLabel('Should participants enter numbers forwards or backwards?'), self.testorder)
        self.layout.addRow(QLabel('Do you want feedback on participant performance?'), self.feedtoggle)
        self.layout.addRow(QLabel('How long, in ms, do you want to give the participant to respond?'), self.timelimit)
        self.layout.addRow(QLabel('Number of tests:'), self.blocksin)
        # self.layout.addRow(QLabel('Are you using an eyetracker?'), self.eyetrackingtoggle)
        self.layout.addRow(QLabel('Current output directory:'), self.wdlabel)
        self.layout.addRow(QLabel('Click to choose where to save your output:'), self.wdset)
        self.layout.addRow(self.quitbutton, self.submit)

        # Add form layout to overarching layout
        self.over_layout.addLayout(self.layout)

        self.setLayout(self.over_layout)

    def submitsettings(self):

        person = memoryp.DsParticipant(self.idform.text(),
                                       self.trialsin.text(),
                                       self.sessionin.text(),
                                       self.wd,
                                       'Digit Span',
                                       self.testorder.currentText(),
                                       self.testdiff.currentText(),
                                       self.feedback,
                                       self.timelimit.text(),
                                       self.blocksin.text(),
                                       self.eyetracking)

        self.exp = memoryexp.DsExp(person)
        self.exp.show()
        self.hide()
