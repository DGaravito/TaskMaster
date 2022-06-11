import time

from PyQt6.QtWidgets import QLabel, QHBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer, pyqtSignal

from expguis import gui


class PBTExp(gui.Experiment):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__(person)

        # Make a timer that controls how long an image is left on the screen
        self.blankouttimer = QTimer()
        self.blankouttimer.timeout.connect(self.blankout)

    def elements(self):
        # Instructions
        self.instructions = QLabel('Press ' + self.person.leftkey[0] + ' for crosses. Press ' +
                                   self.person.rightkey[0] + ' for squares.')

        # Make middle for pictures and text
        middlelayout = QHBoxLayout()

        middlelayout.addStretch(1)
        middlelayout.addWidget(self.middle)
        middlelayout.addStretch(1)

        # Put everything in vertical layout
        self.instquitlayout.addWidget(self.instructions)
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addLayout(middlelayout)
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addWidget(self.quitbutton)

        # Set up layout
        self.setLayout(self.instquitlayout)

    def generatenext(self):

        self.ititimer.stop()

        if self.trialsdone < self.person.get_trials():

            # Get the string that contains the name of the trial picture
            self.picstring = self.person.get_trial_pic()
            pathstring = 'assets/' + self.picstring

            # Make a pixmap of the picture and then set the middle to that pixmap
            pixmap = QPixmap(pathstring)
            self.middle.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))

            self.starttime = time.time()

            # Start the timers
            self.timer.start(5000)
            self.ititimer.start(5500)
            self.blankouttimer.start(250)

        else:

            self.roundsdone += 1
            self.trialsdone = 0

            self.middle.setPixmap(QPixmap())

            self.middle.setText(self.person.nextround(self.roundsdone))

            if self.person.rounds == self.roundsdone:

                self.person.output()
                self.instructions.setText('Thank you!')

    def blankout(self):

        self.blankouttimer.stop()
        self.middle.setPixmap(QPixmap())

    def timeout(self):

        self.timer.stop()

        endtime = time.time()
        rt = endtime - self.starttime

        self.person.updateoutput(self.trialsdone, self.picstring, self.starttime, rt, 'None')

        self.iti()

    def keyaction(self, key):

        if key in ['g', 'G']:

            self.middle.setText('')
            self.inst = 1
            self.iti()

        if key in self.person.rightkey:

            self.timer.stop()
            self.trialsdone += 1

            endtime = time.time()
            rt = endtime - self.starttime

            self.person.updateoutput(self.trialsdone, self.picstring, self.starttime, rt, 'Square')
            self.iti()

        if key in self.person.leftkey:

            self.timer.stop()
            self.trialsdone += 1

            endtime = time.time()
            rt = endtime - self.starttime

            self.person.updateoutput(self.trialsdone, self.picstring, self.starttime, rt, 'Cross')
            self.iti()

        if key in ['i', 'I']:

            self.inst += 1

            if self.inst == 6:
                pixmap = QPixmap('../assets/PBT_DSC.BMP')
                self.middle.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))

            elif self.inst == 9:
                pixmap = QPixmap('../assets/PBT_DCS.BMP')
                self.middle.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))

            else:
                self.middle.setText(self.person.get_instructions(self.person.globallocal, self.inst))

            if self.inst == 11:
                self.inst = 0
