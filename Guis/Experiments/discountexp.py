from PyQt6.QtWidgets import QLabel, QHBoxLayout, QProgressBar
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QTimer, pyqtSignal

import random
import time

from Guis.Experiments import experiment


class DDiscountExp(experiment.Experiment):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__(person)

        # Instructions, depending on controls
        if self.person.controlscheme != 'Mouse':
            instructions = 'Press ' + self.person.leftkey[0] + ' for the left option and ' + self.person.rightkey[0] \
                           + ' for the right option'

        else:
            instructions = 'Click the mouse on the option you prefer.'

        self.instructions.setText(instructions)

        # Left and right options (and middle stuff) with font settingsguis
        self.left = QLabel('')
        self.left.setFont(QFont('Helvetica', 40))
        self.left.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.right = QLabel('')
        self.right.setFont(QFont('Helvetica', 40))
        self.right.setAlignment(Qt.AlignmentFlag.AlignCenter)

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
        self.instquitlayout.addLayout(self.quitmenulayout)

        # if you're using the mouse for controls, then make sure the middle QLabel is connected to a mouse press event
        if self.person.controlscheme == 'Mouse':

            # Attach QLabels to functions
            self.left.mousePressEvent = self.clickedleftresponse

            self.right.mousePressEvent = self.clickedrightresponse

    def generatenext(self):
        """
        Generate the info for the next trial and put it on screen. if the final trial was just completed, then the next
        round is started or the completion text is put on screen
        """

        # stop the timer
        self.ititimer.stop()

        # reset the borders in case there was one
        self.right.setStyleSheet('border: 0px;')
        self.left.setStyleSheet('border: 0px;')

        # if-then statement to determine whether the amount of trials completed is less than the number of trials the
        # user wants
        if self.trialsdone < self.person.get_trials():

            # get trial text
            self.strings = self.person.get_design_text()

            # set the left and right side using the trial text
            self.left.setText(self.strings[0])
            self.right.setText(self.strings[1])

            # set the middle to or
            self.middle.setText('OR')

            # log the trial onset time
            self.starttime = time.time() - self.overallstart

            # start the trial timer
            self.timer.start(5000)

            # enable participant responses
            self.responseenabled = 1

            # if fmri mode, then set the new trial timer now
            if self.person.fmri == 'Yes':
                self.ititimer.start(6000)

        # if the trials requested have been completed
        else:

            # blank out the sides
            self.left.setText('')
            self.right.setText('')

            # increase the number of rounds done and reset the number of trials done to 0
            self.roundsdone += 1
            self.trialsdone = 0

            # set the middle text to the appropriate text from the participant class
            self.middle.setText(self.person.nextround(self.roundsdone))

            # if all of the requested rounds have been completed
            if self.person.rounds == self.roundsdone:

                # output the trial data and thank the participant
                self.person.output()
                self.instructions.setText('Thank you!')
                self.menubutton.show()

                # if the user wanted one of the participant's choices to get randomly chosen, then put that on screen
                if self.person.outcomeopt == 'Yes':
                    outcome = random.choice(self.person.outcomelist)
                    self.middle.setText('Your outcome: ' + outcome)

            # if not, indicate that you are now between rounds
            else:

                self.betweenrounds = 1

    def iti(self, state=0):
        """
        this function blanks out the screen and either warns the participant to be faster or has a fixation cross in the
        middle, depending on the value of state. It then sets the next design text
        :param state: default 0; only changes to 1 if it called from the timeout function and the experiment is in fmri
        mode. The value only serves to indicate this state
        """

        # blank out the sides
        self.left.setText('')
        self.right.setText('')

        # if state is 1, that means the participant timed out and the experiment is in fmri mode, so change iti to the
        # warning
        if state == 1:

            self.middle.setText('Please try to be quicker')

        # if the experiment is not in fmri mode or the participant did not time out, then leave this as a cross
        else:

            self.middle.setText('+')

        # if you are not in fmri mode and you have at least completed one trial, then start the timer for the next round
        if (self.person.fmri == 'No') & (self.trialsdone > 0):

            self.ititimer.start(1000)

        # if this function is called before the first trial is set up, then set up a timer for the first trial
        if self.trialsdone == 0:

            self.ititimer.start(1000)

    def timeout(self):
        """
        if the timer runs out and the participant doesn't respond, then the timers stop, 9999 gets put in as the
        reaction time, and the trial is "completed" with an incorrect response
        """

        # stop the timer
        self.timer.stop()

        # blank out the sides
        self.left.setText('')
        self.right.setText('')

        # set the middle to a warning
        self.middle.setText('Please try to be quicker')

        # send the trial data to the participant class
        self.person.updateoutput(self.trialsdone, self.starttime, 9999)

        # if you're not in fmri mode, then warn and start the reset timer
        if self.person.fmri == 'No':

            self.middle.setText('Please try to be quicker')
            self.trialresettimer.start(1000)

        # if you are in fmri mode, then disable participant input, increment the trial counter, and go to the iti screen
        else:

            self.trialsdone += 1
            self.responseenabled = 0
            self.iti(1)

    def responsereset(self):
        """
        if you're not in fmri mode, then this function resets the trial so that the participant can complete it
        """

        # stop the reset timer
        self.trialresettimer.stop()

        # set the left and right using trial info
        self.left.setText(self.strings[0])
        self.right.setText(self.strings[1])

        # set the middle text to or
        self.middle.setText('OR')

        # log the trial onset time
        self.starttime = time.time() - self.overallstart

        # start the timer again
        self.timer.start(5000)

    def clickedleftresponse(self, event):
        """
        Function that records participant click on left option and sends info to the participant class
        :param event: this is something for the clicking
        """

        # only allow the following if responses are enabled
        if self.responseenabled == 1:

            # stop the timer and prevent users from sending more inputs
            self.timer.stop()
            self.responseenabled = 0

            # increment the trial counter
            self.trialsdone += 1

            # use time.time and the start time variable to compute rt
            endtime = time.time() - self.overallstart
            rt = endtime - self.starttime

            # put a border around the middle to indicate a user input was received
            self.left.setStyleSheet('border: 3px solid blue;')

            # send the trial data to the participant class
            self.person.updateoutput(self.trialsdone, self.starttime, rt, 0)

            self.iti()

    def clickedrightresponse(self, event):
        """
        Function that records participant click on right option and sends info to the participant class
        :param event: this is something for the clicking
        """

        # only allow the following if responses are enabled
        if self.responseenabled == 1:

            # stop the timer and prevent users from sending more inputs
            self.timer.stop()
            self.responseenabled = 0

            # increment the trial counter
            self.trialsdone += 1

            # use time.time and the start time variable to compute rt
            endtime = time.time() - self.overallstart
            rt = endtime - self.starttime

            # put a border around the middle to indicate a user input was received
            self.right.setStyleSheet('border: 3px solid blue;')

            # send the trial data to the participant class
            self.person.updateoutput(self.trialsdone, self.starttime, rt, 1)

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

            # if this is the first trial of the first round, set the global start time to make the onset time make more
            # sense
            if (self.trialsdone == 0) & (self.roundsdone == 0):

                self.overallstart = time.time()

            # set the window to the iti screen
            self.iti()

        # if the participant presses the left or right keys and is allowed to respond
        if ((key in self.person.rightkey) | (key in self.person.leftkey)) & (self.responseenabled == 1):

            # stop the timer and prevent users from sending more inputs
            self.timer.stop()
            self.responseenabled = 0

            # increment the trial counter
            self.trialsdone += 1

            # use time.time and the start time variable to compute rt
            endtime = time.time() - self.overallstart
            rt = endtime - self.starttime

            # if the key was the right key...
            if key in self.person.rightkey:

                # put a border around the middle to indicate a user input was received
                self.right.setStyleSheet('border: 3px solid blue;')

                # set response to 1
                response = 1

            # if the key was the left key...
            else:

                # put a border around the middle to indicate a user input was received
                self.left.setStyleSheet('border: 3px solid blue;')

                # set response to 0
                response = 0

            # send the trial data to the participant class
            self.person.updateoutput(self.trialsdone, self.starttime, rt, response)

            self.iti()

        # if someone presses the i key and the participant is between rounds...
        if (key in ['i', 'I']) & (self.betweenrounds == 1):

            # increase the index for the instructions
            self.inst += 1

            # get the associated text
            self.middle.setText(self.person.get_instructions(self.inst))

            # if the index reaches five...
            if self.inst == 5:

                # reset to zero so the instructions can be viewed again
                self.inst = 0


class PDiscountExp(experiment.Experiment):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__(person)

        # Instructions, depending on controls
        if self.person.controlscheme != 'Mouse':
            instructions = 'Press ' + self.person.leftkey[0] + ' for the left option and ' + self.person.rightkey[0] \
                           + ' for the right option'

        else:
            instructions = 'Click the mouse on the option you prefer.'

        self.instructions.setText(instructions)

        # Left and right options (and middle stuff) with font settingsguis
        self.left = QLabel('')
        self.left.setFont(QFont('Helvetica', 40))
        self.left.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.right = QLabel('')
        self.right.setFont(QFont('Helvetica', 40))
        self.right.setAlignment(Qt.AlignmentFlag.AlignCenter)

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

        # Put everything in vertical layou
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addLayout(expverblayout)
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addLayout(expvislayout)
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addLayout(self.quitmenulayout)

        # if you're using the mouse for controls, then make sure the middle QLabel is connected to a mouse press event
        if self.person.controlscheme == 'Mouse':

            # Attach QLabels to functions
            self.left.mousePressEvent = self.clickedleftresponse

            self.right.mousePressEvent = self.clickedrightresponse

    def generatenext(self):
        """
        Generate the info for the next trial and put it on screen. if the final trial was just completed, then the next
        round is started or the completion text is put on screen
        """

        # stop the timer
        self.ititimer.stop()

        # reset the borders in case there was one
        self.right.setStyleSheet('border: 0px;')
        self.left.setStyleSheet('border: 0px;')

        # if-then statement to determine whether the amount of trials completed is less than the number of trials the
        # user wants
        if self.trialsdone < self.person.get_trials():

            # get trial text
            info = self.person.get_design_text()

            # set the left and right side using the trial info
            self.left.setText(info[0])
            self.leftbar.setValue(100)

            self.right.setText(info[1])
            self.rightbar.setValue(info[2])

            # set the middle to or
            self.middle.setText('OR')

            # log the trial onset time
            self.starttime = time.time() - self.overallstart

            # start the trial timer
            self.timer.start(5000)

            # enable participant responses
            self.responseenabled = 1

            # if fmri mode, then set the new trial timer now
            if self.person.fmri == 'Yes':
                self.ititimer.start(6000)

        # if the trials requested have been completed
        else:

            # blank out the sides
            self.left.setText('')
            self.right.setText('')

            # increase the number of rounds done and reset the number of trials done to 0
            self.roundsdone += 1
            self.trialsdone = 0

            # set the middle text to the appropriate text from the participant class
            self.middle.setText(self.person.nextround(self.roundsdone))

            # if all of the requested rounds have been completed
            if self.person.rounds == self.roundsdone:

                # output the trial data and thank the participant
                self.person.output()
                self.instructions.setText('Thank you!')
                self.menubutton.show()

                # if the user wanted one of the participant's choices to get randomly chosen, then put that on screen
                if self.person.outcomeopt == 'Yes':
                    outcome = random.choice(self.person.outcomelist)
                    self.middle.setText('Your outcome: ' + outcome)

            # if not, indicate that you are now between rounds
            else:

                self.betweenrounds = 1

    def iti(self, state=0):
        """
        this function blanks out the screen and either warns the participant to be faster or has a fixation cross in the
        middle, depending on the value of state. It then sets the next design text
        :param state: default 0; only changes to 1 if it called from the timeout function and the experiment is in fmri
        mode. The value only serves to indicate this state
        """

        # blank out the sides
        self.left.setText('')
        self.leftbar.setValue(0)
        self.right.setText('')
        self.rightbar.setValue(0)

        # if state is 1, that means the participant timed out and the experiment is in fmri mode, so change iti to the
        # warning
        if state == 1:

            self.middle.setText('Please try to be quicker')

        # if the experiment is not in fmri mode or the participant did not time out, then leave this as a cross
        else:

            self.middle.setText('+')

        # if you are not in fmri mode and you have at least completed one trial, then start the timer for the next round
        if (self.person.fmri == 'No') & (self.trialsdone > 0):

            self.ititimer.start(1000)

        # if this function is called before the first trial is set up, then set up a timer for the first trial
        if self.trialsdone == 0:

            self.ititimer.start(1000)

        # set the next design text
        self.person.set_design_text()

    def timeout(self):
        """
        if the timer runs out and the participant doesn't respond, then the timers stop, 9999 gets put in as the
        reaction time, and the trial is "completed" without a  response
        """

        # stop the timer
        self.timer.stop()

        # blank out the sides
        self.left.setText('')
        self.leftbar.setValue(0)
        self.right.setText('')
        self.rightbar.setValue(0)

        # set the middle to a warning
        self.middle.setText('Please try to be quicker')

        # send the trial data to the participant class
        self.person.updateoutput(self.trialsdone, self.starttime, 9999)

        # if you're not in fmri mode, then warn and start the reset timer
        if self.person.fmri == 'No':

            self.middle.setText('Please try to be quicker')
            self.trialresettimer.start(1000)

        # if you are in fmri mode, then disable participant input, increment the trial counter, and go to the iti screen
        else:

            self.trialsdone += 1
            self.responseenabled = 0
            self.iti(1)

    def clickedleftresponse(self, event):
        """
        Function that records participant click on left option and sends info to the participant class
        :param event: this is something for the clicking
        """

        # only allow the following if responses are enabled
        if self.responseenabled == 1:

            # stop the timer and prevent users from sending more inputs
            self.timer.stop()
            self.responseenabled = 0

            # increment the trial counter
            self.trialsdone += 1

            # use time.time and the start time variable to compute rt
            endtime = time.time() - self.overallstart
            rt = endtime - self.starttime

            # put a border around the middle to indicate a user input was received
            self.left.setStyleSheet('border: 3px solid blue;')

            # send the trial data to the participant class
            self.person.updateoutput(self.trialsdone, self.starttime, rt, 0)

            self.iti()

    def clickedrightresponse(self, event):
        """
        Function that records participant click on right option and sends info to the participant class
        :param event: this is something for the clicking
        """

        # only allow the following if responses are enabled
        if self.responseenabled == 1:

            # stop the timer and prevent users from sending more inputs
            self.timer.stop()
            self.responseenabled = 0

            # increment the trial counter
            self.trialsdone += 1

            # use time.time and the start time variable to compute rt
            endtime = time.time() - self.overallstart
            rt = endtime - self.starttime

            # put a border around the middle to indicate a user input was received
            self.right.setStyleSheet('border: 3px solid blue;')

            # send the trial data to the participant class
            self.person.updateoutput(self.trialsdone, self.starttime, rt, 1)

            self.iti()

    def responsereset(self):
        """
        if you're not in fmri mode, then this function resets the trial so that the participant can complete it
        """

        # stop the reset timer
        self.trialresettimer.stop()

        # get the trial info
        info = self.person.get_design_text()

        # set the left and right using that info
        self.left.setText(info[0])
        self.leftbar.setValue(100)

        self.right.setText(info[1])
        self.rightbar.setValue(info[2])

        # set the middle text to or
        self.middle.setText('OR')

        # start the timer again
        self.timer.start(5000)

    def keyaction(self, key):
        """
        Reads the keys that are pressed and does the corresponding actions
        :param key: the key that was pressed
        """

        # if someone presses the g key and the participant is between rounds...
        if (key in ['g', 'G']) & (self.betweenrounds == 1):

            # indicate that the participant is no longer between rounds so g and i keys won't mess things up
            self.betweenrounds = 0

            # if this is the first trial of the first round, set the global start time to make the onset time make more
            # sense
            if (self.trialsdone == 0) & (self.roundsdone == 0):

                self.overallstart = time.time()

            # set the window to the iti screen
            self.iti()

        # if the participant presses the left or right keys and is allowed to respond
        if ((key in self.person.rightkey) | (key in self.person.leftkey)) & (self.responseenabled == 1):

            # stop the timer and prevent users from sending more inputs
            self.timer.stop()
            self.responseenabled = 0

            # increment the trial counter
            self.trialsdone += 1

            # use time.time and the start time variable to compute rt
            endtime = time.time() - self.overallstart
            rt = endtime - self.starttime

            # if the key was the right key...
            if key in self.person.rightkey:

                # put a border around the middle to indicate a user input was received
                self.right.setStyleSheet('border: 3px solid blue;')

                # set response to 1
                response = 1

            # if the key was the left key...
            else:

                # put a border around the middle to indicate a user input was received
                self.left.setStyleSheet('border: 3px solid blue;')

                # set response to 0
                response = 0

            # send the trial data to the participant class
            self.person.updateoutput(self.trialsdone, self.starttime, rt, response)

            self.iti()

        # if someone presses the i key and the participant is between rounds...
        if (key in ['i', 'I']) & (self.betweenrounds == 1):

            # increase the index for the instructions
            self.inst += 1

            # get the associated text
            self.middle.setText(self.person.get_instructions(self.inst))

            # if the index reaches five...
            if self.inst == 5:

                # reset to zero so the instructions can be viewed again
                self.inst = 0


class CEDiscountExp(experiment.Experiment):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__(person)

        # Instructions, depending on controls
        if self.person.controlscheme != 'Mouse':
            instructions = 'Press ' + self.person.leftkey[0] + ' for the left option and ' + self.person.rightkey[0] \
                           + ' for the right option'

        else:
            instructions = 'Click the mouse on the option you prefer.'

        self.instructions.setText(instructions)

        # Left and right options (and middle stuff) with font settingsguis
        self.left = QLabel('')
        self.left.setFont(QFont('Helvetica', 40))
        self.left.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.right = QLabel('')
        self.right.setFont(QFont('Helvetica', 40))
        self.right.setAlignment(Qt.AlignmentFlag.AlignCenter)

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
        self.instquitlayout.addLayout(self.quitmenulayout)

        if self.person.fmri == 'Yes':
            self.extradelay = [0]

        else:
            self.extradelay = [0, 1000, 2000, 3000]

        # Make timer for second half of trial to appear on screen
        self.secondhalftimer = QTimer()
        self.secondhalftimer.timeout.connect(self.displaysecondhalf)

        # if you're using the mouse for controls, then make sure the middle QLabel is connected to a mouse press event
        if self.person.controlscheme == 'Mouse':

            # Attach QLabels to functions
            self.left.mousePressEvent = self.clickedleftresponse

            self.right.mousePressEvent = self.clickedrightresponse

    def generatenext(self):
        """
        Generate the info for the next trial and put it on screen. if the final trial was just completed, then the next
        round is started or the completion text is put on screen
        """

        # stop the timer
        self.ititimer.stop()

        # reset the borders in case there was one
        self.right.setStyleSheet('border: 0px;')
        self.left.setStyleSheet('border: 0px;')

        # if-then statement to determine whether the amount of trials completed is less than the number of trials the
        # user wants
        if self.trialsdone < self.person.get_trials():

            # set design text
            self.person.set_design_text()

            # get trial text
            self.strings = self.person.get_design_text()

            # pick a random either 1 or 2 to see which side appears first
            self.sideint = random.randint(1, 2)

            # if it's a one, left appears first
            if self.sideint == 1:
                self.left.setText(self.strings[0])
                self.right.setText('')

            # if it's a two, right appears first
            else:
                self.right.setText(self.strings[1])
                self.left.setText('')

            # set the middle to blank
            self.middle.setText('')

            # log the trial onset time
            self.starttime = time.time() - self.overallstart

            # get extra delay to add to the 1 second between seeing the first half and seeing the second
            extra = random.choice(self.extradelay)
            self.secondhalftimer.start(1000 + extra)

        # if the trials requested have been completed
        else:

            # blank out the sides
            self.left.setText('')
            self.right.setText('')

            # increase the number of rounds done and reset the number of trials done to 0
            self.roundsdone += 1
            self.trialsdone = 0

            # set the middle text to the appropriate text from the participant class
            self.middle.setText(self.person.nextround(self.roundsdone))

            # if all of the requested rounds have been completed
            if self.person.rounds == self.roundsdone:

                # output the trial data and thank the participant
                self.person.output()
                self.instructions.setText('Thank you!')
                self.menubutton.show()

                # if the user wanted one of the participant's choices to get randomly chosen, then put that on screen
                if self.person.outcomeopt == 'Yes':
                    outcome = random.choice(self.person.outcomelist)
                    self.middle.setText('Your outcome: ' + outcome)

            # if not, indicate that you are now between rounds
            else:

                self.betweenrounds = 1

    def iti(self, state=0):
        """
        this function blanks out the screen and either warns the participant to be faster or has a fixation cross in the
        middle, depending on the value of state. It then sets the next design text
        :param state: default 0; only changes to 1 if it called from the timeout function and the experiment is in fmri
        mode. The value only serves to indicate this state
        """

        # blank out the sides
        self.left.setText('')
        self.right.setText('')

        # if state is 1, that means the participant timed out and the experiment is in fmri mode, so change iti to the
        # warning
        if state == 1:

            self.middle.setText('Please try to be quicker')

        # if the experiment is not in fmri mode or the participant did not time out, then leave this as a cross
        else:

            self.middle.setText('+')

        # if you are not in fmri mode and you have at least completed one trial, then start the timer for the next round
        if (self.person.fmri == 'No') & (self.trialsdone > 0):

            self.ititimer.start(1000)

        # if this function is called before the first trial is set up, then set up a timer for the first trial
        if self.trialsdone == 0:

            self.ititimer.start(1000)

    def displaysecondhalf(self):
        """
        This function is called to display the second half of the trial
        """

        # stop the timer
        self.secondhalftimer.stop()

        # if left appeared first, display right
        if self.sideint == 1:
            self.right.setText(self.strings[1])

        # if right appeared first, display left
        else:
            self.left.setText(self.strings[0])

        # set the middle to or
        self.middle.setText('OR')

        # get the onset of the trial
        self.full = time.time() - self.overallstart

        # enable participant responses
        self.responseenabled = 1

        # start the trial timer
        self.timer.start(5000)

        # if you're in fmri mode, then start the timer to the next trial
        if self.person.fmri == 'Yes':
            self.ititimer.start(5500)

    def timeout(self):
        """
        if the timer runs out and the participant doesn't respond, then the timers stop, 9999 gets put in as the
        reaction time, and the trial is "completed" without a  response
        """

        # stop the timer
        self.timer.stop()

        # blank out the sides
        self.left.setText('')
        self.right.setText('')

        # set the middle to a warning
        self.middle.setText('Please try to be quicker')

        # send the trial data to the participant class
        self.person.updateoutput(self.trialsdone, self.starttime, self.full, 9999)

        # if you're not in fmri mode, then warn and start the reset timer
        if self.person.fmri == 'No':

            self.middle.setText('Please try to be quicker')
            self.trialresettimer.start(1000)

        # if you are in fmri mode, then disable participant input, increment the trial counter, and go to the iti screen
        else:

            self.trialsdone += 1
            self.responseenabled = 0
            self.iti(1)

    def responsereset(self):
        """
        if you're not in fmri mode, then this function resets the trial so that the participant can complete it
        """

        # stop the reset timer
        self.trialresettimer.stop()

        # set the left and right using that text
        self.left.setText(self.strings[0])
        self.right.setText(self.strings[1])

        # set the middle text to or
        self.middle.setText('OR')

        # start the timer again
        self.timer.start(5000)

    def clickedleftresponse(self, event):
        """
        Function that records participant click on left option and sends info to the participant class
        :param event: this is something for the clicking
        """

        # only allow the following if responses are enabled
        if self.responseenabled == 1:

            # stop the timer and prevent users from sending more inputs
            self.timer.stop()
            self.responseenabled = 0

            # increment the trial counter
            self.trialsdone += 1

            # use time.time and the start time variable to compute rt
            endtime = time.time() - self.overallstart
            rt = endtime - self.full

            # put a border around the middle to indicate a user input was received
            self.left.setStyleSheet('border: 3px solid blue;')

            # send the trial data to the participant class
            self.person.updateoutput(self.trialsdone, self.starttime, self.full, rt, 0)

            self.iti()

    def clickedrightresponse(self, event):
        """
        Function that records participant click on right option and sends info to the participant class
        :param event: this is something for the clicking
        """

        # only allow the following if responses are enabled
        if self.responseenabled == 1:

            # stop the timer and prevent users from sending more inputs
            self.timer.stop()
            self.responseenabled = 0

            # increment the trial counter
            self.trialsdone += 1

            # use time.time and the start time variable to compute rt
            endtime = time.time() - self.overallstart
            rt = endtime - self.full

            # put a border around the middle to indicate a user input was received
            self.right.setStyleSheet('border: 3px solid blue;')

            # send the trial data to the participant class
            self.person.updateoutput(self.trialsdone, self.starttime, self.full, rt, 1)

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

            # if this is the first trial of the first round, set the global start time to make the onset time make more
            # sense
            if (self.trialsdone == 0) & (self.roundsdone == 0):

                self.overallstart = time.time()

            # set the window to the iti screen
            self.iti()

        # if the participant presses the left or right keys and is allowed to respond
        if ((key in self.person.rightkey) | (key in self.person.leftkey)) & (self.responseenabled == 1):

            # stop the timer and prevent users from sending more inputs
            self.timer.stop()
            self.responseenabled = 0

            # increment the trial counter
            self.trialsdone += 1

            # use time.time and the start time variable to compute rt
            endtime = time.time() - self.overallstart
            rt = endtime - self.full

            # if the key was the right key...
            if key in self.person.rightkey:

                # put a border around the middle to indicate a user input was received
                self.right.setStyleSheet('border: 3px solid blue;')

                # set response to 1
                response = 1

            # if the key was the left key...
            else:

                # put a border around the middle to indicate a user input was received
                self.left.setStyleSheet('border: 3px solid blue;')

                # set response to 0
                response = 0

            # send the trial data to the participant class
            self.person.updateoutput(self.trialsdone, self.starttime, self.full, rt, response)

            self.iti()

        # if someone presses the i key and the participant is between rounds...
        if (key in ['i', 'I']) & (self.betweenrounds == 1):

            # increase the index for the instructions
            self.inst += 1

            # get the associated text
            self.middle.setText(self.person.get_instructions(self.inst))

            # if the index reaches six...
            if self.inst == 6:

                # reset to zero so the instructions can be viewed again
                self.inst = 0
