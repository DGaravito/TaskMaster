from PyQt6.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QLineEdit, QGridLayout, QPushButton
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
        self.instquitlayout.addLayout(self.quitmenulayout)

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
                self.menubutton.show()

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

        # Instructions, depending on controls
        if self.person.controlscheme != 'Mouse':
            instructions = 'Press ' + self.person.leftkey[0] + ' if the letter is a false alarm. Press ' +\
                           self.person.rightkey[0] + ' if the letter is a target'

        else:
            instructions = 'Click the left button if the letter is a false alarm and the right button if the letter ' \
                           'is a target.'

        self.instructions.setText(instructions)

        # center middle
        self.middle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Put everything in vertical layout
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addWidget(self.middle)

        # if you're using the mouse for controls, then make sure the middle QLabel is connected to a mouse press event
        if self.person.controlscheme == 'Mouse':

            self.fabutton = QPushButton('False Alarm')
            self.targetbutton = QPushButton('Target')

            self.fabutton.clicked.connect(self.clicked_fabutton)
            self.targetbutton.clicked.connect(self.clicked_targetbutton)

            # Make middle layout for pictures and text
            buttonlayout = QHBoxLayout()

            buttonlayout.addStretch(1)
            buttonlayout.addWidget(self.fabutton)
            buttonlayout.addWidget(self.targetbutton)
            buttonlayout.addStretch(1)
            self.instquitlayout.addLayout(buttonlayout)

        self.instquitlayout.addStretch(1)
        self.instquitlayout.addLayout(self.quitmenulayout)

        # if you're using the mouse for controls, then make sure the middle QLabel is connected to a mouse press event
        if self.person.controlscheme == 'Mouse':

            # Attach QLabels to functions
            print('Not implemented yet. Contact the developer.')

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
            if self.person.roundperformance < .70:

                self.roundsdone -= 1

            # if all the rounds are completed, then output the data
            if self.person.rounds == self.roundsdone:

                self.person.output()
                self.menubutton.show()

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

    def clicked_fabutton(self):

        # only allow the button press if response is enabled
        if self.responseenabled == 1:

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

            # send the trial info to the participant class so it can be added to the dataframe
            self.person.updateoutput(self.trialsdone, self.starttime, rt, 0)

            # set the window to the iti screen
            self.iti()

    def clicked_targetbutton(self):

        # only allow the button press if response is enabled
        if self.responseenabled == 1:

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

            # send the trial info to the participant class so it can be added to the dataframe
            self.person.updateoutput(self.trialsdone, self.starttime, rt, 1)

            # set the window to the iti screen
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

            # Instructions, depending on controls
            if self.person.controlscheme != 'Mouse':
                instructions = 'Press ' + self.person.leftkey[0] + ' if the letter is a false alarm. Press ' +\
                               self.person.rightkey[0] + ' if the letter is a target'

            else:
                instructions = 'Click the left mouse button on the option you prefer.'

            self.instructions.setText(instructions)

            # if this is the first trial of the first round, set the global start time to make the onset time make more
            # sense
            if (self.trialsdone == 0) & (self.roundsdone == 0):
                self.overallstart = time.time()

            # set the screen to the iti and then start the timer until the first trial starts
            self.iti()
            self.ititimer.start(1000)

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


class DsExp(experiment.Experiment):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__(person)

        # Instructions, depending on the user settings
        if self.person.order == 'Forwards':
            instruction = 'Wait for ' + str(self.person.get_trials()) + ' numbers to be displayed. Then enter them ' \
                                                                        'in the SAME order.'

        else:
            instruction = 'Wait for ' + str(self.person.get_trials()) + ' numbers to be displayed. Then enter them ' \
                                                                        'in the REVERSE order.'

        self.instructions.setText(instruction)

        # center middle
        self.middle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # make the keypad with display
        self.middle = QVBoxLayout()

        self.display = QLineEdit()
        self.middle.addWidget(self.display)

        # make the buttons for the keypad
        self.button1 = QPushButton('1')
        self.button2 = QPushButton('2')
        self.button3 = QPushButton('3')
        self.button4 = QPushButton('4')
        self.button5 = QPushButton('5')
        self.button6 = QPushButton('6')
        self.button7 = QPushButton('7')
        self.button8 = QPushButton('8')
        self.button9 = QPushButton('9')
        self.buttondel = QPushButton('Delete')
        self.button0 = QPushButton('0')
        self.buttonsub = QPushButton('Enter')

        # connect the buttons
        self.button1.clicked.connect(self.clicked_button1)
        self.button2.clicked.connect(self.clicked_button2)
        self.button3.clicked.connect(self.clicked_button3)
        self.button4.clicked.connect(self.clicked_button4)
        self.button5.clicked.connect(self.clicked_button5)
        self.button6.clicked.connect(self.clicked_button6)
        self.button7.clicked.connect(self.clicked_button7)
        self.button8.clicked.connect(self.clicked_button8)
        self.button9.clicked.connect(self.clicked_button9)
        self.buttondel.clicked.connect(self.clicked_buttondel)
        self.button0.clicked.connect(self.clicked_button0)
        self.buttonsub.clicked.connect(self.clicked_buttonsub)

        # arrange the buttons
        keypad = QGridLayout()

        keypad.addWidget(self.button1, 0, 0, 1, 1)
        keypad.addWidget(self.button2, 0, 1, 1, 1)
        keypad.addWidget(self.button3, 0, 2, 1, 1)
        keypad.addWidget(self.button4, 1, 0, 1, 1)
        keypad.addWidget(self.button5, 1, 1, 1, 1)
        keypad.addWidget(self.button6, 1, 2, 1, 1)
        keypad.addWidget(self.button7, 2, 0, 1, 1)
        keypad.addWidget(self.button8, 2, 1, 1, 1)
        keypad.addWidget(self.button9, 2, 2, 1, 1)
        keypad.addWidget(self.buttondel, 3, 0, 1, 1)
        keypad.addWidget(self.button0, 3, 1, 1, 1)
        keypad.addWidget(self.buttonsub, 3, 2, 1, 1)

        self.middle.addLayout(keypad)

        # Put everything in vertical layout
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addLayout(self.middle)
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addLayout(self.quitmenulayout)

    def generatenext(self):
        """
        Generate the info for the next trial and put it on screen. if the final trial was just completed, then the next
        round is started or the completion text is put on screen
        """

        # stop the timer
        self.ititimer.stop()

        # clear the display screen
        self.display.setText('')

        # if-then statement to determine whether the amount of trials completed is less than the number of trials the
        # user wants
        if self.trialsdone < self.person.get_trials():

            # get the next letter
            self.display.setText(self.person.get_trial_text(self.trialsdone))
            self.ititimer.start(2000)

        # if the trials requested have been completed
        else:

            # get the start time
            self.starttime = time.time() - self.overallstart

            # start test timer and allow the user to respond
            self.timer.start(self.person.timelimit)
            self.responseenabled = 1

    def timeout(self):
        """
        if the timer runs out and the participant doesn't respond, then the timers stop, 9999 gets put in as the
        reaction time, and the trial is "completed" with an incorrect response
        """

        # stop the timer
        self.timer.stop()

        # turn off the ability for the participant to respond
        self.responseenabled = 0

        # send the trial info to the participant class
        self.person.updateoutput(self.starttime, 9999, '')

        # clear the display screen with a warning
        self.display.setText('Too slow!')

    def keyaction(self, key):
        """
        Reads the keys that are pressed and does the corresponding actions
        :param key: the key that was pressed
        """

        # if someone presses the g key and the participant is between rounds...
        if (key in ['g', 'G']) & (self.betweenrounds == 1):

            # indicate that the participant is no longer between rounds so g and i keys won't mess things up
            self.betweenrounds = 0

            # reset the border around the display if there was something different
            self.display.setStyleSheet('border: 0px;')

            # don't allow input yet
            self.responseenabled = 0

            # generate the next trial after 2 seconds
            self.ititimer.start(2000)

            # if this is the first trial of the first round, set the global start time to make the onset time make more
            # sense
            if (self.trialsdone == 0) & (self.roundsdone == 0):
                self.overallstart = time.time()

    def clicked_button1(self):

        # only allow the button press if response is enabled
        if self.responseenabled == 1:

            self.display.setText(self.display.text() + '1')

    def clicked_button2(self):

        # only allow the button press if response is enabled
        if self.responseenabled == 1:

            self.display.setText(self.display.text() + '2')

    def clicked_button3(self):

        # only allow the button press if response is enabled
        if self.responseenabled == 1:

            self.display.setText(self.display.text() + '3')

    def clicked_button4(self):

        # only allow the button press if response is enabled
        if self.responseenabled == 1:

            self.display.setText(self.display.text() + '4')

    def clicked_button5(self):

        # only allow the button press if response is enabled
        if self.responseenabled == 1:

            self.display.setText(self.display.text() + '5')

    def clicked_button6(self):

        # only allow the button press if response is enabled
        if self.responseenabled == 1:

            self.display.setText(self.display.text() + '6')

    def clicked_button7(self):

        # only allow the button press if response is enabled
        if self.responseenabled == 1:

            self.display.setText(self.display.text() + '7')

    def clicked_button8(self):

        # only allow the button press if response is enabled
        if self.responseenabled == 1:

            self.display.setText(self.display.text() + '8')

    def clicked_button9(self):

        # only allow the button press if response is enabled
        if self.responseenabled == 1:

            self.display.setText(self.display.text() + '9')

    def clicked_buttondel(self):

        # only allow the button press if response is enabled
        if self.responseenabled == 1:

            # copy the text of the current display
            orig = self.display.text()

            # get the length of the current text
            length = len(self.display.text())

            # if there is any text
            if length:

                # make new text by trimming the original text by one
                new = orig[:length - 1]

                # set the display to the new text
                self.display.setText(new)

    def clicked_button0(self):

        # only allow the button press if response is enabled
        if self.responseenabled == 1:

            self.display.setText(self.display.text() + '0')

    def clicked_buttonsub(self):

        # only allow the button press if response is enabled
        if self.responseenabled == 1:

            # get the start time
            self.endtime = time.time() - self.overallstart

            # put a border around the display to indicate a user input was received
            self.display.setStyleSheet('border: 3px solid blue;')

            # clear the display screen
            self.display.setText('')

            # indicate that the participant is no longer between rounds so g and i keys won't mess things up
            self.betweenrounds = 0

            # don't allow input anymore
            self.responseenabled = 0

            # send the trial info to the participant class
            self.person.updateoutput(self.starttime, self.endtime, self.display.text())

            # increase the number of rounds done and reset the number of trials done to 0
            self.roundsdone += 1
            self.trialsdone = 0

            # get the approrpiate text depending on if feedback is desired
            self.display.setText(self.person.nextround(self.roundsdone))

            # if all the rounds are completed, then output the data
            if self.person.rounds == self.roundsdone:

                # reset the border around the display if there was something different
                self.display.setStyleSheet('border: 0px;')

                # Output data
                self.person.output()
                self.menubutton.show()

            # if more rounds need to be done, then indicate that it is between rounds
            else:

                self.betweenrounds = 1
