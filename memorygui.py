from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QTimer, pyqtSignal


class MemoryExp(QWidget):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__()

        self.person = person
        self.trialsdone = 0

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

        # Left and right options (and middle stuff) with font settings
        self.left = QLabel('')
        self.left.setFont(QFont('Helvetica', 40))

        self.right = QLabel('')
        self.right.setFont(QFont('Helvetica', 40))

        self.middle = QLabel('Please let the researcher know you are ready')
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
