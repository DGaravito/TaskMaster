import random
import time

from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt, pyqtSignal

from expguis import gui


class ARTTExp(gui.Experiment):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__(person)

    def elements(self):
        # Instructions
        self.instructions = QLabel('Press ' + self.person.leftkey[0] + ' for the left option and ' +
                                   self.person.rightkey[0] + ' for the right option')

        # Set up Left option
        self.left = QLabel('')
        self.left.setFont(QFont('Helvetica', 40))
        self.left.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Set up right option
        self.righttoptext = QLabel('')
        self.righttoptext.setFont(QFont('Helvetica', 40))
        self.righttoptext.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.rightpic = QLabel()
        self.rightpic.setPixmap(QPixmap())
        self.rightpic.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.rightbottomtext = QLabel('')
        self.rightbottomtext.setFont(QFont('Helvetica', 40))
        self.rightbottomtext.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Put right option stuff in a vertical layout
        rightlayout = QVBoxLayout()

        rightlayout.addWidget(self.righttoptext)
        rightlayout.addWidget(self.rightpic)
        rightlayout.addWidget(self.rightbottomtext)

        # Put Left and Right options in horizontal layout
        explayout = QHBoxLayout()

        explayout.addStretch(1)
        explayout.addWidget(self.left)
        explayout.addStretch(1)
        explayout.addWidget(self.middle)
        explayout.addStretch(1)
        explayout.addLayout(rightlayout)
        explayout.addStretch(1)

        # Put everything in vertical layout

        self.instquitlayout.addWidget(self.instructions)
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addLayout(explayout)
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addWidget(self.quitbutton)

        # Set up layout

        self.setLayout(self.instquitlayout)

    def iti(self):

        self.left.setText('')

        self.rightpic.setPixmap(QPixmap())
        self.righttoptext.setText('')
        self.rightbottomtext.setText('')

        self.middle.setText('+')

        endtime = time.time()
        rt = endtime - self.starttime

        self.person.updateoutput(self.trialsdone, self.starttime, rt, self.response)

        if self.response != 'None':
            self.person.engineupdate(self.response)

        if self.person.fmri == 'No':
            self.ititimer.start(1000)

    def generatenext(self):

        self.ititimer.stop()
        if self.trialsdone < self.person.get_trials():

            self.trialsdone += 1

            info = self.person.get_design_text()
            self.left.setText(info[0])

            pixmap = 'assets/' + info[2]
            self.rightpic.setPixmap(QPixmap(pixmap))

            if info[3] == 1:
                self.righttoptext.setText(info[1])
                self.rightbottomtext.setText('0')

            else:
                self.rightbottomtext.setText(info[1])
                self.righttoptext.setText('0')

            self.middle.setText('OR')

            self.starttime = time.time()

            self.timer.start(5000)

            self.responseenabled = 1

            if self.person.fmri == 'Yes':
                self.ititimer.start(5500)

        else:

            self.left.setText('')

            self.righttoptext.setText('')
            self.righttoptext.setText('')

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

        self.responseenabled = 0

        self.left.setText('')

        self.rightpic.setPixmap(QPixmap())
        self.righttoptext.setText('')
        self.rightbottomtext.setText('')

        self.middle.setText('Please try to be quicker')

        if self.person.fmri == 'No':
            self.trialresettimer.start(1000)

        else:
            self.response = 'None'
            self.iti()

    def responsereset(self):

        self.trialresettimer.stop()

        info = self.person.get_design_text()
        self.left.setText(info[0])

        pixmap = 'assets/' + info[2]
        self.rightpic.setPixmap(QPixmap(pixmap))

        if info[3] == 1:
            self.righttoptext.setText(info[1])
            self.rightbottomtext.setText('0')

        else:
            self.rightbottomtext.setText(info[1])
            self.righttoptext.setText('0')

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

            if self.inst == 5:
                pixmap = QPixmap('assets/ARTT_risk_25.bmp')
                self.middle.setPixmap(pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio))

            elif self.inst == 11:
                pixmap = QPixmap('assets/ARTT_ambig_50.bmp')
                self.middle.setPixmap(pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio))

            else:
                self.middle.setText(self.person.get_instructions(self.inst))

            if self.inst == 15:
                self.inst = 0


class RAExp(gui.Experiment):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__(person)

    def elements(self):

        # Instructions
        self.instructions = QLabel('Press ' + self.person.leftkey[0] + ' for the left option and ' +
                                   self.person.rightkey[0] + ' for the right option')

        # Left and right options (and middle stuff) with font settingsguis
        self.left = QLabel('')
        self.left.setFont(QFont('Helvetica', 40))
        self.left.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.rightgain = QLabel('')
        self.rightgain.setFont(QFont('Helvetica', 40))
        self.rightgain.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.rightloss = QLabel('')
        self.rightloss.setFont(QFont('Helvetica', 40))
        self.rightloss.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Put Left and Right visual options in horizontal layout
        gamblelayout = QVBoxLayout()

        gamblelayout.addWidget(self.rightgain)
        gamblelayout.addWidget(self.rightloss)

        # Put Left and Right words for options in horizontal layout
        mainhlayout = QHBoxLayout()

        mainhlayout.addStretch(1)
        mainhlayout.addWidget(self.left)
        mainhlayout.addStretch(1)
        mainhlayout.addWidget(self.middle)
        mainhlayout.addStretch(1)
        mainhlayout.addLayout(gamblelayout)
        mainhlayout.addStretch(1)

        # Put everything in vertical layout

        self.instquitlayout.addWidget(self.instructions)
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addLayout(mainhlayout)
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addWidget(self.quitbutton)

        # Set up layout

        self.setLayout(self.instquitlayout)

    def iti(self):

        self.left.setText('')
        self.rightgain.setText('')
        self.rightloss.setText('')
        self.middle.setText('+')

        endtime = time.time()
        rt = endtime - self.starttime

        self.person.updateoutput(self.trialsdone, self.starttime, rt, self.response)

        self.person.set_design_text()

        if self.person.fmri == 'No':
            self.ititimer.start(1000)

    def generatenext(self):

        self.ititimer.stop()
        if self.trialsdone < self.person.get_trials():

            self.trialsdone += 1

            info = self.person.get_design_text()
            self.left.setText('Getting $0')

            self.rightgain.setText(info[0])
            self.rightloss.setText(info[1])

            self.middle.setText('OR')

            self.starttime = time.time()

            self.timer.start(5000)

            self.responseenabled = 1

            if self.person.fmri == 'Yes':
                self.ititimer.start(5500)

        else:
            self.person.output()

            self.left.setText('')
            self.rightgain.setText('')
            self.rightloss.setText('')

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

        self.responseenabled = 0

        self.left.setText('')

        self.rightgain.setText('')
        self.rightloss.setText('')
        self.middle.setText('Please try to be quicker')

        if self.person.fmri == 'No':
            self.trialresettimer.start(1000)

        else:
            self.response = 'None'
            self.iti()

    def responsereset(self):

        self.trialresettimer.stop()

        info = self.person.get_design_text()
        self.left.setText('0')

        self.rightgain.setText(info[0])
        self.rightloss.setText(info[1])

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

            if self.inst == 5:
                self.inst = 0


class FrameExp(gui.Experiment):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__(person)

    def elements(self):

        # Instructions
        self.instructions = QLabel('Press ' + self.person.leftkey[0] + ' for the left option and ' +
                                   self.person.rightkey[0] + ' for the right option')

        # Left and right options (and middle stuff) with font settingsguis
        self.left = QLabel('')
        self.left.setFont(QFont('Helvetica', 40))
        self.left.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.rightgain = QLabel('')
        self.rightgain.setFont(QFont('Helvetica', 40))
        self.rightgain.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.rightloss = QLabel('')
        self.rightloss.setFont(QFont('Helvetica', 40))
        self.rightloss.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Put gamble parts in vertical layout
        gamblelayout = QVBoxLayout()

        gamblelayout.addWidget(self.rightgain)
        gamblelayout.addWidget(self.rightloss)

        # Put Left and Right words for options in horizontal layout
        mainhlayout = QHBoxLayout()

        mainhlayout.addStretch(1)
        mainhlayout.addWidget(self.left)
        mainhlayout.addStretch(1)
        mainhlayout.addWidget(self.middle)
        mainhlayout.addStretch(1)
        mainhlayout.addLayout(gamblelayout)
        mainhlayout.addStretch(1)

        # Put everything in vertical layout
        self.instquitlayout.addWidget(self.instructions)
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addLayout(mainhlayout)
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addWidget(self.quitbutton)

        # Set up layout
        self.setLayout(self.instquitlayout)

    def iti(self):

        self.left.setText('')
        self.rightgain.setText('')
        self.rightloss.setText('')
        self.middle.setText('+')

        if self.trialsdone > 0:

            endtime = time.time()
            rt = endtime - self.starttime

            self.person.updateoutput(self.trialsdone, self.starttime, rt, self.response)

        else:
            self.ititimer.start(1000)

        self.person.set_design_text()

        if (self.person.fmri == 'No') & (self.trialsdone > 0):
            self.ititimer.start(1000)

    def generatenext(self):

        self.ititimer().stop()
        if self.trialsdone < self.person.get_trials():

            self.trialsdone += 1

            info = self.person.get_design_text()
            self.left.setText(info[0])

            self.rightgain.setText(info[1])
            self.rightloss.setText(info[2])

            self.middle.setText('OR')

            self.starttime = time.time()

            self.timer.start(5000)

            self.responseenabled = 1

            if self.person.fmri == 'Yes':
                self.ititimer.start(5500)

        else:
            self.person.output()

            self.left.setText('')
            self.rightgain.setText('')
            self.rightloss.setText('')

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

        self.responseenabled = 0

        self.left.setText('')

        self.rightgain.setText('')
        self.rightloss.setText('')
        self.middle.setText('Please try to be quicker')

        if self.person.fmri == 'No':
            self.trialresettimer.start(1000)

        else:
            self.response = 'None'
            self.iti()

    def responsereset(self):

        self.trialresettimer.stop()

        info = self.person.get_design_text()
        self.left.setText(info[0])

        self.rightgain.setText(info[1])
        self.rightloss.setText(info[2])

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
