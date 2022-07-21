from PyQt6.QtWidgets import QLabel

from Participants import beadsp

from Guis.Settings import settings
from Guis.Experiments import beadsgui


class BeadsSettings(settings.Settings):

    def __init__(self, task):
        super().__init__(task)

        self.layout.addRow(QLabel('Number of trials:'), self.trialsin)
        self.layout.addRow(QLabel('Are you using an eyetracker?'), self.eyetrackingtoggle)
        self.layout.addRow(QLabel('Enter the output directory:'), self.wd)
        self.layout.addRow(self.quitbutton, self.submit)

        # Add form layout to overarching layout
        self.over_layout.addLayout(self.layout)

        self.setLayout(self.over_layout)

    def submitsettings(self):

        person = beadsp.BeadsParticipant(self.idform.text(),
                                         self.trialsin.text(),
                                         self.sessionin.text(),
                                         self.wd.text(),
                                         'Beads Task',
                                         self.eyetracking)

        self.exp = beadsgui.BeadsExp(person)
        self.exp.show()
        self.hide()
