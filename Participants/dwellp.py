from Participants import participant

import pandas as pd
import random

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
