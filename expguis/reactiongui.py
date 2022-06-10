import random
import time
from pathlib import Path

from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QDir


class SSExp(QWidget):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__()

        self.person = person
        self.trialsdone = 0
        self.roundsdone = 0
        self.inst = 0
        self.signal = False

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

        self.ititimer = QTimer()
        self.ititimer.timeout.connect(self.generatenext)

        self.signaltimer = QTimer()
        self.signaltimer.timeout.connect(self.sendsignal)

    def elements(self):

        # Make overarching layout
        mainlayout = QVBoxLayout()

        # Quit button
        self.quitbutton = QPushButton('Quit')
        self.quitbutton.clicked.connect(QApplication.instance().quit)
        self.quitbutton.setFixedWidth(40)
        self.quitbutton.setFixedHeight(20)

        # Instructions
        self.instructions = QLabel('Press ' + self.leftkey[0] + ' for left arrows. Press ' + self.rightkey[0] +
                                   ' for right arrows.')

        # setting font style and size
        self.instructions.setFont(QFont('Helvetica', 25))
        self.instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # add the assets folder

        toassets = str(Path('..').resolve())
        QDir.addSearchPath('assets', toassets)

        # Make middle for pictures and text

        middlelayout = QHBoxLayout()

        self.middle = QLabel('Press \"G\" to start, \"I\" for instructions')
        self.middle.setFont(QFont('Helvetica', 40))

        # center middle
        self.middle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.middle.setScaledContents(True)

        middlelayout.addStretch(1)
        middlelayout.addWidget(self.middle)
        middlelayout.addStretch(1)

        # Put everything in vertical layout

        mainlayout.addWidget(self.instructions)
        mainlayout.addStretch(1)
        mainlayout.addLayout(middlelayout)
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

            self.ititimer.stop()

            self.picstring = self.person.get_trial_pic()

            pathstring = 'assets/' + self.picstring

            pixmap = QPixmap(pathstring)

            self.middle.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))

            signalrand = random.randint(1, 2)

            if signalrand == 1:

                self.signal = 0

            else:

                self.signal = 1
                self.signaltimer.start(self.person.get_timer())

            self.starttime = time.time()

            self.timer.start(2500)

        else:

            self.ititimer.stop()

            self.roundsdone += 1

            self.middle.setPixmap(QPixmap())

            self.middle.setText(self.person.nextround(self.roundsdone))

            self.trialsdone = 0

            if self.person.rounds == self.roundsdone:

                self.person.output()
                self.instructions.setText('Thank you!')

    def iti(self):

        self.middle.setPixmap(QPixmap())

        self.ititimer.start(500)

    def timeout(self):

        self.timer.stop()
        self.signaltimer.stop()

        endtime = time.time()
        rt = endtime - self.starttime

        self.person.updateoutput(self.trialsdone, self.picstring, self.starttime, rt)

        self.iti()

    def sendsignal(self):

        self.signaltimer.stop()

        if self.picstring == 'SS_LeftArrow.jpg':
            pathstring = 'assets/SS_LeftSignal.jpg'

        else:
            pathstring = 'assets/SS_RightSignal.jpg'

        pixmap = QPixmap(pathstring)

        self.middle.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))

    def keyaction(self, key):

        if key in ['g', 'G']:

            self.middle.setText('')
            self.inst = 1
            self.iti()

        if key in self.person.rightkey:

            self.timer.stop()
            self.signaltimer.stop()
            self.trialsdone += 1

            endtime = time.time()
            rt = endtime - self.starttime

            self.person.updateoutput(self.trialsdone, self.picstring, self.starttime, rt, 2)
            self.iti()

        if key in self.person.leftkey:

            self.timer.stop()
            self.signaltimer.stop()
            self.trialsdone += 1

            endtime = time.time()
            rt = endtime - self.starttime

            self.person.updateoutput(self.trialsdone, self.picstring, self.starttime, rt, 1)
            self.iti()

        if key in ['i', 'I']:

            self.inst += 1

            self.middle.setText(self.person.get_instructions(self.inst))

            if self.inst == 12:
                self.inst = 0
