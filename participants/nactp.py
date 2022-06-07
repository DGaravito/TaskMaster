from participants import participant

import pandas as pd
import random


class NACTParticipant(participant.Participant):

    def __init__(self, expid, trials, outdir, task, money, buttonbox):
        super().__init__(expid, trials, outdir, task)

        self.highcolor = random.choice(['Green', 'Red'])

        if self.highcolor == 'Green':

            self.lowcolor = 'Red'

        else:

            self.lowcolor = 'Green'

        self.part = 1
        self.startmoney = float(money)
        self.buttonbox = buttonbox

        highvaluetrials = round((self.get_trials()-700)/-4)
        lowvaluetrials = round(700-(highvaluetrials*5))

        self.set_design(highvaluetrials, lowvaluetrials)

        # Experiment settingsguis output dataframe
        dict_simulsettings = {
            'Starting money': [money],
            'Low value trials': [lowvaluetrials],
            'Low value color': [self.lowcolor],
            'High value trials': [highvaluetrials],
            'High value color': [self.highcolor]
        }

        self.set_settings(dict_simulsettings)

    def set_design(self, high, low):

        trialtypes = [self.highcolor, self.lowcolor]
        multiplier = [high, low]
        self.piclist = sum([[s] * n for s, n in zip(trialtypes, multiplier)], [])

        self.picorder = list(self.piclist)
        random.shuffle(self.picorder)

    def nextround(self):

        self.part += 1

        if self.part >= 3:

            prompt = 'Thank you! This task is complete.'

        else:

            self.picorder = list(self.piclist)
            random.shuffle(self.picorder)

            prompt = 'Please wait for the researcher to read you the instructions'

        return prompt

    def get_trial_pic(self):

        colors = ['White', 'Purple', 'Yellow', 'Orange', 'Teal', 'Blue']
        random.shuffle(colors)
        shape = random.choice(['Cir', 'Dia'])

        pics = []

        prefix = 'NACT_'

        signalplace = random.randint(0, 5)

        value = self.picorder.pop()

        if self.part == 1:

            for color in colors:

                distractornumber = str(random.randint(1, 2))

                distractorstring = prefix + 'd' + color + shape + distractornumber
                pics.append(distractorstring)

            random.shuffle(pics)

            signalnumber = str(random.randint(1, 2))

            signalstring = prefix + 's' + value + shape + signalnumber

            pics[signalplace] = signalstring

        else:

            for color in colors:

                distractorletter = random.choice(['s', 'd'])
                distractornumber = str(random.randint(1, 2))

                distractorstring = prefix + distractorletter + color + shape + distractornumber
                pics.append(distractorstring)

            random.shuffle(pics)

            if shape == 'Cir':

                signalshape = 'Dia'

            else:

                signalshape = 'Dia'

            signalnumber = str(random.randint(1, 2))

            self.signalstring = prefix + 's' + value + signalshape + signalnumber

            pics[signalplace] = self.signalstring

        return pics

    def updateoutput(self, trial, onset, rt, response=3):
        """
        evaluates whether the person got the trial correct based on their response, updates the performance dataframe
        in the superclass, and gives feedback
        :param trial: the number of the trial that was just completed
        :param onset: onset time for trial
        :param rt: participants's reaction time
        :param response: integer with either 0 or 1 depending on if the person chose x or square. Default is 3 in case
        the participants doesn't answer in time.
        :return: feedback string: how much money they lost and their total money
        """

        if self.signalstring in ['NACT_sRedCir1', 'NACT_sRedDia1', 'NACT_sGreenCir1', 'NACT_sGreebDia1']:

            if response == '|':
                correct = 1

            else:
                correct = 0

        elif self.signalstring in ['NACT_sRedCir2', 'NACT_sRedDia2', 'NACT_sGreenCir2', 'NACT_sGreebDia2']:

            if response == '-':
                correct = 1

            else:
                correct = 0

        else:

            correct = 0

        df_simultrial = {
            'trial': [trial],
            'onset time': [onset],
            'part': [self.part],
            'picture': [self.signalstring],
            'response': [response],
            'reaction time': [rt],
            'correct': [correct]
        }

        if self.part == 1:

            if correct == 1:

                feedback = 0.0

            elif (correct == 0) & (self.highcolor in self.signalstring):

                feedback = 0.15

            else:

                feedback = 0.03

            self.startmoney -= feedback

            feedbackstring = 'You lost $' + str('{:.2f}'.format(feedback)) + '. You have $' + \
                             str('{:.2f}'.format(self.startmoney)) + ' left.'

        else:

            feedbackstring = '+'

        df_simultrial = pd.DataFrame(data=df_simultrial)

        self.set_performance(df_simultrial)

        return feedbackstring

    def get_instructions(self, instint):
        """
        Takes in an int and returns the appropriate instructions string
        :param instint: an int that is supplied and incremented by the expguis
        :return: a string containing the appropriate instructions that the expguis puts up
        """

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
                           ' others).'

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
