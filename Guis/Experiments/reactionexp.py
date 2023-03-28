from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer, pyqtSignal

import random
import time
import glob
import os

from Guis.Experiments import experiment


class SSExp(experiment.Experiment):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__(person)

        # Make middle layout for pictures and text
        middlelayout = QHBoxLayout()

        middlelayout.addStretch(1)
        middlelayout.addWidget(self.middle)
        middlelayout.addStretch(1)

        # Instructions
        self.instructions.setText('Press ' + self.person.leftkey[0] + ' for left arrows. Press ' +
                                  self.person.rightkey[0] + ' for right arrows.')

        # Put everything in vertical layout
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addLayout(middlelayout)
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addWidget(self.quitbutton)

        # Make timer to indicate when a signal should be sent (in signal trials)
        self.signaltimer = QTimer()
        self.signaltimer.timeout.connect(self.sendsignal)

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

            # randomly select zero or one to determine whether the trial will be a signal or non-signal one
            signalrand = random.randint(0, 1)

            # if you get zero, then it's a non-signal trial
            if signalrand == 0:

                self.signal = 0

            # if you get one, then it's a signal trial, so grab the signal timer time and start the timer
            else:

                self.signal = 1
                self.signaltimer.start(self.person.get_timer())

            # get the onset time for the trial, which will also be used to compute reaction time
            self.starttime = time.time() - self.overallstart

            # Start the timers for until timeout and the time until the next trial begins
            self.timer.start(2500)
            self.ititimer.start(3000)

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

    def timeout(self):
        """
        if the timer runs out and the participant doesn't respond, then the timers stop, 9999 gets put in as the
        reaction time, and the trial is completed
        """

        # stop the timers
        self.timer.stop()
        self.signaltimer.stop()

        # turn off the ability for the participant to respond
        self.responseenabled = 0

        # indicate that a trial has been completed
        self.trialsdone += 1

        # send the trial info to the participant class
        self.person.updateoutput(self.trialsdone, self.picstring, self.starttime, 9999, self.signal)

        # set the screen to the iti window
        self.iti()

    def sendsignal(self):
        """
        If this is a signal trial, this function will be called to send the signal
        :return:
        """

        # stop the timer
        self.signaltimer.stop()

        # use the correct signal picture, depending on the arrow picture
        if self.picstring == 'SS_LeftArrow.png':
            pathstring = 'Assets/SS_LeftSignal.png'

        else:
            pathstring = 'Assets/SS_RightSignal.png'

        # set the picture to the pixmap
        pixmap = QPixmap(pathstring)

        # load the pixmap
        self.middle.setPixmap(pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio))

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

            # stop the timers and indicate that the participant completed the trial
            self.timer.stop()
            self.signaltimer.stop()
            self.trialsdone += 1

            # use time.time and the start time variable to compute rt
            endtime = time.time() - self.overallstart
            rt = endtime - self.starttime

            # if the key was the right key...
            if key in self.person.rightkey:

                # set response to one
                response = 1

            # if the key was the left key...
            else:

                # set response to zero
                response = 0

            # send the trial info to the participant class so it can be added to the dataframe
            self.person.updateoutput(self.trialsdone, self.picstring, self.starttime, rt, self.signal, response)

            # set the window to the iti screen
            self.iti()

        # if someone presses the i key and the participant is between rounds...
        if (key in ['i', 'I']) & (self.betweenrounds == 1):

            # increase the index for the instructions
            self.inst += 1

            # set the middle text to the appropriate text instruction, depending on the type of block and the index
            self.middle.setText(self.person.get_instructions(self.inst))

            # if the index reaches twelve...
            if self.inst == 12:

                # reset to zero to allow the user to start the instructions over
                self.inst = 0


class EGNGExp(experiment.Experiment):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__(person)

        # Variable that determines what you see at the start
        self.start = 0

        # Make middle layout for pictures and text
        middlelayout = QHBoxLayout()

        middlelayout.addStretch(1)
        middlelayout.addWidget(self.middle)
        middlelayout.addStretch(1)

        # Instructions
        self.instructions.setText('Press ' + self.person.leftkey[0] + ' to respond to faces.')

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

        # reset the border around the middle if there was something different
        self.middle.setStyleSheet('border: 0px;')

        # if-then statement to determine whether the amount of trials completed is less than the number of trials the
        # user wants
        if self.trialsdone < self.person.get_trials():

            # Get the string that contains the name of the trial picture
            self.pictype = self.person.get_trial_pic()

            match self.pictype:

                case 'Happy':

                    # get a list of all happy pictures
                    picturelist = glob.glob(self.person.picturedir + '/Happy_*.png')

                    # get a random pictures from the list
                    self.picstring = os.path.normpath(random.choice(picturelist))

                case 'Sad':

                    # get a list of all happy pictures
                    picturelist = glob.glob(self.person.picturedir + '/Sad_*.png')

                    # get a random pictures from the list
                    self.picstring = random.choice(picturelist)

                case 'Angry':

                    # get a list of all happy pictures
                    picturelist = glob.glob(self.person.picturedir + '/Angry_*.png')

                    # get a random pictures from the list
                    self.picstring = random.choice(picturelist)

                case 'Fearful':

                    # get a list of all happy pictures
                    picturelist = glob.glob(self.person.picturedir + '/Fearful_*.png')

                    # get a random pictures from the list
                    self.picstring = random.choice(picturelist)

                case _:

                    # get a list of all happy pictures
                    picturelist = glob.glob(self.person.picturedir + '/Neutral_*.png')

                    print(picturelist)

                    # get a random pictures from the list
                    self.picstring = os.path.normpath(random.choice(picturelist))

            # Make a pixmap of the picture and then set the middle to that pixmap
            pixmap = QPixmap(self.picstring)
            self.middle.setPixmap(pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio))

            # get the onset time for the trial, which will also be used to compute reaction time
            self.starttime = time.time() - self.overallstart

            # Start the timers for until timeout and the time until the next trial begins
            self.timer.start(500)

            randomiti = random.randint(1500, 4000)
            self.ititimer.start(randomiti)

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

            prompt = self.person.nextround()

            self.middle.setText(prompt[0])
            self.start = prompt[1]

            # if the number of rounds done is equal to the number the user requested...
            if self.person.rounds == self.roundsdone:

                # output the data to the user's directory and change the instructions to a thank you message
                self.person.output()
                self.instructions.setText('Thank you!')

            # If there are still some blocks to go...
            else:

                # allow the user to start the next round
                self.betweenrounds = 1

    def timeout(self):
        """
        if the timer runs out and the participant doesn't respond, then the timers stop, 9999 gets put in as the
        reaction time, and the trial is completed.
        """

        # stop the timers
        self.timer.stop()

        # turn off the ability for the participant to respond
        self.responseenabled = 0

        # indicate that a trial has been completed
        self.trialsdone += 1

        # send the trial info to the participant class
        self.person.updateoutput(self.trialsdone, self.picstring, self.starttime, 9999)

        # set the screen to the iti window
        self.iti()

    def keyaction(self, key):
        """
        Reads the keys that are pressed and does the corresponding actions
        :param key: the key that was pressed
        """

        # if someone presses the g key and the participant is between rounds...
        if (key in ['g', 'G']) & (self.betweenrounds == 1):

            # if the block info hasn't been displayed on screen yet...
            if self.start == 0:

                # get the block info
                text = self.person.nextround()

                # display the info on screen
                self.middle.setText(text[0])

                # indicate that the block info has been shown
                self.start += 1

            # otherwise...
            else:

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
        if (key in self.person.leftkey) & (self.responseenabled == 1):

            # put a border around the middle to indicate a user input was received
            self.middle.setStyleSheet('border: 3px solid blue;')

            # no longer allow the participant to respond
            self.responseenabled = 0

            # stop the timers and indicate that the participant completed the trial
            self.timer.stop()
            self.trialsdone += 1

            # use time.time and the start time variable to compute rt
            endtime = time.time() - self.overallstart
            rt = endtime - self.starttime

            # send the trial info to the participant class so it can be added to the dataframe
            self.person.updateoutput(self.trialsdone, self.picstring, self.starttime, rt, 1)

            # set the window to the iti screen
            self.iti()

        # if someone presses the i key and the participant is between rounds...
        if (key in ['i', 'I']) & (self.betweenrounds == 1):

            # increase the index for the instructions
            self.inst += 1

            # set the middle text to the appropriate text instruction, depending on the type of block and the index
            self.middle.setText(self.person.get_instructions(self.inst))

            # if the index reaches seven...
            if self.inst == 7:

                # reset to zero to allow the user to start the instructions over
                self.inst = 0


class GNGExp(experiment.Experiment):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__(person)

        # indicate that no blocks have been completed yet
        self.blocksdone = 0

        # Variable that determines what you see at the start
        self.start = 0

        # Make middle layout for pictures and text
        middlelayout = QHBoxLayout()

        middlelayout.addStretch(1)
        middlelayout.addWidget(self.middle)
        middlelayout.addStretch(1)

        # Instructions
        self.instructions.setText('Press ' + self.person.leftkey[0] + ' to respond to signals.')

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

        # reset the border around the middle if there was something different
        self.middle.setStyleSheet('border: 0px;')

        # if-then statement to determine whether the amount of trials completed is less than the number of trials the
        # user wants
        if self.trialsdone < self.person.get_trials():

            # Get the string of the signal
            self.signal = self.person.get_trial_string()

            # Set the middle to that signal
            self.middle.setText(self.signal)

            # get the onset time for the trial, which will also be used to compute reaction time
            self.starttime = time.time() - self.overallstart

            # Start the timers for until timeout and the time until the next trial begins
            self.timer.start(500)
            self.ititimer.start(1500)

            # Set the variable that allows the user to respond
            self.responseenabled = 1

        # if the trials requested have been completed...
        else:

            # indicate that another block (aka round) is complete and reset the number of trials done to 0 for the next
            # block
            self.roundsdone += 1
            self.trialsdone = 0

            # set the text for the middle label to the appropriate text depending on how many blocks the user wanted
            prompt = self.person.nextround()
            self.middle.setText(prompt[0])

            # set start to the number from the nextround function, which will prevent the code from jumping without
            # telling the subject what the next face type is
            self.start = prompt[1]

            # if the number of rounds done is equal to the number the user requested...
            if self.person.rounds == self.roundsdone:

                # output the data to the user's directory and change the instructions to a thank you message
                self.person.output()
                self.instructions.setText('Thank you!')

            # If there are still some blocks to go...
            else:

                # allow the user to start the next round
                self.betweenrounds = 1

    def timeout(self):
        """
        if the timer runs out and the participant doesn't respond, then the timer stops, trial completes, and some
        default info is submitted
        """

        # stop the timers
        self.timer.stop()

        # turn off the ability for the participant to respond
        self.responseenabled = 0

        # indicate that a trial has been completed
        self.trialsdone += 1

        # send the trial info to the participant class
        self.person.updateoutput(self.trialsdone, self.signal, self.starttime, 9999)

        # set the screen to the iti window
        self.iti()

    def keyaction(self, key):
        """
        Reads the keys that are pressed and does the corresponding actions
        :param key: the key that was pressed
        """

        # if someone presses the g key and the participant is between rounds...
        if (key in ['g', 'G']) & (self.betweenrounds == 1):

            # if the block info hasn't been displayed on screen yet...
            if self.start == 0:

                # get the block info
                text = self.person.nextround()

                # display the info on screen
                self.middle.setText(text[0])

                # indicate that the block info has been shown
                self.start += 1

            # otherwise...
            else:

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
        if (key in self.person.leftkey) & (self.responseenabled == 1):

            # put a border around the middle to indicate a user input was received
            self.middle.setStyleSheet('border: 3px solid blue;')

            # no longer allow the participant to respond
            self.responseenabled = 0

            # stop the timers and indicate that the participant completed the trial
            self.timer.stop()
            self.trialsdone += 1

            # use time.time and the start time variable to compute rt
            endtime = time.time() - self.overallstart
            rt = endtime - self.starttime

            # send the trial info to the participant class so it can be added to the dataframe
            self.person.updateoutput(self.trialsdone, self.signal, self.starttime, rt, 1)

            # set the window to the iti screen
            self.iti()

        # if someone presses the i key and the participant is between rounds...
        if (key in ['i', 'I']) & (self.betweenrounds == 1):

            # increase the index for the instructions
            self.inst += 1

            # set the middle text to the appropriate text instruction, depending on the type of block and the index
            self.middle.setText(self.person.get_instructions(self.inst))

            # if the index reaches twelve...
            if self.inst == 12:

                # reset to zero to allow the user to start the instructions over
                self.inst = 0
