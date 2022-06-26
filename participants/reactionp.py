from participants import participant

import pandas as pd
import random


class SSParticipant(participant.Participant):

    def __init__(self, expid, trials, session, outdir, task, maxrt, blocks, buttonbox, eyetracking):
        super().__init__(expid, trials, session, outdir, task, buttonbox, eyetracking)

        self.blocks = int(blocks)
        self.timer = 250
        self.globallocal = random.choice(['Global', 'Local'])
        self.maxrt = int(maxrt)

        self.set_structure()

        # Experiment settingsguis output dataframe
        dict_simulsettings = {
            'Blocks': [blocks],
            'Max reaction time': [maxrt]
        }

        self.set_settings(dict_simulsettings)

    def set_structure(self):
        multnum = int((self.get_trials() / 2) * self.blocks)
        picturenames = ['SS_LeftArrow.png', 'SS_RightArrow.png']
        multiplier = [multnum, multnum]
        self.piclist = sum([[s] * n for s, n in zip(picturenames, multiplier)], [])

        self.picorder = list(self.piclist)
        random.shuffle(self.picorder)

    def nextround(self, blocks):

        if blocks == self.blocks:

            prompt = 'Thank you! This task is complete.'

        else:

            self.picorder = list(self.piclist)
            random.shuffle(self.picorder)

            prompt = 'Please wait for the researcher to read you the instructions'

        return prompt

    def get_trial_pic(self):

        pic = self.picorder.pop()

        return pic

    def set_timer(self, signal, correct):

        if signal == 1:

            if correct == 1:

                self.timer += 50

            else:

                self.timer -= 50

        else:

            choose = random.randint(1, 3)
            incdec = random.randint(1, 9)

            if choose == 1:

                self.timer += incdec

            elif choose == 2:

                self.timer -= incdec

        if self.timer < 10:

            self.timer = 10

        elif self.timer > self.maxrt:

            self.timer = self.maxrt

    def get_timer(self):

        time = self.timer

        return time

    def updateoutput(self, trial, pic, onset, time, signal=0, response=0):
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

        if signal == 1:

            if response == 0:
                correct = 1

            else:
                correct = 0

        else:

            if pic == ['SS_LeftArrow.png']:

                if response == 1:
                    correct = 1

                else:
                    correct = 0

            else:

                if response == 2:
                    correct = 1

                else:
                    correct = 0

        picstripped = pic.removeprefix('SS_').removesuffix('Arrow.png')

        df_simultrial = {
            'trial': [trial],
            'signal': [signal],
            'signal timer': [self.timer],
            'left or right': [picstripped],
            'onset': [onset],
            'response': [response],
            'reaction time': [time],
            'correct': [correct]
        }

        df_simultrial = pd.DataFrame(data=df_simultrial)

        self.set_performance(df_simultrial)
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

        self.blocks = int(blocks)

        self.structlist = []

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

        self.blocktypes = list(self.structlist)
        random.shuffle(self.blocktypes)

        # Experiment settingsguis output dataframe
        dict_simulsettings = {
            'Blocks': [blocks],
            'Faces': [self.structlist]
        }

        self.set_settings(dict_simulsettings)

    def set_structure(self, block):

        self.piclist = ['EGNG_Neutral_']

        if block in ['Happy', 'Happy']:
            self.piclist.append('EGNG_Happy_')

        elif block in ['Sad', 'SadRev']:
            self.piclist.append('EGNG_Sad_')

        elif block in ['Angry', 'AngryRev']:
            self.piclist.append('EGNG_Angry_')

        else:
            self.piclist.append('EGNG_Fearful_')

        multnum = int(self.get_trials()/2)
        multiplier = [multnum, multnum]

        self.piclist = sum([[s] * n for s, n in zip(self.piclist, multiplier)], [])

        self.picorder = list(self.piclist)
        random.shuffle(self.picorder)

    def nextround(self):

        self.blocktype = self.blocktypes.pop()
        self.set_structure(self.blocktype)

        if self.blocktype in ['HappyRev', 'SadRev', 'AngryRev', 'FearfulRev']:

            prompt = 'In this round, only respond to \"Neutral\" faces.\nPress \"G\" to start.'

        elif self.blocktype == 'Happy':

            prompt = 'In this round, only respond to \"Happy\" faces.\nPress \"G\" to start.'

        elif self.blocktype == 'Sad':

            prompt = 'In this round, only respond to \"Sad\" faces.\nPress \"G\" to start.'

        elif self.blocktype == 'Angry':

            prompt = 'In this round, only respond to \"Angry\" faces.\nPress \"G\" to start.'

        else:

            prompt = 'In this round, only respond to \"Fearful\" faces.\nPress \"G\" to start.'

        return prompt

    def nextset(self, blocks):

        if blocks == self.blocks:

            prompt = 'Thank you! This task is complete.'

        else:

            self.blocktypes = list(self.structlist)
            random.shuffle(self.blocktypes)

            prompt = 'You will now repeat the task you just completed.'

        return prompt

    def get_trial_pic(self):

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

        if self.blocktype in ['HappyRev', 'SadRev', 'AngryRev', 'FearfulRev']:

            if 'EGNG_Neutral_' in pic:

                if response == 1:
                    correct = 1

                else:
                    correct = 0

            else:

                if response == 0:
                    correct = 1

                else:
                    correct = 0

        elif self.blocktype == 'Happy':

            if 'EGNG_Happy_' in pic:

                if response == 1:
                    correct = 1

                else:
                    correct = 0

            else:

                if response == 0:
                    correct = 1

                else:
                    correct = 0

        elif self.blocktype == 'Sad':

            if 'EGNG_Sad_' in pic:

                if response == 1:
                    correct = 1

                else:
                    correct = 0

            else:

                if response == 0:
                    correct = 1

                else:
                    correct = 0

        elif self.blocktype == 'Angry':

            if 'EGNG_Angry_' in pic:

                if response == 1:
                    correct = 1

                else:
                    correct = 0

            else:

                if response == 0:
                    correct = 1

                else:
                    correct = 0

        else:

            if pic == 'EGNG_Fearful_':

                if response == 1:
                    correct = 1

                else:
                    correct = 0

            else:

                if response == 0:
                    correct = 1

                else:
                    correct = 0

        picstripped = pic.removeprefix('EGNG_')

        df_simultrial = {
            'trial': [trial],
            'block type': [self.blocktype],
            'picture': [picstripped],
            'onset': [onset],
            'response': [response],
            'reaction time': [time],
            'correct': [correct]
        }

        df_simultrial = pd.DataFrame(data=df_simultrial)

        self.set_performance(df_simultrial)

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