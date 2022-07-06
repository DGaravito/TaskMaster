from PyQt6.QtWidgets import QLabel, QSpinBox, QComboBox

from settingsguis import settings

import participants
import expguis


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
        self.layout.addRow(QLabel('Are you using an eyetracker?'), self.eyetrackingtoggle)
        self.layout.addRow(QLabel('Enter the output directory:'), self.wd)
        self.layout.addRow(self.quitbutton, self.submit)

        # Add form layout to overarching layout
        self.over_layout.addLayout(self.layout)

        self.setLayout(self.over_layout)

    def submitsettings(self):

        person = participants.memoryp.PrParticipant(self.idform.text(),
                                                    self.pairsin.text(),
                                                    self.sessionin.text(),
                                                    self.wd.text(),
                                                    'Pair Recall Memory',
                                                    self.trialsin.text(),
                                                    self.stt,
                                                    self.eyetracking)

        self.exp = expguis.memorygui.PrExp(person)
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
        self.layout.addRow(QLabel('Are you using a button-box instead of the keyboard?'), self.buttontoggle)
        self.layout.addRow(QLabel('Are you using an eyetracker?'), self.eyetrackingtoggle)
        self.layout.addRow(QLabel('Enter the output directory:'), self.wd)
        self.layout.addRow(self.quitbutton, self.submit)

        # Add form layout to overarching layout
        self.over_layout.addLayout(self.layout)

        self.setLayout(self.over_layout)

    def taskchange(self):

        self.task = self.design.currentText()

    def submitsettings(self):

        person = participants.memoryp.NbParticipant(self.idform.text(),
                                                    self.trialsin.text(),
                                                    self.sessionin.text(),
                                                    self.wd.text(),
                                                    self.design.currentText(),
                                                    self.blocksin.text(),
                                                    self.buttonboxstate,
                                                    self.eyetracking)

        self.exp = expguis.memorygui.NbExp(person)
        self.exp.show()
        self.hide()
