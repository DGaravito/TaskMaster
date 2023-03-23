from PyQt6.QtWidgets import QHBoxLayout, QGridLayout, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal

import time

from Guis.Experiments import experiment


class DwellExp(experiment.Experiment):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__(person)

        # Variable that determines what you see at the start
        self.start = 0

        # Make middle layout for pictures and text
        middlelayout = QHBoxLayout()

        # make the grid for the matrix
        self.matrix = QGridLayout()

        middlelayout.addStretch(1)
        middlelayout.addLayout(self.matrix)
        middlelayout.addWidget(self.middle)
        middlelayout.addStretch(1)

        # Instructions
        self.instructions.setText('Press \"G\" to start the task or \"I\" for instructions.')

        # Put everything in vertical layout
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addLayout(middlelayout)
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addWidget(self.quitbutton)

    def generatenext(self):
        """
        Generate the info for the next trial and put it on screen. if the final trial was just completed, then the next
        round is started or the completion text is put on screen
        """

        # stop the timer
        self.ititimer.stop()

        # if-then statement to determine whether the amount of trials completed is less than the number of trials the
        # user wants
        if self.trialsdone < self.person.get_trials():

            # Get the string that contains the name of the trial picture
            self.matrixpics = self.person.get_matrix()

            for row in range(4):

                for column in range(4):

                    pixmap = QPixmap(self.matrixpics.pop())
                    label = QLabel().setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))

                    # add to the layout
                    self.matrix.addWidget(label, row, column)

            # get the onset time for the trial, which will also be used to compute reaction time
            self.starttime = time.time() - self.overallstart

            # Start the timers for until timeout and the time until the next trial begins
            self.timer.start(500)
            self.ititimer.start(1500)

        # if the trials requested have been completed...
        else:

            # indicate that another block (aka round) is complete and reset the number of trials done to 0 for the next
            # block
            self.trialsdone = 0

            # set the text for the middle label to the appropriate text depending on how many blocks the user wanted
            self.instructions.setText(self.person.nextround())

            # if the number of blocks done is not equal to the number the user requested and there are no more matrix
            # types left in the block
            if (self.person.blocksdone != self.person.blocks) & (len(self.person.blockorder) > 0):

                # allow the user to start the next round
                self.betweenrounds = 1

    def timeout(self):
        """
        when the timer runs out, submit the info for that trial
        """

        # stop the timers
        self.timer.stop()

        # turn off the ability for the participant to respond
        self.responseenabled = 0

        # indicate that a trial has been completed
        self.trialsdone += 1

        # send the trial info to the participant class
        self.person.updateoutput(self.trialsdone, self.matrixpics, self.starttime)

        # set the screen to the iti window
        self.iti()

    def keyaction(self, key):
        """
        Reads the keys that are pressed and does the corresponding actions
        :param key: the key that was pressed
        """

        # if someone presses the g key and the participant is between rounds...
        if (key in ['g', 'G']) & (self.betweenrounds == 1):

            # Instructions
            self.instructions.setText('')

            # set the screen to the iti and then start the timer until the first trial starts
            self.iti()
            self.ititimer.start(1000)

            # indicate that the participant is no longer between rounds so g and i keys won't mess things up
            self.betweenrounds = 0

            # if this is the first trial of the first round, set the global start time to make the onset time make more
            # sense
            if (self.trialsdone == 0) & (self.roundsdone == 0):
                self.overallstart = time.time()

        # if someone presses the i key and the participant is between rounds...
        if (key in ['i', 'I']) & (self.betweenrounds == 1):

            # increase the index for the instructions
            self.inst += 1

            # set the middle text to the appropriate text instruction, depending on the type of block and the index
            self.middle.setText(self.person.get_instructions(self.inst))

            # if the index reaches twelve...
            if self.inst == 5:

                # reset to zero to allow the user to start the instructions over
                self.inst = 0
