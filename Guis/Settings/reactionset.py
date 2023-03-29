from PyQt6.QtWidgets import QLabel, QSpinBox, QGridLayout

from os import path
import glob

from Participants import reactionp

from Guis.Settings import settings
from Guis.Experiments import reactionexp


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
        # self.layout.addRow(QLabel('Are you using an eyetracker?'), self.eyetrackingtoggle)
        self.layout.addRow(QLabel('Current output directory:'), self.wdlabel)
        self.layout.addRow(QLabel('Click to choose where to save your output:'), self.wdset)
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
                                         self.controls.currentText(),
                                         self.eyetracking)

        self.exp = reactionexp.SSExp(person)
        self.exp.show()
        self.hide()


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
        self.layout.addRow(QLabel('Number of trials per sub-block (must be divisible by 4):'), self.trialsin)
        self.layout.addRow(QLabel('For above, put 48 to get 48 trials of Happy-Neutral, 48 of Neutral-Happy, etc.'))
        self.layout.addRow(QLabel('Number of blocks:'), self.blocksin)
        self.layout.addRow(QLabel('Which faces would you like to include?'), facelayout)
        # self.layout.addRow(QLabel('Are you using an eyetracker?'), self.eyetrackingtoggle)
        self.layout.addRow(QLabel('Current picture directory:'), self.picdlabel)
        self.layout.addRow(QLabel('Click to select where your pictures are:'), self.picdset)
        self.layout.addRow(QLabel('Remember, pictures should be formatted like the following examples:'))
        self.layout.addRow(QLabel('Fearful_M_NW_12.png - This is a picture of a non-white male making a fearful face.'))
        self.layout.addRow(QLabel('Angry_F_W_21.png - This is a picture of a white female making an angry face.'))
        self.layout.addRow(QLabel('NFNeutral_7.png - This is a picture of a neutral non-face.'))
        self.layout.addRow(QLabel('Current output directory:'), self.wdlabel)
        self.layout.addRow(QLabel('Click to choose where to save your output:'), self.wdset)
        self.layout.addRow(self.quitbutton, self.submit)

        # Add form layout to overarching layout
        self.over_layout.addLayout(self.layout)

        self.setLayout(self.over_layout)

    def submitsettings(self):

        # check to make sure at least one emotion is toggled on
        if self.happy == 'Yes' or self.sad == 'Yes' or self.fear == 'Yes' or self.angry == 'Yes':

            # check if the picture directory is valid
            if path.isdir(self.picd):

                # if so, add an ending / to make things easier later
                picpathstring = self.picd + '/'

                # check to make sure there are PNGs in the picture directory
                if glob.glob(picpathstring + '*.png'):

                    # get the strings for all of the files in the picture directory
                    fullfilelist = glob.glob(picpathstring + '*.png')

                    # Make lists of individual emotions for later
                    happystr = [picstr for picstr in fullfilelist if 'Happy' in picstr]
                    sadstr = [picstr for picstr in fullfilelist if 'Sad' in picstr]
                    angrystr = [picstr for picstr in fullfilelist if 'Angry' in picstr]
                    fearstr = [picstr for picstr in fullfilelist if 'Fearful' in picstr]
                    neustr = [picstr for picstr in fullfilelist if 'Neutral' in picstr]

                    # check to make sure that if the user toggled on an emotion, there is at least one picture with
                    # that emotion and at least one neutral picture
                    if (
                            (self.happy == 'No' or len(happystr) > 0) &
                            (self.sad == 'No' or len(sadstr) > 0) &
                            (self.angry == 'No' or len(angrystr) > 0) &
                            (self.fear == 'No' or len(fearstr) > 0) &
                            (len(neustr) > 0)
                    ):

                        # check to make sure the trials are divisible by 4
                        if (int(self.trialsin.text()) % 4) == 0:
                            person = reactionp.EGNGParticipant(self.idform.text(),
                                                               self.trialsin.text(),
                                                               self.sessionin.text(),
                                                               self.wd,
                                                               'Emo Go/No-Go',
                                                               self.blocksin.text(),
                                                               self.happy,
                                                               len(happystr),
                                                               self.sad,
                                                               len(sadstr),
                                                               self.angry,
                                                               len(angrystr),
                                                               self.fear,
                                                               len(fearstr),
                                                               len(neustr),
                                                               self.picd,
                                                               self.controls.currentText(),
                                                               self.eyetracking)

                            self.exp = reactionexp.EGNGExp(person)
                            self.exp.show()
                            self.hide()

                        else:
                            self.matherrordialog(8)

                    else:
                        self.formaterrordialog()

                else:
                    self.formaterrordialog()

            else:
                self.picdirerrordialog()

        else:
            self.selecterror()


class GNGSettings(settings.Settings):

    def __init__(self, task):
        super().__init__(task)

        # Reaction time input
        self.maxrtin = QSpinBox()
        self.maxrtin.setMaximum(2000)
        self.maxrtin.setValue(1500)

        # Make form layout for all the settingsguis
        self.layout.addRow(QLabel('Number of trials:'), self.trialsin)
        self.layout.addRow(QLabel('Number of blocks?'), self.blocksin)
        self.layout.addRow(QLabel('Current output directory:'), self.wdlabel)
        self.layout.addRow(QLabel('Click to choose where to save your output:'), self.wdset)
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
                                          self.blocksin.text(),
                                          self.controls.currentText(),
                                          self.eyetracking)

        self.exp = reactionexp.GNGExp(person)
        self.exp.show()
        self.hide()
