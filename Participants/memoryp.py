import pandas as pd
import random
import string

from Participants import participant


class PrParticipant(participant.Participant):

    def __init__(self, expid, trials, session, outdir, task, design, stt, eyetracking):
        super().__init__(expid, trials, session, outdir, task, eyetracking)

        # create a list for the eventual trial info
        self.trialinfo = []

        # if the user requested an STT design
        if stt == 'Yes':

            # add STT to a string that is made of "ST" multiplied by how many blocks the user requested (minus one so
            # the STT doesn't add an extra block
            structstr = 'STT' + ('ST' * (int(design) - 1))
            self.structure = list(structstr)

        # if no STT is requested
        else:

            # make the structure string out of of "ST" multiplied by how many blocks the user requested
            structstr = 'ST' * int(design)
            self.structure = list(structstr)

        # Experiment settingsguis output dataframe
        dict_tasksettings = {
            'Design': [structstr]
        }

        # attach the task-specific settings to the task general settings
        self.set_settings(dict_tasksettings)

        # call the set pairs function to create the list of word pairs for all the blocks
        self.set_pairs(int(trials))

    def set_pairs(self, trials):
        """
        Takes the original dictionary of word pairs and then truncates it depending on how many word pairs the user
        requested
        :param trials: an integer representing how many word pairs the user wants
        """

        # make a dictionary of the original word pairs
        originalpairs = {
            'Pony': ['Cranberry'],
            'Minister': ['Liquor'],
            'Cloud': ['Café'],
            'Screwdriver': ['Leg'],
            'Vodka': ['Gym'],
            'Ant': ['Beer'],
            'Refridgerator': ['Lion'],
            'Tangerine': ['Steam'],
            'Cradle': ['Smoke'],
            'Nurse': ['Violin'],
            'Chocolate': ['Square'],
            'Crabs': ['Box'],
            'Toe': ['Crocodile'],
            'Coin': ['Duck'],
            'Microscope': ['Dentist'],
            'Jail': ['Telescope'],
            'Fence': ['Sail'],
            'Dark': ['Rowboat'],
            'Jockey': ['Bubble'],
            'Spinach': ['Mansion'],
            'Fish': ['President'],
            'University': ['Sun'],
            'Bra': ['Can-Opener'],
            'Bracelet': ['Needle'],
            'Beach': ['Penny'],
            'Flashbulbs': ['Bomb'],
            'Cake': ['Professor'],
            'Doctor': ['Mosquito'],
            'Rain': ['Gorilla']
        }

        # if the original number of word pairs is greater than the number of pairs requested
        if len(originalpairs) > trials:

            # measure the difference between the two and then delete any extras
            for n in range(len(originalpairs) - trials):

                del originalpairs[next(iter(originalpairs))]

        # copy the revised word dictionary for the experiment
        self.expwordpairs = dict(originalpairs)

        # copy the dictionary again to make a dictionary for the trial to go through
        self.trialwordpairs = dict(self.expwordpairs)

        # call the function to make the list a dataframe and save it
        self.updateoutput()

    def starttrial(self):
        """
        copy the word pairs for the experiment and then tell the participant to start the trial
        :return: string of instructions for the participant
        """

        # copy the dictionary of word pairs
        self.trialwordpairs = dict(self.expwordpairs)

        # set the prompt
        prompt = 'Please let the researcher know you are ready'

        # return the prompt
        return prompt

    def get_design_text(self, test):
        """
        A function that gets a wordpair for the trial, returns the info, and then eliminates it from the total
        dictionary
        :param test: a binary value, 0 if it's a study block and 1 if it's a test block
        :return: three strings (left, middle (empty), and right (which is empty in test blocks))
        """

        # blank out the list for the trial info
        self.trialinfo = []

        # if this is a study trial
        if test == 0:

            # randomly choose a pair from the wordpair dictionary, make it a list, and then set it to the sides of the
            # trial
            leftstring, rightstring = random.choice(list(self.trialwordpairs.items()))

            # the right string will be the first part of the list that it was set to
            rightstring = rightstring[0]

        # if this is a test trial
        else:

            # set the left string to a list made of a random key from the dictionary
            leftstring = random.choice(list(self.trialwordpairs))

            # make the right side a blank string
            rightstring = ''

        # delete the key and value from the block's dictionary
        del self.trialwordpairs[leftstring]

        # make the middle an empty string
        middlestring = ''

        # add the strings to the trial info
        self.trialinfo = [leftstring, rightstring, middlestring]

        return self.trialinfo

    def updateoutput(self):
        """
        this function just makes a dataframe of the word pairs and updates the corresponding existing dataframe
        :return:
        """

        df_simultrial = pd.DataFrame(data=self.expwordpairs)

        self.set_performance(df_simultrial)

    def get_instructions(self, instint):
        """
        Takes in an int and returns the appropriate instructions string
        :param instint: an int that is supplied and incremented by the expguis
        :return: a string containing the appropriate instructions that the expguis puts up
        """

        match instint:

            case 1:

                inst = 'We are going to do memory tasks that involve\nremembering pairs of familiar words.'

            case 2:

                inst = 'I will show you a list of word pairs, and you will\nattempt to recall one of the words in' \
                       ' each pair.'

            case 3:

                inst = 'On the screen, I will show you pairs of words.'

            case 4:

                inst = 'I will show you the pairs of words one at a time,\nat rate of 4 seconds per pair, and I will' \
                       ' read the words aloud\nas they appear on the screen.'

            case 5:

                inst = 'Your task is to try to remember as many of the\nword pairs as you can, for a later memory' \
                       ' test.'

            case 6:

                inst = 'After I have shown you all word pairs, we will\ndo the first memory test.'

            case 7:

                inst = 'On that test, I will show you the first word\nof each pair, and you will try to recall the' \
                       ' second word that\ngoes with it.'

            case 8:

                inst = 'For example, if one of the word pairs was\nSANDWICH-SHOES, I would show you the word' \
                       ' SANDWICH, and\nyou would try to recall SHOES.'

            case 9:

                inst = 'If you can’t recall a word after 5 seconds,\nwe will move on to the next pair. All pairs will' \
                       ' be tested in a\nrandom order.'

            case 10:

                inst = 'We will continue like this until your memory\nfor all word pairs has been tested.'

            case 11:

                inst = 'After the first test, we will do a second test\nthat is just like the first.'

            case 12:

                inst = 'That is, I will show you the first word of each\npair again, and you will try to recall' \
                       ' the second word that\ngoes with it.'

            case 13:

                inst = 'After this second memory test, we will study\nthe 30 word pairs again.'

            case 14:

                inst = 'After I have shown you all 30 word pairs, we will do\nanother memory test that is just like' \
                       ' the first 2 tests.'

            case 15:

                inst = 'After that memory test, we will study the 30 word\npairs one more time before having a' \
                       'final memory test.'

            case _:

                inst = 'Let the experimenter know you are ready.'

        return inst


class NbParticipant(participant.Participant):

    def __init__(self, expid, trials, session, outdir, task, feedback, rounds, buttonbox, eyetracking):
        super().__init__(expid, trials, session, outdir, task, buttonbox, eyetracking)

        # set whether the user wants participant feedback
        self.feedback = feedback

        # extract the number of blocks from user input
        self.rounds = int(rounds)

        # reset the list of total letters shown with strings of non-letters so that we don't accidentally make a
        # target at the start
        self.backlist = ['1', '1', '1', '1']

        # set the number of correct and percent correct to 0 at the start
        self.roundperformance = 0.0
        self.roundsumcorrect = 0

        # Experiment settingsguis output dataframe
        dict_tasksettings = {
            'Rounds': [rounds],
            'Feedback': [feedback]
        }

        # attach the task-specific settings to the task general settings
        self.set_settings(dict_tasksettings)

    def nextround(self, roundsdone):

        # calculate how well the participant did by dividing total score by total trials
        self.roundperformance = self.roundsumcorrect/self.get_trials()

        # if all requested blocks are completed and the participant got 50% correct or better on the last block...
        if (roundsdone == self.rounds) & (self.roundperformance >= 0.5):

            # thank them and send their performance stats if the user wanted feedback
            prompt2 = 'Thank you! This task is complete.'

            if self.feedback == 'Yes':

                prompt1 = 'You got ' + str('{:.1f}'.format(self.roundperformance)) + '% correct.'

            else:

                prompt1 = ''

        # if there are still blocks to go or the participant did worse than 50% on the last block
        else:

            # reset the list of total letters shown with strings of non-letters so that we don't accidentally make a
            # target at the start
            self.backlist = ['1', '1', '1', '1']

            # if the participant did 50% or better on the last block, return their stats (if the user wanted that)
            if self.roundperformance >= 0.5:

                if self.feedback == 'Yes':

                    prompt1 = 'You got ' + str('{:.1f}'.format((self.roundperformance * 100))) + '% correct.'

                else:

                    prompt1 = ''

            # if the participant did worse than 50% on the last block, return their stats and let them know
            else:

                if self.feedback == 'Yes':

                    prompt1 = 'You got ' + str('{:.1f}'.format(self.roundperformance)) + '% correct.'

                else:

                    prompt1 = 'Please try harder.'

            # tell the participant to wait for the next round
            prompt2 = 'Please let the researcher know you are ready'

        # put the prompts into a list
        prompts = [prompt1, prompt2]

        # reset number of correct to 0
        self.roundsumcorrect = 0

        # return the prompts
        return prompts

    def get_trial_text(self):
        """
        Randomly picks a letter, adds it to the list of all letters shown, and then returns it
        :return: One character string of an uppercase letter
        """

        # randomly pick a letter
        while True:
            newletter = random.choice(string.ascii_uppercase)

            # Use fewer letters and only those that won't be confused with other letters
            if newletter not in ['A', 'E', 'I', 'O', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']:
                break

        # add the new letter to the list of all shown letters
        self.backlist.append(newletter)

        # return the new letter
        return newletter

    def updateoutput(self, trial, onset, time, response=3):
        """
        evaluates whether the person got the n-back correct based on their response
        :param trial: the trial that was just completed
        :param onset: onset time for the trial
        :param time: participants's reaction time
        :param response: integer with either 0 or 1 depending on if the person thought the letter was a false-alarm
        or a target. Default is 3 in case the participants doesn't answer in time.
        :return: updates the performance dataframe in the superclass
        """

        # participant is incorrect by default
        correct = 0

        # if the task was a 1-back
        if self.task == '1-back':

            # the partipant called the letter a target and the last item  is not the same as the one before
            if (response == 1) & (self.backlist[-1] == self.backlist[-2]):
                correct = 1

            # the partipant called the letter a false alarm and the last item  is not the same as the one before
            elif (response == 0) & (self.backlist[-1] != self.backlist[-2]):
                correct = 1

        # if the task was a 2-back
        elif self.task == '2-back':

            # the partipant called the letter a target and the last item is the same as the one 2 before
            if (response == 1) & (self.backlist[-1] == self.backlist[-3]):
                correct = 1

            # the partipant called the letter a false alarm and the last item is not the same as the one 2 before
            elif (response == 0) & (self.backlist[-1] != self.backlist[-3]):
                correct = 1

        # if the task was a 3-back
        elif self.task == '3-back':

            # the partipant called the letter a target and the last item is the same as the one 3 before
            if (response == 1) & (self.backlist[-1] == self.backlist[-4]):
                correct = 1

            # the partipant called the letter a false alarm and the last item is not the same as the one 3 before
            elif (response == 0) & (self.backlist[-1] != self.backlist[-4]):
                correct = 1

        # if the task was a 4-back
        else:

            # the partipant called the letter a target and the last item is the same as the one 4 before
            if (response == 1) & (self.backlist[-1] == self.backlist[-5]):
                correct = 1

            # the partipant called the letter a false alarm and the last item is not the same as the one 4 before
            elif (response == 0) & (self.backlist[-1] != self.backlist[-5]):
                correct = 1

        # add the score (0 or 1) to the participant's score for the round
        self.roundsumcorrect += correct

        # make a dictionary of trial info
        df_trial = {
            'trial': [trial],
            'letter': [self.backlist[-1]],
            'onset': [onset],
            'response': [response],
            'reaction time': [time],
            'correct': [correct]
        }

        # turn that dictionary into a dataframe and use set_performance to add it to the overall dataframe
        df_trial = pd.DataFrame(data=df_trial)
        self.set_performance(df_trial)

    def get_instructions(self, instint):
        """
        Takes in an int and returns the appropriate instructions string
        :param instint: an int that is supplied and incremented by the expguis
        :return: a string containing the appropriate instructions that the expguis puts up
        """

        match instint:

            case 1:

                inst = 'You will see a series of letters come up on\nthe screen.'

            case 2:

                inst = 'Each letter will be followed by a plus sign,\nwhich is just a placeholder that you can ignore.'

            case 3:

                inst = 'Your job is to decide whether each letter that\ncomes up is a \"target\" or a \"false alarm\".'

            case 4:

                inst = 'If a letter is a target,you will press \"' + self.rightkey[0] + \
                       '\"\nwhen it comes up. If it is a false alarm, you will press \"' + self.leftkey[0] + \
                       '\"\nwhen it comes up.'

            case 5:

                # depending on the the specific task, this instruction will be changes
                if self.task == '1-back':

                    inst = 'In this task, a letter is a target if\nit is the same as the letter immediately' \
                           ' before it.'

                elif self.task == '2-back':

                    inst = 'In this task, a letter is a target if\nit is repeated with one letter in between. ' \
                           'Targets are letters\nyou saw two letters ago.'

                elif self.task == '3-back':

                    inst = 'In this task, a letter is a target if\nit is repeated with two letters in between.' \
                           ' Targets are letters\nyou saw three letters ago.'

                else:

                    inst = 'In this task, a letter is a target if\nit is repeated with three letters in between.' \
                           ' Targets are letters\nyou saw four letters ago.'

            case 6:

                # depending on the the specific task, this instruction will be changes
                if self.task == '1-back':

                    inst = 'For example, if you saw A, then B, then\nanother B, the second B would be a target.'

                elif self.task == '2-back':

                    inst = 'For example, if you saw A, then B, then\nanother A, the second A would be a target.'

                elif self.task == '3-back':

                    inst = 'For example, if you saw A, then B, then\nC, then another A, the second A would be a ' \
                           'target.'

                else:

                    inst = 'For example, if you saw A, then B, then\nC, then D, then another A, the second A would be' \
                           ' a target.'

            case 7:

                # depending on the the specific task, this instruction will be changes
                if self.task == '1-back':

                    inst = 'In this case, you would press \"' + self.leftkey[0] + '\" for the A,\nthen \"' + \
                           self.leftkey[0] + '\" for the first B, and then \"' + self.rightkey[0] + \
                           '\" for\nthe second B.'

                elif self.task == '2-back':

                    inst = 'In this case, you would press \"' + self.leftkey[0] + '\" for the A,\nthen \"' + \
                           self.leftkey[0] + '\" for the first B, and then \"' + self.rightkey[0] + \
                           '\" for\nthe second A. If a B came next, it would also be\na target.'

                elif self.task == '3-back':

                    inst = 'In this case, you would press \"' + self.leftkey[0] + \
                           '\" for the A,\nB and C, and then press \"' + self.rightkey[0] + '\" for the second A.'

                else:

                    inst = 'In this case, you would press \"' + self.leftkey[0] + \
                           '\" for the A,\nB, C, and D, and then press \"' + self.rightkey[0] + '\" for the second A.'

            case 8:

                inst = 'Each letter will appear for about 2 second.\n If you do not respond within that time, the ' \
                       'task will\nmove on and you will be marked as incorrect.'

            case 9:

                inst = 'As soon as a letter comes up, make your response.'

            case 10:

                inst = 'You will get feedback on your performance after\neach block of the task.'

            case _:

                inst = 'Please let the experimenter know when you are ready.'

        return inst


class DsParticipant(participant.Participant):

    def __init__(self, expid, trials, session, outdir, task, order, diff, feedback, tlimit, rounds, eyetracking):
        super().__init__(expid, trials, session, outdir, task, eyetracking)

        # extract settings
        self.order = order
        self.diff = diff
        self.feedback = feedback
        self.timelimit = int(tlimit)

        # extract the number of blocks from user input
        self.rounds = int(rounds)

        # make a starting list
        self.set_list()

        # set the number of correct and percent correct to 0 at the start
        self.roundperformance = 0.0
        self.roundsumcorrect = 0

        # Experiment settingsguis output dataframe
        dict_tasksettings = {
            'Tests': [rounds],
            'Order for Participant Input': [order],
            'Starting Difficulty': [trials],
            'Difficulty Change': [diff],
            'Feedback': [feedback],
            'Time Limit for Typing': [tlimit]
        }

        # attach the task-specific settings to the task general settings
        self.set_settings(dict_tasksettings)

    def nextround(self, roundsdone):

        # if all requested tests are completed, provide feedback (if requested) and thank the participant
        if roundsdone == self.rounds:

            if self.feedback == 'Yes':

                prompt = 'You got ' + str('{:.1f}'.format(self.roundperformance)) + '% correct.\nThis task is complete.'

            else:

                prompt = 'This task is complete.'

        # if there are still tests to go
        else:

            # if the user wanted increasing difficulty, add 1 to the number of numbers for the next test
            if self.diff == 'Increasing':

                self.trials += 1

            # if requested, return participant stats
            if self.feedback == 'Yes':

                prompt = 'You got ' + str('{:.1f}'.format((self.roundperformance * 100))) + '% correct.\nPress \'G\' ' \
                                                                                            'for the next test.'

            # otherwise, instruct the participant to start the next trial
            else:

                prompt = 'Press \'G\' wait for the next test.'

            # make a new list of numbers
            self.set_list()

        # reset number of correct to 0
        self.roundsumcorrect = 0

        # return the prompts
        return prompt

    def get_trial_text(self, trial):
        """
        Picks the appropriate number from the number list and returns it
        :param trial: last trial that was completed
        :return: an int from the number list
        """

        # pick the number that corresponds to the correct trial
        displaynumber = self.numberlist[trial]

        # return the new letter
        return displaynumber

    def set_list(self):
        """
        Makes a list of numbers for the test
        """

        # empty list
        self.numberlist = []

        # for the number of numbers requested, add a random one to the list
        for number in range(self.trials):
            # randomly pick a letter
            newnumber = random.randint(0, 9)

            # add the new letter to the list of all shown letters
            self.numberlist.append(newnumber)

    def updateoutput(self, onset, time, response):
        """
        evaluates whether the person got the n-back correct based on their response
        :param onset: onset time for the trial
        :param time: participants's reaction time
        :param response: integer with either 0 or 1 depending on if the person thought the letter was a false-alarm
        or a target. Default is 3 in case the participants doesn't answer in time.
        :return: None: updates the performance dataframe in the superclass
        """

        # only do the following if there was a response by the participant
        if response != '':

            # turn the response string into a list of integers
            responseints = [eval(i) for i in response]

            # for the number of numbers in the test...
            for number in range(self.get_trials()):

                # if the order is forwards...
                if self.order == 'Forwards':

                    # and the number from the list matches the one in the same position in the response
                    if self.numberlist[number] == responseints[number]:

                        # add a point
                        self.roundsumcorrect += 1

                # if the order is backwards...
                else:

                    # reverse the response list by copying by value and then using the reverse function
                    responseintsrev = list(responseints)
                    responseintsrev.reverse()

                    # check the same, but with the reversed response
                    if self.numberlist[number] == responseintsrev[number]:

                        # add a point
                        self.roundsumcorrect += 1

        # calculate how well the participant did by dividing total score by total trials
        self.roundperformance = self.roundsumcorrect / self.get_trials()

        # make a dictionary of trial info
        df_trial = {
            'difficulty': [self.get_trials()],
            'list': [self.numberlist],
            'response': [response],
            'reaction time': [time],
            'correct_raw': [self.roundsumcorrect],
            'correct_perc': [self.roundperformance]
        }

        # turn that dictionary into a dataframe and use set_performance to add it to the overall dataframe
        df_trial = pd.DataFrame(data=df_trial)
        self.set_performance(df_trial)

    def get_instructions(self, instint):
        """
        Takes in an int and returns the appropriate instructions string
        :param instint: an int that is supplied and incremented by the expguis
        :return: a string containing the appropriate instructions that the expguis puts up
        """

        match instint:

            case 1:

                inst = 'You will see a series of numbers come up on\nthe screen.'

            case 2:

                inst = 'Each letter will be followed by a plus sign,\nwhich is just a placeholder that you can ignore.'

            case 3:

                inst = 'Your job is to remember the numbers that\ncome up and then type them when asked.'

            case 4:

                # depending on the the specific settings, this instruction will be changes
                if self.order == 'Forwards':

                    inst = 'When asked, type the numbers back in exactly\nthe SAME order that you saw them.'

                else:

                    inst = 'When asked, type the numbers back in exactly\nthe OPPOSITE order that you saw them.'

            case 5:

                inst = 'For example, if you were shown 9, then 5, then\n3, then 8...'

            case 6:

                # depending on the the specific settings, this instruction will be changes
                if self.task == 'Forwards':

                    inst = 'You would type 9538 (the SAME numbers in the\nSAME order) when asked.'

                else:

                    inst = 'You would type 8359 (the SAME numbers in the\nOPPOSITE order) when asked.'

            case 7:

                inst = 'You will only have ' + str('{:.2f}'.format(self.timelimit/1000)) + ' seconds to enter the ' \
                                                                                           'numbers when asked, so ' \
                                                                                           'keep that in mind.'

            case 8:

                # depending on the the specific settings, this instruction will be changes
                if self.diff == 'Static':

                    inst = 'Each test will only include ' + str(self.get_trials()) + ' numbers.'

                else:

                    inst = 'The next test will include ' + str(self.get_trials()) + ' numbers.\nEach test will ' \
                                                                                    'increase in difficulty by adding' \
                                                                                    ' an additional number.'

            case 9:

                # depending on the the specific settings, this instruction will be changes
                if self.feedback == 'Yes':

                    inst = 'You will get feedback on your performance after\neach test.'

                else:

                    inst = 'You will not get feedback on your performance,\nso make sure to do your best.'

            case _:

                inst = 'Please let the experimenter know when you are ready.'

        return inst
