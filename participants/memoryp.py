from participants import participant

import pandas as pd
import random
import string


class PrParticipant(participant.Participant):

    def __init__(self, expid, trials, outdir, task, design, stt):
        super().__init__(expid, trials, outdir, task)

        design = design
        stt = stt

        if stt == 1:
            structstr = 'STT' + ('ST' * (int(design) - 1))
            self.structure = list(structstr)

        else:
            structstr = 'ST' * int(design)
            self.structure = list(structstr)

        # Experiment settingsguis output dataframe
        dict_simulsettings = {
            'Design': [structstr]
        }

        self.set_settings(dict_simulsettings)

        self.set_pairs(int(trials))

    def set_pairs(self, trials):

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

        if len(originalpairs) - trials != 0:

            for n in range(len(originalpairs) - trials):

                del originalpairs[next(iter(originalpairs))]

        self.expwordpairs = dict(originalpairs)

        self.trialwordpairs = dict(self.expwordpairs)

        self.updateoutput()

    def starttrial(self):

        self.trialwordpairs = dict(self.expwordpairs)

        prompt = 'Please let the researcher know you are ready'

        return prompt

    def get_design_text(self, test=0):

        if test == 0:

            leftstring, rightstring = random.choice(list(self.trialwordpairs.items()))

            rightstring = rightstring[0]

        else:

            leftstring = random.choice(list(self.trialwordpairs))

            rightstring = ''

        del self.trialwordpairs[leftstring]

        middlestring = ''

        return [leftstring, rightstring, middlestring]

    def updateoutput(self):

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

    def __init__(self, expid, trials, outdir, task, rounds, buttonbox):

        super().__init__(expid, trials, outdir, task)

        self.buttonbox = buttonbox
        self.roundperformance = 0.0
        self.roundsumcorrect = 0
        self.rounds = int(rounds)
        self.backlist = ['1', '1', '1', '1']

        # Experiment settingsguis output dataframe
        dict_simulsettings = {
            'Rounds': [rounds]
        }

        self.set_settings(dict_simulsettings)

    def nextround(self, roundsdone):

        self.roundperformance = self.roundsumcorrect/self.get_trials()

        if (roundsdone == self.rounds) & (self.roundperformance >= 0.5):

            prompt2 = 'Thank you! This task is complete.'
            prompt1 = 'You got ' + str('{:.1f}'.format(self.roundperformance)) + '% correct.'

        else:

            self.backlist = ['1', '1', '1', '1']

            if self.roundperformance >= 0.5:
                prompt1 = 'You got ' + str('{:.1f}'.format((self.roundperformance*100))) + '% correct.'

            else:
                prompt1 = 'You got ' + str('{:.1f}'.format(self.roundperformance)) + '% correct. Please try harder.'

            prompt2 = 'Please let the researcher know you are ready'

        prompts = [prompt1, prompt2]

        self.roundperformance = 0.0
        self.roundsumcorrect = 0

        return prompts

    def get_trial_text(self):

        while True:
            newletter = random.choice(string.ascii_uppercase)

            if newletter not in ['a', 'e', 'i', 'o', 't', 'u', 'v', 'w', 'x', 'y', 'z']:
                break

        self.backlist.append(newletter)

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

        if self.task == '1-back':

            if response == 1 & (self.backlist[-1] == self.backlist[-2]):
                correct = 1

            elif response == 0 & (self.backlist[-1] != self.backlist[-2]):
                correct = 1

            else:
                correct = 0

        elif self.task == '2-back':

            if response == 1 & (self.backlist[-1] == self.backlist[-3]):
                correct = 1

            elif response == 0 & (self.backlist[-1] != self.backlist[-3]):
                correct = 1

            else:
                correct = 0

        elif self.task == '3-back':

            if response == 1 & (self.backlist[-1] == self.backlist[-4]):
                correct = 1

            elif response == 0 & (self.backlist[-1] != self.backlist[-4]):
                correct = 1

            else:
                correct = 0

        else:

            if response == 1 & (self.backlist[-1] == self.backlist[-5]):
                correct = 1

            elif response == 0 & (self.backlist[-1] != self.backlist[-5]):
                correct = 1

            else:
                correct = 0

        df_simultrial = {
            'trial': [trial],
            'letter': [self.backlist[-1]],
            'onset': [onset],
            'response': [response],
            'reaction time': [time],
            'correct': [correct]
        }

        self.roundsumcorrect += correct

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

                inst = 'You will see a series of letters come up on\nthe screen.'

            case 2:

                inst = 'Each letter will be followed by a plus sign,\nwhich is just a placeholder that you can ignore.'

            case 3:

                inst = 'Your job is to decide whetehr each letter that\ncomes up is a \"target\" or a \"false alarm\".'

            case 4:

                inst = 'If a letter is a target,you will press \"M\"\nwhen it comes up. If it is a false alarm, you' \
                       ' will press \"C\"\nwhen it comes up.'

            case 5:

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

                if self.task == '1-back':

                    inst = 'In this case, you would press \"C\" for the A,\nthen \"C\" for the first B, and then' \
                           ' \"M\" for\nthe second B.'

                elif self.task == '2-back':

                    inst = 'In this case, you would press \"C\" for the A,\nthen \"C\" for the first B, and then' \
                           ' \"M\" for\nthe second A. If a B came next, it would also be\na target.'

                elif self.task == '3-back':

                    inst = 'In this case, you would press \"C\" for the A,\nB and C, and then press \"M\" for the' \
                           ' second A.'

                else:

                    inst = 'In this case, you would press \"C\" for the A,\nB, C, and D, and then press \"M\" for the' \
                           ' second A.'

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
