from Participants import participant

import pandas as pd
import random


class SSParticipant(participant.Participant):

    def __init__(self, expid, trials, session, outdir, task, maxrt, blocks, buttonbox, eyetracking):
        super().__init__(expid, trials, session, outdir, task, buttonbox, eyetracking)

        # set the defaults based on user input
        self.blocks = int(blocks)
        self.globallocal = random.choice(['Global', 'Local'])
        self.maxrt = int(maxrt)

        # make the starting timer 250 milliseconds
        self.timer = 250

        # set the structure
        self.set_structure()

        # Experiment settingsguis output dataframe
        dict_tasksettings = {
            'Blocks': [blocks],
            'Max reaction time': [maxrt]
        }

        # attach the task-specific settings to the task general settings
        self.set_settings(dict_tasksettings)

    def set_structure(self):
        """
        Sets up the main picture list and copies and shuffles that for the first block's order
        """

        # divide the number of trials by 2 because there are 2 types of trials
        multnum = int(self.get_trials() / 2)

        # list composed of 2 integers which are one half of the total trials
        multiplier = [multnum, multnum]

        # list composed of 2 strings for the 2 types of trials
        picturenames = ['SS_LeftArrow.png', 'SS_RightArrow.png']

        # the strings are multiplied so that you end up with a list of strings. Each string appears half of the time
        self.piclist = sum([[s] * n for s, n in zip(picturenames, multiplier)], [])

        # copy the original picture list to get a new order for the block
        self.picorder = list(self.piclist)

        # shuffle the new order
        random.shuffle(self.picorder)

    def nextround(self, blocks):
        """
        Called to get the text prompt for the next block
        :param blocks: an integer for the block that was just completed
        :return:
        """

        # if all of the blocks have been completed, thank the participant
        if blocks == self.blocks:

            prompt = 'Thank you! This task is complete.'

        # if there are still blocks to be completed...
        else:

            # copy the original picture list to get a new order for the block
            self.picorder = list(self.piclist)

            # shuffle the new order
            random.shuffle(self.picorder)

            # tell the participant to wait for instructions
            prompt = 'Please wait for the researcher to read you the instructions.'

        # return the prompt
        return prompt

    def get_trial_pic(self):
        """
        Pop a picture name from the overall order
        :return: the picture that was popped
        """

        pic = self.picorder.pop()

        return pic

    def set_timer(self, signal, correct):
        """
        adjusts the timer for when the signal occurs depending on the performance of the participant on signal trials
        :param signal: binary, with 1 indicating that it was a signal trial
        :param correct: binary, with 1 indicating that the participant was correct or not
        :return:
        """

        # if the last trial was a signal trial
        if signal == 1:

            # if the participant correctly did not respond, then make the timer go off later
            if correct == 1:

                self.timer += 50

            # if the participant responded when they shouldn't have, then make the timer go off earlier
            else:

                self.timer -= 50

        # randomly choose and integer for whether the signal timer will be additionally incremented or decremented (or
        # stay the same)
        choose = random.randint(1, 3)

        # randomly choose an integer between 1 and 9 (inclusive) to make an adjustment
        incdec = random.randint(1, 9)

        # if the first random integer was 1, then add the second random integer to the timer, making it later
        if choose == 1:

            self.timer += incdec

        # if the first random integer was 2, then subtract the second random integer from the timer, making it earlier
        elif choose == 2:

            self.timer -= incdec

        # if the timer is ever less than 10 milliseconds, set it back to 10
        if self.timer < 10:

            self.timer = 10

        # if the timer is ever greater than the user-determined max, then set it back to that
        elif self.timer > self.maxrt:

            self.timer = self.maxrt

    def get_timer(self):
        """
        get the timer value and return it
        :return: int value for the timer
        """

        time = self.timer

        return time

    def updateoutput(self, trial, pic, onset, time, signal, response=3):
        """
        evaluates whether the person responded correctly and records the stats
        :param trial: the number of the trial that was just completed
        :param pic: string with the picture name in it, so we can see if the participants gave the correct answer
        :param onset: onset time for the trial
        :param time: participants's reaction time
        :param signal: boolean; did this trial have a stop signal?
        :param response: integer with either 0 or 1 depending on if the person chose left or right. Default is 3 in case
        the participants doesn't answer in time.
        :return: updates the performance dataframe in the superclass
        """

        # default is that the participant is not correct
        correct = 0

        # if this was a signal trial..
        if signal == 1:

            # if the participant did not respond, they are correct
            if response == 3:
                correct = 1

        # if this was not a signal trial
        else:

            # if there was a left arrow
            if pic == ['SS_LeftArrow.png']:

                # if the participant said it was left, they are correct
                if response == 0:
                    correct = 1

            # if there was a right arrow...
            else:

                # if the participant said it was right, they are correct
                if response == 1:
                    correct = 1

        # strip the extra stuff off of the picture string
        picstripped = pic.removeprefix('SS_').removesuffix('Arrow.png')

        # make a dictionary of trial info
        df_trial = {
            'trial': [trial],
            'signal': [signal],
            'signal timer': [self.timer],
            'left or right': [picstripped],
            'onset': [onset],
            'response': [response],
            'reaction time': [time],
            'correct': [correct]
        }

        # turn that dictionary into a dataframe and use set_performance to add it to the overall dataframe
        df_trial = pd.DataFrame(data=df_trial)
        self.set_performance(df_trial)

        # call the set_timer function to adjust the signal timer based on the participant's performance
        self.set_timer(signal, correct)

    def get_instructions(self, instint):
        """
        Takes in an int and returns the appropriate instructions string
        :param instint: an int that is supplied and incremented by the expguis
        :return: a string containing the appropriate instructions that the expguis puts up
        """

        match instint:

            case 1:

                inst = 'In this task, you will respond to white arrows that\nappear on the screen.'

            case 2:

                inst = 'Press the \"' + self.leftkey[0] + '\" key when you see a LEFT arrow and\npress the \"' + \
                       self.rightkey[0] + '\" key when you see a RIGHT arrow.'

            case 3:

                inst = '\"' + self.leftkey[0] + '\" = LEFT arrow; \"' + self.rightkey[0] + '\" = RIGHT arrow.'

            case 4:

                inst = 'However, on some trials (signal trials), the\narrow will become blue after a delay.'

            case 5:

                inst = 'This blue signal means that you should not respond\nto the arrow.'

            case 6:

                inst = 'In around half of the trials that use the blue signal,\nthe arrow will become blue quickly' \
                       ' and it will be\neasier to stop yourself.'

            case 7:

                inst = 'In the other half of the trials that use the blue\nsignal, the arrow will become blue later' \
                       ' and it will be\nharder (or impossible) to stop yourself.'

            case 8:

                inst = 'Remember: Not every trial will use the blue signal.'

            case 9:

                inst = 'It is also really important that you do not wait\nfor the blue signal to happen. We want ' \
                       'you to\nrespond as quickly and as accurately as possible to the arrows'

            case 10:

                inst = 'After all, if you wait for the blue signal to occur,\nthe program will delay the ' \
                       'presentation of the arrow\nand you will perform worse on the trials without\nthe signal.'

            case _:

                inst = 'Let the experimenter know when you are ready.'

        return inst


class EGNGParticipant(participant.Participant):

    def __init__(self, expid, trials, session, outdir, task, blocks, happy, sad, angry, fear, buttonbox,
                 eyetracking):
        super().__init__(expid, trials, session, outdir, task, buttonbox, eyetracking)

        # set how many blocks are needed and set the blocks done to 0
        self.blocks = int(blocks)
        self.blocksdone = 0

        # make an empty list for the blocks
        self.structlist = []

        # each of the following if statements checks to see if the user checks any of these emotions. If so, it adds the
        # emotion and the reverse round to the block structure
        if happy == 'Yes':
            self.structlist.append('Happy')
            self.structlist.append('HappyRev')

        if sad == 'Yes':
            self.structlist.append('Sad')
            self.structlist.append('SadRev')

        if angry == 'Yes':
            self.structlist.append('Angry')
            self.structlist.append('AngryRev')

        if fear == 'Yes':
            self.structlist.append('Fearful')
            self.structlist.append('FearfulRev')

        # copy the original list to get an order for the task
        self.blocktypes = list(self.structlist)

        # shuffle the order
        random.shuffle(self.blocktypes)

        # Experiment settingsguis output dataframe
        dict_tasksettings = {
            'Blocks': [blocks],
            'Faces': [self.structlist]
        }

        # attach the task-specific settings to the task general settings
        self.set_settings(dict_tasksettings)

    def set_structure(self, block):
        """
        Takes in a string to describe the block about to occur and then sets up a list of strings
        :param block: a string for the block type that is about to occur
        :return:
        """

        # there will always be neutral pictures in the blocks
        self.piclist = ['EGNG_Neutral_']

        # find out which block is occuring...
        match block:

            # when you find the block type...
            case 'Happy':

                # add those types of pictures to the list of pictures...
                self.piclist.append('EGNG_Happy_')

                # for emotion blocks, set the neutral number to a fourth of the trials; reverse, do the opposite
                neutralnum = int(self.get_trials()/4)

                # whatever set of trials were divided by 4, subtract them from the total trials and that is the other
                # set of trials
                emonum = self.get_trials()-neutralnum

            case 'HappyRev':
                self.piclist.append('EGNG_Happy_')
                emonum = int(self.get_trials()/4)
                neutralnum = self.get_trials()-emonum

            case 'Sad':
                self.piclist.append('EGNG_Sad_')
                neutralnum = int(self.get_trials()/4)
                emonum = self.get_trials()-neutralnum

            case 'SadRev':
                self.piclist.append('EGNG_Sad_')
                emonum = int(self.get_trials()/4)
                neutralnum = self.get_trials()-emonum

            case 'Angry':
                self.piclist.append('EGNG_Angry_')
                neutralnum = int(self.get_trials()/4)
                emonum = self.get_trials()-neutralnum

            case 'AngryRev':
                self.piclist.append('EGNG_Angry_')
                emonum = int(self.get_trials()/4)
                neutralnum = self.get_trials()-emonum

            case 'Fearful':
                self.piclist.append('EGNG_Fearful_')
                neutralnum = int(self.get_trials()/4)
                emonum = self.get_trials()-neutralnum

            case _:
                self.piclist.append('EGNG_Fearful_')
                emonum = int(self.get_trials()/4)
                neutralnum = self.get_trials()-emonum

        # set a list of integers for the number of trials that the neutral pictures and emotional pictures will get
        multiplier = [neutralnum, emonum]

        # the strings are multiplied so that you end up with a list of strings. Depending on the type of block, one type
        # of pictures will appear 3/4 of the time; the other, 1/4 of the time
        self.piclist = sum([[s] * n for s, n in zip(self.piclist, multiplier)], [])

        # copy the original picture list to get a new order for the block
        self.picorder = list(self.piclist)

        # shuffle the new order
        random.shuffle(self.picorder)

    def nextround(self):
        """
        Each block is composed of emotional and reversed rounds of trials. This function checks to see if all of those
        rounds have been completed. If not, prompt the user that they will be doing a new round and to focus on a face.
        If so, check to see if all the blocks have been completed. If so, tell the participant that we'll be starting
        again. If not, then thank the partipant
        :return: list: string for participant instruction; integer to tell the gui whether there are still trials to do
        """

        # default is there are still trials to go
        num = 1

        # if there are still rounds to go in this block...
        if len(self.blocktypes) > 0:

            # pop the next round
            self.blocktype = self.blocktypes.pop()

            # set the structure for that round
            self.set_structure(self.blocktype)

            # if the round is a reverse round, then tell the participant to respond only to neutral faces
            if self.blocktype in ['HappyRev', 'SadRev', 'AngryRev', 'FearfulRev']:

                prompt = 'In this round, only respond to \"Neutral\" faces.\nPress \"G\" to start.'

            # if the round is a happy round, then tell the participant to respond only to happy faces
            elif self.blocktype == 'Happy':

                prompt = 'In this round, only respond to \"Happy\" faces.\nPress \"G\" to start.'

            # if the round is a sad round, then tell the participant to respond only to sad faces
            elif self.blocktype == 'Sad':

                prompt = 'In this round, only respond to \"Sad\" faces.\nPress \"G\" to start.'

            # if the round is a angry round, then tell the participant to respond only to angry faces
            elif self.blocktype == 'Angry':

                prompt = 'In this round, only respond to \"Angry\" faces.\nPress \"G\" to start.'

            # if the round is a fearful round, then tell the participant to respond only to fearful faces
            else:

                prompt = 'In this round, only respond to \"Fearful\" faces.\nPress \"G\" to start.'

        # if all rounds in this block are done...
        else:

            # increment the block counter
            self.blocksdone += 1

            # if all blocks requested have been completed, thank the participant
            if self.blocksdone == self.blocks:

                prompt = 'Thank you! This task is complete.'

            # if there are still more blocks to go...
            else:

                # copy the list of rounds to a new list of rounds and then shuffle it
                self.blocktypes = list(self.structlist)
                random.shuffle(self.blocktypes)

                # tell the participant that another block is starting
                prompt = 'You will now repeat the task you just completed.\nPress \"G\".'

                # set the binary value to 0 so the participant sees the instructions and has to press G once to move to
                # the start screen and once to start the trial
                num = 0

        # make a list composed of the prompt string and the binary value
        promptlist = [prompt, num]

        # return the list
        return promptlist

    def get_trial_pic(self):
        """
        Pop a picture name from the overall order
        :return: the picture that was popped
        """

        pic = self.picorder.pop()

        return pic

    def updateoutput(self, trial, pic, onset, time, response=0):
        """
        evaluates whether the person responded correctly, records the stats, and updates the performance dataframe
        in the superclass
        :param trial: the number of the trial that was just completed
        :param pic: string with the picture name in it, so we can see if the participants gave the correct answer
        :param onset: onset time for the trial
        :param time: participants's reaction time
        :param response: integer with either 0 or 1 depending on if the person chose left or right. Default is 3 in case
        the participants doesn't answer in time.
        """

        # default is that the participant is not correct
        correct = 0

        # if the round was a reverse round...
        if self.blocktype in ['HappyRev', 'SadRev', 'AngryRev', 'FearfulRev']:

            # if the picture was a neutral one...
            if 'EGNG_Neutral_' in pic:

                # if the participant did respond, they are correct
                if response == 1:
                    correct = 1

            # if the picture was an emotional one..
            else:

                # if the participant did not respond, they are correct
                if response == 0:
                    correct = 1

        # if the round was a Happy round...
        elif self.blocktype == 'Happy':

            # if the picture was a Happy one...
            if 'EGNG_Happy_' in pic:

                # if the participant did respond, they are correct
                if response == 1:
                    correct = 1

            # if the picture was a neutral one...
            else:

                # if the participant did not respond, they are correct
                if response == 0:
                    correct = 1

        # if the round was a Sad round...
        elif self.blocktype == 'Sad':

            # if the picture was a Sad one...
            if 'EGNG_Sad_' in pic:

                # if the participant did respond, they are correct
                if response == 1:
                    correct = 1

            # if the picture was a neutral one...
            else:

                # if the participant did not respond, they are correct
                if response == 0:
                    correct = 1

        # if the round was an Angry round...
        elif self.blocktype == 'Angry':

            # if the picture was an Angry one...
            if 'EGNG_Angry_' in pic:

                # if the participant did respond, they are correct
                if response == 1:
                    correct = 1

            # if the picture was a neutral one...
            else:

                # if the participant did not respond, they are correct
                if response == 0:
                    correct = 1

        # if the round was a Fearful round...
        else:

            # if the picture was a Fearful one...
            if pic == 'EGNG_Fearful_':

                # if the participant did respond, they are correct
                if response == 1:
                    correct = 1

            # if the picture was a neutral one...
            else:

                # if the participant did not respond, they are correct
                if response == 0:
                    correct = 1

        # strip the extra junk off of the picture string
        picstripped = pic.removeprefix('EGNG_')

        # make a dictionary of trial info
        df_trial = {
            'trial': [trial],
            'block type': [self.blocktype],
            'picture': [picstripped],
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

                inst = 'In this task, you will respond to faces that\nappear on the screen.'

            case 2:

                inst = 'Each round, you will only respond to one type\nof face.'

            case 3:

                inst = '\"' + self.leftkey[0] + '\" when you see that\ntype of face.'

            case 4:

                inst = 'Other types of faces may appear, but only respond\nto the type you are told to respond to.'

            case 5:

                inst = 'Be sure to respond as quickly as possible.'

            case _:

                inst = 'Let the experimenter know when you are ready.'

        return inst


class GNGParticipant(participant.Participant):

    def __init__(self, expid, trials, session, outdir, task, blocks, buttonbox, eyetracking):
        super().__init__(expid, trials, session, outdir, task, buttonbox, eyetracking)

        # set how many blocks are needed and set the blocks done to 0
        self.blocks = int(blocks)
        self.blocksdone = 0

        # make an empty list for the blocks
        self.structlist = ['A', 'Z']

        # copy the original list to get an order for the task
        self.blocktypes = list(self.structlist)

        # shuffle the order
        random.shuffle(self.blocktypes)

        # Experiment settingsguis output dataframe
        dict_tasksettings = {
            'Blocks': [blocks],
            'Signals': [self.structlist]
        }

        # attach the task-specific settings to the task general settings
        self.set_settings(dict_tasksettings)

    def set_structure(self, block):
        """
        Takes in a string to describe the block about to occur and then sets up a list of strings
        :param block: a string for the block type that is about to occur
        :return:
        """

        # list the type of trials
        self.siglist = ['A', 'Z']

        # find out which block is occuring...
        match block:

            # when you find the block type...
            case 'A':

                # for A blocks, set the neutral number to a fourth of the trials; reverse, do the opposite
                a_num = int(self.get_trials()/4)

                # whatever set of trials were divided by 4, subtract them from the total trials and that is the other
                # set of trials
                z_num = self.get_trials()-a_num

            case _:

                z_num = int(self.get_trials()/4)
                a_num = self.get_trials()-z_num

        # set a list of integers for the number of trials that the neutral pictures and emotional pictures will get
        multiplier = [a_num, z_num]

        # the strings are multiplied so that you end up with a list of strings. Depending on the type of block, one type
        # of signal will appear 3/4 of the time; the other, 1/4 of the time
        self.siglist = sum([[s] * n for s, n in zip(self.siglist, multiplier)], [])

        # copy the original signal list to get a new order for the block
        self.sigorder = list(self.siglist)

        # shuffle the new order
        random.shuffle(self.sigorder)

    def nextround(self):
        """
        Each block is composed of A and Z rounds of trials. This function checks to see if all rounds have been
        completed. If not, prompt the user that they will be doing a new round and what to focus on. If so, check to
        see if all the blocks have been completed. If so, tell the participant that we'll be starting again. If not,
        then thank the partipant.
        :return: list: string for participant instruction; integer to tell the gui whether there are still trials to do
        """

        # default is there are still trials to go
        num = 1

        # if there are still rounds to go in this block...
        if len(self.blocktypes) > 0:

            # pop the next round
            self.blocktype = self.blocktypes.pop()

            # set the structure for that round
            self.set_structure(self.blocktype)

            # if the round is an A round, then tell the participant to respond only to A's
            if self.blocktype == 'A':

                prompt = 'In this round, only respond to \"A\" signals.\nPress \"G\" to start.'

            # if the round is a Z round, then tell the participant to respond only to Z's
            else:

                prompt = 'In this round, only respond to \"Z\" signals.\nPress \"G\" to start.'

        # if all rounds in this block are done...
        else:

            # increment the block counter
            self.blocksdone += 1

            # if all blocks requested have been completed, thank the participant
            if self.blocksdone == self.blocks:

                prompt = 'Thank you! This task is complete.'

            # if there are still more blocks to go...
            else:

                # copy the list of rounds to a new list of rounds and then shuffle it
                self.blocktypes = list(self.structlist)
                random.shuffle(self.blocktypes)

                # tell the participant that another block is starting
                prompt = 'You will now repeat the task you just completed.\nPress \"G\".'

                # set the binary value to 0 so the participant sees the instructions and has to press G once to move to
                # the start screen and once to start the trial
                num = 0

        # make a list composed of the prompt string and the binary value
        promptlist = [prompt, num]

        # return the list
        return promptlist

    def get_trial_pic(self):
        """
        Pop a picture name from the overall order
        :return: the picture that was popped
        """

        sig = self.sigorder.pop()

        return sig

    def updateoutput(self, trial, sig, onset, time, response=0):
        """
        evaluates whether the person responded correctly, records the stats, and updates the performance dataframe
        in the superclass
        :param trial: the number of the trial that was just completed
        :param sig: string with the signal  in it, so we can see if the participants gave the correct answer
        :param onset: onset time for the trial
        :param time: participants's reaction time
        :param response: integer with either 0 or 1 depending on if the person chose left or right. Default is 3 in case
        the participants doesn't answer in time.
        """

        # default is that the participant is not correct
        correct = 0

        # if the round was an A round...
        if self.blocktype == 'A':

            # if the signal was A...
            if sig == 'A':

                # if the participant did respond, they are correct
                if response == 1:
                    correct = 1

            # if the signal was Z..
            else:

                # if the participant did not respond, they are correct
                if response == 0:
                    correct = 1

        # if the round was a Z round...
        else:

            # if the signal was Z...
            if sig == 'Z':

                # if the participant did respond, they are correct
                if response == 1:
                    correct = 1

            # if the signal was A...
            else:

                # if the participant did not respond, they are correct
                if response == 0:
                    correct = 1

        # make a dictionary of trial info
        df_trial = {
            'trial': [trial],
            'block type': [self.blocktype],
            'signal': [sig],
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

                inst = 'In this task, you will respond to letters that\nappear on the screen.'

            case 2:

                inst = 'Each round, you will only respond to one type\nof letter.'

            case 3:

                inst = '\"' + self.leftkey[0] + '\" when you see that\ntype of letter.'

            case 4:

                inst = 'Other types of letters may appear, but only respond\nto the type you are told to respond to.'

            case 5:

                inst = 'Be sure to respond as quickly as possible.'

            case _:

                inst = 'Let the experimenter know when you are ready.'

        return inst
