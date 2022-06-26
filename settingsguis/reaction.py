from PyQt6.QtWidgets import QLabel, QSpinBox, QCheckBox, QGridLayout

from settingsguis import settings

from participants import reactionp
from expguis import reactiongui


class SSSettings(settings.Settings):

    def __init__(self, task):
        super().__init__(task)

        # Reaction time input
        self.maxrtin = QSpinBox()
        self.maxrtin.setMaximum(2000)
        self.maxrtin.setValue(1500)

        # Make form layout for all the settingsguis
        self.layout.addRow(QLabel('Number of trials:'), self.trialsin)
        self.layout.addRow(QLabel('Maximum delay for signal (in milliseconds; max is 2000):'), self.maxrtin)
        self.layout.addRow(QLabel('Number of blocks:'), self.blocksin)
        self.layout.addRow(QLabel('Are you using a button-box instead of the keyboard?'), self.buttontoggle)
        self.layout.addRow(QLabel('Are you using an eyetracker?'), self.eyetrackingtoggle)
        self.layout.addRow(QLabel('Current output directory:'), self.wdlabel)
        self.layout.addRow(QLabel('Click to choose where to save your output:'), self.wdset)
        self.layout.addRow(self.quitbutton, self.submit)

        # Add form layout to overarching layout
        self.over_layout.addLayout(self.layout)

        self.setLayout(self.over_layout)

    def submitsettings(self):

        person = reactionp.SSParticipant(self.idform.text(),
                                         self.trialsin.text(),
                                         self.sessionin.text(),
                                         self.wd,
                                         'Stop-Signal Task',
                                         self.maxrtin.text(),
                                         self.blocksin.text(),
                                         self.buttonboxstate,
                                         self.eyetracking)

        self.exp = reactiongui.SSExp(person)
        self.exp.show()
        self.hide()


class EGNGSettings(settings.Settings):

    def __init__(self, task):
        super().__init__(task)

        # Add faces to layout
        facelayout = QGridLayout()

        facelayout.addWidget(self.happytoggle, 0, 0)
        facelayout.addWidget(self.sadtoggle, 0, 1)
        facelayout.addWidget(self.angertoggle, 1, 0)
        facelayout.addWidget(self.feartoggle, 1, 1)

        # Make form layout for all the settings
        self.layout.addRow(QLabel('Number of trials per block:'), self.trialsin)
        self.layout.addRow(QLabel('Number of blocks:'), self.blocksin)
        self.layout.addRow(QLabel('Which faces would you like to include?'), facelayout)
        self.layout.addRow(QLabel('Are you using a button-box instead of the keyboard?'), self.buttontoggle)
        self.layout.addRow(QLabel('Current output directory:'), self.wdlabel)
        self.layout.addRow(QLabel('Click to choose where to save your output:'), self.wdset)
        self.layout.addRow(self.quitbutton, self.submit)

        # Add form layout to overarching layout
        self.over_layout.addLayout(self.layout)

        self.setLayout(self.over_layout)

    def submitsettings(self):

        divisible = 0

        if self.happy == "Yes":
            divisible += 2

        if self.sad == "Yes":
            divisible += 2

        if self.angry == "Yes":
            divisible += 2

        if self.fear == "Yes":
            divisible += 2

        if (int(self.trialsin.text()) % divisible) == 0:
            person = reactionp.EGNGParticipant(self.idform.text(),
                                               self.trialsin.text(),
                                               self.sessionin.text(),
                                               self.wd,
                                               'Emo Go/No-Go',
                                               self.blocksin.text(),
                                               self.happy,
                                               self.sad,
                                               self.angry,
                                               self.fear,
                                               self.buttonboxstate,
                                               self.eyetracking)

            self.exp = reactiongui.EGNGExp(person)
            self.exp.show()
            self.hide()

        else:
            self.matherrordialog(2)


class GNGSettings(settings.Settings):

    def __init__(self, task):
        super().__init__(task)

        # Reaction time input
        self.maxrtin = QSpinBox()
        self.maxrtin.setMaximum(2000)
        self.maxrtin.setValue(1500)

        # Make form layout for all the settingsguis
        self.layout.addRow(QLabel('Number of trials:'), self.trialsin)
        self.layout.addRow(QLabel('Maximal reaction time (in milliseconds)?'), self.maxrtin)
        self.layout.addRow(QLabel('Number of blocks?'), self.blocksin)
        self.layout.addRow(QLabel('Current output directory:'), self.wdlabel)
        self.layout.addRow(QLabel('Click to choose where to save your output:'), self.wdset)
        self.layout.addRow(self.quitbutton, self.submit)

        # Add form layout to overarching layout
        self.over_layout.addLayout(self.layout)

        self.setLayout(self.over_layout)

    def submitsettings(self):

        person = reactionp.GNGParticipant(self.idform.text(),
                                          self.trialsin.text(),
                                          self.sessionin.text(),
                                          self.wd,
                                          'Go/No-Go',
                                          self.maxrtin.text(),
                                          self.blocksin.text(),
                                          self.buttonboxstate,
                                          self.eyetracking,
                                          self.fmri)

        self.exp = reactiongui.GNGExp(person)
        self.exp.show()
        self.hide()
