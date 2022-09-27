from Participants import participant

import pandas as pd
import random


class NACTParticipant(participant.Participant):

    def __init__(self, expid, session, outdir, task, hightrials, lowtrials, money, buttonbox, eyetracking):

        # the total number of trials is equal to the sum of the low and high trials
        trials = lowtrials + hightrials

        super().__init__(expid, trials, session, outdir, task, buttonbox, eyetracking)

        # either green or red is chosen as the high-value color
        self.highcolor = random.choice(['Green', 'Red'])

        # if the high-value color is green, the low-value color is red
        if self.highcolor == 'Green':

            self.lowcolor = 'Red'

        # if the high-value color is red, the low-value color is green
        else:

            self.lowcolor = 'Green'

        # set the variable to indicate to start with the first part
        self.part = 1

        # set the variable for how much starting money the participant has
        self.startmoney = float(money)

        # call the set_design function with the number of low and high trials
        self.set_design(hightrials, lowtrials)

        # Experiment settingsguis output dictionary
        dict_simulsettings = {
            'Starting money': [money],
            'Low value trials': [lowtrials],
            'Low value color': [self.lowcolor],
            'High value trials': [hightrials],
            'High value color': [self.highcolor]
        }

        # send the task-specific dictionary to be added to the generic task settings
        self.set_settings(dict_simulsettings)

    def set_design(self, high, low):
        """
        takes in the number of high and low trials and creates a list of strings that represents which trials are high-
        value and which are low-value. This is then randomized so that you get the final order
        :param high: integer that is the number of high-value trials
        :param low: integer that is the number of low-value trials
        """

        # list composed of the two strings: the high-value color and the low-value color
        trialtypes = [self.highcolor, self.lowcolor]

        # list composed of the number of high-value trials and number of low-value trials
        multiplier = [high, low]

        # the strings are multiplied so that you end up with a list of strings. The name of the low-value color appears
        # however many low-value trials were requested, and vice versa
        self.piclist = sum([[s] * n for s, n in zip(trialtypes, multiplier)], [])

        # copy this list to a new variable so that it can be copied again in the future
        self.picorder = list(self.piclist)

        # randomize the order of things in the list
        random.shuffle(self.picorder)

    def nextround(self):
        """
        increments the part that the participant is on and sends the appropriate string back
        :return:
        """

        # increment the part indicator
        self.part += 1

        # if you have completed part 2, then thank the participant
        if self.part >= 3:

            prompt = 'Thank you! This task is complete.'

        # otherwise...
        else:

            # grab the list of pictures and then randomize the order
            self.picorder = list(self.piclist)
            random.shuffle(self.picorder)

            # tell the participant to wait for instruction
            prompt = 'Please wait for the researcher to read you the instructions'

        # return the prompt
        return prompt

    def get_trial_pic(self):
        """
        technically a setter and getter. depending on the part of the task, you'll generate something different
        :return: randomized list of picture strings to the gui so that the pictures appear on screen
        """

        # have a list of all possible colors (not including the high and low value colors)
        colors = ['Black', 'Purple', 'Yellow', 'Orange', 'Teal', 'Blue']

        # shuffle the list of colors
        random.shuffle(colors)

        # make an empty list that will be filled with your picture strings
        pics = []

        # set a string that is equal to the prefix for all pictures
        prefix = 'NACT_'

        # pop the value, which determines whether the trial will include the high or low value color
        self.trialvalue = self.picorder.pop()

        # randomly pick whether the signal will have a horizontal or vertical line
        self.signalnumber = random.randint(1, 2)

        if self.part == 1:
            # In part one, we need everything to be circles, and the high or low value color will always be the
            # stimuli that the participants focuses on

            # for those remaining distractor colors, turn them each into strings for a picture
            for color in colors:

                distractornumber = str(random.randint(1, 2))

                distractorstring = prefix + 'd' + color + 'Cir' + distractornumber
                pics.append(distractorstring)

            # shuffle the list of distractor pictures
            random.shuffle(pics)

            # get a string to represent the signal picture
            signalstring = prefix + 's' + self.trialvalue + 'Cir' + str(self.signalnumber)

            # generate a random integer that will be used to pic a random distractor so that you can...
            signalplace = random.randint(0, 5)

            # ...replace one of the distractors with this signal string!
            pics[signalplace] = signalstring

        else:
            # for part two, we need to have all the distractors one shape and the signal be the other shape
            # We also need to add the high or low value color in the list but can't make it a signal because we
            # don't have an asset for that

            # remove one of the colors; that will be our signal color
            signalcolor = colors.pop()

            # pick a random shape for all the distractors to be
            shape = random.choice(['Cir', 'Dia'])

            # for those remaining distractor colors, turn them each into strings for a picture
            for color in colors:

                distractornumber = str(random.randint(1, 2))

                distractorstring = prefix + 'd' + color + shape + distractornumber
                pics.append(distractorstring)

            # next, shuffle the picture strings
            random.shuffle(pics)

            # if the distractors are circles, make the signal a diamond, and vice versa
            if shape == 'Cir':

                signalshape = 'Dia'

            else:

                signalshape = 'Cir'

            # get a string to represent the signal picture
            signalstring = prefix + 's' + signalcolor + signalshape + str(self.signalnumber)

            # generate a random integer that will be used to pic a random distractor so that you can...
            signalplace = random.randint(0, 4)

            # ...replace one of the distractors with this signal string!
            pics[signalplace] = signalstring

            # add in a distractor that has the high or low value color
            valuedistractornumber = str(random.randint(1, 2))
            valuedistractorstring = prefix + 'd' + self.trialvalue + shape + valuedistractornumber
            pics.append(valuedistractorstring)

        # shuffle the list of picture strings
        random.shuffle(pics)

        # return the pictures
        return pics

    def updateoutput(self, trial, onset, rt, response):
        """
        evaluates whether the person got the trial correct based on their response, updates the performance dataframe
        in the superclass, and gives feedback
        :param trial: the number of the trial that was just completed
        :param onset: onset time for trial
        :param rt: participants's reaction time
        :param response: int with 0, 1, or 3 depending on what the person chose (3 if they didn't choose).
        :return: feedback string: how much money they lost and their total money (or a fixation cross), which is use
         in the iti
        """

        # participant is incorrect by default
        correct = 0

        # find out whether the participants was correct
        # if the stimulus included a vertical line...
        if self.signalnumber == 1:

            # make the stimulus string 'Vertical'
            stimstring = 'Vertical'

            # the participant was correct if they hit the left key
            if response == 0:
                correct = 1

        # if the stimulus included a horizontal line...
        else:

            # make the stimulus string 'Horizontal'
            stimstring = 'Horizontal'

            # the participant was correct if they hit the right key
            if response == 1:
                correct = 1

        # if you're in the first part...
        if self.part == 1:

            # and you are correct...
            if correct == 1:

                # you lose nothing.
                feedback = 0.0

            # and you are incorrect on a high value trial...
            elif (correct == 0) & (self.highcolor == self.trialvalue):

                # you lose 15 cents.
                feedback = 0.15

            # and you are incorrect on a low value trial...
            else:

                # you lose 3 cents.
                feedback = 0.03

            # subtract how much yuou lost from the starting money
            self.startmoney -= feedback

            # create a string to inform the participants
            feedbackstring = 'You lost $' + str('{:.2f}'.format(feedback)) + '. You have $' + \
                             str('{:.2f}'.format(self.startmoney)) + ' left.'

        # If you are in part 2, just create a fixation cross
        else:
            feedbackstring = '+'

        # create a dictionary of the trial info so that you can update the overall performance dataframe
        df_simultrial = {
            'trial': [trial],
            'onset time': [onset],
            'part': [self.part],
            'value color': [self.trialvalue],
            'signal': [stimstring],
            'response': [response],
            'reaction time': [rt],
            'correct': [correct],
            'money remaining': [self.startmoney]
        }

        # turn the dictionary into a dataframe
        df_simultrial = pd.DataFrame(data=df_simultrial)

        # update the overall performance dataframe
        self.set_performance(df_simultrial)

        # return the string for the iti
        return feedbackstring

    def get_instructions(self, instint):
        """
        Takes in an int and returns the appropriate instructions string
        :param instint: an int that is supplied and incremented by the expguis
        :return: a string containing the appropriate instructions that the expguis puts up
        """

        # if the participant is on the first part, you have a different set of instructions compared to the second part
        if self.part == 1:

            match instint:

                case 1:

                    inst = 'In this part of the task, you need to look\nfor a red or green circle (either one ' \
                           'could appear,\nbut never both).'

                case 2:

                    inst = 'Inside the red or green circle, there will\nbe a line that either looks like this \"|\"' \
                           ' or like\nthis \"-\".'

                case 3:

                    inst = 'Next, you will see two examples, which the experimenter will describe'

                case 6:

                    inst = 'You have $' + str('{:.2f}'.format(self.startmoney)) + ' in starting money. Your final ' \
                                                                                  'payment\nwill depend on the ' \
                                                                                  'choices you make in this task.'

                case 7:

                    inst = 'You will lose money each time you respond\nincorrectly or too slowly.'

                case 8:

                    inst = 'If you respond too slowly, you will hear\na beeping sound.'

                case 9:

                    inst = 'You will be able to see how much you have\nlost.'

                case 10:

                    inst = 'How much you lose each time will vary.'

                case 11:

                    inst = 'Also, try to keep your eyes on the cross\nat the center of the screen.'

                case _:

                    inst = 'Please let the experimenter know\nwhen you are ready.'

        else:

            match instint:

                case 1:

                    inst = 'In this part of the task, you need to look\nfor the shape that is different from all the' \
                           ' others.'

                case 2:

                    inst = 'The only possible shapes are circles or squares.'

                case 3:

                    inst = 'Inside the different shape, there will\nbe a line that either looks like this \"|\"' \
                           ' or like\nthis \"-\".'

                case 4:

                    inst = 'Next, you will see two examples, which the experimenter will describe'

                case 7:

                    inst = 'Just like before, try to respond quickly\nand keep your eyes on the cross at the center ' \
                           'of\nthe screen.'

                case 9:

                    inst = 'Again, if you respond too slowly, you\nwill hear a beeping sound.'

                case 10:

                    inst = 'You cannot lose money in this part of\nthe task. Just try to respond quickly while still' \
                           '\ngetting most of the trials correct.'

                case _:

                    inst = 'Please let the experimenter know\nwhen you are ready.'

        return inst
