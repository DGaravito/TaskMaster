import time

from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer, pyqtSignal

from Guis.Experiments import experiment


class PBTExp(experiment.Experiment):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__(person)

        # Instructions
        self.instructions.setText('Press ' + self.person.leftkey[0] + ' for crosses. Press ' +
                                  self.person.rightkey[0] + ' for squares.')

        # Make middle for pictures and text
        middlelayout = QHBoxLayout()

        middlelayout.addStretch(1)
        middlelayout.addWidget(self.middle)
        middlelayout.addStretch(1)

        # Put everything in vertical layout
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addLayout(middlelayout)
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addWidget(self.quitbutton)

        # Make a timer that controls how long an image is left on the screen
        self.blankouttimer = QTimer()
        self.blankouttimer.timeout.connect(self.blankout)

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

            # Get the string that contains the name of the trial picture
            self.picstring = self.person.get_trial_pic()
            pathstring = 'Assets/' + self.picstring

            # Make a pixmap of the picture and then set the middle to that pixmap
            pixmap = QPixmap(pathstring)
            self.middle.setPixmap(pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio))

            # get the onset time for the trial, which will also be used to compute reaction time
            self.starttime = time.time() - self.overallstart

            # Start the timers for until timeout, the time until the next trial begins, and how long the picture is seen
            self.timer.start(5000)
            self.ititimer.start(5500)
            self.blankouttimer.start(250)

            # Set the variable that allows the user to respond
            self.responseenabled = 1

        # if the trials requested have been completed...
        else:

            # indicate that another block (aka round) is complete and reset the number of trials done to 0 for the next
            # block
            self.roundsdone += 1
            self.trialsdone = 0

            # set the text for the middle label to the appropriate text depending on how many blocks the user wanted
            self.middle.setText(self.person.nextround(self.roundsdone))

            # if the number of rounds done is equal to the number the user requested...
            if self.person.rounds == self.roundsdone:

                # output the data to the user's directory and change the instructions to a thank you message
                self.person.output()
                self.instructions.setText('Thank you!')

            # If there are still some blocks to go...
            else:

                # allow the user to start the next round
                self.betweenrounds = 1

    def blankout(self):
        """
        This function only serves to remove the picture after the blankout time expires
        """

        self.blankouttimer.stop()
        self.middle.setPixmap(QPixmap())

    def timeout(self):
        """
        if the timer runs out and the participant doesn't respond, then the
        """

        # stop the timer
        self.timer.stop()

        # turn off the ability for the participant to respond
        self.responseenabled = 0

        # indicate that a trial has been completed
        self.trialsdone += 1

        # send the trial info to the participant class
        self.person.updateoutput(self.trialsdone, self.picstring, self.starttime, 9999, 'None')

        # set the screen to the iti window
        self.iti()

    def keyaction(self, key):
        """
        Reads the keys that are pressed and does the corresponding actions
        :param key: the key that was pressed
        """

        # if someone presses the g key and the participant is between rounds...
        if (key in ['g', 'G']) & (self.betweenrounds == 1):

            # remove all text from the middle label
            self.middle.setText('')

            # reset the instructions to 1 in case they user wants to read instructions again next round
            self.inst = 1

            # set the screen to the iti and then start the timer until the first trial starts
            self.iti()
            self.ititimer.start(1000)

            # indicate that the participant is no longer between rounds so g and i keys won't mess things up
            self.betweenrounds = 0

            # if this is the first trial of the first round, set the global start time to make the onset time make more
            # sense
            if (self.trialsdone == 0) & (self.roundsdone == 0):
                self.overallstart = time.time()

        # if the participant presses the right or left key and is allowed to respond...
        if ((key in self.person.rightkey) | (key in self.person.leftkey)) & (self.responseenabled == 1):

            # put a border around the middle to indicate a user input was received
            self.middle.setStyleSheet('border: 3px solid blue;')

            # no longer allow the participant to respond
            self.responseenabled = 0

            # stop the timeout timer and indicate that the participant completed the trial
            self.timer.stop()
            self.trialsdone += 1

            # use time.time and the start time variable to compute rt
            endtime = time.time() - self.overallstart
            rt = endtime - self.starttime

            # if the key was the right key...
            if key in self.person.rightkey:

                # set response to square
                response = 'Square'

            # if the key was the left key...
            else:

                # set response to cross
                response = 'Cross'

            # send the trial info to the participant class so it can be added to the dataframe
            self.person.updateoutput(self.trialsdone, self.picstring, self.starttime, rt, response)

            # set the window to the iti screen
            self.iti()

        # if someone presses the i key and the participant is between rounds...
        if (key in ['i', 'I']) & (self.betweenrounds == 1):

            # increase the index for the instructions
            self.inst += 1

            # if this is the sixth instruction...
            if self.inst == 6:
                pixmap = QPixmap('Assets/PBT_DSC.png')
                self.middle.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))

            # if this is the ninth instruction...
            elif self.inst == 9:
                pixmap = QPixmap('Assets/PBT_DCS.png')
                self.middle.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))

            # if this is an instruction other than sixth or ninth...
            else:
                # set the middle text to the appropriate text instruction, depending on the type of block and the index
                self.middle.setText(self.person.get_instructions(self.person.globallocal, self.inst))

            # if the index reaches eleven...
            if self.inst == 11:

                # reset to zero to allow the user to start the instructions over
                self.inst = 0
