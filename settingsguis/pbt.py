from PyQt6.QtWidgets import QLabel

from settingsguis import settings

from participants import pbtp
from expguis import pbtgui


class PBTSettings(settings.Settings):

    def __init__(self, task):
        super().__init__(task)

        # Make form layout for all the settingsguis
        self.layout.addRow(QLabel('Number of blocks:'), self.blocksin)
        self.layout.addRow(QLabel('Number of trials per block (make sure it\'s divisible by 4):'), self.trialsin)
        self.layout.addRow(QLabel('Are you using a button-box instead of the keyboard?'), self.buttontoggle)
        self.layout.addRow(QLabel('Are you using an eyetracker?'), self.eyetrackingtoggle)
        self.layout.addRow(QLabel('Current output directory:'), self.wdlabel)
        self.layout.addRow(QLabel('Click to choose where to save your output:'), self.wdset)
        self.layout.addRow(self.quitbutton, self.submit)

        # Add form layout to overarching layout
        self.over_layout.addLayout(self.layout)

        self.setLayout(self.over_layout)

    def submitsettings(self):

        if (int(self.trialsin.text()) % 4) == 0:

            person = pbtp.PBTParticipant(self.idform.text(),
                                         self.trialsin.text(),
                                         self.sessionin.text(),
                                         self.wd,
                                         'Perceptual Bias Task',
                                         self.blocksin.text(),
                                         self.buttonboxstate,
                                         self.eyetracking)

            self.exp = pbtgui.PBTExp(person)
            self.exp.show()
            self.hide()

        else:
            self.matherrordialog(1)
