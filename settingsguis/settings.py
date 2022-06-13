from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QSpinBox, QLineEdit, QVBoxLayout, QDialog, \
    QCheckBox, QFileDialog
from PyQt6.QtCore import Qt

from os import path


class WDErrorBox(QDialog):
    """
    This is a popup window that may come up after the settingsguis window checks to see if the directory that the user
    put in is actually a directory. If not, this popup lets the user know that they goofed and gives them examples to
    reference when redoing the settingsguis window
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

    def __init__(self):
        super().__init__()

        # Window title
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # setting the minimum window size
        self.setMinimumSize(500, 500)

        # Defaults for various tasks and options
        self.buttonboxstate = 'No'
        self.outcome = 'No'
        self.eyetracking = 'No'
        self.fmri = 'No'
        self.ftt = 'No'

        # Default directory
        self.wd = 'No directory selected'

        # center window
        self.centerscreen()

        # Quit button
        self.quitbutton = QPushButton('Quit')
        self.quitbutton.clicked.connect(QApplication.instance().quit)
        self.quitbutton.resize(self.quitbutton.sizeHint())

        # ID
        self.idform = QLineEdit()
        self.idform.setText('9999')

        # Session form
        self.sessionin = QLineEdit()
        self.sessionin.setText('1')

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

    def centerscreen(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def clickbox(self):

        print('if you see this, panic')

    def checksettings(self):

        if path.isdir(self.wd):
            self.submitsettings()

        else:
            self.wderrordialog()

    def wderrordialog(self):

        error = WDErrorBox()

        error.exec()

    def submitsettings(self):
        print('If you see this, panic')

    def matherrordialog(self, state):

        error = MathErrorBox(state)

        error.exec()

    def fileselect(self):
        self.wd = str(QFileDialog.getExistingDirectory(self, 'Select Directory'))
        self.wdlabel.setText(self.wd)
