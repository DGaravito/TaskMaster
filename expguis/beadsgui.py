from pathlib import Path

from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QDialog, QGridLayout, QSlider
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QDir

from expguis import gui


class BeadsConfidence(QDialog):
    """
    This is a popup window that allows for user input to indicate confidence in their jar choice for the bead task.
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Confidence Rating')

        # Make  layout
        layout = QVBoxLayout()

        # add instructions

        instructions = QLabel('How confident were you in your choice?')
        instructions.setFont(QFont('Helvetica', 25))
        layout.addWidget(instructions)

        # add slider

        self.output = 0

        sliderlayout = QGridLayout()

        slider = QSlider()
        slider.setMinimum(1)
        slider.setMaximum(10)
        slider.setTickInterval(1)
        slider.setSingleStep(1)
        slider.setTickPosition(QSlider.TickPosition.TicksBothSides)
        slider.setValue(1)
        slider.setOrientation(Qt.Orientation.Horizontal)
        slider.setContentsMargins(10, 10, 10, 10)

        # Add slider labels

        lowlabel = QLabel('Not Confident')
        lowlabel.setFont(QFont('Helvetica', 15))
        lowlabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        highlabel = QLabel('Very Confident')
        highlabel.setFont(QFont('Helvetica', 15))
        highlabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Arrange slider and labels

        sliderlayout.addWidget(slider, 0, 0, 1, 10)
        sliderlayout.addWidget(lowlabel, 1, 0, 1, 1)
        sliderlayout.addWidget(highlabel, 1, 9, 1, 1)

        layout.addLayout(sliderlayout)

        slider.valueChanged.connect(lambda: self.changeoutput(slider.value()))

        # Add button

        button = QPushButton('OK')
        layout.addWidget(button)

        # Add signals
        button.clicked.connect(self.accept)

        self.setLayout(layout)

    def changeoutput(self, number):
        self.output = number


class BeadsInventory(QDialog):
    """
        This is a popup window that contains the participants's 'inventory' in the beads task. It has a grid layout of
        all of the beads they have draw in that round.
        """

    def __init__(self, beadlist):
        super().__init__()

        self.setWindowTitle('Beads you have drawn')

        # Make  layout
        layout = QGridLayout()

        pixmaplist = []

        # add the assets folder

        toassets = str(Path('..').resolve())
        QDir.addSearchPath('assets', toassets)

        for index, bead in enumerate(beadlist):
            pixmaplist.append(QLabel(''))
            pixmap = QPixmap(bead)
            pixmaplist[index].setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))

        # Make the grid for the inventory

        for row in range(0, 4):

            for column in range(0, 5):
                layout.addWidget(pixmaplist[(column + (row * 5))], (0 + row), column)

        self.setLayout(layout)


class BeadsExp(gui.Experiment):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__(person)

        # create variables to represent the number of beads drawn and the (currently empty) list of beads drawn
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

        # Inventory button
        self.invbutton = QPushButton('Beads you\'ve drawn')
        self.invbutton.clicked.connect(self.openinventory)

        # Instructions
        self.instructions.setText('Press \"M\" to draw a bead and \"C\" to choose a jar')

        # Left and right options (and middle stuff) with font settingsguis
        self.left = QLabel('')
        self.left.setFont(QFont('Helvetica', 40))

        self.right = QLabel('')
        self.right.setFont(QFont('Helvetica', 40))

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
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addLayout(mainhlayout)
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addLayout(quitinvlayout)

        # Make timer for jitter screen
        self.jittertimer = QTimer()
        self.jittertimer.timeout.connect(self.newround)

        # Make timer for jitter screen
        self.starttimer = QTimer()
        self.starttimer.timeout.connect(self.startround)

        # Attach left and right to functions
        self.left.mousePressEvent = self.choseleftjar
        self.right.mousePressEvent = self.choserightjar

    def choseleftjar(self, event):

        window = BeadsConfidence()
        window.exec()

        conf = window.output

        self.person.updateoutput(self.roundsdone, self.beadsdrawn, 1, 'Red', conf)
        self.jitter()

    def choserightjar(self, event):

        window = BeadsConfidence()
        window.exec()

        conf = window.output

        self.person.updateoutput(self.roundsdone, self.beadsdrawn, 1, 'Blue', conf)
        self.jitter()

    def openinventory(self):

        window = BeadsInventory(self.beadlist)
        window.exec()

    def jitter(self):

        self.left.setPixmap(QPixmap())
        self.right.setPixmap(QPixmap())
        self.middle.setText('+')

        self.jittertimer.start(1000)

    def newround(self):

        self.jittertimer.stop()
        self.middle.setText(self.person.nextround(self.roundsdone))

        if self.roundsdone < self.person.get_trials():
            self.roundsdone += 1
            self.starttimer.start(500)

        else:
            self.person.output()

    def startround(self):

        self.starttimer.stop()
        self.middle.setText('')

        leftpixmap = QPixmap('assets/BeadsTask_RedJar.png')
        rightpixmap = QPixmap('assets/BeadsTask_BlueJar.png')

        self.left.setPixmap(leftpixmap.scaledToWidth(300, Qt.TransformationMode.SmoothTransformation))
        self.right.setPixmap(rightpixmap.scaledToWidth(300, Qt.TransformationMode.SmoothTransformation))

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

        newbead = 'assets/' + self.person.get_bead() + '.png'

        self.beadlist[self.beadsdrawn] = newbead

        pixmap = QPixmap(newbead)

        self.middle.setPixmap(pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio))

        self.beadsdrawn += 1

        self.person.updateoutput(self.roundsdone, self.beadsdrawn)

    def keyaction(self, key):

        if key in self.person.leftkey:
            self.middle.setText('Click on the jar\nyou want to choose')

        if key in self.person.rightkey:

            self.middle.setText('')

            if self.beadsdrawn < 20:
                self.drawbead()

            else:
                self.middle.setText('Max number of\nbeads drawn')

        if key in ['g', 'G']:
            self.jitter()
            self.middle.setFont(QFont('Helvetica', 20))

        if key in ['i', 'I']:
            self.inst += 1
            self.middle.setText(self.person.get_instructions(self.inst))

            if self.inst == 20:
                self.inst = 0
