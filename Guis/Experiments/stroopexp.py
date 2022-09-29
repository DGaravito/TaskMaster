from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtCore import QTimer, pyqtSignal

import random

from Guis.Experiments import experiment


class StroopExp(experiment.Experiment):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__(person)

        # Put Left and Right options in horizontal layout
        explayout = QHBoxLayout()

        explayout.addStretch(1)
        explayout.addWidget(self.middle)
        explayout.addStretch(1)

        # Put everything in vertical layout
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addLayout(explayout)
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addWidget(self.quitbutton)

        # Make timer for new trial screen
        self.newblocktimer = QTimer()
        self.newblocktimer.timeout.connect(self.generateblock)

    def generatenext(self):

        # stop the timer to generate a new trial
        self.ititimer.stop()

        # if-then statement to determine whether the amount of trials completed is less than the number of trials the
        # user wants
        if self.trialsdone < self.person.get_trials():

            trialword = self.person.get_design_text()

            # find out if it's a study or test trial, and set the strings to the appropriate text
            if self.blocktype == 'Consistent':

                match trialword:

                    case 'red':

                        self.middle.setStyleSheet('color: red')

                    case 'green':

                        self.middle.setStyleSheet('color: green')

                    case 'yellow':

                        self.middle.setStyleSheet('color: yellow')

                    case 'blue':

                        self.middle.setStyleSheet('color: blue')

                    case 'black':

                        self.middle.setStyleSheet('color: black')

                    case 'orange':

                        self.middle.setStyleSheet('color: orange')

                    case _:

                        self.middle.setStyleSheet('color: purple')

            else:

                stylestring = 'color: '

                match trialword:

                    case 'red':

                        colorstring = random.choice(['green', 'yellow', 'blue', 'black', 'orange', 'purple'])

                    case 'green':

                        colorstring = random.choice(['red', 'yellow', 'blue', 'black', 'orange', 'purple'])

                    case 'yellow':

                        colorstring = random.choice(['red', 'green', 'blue', 'black', 'orange', 'purple'])

                    case 'blue':

                        colorstring = random.choice(['red', 'green', 'yellow', 'black', 'orange', 'purple'])

                    case 'black':

                        colorstring = random.choice(['red', 'green', 'yellow', 'blue', 'orange', 'purple'])

                    case 'orange':

                        colorstring = random.choice(['red', 'green', 'yellow', 'blue', 'black', 'purple'])

                    case _:

                        colorstring = random.choice(['red', 'green', 'yellow', 'blue', 'black', 'orange'])

                self.middle.setStyleSheet(stylestring + colorstring)

            # set the text to the screen
            self.middle.setText(trialword)

            # increment the trial counter
            self.trialsdone += 1

            # set the timer
            self.ititimer.start(5000)

        else:

            # if there are no more blocks to do, then thank the participant and end the task!
            if len(self.person.blocklist) == 0:

                # output info
                self.person.output()

                self.instructions.setText('Thank you!')
                self.middle.setText('You have finished this part of the study.')

            # if there are still blocks to do, then clear the text and start the trial to start the next round
            else:

                self.instructions.setText('')
                self.middle.setText('You have finished this round.')

                # start the timer to move to the next round
                self.newblocktimer.start(3000)

    def generateblock(self):
        """
        At the end of a block, this is called if there are more blocks to go. It resets the trial counter and gets the
        new block info
        :return:
        """

        # stop the timer
        self.newblocktimer.stop()

        # reset the trial count to 0
        self.trialsdone = 0

        # call the function that sets the word list for the next round and gets the block type
        self.blocktype = self.person.starttrial()

        # stop user input
        self.betweenrounds = 1

    def keyaction(self, key):
        """
        Reads the keys that are pressed and does the corresponding actions
        :param key: the key that was pressed
        """

        # if someone presses the g key and the participant is between rounds...
        if (key in ['g', 'G']) & (self.betweenrounds == 1):

            # stop the iti screen and start the timer
            self.iti()
            self.ititimer.start(1000)

            # indicate that the participant is no longer between rounds so g and i keys won't mess things up
            self.betweenrounds = 0

            # set instructions to a blank string
            self.instructions.setText('')

        if (key in ['i', 'I']) & (self.betweenrounds == 1):

            # increase the index for the instructions
            self.inst += 1

            # get the associated text
            self.middle.setText(self.person.get_instructions(self.inst))

            # if the index reaches seven...
            if self.inst == 7:

                # reset to zero so the instructions can be viewed again
                self.inst = 0
