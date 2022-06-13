import time
import random

from PyQt6.QtWidgets import QLabel, QHBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal

from expguis import gui


class NACTExp(gui.Experiment):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__(person)

    def elements(self):
        # Instructions
        self.instructions.setText('Press ' + self.person.leftkey[0] + ' for |. Press ' + self.person.rightkey[0] +
                                  ' for -.')

        # Make middle layout for pictures and text
        middlelayout = QHBoxLayout()

        self.left = QLabel('')
        self.left.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left.setScaledContents(True)

        self.right = QLabel('')
        self.right.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.right.setScaledContents(True)

        middlelayout.addStretch(1)
        middlelayout.addWidget(self.left)
        middlelayout.addStretch(1)
        middlelayout.addWidget(self.middle)
        middlelayout.addStretch(1)
        middlelayout.addWidget(self.right)
        middlelayout.addStretch(1)

        # Make middle top for pictures
        middletoplayout = QHBoxLayout()

        self.topleft = QLabel('')
        self.topleft.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.topleft.setScaledContents(True)

        self.topright = QLabel('')
        self.topright.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.topright.setScaledContents(True)

        middletoplayout.addStretch(1)
        middletoplayout.addWidget(self.topleft)
        middletoplayout.addStretch(1)
        middletoplayout.addWidget(self.topright)
        middletoplayout.addStretch(1)

        # Make middle bottom for pictures

        middlebottomlayout = QHBoxLayout()

        self.bottomleft = QLabel('')
        self.bottomleft.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bottomleft.setScaledContents(True)

        self.bottomright = QLabel('')
        self.bottomright.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bottomright.setScaledContents(True)

        middlebottomlayout.addStretch(1)
        middlebottomlayout.addWidget(self.bottomleft)
        middlebottomlayout.addStretch(1)
        middlebottomlayout.addWidget(self.bottomright)
        middlebottomlayout.addStretch(1)

        # Put everything in vertical layout

        self.instquitlayout.addWidget(self.instructions)
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addLayout(middletoplayout)
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addLayout(middlelayout)
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addLayout(middlebottomlayout)
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addWidget(self.quitbutton)

        # Set up layout

        self.setLayout(self.instquitlayout)

    def generatenext(self):

        if self.trialsdone < self.person.get_trials():

            if self.trialsdone != 0:

                self.ititimer.stop()

            self.pixmaps = []

            self.picstrings = self.person.get_trial_pic()

            for pic in self.picstrings:

                pathstring = 'assets/' + pic + '.bmp'
                self.pixmaps.append(QPixmap(pathstring))

            self.topleft.setPixmap(self.pixmaps[0].scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio))
            self.left.setPixmap(self.pixmaps[1].scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio))
            self.bottomleft.setPixmap(self.pixmaps[2].scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio))
            self.bottomright.setPixmap(self.pixmaps[3].scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio))
            self.right.setPixmap(self.pixmaps[4].scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio))
            self.topright.setPixmap(self.pixmaps[5].scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio))

            self.middle.setText('+')

            self.starttime = time.time()

            randomtimer = random.randint(1200, 1500)

            self.timer.start(randomtimer)
            self.ititimer.start(randomtimer+1000)

            self.responseenabled = 1

        else:

            self.ititimer.stop()

            self.trialsdone = 0

            self.topleft.setPixmap(QPixmap())
            self.left.setPixmap(QPixmap())
            self.bottomleft.setPixmap(QPixmap())
            self.bottomright.setPixmap(QPixmap())
            self.right.setPixmap(QPixmap())
            self.topright.setPixmap(QPixmap())

            self.middle.setText(self.person.nextround())

            if self.person.part == 3:

                self.person.output()
                self.instructions.setText('Thank you!')

            else:
                self.betweenrounds = 1

    def iti(self):

        self.topleft.setPixmap(QPixmap())
        self.left.setPixmap(QPixmap())
        self.bottomleft.setPixmap(QPixmap())
        self.bottomright.setPixmap(QPixmap())
        self.right.setPixmap(QPixmap())
        self.topright.setPixmap(QPixmap())

    def timeout(self):

        self.timer.stop()

        self.responseenabled = 0

        endtime = time.time()
        rt = endtime - self.starttime

        self.middle.setText(self.person.updateoutput(self.trialsdone, self.starttime, rt, 3))

        self.iti()

    def keyaction(self, key):

        if (key in ['g', 'G']) & (self.betweenrounds == 1):

            self.middle.setText('')
            self.inst = 0
            self.generatenext()
            self.betweenrounds = 0

        if (key in self.person.rightkey) & (self.responseenabled == 1):

            self.responseenabled = 0

            self.timer.stop()
            self.trialsdone += 1

            endtime = time.time()
            rt = endtime - self.starttime

            self.middle.setText(self.person.updateoutput(self.trialsdone, self.starttime, rt, 1))

            self.iti()

        if (key in self.person.leftkey) & (self.responseenabled == 1):

            self.responseenabled = 0

            self.timer.stop()
            self.trialsdone += 1

            endtime = time.time()
            rt = endtime - self.starttime

            self.middle.setText(self.person.updateoutput(self.trialsdone, self.starttime, rt, 0))

            self.iti()

        if (key in ['i', 'I']) & (self.betweenrounds == 1):

            self.inst += 1

            if self.person.part == 1:

                if self.inst == 4:
                    pixmap = QPixmap('assets/NACT_Part1Ex1.bmp')
                    self.middle.setPixmap(pixmap.scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio))

                elif self.inst == 5:
                    pixmap = QPixmap('assets/NACT_Part1Ex2.bmp')
                    self.middle.setPixmap(pixmap.scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio))

                elif self.inst == 12:
                    pixmap = QPixmap('assets/NACT_FixEx.bmp')
                    self.middle.setPixmap(pixmap.scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio))

                else:
                    self.middle.setText(self.person.get_instructions(self.inst))

                if self.inst == 14:
                    self.inst = 0

            else:

                if self.inst == 5:
                    pixmap = QPixmap('assets/NACT_Part2Ex1.bmp')
                    self.middle.setPixmap(pixmap.scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio))

                elif self.inst == 6:
                    pixmap = QPixmap('assets/NACT_Part2Ex2.bmp')
                    self.middle.setPixmap(pixmap.scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio))

                elif self.inst == 8:
                    pixmap = QPixmap('assets/NACT_FixEx.bmp')
                    self.middle.setPixmap(pixmap.scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio))

                else:
                    self.middle.setText(self.person.get_instructions(self.inst))

                if self.inst == 13:
                    self.inst = 0
