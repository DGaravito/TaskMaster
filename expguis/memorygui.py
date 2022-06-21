from PyQt6.QtWidgets import QLabel, QHBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QTimer, pyqtSignal

import time

from expguis import gui


class PrExp(gui.Experiment):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__(person)

        # Left and right options (and middle stuff) with font settingsguis
        self.left = QLabel('')
        self.left.setFont(QFont('Helvetica', 40))
        self.instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.right = QLabel('')
        self.right.setFont(QFont('Helvetica', 40))
        self.instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)

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
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addLayout(explayout)
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addWidget(self.quitbutton)

        # Get the structure
        self.structure = self.person.structure

        # Make timer for new trial screen
        self.newtrialtimer = QTimer()
        self.newtrialtimer.timeout.connect(self.generatetrial)

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

            self.ititimer.start(5000)

        elif self.person.get_trials() > self.trialsdone:

            self.ititimer.stop()

            if self.structure[0] == 'S':

                strings = self.person.get_design_text()

            else:

                strings = self.person.get_design_text(1)

            self.left.setText(strings[0])
            self.right.setText(strings[1])
            self.middle.setText('')

            self.trialsdone += 1

            self.ititimer.start(5000)

        else:

            self.ititimer.stop()

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

                self.newtrialtimer.start(3000)

    def generatetrial(self):

        self.newtrialtimer.stop()

        self.trialsdone = 0

        string = self.person.starttrial()
        self.instructions.setText(string)
        self.betweenrounds = 1

    def keyaction(self, key):

        if (key in ['g', 'G']) & (self.betweenrounds == 1):
            self.betweenrounds = 0
            self.generatenext()

        if (key in ['i', 'I']) & (self.betweenrounds == 1):

            self.inst += 1
            self.middle.setText(self.person.get_instructions(self.inst))

            if self.inst == 16:

                self.inst = 0


class NbExp(gui.Experiment):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__(person)

        # Instructions
        self.instructions.setText('Press ' + self.person.leftkey[0] + ' if the letter is a false alarm. Press ' +
                                  self.person.rightkey[0] + ' if the letter is a target')

        # center middle
        self.middle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Put everything in vertical layout
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addWidget(self.middle)
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addWidget(self.quitbutton)

    def generatenext(self):

        self.ititimer.stop()

        if self.trialsdone < self.person.get_trials():

            self.middle.setText(self.person.get_trial_text())

            self.starttime = time.time()

            self.timer.start(3000)
            self.ititimer.start(3500)
            self.responseenabled = 1

        else:

            self.roundsdone += 1
            self.trialsdone = 0

            text = self.person.nextround(self.roundsdone)

            self.instructions.setText(text[0])
            self.middle.setText(text[1])

            if self.person.roundperformance < 70:

                self.roundsdone -= 1

            if self.person.rounds == self.roundsdone:

                self.person.output()
                self.instructions.setText('Thank you!')

            else:

                self.betweenrounds = 1

    def timeout(self):
        self.timer.stop()

        self.responseenabled = 0

        self.trialsdone += 1

        endtime = time.time()
        rt = endtime - self.starttime

        self.person.updateoutput(self.trialsdone, self.starttime, rt)
        self.iti()

    def keyaction(self, key):

        if (key in ['g', 'G']) & (self.betweenrounds == 1):

            self.betweenrounds = 0

            self.generatenext()

            self.instructions.setText('Press ' + self.person.leftkey[0] + ' if the letter is a false alarm. Press ' +
                                      self.person.rightkey[0] + ' if the letter is a target')

        if (key in self.person.rightkey) & (self.responseenabled == 1):

            self.responseenabled = 0

            self.timer.stop()
            self.trialsdone += 1

            endtime = time.time()
            rt = endtime - self.starttime

            self.person.updateoutput(self.trialsdone, self.starttime, rt, 1)
            self.iti()

        if (key in self.person.leftkey) & (self.responseenabled == 1):

            self.responseenabled = 0

            self.timer.stop()
            self.trialsdone += 1

            endtime = time.time()
            rt = endtime - self.starttime

            self.person.updateoutput(self.trialsdone, self.starttime, rt, 0)
            self.iti()

        if (key in ['i', 'I']) & (self.betweenrounds == 1):

            self.inst += 1
            self.middle.setText(self.person.get_instructions(self.inst))

            if self.inst == 12:

                self.inst = 0
