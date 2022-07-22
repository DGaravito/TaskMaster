from Participants import participant

import pandas as pd
import random


class PBTParticipant(participant.Participant):

    def __init__(self, expid, trials, session, outdir, task, rounds, buttonbox, eyetracking):
        super().__init__(expid, trials, session, outdir, task, buttonbox, eyetracking)

        # number of rounds equals what the user put in
        self.rounds = int(rounds)

        # pic whether the starting block is global or local
        self.globallocal = random.choice(['Global', 'Local'])

        # call the set_design function with the number of low and high trials
        self.set_design(trials)

        # Experiment settingsguis output dataframe
        dict_simulsettings = {
            'Rounds': [rounds],
            'Starting Block': [self.globallocal]
        }

        # send the task-specific dictionary to be added to the generic task settings
        self.set_settings(dict_simulsettings)

    def set_design(self, trials):
        """
        takes in the number of trials and creates a list of strings that is then randomized so that you get the final
        order
        :param trials: integer that is the number of trials
        """

        # divide the number of trials by 4 because there are 4 types of pictures
        multnum = int(int(trials)/4)

        # list composed of 4 integers which are one quarter of the total trials
        multiplier = [multnum, multnum, multnum, multnum]

        # list composed of the 4 strings, one for each picture
        picturenames = ['PBT_DCC.png', 'PBT_DCS.png', 'PBT_DSC.png', 'PBT_DSS.png']

        # the strings are multiplied so that you end up with a list of strings. Each picture appears one quarter of the
        # trials
        self.piclist = sum([[s] * n for s, n in zip(picturenames, multiplier)], [])

        # copy this list to a new variable so that it can be copied again in the future
        self.picorder = list(self.piclist)

        # randomize the order of things in the list
        random.shuffle(self.picorder)

    def nextround(self, blocks):
        """
        takes the block that was completed and returns the appropriate prompt depending on if that was the last trial or
        if there are more to do
        :param blocks: an integer for the block that was just completed
        :return: the prompt for the participant
        """

        # if all the requested blocks were completed, thank the participant
        if blocks == self.rounds:

            prompt = 'Thank you! This task is complete.'

        # if there are still more blocks to do...
        else:

            # set the trial order to the list of pictures
            self.picorder = list(self.piclist)

            # randomize the order
            random.shuffle(self.picorder)

            # if this is not the first block...
            if blocks > 0:

                # then flip the block type to global or local depending on what the last one was
                if self.globallocal == 'Global':

                    self.globallocal = 'Local'

                else:

                    self.globallocal = 'Global'

            # set the prompt to participant instructions
            prompt = 'Please wait for the researcher to read you the instructions'

        # return the prompt
        return prompt

    def get_trial_pic(self):
        """
        Pop a picture name from the overall order
        :return: the picture that was popped
        """

        pic = self.picorder.pop()

        return pic

    def updateoutput(self, trial, pic, onset, time, response=3):
        """
        evaluates whether the person got the trial correct based on their response
        :param trial: the number of the trial that was just completed
        :param pic: string with the picture name in it, so we can see if the participants gave the correct answer
        :param onset: onset time for the trial
        :param time: participants's reaction time
        :param response: integer with either 0 or 1 depending on if the person chose x or square. Default is 3 in case
        the participants doesn't answer in time.
        :return: updates the performance dataframe in the superclass
        """

        # participant is incorrect by default
        correct = 0

        # if the block was a local one
        if self.globallocal == 'Local':

            # if the larger figure was made of squares
            if pic in ['PBT_DCS.BMP', 'PBT_DSS.BMP']:

                # if the participant responded square then they are correct
                if response == 'Square':
                    correct = 1

            # if the larger figure was made of crosses
            else:

                # if the participant responded cross then they are correct
                if response == 'Cross':
                    correct = 1

        # if the block was a global one
        else:

            # if the larger figure was a square
            if pic in ['PBT_DSS.BMP', 'PBT_DSC.BMP']:

                # if the participant responded square then they are correct
                if response == 'Square':
                    correct = 1

            # if the larger figure was a cross
            else:

                # if the participant responded cross then they are correct
                if response == 'Cross':
                    correct = 1

        # make a dictionary of trial info
        df_simultrial = {
            'trial': [trial],
            'block': [self.globallocal],
            'picture': [pic],
            'onset': [onset],
            'response': [response],
            'reaction time': [time],
            'correct': [correct]
        }

        # set the dictionary to a dataframe and use set_performance to attach it to previous trial dataframes
        df_simultrial = pd.DataFrame(data=df_simultrial)
        self.set_performance(df_simultrial)

    def get_instructions(self, block_type, instint):
        """
        Takes in an int and returns the appropriate instructions string
        :param block_type: a string that indicates whether the upcoming block is a global or local one so that the
        instructions match
        :param instint: an int that is supplied and incremented by the expguis
        :return: a string containing the appropriate instructions that the expguis puts up
        """

        # if the user is looking at the first two instructions, then the type of block doesn't matter
        if instint <= 2:

            match instint:

                case 1:

                    inst = 'A large figure made of small pieces will be shown on\nevery trial.'

                case _:

                    inst = 'For example, a large square made of small crosses.'

        # after the first two instructions, the specific instructions depends on the type of block
        else:

            # if the upcoming block is global, print these instructions
            if block_type == 'Global':

                match instint:

                    case 3:

                        inst = 'Your task is to decide whether the LARGE figure\nis a square or cross.'

                    case 4:

                        inst = 'Ignore the small elements. Press \"' + self.rightkey[0] + \
                               '\" if the\nlarge figure is a SQUARE and \"' + self.leftkey[0] + \
                               '\" if the large figure\nis a CROSS.'

                    case 5:

                        inst = 'Continue for an example picture.'

                    case 7:

                        inst = 'There, the large figure was a SQUARE,\nso you would press \"' + self.rightkey[0] + '\".'

                    case 8:

                        inst = 'Continue for another example.'

                    case 10:

                        inst = 'There, the large figure was a CROSS,\nso you would press \"' + self.leftkey[0] + '\".'

                    case _:

                        inst = 'Please let the experimenter know\nwhen you are ready.'

            # if the upcoming block is local, print these instructions
            else:

                match instint:

                    case 3:

                        inst = 'Your task is to decide whether the SMALL figure\nis a square or cross.'

                    case 4:

                        inst = 'Ignore the small elements. Press \"' + self.rightkey[0] + \
                               '\" if the\nsmall figure is a SQUARE and \"' + self.leftkey[0] + \
                               '\" if the small figure\nis a CROSS.'

                    case 5:

                        inst = 'Continue for an example picture.'

                    case 7:

                        inst = 'There, the small figure was a CROSS,\nso you would press \"' + self.leftkey[0] + '\".'

                    case 8:

                        inst = 'Continue for another example.'

                    case 10:

                        inst = 'There, the small figure was a SQUARE,\nso you would press \"' + self.rightkey[0] + '\".'

                    case _:

                        inst = 'Please let the experimenter know\nwhen you are ready.'

        return inst
