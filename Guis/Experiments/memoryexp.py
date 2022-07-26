from PyQt6.QtWidgets import QLabel, QHBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QTimer, pyqtSignal

import time

from Guis.Experiments import experiment


class PrExp(experiment.Experiment):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__(person)

        # Left and right options (and middle stuff) with font settingsguis
        self.left = QLabel('')
        self.left.setFont(QFont('Helvetica', 40))
        self.instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.right = QLabel('')
        self.right.setFont(QFont('Helvetica', 40))
        self.instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)

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
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addLayout(explayout)
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addWidget(self.quitbutton)

        # Make timer for new trial screen
        self.newtrialtimer = QTimer()
        self.newtrialtimer.timeout.connect(self.generatetrial)

    def generatenext(self):

        # stop the timer to generate a new trial
        self.ititimer.stop()

        # if-then statement to determine whether the amount of trials completed is less than the number of trials the
        # user wants
        if self.trialsdone < self.person.get_trials():

            # find out if it's a study or test trial, and set the strings to the appropriate text
            if self.person.structure[0] == 'S':

                strings = self.person.get_design_text(0)

            else:

                strings = self.person.get_design_text(1)

            # set the text to the screen
            self.left.setText(strings[0])
            self.right.setText(strings[1])
            self.middle.setText('')

            # increment the trial counter
            self.trialsdone += 1

            # set the timer
            self.ititimer.start(5000)

        else:

            # remove the current block that was just completed from the block list
            del self.person.structure[0]

            # if there are no more blocks to do, then thank the participant and end the task!
            if len(self.person.structure) == 0:

                # output info
                self.person.output()

                self.left.setText('')
                self.right.setText('')
                self.instructions.setText('Thank you!')
                self.middle.setText('You have finished this part of the study.')

            # if there are still blocks to do, then clear the text and start the trial to start the next round
            else:

                self.left.setText('')
                self.right.setText('')
                self.instructions.setText('')
                self.middle.setText('You have finished this round.')

                # start the timer to move to the next round
                self.newtrialtimer.start(3000)

    def generatetrial(self):

        # stop the timer
        self.newtrialtimer.stop()

        # reset the trial count to 0
        self.trialsdone = 0

        # set the instructions to the appropriate text for the next round
        string = self.person.starttrial()
        self.instructions.setText(string)

        # stop user input
        self.betweenrounds = 1

    def keyaction(self, key):
        """
        Reads the keys that are pressed and does the corresponding actions
        :param key: the key that was pressed
        """

        # if someone presses the g key and the participant is between rounds...
        if (key in ['g', 'G']) & (self.betweenrounds == 1):

            # send to the iti screen and start the timer
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

            # if the index reaches sixteen...
            if self.inst == 16:

                # reset to zero so the instructions can be viewed again
                self.inst = 0


class NbExp(experiment.Experiment):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__(person)

        # Instructions
        self.instructions.setText('Press ' + self.person.leftkey[0] + ' if the letter is a false alarm. Press ' +
                                  self.person.rightkey[0] + ' if the letter is a target')

        # center middle
        self.middle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Put everything in vertical layout
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addWidget(self.middle)
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addWidget(self.quitbutton)

    def generatenext(self):
        """
        Generate the info for the next trial and put it on screen. if the final trial was just completed, then the next
        round is started or the completion text is put on screen
        """

        # stop the timer
        self.ititimer.stop()

        # reset the border around the middle if there was something different
        self.middle.setStyleSheet('border: 0px;')

        # if-then statement to determine whether the amount of trials completed is less than the number of trials the
        # user wants
        if self.trialsdone < self.person.get_trials():

            # get the next letter
            self.middle.setText(self.person.get_trial_text())

            # get the start time
            self.starttime = time.time() - self.overallstart

            # start trial timers and allow the user to respond
            self.timer.start(3000)
            self.ititimer.start(3500)
            self.responseenabled = 1

        # if the trials requested have been completed
        else:

            # increase the number of rounds done and reset the number of trials done to 0
            self.roundsdone += 1
            self.trialsdone = 0

            # get the approrpiate text depending on if all the rounds are done or more need to be run
            text = self.person.nextround(self.roundsdone)

            # set the instructions and middle to that appropriate text
            self.instructions.setText(text[0])
            self.middle.setText(text[1])

            # if the person did badly that round, make them do an additional
            if self.person.roundperformance < 70:

                self.roundsdone -= 1

            # if all the rounds are completed, then output the data
            if self.person.rounds == self.roundsdone:

                self.person.output()

            # if more rounds need to be done, then indicate that it is between rounds
            else:

                self.betweenrounds = 1

    def timeout(self):
        """
        if the timer runs out and the participant doesn't respond, then the timers stop, 9999 gets put in as the
        reaction time, and the trial is "completed" with an incorrect response
        """

        # stop the timer
        self.timer.stop()

        # turn off the ability for the participant to respond
        self.responseenabled = 0

        # indicate that a trial has been completed
        self.trialsdone += 1

        # send the trial info to the participant class
        self.person.updateoutput(self.trialsdone, self.starttime, 9999)

        # set the screen to the iti window
        self.iti()

    def keyaction(self, key):
        """
        Reads the keys that are pressed and does the corresponding actions
        :param key: the key that was pressed
        """

        # if someone presses the g key and the participant is between rounds...
        if (key in ['g', 'G']) & (self.betweenrounds == 1):

            # indicate that the participant is no longer between rounds so g and i keys won't mess things up
            self.betweenrounds = 0

            # generate the next trial
            self.generatenext()

            # set the instructions for the task
            self.instructions.setText('Press ' + self.person.leftkey[0] + ' if the letter is a false alarm. Press ' +
                                      self.person.rightkey[0] + ' if the letter is a target')

            # if this is the first trial of the first round, set the global start time to make the onset time make more
            # sense
            if (self.trialsdone == 0) & (self.roundsdone == 0):
                self.overallstart = time.time()

        # if the participant presses the left or right keys and is allowed to respond
        if ((key in self.person.rightkey) | (key in self.person.leftkey)) & (self.responseenabled == 1):

            # put a border around the middle to indicate a user input was received
            self.middle.setStyleSheet('border: 3px solid blue;')

            # no longer allow the participant to respond
            self.responseenabled = 0

            # stop the timer and increment the number of trials done
            self.timer.stop()
            self.trialsdone += 1

            # use time.time and the start time variable to compute rt
            endtime = time.time() - self.overallstart
            rt = endtime - self.starttime

            # if the key was the right key...
            if key in self.person.rightkey:

                # set response to 1
                response = 1

            # if the key was the left key...
            else:

                # set response to 0
                response = 0

            # send the trial info to the participant class so it can be added to the dataframe
            self.person.updateoutput(self.trialsdone, self.starttime, rt, response)

            # set the window to the iti screen
            self.iti()

        # if someone presses the i key and the participant is between rounds...
        if (key in ['i', 'I']) & (self.betweenrounds == 1):

            # increase the index for the instructions
            self.inst += 1

            # get the associated instruction text
            self.middle.setText(self.person.get_instructions(self.inst))

            # if the index reaches twelve...
            if self.inst == 12:

                # reset to zero so the instructions can be viewed again
                self.inst = 0
