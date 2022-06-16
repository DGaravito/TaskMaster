from PyQt6.QtWidgets import QLabel

from settingsguis import settings

from participants import beadsp
from expguis import beadsgui


class BeadsSettings(settings.Settings):

    def __init__(self, task):
        super().__init__(task)

    def elements(self):

        self.layout.addRow(QLabel('Number of trials:'), self.trialsin)
        self.layout.addRow(QLabel('Are you using an eyetracker?'), self.eyetrackingtoggle)
        self.layout.addRow(QLabel('Current output directory:'), self.wdlabel)
        self.layout.addRow(QLabel('Click to choose where to save your output:'), self.wdset)
        self.layout.addRow(self.quitbutton, self.submit)

        # Add form layout to overarching layout
        self.over_layout.addLayout(self.layout)

        self.setLayout(self.over_layout)

    def submitsettings(self):

        person = beadsp.BeadsParticipant(self.idform.text(),
                                         self.trialsin.text(),
                                         self.sessionin.text(),
                                         self.wd,
                                         'Beads Task',
                                         self.eyetracking)

        self.exp = beadsgui.BeadsExp(person)
        self.exp.show()
        self.hide()
