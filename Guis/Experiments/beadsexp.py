from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QDialog, QGridLayout, QSlider
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QDir

from pathlib import Path

from Guis.Experiments import experiment


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

        # add slider variable
        self.output = 0

        # add slider to layout
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

        # add the Assets folder
        toassets = str(Path('../../..').resolve())
        QDir.addSearchPath('Assets', toassets)

        # go through the beadlist and make a list of pixmaps from each bead (or empty string) in the list
        for index, bead in enumerate(beadlist):
            pixmaplist.append(QLabel(''))
            pixmap = QPixmap(bead)
            pixmaplist[index].setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))

        # Make the 5x6 grid for the inventory
        for row in range(0, 4):

            for column in range(0, 5):
                layout.addWidget(pixmaplist[(column + (row * 5))], (0 + row), column)

        self.setLayout(layout)


class BeadsExp(experiment.Experiment):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__(person)

        # create a variable that will be toggled to indicate whether the participant is choosing a jar or not
        self.choosing = 0

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
        self.invbutton.setFixedWidth(310)
        self.invbutton.setFixedHeight(40)
        self.invbutton.setFont(QFont('Helvetica', 25))

        # Draw bead button
        self.drawbutton = QPushButton('Draw a bead')
        self.drawbutton.clicked.connect(self.drawbead)
        self.drawbutton.setFixedWidth(310)
        self.drawbutton.setFixedHeight(40)
        self.drawbutton.setFont(QFont('Helvetica', 25))
        self.drawbutton.hide()

        # Choose jar button
        self.choosebutton = QPushButton('Choose a jar')
        self.choosebutton.clicked.connect(self.start_choosing)
        self.choosebutton.setFixedWidth(310)
        self.choosebutton.setFixedHeight(40)
        self.choosebutton.setFont(QFont('Helvetica', 25))
        self.choosebutton.hide()

        # Instructions, depending on controls
        if self.person.controlscheme != 'Mouse':
            instructions = 'Press ' + self.person.leftkey[0] + ' to choose a jar and ' + self.person.rightkey[0] \
                           + ' to draw a bead'

        else:
            instructions = 'Click the button to draw a bead or choose a jar.'

        self.instructions.setText(instructions)

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

        # If using mouse controls, then add buttons to a specific layout in the middle; otherwise, just put middle in
        # regular layout
        if self.person.controlscheme == 'Mouse':

            self.mousemiddle = QVBoxLayout()

            self.mousemiddle.addWidget(self.middle)
            self.mousemiddle.addWidget(self.drawbutton)
            self.mousemiddle.addWidget(self.choosebutton)

            mainhlayout.addLayout(self.mousemiddle)

        else:
            mainhlayout.addWidget(self.middle)

        mainhlayout.addStretch(1)
        mainhlayout.addWidget(self.right)
        mainhlayout.addStretch(1)

        # Only add the inventory button if using mouse controls
        if self.person.controlscheme == 'Mouse':

            self.quitmenulayout.addStretch(1)
            self.quitmenulayout.addWidget(self.invbutton)

        # Put everything in vertical layout
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addLayout(mainhlayout)
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addLayout(self.quitmenulayout)

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
        """
        Function that launches the confidence window (if requested), takes the output of that, and then sends all info
        to the participant class
        :param event: this is something for the clicking
        """

        if self.choosing == 1:

            if self.person.confidenceoption == 'Yes':

                # launch the confidence window
                window = BeadsConfidence()
                window.exec()

                # take the output from the confidence window
                conf = window.output

                # send all the trial info to the participant class
                self.person.updateoutput(self.roundsdone, self.beadsdrawn, 1, 'Red', conf)

            else:

                # send all the trial info to the participant class
                self.person.updateoutput(self.roundsdone, self.beadsdrawn, 1, 'Red', 9999)

            # set the window to the iti screen
            self.iti()

    def choserightjar(self, event):
        """
        Function that launches the confidence window (if requested), takes the output of that, and then sends all info
        to the participant class
        :param event: this is something for the clicking
        """

        if self.choosing == 1:

            if self.person.confidenceoption == 'Yes':

                # launch the confidence window
                window = BeadsConfidence()
                window.exec()

                # take the output from the confidence window
                conf = window.output

                # send all the trial info to the participant class
                self.person.updateoutput(self.roundsdone, self.beadsdrawn, 1, 'Blue', conf)

            else:

                # send all the trial info to the participant class
                self.person.updateoutput(self.roundsdone, self.beadsdrawn, 1, 'Blue', 9999)

            # set the window to the iti screen
            self.iti()

    def openinventory(self):
        """
        Open the inventory window
        """

        window = BeadsInventory(self.beadlist)
        window.exec()

    def iti(self):
        """
        blankes the left and right labels and puts a fixation cross in the middle
        """

        self.left.setPixmap(QPixmap())
        self.right.setPixmap(QPixmap())
        self.middle.setText('+')

        # hide the buttons if using mouse controls
        if self.person.controlscheme == 'Mouse':
            self.choosebutton.hide()
            self.drawbutton.hide()

        self.jittertimer.start(1000)

    def newround(self):
        """
        Generate a new round and put it on screen. if the last round completed, then output the data instead
        """

        # stop the timer and set the text based on the participant class
        self.jittertimer.stop()
        self.middle.setText(self.person.nextround(self.roundsdone))

        # if fewer than the requested rounds have been completed...
        if self.roundsdone < self.person.get_trials():

            # increase the round number
            self.roundsdone += 1

            # start the timer to start the next round
            self.starttimer.start(500)

        # otherwise, output to the user's directory
        else:
            self.person.output()
            self.menubutton.show()

    def startround(self):
        """
        At the start of the round, clear the middle text, put the jars up, blank out the beadlist, and reset beads
        drawn to 0
        """

        # stop the timer and clear the middle
        self.starttimer.stop()
        self.middle.setText('')

        # show the buttons if using mouse controls
        if self.person.controlscheme == 'Mouse':
            self.choosebutton.show()
            self.drawbutton.show()

        # put the jars into pixmaps
        leftpixmap = QPixmap('Assets/BeadsTask_RedJar.png')
        rightpixmap = QPixmap('Assets/BeadsTask_BlueJar.png')

        # set the left and right to the pixmaps
        self.left.setPixmap(leftpixmap.scaledToWidth(300, Qt.TransformationMode.SmoothTransformation))
        self.right.setPixmap(rightpixmap.scaledToWidth(300, Qt.TransformationMode.SmoothTransformation))

        # set beadsdrawn back to 0
        self.beadsdrawn = 0

        # clear out the beadslist
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
        """
        draw a bead and add it to the bead list
        """

        # get the new bead
        newbead = 'Assets/' + self.person.get_bead() + '.png'

        # add the bead to the list
        self.beadlist[self.beadsdrawn] = newbead

        # set the center label to the new bead pixmap
        pixmap = QPixmap(newbead)
        self.middle.setPixmap(pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio))

        # increase the total number of beads drawn
        self.beadsdrawn += 1

        # send that info to the participant class
        self.person.updateoutput(self.roundsdone, self.beadsdrawn)

    def start_choosing(self):
        """
        puts the instructions for choosing a jar on screen and then changes the class variable to indicate that the
        participant is choosing a jar
        """

        if self.person.controlscheme != 'Mouse':
            chooseprompt = 'Press ' + self.person.leftkey[0] + ' to choose the left jar\nPress ' + \
                           self.person.rightkey[0] + ' to choose the right jar'

        else:
            chooseprompt = 'Click on the jar\nyou want to choose'

        self.middle.setText(chooseprompt)
        self.choosing = 1

    def keyaction(self, key):
        """
        Reads the keys that are pressed and does the corresponding actions
        :param key: the key that was pressed
        """

        # If the user presses the left key, the center text tells the user to click on the jar the choose
        if (key in self.person.leftkey) & (self.betweenrounds == 0):

            if self.choosing == 0:

                self.start_choosing()

            else:

                if self.person.confidenceoption == 'Yes':

                    # launch the confidence window
                    window = BeadsConfidence()
                    window.exec()

                    # take the output from the confidence window
                    conf = window.output

                    # send all the trial info to the participant class
                    self.person.updateoutput(self.roundsdone, self.beadsdrawn, 1, 'Red', conf)

                else:

                    # send all the trial info to the participant class
                    self.person.updateoutput(self.roundsdone, self.beadsdrawn, 1, 'Red', 9999)

                # set the window to the iti screen
                self.iti()

        # if the user preses the right key...
        if (key in self.person.rightkey) & (self.betweenrounds == 0):

            if self.choosing == 0:

                # clear the middle label
                self.middle.setText('')

                # if there have been fewer than 20 beads drawn, draw a bead
                if self.beadsdrawn < 20:
                    self.drawbead()

                # if 20 or more have been drawn, tell the user that no more can be drawn
                else:
                    self.middle.setText('Max number of\nbeads drawn')

            else:

                if self.person.confidenceoption == 'Yes':

                    # launch the confidence window
                    window = BeadsConfidence()
                    window.exec()

                    # take the output from the confidence window
                    conf = window.output

                    # send all the trial info to the participant class
                    self.person.updateoutput(self.roundsdone, self.beadsdrawn, 1, 'Blue', conf)

                else:

                    # send all the trial info to the participant class
                    self.person.updateoutput(self.roundsdone, self.beadsdrawn, 1, 'Blue', 9999)

                # set the window to the iti screen
                self.iti()

        # if the user presses the g key, then set the window to the iti screen
        if (key in ['g', 'G']) & (self.betweenrounds == 1):
            self.iti()

        # if the user presses the i key, then...
        if key in ['i', 'I']:

            if self.betweenrounds == 1:

                # increase the instruction index
                self.inst += 1

                # set the middle text to the corresponding instruction
                self.middle.setText(self.person.get_instructions(self.inst))

                # if the index reaches 20, reset to 0 so the instructions can be read again if desired
                if self.inst == 20:
                    self.inst = 0

            else:

                self.openinventory()
