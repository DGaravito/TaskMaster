from PyQt6.QtWidgets import QLabel

from Participants import stroopp

from Guis.Settings import settings
from Guis.Experiments import stroopexp


class StroopSettings(settings.Settings):

    def __init__(self, task):
        super().__init__(task)

        # Make form layout for all the settingsguis
        self.layout.addRow(QLabel('Number of trials per block:'), self.trialsin)
        self.layout.addRow(QLabel('How many pairs of Consistent and Inconsistent blocks do you want?:'), self.blocksin)
        # self.layout.addRow(QLabel('Are you using an eyetracker?'), self.eyetrackingtoggle)
        self.layout.addRow(QLabel('Current output directory:'), self.wdlabel)
        self.layout.addRow(QLabel('Click to choose where to save your output:'), self.wdset)
        self.layout.addRow(self.quitbutton, self.submit)

        # Add form layout to overarching layout
        self.over_layout.addLayout(self.layout)

        self.setLayout(self.over_layout)

    def submitsettings(self):
        person = stroopp.StroopParticipant(self.idform.text(),
                                           self.trialsin.text(),
                                           self.sessionin.text(),
                                           self.wd,
                                           self.blocksin.text(),
                                           self.eyetracking)

        self.exp = stroopexp.StroopExp(person)
        self.exp.show()
        self.hide()
