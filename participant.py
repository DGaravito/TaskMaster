from adopy.tasks.dd import *
from adopy.tasks.cra import *
from adopy import Engine

import numpy as np
import pandas as pd
import random
import string

import xlsxwriter
import os


class Participant(object):
    def __init__(self, expid, trials, outdir, task):

        self.expid = expid

        self.trials = trials

        self.outdir = outdir

        self.task = task

        # Experiment settings output dataframe
        self.dict_settings = {
            'Participant ID': [self.expid],
            'Task': [self.task],
            'Number of trials': [self.trials]
        }

        self.df_settings = pd.DataFrame(self.dict_settings)

        # Task Performance
        self.df_performance = pd.DataFrame()

    def get_trials(self):
        return int(self.trials)

    def set_settings(self, append):

        self.df_settings = self.df_settings.join(
            pd.DataFrame(
                append,
                index=self.df_settings.index
            )
        )

    def set_performance(self, append):
        self.df_performance = pd.concat(
            [
                self.df_performance, append
            ]
        )

    def output(self):

        match self.task:

            case TaskDD():
                taskstr = '_DD'

            case 'Probability Discounting':
                taskstr = '_PD'

            case 'CogED Task':
                taskstr = '_CEDT'

            case TaskCRA():
                taskstr = '_ARTT'

            case 'Risk Aversion':
                taskstr = '_RA'

            case 'Framing Task':
                taskstr = '_Framing'

            case 'Beads Task':
                taskstr = '_Beads'

            case 'Perceptual Bias Task':
                taskstr = '_PBT'

            case 'Negative Attention Capture':
                taskstr = '_NACT'

            case 'Stop-Signal Task':
                taskstr = '_SS'

            case 'Emo Go/No-Go':
                taskstr = '_EGNG'

            case 'Pair Recall Memory':
                taskstr = '_PR'

            case '1-back':
                taskstr = '_' + self.task

            case '2-back':
                taskstr = '_' + self.task

            case '3-back':
                taskstr = '_' + self.task

            case '4-back':
                taskstr = '_' + self.task

            case _:
                taskstr = '_'

        os.chdir(self.outdir)

        writer = pd.ExcelWriter(self.expid + taskstr + '.xlsx', engine='xlsxwriter')

        # Write each dataframe to a different worksheet.
        self.df_settings.to_excel(writer, sheet_name='Sheet1')
        self.df_performance.to_excel(writer, sheet_name='Sheet2')

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()


class DdParticipant(Participant):

    def __init__(self, expid, trials, outdir, task, ss_del, ll_shortdel, ll_longdel, ss_smallrew, ll_rew):
        super().__init__(expid, trials, outdir, task)

        self.engine = self.create_dd_engine(self.task, ss_del, ll_shortdel, ll_longdel, ss_smallrew, ll_rew)

        # Compute an optimal design for the first trial
        self.design = self.engine.get_design('optimal')

        # Experiment settings output dataframe
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


class PdParticipant(Participant):

    def __init__(self, expid, trials, outdir, task, design, minimum, maximum):
        super().__init__(expid, trials, outdir, task)

        self.design = design
        self.maximum = float(maximum)
        self.minimum = float(minimum)
        self.trialdesign = []

        self.create_design()

        # Experiment settings output dataframe
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

        # Return the values to the gui
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


class CEDTParticipant(Participant):

    def __init__(self, expid, trials, outdir, task, ss_del, ll_shortdel, ll_longdel, ss_smallrew, ll_rew):
        super().__init__(expid, trials, outdir, task)

        self.engine = self.create_dd_engine(self.task, ss_del, ll_shortdel, ll_longdel, ss_smallrew, ll_rew)

        # Compute an optimal design for the first trial
        self.design = self.engine.get_design('optimal')

        # Experiment settings output dataframe
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


class ARTTParticipant(Participant):

    def __init__(self, expid, trials, outdir, task, risklist, amblist, rewmin, rewmax, structure):
        super().__init__(expid, trials, outdir, task)

        self.structure = structure

        self.create_structure()

        self.engine = self.create_artt_engine(self.task, risklist, amblist, rewmin, rewmax)

        # Compute an optimal design for the first trial
        self.design = self.engine.get_design('optimal')

        # Experiment settings output dataframe
        dict_simulsettings = {'Risky Probabilities': [risklist],
                              'Ambiguous Probabilities': [amblist],
                              'Fixed Reward': [rewmin],
                              'Largest Reward': [rewmax],
                              'Design': [structure]
                              }

        self.set_settings(dict_simulsettings)

    def create_structure(self):
        """
        If you want both gains and losses, then it creates a random order for gain and loss questions
        :return: Does not return a value, instead creates the class dictionaries and then calls set design text to make
        the first trial
        """

        if self.structure == 'Gains and Losses':

            multnum = int(self.get_trials() / 2)
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

            picstring = 'ARTT_risk_' + str(round(self.design['p_var'] * 100)) + '.bmp'

        else:

            picstring = 'ARTT_ambig_' + str(round(self.design['a_var'] * 100)) + '.bmp'

        return [fixedstring, otherstring, picstring]

    def engineupdate(self, response):

        # Update engine with the response and current design
        self.engine.update(self.design, response)

        # Generate new optimal design based on previous design and response
        self.design = self.engine.get_design('optimal')

    def updateoutput(self, response, trial):

        df_simultrial = {
            'trial': [trial],
            'cond': [self.state],
            'Proportion Ambiguous': float(self.design['a_var']),
            'Proportion Risky': [float(self.design['p_var'])],
            'Fixed Reward': [self.design['r_fix']],
            'Variable Reward': [self.design['r_var']],
            'response': [response],
            'mean_alpha': [self.engine.post_mean[0]],
            'mean_beta': [self.engine.post_mean[1]],
            'mean_gamma': [self.engine.post_mean[2]],
            'sd_alpha': [self.engine.post_sd[0]],
            'sd_beta': [self.engine.post_sd[1]],
            'sd_gamma': [self.engine.post_sd[2]]
        }

        df_simultrial = pd.DataFrame(data=df_simultrial)
        self.set_performance(df_simultrial)


class RAParticipant(Participant):

    def __init__(self, expid, trials, outdir, task, minimum, maximum):
        super().__init__(expid, trials, outdir, task)

        self.trialtext = []

        self.create_stim(minimum, maximum)

        # Experiment settings output dataframe
        dict_simulsettings = {'Minimum Reward': [minimum],
                              'Maximum Reward': [maximum]
                              }

        self.set_settings(dict_simulsettings)

    def create_stim(self, minimum, maximum):
        """
        Uses the parameters from the settings input and makes a set of dictionaries for gamble probabilities and sure
        values
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

        # Return the values to the gui
        return [gainstring, lossstring]

    def updateoutput(self, response, trial):

        df_simultrial = {
            'trial': [trial],
            'gain': [str('{:.2f}'.format(self.gainint))],
            'loss': [str('{:.2f}'.format(self.lossfloat))],
            'certain': [0],
            'response': [response]
        }

        df_simultrial = pd.DataFrame(data=df_simultrial)
        self.set_performance(df_simultrial)


class FrameParticipant(Participant):

    def __init__(self, expid, trials, outdir, task, minimum, maximum, design, ftt):
        super().__init__(expid, trials, outdir, task)

        self.design = design
        self.ftt = ftt
        self.maxrew = maximum
        self.minrew = minimum
        self.order = []
        self.trialdesign = []

        self.set_order()

        # Experiment settings output dataframe
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

        random.shuffle(self.order)

    def set_design_text(self):
        """
        Gets the actual text used in the design
        :return: Creates self.trialdesign
        """

        gambleprob = random.uniform(.01, .99)
        gambleamount = random.uniform(float(self.minrew), float(self.maxrew))
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

        # Return the values to the gui
        return [leftstring, righttopstring, rightbottomstring]

    def updateoutput(self, response, trial):

        df_simultrial = {
            'trial': [trial],
            'cond': [str(self.state)],
            'SureAmount': [str('{:.2f}'.format(self.trialdesign[0]))],
            'RiskyAmount': [str('{:.2f}'.format(self.trialdesign[2]))],
            'RiskyProbability': [self.trialdesign[1]],
            'response': [response]
        }

        df_simultrial = pd.DataFrame(data=df_simultrial)
        self.set_performance(df_simultrial)


class BeadsParticipant(Participant):

    def __init__(self, expid, rounds, outdir, task):
        super().__init__(expid, rounds, outdir, task)

        self.blue_jar = ['BeadsTask_BlueBead',
                         'BeadsTask_BlueBead',
                         'BeadsTask_BlueBead',
                         'BeadsTask_BlueBead',
                         'BeadsTask_RedBead']

        self.red_jar = ['BeadsTask_BlueBead',
                        'BeadsTask_RedBead',
                        'BeadsTask_RedBead',
                        'BeadsTask_RedBead',
                        'BeadsTask_RedBead']

    def nextround(self, completedround):

        if completedround == self.get_trials():

            prompt = 'Thank you! This task is complete.'

        else:

            jarint = random.randint(1, 2)

            if jarint == 1:

                self.jarname = 'Blue'
                self.jar = self.blue_jar

            else:

                self.jarname = 'Red'
                self.jar = self.red_jar

            prompt = ''

        return prompt

    def get_bead(self):

        self.pic = random.choice(self.jar)

        return self.pic

    def updateoutput(self, currentround, beadspicked, response=0, pick='None'):
        """
        updates the performance dataframe for each trial, and if they chose to pick a jar, were they correct
        :param currentround: the number of the current round
        :param beadspicked: the number of the trial that was just completed
        :param response: integer with either 0 or 1 depending on if the person chose to draw a bead or pick a jar
        :param pick: if they picked a jar, what jar did they pick
        :return: updates the performance dataframe in the superclass
        """

        correct = 0

        if response == 1:

            if pick == self.jarname:

                correct = 1

        df_simultrial = {
            'round': [currentround],
            'beads': [beadspicked],
            'last bead': [self.pic],
            'response': [response],
            'jar picked': [pick],
            'correct': [correct]
        }

        df_simultrial = pd.DataFrame(data=df_simultrial)

        self.set_performance(df_simultrial)

    def get_instructions(self, instruction):

        match instruction:

            case 1:

                inst = 'In this game, the computer is going to take beds out\nof one of two jars on the screen.'

            case 2:

                inst = 'Your goal is to figure out from which jar (left\nor right) the computer took out the beads.'

            case 3:

                inst = 'You are going to see two clear jars with 100 beads\nin each jar'

            case 4:

                inst = 'One jar has 80% blue beads and 20% red beads.\nThe other jar has the opposite, with 80% read' \
                       ' beads and 20% blue beads.'

            case 5:

                inst = 'The computer will take beads from ONE jar and\nwill show you the color of the bead it took out' \
                       ' from that jar.'

            case 6:

                inst = 'The computer will select form the SAME jar until\nyou make a choice (of left or right jar).'

            case 7:

                inst = 'The bead the computer takes out will be shown\nto you one at a time in the middle of the' \
                       ' screen.'

            case 8:

                inst = 'If you want to see the computer pick a bead,\npress the \"M\" key.'

            case 9:

                inst = 'When you are ready to decide which jar the computer\nis selecting the beads from, press the' \
                       ' \"C\" key'

            case 10:

                inst = 'The computer will continue to select from the SAME\njar until you\'ve made a decision about' \
                       ' which jar the computer\nwas picking from.'

            case 11:

                inst = 'You can make a decision any time after seeing the first bead.'

            case 12:

                inst = 'You can see up to 20 beads. After the bead is shown\nto you, it will be put back into the' \
                       'same jar before selecting\nthe next bead.'

            case 13:

                inst = 'You will be able to see all of the beads that have\nbeen drawn by clicking on the button in' \
                       'the bottom right of the screen.'

            case 14:

                inst = 'Remember, you can make a decision anytime after\nseeing the first bead.'

            case _:

                inst = 'Let the experimenter know you are ready.'

        return inst


class PBTParticipant(Participant):

    def __init__(self, expid, trials, outdir, task, rounds):
        super().__init__(expid, trials, outdir, task)

        self.rounds = int(rounds)
        self.globallocal = random.choice(['Global', 'Local'])

        multnum = int(int(trials)/4)
        picturenames = ['PBT_DCC.BMP', 'PBT_DCS.BMP', 'PBT_DSC.BMP', 'PBT_DSS.BMP']
        multiplier = [multnum, multnum, multnum, multnum]
        self.piclist = sum([[s] * n for s, n in zip(picturenames, multiplier)], [])

        self.picorder = list(self.piclist)
        random.shuffle(self.picorder)

        # Experiment settings output dataframe
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

    def updateoutput(self, trial, pic, time, response=3):
        """
        evaluates whether the person got the n-back correct based on their response
        :param trial: the number of the trial that was just completed
        :param pic: string with the picture name in it, so we can see if the participant gave the correct answer
        :param time: participant's reaction time
        :param response: integer with either 0 or 1 depending on if the person chose x or square. Default is 3 in case
        the participant doesn't answer in time.
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
            'response': [response],
            'reaction time': [time],
            'correct': [correct]
        }

        df_simultrial = pd.DataFrame(data=df_simultrial)

        self.set_performance(df_simultrial)

    def get_instructions(self, block_type, instint):

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

                        inst = 'Ignore the small elements. Press \"M\" if the\nlarge figure is a SQUARE and \"C\" if' \
                               ' the large figure\nis a CROSS.'

                    case 5:

                        inst = 'Continue for an example picture.'

                    case 7:

                        inst = 'There, the large figure was a SQUARE,\nso you would press \"M\".'

                    case 8:

                        inst = 'Continue for another example.'

                    case 10:

                        inst = 'There, the large figure was a CROSS,\nso you would press \"C\".'

                    case _:

                        inst = 'Please let the experimenter know\nwhen you are ready.'

            else:

                match instint:

                    case 3:

                        inst = 'Your task is to decide whether the SMALL figure\nis a square or cross.'

                    case 4:

                        inst = 'Ignore the small elements. Press \"M\" if the\nsmall figure is a SQUARE and \"C\" if' \
                               ' the small figure\nis a CROSS.'

                    case 5:

                        inst = 'Continue for an example picture.'

                    case 7:

                        inst = 'There, the small figure was a CROSS,\nso you would press \"C\".'

                    case 8:

                        inst = 'Continue for another example.'

                    case 10:

                        inst = 'There, the small figure was a SQUARE,\nso you would press \"M\".'

                    case _:

                        inst = 'Please let the experimenter know\nwhen you are ready.'

        return inst


class PrParticipant(Participant):

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

        # Experiment settings output dataframe
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


class NbParticipant(Participant):

    def __init__(self, expid, trials, outdir, task, rounds):

        super().__init__(expid, trials, outdir, task)

        self.rounds = int(rounds)
        self.backlist = ['1', '1', '1', '1']

        # Experiment settings output dataframe
        dict_simulsettings = {
            'Rounds': [rounds]
        }

        self.set_settings(dict_simulsettings)

    def nextround(self, roundsdone):

        if roundsdone == self.rounds:

            prompt = 'Thank you! This task is complete.'

        else:

            self.backlist = ['1', '1', '1', '1']

            prompt = 'Please let the researcher know you are ready'

        return prompt

    def get_trial_text(self):

        newletter = random.choice(string.ascii_uppercase)

        self.backlist.append(newletter)

        return newletter

    def updateoutput(self, trial, response=3):
        """
        evaluates whether the person got the n-back correct based on their response
        :param trial: the trial that was just completed
        :param response: integer with either 0 or 1 depending on if the person thought the letter was a false-alarm
        or a target. Default is 3 in case the participant doesn't answer in time.
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
            'response': [response],
            'correct': [correct]
        }

        df_simultrial = pd.DataFrame(data=df_simultrial)

        self.set_performance(df_simultrial)
