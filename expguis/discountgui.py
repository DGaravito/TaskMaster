import random
import time

from PyQt6.QtWidgets import QLabel, QHBoxLayout, QProgressBar
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QTimer, pyqtSignal

from expguis import gui


class DDiscountExp(gui.Experiment):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__(person)

        # Instructions
        self.instructions.setText('Press ' + self.person.leftkey[0] + ' for the left option and ' +
                                  self.person.rightkey[0] + ' for the right option')

        # Left and right options (and middle stuff) with font settingsguis
        self.left = QLabel('')
        self.left.setFont(QFont('Helvetica', 40))
        self.left.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.right = QLabel('')
        self.right.setFont(QFont('Helvetica', 40))
        self.right.setAlignment(Qt.AlignmentFlag.AlignCenter)

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

    def iti(self):

        self.left.setText('')
        self.right.setText('')
        self.middle.setText('+')

        if self.trialsdone != 0:
            endtime = time.time()
            rt = endtime - self.starttime

            self.person.updateoutput(self.trialsdone, self.starttime, rt, self.response)

            if self.response != 'None':
                self.person.engineupdate(self.response)

            if self.person.fmri == 'No':
                self.ititimer.start(1000)

    def generatenext(self):

        self.ititimer.stop()

        if self.person.get_trials() > self.trialsdone:

            strings = self.person.get_design_text()
            self.left.setText(strings[0])
            self.right.setText(strings[1])
            self.middle.setText('OR')

            self.trialsdone += 1

            self.timer.start(5000)
            self.starttime = time.time()

            if self.person.fmri == 'Yes':
                self.ititimer.start(5500)

            self.responseenabled = 1

        else:
            self.person.output()

            self.left.setText('')
            self.right.setText('')

            self.roundsdone += 1
            self.trialsdone = 0

            self.middle.setText(self.person.nextround(self.roundsdone))

            if self.person.rounds == self.roundsdone:

                self.person.output()
                self.instructions.setText('Thank you!')

            else:

                self.betweenrounds = 1

    def timeout(self):

        self.timer.stop()

        self.left.setText('')
        self.right.setText('')
        self.middle.setText('Please try to be quicker')

        if self.person.fmri == 'No':
            self.trialresettimer.start(1000)

        else:
            self.response = 'None'
            self.responseenabled = 0
            self.iti()

    def responsereset(self):

        self.trialresettimer.stop()

        strings = self.person.get_design_text()
        self.left.setText(strings[0])
        self.right.setText(strings[1])

        self.middle.setText('OR')

        self.timer.start(5000)

    def keyaction(self, key):

        if (key in ['g', 'G']) & (self.betweenrounds == 1):

            self.betweenrounds = 0
            self.iti()
            self.ititimer.start(500)

        if (key in self.person.leftkey) & (self.responseenabled == 1):

            self.responseenabled = 0

            self.timer.stop()
            self.response = 0
            self.iti()

        if (key in self.person.rightkey) & (self.responseenabled == 1):

            self.responseenabled = 0

            self.timer.stop()
            self.response = 1
            self.iti()

        if (key in ['i', 'I']) & (self.betweenrounds == 1):
            self.inst += 1

            self.middle.setText(self.person.get_instructions(self.inst))

            if self.inst == 5:
                self.inst = 0


class PDiscountExp(gui.Experiment):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__(person)

        # Instructions
        self.instructions.setText('Press ' + self.person.leftkey[0] + ' for the left option and ' +
                                  self.person.rightkey[0] + ' for the right option')

        # Left and right options (and middle stuff) with font settingsguis
        self.left = QLabel('')
        self.left.setFont(QFont('Helvetica', 40))
        self.left.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.right = QLabel('')
        self.right.setFont(QFont('Helvetica', 40))
        self.right.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Put Left and Right words for options in horizontal layout
        expverblayout = QHBoxLayout()

        expverblayout.addStretch(1)
        expverblayout.addWidget(self.left)
        expverblayout.addStretch(1)
        expverblayout.addWidget(self.middle)
        expverblayout.addStretch(1)
        expverblayout.addWidget(self.right)
        expverblayout.addStretch(1)

        # creating vertical progress bar to represent options
        self.leftbar = QProgressBar(self)
        self.leftbar.setOrientation(Qt.Orientation.Vertical)

        self.rightbar = QProgressBar(self)
        self.rightbar.setOrientation(Qt.Orientation.Vertical)

        # Put Left and Right visual options in horizontal layout
        expvislayout = QHBoxLayout()

        expvislayout.addStretch(1)
        expvislayout.addWidget(self.leftbar)
        expvislayout.addStretch(1)
        expvislayout.addWidget(QLabel(''))
        expvislayout.addStretch(1)
        expvislayout.addWidget(self.rightbar)
        expvislayout.addStretch(1)

        # Put everything in vertical layou
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addLayout(expverblayout)
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addLayout(expvislayout)
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addWidget(self.quitbutton)

    def iti(self):

        self.left.setText('')
        self.leftbar.setValue(0)
        self.right.setText('')
        self.rightbar.setValue(0)
        self.middle.setText('+')

        if self.trialsdone != 0:

            endtime = time.time()
            rt = endtime - self.starttime

            self.person.updateoutput(self.trialsdone, self.starttime, rt, self.response)

            if self.person.fmri == 'No':
                self.ititimer.start(1000)

        else:
            self.ititimer.start(1000)

        self.person.set_design_text()

    def generatenext(self):

        self.ititimer.stop()
        if self.person.get_trials() > self.trialsdone:

            self.trialsdone += 1

            info = self.person.get_design_text()
            self.left.setText(info[0])
            self.leftbar.setValue(100)

            self.right.setText(info[1])
            self.rightbar.setValue(info[2])

            self.middle.setText('OR')

            self.starttime = time.time()

            self.timer.start(5000)

            if self.person.fmri == 'Yes':
                self.ititimer.start(5500)

            self.responseenabled = 1

        else:
            self.person.output()

            self.left.setText('')
            self.right.setText('')

            self.roundsdone += 1
            self.trialsdone = 0

            self.middle.setText(self.person.nextround(self.roundsdone))

            if self.person.rounds == self.roundsdone:

                self.person.output()
                self.instructions.setText('Thank you!')

                if self.person.outcomeopt == 'Yes':

                    outcome = random.choice(self.person.outcomelist)
                    self.middle.setText('Your outcome: ' + outcome)

            else:

                self.betweenrounds = 1

    def timeout(self):

        self.timer.stop()

        self.left.setText('')
        self.leftbar.setValue(0)

        self.right.setText('')
        self.rightbar.setValue(0)
        self.middle.setText('Please try to be quicker')

        if self.person.fmri == 'No':
            self.trialresettimer.start(1000)

        else:
            self.response = 'None'
            self.responseenabled = 0
            self.iti()

    def responsereset(self):

        self.trialresettimer.stop()

        info = self.person.get_design_text()
        self.left.setText(info[0])
        self.leftbar.setValue(100)

        self.right.setText(info[1])
        self.rightbar.setValue(info[2])

        self.middle.setText('OR')

        self.timer.start(5000)

    def keyaction(self, key):

        if (key in ['g', 'G']) & (self.betweenrounds == 1):

            self.betweenrounds = 0
            self.iti()

        if (key in self.person.leftkey) & (self.responseenabled == 1):

            self.responseenabled = 0

            self.timer.stop()
            self.response = 0
            self.iti()

        if (key in self.person.rightkey) & (self.responseenabled == 1):

            self.responseenabled = 0

            self.timer.stop()
            self.response = 1
            self.iti()

        if (key in ['i', 'I']) & (self.betweenrounds == 1):
            self.inst += 1

            self.middle.setText(self.person.get_instructions(self.inst))

            if self.inst == 5:
                self.inst = 0


class CEDiscountExp(gui.Experiment):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__(person)

        # Instructions
        self.instructions.setText('Press ' + self.person.leftkey[0] + ' for the left option and ' +
                                  self.person.rightkey[0] + ' for the right option')

        # Left and right options (and middle stuff) with font settingsguis
        self.left = QLabel('')
        self.left.setFont(QFont('Helvetica', 40))
        self.left.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.right = QLabel('')
        self.right.setFont(QFont('Helvetica', 40))
        self.right.setAlignment(Qt.AlignmentFlag.AlignCenter)

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

        if self.person.fmri == 'Yes':
            self.extradelay = [0]

        else:
            self.extradelay = [0, 2000, 4000]

        # Make timer for second half of trial to appear on screen
        self.secondhalftimer = QTimer()
        self.secondhalftimer.timeout.connect(self.displaysecondhalf)

    def iti(self):

        self.left.setText('')
        self.right.setText('')
        self.middle.setText('+')

        endtime = time.time()
        rt = endtime - self.starttime

        self.person.updateoutput(self.trialsdone, self.starttime, rt, self.response)

        if self.person.fmri == 'No':
            self.ititimer.start(1000)

    def generatenext(self):

        self.timer.stop()
        self.ititimer.stop()

        if self.person.get_trials() > self.trialsdone:

            self.person.set_design_text()
            self.trialsdone += 1

            strings = self.person.get_design_text()
            self.left.setText(strings[0])
            self.middle.setText('')
            self.right.setText('')

            extra = random.choice(self.extradelay)
            self.secondhalftimer.start(1000 + extra)

            self.responseenabled = 1

        else:

            self.left.setText('')
            self.right.setText('')

            self.roundsdone += 1
            self.trialsdone = 0

            self.middle.setText(self.person.nextround(self.roundsdone))

            if self.person.rounds == self.roundsdone:

                self.instructions.setText('Thank you!')

                self.person.output()

            else:

                self.betweenrounds = 1

    def displaysecondhalf(self):

        self.secondhalftimer.stop()

        strings = self.person.get_design_text()

        self.right.setText(strings[1])
        self.middle.setText('OR')

        self.starttime = time.time()

        self.timer.start(5000)

        if self.person.fmri == 'Yes':
            self.ititimer.start(5500)

    def timeout(self):

        self.timer.stop()
        self.secondhalftimer.stop()

        self.left.setText('')
        self.right.setText('')
        self.middle.setText('Please try to be quicker')

        if self.person.fmri == 'No':
            self.trialresettimer.start(1000)

        else:
            self.response = 'None'
            self.responseenabled = 0
            self.iti()

    def responsereset(self):

        self.trialresettimer.stop()

        strings = self.person.get_design_text()
        self.left.setText(strings[0])
        self.right.setText(strings[1])

        self.middle.setText('OR')

        self.timer.start(5000)

    def keyaction(self, key):

        if (key in ['g', 'G']) & (self.betweenrounds == 1):

            self.betweenrounds = 0
            self.generatenext()

        if (key in self.person.leftkey) & (self.responseenabled == 1):

            self.responseenabled = 0

            self.timer.stop()
            self.response = 0
            self.iti()

        if (key in self.person.rightkey) & (self.responseenabled == 1):

            self.responseenabled = 0

            self.timer.stop()
            self.response = 1
            self.iti()

        if (key in ['i', 'I']) & (self.betweenrounds == 1):
            self.inst += 1

            self.middle.setText(self.person.get_instructions(self.inst))

            if self.inst == 6:
                self.inst = 0
