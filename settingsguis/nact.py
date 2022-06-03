from PyQt6.QtWidgets import QLabel, QSpinBox, QFormLayout, QVBoxLayout, QCheckBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from settingsguis import settings

from participants import nactp
from expguis import nactgui


class NACTSettings(settings.Settings):  # TODO Make this negative attention specific

    def __init__(self):
        super().__init__()

        # setting  the geometry of window
        self.setGeometry(0, 0, 650, 350)

        # center window
        self.centerscreen()

        # STT default
        self.stt = 0

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

        # Pairs input
        self.pairsin = QSpinBox()
        self.pairsin.setSpecialValueText('30')

        # ST Trials input
        self.trialsin = QSpinBox()
        self.trialsin.setSpecialValueText('3')

        # ST Trials input
        self.stttoggle = QCheckBox('STT?', self)
        self.stttoggle.stateChanged.connect(self.clickBox)

        # Make form layout for all the settingsguis
        layout = QFormLayout()

        layout.addRow(QLabel('Subject ID:'), self.idform)
        layout.addRow(QLabel('Number of word pairs (Max: 30):'), self.pairsin)
        layout.addRow(QLabel('Number of study-test trials:'), self.trialsin)
        layout.addRow(QLabel('Do you want an STT trial?:'), self.stttoggle)
        layout.addRow(QLabel('Where do you want to save the output?'), self.wdset)
        layout.addRow(self.submit, self.quitbutton)

        # Add form layout to overarching layout
        over_layout.addLayout(layout)

        self.setLayout(over_layout)

    def clickBox(self):

        if self.stttoggle.isChecked():
            self.stt = 1
        else:
            self.stt = 0

    def submitsettings(self):

        person = nactp.NACTParticipant(self.idform.text(),
                                       self.pairsin.text(),
                                       self.wdset.text(),
                                       'Negative Attention Capture',
                                       self.trialsin.text(),
                                       self.stt)

        self.exp = nactgui.NACTExp(person)
        self.exp.show()
        self.hide()
