from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QTimer, pyqtSignal


class PrExp(QWidget):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__()

        self.person = person
        self.trialsdone = 0
        self.inst = 0

        self.structure = self.person.structure

        # Window title
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # center window
        self.centerscreen()

        # Add in elements
        self.elements()

        # Show all elements
        self.showMaximized()

        # Attach keyboard keys to functions
        self.keyPressed.connect(self.keyaction)

        # Make timer to transition word pairs
        self.timermemory = QTimer()
        self.timermemory.timeout.connect(self.generatenext)

        # Make timer for new trial screen
        self.timer_newtrial = QTimer()
        self.timer_newtrial.timeout.connect(self.generatetrial)

    def elements(self):

        # Make overarching layout
        instquitlayout = QVBoxLayout()

        # Quit button
        self.quitbutton = QPushButton('Quit')
        self.quitbutton.clicked.connect(QApplication.instance().quit)
        self.quitbutton.setFixedWidth(40)
        self.quitbutton.setFixedHeight(20)

        # Instructions
        self.instructions = QLabel('')

        # setting font style and size
        self.instructions.setFont(QFont('Helvetica', 25))

        # center Instructions
        self.instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Left and right options (and middle stuff) with font settingsguis
        self.left = QLabel('')
        self.left.setFont(QFont('Helvetica', 40))

        self.right = QLabel('')
        self.right.setFont(QFont('Helvetica', 40))

        self.middle = QLabel('Press \"I\"')
        self.middle.setFont(QFont('Helvetica', 30))

        # Put Left and Right options in horizontal layout
        explayout = QHBoxLayout()

        explayout.addStretch(1)
        explayout.addWidget(self.left)
        explayout.addStretch(1)
        explayout.addWidget(self.middle)
        explayout.addStretch(1)
        explayout.addWidget(self.right)
        explayout.addStretch(1)

        # Put everything in vertical layout

        instquitlayout.addWidget(self.instructions)
        instquitlayout.addStretch(1)
        instquitlayout.addLayout(explayout)
        instquitlayout.addStretch(1)
        instquitlayout.addWidget(self.quitbutton)

        # Set up layout

        self.setLayout(instquitlayout)

    def centerscreen(self):

        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def keyPressEvent(self, keyevent):
        self.keyPressed.emit(keyevent.text())

    def generatenext(self):

        if self.trialsdone == 0:

            if self.structure[0] == 'S':

                strings = self.person.get_design_text()

            else:

                strings = self.person.get_design_text(1)

            self.left.setText(strings[0])
            self.right.setText(strings[1])
            self.middle.setText('')

            self.trialsdone += 1

            self.timermemory.start(5000)

        elif self.person.get_trials() > self.trialsdone:

            self.timermemory.stop()

            if self.structure[0] == 'S':

                strings = self.person.get_design_text()

            else:

                strings = self.person.get_design_text(1)

            self.left.setText(strings[0])
            self.right.setText(strings[1])
            self.middle.setText('')

            self.trialsdone += 1

            self.timermemory.start(5000)

        else:

            self.timermemory.stop()

            self.person.output()

            del self.structure[0]

            if len(self.structure) == 0:

                self.left.setText('')
                self.right.setText('')
                self.instructions.setText('Thank you!')
                self.middle.setText('You have finished this part of the study.')

            else:

                self.left.setText('')
                self.right.setText('')
                self.instructions.setText('')
                self.middle.setText('You have finished this trial.')

                self.timer_newtrial.start(3000)

    def generatetrial(self):

        self.timer_newtrial.stop()

        self.trialsdone = 0

        string = self.person.starttrial()
        self.instructions.setText(string)

    def keyaction(self, key):

        if key in ['g', 'G']:
            self.generatenext()

        if key in ['i', 'I']:

            self.inst += 1
            self.middle.setText(self.person.get_instructions(self.inst))

            if self.inst == 16:

                self.inst = 0


class NbExp(QWidget):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__()

        self.person = person
        self.trialsdone = 0
        self.roundsdone = 0
        self.inst = 0

        if self.person.buttonbox == 'Yes':
            self.leftkey = ['1']
            self.rightkey = ['2']

        else:
            self.leftkey = ['C', 'c']
            self.rightkey = ['M', 'm']

        # Window title
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # center window
        self.centerscreen()

        # Add in elements
        self.elements()

        # Show all elements
        self.showMaximized()

        # Attach keyboard keys to functions
        self.keyPressed.connect(self.keyaction)

        # Make timer to transition word pairs
        self.timer = QTimer()
        self.timer.timeout.connect(self.timeout)

    def elements(self):

        # Make overarching layout
        mainlayout = QVBoxLayout()

        # Quit button
        self.quitbutton = QPushButton('Quit')
        self.quitbutton.clicked.connect(QApplication.instance().quit)
        self.quitbutton.setFixedWidth(40)
        self.quitbutton.setFixedHeight(20)

        # Instructions
        self.instructions = QLabel('Press ' + self.leftkey[0] + ' if the letter is a false alarm. Press ' +
                                   self.rightkey[0] + ' if the letter is a target')

        # setting font style and size
        self.instructions.setFont(QFont('Helvetica', 25))

        # center Instructions
        self.instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Make the middle for the actualy n-back task

        self.middle = QLabel(self.person.nextround(0))
        self.middle.setFont(QFont('Helvetica', 40))

        # center middle
        self.middle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Put everything in vertical layout

        mainlayout.addWidget(self.instructions)
        mainlayout.addStretch(1)
        mainlayout.addWidget(self.middle)
        mainlayout.addStretch(1)
        mainlayout.addWidget(self.quitbutton)

        # Set up layout

        self.setLayout(mainlayout)

    def centerscreen(self):

        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def keyPressEvent(self, keyevent):
        self.keyPressed.emit(keyevent.text())

    def generatenext(self):

        if self.trialsdone < self.person.get_trials():

            self.middle.setText(self.person.get_trial_text())

            self.timer.start(3000)

        else:

            self.roundsdone += 1

            text = self.person.nextround(self.roundsdone)

            self.instructions.setText(text[0])
            self.middle.setText(text[1])

            if self.person.roundperformance < 70:

                self.roundsdone -= 1

            if self.person.rounds == self.roundsdone:

                self.person.output()
                self.instructions.setText('Thank you!')

    def timeout(self):

        self.timer.stop()

        self.trialsdone += 1

        self.person.updateoutput(self.trialsdone)
        self.generatenext()

        self.timer.start(3000)

    def keyaction(self, key):

        if key in ['g', 'G']:

            self.generatenext()

            self.instructions.setText('Press ' + self.leftkey[0] + ' if the letter is a false alarm. Press ' +
                                      self.rightkey[0] + ' if the letter is a target')

        if key in self.rightkey:

            self.timer.stop()
            self.trialsdone += 1
            self.person.updateoutput(self.trialsdone, 1)
            self.generatenext()

        if key in self.leftkey:

            self.timer.stop()
            self.trialsdone += 1
            self.person.updateoutput(self.trialsdone, 0)
            self.generatenext()

        if key in ['i', 'I']:

            self.inst += 1
            self.middle.setText(self.person.get_instructions(self.inst))

            if self.inst == 12:

                self.inst = 0
