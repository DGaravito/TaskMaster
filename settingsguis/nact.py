from PyQt6.QtWidgets import QLabel, QSpinBox, QFormLayout, QVBoxLayout, QCheckBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from settingsguis import settings

from participants import nactp
from expguis import nactgui


class NACTSettings(settings.Settings):

    def __init__(self, task):
        super().__init__(task)

    def elements(self):
        # Make overarching layout
        over_layout = QVBoxLayout()

        # Make a label with instructions
        self.header = QLabel('Enter the appropriate values:', self)

        # setting font style and size
        self.header.setFont(QFont('Helvetica', 30))

        # center header
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add header to overarching layout

        over_layout.addWidget(self.header)

        # Low Value Trials input
        self.lowtrialsin = QSpinBox()
        self.lowtrialsin.setSpecialValueText('120')

        # High Value Trials input
        self.hightrialsin = QSpinBox()
        self.hightrialsin.setSpecialValueText('120')

        # Starting money input
        self.smoneyin = QSpinBox()
        self.smoneyin.setSpecialValueText('25')

        # Starting money input
        self.minmoneyin = QSpinBox()
        self.minmoneyin.setSpecialValueText('3')

        # Make form layout for all the settingsguis
        layout = QFormLayout()

        layout.addRow(QLabel('Subject ID:'), self.idform)
        layout.addRow(QLabel('Session name/number (enter \'Practice\' to not have output):'), self.sessionin)
        layout.addRow(QLabel('Number of high value ($0.15) trials:'), self.hightrialsin)
        layout.addRow(QLabel('Number of low value ($0.03) trials:'), self.lowtrialsin)
        layout.addRow(QLabel('Participant starting money:'), self.smoneyin)
        layout.addRow(QLabel('Minimum money a participant could have at the end:'), self.minmoneyin)
        layout.addRow(QLabel('Are you using a button-box instead of the keyboard?'), self.buttontoggle)
        layout.addRow(QLabel('Are you using an eyetracker?'), self.eyetrackingtoggle)
        layout.addRow(QLabel('Current output directory:'), self.wdlabel)
        layout.addRow(QLabel('Click to choose where to save your output:'), self.wdset)
        layout.addRow(self.quitbutton, self.submit)

        # Add form layout to overarching layout
        over_layout.addLayout(layout)

        self.setLayout(over_layout)

    def clickBox(self):

        if self.buttontoggle.isChecked():
            self.buttonboxstate = 'Yes'
        else:
            self.buttonboxstate = 'No'

        if self.eyetrackingtoggle.isChecked():
            self.eyetracking = 'Yes'
        else:
            self.eyetracking = 'No'

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

            self.exp = nactgui.NACTExp(person)
            self.exp.show()
            self.hide()

        else:
            self.matherrordialog(7)
