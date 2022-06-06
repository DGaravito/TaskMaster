from PyQt6.QtWidgets import QLabel, QSpinBox, QFormLayout, QVBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from settingsguis import settings

from participants import pbtp
from expguis import pbtgui


class PBTSettings(settings.Settings):

    def __init__(self):
        super().__init__()

        # setting  the geometry of window
        self.setGeometry(0, 0, 650, 350)

        # center window
        self.centerscreen()

        # Add in elements
        self.elements()

        # Show all elements
        self.show()

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

        # Trials input
        self.trialsin = QSpinBox()
        self.trialsin.setSpecialValueText('120')

        # Make form layout for all the settingsguis
        layout = QFormLayout()

        layout.addRow(QLabel('Subject ID:'), self.idform)
        layout.addRow(QLabel('Number of blocks:'), self.blocksin)
        layout.addRow(QLabel('Number of trials per block (make sure it\'s divisible by 4):'), self.trialsin)
        layout.addRow(QLabel('Are you using a button-box instead of the keyboard?:'), self.buttonbox)
        layout.addRow(QLabel('Where do you want to save the output?'), self.wdset)
        layout.addRow(self.submit, self.quitbutton)

        # Add form layout to overarching layout
        over_layout.addLayout(layout)

        self.setLayout(over_layout)

    def clickbox(self):

        if self.buttonbox.isChecked():
            self.buttonboxstate = 'Yes'
        else:
            self.buttonboxstate = 'No'

    def submitsettings(self):

        if (int(self.trialsin.text()) % 4) == 0:

            person = pbtp.PBTParticipant(self.idform.text(),
                                         self.trialsin.text(),
                                         self.wdset.text(),
                                         'Perceptual Bias Task',
                                         self.blocksin.text(),
                                         self.buttonboxstate)

            self.exp = pbtgui.PBTExp(person)
            self.exp.show()
            self.hide()

        else:
            self.matherrordialog(1)
