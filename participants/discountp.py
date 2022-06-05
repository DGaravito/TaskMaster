from participants import participant

from adopy.tasks.dd import *
from adopy import Engine

import numpy as np
import pandas as pd
import random


class DdParticipant(participant.Participant):

    def __init__(self, expid, trials, outdir, task, ss_del, ll_shortdel, ll_longdel, ss_smallrew, ll_rew):
        super().__init__(expid, trials, outdir, task)

        self.engine = self.create_dd_engine(self.task, ss_del, ll_shortdel, ll_longdel, ss_smallrew, ll_rew)

        # Compute an optimal design for the first trial
        self.design = self.engine.get_design('optimal')

        # Experiment settingsguis output dataframe
        dict_simulsettings = {'Immediate Option Delay': [ss_del],
                              'Shortest Delay': [ll_shortdel],
                              'Longest Delay': [ll_longdel],
                              'Smallest Smaller Sooner Reward': [ss_smallrew],
                              'Largest Smaller Sooner Reward': [(float(ll_rew) - float(ss_smallrew))],
                              'Larger Later Reward': [ll_rew]
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

    def updateoutput(self, response, trial):

        df_simultrial = {
            'trial': [trial],
            'SSAmount': [float(self.design['r_ss'])],
            'LLAmount': [float(self.design['r_ll'])],
            'LLDelay': [float(self.design['t_ll'])],
            'response': [response],
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

    def __init__(self, expid, trials, outdir, task, design, minimum, maximum):
        super().__init__(expid, trials, outdir, task)

        self.design = design
        self.maximum = float(maximum)
        self.minimum = float(minimum)
        self.trialdesign = []

        self.create_design()

        # Experiment settingsguis output dataframe
        dict_simulsettings = {'Design': [design],
                              'Minimum Reward': [minimum],
                              'Maximum Reward': [maximum]
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

    def updateoutput(self, response, trial):

        df_simultrial = {
            'trial': [trial],
            'cond': [self.state],
            'SureAmount': [str('{:.2f}'.format(self.trialdesign[0]))],
            'RiskyAmount': [self.maximum],
            'RiskyProbability': [str(self.trialdesign[1])],
            'response': [response]
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

                inst = 'In this task, you will be making choices between\n guarantees of winning or losing some money' \
                       ' or taking\ngambles to win more money or lose less money.'

            case 2:

                inst = 'You will use the keyboard to make your choice\nbetween the pretend rewards shown on the ' \
                       'left and\nright side of the screen.'

            case 3:

                inst = 'Even though these money rewards are pretend,\ntry to choose as if you were being offered ' \
                       'these rewards\nfor real.'

            case _:

                inst = 'Let the experimenter know you are ready.'

        return inst


class CEDParticipant(participant.Participant):

    def __init__(self, expid, trials, outdir, task, smallrew, largerew):
        super().__init__(expid, trials, outdir, task)

        # Experiment settingsguis output dataframe
        dict_simulsettings = {
                              'Smallest Reward': [smallrew],
                              'Largest Reward': [largerew]
                              }

        self.set_settings(dict_simulsettings)

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

    def updateoutput(self, response, trial):

        df_simultrial = {
            'trial': [trial],
            'left task': [float(self.design['r_ss'])],
            'left value': [float(self.design['r_ll'])],
            'right task': [float(self.design['t_ll'])],
            'right value': [response],
            'response': [response]
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

                inst = 'Remember those memory tasks? Now you will make\ndecisions about these tasks.'

            case 2:

                inst = 'You will first see one option by itself. Use this\ntime to think about how much you would ' \
                       'like to repeat\nthe task for that amount of money.'

            case 3:

                inst = 'Next, you will see two options, each including a\ndollar amount and a task.'

            case 4:

                inst = 'For example, you may have to choose between\ncompleting extra rounds of the easiest task ' \
                       'for $1\nor extra rounds of the hardest task for $7.'

            case 5:

                inst = 'There is no right answer! Just choose the option\nthat you would prefer.'

            case 6:

                inst = 'Any one of the choices you make could determine\nwhat task you complete extra rounds of and' \
                       ' how much\nyou are paid for completing that task.'

            case 7:

                inst = 'We will pick one of your choices at random. It does\nnot matter how well you do on the task ' \
                       'chosen. You\nwill be paid as long as you maintain your effort.'

            case 8:

                inst = 'Take as much time as you need to choose. After a\nwhile, the decision will disappear, but ' \
                       'those choices\nwill be shown again at the end.'

            case _:

                inst = 'Let the experimenter know you are ready.'

        return inst
