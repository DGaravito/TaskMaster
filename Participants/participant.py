# from adopy.tasks.dd import *
# from adopy.tasks.cra import *

import pandas as pd
import os
import xlsxwriter


class Participant(object):
    def __init__(self, expid, trials, session, outdir, task, eyetrack='No', controls='Default', fmri='No'):

        # extract the control scheme
        self.controlscheme = controls

        # set up keys depending on controls option
        if controls == 'Default (C & M)':
            self.leftkey = ['1']
            self.rightkey = ['2']

        elif controls == 'Buttonbox (1 & 2)':
            self.leftkey = ['C', 'c']
            self.rightkey = ['M', 'm']

        else:
            self.leftkey = ['']
            self.rightkey = ['']

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
        """
        A typical getter function; it returns the self.trials class function as an integer
        :return: self.trials as an integer
        """

        return int(self.trials)

    def set_settings(self, append):
        """
        Takes a dictionary of task-specific settings, converts it to a pandas dataframe, and then appends it to the
        existing pandas dataframe that holds the settings that are not task specific
        :param append: a dictionary of task-specific settings
        """

        self.df_settings = self.df_settings.join(
            pd.DataFrame(
                append,
                index=self.df_settings.index
            )
        )

    def set_performance(self, append):
        """
        Takes a dictionary of trial data, converts it to a pandas dataframe, and then appends it to the existing pandas
        dataframe that holds the data for all of the trials (and starts out empty)
        :param append: a dictionary of trial data
        """

        self.df_performance = pd.concat(
            [
                self.df_performance, append
            ]
        )

    def output(self):
        """
        First, the function looks to see if this is a practice session. If so, then there's no output from this trial.
        Next, if this is not a practice session, then we make a string to represent the task, which we will later use
        when making the string to name the output file. Next, we change directories to where the user chose to save the
        data and put together the ID, task string, and session name to make the name of the output xlsx file. We then
        name and open that excel file, put the settings info on the first sheet and the trial data on the second sheet,
        and then save, close, and output that file.
        """

        # If you are in a practice session, skip all of this and don't give any output
        if self.session not in ['Practice', 'practice']:

            # Look at what is in self.task and create an appropriate string to represent the task in the output file
            match self.task:

                case 'Delay Discounting':
                    taskstr = 'DD'

                case 'Probability Discounting':
                    taskstr = 'PD'

                case 'CogED Task':
                    taskstr = 'CEDT'

                case 'ARTT':
                    taskstr = 'ARTT'

                case 'Risk Aversion':
                    taskstr = 'RA'

                case 'Framing Task':
                    taskstr = 'Framing'

                case 'Beads Task':
                    taskstr = 'Beads'

                case 'Perceptual Bias Task':
                    taskstr = 'PBT'

                case 'Negative Attention Capture Task':
                    taskstr = 'NACT'

                case 'Stop-Signal Task':
                    taskstr = 'SS'

                case 'Emo Go/No-Go':
                    taskstr = 'EGNG'

                case 'Go/No-Go':
                    taskstr = 'GNG'

                case 'Stroop':
                    taskstr = 'Stroop'

                case 'Dwell':
                    taskstr = 'Dwell'

                case 'Pair Recall Memory':
                    taskstr = 'PR'

                case '1-back':
                    taskstr = self.task

                case '2-back':
                    taskstr = self.task

                case '3-back':
                    taskstr = self.task

                case '4-back':
                    taskstr = self.task

                case _:
                    taskstr = ''

            # change to the output directory
            os.chdir(self.outdir)

            # Make the string to name the output file
            outputname = self.expid + '_' + taskstr + '_' + self.session + '.xlsx'

            # Name an excel file and open it
            writer = pd.ExcelWriter(outputname, engine='xlsxwriter')

            # Write each dataframe to a different worksheet.
            self.df_settings.to_excel(writer, sheet_name='Information')
            self.df_performance.to_excel(writer, sheet_name='Performance')

            # Close the Pandas Excel writer and output the Excel file.
            writer.close()
