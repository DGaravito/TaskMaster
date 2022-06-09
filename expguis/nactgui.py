import time
from pathlib import Path
import random

from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QDir


class NACTExp(QWidget):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__()

        self.person = person
        self.trialsdone = 0
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

        self.ititimer = QTimer()
        self.ititimer.timeout.connect(self.generatenext)

    def elements(self):

        # Make overarching layout
        mainlayout = QVBoxLayout()

        # Quit button
        self.quitbutton = QPushButton('Quit')
        self.quitbutton.clicked.connect(QApplication.instance().quit)
        self.quitbutton.setFixedWidth(40)
        self.quitbutton.setFixedHeight(20)

        # Instructions
        self.instructions = QLabel('Press ' + self.leftkey[0] + ' for |. Press ' + self.rightkey[0] +
                                   ' for -.')

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
        self.middle.setAlignment(Qt.AlignmentFlag.AlignCenter)

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

        mainlayout.addWidget(self.instructions)
        mainlayout.addStretch(1)
        mainlayout.addLayout(middletoplayout)
        mainlayout.addStretch(1)
        mainlayout.addLayout(middlelayout)
        mainlayout.addStretch(1)
        mainlayout.addLayout(middlebottomlayout)
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

    def iti(self, reaction, response=3):

        self.topleft.setPixmap(QPixmap())
        self.left.setPixmap(QPixmap())
        self.bottomleft.setPixmap(QPixmap())
        self.bottomright.setPixmap(QPixmap())
        self.right.setPixmap(QPixmap())
        self.topright.setPixmap(QPixmap())

        self.middle.setText(self.person.updateoutput(self.trialsdone, self.starttime, reaction, response))

        self.ititimer.start(1000)

    def timeout(self):

        self.timer.stop()

        endtime = time.time()
        rt = endtime - self.starttime

        self.iti(rt)

    def keyaction(self, key):

        if key in ['g', 'G']:

            self.middle.setText('')
            self.inst = 0
            self.generatenext()

        if key in self.rightkey:

            self.timer.stop()
            self.trialsdone += 1

            endtime = time.time()
            rt = endtime - self.starttime

            self.iti(rt, 1)

        if key in self.leftkey:

            self.timer.stop()
            self.trialsdone += 1

            endtime = time.time()
            rt = endtime - self.starttime

            self.iti(rt, 0)

        if key in ['i', 'I']:

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
