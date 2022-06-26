from participants import participant

import pandas as pd
import random


class PBTParticipant(participant.Participant):

    def __init__(self, expid, trials, session, outdir, task, rounds, buttonbox, eyetracking):
        super().__init__(expid, trials, session, outdir, task, buttonbox, eyetracking)

        self.rounds = int(rounds)
        self.globallocal = random.choice(['Global', 'Local'])

        multnum = int(int(trials)/4)
        picturenames = ['PBT_DCC.BMP', 'PBT_DCS.BMP', 'PBT_DSC.BMP', 'PBT_DSS.BMP']
        multiplier = [multnum, multnum, multnum, multnum]
        self.piclist = sum([[s] * n for s, n in zip(picturenames, multiplier)], [])

        self.picorder = list(self.piclist)
        random.shuffle(self.picorder)

        # Experiment settingsguis output dataframe
        dict_simulsettings = {
            'Rounds': [rounds],
            'Starting Block': [self.globallocal]
        }

        self.set_settings(dict_simulsettings)

    def nextround(self, blocks):

        if blocks == self.rounds:

            prompt = 'Thank you! This task is complete.'

        else:

            self.picorder = list(self.piclist)
            random.shuffle(self.picorder)

            if blocks > 0:

                if self.globallocal == 'Global':

                    self.globallocal = 'Local'

                else:

                    self.globallocal = 'Global'

            prompt = 'Please wait for the researcher to read you the instructions'

        return prompt

    def get_trial_pic(self):

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

        if self.globallocal == 'Local':

            if pic in ['PBT_DCS.BMP', 'PBT_DSS.BMP']:

                if response == 'Square':
                    correct = 1

                else:
                    correct = 0

            else:

                if response == 'Cross':
                    correct = 1

                else:
                    correct = 0

        else:

            if pic in ['PBT_DSS.BMP', 'PBT_DSC.BMP']:

                if response == 'Square':
                    correct = 1

                else:
                    correct = 0

            else:

                if response == 'Cross':
                    correct = 1

                else:
                    correct = 0

        df_simultrial = {
            'trial': [trial],
            'block': [self.globallocal],
            'picture': [pic],
            'onset': [onset],
            'response': [response],
            'reaction time': [time],
            'correct': [correct]
        }

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

        if instint <= 2:

            match instint:

                case 1:

                    inst = 'A large figure made of small pieces will be shown on\nevery trial.'

                case _:

                    inst = 'For example, a large square made of small crosses.'

        else:

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
