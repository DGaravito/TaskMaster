from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QProgressBar
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QTimer, pyqtSignal


class DDiscountExp(QWidget):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__()

        self.inst = 0
        self.response = 0
        self.person = person
        self.trialsdone = 0

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
        self.instructions = QLabel('Press C for the left option and M for the right option')

        # setting font style and size
        self.instructions.setFont(QFont('Helvetica', 25))

        # center Instructions
        self.instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Left and right options (and middle stuff) with font settingsguis
        self.left = QLabel('')
        self.left.setFont(QFont('Helvetica', 40))

        self.right = QLabel('')
        self.right.setFont(QFont('Helvetica', 40))

        self.middle = QLabel('Press G to Start')
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

    def jitter(self):

        self.left.setText('')
        self.right.setText('')
        self.middle.setText('+')

        self.person.engineupdate(self.response)

        self.person.updateoutput(self.response, self.trialsdone)

        self.timerjitter.start(1000)

    def generatenext(self):

        self.timerjitter.stop()
        if self.trialsdone == 0:

            strings = self.person.get_design_text()
            self.left.setText(strings[0])
            self.right.setText(strings[1])
            self.middle.setText('OR')

            self.trialsdone += 1

            self.timerresponse.start(5000)

        elif self.person.get_trials() > self.trialsdone:

            self.person.engineupdate(self.response)

            strings = self.person.get_design_text()
            self.left.setText(strings[0])
            self.right.setText(strings[1])
            self.middle.setText('OR')

            self.trialsdone += 1

            self.timerresponse.start(5000)

        else:
            self.person.output()

            self.left.setText('')
            self.right.setText('')
            self.instructions.setText('Thank you!')
            self.middle.setText('You may now quit the application.')

    def timerwarning(self):

        self.timerresponse.stop()

        self.left.setText('')
        self.right.setText('')
        self.middle.setText('Please try to be quicker')

        self.timerreset.start(1000)

    def responsereset(self):

        self.timerreset.stop()

        strings = self.person.get_design_text()
        self.left.setText(strings[0])
        self.right.setText(strings[1])

        self.middle.setText('OR')

        self.timerresponse.start(5000)

    def keyaction(self, key):

        self.timerresponse.stop()

        if key == 'c':
            self.response = 0
            self.jitter()

        elif key == 'm':
            self.response = 1
            self.jitter()

        elif key in ['g', 'G']:
            self.generatenext()

        elif key in ['i', 'I']:
            self.inst += 1

            self.middle.setText(self.person.get_instructions(self.inst))

            if self.inst == 5:
                self.inst = 0


class PDiscountExp(QWidget):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__()

        self.response = 0
        self.person = person
        self.trialsdone = 0
        self.inst = 0

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
        self.instructions = QLabel('Press C for the left option and M for the right option')

        # setting font style and size
        self.instructions.setFont(QFont('Helvetica', 25))

        # center Instructions
        self.instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Left and right options (and middle stuff) with font settingsguis
        self.left = QLabel('')
        self.left.setFont(QFont('Helvetica', 40))

        self.right = QLabel('')
        self.right.setFont(QFont('Helvetica', 40))

        self.middle = QLabel('Press G to Start')
        self.middle.setFont(QFont('Helvetica', 30))

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

        # Put everything in vertical layout

        instquitlayout.addWidget(self.instructions)
        instquitlayout.addStretch(1)
        instquitlayout.addLayout(expverblayout)
        instquitlayout.addStretch(1)
        instquitlayout.addLayout(expvislayout)
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
        self.leftbar.setValue(0)
        self.right.setText('')
        self.rightbar.setValue(0)
        self.middle.setText('+')

        if self.trialsdone != 0:

            self.person.updateoutput(self.response, self.trialsdone)

        self.person.set_design_text()

        self.timerjitter.start(1000)

    def generatenext(self):

        self.timerjitter.stop()
        if self.person.get_trials() > self.trialsdone:

            info = self.person.get_design_text()
            self.left.setText(info[0])
            self.leftbar.setValue(100)

            self.right.setText(info[1])
            self.rightbar.setValue(info[2])

            self.middle.setText('OR')

            self.trialsdone += 1

            self.timerresponse.start(5000)

        else:
            self.person.output()

            self.left.setText('')
            self.right.setText('')
            self.instructions.setText('Thank you!')
            self.middle.setText('You may now quit the application.')

    def timerwarning(self):

        self.timerresponse.stop()

        self.left.setText('')
        self.leftbar.setValue(0)

        self.right.setText('')
        self.rightbar.setValue(0)
        self.middle.setText('Please try to be quicker')

        self.timerreset.start(1000)

    def responsereset(self):

        self.timerreset.stop()

        info = self.person.get_design_text()
        self.left.setText(info[0])
        self.leftbar.setValue(100)

        self.right.setText(info[1])
        self.rightbar.setValue(info[2])

        self.middle.setText('OR')

        self.timerresponse.start(5000)

    def keyaction(self, key):

        self.timerresponse.stop()

        if key == 'c':
            self.response = 0
            self.jitter()

        elif key == 'm':
            self.response = 1
            self.jitter()

        elif key in ['g', 'G']:
            self.jitter()

        elif key in ['i', 'I']:
            self.inst += 1

            self.middle.setText(self.person.get_instructions(self.inst))

            if self.inst == 5:
                self.inst = 0


class CEDiscountExp(QWidget):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__()

        self.inst = 0
        self.response = 0
        self.person = person
        self.trialsdone = 0

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
        self.instructions = QLabel('Press C for the left option and M for the right option')

        # setting font style and size
        self.instructions.setFont(QFont('Helvetica', 25))

        # center Instructions
        self.instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Left and right options (and middle stuff) with font settingsguis
        self.left = QLabel('')
        self.left.setFont(QFont('Helvetica', 40))

        self.right = QLabel('')
        self.right.setFont(QFont('Helvetica', 40))

        self.middle = QLabel('Press G to Start')
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

    def jitter(self):

        self.left.setText('')
        self.right.setText('')
        self.middle.setText('+')

        self.person.engineupdate(self.response)

        self.person.updateoutput(self.response, self.trialsdone)

        self.timerjitter.start(1000)

    def generatenext(self):

        self.timerjitter.stop()
        if self.trialsdone == 0:

            strings = self.person.get_design_text()
            self.left.setText(strings[0])
            self.right.setText(strings[1])
            self.middle.setText('OR')

            self.trialsdone += 1

            self.timerresponse.start(5000)

        elif self.person.get_trials() > self.trialsdone:

            self.person.engineupdate(self.response)

            strings = self.person.get_design_text()
            self.left.setText(strings[0])
            self.right.setText(strings[1])
            self.middle.setText('OR')

            self.trialsdone += 1

            self.timerresponse.start(5000)

        else:
            self.person.output()

            self.left.setText('')
            self.right.setText('')
            self.instructions.setText('Thank you!')
            self.middle.setText('You may now quit the application.')

    def timerwarning(self):

        self.timerresponse.stop()

        self.left.setText('')
        self.right.setText('')
        self.middle.setText('Please try to be quicker')

        self.timerreset.start(1000)

    def responsereset(self):

        self.timerreset.stop()

        strings = self.person.get_design_text()
        self.left.setText(strings[0])
        self.right.setText(strings[1])

        self.middle.setText('OR')

        self.timerresponse.start(5000)

    def keyaction(self, key):

        self.timerresponse.stop()

        if key == 'c':
            self.response = 0
            self.jitter()

        elif key == 'm':
            self.response = 1
            self.jitter()

        elif key in ['g', 'G']:
            self.generatenext()

        elif key in ['i', 'I']:
            self.inst += 1

            self.middle.setText(self.person.get_instructions(self.inst))

            if self.inst == 6:
                self.inst = 0
