from adopy.tasks.dd import *
from adopy.tasks.cra import *
from adopy import Engine

import numpy as np
import pandas as pd
import random

import xlsxwriter
import os
import time


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
            'Number of trials': [self.trials]
        }

        self.df_settings = pd.DataFrame(self.dict_settings)

        # Task Performance
        self.df_performance = pd.DataFrame()

    def get_trials(self):
        return int(self.trials)

    def set_settings(self, append):
        self.df_settings = pd.concat([self.df_settings, append])

    def set_performance(self, append):
        self.df_performance = pd.concat([self.df_performance, append])

    def output(self):
        if self.task == TaskDD():
            taskstr = 'DD_'
        else:
            taskstr = ''

        writer = pd.ExcelWriter(taskstr + self.expid + '.xlsx', engine='xlsxwriter')

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

        df_simulsettings = pd.DataFrame(dict_simulsettings)

        self.set_settings(df_simulsettings)

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

        self.create_stim(self.task, min, max, design)

        # Experiment settings output dataframe
        dict_simulsettings = {'Design': [design],
                              'Minimum Reward': [min],
                              'Maximum Reward': [max]
                              }

        df_simulsettings = pd.DataFrame(dict_simulsettings)

        self.set_settings(df_simulsettings)

    def create_stim(self, task, min, max, design):

        self.gains = np.arange(int(min), int(max)-1, 1)
        self.losses = np.arange(int(min), int(max)-1, 1)
        probabilities = np.arange(1, 100, 1)

    def get_design_text(self):

        if int(self.design['t_ss']) == 0:
            leftstring = 'Getting $' + str('{:.2f}'.format(self.design['r_ss'])) + '\nnow'

        else:
            leftstring = 'Getting $' + str('{:.2f}'.format(self.design['r_ll'])) + '\nafter '\
                         + str(int(self.design['t_ss'])) + ' weeks'

        rightstring = 'Getting $' + str('{:.2f}'.format(self.design['r_ll'])) + '\nafter '\
                      + str(int(self.design['t_ll'])) + ' weeks'

        return [leftstring, rightstring]

    def updateoutput(self, response, trial):

        df_simultrial = {
            'trial': [trial],
            'SureAmount': [float(self.design['r_ss'])],
            'RiskyAmount': [float(self.design['r_ll'])],
            'RiskyProbability': [float(self.design['t_ll'])],
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

        df_simulsettings = pd.DataFrame(dict_simulsettings)

        self.set_settings(df_simulsettings)

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

        df_simulsettings = pd.DataFrame(dict_simulsettings)

        self.set_settings(df_simulsettings)

    def create_artt_engine(self, task, risklist, amblist, rewmin, rewmax):

        start = time.time()
        print("create")

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

        end = time.time()
        print(end - start)

        return engine

    def get_design_text(self):

        start = time.time()
        print("get text")

        fixedstring = str('{:.2f}'.format(self.design['r_fix']))

        otherstring = str('{:.2f}'.format(self.design['r_var']))

        end = time.time()
        print(end - start)

        return [fixedstring, otherstring, int(self.design['a_var']*100), int(self.design['p_var']*100)]

    def engineupdate(self, response):

        start = time.time()
        print("update engine")

        # Update engine with the response and current design
        self.engine.update(self.design, response)

        end = time.time()
        print(end - start)

        start2 = time.time()
        print("get design")

        # Generate new optimal design based on previous design and response
        self.design = self.engine.get_design('optimal')

        end2 = time.time()
        print(end2 - start2)

    def updateoutput(self, response, trial):

        start = time.time()
        print("update output")

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

        end = time.time()
        print(end - start)


class PrParticipant(Participant):

    def __init__(self, expid, trials, outdir, task, design, stt):
        super().__init__(expid, trials, outdir, task)

        design = design
        stt = stt

        if stt == 1:
            self.structstr = 'STT' + ('ST' * (int(design) - 1))
            self.structure = list(self.structstr)

        else:
            self.structstr = 'ST' * int(design)
            self.structure = list(self.structstr)

        # Experiment settings output dataframe
        dict_simulsettings = {
                              'Design': [self.structstr]
                              }

        df_simulsettings = pd.DataFrame(dict_simulsettings)

        self.set_settings(df_simulsettings)

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
