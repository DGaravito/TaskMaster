from participants import participant

from adopy.tasks.cra import *
from adopy import Engine

import numpy as np
import pandas as pd
import random


class ARTTParticipant(participant.Participant):

    def __init__(self, expid, trials, session, outdir, task, risklist, amblist, rewmin, rewmax, structure, outcome,
                 money, rounds, buttonbox, eyetracking, fmri):
        super().__init__(expid, trials, session, outdir, task, buttonbox, eyetracking, fmri)

        self.rounds = int(rounds)
        self.startmoney = float(money)
        self.inst = 0
        self.outcomeopt = outcome
        self.outcomelist = []

        self.structure = structure
        self.create_structure()

        self.engine = self.create_artt_engine(self.task, risklist, amblist, rewmin, rewmax)

        # Compute an optimal design for the first trial
        self.design = self.engine.get_design('optimal')

        # Experiment settingsguis output dataframe
        dict_simulsettings = {'Risky Probabilities': [risklist],
                              'Ambiguous Probabilities': [amblist],
                              'Fixed Reward': [rewmin],
                              'Largest Reward': [rewmax],
                              'Design': [structure],
                              'Blocks': [rounds]
                              }

        self.set_settings(dict_simulsettings)

    def create_structure(self):
        """
        If you want both gains and losses, then it creates a random order for gain and loss questions
        :return: Does not return a value, instead creates the class dictionaries and then calls set design text to make
        the first trial
        """

        if self.structure == 'Gains and Losses':

            multnum = int((self.get_trials() / 2) * self.rounds)
            gainlosscond = ['Gain', 'Loss']
            multiplier = [multnum, multnum]
            self.order = sum([[s] * n for s, n in zip(gainlosscond, multiplier)], [])
            random.shuffle(self.order)

    def create_artt_engine(self, task, risklist, amblist, rewmin, rewmax):

        model = ModelLinear()

        r_var = np.arange(float(rewmin) + .5, int(rewmax), .5)
        r_fix = rewmin

        rewards = np.array([
            [rv, rf] for rv in r_var for rf in r_fix
        ])

        pa_risky = np.array([[pr, 0] for pr in risklist])

        pa_ambig = np.array([[0.5, am] for am in amblist])

        pr_am = np.vstack([pa_risky, pa_ambig])

        grid_design = {('p_var', 'a_var'): pr_am,
                       ('r_var', 'r_fix'): rewards}

        grid_param = {
            'alpha': np.linspace(0, 3, 11)[1:],
            'beta': np.linspace(-3, 3, 11),
            'gamma': np.linspace(0, 5, 11)[1:]
        }

        grid_response = {
            'choice': [0, 1]
        }

        # Set up engine
        engine = Engine(task, model, grid_design, grid_param, grid_response)

        return engine

    def get_design_text(self):

        bluered = random.randint(1, 2)

        if self.structure == 'Gains and Losses':

            self.state = self.order.pop()

            if self.state == 'Gain':

                fixedstring = 'Win $' + str('{:.2f}'.format(self.design['r_fix'])) + ' for sure'
                otherstring = 'Win $' + str('{:.2f}'.format(self.design['r_var']))

            else:

                fixedstring = 'Lose $' + str('{:.2f}'.format(self.design['r_fix'])) + ' for sure'
                otherstring = 'Lose $' + str('{:.2f}'.format(self.design['r_var']))

        elif self.structure == 'Gains only':

            self.state = 'Gain'

            fixedstring = 'Win $' + str('{:.2f}'.format(self.design['r_fix'])) + ' for sure'
            otherstring = 'Win $' + str('{:.2f}'.format(self.design['r_var']))

        else:

            self.state = 'Loss'

            fixedstring = 'Lose $' + str('{:.2f}'.format(self.design['r_fix'])) + ' for sure'
            otherstring = 'Lose $' + str('{:.2f}'.format(self.design['r_var']))

        if self.design['a_var'] == 0:

            if bluered == 1:

                picstring = 'ARTT_risk_' + str(100-round(self.design['p_var'] * 100)) + '.bmp'

            else:

                picstring = 'ARTT_risk_' + str(round(self.design['p_var'] * 100)) + '.bmp'

        else:

            picstring = 'ARTT_ambig_' + str(round(self.design['a_var'] * 100)) + '.bmp'

        return [fixedstring, otherstring, picstring, bluered]

    def nextround(self, blocks):

        if blocks == self.rounds:

            prompt = 'Thank you! This task is complete.'

        else:

            prompt = 'Please wait for the next round.'

        return prompt

    def engineupdate(self, response):

        # Update engine with the response and current design
        self.engine.update(self.design, response)

        # Generate new optimal design based on previous design and response
        self.design = self.engine.get_design('optimal')

    def updateoutput(self, trial, onset, time, response):
        """
        Records the stats
        :param trial: the number of the trial that was just completed
        :param onset: onset time for the trial
        :param time: participants's reaction time
        :param response: integer with either 0 or 1 depending on if the person chose left or right. Default is 3 in case
        the participants doesn't answer in time.
        :return: updates the performance dataframe in the superclass
        """

        df_simultrial = {
            'trial': [trial],
            'cond': [self.state],
            'Proportion Ambiguous': float(self.design['a_var']),
            'Proportion Risky': [float(self.design['p_var'])],
            'Fixed Reward': [self.design['r_fix']],
            'Variable Reward': [self.design['r_var']],
            'onset': [onset],
            'response': [response],
            'reaction time': [time],
            'mean_alpha': [self.engine.post_mean[0]],
            'mean_beta': [self.engine.post_mean[1]],
            'mean_gamma': [self.engine.post_mean[2]],
            'sd_alpha': [self.engine.post_sd[0]],
            'sd_beta': [self.engine.post_sd[1]],
            'sd_gamma': [self.engine.post_sd[2]]
        }

        df_simultrial = pd.DataFrame(data=df_simultrial)
        self.set_performance(df_simultrial)

        # only do the following if the user wanted a random reward/loss at the end
        if (self.outcomeopt == 'Yes') & (response != 'None'):

            # Add the potential outcome of this choice to the list for post-task rewards.
            # If they chose the sure thing...
            if response == 0:

                # then add the fixed value to the list
                self.outcomelist.append(float(self.design['r_fix']))

            # if not...
            else:

                # actually generate a random probability to see if they win the gamble
                actualprob = random.uniform(0.0, 1.0)

                # if they win, add the reward
                if actualprob > float(self.design['p_var']):
                    self.outcomelist.append(float(self.design['r_var']))

                # if they don't, add 0
                else:
                    self.outcomelist.append(0.0)

            if response == 0:

                # if they only have gains...
                if self.design == 'Gains only':

                    # then add the fixed gain to the list
                    self.outcomelist.append('$' + str('{:.2f}'.format(float(self.design['r_fix']))))

                # if they only have losses...
                elif self.design == 'Losses only':

                    # then add the fixed loss to the list
                    self.outcomelist.append('-$' + str('{:.2f}'.format(float(self.design['r_fix']))))

                # if they have gains and losses...
                else:

                    # Then look at the state to see if it was a gain or loss
                    if self.state == "Gain":
                        self.outcomelist.append('$' + str('{:.2f}'.format(float(self.design['r_fix']))))

                    else:
                        self.outcomelist.append('-$' + str('{:.2f}'.format(float(self.design['r_fix']))))

            # if they chose the gamble...
            else:

                # actually generate a random probability to see if they win the gamble
                actualprob = random.uniform(0.0, 1.0)

                # if they only have gains...
                if self.design == 'Gains only':

                    # if they win, add the reward
                    if actualprob > float(self.design['p_var']):
                        self.outcomelist.append('$' + str('{:.2f}'.format(float(self.design['r_var']))))

                    # if not, add 0
                    else:
                        self.outcomelist.append(self.outcomelist.append('$0.00'))

                # if they only have losses...
                elif self.design == 'Losses only':

                    # if they lose, add the loss
                    if actualprob < float(self.design['p_var']):
                        self.outcomelist.append('-$' + str('{:.2f}'.format(float(self.design['r_var']))))

                    # if not, add 0
                    else:
                        self.outcomelist.append(self.outcomelist.append('$0.00'))

                # if they have gains and losses...
                else:

                    # Then look at the state to see if it was a gain or loss
                    if self.state[1] == "Gain":

                        # if they win, add the reward
                        if actualprob > float(self.design['p_var']):
                            self.outcomelist.append('$' + str('{:.2f}'.format(float(self.design['r_var']))))

                        # if not, add 0
                        else:
                            self.outcomelist.append(self.outcomelist.append('$0.00'))

                    else:

                        # if they lose, add the loss
                        if actualprob < float(self.design['p_var']):
                            self.outcomelist.append('-$' + str('{:.2f}'.format(float(self.design['r_var']))))

                        # if not, add 0
                        else:
                            self.outcomelist.append(self.outcomelist.append('$0.00'))

    def get_instructions(self, instint):
        """
        Takes in an int and returns the appropriate instructions string
        :param instint: an int that is supplied and incremented by the expguis
        :return: a string containing the appropriate instructions that the expguis puts up
        """

        match instint:

            case 1:

                inst = 'You are participating in a study about decision making\nand will be asked to make a number' \
                       ' of choices.'

            case 2:

                if self.outcomeopt == 'Yes':

                    inst = 'You have $' + str('{:.2f}'.format(self.startmoney)) + ' in starting money. Your final ' \
                                                                                  'payment\nwill depend on the ' \
                                                                                  'choices you make in this task.'

                else:

                    inst = 'Even though these money rewards are pretend,\ntry to choose as if you were being offered ' \
                           'these rewards\nfor real.'

            case 3:

                inst = 'In this task, you will see images that show gambles.'

            case 4:

                inst = 'Each gamble represents a bag of red and blue poker\nchips. Continue to see an example.'

            case 6:

                inst = 'The size of the colored areas represent the number\nof chips of each color in the bag. In ' \
                       'the example, 25 chips\nare blue and 75 chips are red.'

            case 7:

                inst = 'Next to each color is a dollar amount. This amount\nrepresents how much you will win or' \
                       ' lose if that color\nof chip is drawn.'

            case 8:

                inst = 'In around half of the trials, the red color will be associated\nwith zero; in the other half,' \
                       ' the blue color will\nbe.'

            case 9:

                inst = 'In some gambles, part of the gamble will be hidden,\nso you will have less information about' \
                       'the number of\nred and blue chips in the bag.'

            case 10:

                inst = 'In the next example, the gray bar covers the other\n50 chips in the bag. The remaining ' \
                       '50 could be all\nred, all blue, or something in between.'

            case 12:

                inst = 'Although there could be many possible combinations\nof red and blue chips in the mystery' \
                       ' bags, remember\nthat these gambles still have actual chances of winning and losing.'

            case _:

                inst = 'Let the experimenter know you are ready.'

        return inst


class RAParticipant(participant.Participant):

    def __init__(self, expid, trials, session, outdir, task, minimum, maximum, outcome, money, rounds, buttonbox,
                 eyetracking, fmri):
        super().__init__(expid, trials, session, outdir, task, buttonbox, eyetracking, fmri)

        self.rounds = int(rounds)
        self.startmoney = money
        self.outcomeopt = outcome
        self.trialtext = []
        self.outcomelist = []

        self.create_stim(minimum, maximum)

        # Experiment settingsguis output dataframe
        dict_simulsettings = {'Minimum Reward': [minimum],
                              'Maximum Reward': [maximum],
                              'Blocks': [rounds]
                              }

        self.set_settings(dict_simulsettings)

    def create_stim(self, minimum, maximum):
        """
        Uses the parameters from the settingsguis input and makes a set of dictionaries for gamble probabilities and
        sure values
        :param minimum: the minimum reward value possible, as an integer, given by participants
        :param maximum: the maximum reward value possible, as an integer, given by participants
        :return: Does not return a value, instead creates array of possible gains
        """

        self.gainamounts = np.arange(int(minimum), int(maximum), 1)
        self.multiplieramounts = np.arange(.25, 2, .125)

        self.set_design_text()

    def set_design_text(self):
        """
        Gets the actual text used in the design. The sure thing is always zero; the gamble has a possible gain equal to
        a random gain amount and a possible loss that is equal to the random gain amount multiplied by the negative
        multiplier
        :return: Creates self.trialdesign
        """

        self.gainint = random.choice(self.gainamounts)
        self.lossfloat = self.gainint * random.choice(self.multiplieramounts)

    def get_design_text(self):
        """
        Looks at self.trialdesign and returns strings for the GUI
        :return: gain text, loss text for the gamble, as a list
        """

        # Set up the left string for sure value
        gainstring = '50% chance to win $' + str('{:.2f}'.format(self.gainint))

        # Set up the right string for risky gamble
        lossstring = '50% chance to lose $' + str('{:.2f}'.format(self.lossfloat))

        # Return the values to the expguis
        return [gainstring, lossstring]

    def nextround(self, blocks):

        if blocks == self.rounds:

            prompt = 'Thank you! This task is complete.'

        else:

            prompt = 'Please wait for the next round.'

        return prompt

    def updateoutput(self, trial, onset, time, response):
        """
        Records the stats
        :param trial: the number of the trial that was just completed
        :param onset: onset time for the trial
        :param time: participants's reaction time
        :param response: integer with either 0 or 1 depending on if the person chose left or right. Default is 3 in case
        the participants doesn't answer in time.
        :return: updates the performance dataframe in the superclass
        """

        df_simultrial = {
            'trial': [trial],
            'gain': [str('{:.2f}'.format(self.gainint))],
            'loss': [str('{:.2f}'.format(self.lossfloat))],
            'certain': [0],
            'onset': [onset],
            'response': [response],
            'reaction time': [time]
        }

        df_simultrial = pd.DataFrame(data=df_simultrial)
        self.set_performance(df_simultrial)

        # only do the following if the user wanted a random reward/loss at the end
        if (self.outcomeopt == 'Yes') & (response != 'None'):

            # Add the potential outcome of this choice to the list for post-task rewards.
            # If they chose the sure thing...
            if response == 0:

                # then add the fixed value to the list
                self.outcomelist.append('$0.00')

            # if not...
            else:

                # actually flip a coin to see if they win the gamble
                coin = random.randint(1, 2)

                # if they win, add the reward
                if coin == 1:
                    self.outcomelist.append('$' + str('{:.2f}'.format(float(self.gainint))))

                # if they don't, add the loss
                else:
                    self.outcomelist.append('-$' + str('{:.2f}'.format(self.lossfloat)))

    def get_instructions(self, instint):
        """
        Takes in an int and returns the appropriate instructions string
        :param instint: an int that is supplied and incremented by the expguis
        :return: a string containing the appropriate instructions that the expguis puts up
        """

        match instint:

            case 1:

                inst = 'In this task, you will be choose whether to\ntake gambles where you have the possibility ' \
                       'to win\nor lose money.'

            case 2:

                inst = 'You will use the keyboard to make your choice\nbetween neither winning nor losing money on ' \
                       'the left\nside of the screen and taking a gamble right side\nof the screen.'

            case 3:

                if self.outcomeopt == 'Yes':

                    inst = 'You have $' + str('{:.2f}'.format(self.startmoney)) + ' in starting money. Your final ' \
                                                                                  'payment\nwill depend on the ' \
                                                                                  'choices you make in this task.'

                else:

                    inst = 'Even though these money rewards are pretend,\ntry to choose as if you were being offered ' \
                           'these rewards\nfor real.'

            case _:

                inst = 'Let the experimenter know you are ready.'

        return inst


class FrameParticipant(participant.Participant):

    def __init__(self, expid, trials, session, outdir, task, minimum, maximum, design, ftt, outcome, money, rounds,
                 buttonbox, eyetracking, fmri):
        super().__init__(expid, trials, session, outdir, task, buttonbox, eyetracking, fmri)

        self.rounds = int(rounds)
        self.startmoney = float(money)
        self.outcomeopt = outcome
        self.design = design
        self.ftt = ftt
        self.maxrew = float(maximum)
        self.minrew = float(minimum)
        self.order = []
        self.trialdesign = []
        self.outcomelist = []

        self.set_order()

        # Experiment settingsguis output dataframe
        dict_simulsettings = {'Design': [design],
                              'FTT': [ftt],
                              'Minimum Reward': [minimum],
                              'Maximum Reward': [maximum]
                              }

        self.set_settings(dict_simulsettings)

    def set_order(self):

        if (self.design == 'Gains and Losses') & (self.ftt == 'Yes'):

            multnum = int(self.get_trials() / 6)
            fttglcond = [['Gist', 'Loss'],
                         ['Gist', 'Gain'],
                         ['Mixed', 'Loss'],
                         ['Mixed', 'Gain'],
                         ['Verbatim', 'Loss'],
                         ['Verbatim', 'Gain']]
            multiplier = [multnum, multnum, multnum, multnum, multnum, multnum]
            self.order = sum([[s] * n for s, n in zip(fttglcond, multiplier)], [])
            random.shuffle(self.order)

        elif self.ftt == 'Yes':

            multnum = int(self.get_trials() / 3)
            fttcond = ['Gist', 'Mixed', 'Verbatim']
            multiplier = [multnum, multnum, multnum]
            self.order = sum([[s] * n for s, n in zip(fttcond, multiplier)], [])

        elif self.design == 'Gains and Losses':

            multnum = int(self.get_trials() / 2)
            gainlosscond = ['Gain', 'Loss']
            multiplier = [multnum, multnum]
            self.order = sum([[s] * n for s, n in zip(gainlosscond, multiplier)], [])

        elif self.design == 'Gains only':

            self.order = ['Gain'] * self.get_trials()

        else:

            self.order = ['Loss'] * self.get_trials()

        random.shuffle(self.order)

    def set_design_text(self):
        """
        Gets the actual text used in the design
        :return: Creates self.trialdesign
        """

        gambleprob = random.uniform(.01, .99)
        gambleamount = random.uniform(self.minrew, self.maxrew)
        sureamount = gambleamount*gambleprob

        self.trialdesign = [sureamount, gambleprob, gambleamount]

    def get_design_text(self):
        """
        Looks at self.trialdesign and returns strings for the GUI
        :return: left text (sure), right text (gamble), and gamble probability
        """

        self.state = self.order.pop()

        if (self.design == 'Gains and Losses') & (self.ftt == 'Yes'):

            match self.state:

                case ['Gist', 'Loss']:
                    # Set up the left string for sure value
                    leftstring = 'Lose $' + str('{:.2f}'.format(self.trialdesign[0])) + ' for sure'

                    # Set up the right string for positive gamble outcome
                    righttopstring = 'A ' + str(round(100*self.trialdesign[1])) + '% chance to lose nothing'

                    rightbottomstring = ''

                case ['Gist', 'Gain']:
                    # Set up the left string for sure value
                    leftstring = 'Win $' + str('{:.2f}'.format(self.trialdesign[0])) + ' for sure'

                    righttopstring = ''

                    # Set up the right string for negative gamble outcome
                    rightbottomstring = 'A ' + str(round(100*(1-self.trialdesign[1]))) + '% chance to win nothing'

                case ['Mixed', 'Loss']:
                    # Set up the left string for sure value
                    leftstring = 'Lose $' + str('{:.2f}'.format(self.trialdesign[0])) + ' for sure'

                    # Set up the right string for positive gamble outcome
                    righttopstring = 'A ' + str(round(100*self.trialdesign[1])) + '% chance to lose nothing'

                    # Set up the right string for negative gamble outcome
                    rightbottomstring = 'A ' + str(round(100*(1-self.trialdesign[1]))) + '% chance to lose $' + \
                                        str('{:.2f}'.format(self.trialdesign[2]))

                case ['Mixed', 'Gain']:
                    # Set up the left string for sure value
                    leftstring = 'Win $' + str('{:.2f}'.format(self.trialdesign[0])) + ' for sure'

                    # Set up the right string for positive gamble outcome
                    righttopstring = 'A ' + str(round(100*self.trialdesign[1])) + '% chance to win $' + \
                                     str('{:.2f}'.format(self.trialdesign[2]))

                    # Set up the right string for negative gamble outcome
                    rightbottomstring = 'A ' + str(round(100*(1-self.trialdesign[1]))) + '% chance to win nothing'

                case ['Verbatim', 'Loss']:
                    # Set up the left string for sure value
                    leftstring = 'Lose $' + str('{:.2f}'.format(self.trialdesign[0])) + ' for sure'

                    righttopstring = ''

                    # Set up the right string for negative gamble outcome
                    rightbottomstring = 'A ' + str(round(100*(1-self.trialdesign[1]))) + '% chance to lose $' + \
                                        str('{:.2f}'.format(self.trialdesign[2]))

                case ['Verbatim', 'Gain']:
                    # Set up the left string for sure value
                    leftstring = 'Win $' + str('{:.2f}'.format(self.trialdesign[0])) + ' for sure'

                    # Set up the right string for positive gamble outcome
                    righttopstring = 'A ' + str(round(100*self.trialdesign[1])) + '% chance to win $' + \
                                     str('{:.2f}'.format(self.trialdesign[2]))

                    rightbottomstring = ''

                case _:

                    leftstring = 'ummm'
                    righttopstring = 'uh'
                    rightbottomstring = 'oh'

        elif (self.ftt == 'Yes') & (self.design == 'Losses only'):

            if self.state == 'Gist':

                # Set up the left string for sure value
                leftstring = 'Lose $' + str('{:.2f}'.format(self.trialdesign[0])) + ' for sure'

                # Set up the right string for positive gamble outcome
                righttopstring = 'A ' + str(round(100*self.trialdesign[1])) + '% chance to lose nothing'

                rightbottomstring = ''

            elif self.state == 'Mixed':

                # Set up the left string for sure value
                leftstring = 'Lose $' + str('{:.2f}'.format(self.trialdesign[0])) + ' for sure'

                # Set up the right string for positive gamble outcome
                righttopstring = 'A ' + str(round(100 * self.trialdesign[1])) + '% chance to lose nothing'

                # Set up the right string for negative gamble outcome
                rightbottomstring = 'A ' + str(round(100 * (1 - self.trialdesign[1]))) + '% chance to lose $' + \
                                    str('{:.2f}'.format(self.trialdesign[2]))

            else:
                # Set up the left string for sure value
                leftstring = 'Lose $' + str('{:.2f}'.format(self.trialdesign[0])) + ' for sure'

                righttopstring = ''

                # Set up the right string for negative gamble outcome
                rightbottomstring = 'A ' + str(100*(1-self.trialdesign[1])) + '% chance to lose ' + \
                                    str('{:.2f}'.format(self.trialdesign[2]))

        elif (self.ftt == 'Yes') & (self.design == 'Gains only'):

            if self.state == 'Gist':

                # Set up the left string for sure value
                leftstring = 'Win $' + str('{:.2f}'.format(self.trialdesign[0])) + ' for sure'

                righttopstring = ''

                # Set up the right string for negative gamble outcome
                rightbottomstring = 'A ' + str(round(100*(1-self.trialdesign[1]))) + '% chance to win nothing'

            elif self.state == 'Mixed':

                # Set up the left string for sure value
                leftstring = 'Win $' + str('{:.2f}'.format(self.trialdesign[0])) + ' for sure'

                # Set up the right string for positive gamble outcome
                righttopstring = 'A ' + str(round(100 * self.trialdesign[1])) + '% chance to win $' + \
                                 str('{:.2f}'.format(self.trialdesign[2]))

                # Set up the right string for negative gamble outcome
                rightbottomstring = 'A ' + str(round(100 * (1 - self.trialdesign[1]))) + '% chance to win nothing'

            else:
                # Set up the left string for sure value
                leftstring = 'Win $' + str('{:.2f}'.format(self.trialdesign[0])) + ' for sure'

                # Set up the right string for positive gamble outcome
                righttopstring = 'A ' + str(round(100*self.trialdesign[1])) + '% chance to win $' + \
                                 str('{:.2f}'.format(self.trialdesign[2]))

                rightbottomstring = ''

        else:

            if self.state == 'Gain':
                # Set up the left string for sure value
                leftstring = 'Win $' + str('{:.2f}'.format(self.trialdesign[0])) + ' for sure'

                # Set up the right string for positive gamble outcome
                righttopstring = 'A ' + str(round(100*self.trialdesign[1])) + '% chance to win $' + \
                                 str('{:.2f}'.format(self.trialdesign[2]))

                # Set up the right string for negative gamble outcome
                rightbottomstring = 'A ' + str(round(100*(1-self.trialdesign[1]))) + '% chance to win nothing'

            else:
                # Set up the left string for sure value
                leftstring = 'Lose $' + str('{:.2f}'.format(self.trialdesign[0])) + ' for sure'

                # Set up the right string for positive gamble outcome
                righttopstring = 'A ' + str(round(100*self.trialdesign[1])) + '% chance to lose nothing'

                # Set up the right string for negative gamble outcome
                rightbottomstring = 'A ' + str(round(100*(1-self.trialdesign[1]))) + '% chance to lose $' + \
                                    str('{:.2f}'.format(self.trialdesign[2]))

        # Return the values to the expguis
        return [leftstring, righttopstring, rightbottomstring]

    def nextround(self, blocks):

        if blocks == self.rounds:

            prompt = 'Thank you! This task is complete.'

        else:

            prompt = 'Please wait for the next round.'

        return prompt

    def updateoutput(self, trial, onset, time, response):
        """
        Records the stats
        :param trial: the number of the trial that was just completed
        :param onset: onset time for the trial
        :param time: participants's reaction time
        :param response: integer with either 0 or 1 depending on if the person chose left or right. Default is 3 in case
        the participants doesn't answer in time.
        :return: updates the performance dataframe in the superclass
        """

        df_simultrial = {
            'trial': [trial],
            'cond': [str(self.state)],
            'SureAmount': [str('{:.2f}'.format(self.trialdesign[0]))],
            'RiskyAmount': [str('{:.2f}'.format(self.trialdesign[2]))],
            'RiskyProbability': [self.trialdesign[1]],
            'onset': [onset],
            'response': [response],
            'reaction time': [time]
        }

        df_simultrial = pd.DataFrame(data=df_simultrial)
        self.set_performance(df_simultrial)

        # only do the following if the user wanted a random reward/loss at the end
        if (self.outcomeopt == 'Yes') & (response != 'None'):

            # Add the potential outcome of this choice to the list for post-task rewards.
            # If they chose the sure thing...
            if response == 0:

                # if they only have gains...
                if self.design == 'Gains only':

                    # then add the fixed gain to the list
                    self.outcomelist.append('$' + str('{:.2f}'.format(float(self.trialdesign[0]))))

                # if they only have losses...
                elif self.design == 'Losses only':

                    # then add the fixed loss to the list
                    self.outcomelist.append('-$' + str('{:.2f}'.format(float(self.trialdesign[0]))))

                # if they have gains and losses...
                else:

                    # Then look at the state to see if it was a gain or loss
                    if self.state[1] == "Gain":
                        self.outcomelist.append('$' + str('{:.2f}'.format(float(self.trialdesign[0]))))

                    else:
                        self.outcomelist.append('-$' + str('{:.2f}'.format(float(self.trialdesign[0]))))

            # if they chose the gamble...
            else:

                # actually generate a random probability to see if they win the gamble
                actualprob = random.uniform(0.0, 1.0)

                # if they only have gains...
                if self.design == 'Gains only':

                    # if they win, add the reward
                    if actualprob > float(self.trialdesign[1]):
                        self.outcomelist.append('$' + str('{:.2f}'.format(float(self.trialdesign[2]))))

                    # if not, add 0
                    else:
                        self.outcomelist.append(self.outcomelist.append('$0.00'))

                # if they only have losses...
                elif self.design == 'Losses only':

                    # if they lose, add the loss
                    if actualprob < float(self.trialdesign[1]):
                        self.outcomelist.append('-$' + str('{:.2f}'.format(float(self.trialdesign[2]))))

                    # if not, add 0
                    else:
                        self.outcomelist.append(self.outcomelist.append('$0.00'))

                # if they have gains and losses...
                else:

                    # Then look at the state to see if it was a gain or loss
                    if self.state[1] == "Gain":

                        # if they win, add the reward
                        if actualprob > float(self.trialdesign[1]):
                            self.outcomelist.append('$' + str('{:.2f}'.format(float(self.trialdesign[2]))))

                        # if not, add 0
                        else:
                            self.outcomelist.append(self.outcomelist.append('$0.00'))

                    else:

                        # if they lose, add the loss
                        if actualprob < float(self.trialdesign[1]):
                            self.outcomelist.append('-$' + str('{:.2f}'.format(float(self.trialdesign[2]))))

                        # if not, add 0
                        else:
                            self.outcomelist.append(self.outcomelist.append('$0.00'))

    def get_instructions(self, instint):
        """
        Takes in an int and returns the appropriate instructions string
        :param instint: an int that is supplied and incremented by the expguis
        :return: a string containing the appropriate instructions that the expguis puts up
        """

        match instint:

            case 1:

                inst = 'In this task, you will be making choices between\n guarantees of winning or losing some money' \
                       ' or taking\ngambles to win more money or lose less money.'

            case 2:

                inst = 'You will use the keyboard to make your choice\nbetween the pretend rewards shown on the ' \
                       'left and\nright side of the screen.'

            case 3:

                if self.outcomeopt == 'Yes':

                    inst = 'You have $' + str('{:.2f}'.format(self.startmoney)) + ' in starting money. Your final ' \
                                                                                  'payment\nwill depend on the ' \
                                                                                  'choices you make in this task.'

                else:

                    inst = 'Even though these money rewards are pretend,\ntry to choose as if you were being offered ' \
                           'these rewards\nfor real.'

            case _:

                inst = 'Let the experimenter know you are ready.'

        return inst
