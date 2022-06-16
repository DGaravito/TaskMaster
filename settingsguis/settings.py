from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QSpinBox, QLineEdit, QVBoxLayout, QDialog, \
    QCheckBox, QFileDialog
from PyQt6.QtCore import Qt

from os import path


class WDErrorBox(QDialog):
    """
    This is a popup window that may come up after the settingsguis window checks to see if the directory that the user
    put in is actually a directory. If not, this popup lets the user know that they goofed.
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Error')

        # Make  layout
        dialayout = QVBoxLayout()

        # Make labels for text
        self.mainerror = QLabel('It looks like you entered an invalid directory!')
        self.mainerror.setStyleSheet('padding :5px')

        self.instruction = QLabel('Use the settings window to select a directory to save your output to.')
        self.instruction.setStyleSheet('padding :5px')

        # Add stuff to overarching layout
        dialayout.addWidget(self.mainerror),
        dialayout.addWidget(self.instruction)

        self.setLayout(dialayout)


class FileErrorBox(QDialog):
    """
    This is a popup window that may come up after the settingsguis window checks to see if the file that the user
    will create alreaedy exists. If so, this popup lets the user know that they goofed and tells them to delete the
    old file or change their settings
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Error')

        # Make  layout
        dialayout = QVBoxLayout()

        # Make labels for text
        self.mainerror = QLabel('It looks like your file already exists!')
        self.mainerror.setStyleSheet('padding :5px')

        self.instruction = QLabel('Either delete the old file, pick a new directory, or change your ID, session name' +
                                  ', or task.')
        self.instruction.setStyleSheet('padding :5px')

        # Add stuff to overarching layout
        dialayout.addWidget(self.mainerror),
        dialayout.addWidget(self.instruction)

        self.setLayout(dialayout)


class MathErrorBox(QDialog):
    """
    This is a popup window that may come up after the settingsguis window checks to see if the math works out.
    Condition is determined by the settingsguis GUI that has the error and the settingsguis within that. For example,
    PBT needs to be divisible by 4 because there are four pictures. Framing needs to be divisible by 2 if gains and
    losses are enabled, divisible by 3 if FTT is enabled, and divisible by 6 if both are enabled.
    """

    def __init__(self, state):
        super().__init__()

        self.setWindowTitle('Input Error')

        # Make  layout
        dialayout = QVBoxLayout()

        # Make labels for text

        self.mainerror = QLabel('Your number of trials isn\'t compatible with the settings and/or task you chose!')
        self.mainerror.setStyleSheet('padding :5px')

        match state:

            case 1:

                followupstring = 'There are 4 pictures for stimuli, so the total number of trials must be ' \
                                 'divisible by 4.'

            case 2:

                followupstring = 'You enabled gains and losses, so your number of trials should be divisible by 2.'

            case 3:

                followupstring = 'You enabled FTT, so your number of trials should be divisible by 3.'

            case 4:

                followupstring = 'You enabled FTT and need gains and losses, so your number of trials should' \
                                 ' be divisible by 6 (minimum Gist, Mixed, and Verbatim version of 1 gain and' \
                                 ' 1 loss question.'

            case 5:

                followupstring = 'There are 4 task difficulty levels, so the total number of trials must be ' \
                                 'divisible by 3 (enough for 1 to be compared to 2, 3, and 4) in the original task.'

            case 6:

                followupstring = 'There are 4 task difficulty levels, so the total number of trials must be ' \
                                 'divisible by 6 (enough for each difficulty to be compared) in the alternate task.'

            case 7:

                followupstring = 'It seems that the number of high value and low trials you entered means that ' \
                                 'the participant could end up with less money than the minimum allowed.' \
                                 '\n(# of low value trials X $0.15) + (# of low value trials X $0.03) <= ' \
                                 'starting money - minimum money that a participant can leave with.'

            case _:

                followupstring = 'I don\'t know what you put, but the math doesn\'t work out'

        self.followup = QLabel(followupstring)
        self.followup.setStyleSheet('padding :5px')

        # Add stuff to overarching layout
        dialayout.addWidget(self.mainerror),
        dialayout.addWidget(self.followup)

        self.setLayout(dialayout)


class Settings(QWidget):
    """
    Main class for the settingsguis window. This guy has all of the characteristics and things that every settingsguis
    window should have: A quit button, a submit settingsguis button, a minimum window size, a function for checking
    that the user inputted a valid directory, etc.
    """

    def __init__(self, task):
        super().__init__()

        # Window title
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # setting the geometry of window
        self.setGeometry(0, 0, 700, 400)

        # center window
        self.centerscreen()

        # Defaults for various tasks and options
        self.task = task
        self.buttonboxstate = 'No'
        self.outcome = 'No'
        self.eyetracking = 'No'
        self.fmri = 'No'
        self.ftt = 'No'

        # Default directory
        self.wd = 'No directory selected'

        # Quit button
        self.quitbutton = QPushButton('Quit')
        self.quitbutton.clicked.connect(QApplication.instance().quit)
        self.quitbutton.resize(self.quitbutton.sizeHint())

        # ID
        self.idform = QLineEdit()
        self.idform.setText('9999')

        # Session form
        self.sessionin = QLineEdit()
        self.sessionin.setText('Pretest')

        # Button check
        self.buttontoggle = QCheckBox()
        self.buttontoggle.stateChanged.connect(self.clickbox)

        # Eyetracking check
        self.eyetrackingtoggle = QCheckBox()
        self.eyetrackingtoggle.stateChanged.connect(self.clickbox)

        # fMRI check
        self.fmritoggle = QCheckBox()
        self.fmritoggle.stateChanged.connect(self.clickbox)

        # Blocks input
        self.blocksin = QSpinBox()
        self.blocksin.setSpecialValueText('1')

        # WD input
        self.wdset = QPushButton('Select Directory')
        self.wdset.clicked.connect(self.fileselect)
        self.wdlabel = QLabel(self.wd)

        # Submit button
        self.submit = QPushButton('Submit')
        self.submit.clicked.connect(self.checksettings)

        # Add in elements
        self.elements()

        # Show all elements
        self.show()

    def elements(self):
        """
        This is a placeholder function. All settings windows will have some unique settings stuff for the window.
        This is intentionally left blank for that reason.
        """

    def centerscreen(self):
        """
        Finds the geometry of the computer's screen and moves the window to the center of it
        """

        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def clickbox(self):
        """
        This is a function that will activate whenever you click on one of the checkboxes
        """

        print('if you see this, panic')

    def checksettings(self):
        """
        Once you hit submit, the following function is called, which figures out if the selected directory is valid. If
        not, it calls the directory error function. If the directory is valid, it then checks if a file exists in that
        location that would be overwritten. If there is, it calls the file error function. If there is not pre-existing
        file, then it calls the function that submits the settings.
        """

        if path.isdir(self.wd):

            if path.isfile(self.wd + '/' + self.idform.text() + '_' + self.task + '_' + self.sessionin.text() +
                           '.xlsx'):
                self.fileerrordialog()

            else:
                self.submitsettings()

        else:
            self.wderrordialog()

    def wderrordialog(self):
        """
        This function activates if there is the output directory submitted is not valid
        """

        error = WDErrorBox()

        error.exec()

    def fileerrordialog(self):
        """
        This function activates if the output directory is valid but a file exists there that would be overwritten if
        the program were to run with the selected task.
        """

        error = FileErrorBox()

        error.exec()

    def matherrordialog(self, state):
        """
        This function activates if there is a problem with the settings such that the math doesn't work out. It takes
        one argument which determines the text of the resulting error dialog window.
        :param state: an integer that indicates what type of math error happened and what the resulting text in the
        error should be.
        """

        error = MathErrorBox(state)

        error.exec()

    def submitsettings(self):
        """
        This function activates if you hit submit on a settings window and both the directory is valid and a file
        doesn't already exist. Since the resulting actions will depend on the selected task, this is left blank here.
        """

        print('If you see this, panic')

    def fileselect(self):
        """
        This function creates a dialog window to select a directory that will be the output directoty and then sets
        the class variable (and associated QLabel) for the working directory to the directory you chose
        """

        self.wd = str(QFileDialog.getExistingDirectory(self, 'Select Directory'))
        self.wdlabel.setText(self.wd)
