from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QSpinBox, QLineEdit,\
    QFormLayout, QVBoxLayout, QCheckBox, QComboBox, QDialog
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from os import path

from adopy.tasks.dd import TaskDD
from adopy.tasks.cra import TaskCRA
import participant
import gui


class WDErrorBox(QDialog):
    """
    This is a popup window that may come up after the settings window checks to see if the directory that the user put
    in is actually a directory. If not, this popup lets the user know that they goofed and gives them examples to
    reference when redoing the settings window
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Error')

        # Make  layout
        dialayout = QVBoxLayout()

        # Make labels for text
        self.mainerror = QLabel('It looks like you entered an invalid directory!')
        self.mainerror.setStyleSheet('padding :5px')

        self.windowsex = QLabel('Windows example: \'C:\\Users\\dgara\\desktop\'')
        self.windowsex.setStyleSheet('padding :5px')

        self.macex = QLabel('Mac example: \'Users\\DGaravito\\desktop\'')
        self.macex.setStyleSheet('padding :5px')

        # Add stuff to overarching layout
        dialayout.addWidget(self.mainerror),
        dialayout.addWidget(self.windowsex),
        dialayout.addWidget(self.macex)

        self.setLayout(dialayout)


class MathErrorBox(QDialog):
    """
    This is a popup window that may come up after the settings window checks to see if the math works out. Condition is
    determined by the settings GUI that has the error and the settings within that. For example, PBT needs to be
    divisible by 4 because there are four pictures. Framing needs to be divisible by 2 if gains and losses are enabled,
    divisible by 3 if FTT is enabled, and divisible by 6 if both are enabled.
    """

    def __init__(self, state):
        super().__init__()

        self.setWindowTitle('Input Error')

        # Make  layout
        dialayout = QVBoxLayout()

        # Make labels for text

        self.mainerror = QLabel('Your number of trials isn\'t compatible with the settings and/or task you chose!')
        self.mainerror.setStyleSheet('padding :5px')

        if state == 1:

            self.followup = QLabel('There are 4 pictures for stimuli, so the total number of trials must be ' +
                                   'divisible by 4.')

        elif state == 2:

            self.followup = QLabel('You enabled gains and losses, so your number of trials should be divisible by 2.')

        elif state == 3:

            self.followup = QLabel('You enabled FTT, so your number of trials should be divisible by 3.')

        elif state == 4:

            self.followup = QLabel('You enabled FTT and need gains and losses, so your number of trials should be ' +
                                   ' divisible by 6 (minimum Gist, Mixed, and Verbatim version of 1 gain and 1 loss ' +
                                   ' question.')

        self.followup.setStyleSheet('padding :5px')

        # Add stuff to overarching layout
        dialayout.addWidget(self.mainerror),
        dialayout.addWidget(self.followup)

        self.setLayout(dialayout)


class Settings(QWidget):
    """
    Main class for the settings window. This guy has all of the characteristics and things that every settings window
    should have: A quit button, a submit settings button, a minimum window size, a function for checking that the user
    inputted a valid directory, etc.
    """

    def __init__(self):
        super().__init__()

        # Window title
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # setting the minimum window size
        self.setMinimumSize(500, 350)

        # center window
        self.centerscreen()

        # Quit button
        self.quitbutton = QPushButton('Quit')
        self.quitbutton.clicked.connect(QApplication.instance().quit)
        self.quitbutton.resize(self.quitbutton.sizeHint())

        # ID form
        self.idform = QLineEdit()
        self.idform.setText('9999')

        # WD input
        self.wdset = QLineEdit()
        self.wdset.setText('C:/Users/dgaravito/Desktop')

        # Submit button
        self.submit = QPushButton('Submit')
        self.submit.clicked.connect(self.checksettings)

    def centerscreen(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def checksettings(self):

        if path.isdir(self.wdset.text()):
            self.submitsettings()

        else:
            self.wderrordialog()

    def wderrordialog(self):

        error = WDErrorBox()

        error.exec()

    def submitsettings(self):
        print('If you see this, panic')


class DdSettings(Settings):

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
        self.trialsin.setSpecialValueText('10')

        # Immediate Delay input
        self.imdin = QSpinBox()
        self.imdin.setSpecialValueText('0')

        # Short Delay input
        self.sdin = QSpinBox()
        self.sdin.setSpecialValueText('1')

        # Long Delay input
        self.ldin = QSpinBox()
        self.ldin.setSpecialValueText('52')

        # SS reward input
        self.ssrewin = QSpinBox()
        self.ssrewin.setSpecialValueText('1')

        # LL reward input
        self.llrewin = QSpinBox()
        self.llrewin.setSpecialValueText('250')

        # Make form layout for all the settings
        layout = QFormLayout()

        layout.addRow(QLabel('Subject ID:'), self.idform)
        layout.addRow(QLabel('Number of trials:'), self.trialsin)
        layout.addRow(QLabel('Shortest delay in immediate option (weeks):'), self.imdin)
        layout.addRow(QLabel('Shortest delay in delayed option (weeks):'), self.sdin)
        layout.addRow(QLabel('Longest delay in delayed option (weeks):'), self.ldin)
        layout.addRow(QLabel('Smallest reward in immediate option:'), self.ssrewin)
        layout.addRow(QLabel('Biggest reward in delayed option:'), self.llrewin)
        layout.addRow(QLabel('Where do you want to save the output?'), self.wdset)
        layout.addRow(self.submit, self.quitbutton)

        # Add form layout to overarching layout
        over_layout.addLayout(layout)

        self.setLayout(over_layout)

    def submitsettings(self):
        person = participant.DdParticipant(self.idform.text(),
                                           self.trialsin.text(),
                                           self.wdset.text(),
                                           TaskDD(),
                                           self.imdin.text(),
                                           self.sdin.text(),
                                           self.ldin.text(),
                                           self.ssrewin.text(),
                                           self.llrewin.text())

        self.exp = gui.DDiscountExp(person)
        self.exp.show()
        self.hide()


class PdSettings(Settings):

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
        self.trialsin.setSpecialValueText('10')

        # Minimum input
        self.rewmin = QSpinBox()
        self.rewmin.setSpecialValueText('1')

        # Maximum input
        self.rewmax = QSpinBox()
        self.rewmax.setSpecialValueText('250')

        # Dropdown box for gains, losses, or both
        self.design = QComboBox()
        self.design.addItems(['Gains only', 'Losses only', 'Gains and Losses'])

        # Make form layout for all the settings
        layout = QFormLayout()

        layout.addRow(QLabel('Subject ID:'), self.idform)
        layout.addRow(QLabel('Number of trials:'), self.trialsin)
        layout.addRow(QLabel('Smallest amount of money:'), self.rewmin)
        layout.addRow(QLabel('Biggest amount of money:'), self.rewmax)
        layout.addRow(QLabel('What type of questions do you want?:'), self.design)
        layout.addRow(QLabel('Where do you want to save the output?'), self.wdset)
        layout.addRow(self.submit, self.quitbutton)

        # Add form layout to overarching layout
        over_layout.addLayout(layout)

        self.setLayout(over_layout)

    def submitsettings(self):
        person = participant.PdParticipant(self.idform.text(),
                                           self.trialsin.text(),
                                           self.wdset.text(),
                                           'Probability Discounting',
                                           self.design.currentText(),
                                           self.rewmin.text(),
                                           self.rewmax.text())

        self.exp = gui.PDiscountExp(person)
        self.exp.show()
        self.hide()


class CEDTSettings(Settings): # TODO Review CEDT for proper variables

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
        self.trialsin.setSpecialValueText('10')

        # Immediate Delay input
        self.imdin = QSpinBox()
        self.imdin.setSpecialValueText('0')

        # Short Delay input
        self.sdin = QSpinBox()
        self.sdin.setSpecialValueText('1')

        # Long Delay input
        self.ldin = QSpinBox()
        self.ldin.setSpecialValueText('52')

        # SS reward input
        self.ssrewin = QSpinBox()
        self.ssrewin.setSpecialValueText('1')

        # LL reward input
        self.llrewin = QSpinBox()
        self.llrewin.setSpecialValueText('250')

        # Make form layout for all the settings
        layout = QFormLayout()

        layout.addRow(QLabel('Subject ID:'), self.idform)
        layout.addRow(QLabel('Number of trials:'), self.trialsin)
        layout.addRow(QLabel('Shortest delay in immediate option (weeks):'), self.imdin)
        layout.addRow(QLabel('Shortest delay in delayed option (weeks):'), self.sdin)
        layout.addRow(QLabel('Longest delay in delayed option (weeks):'), self.ldin)
        layout.addRow(QLabel('Smallest reward in immediate option:'), self.ssrewin)
        layout.addRow(QLabel('Where do you want to save the output?'), self.wdset)
        layout.addRow(self.submit, self.quitbutton)

        # Add form layout to overarching layout
        over_layout.addLayout(layout)

        self.setLayout(over_layout)

    def submitsettings(self):
        person = participant.DdParticipant(self.idform.text(),
                                           self.trialsin.text(),
                                           self.wdset.text(),
                                           'CogED Task',
                                           self.imdin.text(),
                                           self.sdin.text(),
                                           self.ldin.text(),
                                           self.ssrewin.text(),
                                           self.llrewin.text())

        self.exp = gui.DDiscountExp(person)
        self.exp.show()
        self.hide()


class ARTTSettings(Settings):  # TODO Review ADOPy for required stuff - rework with pictures?

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
        self.trialsin.setSpecialValueText('10')

        # probability input
        # self.probriskin = QLineEdit()
        # self.probriskin.setText('.13, .25, .38, .5, .75')
        self.probabilities = [.13, .25, .38, .5, .62, .75, .87]

        # proportion input
        # self.probambin = QLineEdit()
        # self.probambin.setText('.25, .5, .75')
        self.proportions = [.25, .5, .75]

        # Smallest reward input
        self.srewin = QSpinBox()
        self.srewin.setSpecialValueText('5')

        # Largest reward input
        self.lrewin = QSpinBox()
        self.lrewin.setSpecialValueText('50')

        # Dropdown box for gains, losses, or both
        self.design = QComboBox()
        self.design.addItems(['Gains only', 'Losses only', 'Gains and Losses'])

        # Make form layout for all the settings
        layout = QFormLayout()

        layout.addRow(QLabel('Subject ID:'), self.idform)
        layout.addRow(QLabel('Number of trials:'), self.trialsin)
        # layout.addRow(QLabel('Enter the probablities for risky trials:'), self.probriskin)
        # layout.addRow(QLabel('Enter the proportions covered for ambiguous trials:'), self.probambin)
        layout.addRow(QLabel('Fixed reward/loss magnitude:'), self.srewin)
        layout.addRow(QLabel('Largest reward/loss possible:'), self.lrewin)
        layout.addRow(QLabel('What type of questions do you want?:'), self.design)
        layout.addRow(QLabel('Where do you want to save the output?'), self.wdset)
        layout.addRow(self.submit, self.quitbutton)

        # Add form layout to overarching layout
        over_layout.addLayout(layout)

        self.setLayout(over_layout)

    def submitsettings(self):

        # riskstring = self.probriskin.text()
        # risklist = list(riskstring.split(", "))

        # ambstring = self.probambin.text()
        # amblist = list(ambstring.split(", "))

        person = participant.ARTTParticipant(self.idform.text(),
                                             self.trialsin.text(),
                                             self.wdset.text(),
                                             TaskCRA(),
                                             self.probabilities,
                                             self.proportions,
                                             self.srewin.text(),
                                             self.lrewin.text(),
                                             self.design.currentText())

        self.exp = gui.ARTTExp(person)
        self.exp.show()
        self.hide()


class RASettings(Settings):

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

        # Trials input
        self.trialsin = QSpinBox()
        self.trialsin.setSpecialValueText('30')

        # Minimum input
        self.minin = QSpinBox()
        self.minin.setSpecialValueText('1')

        # Maximum input
        self.maxin = QSpinBox()
        self.maxin.setSpecialValueText('30')

        # Make form layout for all the settings
        layout = QFormLayout()

        layout.addRow(QLabel('Subject ID:'), self.idform)
        layout.addRow(QLabel('Number of trials:'), self.trialsin)
        layout.addRow(QLabel('Smallest possible gain:'), self.minin)
        layout.addRow(QLabel('Largest possible gain:'), self.maxin)
        layout.addRow(QLabel('Where do you want to save the output?'), self.wdset)
        layout.addRow(self.submit, self.quitbutton)

        # Add form layout to overarching layout
        over_layout.addLayout(layout)

        self.setLayout(over_layout)

    def submitsettings(self):
        person = participant.RAParticipant(self.idform.text(),
                                           self.trialsin.text(),
                                           self.wdset.text(),
                                           'Risk Aversion',
                                           self.minin.text(),
                                           self.maxin.text())

        self.exp = gui.RAExp(person)
        self.exp.show()
        self.hide()


class FrameSettings(Settings):

    def __init__(self):
        super().__init__()

        # setting  the geometry of window
        self.setGeometry(0, 0, 650, 350)

        # center window
        self.centerscreen()

        # STT default
        self.ftt = 0

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
        self.trialsin.setSpecialValueText('30')

        # min EV input
        self.minin = QSpinBox()
        self.minin.setSpecialValueText('1')

        # max EV input
        self.maxin = QSpinBox()
        self.maxin.setSpecialValueText('50')

        # Dropdown box for gains, losses, or both
        self.design = QComboBox()
        self.design.addItems(['Gains only', 'Losses only', 'Gains and Losses'])

        # FTT  input
        self.ftttoggle = QCheckBox('', self)
        self.ftttoggle.stateChanged.connect(self.clickBox)

        # Make form layout for all the settings
        layout = QFormLayout()

        layout.addRow(QLabel('Subject ID:'), self.idform)
        layout.addRow(QLabel('Number of trials:'), self.trialsin)
        layout.addRow(QLabel('Minimum expected value:'), self.minin)
        layout.addRow(QLabel('Maximum expected value:'), self.maxin)
        layout.addRow(QLabel('What type of questions do you want?:'), self.design)
        layout.addRow(QLabel('Do you want FTT truncations (i.e., Gist, Mixed, Verbatim)?:'), self.ftttoggle)
        layout.addRow(QLabel('Where do you want to save the output?'), self.wdset)
        layout.addRow(self.submit, self.quitbutton)

        # Add form layout to overarching layout
        over_layout.addLayout(layout)

        self.setLayout(over_layout)

    def clickBox(self):

        if self.ftttoggle.isChecked():
            self.ftt = 'Yes'
        else:
            self.ftt = 'No'

    def submitsettings(self):

        if (
                (self.design.currentText() == 'Gains and Losses') &
                (self.ftt == 'Yes') &
                int(self.trialsin.text()) % 6 != 0
        ):

            self.matherrordialog(4)

        elif (self.ftt == 'Yes') & (int(self.trialsin.text()) % 3 != 0):

            self.matherrordialog(3)

        elif (self.design.currentText() == 'Gains and Losses') & (int(self.trialsin.text()) % 2 != 0):

            self.matherrordialog(2)

        else:

            person = participant.FrameParticipant(self.idform.text(),
                                                  self.trialsin.text(),
                                                  self.wdset.text(),
                                                  'Framing',
                                                  self.minin.text(),
                                                  self.maxin.text(),
                                                  self.design.currentText(),
                                                  self.ftt)

            self.exp = gui.FrameExp(person)
            self.exp.show()
            self.hide()

    def matherrordialog(self, state):

        error = MathErrorBox(state)

        error.exec()


class BeadsSettings(Settings):

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

        # ST Trials input
        self.trialsin = QSpinBox()
        self.trialsin.setSpecialValueText('3')

        # Make form layout for all the settings
        layout = QFormLayout()

        layout.addRow(QLabel('Subject ID:'), self.idform)
        layout.addRow(QLabel('Number of trials:'), self.trialsin)
        layout.addRow(QLabel('Where do you want to save the output?'), self.wdset)
        layout.addRow(self.submit, self.quitbutton)

        # Add form layout to overarching layout
        over_layout.addLayout(layout)

        self.setLayout(over_layout)

    def submitsettings(self):
        person = participant.BeadsParticipant(self.idform.text(),
                                              self.trialsin.text(),
                                              self.wdset.text(),
                                              'Beads Task')

        self.exp = gui.BeadsExp(person)
        self.exp.show()
        self.hide()


class PBTSettings(Settings):

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

        # Blocks input
        self.blocksin = QSpinBox()
        self.blocksin.setSpecialValueText('2')

        # Trials input
        self.trialsin = QSpinBox()
        self.trialsin.setSpecialValueText('120')

        # Make form layout for all the settings
        layout = QFormLayout()

        layout.addRow(QLabel('Subject ID:'), self.idform)
        layout.addRow(QLabel('Number of blocks:'), self.blocksin)
        layout.addRow(QLabel('Number of trials per block (make sure it\'s divisible by 4):'), self.trialsin)
        layout.addRow(QLabel('Where do you want to save the output?'), self.wdset)
        layout.addRow(self.submit, self.quitbutton)

        # Add form layout to overarching layout
        over_layout.addLayout(layout)

        self.setLayout(over_layout)

    def submitsettings(self):

        if (int(self.trialsin.text()) % 4) == 0:
            person = participant.PBTParticipant(self.idform.text(),
                                                self.trialsin.text(),
                                                self.wdset.text(),
                                                'Perceptual Bias Task',
                                                self.blocksin.text())

            self.exp = gui.PBTExp(person)
            self.exp.show()
            self.hide()

        else:
            self.matherrordialog()

    def matherrordialog(self):

        error = MathErrorBox(1)

        error.exec()


class NACTSettings(Settings): # TODO Make this negative attention specific

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

        # Make form layout for all the settings
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
        person = participant.PrParticipant(self.idform.text(),
                                           self.pairsin.text(),
                                           self.wdset.text(),
                                           'Negative Attention Capture',
                                           self.trialsin.text(),
                                           self.stt)

        self.exp = gui.MemoryExp(person)
        self.exp.show()
        self.hide()


class SSSettings(Settings):

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

        # ST Trials input
        self.trialsin = QSpinBox()
        self.trialsin.setSpecialValueText('3')

        # Make form layout for all the settings
        layout = QFormLayout()

        layout.addRow(QLabel('Subject ID:'), self.idform)
        layout.addRow(QLabel('Number of trials:'), self.trialsin)
        layout.addRow(QLabel('Where do you want to save the output?'), self.wdset)
        layout.addRow(self.submit, self.quitbutton)

        # Add form layout to overarching layout
        over_layout.addLayout(layout)

        self.setLayout(over_layout)

    def submitsettings(self):
        person = participant.SSParticipant(self.idform.text(),
                                           self.trialsin.text(),
                                           self.wdset.text(),
                                           'Stop-Signal Task')

        self.exp = gui.SSExp(person)
        self.exp.show()
        self.hide()


class EGNGSettings(Settings):

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

        # ST Trials input
        self.trialsin = QSpinBox()
        self.trialsin.setSpecialValueText('3')

        # Make form layout for all the settings
        layout = QFormLayout()

        layout.addRow(QLabel('Subject ID:'), self.idform)
        layout.addRow(QLabel('Number of trials:'), self.trialsin)
        layout.addRow(QLabel('Where do you want to save the output?'), self.wdset)
        layout.addRow(self.submit, self.quitbutton)

        # Add form layout to overarching layout
        over_layout.addLayout(layout)

        self.setLayout(over_layout)

    def submitsettings(self):
        person = participant.EGNGParticipant(self.idform.text(),
                                             self.trialsin.text(),
                                             self.wdset.text(),
                                             'Emo Go/No-Go')

        self.exp = gui.EGNGExp(person)
        self.exp.show()
        self.hide()


class PrSettings(Settings):

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

        # Make form layout for all the settings
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
        person = participant.PrParticipant(self.idform.text(),
                                           self.pairsin.text(),
                                           self.wdset.text(),
                                           'Pair Recall Memory',
                                           self.trialsin.text(),
                                           self.stt)

        self.exp = gui.PrExp(person)
        self.exp.show()
        self.hide()


class NBackSettings(Settings):

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

        # Trials input
        self.trialsin = QSpinBox()
        self.trialsin.setSpecialValueText('30')

        # Rounds input
        self.roundsin = QSpinBox()
        self.roundsin.setSpecialValueText('1')

        # Dropdown box for gains, losses, or both
        self.design = QComboBox()
        self.design.addItems(['1-back', '2-back', '3-back', '4-back'])

        # Make form layout for all the settings
        layout = QFormLayout()

        layout.addRow(QLabel('Subject ID:'), self.idform)
        layout.addRow(QLabel('Number of trials:'), self.trialsin)
        layout.addRow(QLabel('Number of rounds (do you want more than 1 round of X number of trials?):'), self.roundsin)
        layout.addRow(QLabel('What type of n-Back?:'), self.design)
        layout.addRow(QLabel('Where do you want to save the output?'), self.wdset)
        layout.addRow(self.submit, self.quitbutton)

        # Add form layout to overarching layout
        over_layout.addLayout(layout)

        self.setLayout(over_layout)

    def submitsettings(self):

        person = participant.NbParticipant(self.idform.text(),
                                           self.trialsin.text(),
                                           self.wdset.text(),
                                           self.design.currentText(),
                                           self.roundsin.text())

        self.exp = gui.NbExp(person)
        self.exp.show()
        self.hide()
