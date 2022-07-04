from PyQt6.QtWidgets import QLabel, QSpinBox, QGridLayout, QDialog, QVBoxLayout

from settingsguis import settings

from participants import reactionp
from expguis import reactiongui


class SSSettings(settings.Settings):

    def __init__(self, task):
        super().__init__(task)

        # Reaction time input
        self.maxrtin = QSpinBox()
        self.maxrtin.setMaximum(2000)
        self.maxrtin.setValue(1500)

        # Make form layout for all the settingsguis
        self.layout.addRow(QLabel('Number of trials:'), self.trialsin)
        self.layout.addRow(QLabel('Maximum delay for signal (in milliseconds; max is 2000):'), self.maxrtin)
        self.layout.addRow(QLabel('Number of blocks:'), self.blocksin)
        self.layout.addRow(QLabel('Are you using a button-box instead of the keyboard?'), self.buttontoggle)
        self.layout.addRow(QLabel('Are you using an eyetracker?'), self.eyetrackingtoggle)
        self.layout.addRow(QLabel('Enter the output directory:'), self.wd)
        self.layout.addRow(self.quitbutton, self.submit)

        # Add form layout to overarching layout
        self.over_layout.addLayout(self.layout)

        self.setLayout(self.over_layout)

    def submitsettings(self):

        person = reactionp.SSParticipant(self.idform.text(),
                                         self.trialsin.text(),
                                         self.sessionin.text(),
                                         self.wd,
                                         'Stop-Signal Task',
                                         self.maxrtin.text(),
                                         self.blocksin.text(),
                                         self.buttonboxstate,
                                         self.eyetracking)

        self.exp = reactiongui.SSExp(person)
        self.exp.show()
        self.hide()


class EGNGSelectErrorBox(QDialog):
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
        self.mainerror = QLabel('It looks like you didn\'t select an emotional face!')
        self.mainerror.setStyleSheet('padding :5px')

        text = 'Please select at least one of happy, sad, angry, or fearful.'

        self.instruction = QLabel(text)
        self.instruction.setStyleSheet('padding :5px')

        # Add stuff to overarching layout
        dialayout.addWidget(self.mainerror),
        dialayout.addWidget(self.instruction)

        self.setLayout(dialayout)


class EGNGSettings(settings.Settings):

    def __init__(self, task):
        super().__init__(task)

        # Add faces to layout
        facelayout = QGridLayout()

        facelayout.addWidget(self.happytoggle, 0, 0)
        facelayout.addWidget(self.sadtoggle, 0, 1)
        facelayout.addWidget(self.angertoggle, 1, 0)
        facelayout.addWidget(self.feartoggle, 1, 1)

        # Make form layout for all the settings
        self.layout.addRow(QLabel('Number of trials per block (must be divisible by 4):'), self.trialsin)
        self.layout.addRow(QLabel('Number of blocks:'), self.blocksin)
        self.layout.addRow(QLabel('Which faces would you like to include?'), facelayout)
        self.layout.addRow(QLabel('Are you using a button-box instead of the keyboard?'), self.buttontoggle)
        self.layout.addRow(QLabel('Enter the output directory:'), self.wd)
        self.layout.addRow(self.quitbutton, self.submit)

        # Add form layout to overarching layout
        self.over_layout.addLayout(self.layout)

        self.setLayout(self.over_layout)

    def submitsettings(self):

        if self.happytoggle.isChecked() | self.sadtoggle.isChecked() | self.angertoggle.isChecked() | \
                self.feartoggle.isChecked():

            if (int(self.trialsin.text()) % 4) == 0:
                person = reactionp.EGNGParticipant(self.idform.text(),
                                                   self.trialsin.text(),
                                                   self.sessionin.text(),
                                                   self.wd,
                                                   'Emo Go/No-Go',
                                                   self.blocksin.text(),
                                                   self.happy,
                                                   self.sad,
                                                   self.angry,
                                                   self.fear,
                                                   self.buttonboxstate,
                                                   self.eyetracking)

                self.exp = reactiongui.EGNGExp(person)
                self.exp.show()
                self.hide()

            else:
                self.matherrordialog(8)

        else:
            self.selecterror()

    def selecterror(self):
        """
        This function activates if there is the output directory submitted is not valid
        """

        error = EGNGSelectErrorBox()

        error.exec()


class GNGSettings(settings.Settings):

    def __init__(self, task):
        super().__init__(task)

        # Reaction time input
        self.maxrtin = QSpinBox()
        self.maxrtin.setMaximum(2000)
        self.maxrtin.setValue(1500)

        # Make form layout for all the settingsguis
        self.layout.addRow(QLabel('Number of trials:'), self.trialsin)
        self.layout.addRow(QLabel('Maximal reaction time (in milliseconds)?'), self.maxrtin)
        self.layout.addRow(QLabel('Number of blocks?'), self.blocksin)
        self.layout.addRow(QLabel('Enter the output directory:'), self.wd)
        self.layout.addRow(self.quitbutton, self.submit)

        # Add form layout to overarching layout
        self.over_layout.addLayout(self.layout)

        self.setLayout(self.over_layout)

    def submitsettings(self):

        person = reactionp.GNGParticipant(self.idform.text(),
                                          self.trialsin.text(),
                                          self.sessionin.text(),
                                          self.wd,
                                          'Go/No-Go',
                                          self.maxrtin.text(),
                                          self.blocksin.text(),
                                          self.buttonboxstate,
                                          self.eyetracking,
                                          self.fmri)

        self.exp = reactiongui.GNGExp(person)
        self.exp.show()
        self.hide()
