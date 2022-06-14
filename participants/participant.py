from adopy.tasks.dd import *
from adopy.tasks.cra import *
import pandas as pd

import os
import xlsxwriter


class Participant(object):
    def __init__(self, expid, trials, session, outdir, task, buttonbox='No', eyetrack='No', fmri='No'):

        # set up keys depending on buttonbox option
        if buttonbox == 'Yes':
            self.leftkey = ['1']
            self.rightkey = ['2']

        else:
            self.leftkey = ['C', 'c']
            self.rightkey = ['M', 'm']

        # Set up class variables
        self.eyetracking = eyetrack
        self.fmri = fmri
        self.expid = expid
        self.trials = trials
        self.outdir = outdir
        self.task = task
        self.session = session

        # Experiment settingsguis output dataframe
        self.dict_settings = {
            'Participant ID': [self.expid],
            'Task': [self.task],
            'Session': [self.task],
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

        if self.session not in ['Practice', 'practice']:

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

                case 'Negative Attention Capture Task':
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

            writer = pd.ExcelWriter(self.expid + taskstr + '_' + self.session + '.xlsx', engine='xlsxwriter')

            # Write each dataframe to a different worksheet.
            self.df_settings.to_excel(writer, sheet_name='Sheet1')
            self.df_performance.to_excel(writer, sheet_name='Sheet2')

            # Close the Pandas Excel writer and output the Excel file.
            writer.save()
