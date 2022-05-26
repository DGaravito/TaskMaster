import time
from pathlib import Path

from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QProgressBar,\
    QDialog, QGridLayout
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QDir


class DDiscountExp(QWidget):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__()

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

        # Make timer for participant taking too long
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

        # Left and right options (and middle stuff) with font settings
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


class PDiscountExp(QWidget):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__()

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

        # Make timer for participant taking too long
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

        # Left and right options (and middle stuff) with font settings
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


class ARTTExp(QWidget):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__()

        self.response = 0
        self.person = person
        self.trialsdone = 0

        # Window title
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # center window
        self.centerscreen()

        # add the assets folder

        toassets = str(Path('.').resolve())
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

        # Make timer for participant taking too long
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

        # Left option (and middle stuff) with font settings
        self.left = QLabel('')
        self.left.setFont(QFont('Helvetica', 40))

        self.middle = QLabel('Press G to Start')
        self.middle.setFont(QFont('Helvetica', 30))

        # Set up right option stuff

        self.righttoptext = QLabel('')
        self.righttoptext.setFont(QFont('Helvetica', 40))

        self.rightpic = QLabel()
        self.rightpic.setPixmap(QPixmap())

        self.rightbottomtext = QLabel('')
        self.rightbottomtext.setFont(QFont('Helvetica', 40))

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

            self.person.engineupdate(self.response)

            self.person.updateoutput(self.response, self.trialsdone)

        self.timerjitter.start(1000)

    def generatenext(self):

        self.timerjitter.stop()
        if self.trialsdone < self.person.get_trials():

            info = self.person.get_design_text()
            self.left.setText(info[0])

            pixmap = 'assets/' + info[2]
            self.rightpic.setPixmap(QPixmap(pixmap))
            self.righttoptext.setText(info[1])
            self.rightbottomtext.setText('0')

            self.middle.setText('OR')

            self.trialsdone += 1

            self.timerresponse.start(5000)

        else:
            self.person.output()

            self.left.setText('')

            self.righttoptext.setText('')
            self.righttoptext.setText('')

            self.instructions.setText('Thank you!')
            self.middle.setText('You may now quit the application.')

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
        self.righttoptext.setText(info[1])
        self.rightbottomtext.setText('0')

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


class RAExp(QWidget):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__()

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

        # Make timer for participant taking too long
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

        # Left and right options (and middle stuff) with font settings
        self.left = QLabel('')
        self.left.setFont(QFont('Helvetica', 40))

        self.rightgain = QLabel('')
        self.rightgain.setFont(QFont('Helvetica', 40))

        self.rightloss = QLabel('')
        self.rightloss.setFont(QFont('Helvetica', 40))

        self.middle = QLabel('Press G to Start')
        self.middle.setFont(QFont('Helvetica', 30))

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

        self.person.updateoutput(self.response, self.trialsdone)

        self.person.set_design_text()

        self.timerjitter.start(1000)

    def generatenext(self):

        self.timerjitter.stop()
        if self.trialsdone < self.person.get_trials():

            info = self.person.get_design_text()
            self.left.setText('Getting $0')

            self.rightgain.setText(info[0])
            self.rightloss.setText(info[1])

            self.middle.setText('OR')

            self.trialsdone += 1

            self.timerresponse.start(5000)

        else:
            self.person.output()

            self.left.setText('')
            self.rightgain.setText('')
            self.rightloss.setText('')
            self.instructions.setText('Thank you!')
            self.middle.setText('You may now quit the application.')

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

        if key in ['c', 'C']:
            self.response = 0
            self.jitter()

        elif key in ['m', 'M']:
            self.response = 1
            self.jitter()

        elif key in ['g', 'G']:
            self.generatenext()


class FrameExp(QWidget):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__()

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

        # Make timer for participant taking too long
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

        # Left and right options (and middle stuff) with font settings
        self.left = QLabel('')
        self.left.setFont(QFont('Helvetica', 40))

        self.rightgain = QLabel('')
        self.rightgain.setFont(QFont('Helvetica', 40))

        self.rightloss = QLabel('')
        self.rightloss.setFont(QFont('Helvetica', 40))

        self.middle = QLabel('Press G to Start')
        self.middle.setFont(QFont('Helvetica', 30))

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

            self.person.updateoutput(self.response, self.trialsdone)

        self.person.set_design_text()

        self.timerjitter.start(1000)

    def generatenext(self):

        self.timerjitter.stop()
        if self.trialsdone < self.person.get_trials():

            info = self.person.get_design_text()
            self.left.setText(info[0])

            self.rightgain.setText(info[1])
            self.rightloss.setText(info[2])

            self.middle.setText('OR')

            self.trialsdone += 1

            self.timerresponse.start(5000)

        else:
            self.person.output()

            self.left.setText('')
            self.rightgain.setText('')
            self.rightloss.setText('')
            self.instructions.setText('Thank you!')
            self.middle.setText('You may now quit the application.')

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

        if key in ['c', 'C']:
            self.response = 0
            self.jitter()

        elif key in ['m', 'M']:
            self.response = 1
            self.jitter()

        elif key in ['g', 'G']:
            self.jitter()


class BeadsInventory(QDialog):
    """
        This is a popup window that contains the participant's 'inventory' in the beads task. It has a grid layout of
        all of the beads they have draw in that round.
        """

    def __init__(self, list):
        super().__init__()

        self.setWindowTitle('Beads you have drawn')

        # Make  layout
        layout = QGridLayout()

        one = QLabel().setPixmap(list[0])
        two = QLabel().setPixmap(list[1])
        three = QLabel().setPixmap(list[2])
        four = QLabel().setPixmap(list[3])
        five = QLabel().setPixmap(list[4])
        six = QLabel().setPixmap(list[5])
        seven = QLabel().setPixmap(list[6])
        eight = QLabel().setPixmap(list[7])
        nine = QLabel().setPixmap(list[8])
        ten = QLabel().setPixmap(list[9])
        eleven = QLabel().setPixmap(list[10])
        twelve = QLabel().setPixmap(list[11])
        thirteen = QLabel().setPixmap(list[12])
        fourteen = QLabel().setPixmap(list[13])
        fifteen = QLabel().setPixmap(list[14])
        sixteen = QLabel().setPixmap(list[15])
        seventeen = QLabel().setPixmap(list[16])
        eighteen = QLabel().setPixmap(list[17])
        nineteen = QLabel().setPixmap(list[18])
        twenty = QLabel().setPixmap(list[19])

        layout.addWidget(one, 0, 0)
        layout.addWidget(two, 0, 1)
        layout.addWidget(three, 0, 2)
        layout.addWidget(four, 0, 3)
        layout.addWidget(five, 0, 4)
        layout.addWidget(six, 1, 0)
        layout.addWidget(seven, 1, 1)
        layout.addWidget(eight, 1, 2)
        layout.addWidget(nine, 1, 3)
        layout.addWidget(ten, 1, 4)
        layout.addWidget(eleven, 2, 0)
        layout.addWidget(twelve, 2, 1)
        layout.addWidget(thirteen, 2, 2)
        layout.addWidget(fourteen, 2, 3)
        layout.addWidget(fifteen, 2, 4)
        layout.addWidget(sixteen, 3, 0)
        layout.addWidget(seventeen, 3, 1)
        layout.addWidget(eighteen, 3, 2)
        layout.addWidget(nineteen, 3, 3)
        layout.addWidget(twenty, 3, 4)

        self.setLayout(layout)


class BeadsExp(QWidget):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__()

        self.inst = 0
        self.response = 0
        self.person = person
        self.roundsdone = 0
        self.beadsdrawn = 0
        self.beadlist = ['',
                         '',
                         '',
                         '',
                         '',
                         '',
                         '',
                         '',
                         '',
                         '',
                         '',
                         '',
                         '',
                         '',
                         '',
                         '',
                         '',
                         '',
                         '',
                         '']

        # Window title
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # center window
        self.centerscreen()

        # Add in elements
        self.elements()

        # Show all elements
        self.showMaximized()

        # Make timer for jitter screen
        self.jittertimer = QTimer()
        self.jittertimer.timeout.connect(self.newround)

        # Make timer for jitter screen
        self.starttimer = QTimer()
        self.starttimer.timeout.connect(self.startround)

        # Attach keyboard keys to functions
        self.keyPressed.connect(self.keyaction)

        # Attach left and right to functions
        self.left.mouseReleaseEvent = lambda: self.chosejar('Red')
        self.right.mouseReleaseEvent = lambda: self.chosejar('Blue')

    def elements(self):

        # Make overarching layout
        totallayout = QVBoxLayout()

        # Quit button
        self.quitbutton = QPushButton('Quit')
        self.quitbutton.clicked.connect(QApplication.instance().quit)
        self.quitbutton.setFixedWidth(40)
        self.quitbutton.setFixedHeight(20)

        # Inventory button
        self.invbutton = QPushButton('Beads you\'ve drawn')
        self.invbutton.clicked.connect(BeadsInventory.exec)

        # Instructions
        self.instructions = QLabel('Press \"M\" to draw a bead and \"C\" to choose a jar')

        # setting font style and size
        self.instructions.setFont(QFont('Helvetica', 25))

        # center Instructions
        self.instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # add the assets folder

        toassets = str(Path('.').resolve())
        QDir.addSearchPath('assets', toassets)

        # Left and right options (and middle stuff) with font settings
        self.left = QLabel('')
        self.left.setFont(QFont('Helvetica', 40))

        self.right = QLabel('')
        self.right.setFont(QFont('Helvetica', 40))

        self.middle = QLabel('Press G to Start and I for Instructions')
        self.middle.setFont(QFont('Helvetica', 30))

        # Put Left and Right jars, plus middle for instructions, in horizontal layout
        mainhlayout = QHBoxLayout()

        mainhlayout.addStretch(1)
        mainhlayout.addWidget(self.left)
        mainhlayout.addStretch(1)
        mainhlayout.addWidget(self.middle)
        mainhlayout.addStretch(1)
        mainhlayout.addWidget(self.right)
        mainhlayout.addStretch(1)

        # Put inventory and quit button in horizontal layout
        quitinvlayout = QHBoxLayout()

        quitinvlayout.addWidget(self.quitbutton)
        quitinvlayout.addStretch(1)
        quitinvlayout.addWidget(self.invbutton)

        # Put everything in vertical layout

        totallayout.addWidget(self.instructions)
        totallayout.addStretch(1)
        totallayout.addLayout(mainhlayout)
        totallayout.addStretch(1)
        totallayout.addLayout(quitinvlayout)

        # Set up layout

        self.setLayout(totallayout)

    def centerscreen(self):

        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def keyPressEvent(self, keyevent):
        self.keyPressed.emit(keyevent.text())

    def jitter(self):

        self.left.setPixmap(QPixmap())
        self.right.setPixmap(QPixmap())
        self.middle.setText('+')

        self.jittertimer.start(1000)

    def newround(self):

        self.jittertimer.stop()
        self.middle.setText(self.person.nextround(self.roundsdone))
        self.roundsdone += 1
        self.starttimer.start(500)

    def startround(self):

        self.starttimer.stop()
        self.middle.setText('')

        leftpixmap = QPixmap('assets/BeadsTask_RedJar.png')
        rightpixmap = QPixmap('assets/BeadsTask_BlueJar.png')

        self.left.setPixmap(leftpixmap)
        self.right.setPixmap(rightpixmap)

        self.beadsdrawn = 0

        self.beadlist = ['',
                         '',
                         '',
                         '',
                         '',
                         '',
                         '',
                         '',
                         '',
                         '',
                         '',
                         '',
                         '',
                         '',
                         '',
                         '',
                         '',
                         '',
                         '',
                         '']

    def drawbead(self):

        newbead = 'assets/' + self.person.get_bead()

        self.beadlist[self.beadsdrawn] = newbead
        print('added')

        self.beadsdrawn += 1

        self.person.updateoutput(self.roundsdone, self.beadsdrawn)

    def chosejar(self, choice):

        self.person.updateoutput(self.roundsdone, self.beadsdrawn, 1, choice)

    def keyaction(self, key):

        if key in ['c', 'C']:
            self.middle.setText('Click on the jar you want to choose\nPress \"M\" to go back')

        elif key in ['m', 'M']:

            self.middle.setText('')

            if self.beadsdrawn < 20:
                self.drawbead()

            else:
                self.middle.setText('Max number of beads drawn')

        elif key in ['g', 'G']:
            self.jitter()

        elif key in ['i', 'I']:
            self.inst += 1
            self.middle.setText(self.person.get_instructions(self.inst))

            if self.inst == 20:

                self.inst = 0


class PBTExp(QWidget):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__()

        self.person = person
        self.trialsdone = 0
        self.roundsdone = 0

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
        self.instructions = QLabel('Press C for crosses. Press M for squares.')

        # setting font style and size
        self.instructions.setFont(QFont('Helvetica', 25))
        self.instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # add the assets folder

        toassets = str(Path('.').resolve())
        QDir.addSearchPath('assets', toassets)

        # Make middle for pictures and text

        middlelayout = QHBoxLayout()

        self.middle = QLabel('Please let the researcher know you are ready')
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

            self.middle.setPixmap(pixmap)

            self.starttime = time.time()

            self.timer.start(5000)

        else:

            self.ititimer.stop()

            self.roundsdone += 1

            self.middle.setPixmap(QPixmap())

            self.middle.setText(self.person.nextround(self.roundsdone))

            if self.person.rounds == self.roundsdone:

                self.person.output()
                self.instructions.setText('Thank you!')

    def iti(self):

        self.middle.setPixmap(QPixmap())

        self.ititimer.start(500)

    def timeout(self):

        self.timer.stop()

        endtime = time.time()
        rt = endtime - self.starttime

        self.person.updateoutput(self.trialsdone, self.picstring, rt, 'None')

        self.iti()

    def keyaction(self, key):

        if key in ['g', 'G']:

            self.middle.setText('')

            self.iti()

        if key in ['m', 'M']:

            self.timer.stop()
            self.trialsdone += 1

            endtime = time.time()
            rt = endtime - self.starttime

            self.person.updateoutput(self.trialsdone, self.picstring, rt, 'Square')
            self.iti()

        if key in ['c', 'C']:

            self.timer.stop()
            self.trialsdone += 1

            endtime = time.time()
            rt = endtime - self.starttime

            self.person.updateoutput(self.trialsdone, self.picstring, rt, 'Cross')
            self.iti()

        if key in ['i', 'I']:

            self.middle.setText(self.person.get_instructions(self.person.globallocal, self.person.instructions))


class PrExp(QWidget):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__()

        self.person = person
        self.trialsdone = 0

        self.structure = self.person.structure

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
        self.timermemory = QTimer()
        self.timermemory.timeout.connect(self.generatenext)

        # Make timer for new trial screen
        self.timer_newtrial = QTimer()
        self.timer_newtrial.timeout.connect(self.generatetrial)

    def elements(self):

        # Make overarching layout
        instquitlayout = QVBoxLayout()

        # Quit button
        self.quitbutton = QPushButton('Quit')
        self.quitbutton.clicked.connect(QApplication.instance().quit)
        self.quitbutton.setFixedWidth(40)
        self.quitbutton.setFixedHeight(20)

        # Instructions
        self.instructions = QLabel('')

        # setting font style and size
        self.instructions.setFont(QFont('Helvetica', 25))

        # center Instructions
        self.instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Left and right options (and middle stuff) with font settings
        self.left = QLabel('')
        self.left.setFont(QFont('Helvetica', 40))

        self.right = QLabel('')
        self.right.setFont(QFont('Helvetica', 40))

        self.middle = QLabel('Please let the researcher know you are ready')
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

            self.timermemory.start(5000)

        elif self.person.get_trials() > self.trialsdone:

            self.timermemory.stop()

            if self.structure[0] == 'S':

                strings = self.person.get_design_text()

            else:

                strings = self.person.get_design_text(1)

            self.left.setText(strings[0])
            self.right.setText(strings[1])
            self.middle.setText('')

            self.trialsdone += 1

            self.timermemory.start(5000)

        else:

            self.timermemory.stop()

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

                self.timer_newtrial.start(3000)

    def generatetrial(self):

        self.timer_newtrial.stop()

        self.trialsdone = 0

        string = self.person.starttrial()
        self.instructions.setText(string)

    def keyaction(self, key):

        if key in ['g', 'G']:
            self.generatenext()


class NbExp(QWidget):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__()

        self.person = person
        self.trialsdone = 0
        self.roundsdone = 0

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

    def elements(self):

        # Make overarching layout
        mainlayout = QVBoxLayout()

        # Quit button
        self.quitbutton = QPushButton('Quit')
        self.quitbutton.clicked.connect(QApplication.instance().quit)
        self.quitbutton.setFixedWidth(40)
        self.quitbutton.setFixedHeight(20)

        # Instructions
        self.instructions = QLabel('Press C if the letter is a false-alarm. Press M if the letter is a target')

        # setting font style and size
        self.instructions.setFont(QFont('Helvetica', 25))

        # center Instructions
        self.instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Make the middle for the actualy n-back task

        self.middle = QLabel(self.person.nextround(0))
        self.middle.setFont(QFont('Helvetica', 40))

        # center middle
        self.middle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Put everything in vertical layout

        mainlayout.addWidget(self.instructions)
        mainlayout.addStretch(1)
        mainlayout.addWidget(self.middle)
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

            self.middle.setText(self.person.get_trial_text())

            self.timer.start(3000)

        else:

            self.roundsdone += 1

            self.middle.setText(self.person.nextround(self.roundsdone))

            if self.person.rounds == self.roundsdone:

                self.person.output()
                self.instructions.setText('Thank you!')

    def timeout(self):

        self.timer.stop()

        self.trialsdone += 1

        self.person.updateoutput(self.trialsdone)
        self.generatenext()

        self.timer.start(3000)

    def keyaction(self, key):

        if key in ['g', 'G']:

            self.generatenext()

        if key in ['m', 'M']:

            self.timer.stop()
            self.trialsdone += 1
            self.person.updateoutput(self.trialsdone, 1)
            self.generatenext()

        if key in ['c', 'C']:

            self.timer.stop()
            self.trialsdone += 1
            self.person.updateoutput(self.trialsdone, 0)
            self.generatenext()
