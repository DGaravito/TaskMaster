from Participants import participant

import pandas as pd
import random


class StroopParticipant(participant.Participant):

    def __init__(self, expid, trials, session, outdir, blocks, eyetracking):
        super().__init__(expid, trials, session, outdir, blocks, eyetracking)

        self.blocklist = ['Consistent', 'Inconsistent']

        # if the user wants multiple blocks...
        if int(blocks)-1 > 0:

            # calculate the number of additional blocks
            additionalblocks = int(blocks)-1

            # make a while loop that adds extra blocks and decrements until you're out of blocks
            while additionalblocks > 0:

                # add the two subblock types
                self.blocklist.append('Consistent')
                self.blocklist.append('Inconsistent')

                # decrement
                additionalblocks -= 1

        # make a blank word list to start
        self.wordlist = []

    def set_pairs(self, trials):
        """
        Sets the list of words
        :param trials: an integer representing how many words the user wants
        """

        # make a list of colors to be used
        colorslist = ['red', 'green', 'yellow', 'blue', 'black', 'orange', 'purple']

        # set a count of the number of trials that were set up to 0
        trialcount = 0

        # while the number of trials set up is less than the number of trials needed...
        while trialcount < trials:

            # randomly choose a color and appeand it to the list of trial colors
            self.wordlist.append(random.choice(colorslist))

            # increment to indicate a trial is set up
            trialcount += 1

    def starttrial(self):
        """
        Set up the color list for the trial, set the blocktype, and tell the participant to start the trial
        :return: string of block type
        """

        # call the set pairs function to create the list of word pairs for all the blocks
        self.set_pairs(self.get_trials())

        # pop the block type for this block
        self.block = self.blocklist.pop()

        # return the block type
        return self.block

    def get_design_text(self):
        """
        A function that gets a wordpair for the trial, returns the info, and then eliminates it from the total
        dictionary
        :return: a string with the word
        """

        # pop a color word from the list
        middlestring = self.wordlist.pop()

        return middlestring

    def updateoutput(self, trial, word, onset):
        """
        this function just makes a dataframe of the word pairs and updates the corresponding existing dataframe
        :return:
        """

        # make dictionary of trial data
        df_trial = {
            'trial': [trial],
            'word': [word],
            'cond': [self.block],
            'onset': [onset]
        }

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

                inst = 'We are going to do a tasks that involves\nreading out colored words.'

            case 2:

                inst = 'I will show you a list of words, and, when\na word appears, say it out loud'

            case 3:

                inst = 'Only say the word, not the color that the text is.'

            case 4:

                inst = 'At first the color of the text and the\nword will be the same.'

            case 5:

                inst = 'Sometimes, the color and word will be different.'

            case 6:

                inst = 'Try to go as fast as you can, and do your best.'

            case _:

                inst = 'Let the experimenter know you are ready.'

        return inst
