from PyQt6.QtWidgets import QLabel, QSpinBox, QFormLayout, QVBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from settingsguis import settings

from participants import beadsp
from expguis import beadsgui


class BeadsSettings(settings.Settings):

    def __init__(self, task):
        super().__init__(task)

        # setting the geometry of window
        self.setGeometry(0, 0, 650, 350)

        # center window
        self.centerscreen()

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

        # ST Trials input
        self.trialsin = QSpinBox()
        self.trialsin.setSpecialValueText('3')

        # Make form layout for all the settingsguis
        layout = QFormLayout()

        layout.addRow(QLabel('Subject ID:'), self.idform)
        layout.addRow(QLabel('Session name/number (enter \'Practice\' to not have output):'), self.sessionin)
        layout.addRow(QLabel('Number of trials:'), self.trialsin)
        layout.addRow(QLabel('Are you using an eyetracker?'), self.eyetrackingtoggle)
        layout.addRow(QLabel('Current output directory:'), self.wdlabel)
        layout.addRow(QLabel('Click to choose where to save your output:'), self.wdset)
        layout.addRow(self.quitbutton, self.submit)

        # Add form layout to overarching layout
        over_layout.addLayout(layout)

        self.setLayout(over_layout)

    def clickbox(self):

        if self.eyetrackingtoggle.isChecked():
            self.eyetracking = 'Yes'
        else:
            self.eyetracking = 'No'

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
