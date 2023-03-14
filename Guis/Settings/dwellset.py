from PyQt6.QtWidgets import QLabel, QDialog, QGridLayout, QVBoxLayout

from Participants import pbtp

from Guis.Settings import settings
from Guis.Experiments import pbtexp


class DwellSelectErrorBox(QDialog):
    """
    This is a popup window that may come up after the Emo Go/NoGo window checks to see if the user select any of the
    emotional faces. If not, it tells the user to do so.
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Error')

        # Make  layout
        dialayout = QVBoxLayout()

        # Make labels for text
        self.mainerror = QLabel('It looks like you didn\'t select a matrix type to include!')
        self.mainerror.setStyleSheet('padding :5px')

        text = 'Please select at least one of the matrix types (e.g., happy).'

        self.instruction = QLabel(text)
        self.instruction.setStyleSheet('padding :5px')

        # Add stuff to overarching layout
        dialayout.addWidget(self.mainerror),
        dialayout.addWidget(self.instruction)

        self.setLayout(dialayout)


class DwellSettings(settings.Settings):

    def __init__(self, task):
        super().__init__(task)

        # Add matrix types to layout
        facelayout = QGridLayout()

        facelayout.addWidget(self.happytoggle, 0, 0)
        facelayout.addWidget(self.sadtoggle, 0, 1)
        facelayout.addWidget(self.angertoggle, 1, 0)
        facelayout.addWidget(self.feartoggle, 1, 1)
        facelayout.addWidget(self.nonfacetoggle, 2, 0)

        # Make form layout for all the settingsguis
        self.layout.addRow(QLabel('Number of blocks:'), self.blocksin)
        self.layout.addRow(QLabel('Number of trials per block (make sure it\'s divisible by 4):'), self.trialsin)
        self.layout.addRow(QLabel('Which matrices would you like to include?'), facelayout)
        # self.layout.addRow(QLabel('Are you using an eyetracker?'), self.eyetrackingtoggle)
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
                                         self.wd.text(),
                                         'Perceptual Bias Task',
                                         self.blocksin.text(),
                                         self.buttonboxstate,
                                         self.eyetracking)

            self.exp = pbtexp.PBTExp(person)
            self.exp.show()
            self.hide()

        else:
            self.matherrordialog(1)
