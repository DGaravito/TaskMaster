import random
import time

from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer, pyqtSignal

from expguis import gui


class SSExp(gui.Experiment):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__(person)

        # Make timer to indicate when a signal should be sent (in signal trials)
        self.signaltimer = QTimer()
        self.signaltimer.timeout.connect(self.sendsignal)

        # Show all elements
        self.showMaximized()

    def elements(self):

        # Make middle layout for pictures and text
        middlelayout = QHBoxLayout()

        middlelayout.addStretch(1)
        middlelayout.addWidget(self.middle)
        middlelayout.addStretch(1)

        # Instructions
        self.instructions.setText('Press ' + self.person.leftkey[0] + ' for left arrows. Press ' +
                                  self.person.rightkey[0] + ' for right arrows.')

        # Put everything in vertical layout
        self.instquitlayout.addWidget(self.instructions)
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addLayout(middlelayout)
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addWidget(self.quitbutton)

        # set layout
        self.setLayout(self.instquitlayout)

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
            self.ititimer.start(3000)

        else:

            self.ititimer.stop()

            self.roundsdone += 1

            self.middle.setPixmap(QPixmap())

            self.middle.setText(self.person.nextround(self.roundsdone))

            self.trialsdone = 0

            if self.person.rounds == self.roundsdone:

                self.person.output()
                self.instructions.setText('Thank you!')

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

            self.inst = 1
            self.iti()
            self.ititimer.start(500)

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
