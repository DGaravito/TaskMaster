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
        os.chdir(self.outdir)

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

        self.df_settings.join(pd.DataFrame(
            append, index=self.df_settings.index
        ))

    def set_performance(self, append):
        self.df_performance = pd.concat(
            [
                self.df_performance, append
            ]
        )

    def output(self):

        if self.task == TaskDD():
            taskstr = '_DD'

        elif self.task == 'Pair Recall Memory':
            taskstr = '_PR'

        elif self.task == 'Perceptual Bias Task':
            taskstr = '_PBT'

        elif self.task in ['1-back', '2-back', '3-back', '4-back']:
            taskstr = '_' + self.task

        else:
            taskstr = '_'

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

    def __init__(self, expid, trials, outdir, task, design, min, max):
        super().__init__(expid, trials, outdir, task)

        self.design = design
        self.max = max
        self.trialdesign = []

        self.create_stim(min, max)

        # Experiment settings output dataframe
        dict_simulsettings = {'Design': [design],
                              'Minimum Reward': [min],
                              'Maximum Reward': [max]
                              }

        self.set_settings(dict_simulsettings)

    def create_stim(self, min, max):
        """
        Uses the parameters from the settings input and makes a set of dictionaries for gamble probabilities and sure
        values
        :param min: the minimum reward value possible, as an integer, given by participants
        :param max: the maximum reward value possible, as an integer, given by participants
        :return: Does not return a value, instead creates the class dictionaries and then calls set design text to make
        the first trial
        """

        if self.design == 'Gains only':

            sureamounts = np.arange(int(min), int(max) - .5, .5)
            self.suredict = dict(zip(sureamounts, sureamounts))

            riskyprobabilities = np.arange(.01, 1, .01)
            riskkeys = riskyprobabilities * max

            self.riskdict = dict(zip(riskkeys, riskyprobabilities))

        elif self.design == 'Losses only':

            sureamounts = np.arange(int(min), int(max)-.5, .5)
            surekeys = sureamounts * -1

            self.suredict = dict(zip(surekeys, sureamounts))

            riskyprobabilities = np.arange(.01, 1, .01)
            riskkeys = riskyprobabilities * max * -1

            self.riskdict = dict(zip(riskkeys, riskyprobabilities))

        else:

            # Gains
            suregainamounts = np.arange(int(min), int(max) - .5, .5)
            self.suregaindict = dict(zip(suregainamounts, suregainamounts))

            riskygainprobabilities = np.arange(.01, 1, .01)
            riskgainkeys = riskygainprobabilities * max

            self.riskgaindict = dict(zip(riskgainkeys, riskygainprobabilities))

            # Losses
            surelossamounts = np.arange(int(min), int(max) - .5, .5)
            surelosskeys = surelossamounts * -1

            self.surelossdict = dict(zip(surelosskeys, surelossamounts))

            riskylossprobabilities = np.arange(.01, 1, .01)
            risklosskeys = riskylossprobabilities * max * -1

            self.risklossdict = dict(zip(risklosskeys, riskylossprobabilities))

        self.set_design_text()

    def set_design_text(self, trial=0):

        """
        Gets the actual text used in the design
        :param trial: This is the trial number, as an integer, that the experiment is on
        :return: Creates self.trialdesign
        """

        # If you're using gains and losses
        if self.design == 'Gains and losses':

            # If the trial was even, work with gains, otherwise, use the else statement for losses
            if ((trial + 1) % 2) != 0:

                # Pick a random reward for the sure option and probability for the gamble option
                self.currentsuregainkey = random.choice(self.suregaindict)
                self.currentriskgainkey = random.choice(self.riskgaindict)

                # The following if-else statement looks at if there is just one value left in a dictionary. If so,
                # then you don't want to pop, as that would leave an empty dictionary, resulting in errors next time
                # you tried to get the trial info. We use get() instead so that the key:value pair remains in the
                # dictionary, which continues to have a length of 1
                if len(self.suregaindict) >= 1 & len(self.riskgaindict) >= 1:

                    # actually grab the values for the trial design, which is a list of integers
                    trialdesign = [
                        self.suregaindict.pop(self.currentsuregainkey),
                        self.riskgaindict.pop(self.currentriskgainkey)
                    ]

                elif len(self.suregaindict) >= 1 & len(self.riskgaindict) == 1:

                    trialdesign = [
                        self.suregaindict.pop(self.currentsuregainkey),
                        self.riskgaindict.get(self.currentriskgainkey)
                    ]

                elif len(self.suregaindict) == 1 & len(self.riskgaindict) >= 1:

                    trialdesign = [
                        self.suregaindict.get(self.currentsuregainkey),
                        self.riskgaindict.pop(self.currentriskgainkey)
                    ]

                else:

                    trialdesign = [
                        self.suregaindict.get(self.currentsuregainkey),
                        self.riskgaindict.get(self.currentriskgainkey)
                    ]

            else:

                # Same as above: do the random selection and then go through the big if-else statement
                self.currentsurelosskey = random.choice(self.surelossdict)
                self.currentrisklosskey = random.choice(self.risklossdict)

                if len(self.surelossdict) >= 1 & len(self.risklossdict) >= 1:

                    # actually grap the values for the trial design, which is a list of integers
                    trialdesign = [
                        self.surelossdict.pop(self.currentsurelosskey),
                        self.risklossdict.pop(self.currentrisklosskey)
                    ]

                elif len(self.surelossdict) >= 1 & len(self.risklossdict) == 1:

                    trialdesign = [
                        self.surelossdict.pop(self.currentsurelosskey),
                        self.risklossdict.get(self.currentrisklosskey)
                    ]

                elif len(self.surelossdict) == 1 & len(self.risklossdict) >= 1:

                    trialdesign = [
                        self.surelossdict.get(self.currentsurelosskey),
                        self.risklossdict.pop(self.currentrisklosskey)
                    ]

                else:

                    trialdesign = [
                        self.surelossdict.get(self.currentsurelosskey),
                        self.risklossdict.get(self.currentrisklosskey)
                    ]

        else:

            # This whole section is if you just have gains or just have losses. Same concept though: we select a random
            # value for the sure option and probability for the gamble
            self.currentsurekey = random.choice(self.suredict)
            self.currentriskkey = random.choice(self.riskdict)

            # Then we have to see if the dictionaries have more than one key:value pair left. If so, we can pop and
            # not have to worry about errors. If not, then we use get and keep the length at 1
            if len(self.suredict) >= 1 & len(self.riskdict) >= 1:

                # actually grap the values for the trial design, which is a list of integers
                trialdesign = [
                    self.suredict.pop(self.currentsurekey),
                    self.riskdict.pop(self.currentriskkey)
                ]

            elif len(self.suredict) >= 1 & len(self.riskdict) == 1:

                trialdesign = [
                    self.suredict.pop(self.currentsurekey),
                    self.riskdict.get(self.currentriskkey)
                ]

            elif len(self.suredict) == 1 & len(self.riskdict) >= 1:

                trialdesign = [
                    self.suredict.get(self.currentsurekey),
                    self.riskdict.pop(self.currentriskkey)
                ]

            else:

                trialdesign = [
                    self.suredict.get(self.currentsurekey),
                    self.riskdict.get(self.currentriskkey)
                ]

        self.trialdesign = trialdesign

    def get_design_text(self):

        """
        Looks at self.trialdesign and returns strings for the GUI
        :return: left text (sure), right text (gamble), and gamble probability
        """

        # Set up the left string for sure value
        leftstring = '$' + str('{:.2f}'.format(self.trialdesign[0])) + ' for sure'

        # Set up the right string for risky gamble
        rightstring = 'A ' + str(self.trialdesign[1]) + '% chance for ' +\
                      str('{:.2f}'.format(self.max))

        # Set the probability bar for the risky gamble
        barvalue = self.trialdesign[1] * 100

        # Return the values to the gui
        return [leftstring, rightstring, barvalue]

    def update(self, response, trial):
        """
        Updates the dictionaries for experimental parameters based on the participant's response (and the type of trial
        if you are using gains and losses)
        :param response: A binary 0 or 1 depending on if the participant chose the sure option (0) or gamble (1)
        :param trial: The trial (in an integer format) that the participant just completed
        :return: N/A
        """

        # Flip a coin for later - 1 or 2
        coinflip = random.randint(1, 2)

        # If you are using gains and losses, use the top; otherwise, use the else
        if self.design == 'Gains and losses':

            # If the trial is an even number, it was a gains trial and use the top; otherwise, it was loss and use else
            if ((trial + 1) % 2) != 0:

                # If the participant chose the sure thing, use the top; otherwise, use else
                if response == 0:

                    # If the coin flip resulted in a 1, use the top; otherwise, use else
                    if coinflip == 1:

                        # Loop for every key (i.e., EV of the possible reward value in the sure option) in the sure gain
                        # dictionary
                        for key in self.suregaindict:

                            # If the EV for that key is greater in value compared to EV of the option that
                            # was just used AND the dictionary is more than 1 in length (to avoid an empty dict)...
                            if int(key) > self.currentsuregainkey & len(self.suregaindict) > 1:

                                # ...Delete that option
                                del self.suregaindict[key]

                    else:

                        # Loop for every key (i.e., EV of the possible reward value in the risk option) in the risky
                        # gain dictionary
                        for key in self.riskgaindict:

                            # If the EV for that key is lesser in value compared to EV of the option that
                            # was just used...
                            if int(key) < self.currentriskgainkey & len(self.riskgaindict) > 1:

                                # ...Delete that option
                                del self.riskgaindict[key]

                else:

                    # This does the same thing as the above but is responding to the participant choosing the risky
                    # option
                    if coinflip == 1:

                        for key in self.suregaindict:

                            # Remove all values for the sure option that would have a lesser EV than what the
                            # participant just rejected
                            if int(key) < self.currentsuregainkey & len(self.suregaindict) > 1:

                                del self.suregaindict[key]

                    else:

                        for key in self.riskgaindict:

                            # Remove all values for the risky option that would have a greater EV than what the
                            # participant just accepted
                            if int(key) > self.currentriskgainkey & len(self.riskgaindict) > 1:

                                del self.riskgaindict[key]

            else:

                # This section is the same as all that was above but if the trial just conducted was a loss trial.
                if response == 0:

                    # If the participant chose the sure loss...
                    if coinflip == 1:

                        # And the coin flipped 1...
                        for key in self.surelossdict:

                            # Then look at the EVs for all the possible sure loss options...
                            if int(key) > self.currentsurelosskey & len(self.surelossdict) > 1:

                                # And delete those where the EV for the sure option is greater.
                                del self.surelossdict[key]

                    else:

                        # If the coin flipped 2...
                        for key in self.risklossdict:

                            # Then look at the EVs for all the possible risky loss options...
                            if int(key) < self.currentrisklosskey & len(self.risklossdict) > 1:

                                # And delete those where the EV for the sure option is less.
                                del self.risklossdict[key]

                else:

                    # If the participant chose the risky option...
                    if coinflip == 1:

                        # And the coin flipped 1...
                        for key in self.surelossdict:

                            # Then look at the EVs for all the possible sure loss options...
                            if int(key) < self.currentsurelosskey & len(self.surelossdict) > 1:

                                # And delete those where the EV for the sure option is less.
                                del self.surelossdict[key]

                    else:

                        # If the coin flipped 2...
                        for key in self.risklossdict:

                            # Then look at the EVs for all the possible risky loss options...
                            if int(key) > self.currentrisklosskey & len(self.risklossdict) > 1:

                                # And delete those where the EV for the risky option is more.
                                del self.risklossdict[key]

        else:

            # If you don't have both gains and losses and instead have gains or losses, then the above is condensed
            if response == 0:

                if coinflip == 1:

                    for key in self.suredict:

                        if int(key) > self.currentsurekey & len(self.suredict) > 1:

                            del self.suredict[key]

                else:

                    for key in self.riskdict:

                        if int(key) < self.currentriskkey & len(self.riskdict) > 1:

                            del self.riskdict[key]

            else:

                if coinflip == 1:

                    for key in self.suredict:

                        if int(key) < self.currentsurekey & len(self.suredict) > 1:

                            del self.suredict[key]

                else:

                    for key in self.riskdict:

                        if int(key) > self.currentriskkey & len(self.riskdict) > 1:

                            del self.riskdict[key]

        # Now, given the dictionaries are adjusted, generate a new random set of parameters
        self.set_design_text(trial)

    def updateoutput(self, response, trial):

        df_simultrial = {
            'trial': [trial],
            'SureAmount': [str('{:.2f}'.format(self.trialdesign[0]))],
            'RiskyAmount': [self.max],
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

    def __init__(self, expid, trials, outdir, task, risklist, amblist, rewmin, rewmax):
        super().__init__(expid, trials, outdir, task)

        self.engine = self.create_artt_engine(self.task, risklist, amblist, rewmin, rewmax)

        # Compute an optimal design for the first trial
        self.design = self.engine.get_design('optimal')

        # Experiment settings output dataframe
        dict_simulsettings = {'Risky Probabilities': [risklist],
                              'Ambiguous Probabilities': [amblist],
                              'Smallest Reward': [rewmin],
                              'Largest Reward': [rewmax]
                              }

        self.set_settings(dict_simulsettings)

    def create_artt_engine(self, task, risklist, amblist, rewmin, rewmax):

        model = ModelLinear()

        r_var = np.arange(int(rewmin), int(rewmax), .5)
        r_fix = np.arange(int(rewmin), (int(rewmax)/2), .5)

        rewards = np.array([
            [rv, rf] for rv in r_var for rf in r_fix if rv > rf
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

        fixedstring = str('{:.2f}'.format(self.design['r_fix']))

        otherstring = str('{:.2f}'.format(self.design['r_var']))

        return [fixedstring, otherstring, int(self.design['a_var']*100), int(self.design['p_var']*100)]

    def engineupdate(self, response):

        # Update engine with the response and current design
        self.engine.update(self.design, response)

        # Generate new optimal design based on previous design and response
        self.design = self.engine.get_design('optimal')

    def updateoutput(self, response, trial):

        df_simultrial = {
            'trial': [trial],
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

        self.rounds = rounds
        self.backlist = ['1', '1', '1', '1']

        # Experiment settings output dataframe
        dict_simulsettings = {
            'Rounds': [rounds]
        }

        self.set_settings(dict_simulsettings)

    def nextround(self, round):

        if round == self.rounds:

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


class PBTParticipant(Participant):

    def __init__(self, expid, trials, outdir, task, rounds):
        super().__init__(expid, trials, outdir, task)

        self.rounds = rounds
        self.globallocal = random.choice(['Global', 'Local'])
        self.instructions = 0

        multnum = int(int(trials)/4)
        picturenames = ['PBT_DCC.BMP', 'PBT_DCS.BMP', 'PBT_DSC.BMP', 'PBT_DSS.BMP']
        multiplier = [multnum, multnum, multnum, multnum]
        self.piclist = sum([[s] * n for s, n in zip(picturenames, multiplier)], [])

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

            prompt = 'Please let the researcher know you are ready'

        return prompt

    def get_trial_pic(self):

        pic = self.picorder.pop()

        return [pic]

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

    def get_instructions(self, block_type, instruction):

        if block_type == 'Global':

            if instruction == 1:

                inst = 'pretend something is here about global stuff'

            else:

                inst = 'pretend something else is here about global stuff'

        else:

            if instruction == 1:

                inst = 'pretend something is here about local stuff'

            else:

                inst = 'pretend something else is here about local stuff'

        return inst
