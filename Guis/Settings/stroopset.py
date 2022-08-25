from PyQt6.QtWidgets import QLabel, QSpinBox, QComboBox

from Participants import memoryp

from Guis.Settings import settings
from Guis.Experiments import memoryexp


class StroopSettings(settings.Settings):

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
        self.layout.addRow(QLabel('Are you using a button-box instead of the keyboard?'), self.buttontoggle)
        # self.layout.addRow(QLabel('Are you using an eyetracker?'), self.eyetrackingtoggle)
        self.layout.addRow(QLabel('Enter the output directory:'), self.wd)
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
                                       self.wd.text(),
                                       self.design.currentText(),
                                       self.blocksin.text(),
                                       self.buttonboxstate,
                                       self.eyetracking)

        self.exp = memoryexp.NbExp(person)
        self.exp.show()
        self.hide()
