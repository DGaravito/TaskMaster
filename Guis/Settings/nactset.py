from PyQt6.QtWidgets import QLabel, QSpinBox

from Participants import nactp

from Guis.Settings import settings
from Guis.Experiments import nactexp


class NACTSettings(settings.Settings):

    def __init__(self, task):
        super().__init__(task)

        # Low Value Trials input
        self.lowtrialsin = QSpinBox()
        self.lowtrialsin.setRange(0, 1000)
        self.lowtrialsin.setValue(120)

        # High Value Trials input
        self.hightrialsin = QSpinBox()
        self.hightrialsin.setRange(0, 1000)
        self.hightrialsin.setValue(120)

        # minimum possible ending money input
        self.minmoneyin = QSpinBox()
        self.minmoneyin.setRange(0, 1000000)
        self.minmoneyin.setValue(3)

        # Make form layout for all the settingsguis
        self.layout.addRow(QLabel('Number of high value ($0.15) trials:'), self.hightrialsin)
        self.layout.addRow(QLabel('Number of low value ($0.03) trials:'), self.lowtrialsin)
        self.layout.addRow(QLabel('Participant starting money:'), self.smoneyin)
        self.layout.addRow(QLabel('Minimum money a participants could have at the end:'), self.minmoneyin)
        self.layout.addRow(QLabel('Are you using a button-box instead of the keyboard?'), self.buttontoggle)
        # self.layout.addRow(QLabel('Are you using an eyetracker?'), self.eyetrackingtoggle)
        self.layout.addRow(QLabel('Current output directory:'), self.wdlabel)
        self.layout.addRow(QLabel('Click to choose where to save your output:'), self.wdset)
        self.layout.addRow(self.quitbutton, self.submit)

        # Add form layout to overarching layout
        self.over_layout.addLayout(self.layout)

        self.setLayout(self.over_layout)

    def submitsettings(self):

        hightrials = int(self.hightrialsin.text())
        lowtrials = int(self.lowtrialsin.text())

        if ((.15*hightrials) + (.03 * lowtrials)) <= (float(self.smoneyin.text()) - float(self.minmoneyin.text())):

            person = nactp.NACTParticipant(self.idform.text(),
                                           self.sessionin.text(),
                                           self.wd,
                                           'Negative Attention Capture Task',
                                           hightrials,
                                           lowtrials,
                                           self.smoneyin.text(),
                                           self.buttonboxstate,
                                           self.eyetracking)

            self.exp = nactexp.NACTExp(person)
            self.exp.show()
            self.hide()

        else:
            self.matherrordialog(7)
