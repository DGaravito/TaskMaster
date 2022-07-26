import time
import random

from PyQt6.QtWidgets import QLabel, QHBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal

from Guis.Experiments import experiment


class NACTExp(experiment.Experiment):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__(person)

        # Instructions
        self.instructions.setText('Press ' + self.person.leftkey[0] + ' for |. Press ' + self.person.rightkey[0] +
                                  ' for -.')

        # Make middle layout for pictures and text
        middlelayout = QHBoxLayout()

        self.left = QLabel('')
        self.left.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left.setScaledContents(True)

        self.right = QLabel('')
        self.right.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.right.setScaledContents(True)

        middlelayout.addStretch(1)
        middlelayout.addWidget(self.left)
        middlelayout.addStretch(1)
        middlelayout.addWidget(self.middle)
        middlelayout.addStretch(1)
        middlelayout.addWidget(self.right)
        middlelayout.addStretch(1)

        # Make middle top for pictures
        middletoplayout = QHBoxLayout()

        self.topleft = QLabel('')
        self.topleft.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.topleft.setScaledContents(True)

        self.topright = QLabel('')
        self.topright.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.topright.setScaledContents(True)

        middletoplayout.addStretch(1)
        middletoplayout.addWidget(self.topleft)
        middletoplayout.addStretch(1)
        middletoplayout.addWidget(self.topright)
        middletoplayout.addStretch(1)

        # Make middle bottom for pictures
        middlebottomlayout = QHBoxLayout()

        self.bottomleft = QLabel('')
        self.bottomleft.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bottomleft.setScaledContents(True)

        self.bottomright = QLabel('')
        self.bottomright.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bottomright.setScaledContents(True)

        middlebottomlayout.addStretch(1)
        middlebottomlayout.addWidget(self.bottomleft)
        middlebottomlayout.addStretch(1)
        middlebottomlayout.addWidget(self.bottomright)
        middlebottomlayout.addStretch(1)

        # Put everything in vertical layout
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addLayout(middletoplayout)
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addLayout(middlelayout)
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addLayout(middlebottomlayout)
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addWidget(self.quitbutton)

    def generatenext(self):
        """
        Generate the info for the next trial and put it on screen. if the final trial was just completed, then the next
        round is started or the completion text is put on screen
        """

        # if this is after the first trial is begun, stop the timer to generate a new trial
        if self.trialsdone != 0:
            self.ititimer.stop()

        # reset the border around the middle if there was something different
        self.middle.setStyleSheet('border: 0px;')

        # if-then statement to determine whether the amount of trials completed is less than the number of trials the
        # user wants
        if self.trialsdone < self.person.get_trials():

            # make a list for the pixmaps
            self.pixmaps = []

            # obtain the list of strings
            self.picstrings = self.person.get_trial_pic()

            # add the appropriate elements to the picture strings and add the revised strings to the pixmap list
            for pic in self.picstrings:

                pathstring = 'Assets/' + pic + '.png'
                self.pixmaps.append(QPixmap(pathstring))

            # arrange the pixmaps around the screen
            self.topleft.setPixmap(self.pixmaps[0].scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio))
            self.left.setPixmap(self.pixmaps[1].scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio))
            self.bottomleft.setPixmap(self.pixmaps[2].scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio))
            self.bottomright.setPixmap(self.pixmaps[3].scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio))
            self.right.setPixmap(self.pixmaps[4].scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio))
            self.topright.setPixmap(self.pixmaps[5].scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio))

            # set the fixation cross
            self.middle.setText('+')

            # get the onset time for the trial, which will also be used to compute reaction time
            self.starttime = time.time() - self.overallstart

            # set the timers, with the trial lasting between 1.2 and 1.5 seconds
            randomtimer = random.randint(1200, 1500)

            self.timer.start(randomtimer)
            self.ititimer.start(randomtimer+1000)

            # Set the variable that allows the user to respond
            self.responseenabled = 1

        # if the trials requested have been completed
        else:

            # reset trials done to 0
            self.trialsdone = 0

            # load the text for the next round
            self.middle.setText(self.person.nextround())

            # if the second part is finished, output the data and thank the participant
            if self.person.part == 3:

                self.person.output()
                self.instructions.setText('Thank you!')

            # otherwise, allow the user to start the next round
            else:
                self.betweenrounds = 1

    def iti(self):
        """
        screen for between trials, which blanks out the pixmaps and removes the border around the middle
        """

        # blank out all pixmaps
        self.topleft.setPixmap(QPixmap())
        self.left.setPixmap(QPixmap())
        self.bottomleft.setPixmap(QPixmap())
        self.bottomright.setPixmap(QPixmap())
        self.right.setPixmap(QPixmap())
        self.topright.setPixmap(QPixmap())

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
        self.middle.setText(self.person.updateoutput(self.trialsdone, self.starttime, 9999, 3))

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

            # reset the instructions to 0 in case they user wants to read instructions again next round
            self.inst = 0

            # generate the next trial
            self.generatenext()

            # indicate that the participant is no longer between rounds so g and i keys won't mess things up
            self.betweenrounds = 0

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
            self.middle.setText(self.person.updateoutput(self.trialsdone, self.starttime, rt, response))

            # set the window to the iti screen
            self.iti()

        # if someone presses the i key and the participant is between rounds...
        if (key in ['i', 'I']) & (self.betweenrounds == 1):

            # increase the index for the instructions
            self.inst += 1

            # if this is the first part...
            if self.person.part == 1:

                # if this is the fourth instruction...
                if self.inst == 4:
                    pixmap = QPixmap('Assets/NACT_Part1Ex1.png')
                    self.middle.setPixmap(pixmap.scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio))

                # if this is the fifth instruction...
                elif self.inst == 5:
                    pixmap = QPixmap('Assets/NACT_Part1Ex2.png')
                    self.middle.setPixmap(pixmap.scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio))

                # if this is the twelth instruction...
                elif self.inst == 12:
                    pixmap = QPixmap('Assets/NACT_FixEx.png')
                    self.middle.setPixmap(pixmap.scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio))

                # if this is an instruction other than those above...
                else:

                    # get the associated text
                    self.middle.setText(self.person.get_instructions(self.inst))

                # if the index reaches fourteen...
                if self.inst == 14:

                    # reset to zero so the instructions can be viewed again
                    self.inst = 0

            # if this is part 2...
            else:

                # if this is the fifth instruction...
                if self.inst == 5:
                    pixmap = QPixmap('Assets/NACT_Part2Ex1.png')
                    self.middle.setPixmap(pixmap.scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio))

                # if this is the sixth instruction...
                elif self.inst == 6:
                    pixmap = QPixmap('Assets/NACT_Part2Ex2.png')
                    self.middle.setPixmap(pixmap.scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio))

                # if this is the eighth instruction...
                elif self.inst == 8:
                    pixmap = QPixmap('Assets/NACT_FixEx.png')
                    self.middle.setPixmap(pixmap.scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio))

                # if this is an instruction other than those above...
                else:

                    # get the associated text
                    self.middle.setText(self.person.get_instructions(self.inst))

                # if the index reaches thirteen...
                if self.inst == 13:

                    # reset to zero so the instructions can be viewed again
                    self.inst = 0
