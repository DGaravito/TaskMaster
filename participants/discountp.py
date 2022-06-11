from participants import participant

from adopy.tasks.dd import *
from adopy import Engine

import numpy as np
import pandas as pd
import random


class DdParticipant(participant.Participant):

    def __init__(self, expid, trials, session, outdir, task, ss_del, ll_shortdel, ll_longdel, ss_smallrew, ll_rew,
                 rounds, buttonbox, eyetracking, fmri):
        super().__init__(expid, trials, session, outdir, task, buttonbox, eyetracking, fmri)

        self.rounds = int(rounds)

        self.engine = self.create_dd_engine(self.task, ss_del, ll_shortdel, ll_longdel, ss_smallrew, ll_rew)

        # Compute an optimal design for the first trial
        self.design = self.engine.get_design('optimal')

        # Experiment settingsguis output dataframe
        dict_simulsettings = {'Immediate Option Delay': [ss_del],
                              'Shortest Delay': [ll_shortdel],
                              'Longest Delay': [ll_longdel],
                              'Smallest Smaller Sooner Reward': [ss_smallrew],
                              'Largest Smaller Sooner Reward': [(float(ll_rew) - float(ss_smallrew))],
                              'Larger Later Reward': [ll_rew],
                              'Blocks': [rounds]
                              }

        self.set_settings(dict_simulsettings)

    def create_dd_engine(self, task, ss_del, ll_shortdel, ll_longdel, ss_smallrew, ll_rew):

        model = ModelHyp()

        grid_design = {
            # [Now]
            't_ss': [float(ss_del)],

            # [1 week, 2 weeks, ..., longdelay] in weeks
            't_ll': np.arange(float(ll_shortdel), float(ll_longdel), .5),

            # [smallreward, smallreward + $1, ..., bigreward]
            'r_ss': np.arange(float(ss_smallrew), float(ll_rew), .5),

            # [bigreward]
            'r_ll': [float(ll_rew)]
        }

        grid_param = {
            # 50 points on [10^-5, ..., 1] in a log scale
            'k': np.logspace(-5, 0, 50, base=10),

            # 10 points on (0, 5] in a linear scale
            'tau': np.linspace(0, 5, 11)[1:]
        }

        grid_response = {
            'choice': [0, 1]
        }

        # Set up engine
        engine = Engine(task, model, grid_design, grid_param, grid_response)

        return engine

    def get_design_text(self):

        if int(self.design['t_ss']) == 0:
            leftstring = 'Getting $' + str('{:.2f}'.format(self.design['r_ss'])) + '\nnow'

        else:
            leftstring = 'Getting $' + str('{:.2f}'.format(self.design['r_ll'])) + '\nafter '\
                         + str(int(self.design['t_ss'])) + ' weeks'

        rightstring = 'Getting $' + str('{:.2f}'.format(self.design['r_ll'])) + '\nafter '\
                      + str(int(self.design['t_ll'])) + ' weeks'

        return [leftstring, rightstring]

    def engineupdate(self, response):
        # Update engine with the response and current design
        self.engine.update(self.design, response)

        # Generate new optimal design based on previous design and response
        self.design = self.engine.get_design('optimal')

    def nextround(self, blocks):

        if blocks == self.rounds:

            prompt = 'Thank you! This task is complete.'

        else:

            prompt = 'Please wait for the next round.'

        return prompt

    def updateoutput(self, trial, onset, time, response):
        """
        records stats for the trial
        :param trial: the number of the trial that was just completed
        :param onset: onset time for the trial
        :param time: participants's reaction time
        :param response: integer with either 0 or 1 depending on if the person chose left or right
        :return: updates the performance dataframe in the superclass
        """

        df_simultrial = {
            'trial': [trial],
            'onset': [onset],
            'SSAmount': [float(self.design['r_ss'])],
            'LLAmount': [float(self.design['r_ll'])],
            'LLDelay': [float(self.design['t_ll'])],
            'response': [response],
            'reaction time': [time],
            'mean_k': [self.engine.post_mean[0]],
            'mean_tau': [self.engine.post_mean[1]],
            'sd_k': [self.engine.post_sd[0]],
            'sd_tau': [self.engine.post_sd[1]]
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

                inst = 'In this task, you will be making choices between\nreceiving pretend amounts of money either' \
                       ' right now or\nsome time in the future.'

            case 2:

                inst = 'You will use the keyboard to make your choice\nbetween the pretend rewards shown on the ' \
                       'left and\nright side of the screen.'

            case 3:

                inst = 'Even though these money rewards are pretend,\ntry to choose as if you were being offered ' \
                       'these rewards\nfor real.'

            case _:

                inst = 'Let the experimenter know you are ready.'

        return inst


class PdParticipant(participant.Participant):

    def __init__(self, expid, trials, session, outdir, task, design, minimum, maximum, outcome, money, rounds,
                 buttonbox, eyetracking, fmri):
        super().__init__(expid, trials, session, outdir, task, buttonbox, eyetracking, fmri)

        self.rounds = int(rounds)

        self.design = design
        self.maximum = float(maximum)
        self.minimum = float(minimum)
        self.trialdesign = []
        self.startmoney = float(money)
        self.outcomeopt = outcome
        self.outcomelist = []

        self.create_design()

        # Experiment settingsguis output dataframe
        dict_simulsettings = {'Design': [design],
                              'Minimum Reward': [minimum],
                              'Maximum Reward': [maximum],
                              'Blocks': [rounds]
                              }

        self.set_settings(dict_simulsettings)

    def create_design(self):
        """
        If you want both gains and losses, then it creates a random order for gain and loss questions
        :return: Does not return a value, instead creates the class dictionaries and then calls set design text to make
        the first trial
        """

        if self.design == 'Gains and Losses':

            multnum = int(self.get_trials() / 2)
            gainlosscond = ['Gain', 'Loss']
            multiplier = [multnum, multnum]
            self.order = sum([[s] * n for s, n in zip(gainlosscond, multiplier)], [])
            random.shuffle(self.order)

    def set_design_text(self):
        """
        Sets the actual text used in the design
        :return: Creates self.trialdesign
        """

        self.trialdesign = [
            random.uniform(self.minimum, self.maximum-.5),
            random.uniform(.01, .99)
        ]

    def get_design_text(self):
        """
        Looks at self.trialdesign and returns strings for the GUI
        :return: left text (sure), right text (gamble), and gamble probability
        """

        if self.design == 'Gains and Losses':

            self.state = self.order.pop()

            if self.state == 'Gain':

                # Set up the left string for sure value
                leftstring = 'Win $' + str('{:.2f}'.format(self.trialdesign[0])) + ' for sure'

                # Set up the right string for risky gamble
                rightstring = 'A ' + str(round(self.trialdesign[1] * 100)) + '% chance to win $' + \
                              str('{:.2f}'.format(self.maximum))

                # Set the probability bar for the risky gamble
                barvalue = round(self.trialdesign[1] * 100)

            else:

                # Set up the left string for sure value
                leftstring = 'Lose $' + str('{:.2f}'.format(self.trialdesign[0])) + ' for sure'

                # Set up the right string for risky gamble
                rightstring = 'A ' + str(round(self.trialdesign[1] * 100)) + '% chance to lose $' + \
                              str('{:.2f}'.format(self.maximum))

                # Set the probability bar for the risky gamble
                barvalue = round((1 - self.trialdesign[1]) * 100)

        elif self.design == "Gains only":

            self.state = 'Gain'

            # Set up the left string for sure value
            leftstring = 'Win $' + str('{:.2f}'.format(self.trialdesign[0])) + ' for sure'

            # Set up the right string for risky gamble
            rightstring = 'A ' + str(round(self.trialdesign[1] * 100)) + '% chance to win $' + \
                          str('{:.2f}'.format(self.maximum))

            # Set the probability bar for the risky gamble
            barvalue = round(self.trialdesign[1] * 100)

        else:

            self.state = 'Loss'

            # Set up the left string for sure value
            leftstring = 'Lose $' + str('{:.2f}'.format(self.trialdesign[0])) + ' for sure'

            # Set up the right string for risky gamble
            rightstring = 'A ' + str(round(self.trialdesign[1] * 100)) + '% chance to lose $' + \
                          str('{:.2f}'.format(self.maximum))

            # Set the probability bar for the risky gamble
            barvalue = round((1 - self.trialdesign[1]) * 100)

        # Return the values to the expguis
        return [leftstring, rightstring, barvalue]

    def nextround(self, blocks):

        if blocks == self.rounds:

            prompt = 'Thank you! This task is complete.'

        else:

            prompt = 'Please wait for the next round.'

        return prompt

    def updateoutput(self, trial, onset, time, response):
        """
        records stats for the trial
        :param trial: the number of the trial that was just completed
        :param onset: onset time for the trial
        :param time: participants's reaction time
        :param response: integer with either 0 or 1 depending on if the person chose left or right
        :return: updates the performance dataframe in the superclass
        """

        df_simultrial = {
            'trial': [trial],
            'cond': [self.state],
            'SureAmount': [str('{:.2f}'.format(self.trialdesign[0]))],
            'RiskyAmount': [self.maximum],
            'RiskyProbability': [str(self.trialdesign[1])],
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
                    if self.state == "Gain":
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
                        self.outcomelist.append('$' + str('{:.2f}'.format(float(self.maximum))))

                    # if not, add 0
                    else:
                        self.outcomelist.append(self.outcomelist.append('$0.00'))

                # if they only have losses...
                elif self.design == 'Losses only':

                    # if they lose, add the loss
                    if actualprob < float(self.trialdesign[1]):
                        self.outcomelist.append('-$' + str('{:.2f}'.format(float(self.maximum))))

                    # if not, add 0
                    else:
                        self.outcomelist.append(self.outcomelist.append('$0.00'))

                # if they have gains and losses...
                else:

                    # Then look at the state to see if it was a gain or loss
                    if self.state[1] == "Gain":

                        # if they win, add the reward
                        if actualprob > float(self.trialdesign[1]):
                            self.outcomelist.append('$' + str('{:.2f}'.format(float(self.maximum))))

                        # if not, add 0
                        else:
                            self.outcomelist.append(self.outcomelist.append('$0.00'))

                    else:

                        # if they lose, add the loss
                        if actualprob < float(self.trialdesign[1]):
                            self.outcomelist.append('-$' + str('{:.2f}'.format(float(self.maximum))))

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


class CEDParticipant(participant.Participant):

    def __init__(self, expid, trials, session, outdir, task, maxrew, outcome, names, version, rounds, buttonbox,
                 eyetracking, fmri):
        super().__init__(expid, trials, session, outdir, task, buttonbox, eyetracking, fmri)

        self.rounds = int(rounds)
        self.version = version

        self.outcomeopt = outcome
        self.outcomelist = []

        if names == 'a, e, i, u':

            self.stimnames = ['a', 'e', 'i', 'u']

        else:

            self.stimnames = ['Black', 'Red', 'Blue', 'Purple']

        # setting the default amounts for the tasks
        self.onebackamount = float(maxrew)
        self.fourbackamount = float(maxrew)

        # anything above one (but below four) back gets two values: one when the easier task, one when the harder
        self.twoeasyamount = float(maxrew)
        self.threeeasyamount = float(maxrew)

        self.twohardamount = float(maxrew)
        self.threehardamount = float(maxrew)

        # set up the modifiers

        self.onetwomodifier = 0.0
        self.onethreemodifier = 0.0
        self.onefourmodifier = 0.0
        self.twothreemodifier = 0.0
        self.twofourmodifier = 0.0
        self.threefourmodifier = 0.0

        # set up trial counts for modifiers

        self.onetwotrials = 0
        self.onethreetrials = 0
        self.onefourtrials = 0
        self.twothreetrials = 0
        self.twofourtrials = 0
        self.threefourtrials = 0

        # Experiment settingsguis output dataframe
        dict_simulsettings = {
            'Maximum Reward': [maxrew],
            'Version': [version]
                              }

        self.set_settings(dict_simulsettings)

        self.set_structure()

    def set_structure(self):

        if self.version == 'Alternate':

            multnum = int((self.get_trials() * self.rounds) / 6)
            gainlosscond = ['1-2', '1-3', '1-4', '2-3', '2-4', '3-4']
            multiplier = [multnum, multnum, multnum, multnum, multnum, multnum]
            self.order = sum([[s] * n for s, n in zip(gainlosscond, multiplier)], [])
            random.shuffle(self.order)

        else:

            multnum = int((self.get_trials() * self.rounds) / 3)
            gainlosscond = ['1-2', '1-3', '1-4']
            multiplier = [multnum, multnum, multnum]
            self.order = sum([[s] * n for s, n in zip(gainlosscond, multiplier)], [])
            random.shuffle(self.order)

    def set_design_text(self):

        self.state = self.order.pop()

        self.randomside = random.randint(1, 2)

        match self.state:

            case '1-2':

                self.onetwotrials += 1

                if self.randomside == 1:

                    self.lefttask = self.stimnames[0]
                    self.leftmoney = str('{:.2f}'.format(self.onebackamount + self.onetwomodifier))
                    self.righttask = self.stimnames[1]
                    self.rightmoney = str('{:.2f}'.format(self.twohardamount))

                else:

                    self.lefttask = self.stimnames[1]
                    self.leftmoney = str('{:.2f}'.format(self.twohardamount))
                    self.righttask = self.stimnames[0]
                    self.rightmoney = str('{:.2f}'.format(self.onebackamount + self.onetwomodifier))

            case '1-3':

                self.onethreetrials += 1

                if self.randomside == 1:

                    self.lefttask = self.stimnames[0]
                    self.leftmoney = str('{:.2f}'.format(self.onebackamount + self.onethreemodifier))
                    self.righttask = self.stimnames[2]
                    self.rightmoney = str('{:.2f}'.format(self.threehardamount))

                else:

                    self.lefttask = self.stimnames[2]
                    self.leftmoney = str('{:.2f}'.format(self.threehardamount))
                    self.righttask = self.stimnames[0]
                    self.rightmoney = str('{:.2f}'.format(self.onebackamount + self.onethreemodifier))

            case '1-4':

                self.onefourtrials += 1

                if self.randomside == 1:

                    self.lefttask = self.stimnames[0]
                    self.leftmoney = str('{:.2f}'.format(self.onebackamount + self.onefourmodifier))
                    self.righttask = self.stimnames[3]
                    self.rightmoney = str('{:.2f}'.format(self.fourbackamount))

                else:

                    self.lefttask = self.stimnames[3]
                    self.leftmoney = str('{:.2f}'.format(self.fourbackamount))
                    self.righttask = self.stimnames[0]
                    self.rightmoney = str('{:.2f}'.format(self.onebackamount + self.onefourmodifier))

            case '2-3':

                self.twothreetrials += 1

                if self.randomside == 1:

                    self.lefttask = self.stimnames[1]
                    self.leftmoney = str('{:.2f}'.format(self.twoeasyamount + self.twothreemodifier))
                    self.righttask = self.stimnames[2]
                    self.rightmoney = str('{:.2f}'.format(self.threehardamount))

                else:

                    self.lefttask = self.stimnames[2]
                    self.leftmoney = str('{:.2f}'.format(self.threehardamount))
                    self.righttask = self.stimnames[1]
                    self.rightmoney = str('{:.2f}'.format(self.twoeasyamount + self.twothreemodifier))

            case '2-4':

                self.twofourtrials += 1

                if self.randomside == 1:

                    self.lefttask = self.stimnames[1]
                    self.leftmoney = str('{:.2f}'.format(self.twoeasyamount + self.twofourmodifier))
                    self.righttask = self.stimnames[3]
                    self.rightmoney = str('{:.2f}'.format(self.fourbackamount))

                else:

                    self.lefttask = self.stimnames[3]
                    self.leftmoney = str('{:.2f}'.format(self.fourbackamount))
                    self.righttask = self.stimnames[1]
                    self.rightmoney = str('{:.2f}'.format(self.twoeasyamount + self.twofourmodifier))

            case '3-4':

                self.threefourtrials += 1

                if self.randomside == 1:

                    self.lefttask = self.stimnames[2]
                    self.leftmoney = str('{:.2f}'.format(self.threeeasyamount + self.threefourmodifier))
                    self.righttask = self.stimnames[3]
                    self.rightmoney = str('{:.2f}'.format(self.fourbackamount))

                else:

                    self.lefttask = self.stimnames[3]
                    self.leftmoney = str('{:.2f}'.format(self.fourbackamount))
                    self.righttask = self.stimnames[2]
                    self.rightmoney = str('{:.2f}'.format(self.threeeasyamount + self.threefourmodifier))

            case _:

                print('Panic!')

    def nextround(self, roundsdone):

        if self.rounds == roundsdone:

            if self.outcomeopt == 'Yes':

                prompt = 'Your outcome: ' + random.choice(self.outcomelist)

            else:

                prompt = 'Thank you! This task is complete.'

        else:

            prompt = 'Please wait for the next round.'

        return prompt

    def get_design_text(self):

        leftstring = 'Doing extra rounds of the\n\"' + self.lefttask + '\" task for $' + self.leftmoney
        rightstring = 'Doing extra rounds of the\n\"' + self.righttask + '\" task for $' + self.rightmoney

        return [leftstring, rightstring]

    def updateoutput(self, trial, onset, time, response):
        """
        records stats for the trial
        :param trial: the number of the trial that was just completed
        :param onset: onset time for the trial
        :param time: participants's reaction time
        :param response: integer with either 0 or 1 depending on if the person chose left or right
        :return: updates the performance dataframe in the superclass
        """

        df_simultrial = {
            'trial': [trial],
            'left task': [self.lefttask],
            'left value': [self.leftmoney],
            'right task': [self.righttask],
            'right value': [self.rightmoney],
            'onset': [onset],
            'response': [response],
            'reaction time': [time]
        }

        df_simultrial = pd.DataFrame(data=df_simultrial)
        self.set_performance(df_simultrial)

        # only do the following if the user wanted a random reward/loss at the end
        if (self.outcomeopt == 'Yes') & (response != 'None'):

            # Generate a random number of rounds to be done for that task
            randomrounds = random.randint(1, 10)

            # Add their choice (with the random number of rounds)
            # if they chose the left option...
            if response == 0:

                outcomestring = str(randomrounds) + ' rounds of the ' + self.lefttask + ' task for $' + self.leftmoney

            # if they chose the right option...
            else:

                outcomestring = str(randomrounds) + ' rounds of the ' + self.righttask + ' task for $' + self.rightmoney

            self.outcomelist.append(outcomestring)

        modifiermod = 0.5

        if response != 'None':

            match self.state:

                case '1-2':

                    if (self.randomside == 1) & (response == 0):

                        self.onetwomodifier = self.onetwomodifier - (modifiermod / float(self.onetwotrials))

                    elif (self.randomside == 2) & (response == 1):

                        self.onetwomodifier = self.onetwomodifier - (modifiermod / float(self.onetwotrials))

                    else:

                        self.onetwomodifier = self.onetwomodifier + (modifiermod / float(self.onetwotrials))

                case '1-3':

                    if (self.randomside == 1) & (response == 0):

                        self.onethreemodifier = self.onethreemodifier - (modifiermod / float(self.onethreetrials))

                    elif (self.randomside == 2) & (response == 1):

                        self.onethreemodifier = self.onethreemodifier - (modifiermod / float(self.onethreetrials))

                    else:

                        self.onethreemodifier = self.onethreemodifier + (modifiermod / float(self.onethreetrials))

                case '1-4':

                    if (self.randomside == 1) & (response == 0):

                        self.onefourmodifier = self.onefourmodifier - (modifiermod / float(self.onefourtrials))

                    elif (self.randomside == 2) & (response == 1):

                        self.onefourmodifier = self.onefourmodifier - (modifiermod / float(self.onefourtrials))

                    else:

                        self.onefourmodifier = self.onefourmodifier + (modifiermod / float(self.onefourtrials))

                case '2-3':

                    if (self.randomside == 1) & (response == 0):

                        self.twothreemodifier = self.twothreemodifier - (modifiermod / float(self.twothreetrials))

                    elif (self.randomside == 2) & (response == 1):

                        self.twothreemodifier = self.twothreemodifier - (modifiermod / float(self.twothreetrials))

                    else:

                        self.twothreemodifier = self.twothreemodifier + (modifiermod / float(self.twothreetrials))

                case '2-4':

                    if (self.randomside == 1) & (response == 0):

                        self.twofourmodifier = self.twofourmodifier - (modifiermod / float(self.twofourtrials))

                    elif (self.randomside == 2) & (response == 1):

                        self.twofourmodifier = self.twofourmodifier - (modifiermod / float(self.twofourtrials))

                    else:

                        self.twofourmodifier = self.twofourmodifier + (modifiermod / float(self.twofourtrials))

                case '3-4':

                    if (self.randomside == 1) & (response == 0):

                        self.threefourmodifier = self.threefourmodifier - (modifiermod / float(self.threefourtrials))

                    elif (self.randomside == 2) & (response == 1):

                        self.threefourmodifier = self.threefourmodifier - (modifiermod / float(self.threefourtrials))

                    else:

                        self.threefourmodifier = self.threefourmodifier + (modifiermod / float(self.threefourtrials))

    def get_instructions(self, instint):
        """
        Takes in an int and returns the appropriate instructions string
        :param instint: an int that is supplied and incremented by the expguis
        :return: a string containing the appropriate instructions that the expguis puts up
        """

        match instint:

            case 1:

                inst = 'Remember those memory tasks? Now you will make\ndecisions about these tasks.'

            case 2:

                inst = 'You will first see one option by itself. Use this\ntime to think about how much you would ' \
                       'like to repeat\nthe task for that amount of money.'

            case 3:

                inst = 'Next, you will see two options, each including a\ndollar amount and a task.'

            case 4:

                inst = 'For example, you may have to choose between\ncompleting extra rounds of the easiest task ' \
                       'for $1\nor extra rounds of the hardest task for $10.'

            case 5:

                inst = 'There is no right answer! Just choose the option\nthat you would prefer.'

            case 6:

                if self.outcomeopt == 'Yes':

                    inst = 'Any one of the choices you make could determine\nwhat task you complete extra rounds of ' \
                           'and how much\nyou are paid for completing that task.'

                else:

                    inst = 'Take as much time as you need to choose. After a\nwhile, the decision will disappear, ' \
                           'but those choices\nwill be shown again at the end.'

            case 7:

                if self.outcomeopt == 'Yes':

                    inst = 'We will pick one of your choices at random. It does\nnot matter how well you do on the ' \
                           'task chosen. You\nwill be paid as long as you maintain your effort.'

                else:

                    inst = 'Let the experimenter know you are ready.'

            case 8:

                if self.outcomeopt == 'Yes':

                    inst = 'Take as much time as you need to choose. After a\nwhile, the decision will disappear, ' \
                           'but those choices\nwill be shown again at the end.'

                else:

                    inst = 'Let the experimenter know you are ready.'

            case _:

                inst = 'Let the experimenter know you are ready.'

        return inst
