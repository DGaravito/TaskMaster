import random
import time
from pathlib import Path

from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QProgressBar
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QDir


class ARTTExp(QWidget):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__()

        self.response = 0
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

        # add the assets folder

        toassets = str(Path('..').resolve())
        QDir.addSearchPath('assets', toassets)

        # Add in elements
        self.elements()

        # Show all elements
        self.showMaximized()

        # Attach keyboard keys to functions
        self.keyPressed.connect(self.keyaction)

        # Make timer for jitter screen
        self.timerjitter = QTimer()
        self.timerjitter.timeout.connect(self.generatenext)

        # Make timer for participants taking too long
        self.timerresponse = QTimer()
        self.timerresponse.timeout.connect(self.timerwarning)

        # Make timer for resetting after the above time warning
        self.timerreset = QTimer()
        self.timerreset.timeout.connect(self.responsereset)

    def elements(self):

        # Make overarching layout
        instquitlayout = QVBoxLayout()

        # Quit button
        self.quitbutton = QPushButton('Quit')
        self.quitbutton.clicked.connect(QApplication.instance().quit)
        self.quitbutton.setFixedWidth(40)
        self.quitbutton.setFixedHeight(20)

        # Instructions
        self.instructions = QLabel('Press ' + self.leftkey[0] + ' for the left option and ' + self.rightkey[0]
                                   + ' for the right option')

        # setting font style and size
        self.instructions.setFont(QFont('Helvetica', 25))

        # center Instructions
        self.instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Left option (and middle stuff) with font settingsguis
        self.left = QLabel('')
        self.left.setFont(QFont('Helvetica', 40))
        self.left.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.middle = QLabel('Press G to Start')
        self.middle.setFont(QFont('Helvetica', 30))
        self.middle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Set up right option stuff

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

    def jitter(self):

        self.left.setText('')

        self.rightpic.setPixmap(QPixmap())
        self.righttoptext.setText('')
        self.rightbottomtext.setText('')

        self.middle.setText('+')

        if self.trialsdone > 0:

            endtime = time.time()
            rt = endtime - self.starttime

            self.person.engineupdate(self.response)

            self.person.updateoutput(self.trialsdone, self.starttime, rt, self.response)

        self.timerjitter.start(1000)

    def generatenext(self):

        self.timerjitter.stop()
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

            self.timerresponse.start(5000)

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

    def timerwarning(self):

        self.timerresponse.stop()

        self.left.setText('')

        self.rightpic.setPixmap(QPixmap())
        self.righttoptext.setText('')
        self.rightbottomtext.setText('')

        self.middle.setText('Please try to be quicker')

        self.timerreset.start(1000)

    def responsereset(self):

        self.timerreset.stop()

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

        self.timerresponse.start(5000)

    def keyaction(self, key):

        self.timerresponse.stop()

        if key in self.leftkey:
            self.response = 0
            self.jitter()

        elif key in self.rightkey:
            self.response = 1
            self.jitter()

        elif key in ['g', 'G']:
            self.generatenext()

        elif key in ['i', 'I']:
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


class RAExp(QWidget):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__()

        self.response = 0
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

        # Make timer for jitter screen
        self.timerjitter = QTimer()
        self.timerjitter.timeout.connect(self.generatenext)

        # Make timer for participants taking too long
        self.timerresponse = QTimer()
        self.timerresponse.timeout.connect(self.timerwarning)

        # Make timer for resetting after the above time warning
        self.timerreset = QTimer()
        self.timerreset.timeout.connect(self.responsereset)

    def elements(self):

        # Make overarching layout
        instquitlayout = QVBoxLayout()

        # Quit button
        self.quitbutton = QPushButton('Quit')
        self.quitbutton.clicked.connect(QApplication.instance().quit)
        self.quitbutton.setFixedWidth(40)
        self.quitbutton.setFixedHeight(20)

        # Instructions
        self.instructions = QLabel('Press ' + self.leftkey[0] + ' for the left option and ' + self.rightkey[0]
                                   + ' for the right option')

        # setting font style and size
        self.instructions.setFont(QFont('Helvetica', 25))

        # center Instructions
        self.instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)

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

        self.middle = QLabel('Press G to Start')
        self.middle.setFont(QFont('Helvetica', 30))
        self.middle.setAlignment(Qt.AlignmentFlag.AlignCenter)

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

        instquitlayout.addWidget(self.instructions)
        instquitlayout.addStretch(1)
        instquitlayout.addLayout(mainhlayout)
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

    def jitter(self):

        self.left.setText('')
        self.rightgain.setText('')
        self.rightloss.setText('')
        self.middle.setText('+')

        endtime = time.time()
        rt = endtime - self.starttime

        self.person.updateoutput(self.trialsdone, self.starttime, rt, self.response)

        self.person.set_design_text()

        self.timerjitter.start(1000)

    def generatenext(self):

        self.timerjitter.stop()
        if self.trialsdone < self.person.get_trials():

            self.trialsdone += 1

            info = self.person.get_design_text()
            self.left.setText('Getting $0')

            self.rightgain.setText(info[0])
            self.rightloss.setText(info[1])

            self.middle.setText('OR')

            self.starttime = time.time()

            self.timerresponse.start(5000)

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

    def timerwarning(self):

        self.timerresponse.stop()

        self.left.setText('')

        self.rightgain.setText('')
        self.rightloss.setText('')
        self.middle.setText('Please try to be quicker')

        self.timerreset.start(1000)

    def responsereset(self):

        self.timerreset.stop()

        info = self.person.get_design_text()
        self.left.setText('0')

        self.rightgain.setText(info[0])
        self.rightloss.setText(info[1])

        self.middle.setText('OR')

        self.timerresponse.start(5000)

    def keyaction(self, key):

        self.timerresponse.stop()

        if key in self.leftkey:
            self.response = 0
            self.jitter()

        elif key in self.rightkey:
            self.response = 1
            self.jitter()

        elif key in ['g', 'G']:
            self.generatenext()

        elif key in ['i', 'I']:
            self.inst += 1

            self.middle.setText(self.person.get_instructions(self.inst))

            if self.inst == 5:
                self.inst = 0


class FrameExp(QWidget):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__()

        self.response = 0
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

        # Make timer for jitter screen
        self.timerjitter = QTimer()
        self.timerjitter.timeout.connect(self.generatenext)

        # Make timer for participants taking too long
        self.timerresponse = QTimer()
        self.timerresponse.timeout.connect(self.timerwarning)

        # Make timer for resetting after the above time warning
        self.timerreset = QTimer()
        self.timerreset.timeout.connect(self.responsereset)

    def elements(self):

        # Make overarching layout
        instquitlayout = QVBoxLayout()

        # Quit button
        self.quitbutton = QPushButton('Quit')
        self.quitbutton.clicked.connect(QApplication.instance().quit)
        self.quitbutton.setFixedWidth(40)
        self.quitbutton.setFixedHeight(20)

        # Instructions
        self.instructions = QLabel('Press ' + self.leftkey[0] + ' for the left option and ' + self.rightkey[0]
                                   + ' for the right option')

        # setting font style and size
        self.instructions.setFont(QFont('Helvetica', 25))

        # center Instructions
        self.instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)

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

        self.middle = QLabel('Press G to Start')
        self.middle.setFont(QFont('Helvetica', 30))
        self.middle.setAlignment(Qt.AlignmentFlag.AlignCenter)

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

        instquitlayout.addWidget(self.instructions)
        instquitlayout.addStretch(1)
        instquitlayout.addLayout(mainhlayout)
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

    def jitter(self):

        self.left.setText('')
        self.rightgain.setText('')
        self.rightloss.setText('')
        self.middle.setText('+')

        if self.trialsdone > 0:

            endtime = time.time()
            rt = endtime - self.starttime

            self.person.updateoutput(self.trialsdone, self.starttime, rt, self.response)

        self.person.set_design_text()

        self.timerjitter.start(1000)

    def generatenext(self):

        self.timerjitter.stop()
        if self.trialsdone < self.person.get_trials():

            self.trialsdone += 1

            info = self.person.get_design_text()
            self.left.setText(info[0])

            self.rightgain.setText(info[1])
            self.rightloss.setText(info[2])

            self.middle.setText('OR')

            self.starttime = time.time()

            self.timerresponse.start(5000)

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

    def timerwarning(self):

        self.timerresponse.stop()

        self.left.setText('')

        self.rightgain.setText('')
        self.rightloss.setText('')
        self.middle.setText('Please try to be quicker')

        self.timerreset.start(1000)

    def responsereset(self):

        self.timerreset.stop()

        info = self.person.get_design_text()
        self.left.setText(info[0])

        self.rightgain.setText(info[1])
        self.rightloss.setText(info[2])

        self.middle.setText('OR')

        self.timerresponse.start(5000)

    def keyaction(self, key):

        self.timerresponse.stop()

        if key in self.leftkey:
            self.response = 0
            self.jitter()

        elif key in self.rightkey:
            self.response = 1
            self.jitter()

        elif key in ['g', 'G']:
            self.jitter()

        elif key in ['i', 'I']:
            self.inst += 1

            self.middle.setText(self.person.get_instructions(self.inst))

            if self.inst == 5:
                self.inst = 0
