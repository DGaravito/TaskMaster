from PyQt6.QtWidgets import QLabel, QDialog, QGridLayout, QVBoxLayout

from os import path
import glob

from Participants import dwellp

from Guis.Settings import settings
from Guis.Experiments import dwellexp


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
        matrixlayout = QGridLayout()

        matrixlayout.addWidget(self.happytoggle, 0, 0)
        matrixlayout.addWidget(self.sadtoggle, 0, 1)
        matrixlayout.addWidget(self.angertoggle, 1, 0)
        matrixlayout.addWidget(self.feartoggle, 1, 1)
        matrixlayout.addWidget(self.negtoggle, 2, 0)

        # Make form layout for all the settingsguis
        self.layout.addRow(QLabel('Number of blocks:'), self.blocksin)
        self.layout.addRow(QLabel('Number of trials per matrix type (see below) per block:'), self.trialsin)
        self.layout.addRow(QLabel('Which matrices would you like to include?'), matrixlayout)
        # self.layout.addRow(QLabel('Are you using an eyetracker?'), self.eyetrackingtoggle)
        self.layout.addRow(QLabel('Do you want to balance matrix pictures by sex?'), self.sexbalancetoggle)
        self.layout.addRow(QLabel('Do you want to balance matrix pictures by race?'), self.racebalancetoggle)
        self.layout.addRow(QLabel('Current output directory:'), self.wdlabel)
        self.layout.addRow(QLabel('Click to choose where to save your output:'), self.wdset)
        self.layout.addRow(self.quitbutton, self.submit)

        # Add form layout to overarching layout
        self.over_layout.addLayout(self.layout)

        self.setLayout(self.over_layout)

    def submitsettings(self):

        # check to make sure at least one emotion is toggled on
        if self.happy == 'Yes' or self.sad == 'Yes' or self.fear == 'Yes' or self.angry == 'Yes' or self.neg == 'Yes':

            # check if the picture directory is valid
            if path.isdir(self.picd):

                # if so, add an ending / to make things easier later
                picpathstring = self.picd + '/'

                # check to make sure there are PNGs in the picture directory
                if glob.glob(picpathstring + '*.png'):

                    # get the strings for all of the files in the picture directory
                    fullfilelist = glob.glob(picpathstring + '*.png')

                    # for each of those file strings, trim the path off of the strings to make the trimmed list
                    trimmedlist = [sub.replace(picpathstring, '') for sub in fullfilelist]

                    # Make lists of individual emotions for later
                    happystr = [picstr for picstr in trimmedlist if picstr.startswith('Happy')]
                    sadstr = [picstr for picstr in trimmedlist if picstr.startswith('Sad')]
                    angrystr = [picstr for picstr in trimmedlist if picstr.startswith('Angry')]
                    fearstr = [picstr for picstr in trimmedlist if picstr.startswith('Fearful')]
                    neustr = [picstr for picstr in trimmedlist if picstr.startswith('Neutral')]
                    nfnegstr = [picstr for picstr in trimmedlist if picstr.startswith('NFNegative')]
                    nfneustr = [picstr for picstr in trimmedlist if picstr.startswith('NFNeutral')]

                    # check to make sure that if the user toggled on an emotion, there is at least one picture with
                    # that emotion and at least one neutral picture
                    if (
                            (self.happy == 'No' or len(happystr) > 0) &
                            (self.sad == 'No' or len(sadstr) > 0) &
                            (self.angry == 'No' or len(angrystr) > 0) &
                            (self.fear == 'No' or len(fearstr) > 0) &
                            (len(neustr) > 0) &
                            (self.neg == 'No' or len(nfnegstr) > 0)
                    ):

                        # check to make sure the trials are divisible by 4
                        if (
                                (self.happy == 'No' or len(happystr) >= 16) &
                                (self.sad == 'No' or len(sadstr) >= 16) &
                                (self.angry == 'No' or len(angrystr) >= 16) &
                                (self.fear == 'No' or len(fearstr) >= 16) &
                                (((self.happy == 'No') & (self.sad == 'No') & (self.angry == 'No') &
                                  (self.fear == 'No')) or len(neustr) >= 16) &
                                (self.neg == 'No' or (len(nfnegstr) >= 16) & len(nfneustr) >= 16)
                        ):
                            person = dwellp.DwellParticipant(self.idform.text(),
                                                             self.trialsin.text(),
                                                             self.sessionin.text(),
                                                             self.wd,
                                                             'Dwell',
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
                                                             self.neg,
                                                             len(nfnegstr),
                                                             len(nfneustr),
                                                             self.sexbalancing,
                                                             self.racebalancing,
                                                             self.picd,
                                                             self.buttonboxstate,
                                                             self.eyetracking)

                            self.exp = dwellexp.DwellExp(person)
                            self.exp.show()
                            self.hide()

                        else:
                            self.matherrordialog(9)

                    else:
                        self.formaterrordialog()

                else:
                    self.formaterrordialog()

            else:
                self.picdirerrordialog()

        else:
            self.selecterror()
