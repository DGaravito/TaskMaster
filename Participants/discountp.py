# from adopy.tasks.dd import *
# from adopy import Engine
# import numpy as np
import pandas as pd
import random

from Participants import participant


class DdParticipant(participant.Participant):

    def __init__(self, expid, trials, session, outdir, task, ss_del, ll_shortdel, ll_longdel, ss_smallrew, ll_rew,
                 rounds, outcome, adopy, buttonbox, eyetracking, fmri):
        super().__init__(expid, trials, session, outdir, task, buttonbox, eyetracking, fmri)

        # make a variable for ADOPy status
        self.adopy = adopy

        # make variable to store user input on whether they wanted an outcome chosen
        self.outcomeopt = outcome

        # set how many blocks there are
        self.rounds = int(rounds)

        # store the user input
        self.userinput = [float(ss_del), float(ll_shortdel), float(ll_longdel), float(ss_smallrew), float(ll_rew)]

        # # if you want ADOPy, then create the engine
        # if adopy == 'Yes':
        #
        #     # call the function to create the adopy engine
        #     self.engine = self.create_dd_engine(self.task, self.userinput[0], self.userinput[1], self.userinput[2],
        #                                         self.userinput[3], self.userinput[4])
        #
        #     # Compute an optimal design for the first trial
        #     self.design = self.engine.get_design('optimal')
        #
        # # if not...
        # else:

        # make the list for the stimuli
        self.taskstimuli = []

        # create the stimuli for the task
        self.createstim(self.userinput[0], self.userinput[1], self.userinput[2], self.userinput[3],
                        self.userinput[4])

        # make a list for the specific trial info
        self.trialinfo = []

        # Experiment settingsguis output dataframe
        dict_tasksettings = {'Immediate Option Delay': [ss_del],
                             'Shortest Delay (weeks)': [ll_shortdel],
                             'Longest Delay (weeks)': [ll_longdel],
                             'Smallest Smaller Sooner Reward': [ss_smallrew],
                             'Largest Smaller Sooner Reward': [(float(ll_rew) - float(ss_smallrew))],
                             'Larger Later Reward': [ll_rew],
                             'Blocks': [rounds],
                             'ADOPy?': [adopy]
                             }

        # attach the task-specific settings to the task general settings
        self.set_settings(dict_tasksettings)

    # def create_dd_engine(self, task, ss_del, ll_shortdel, ll_longdel, ss_smallrew, ll_rew):
    #     """
    #     creates the ADOPy engine for the delay discounting task
    #     :param task: for the adopy dd task
    #     :param ss_del: float for the delay for the sooner option
    #     :param ll_shortdel: float for the shortest delay for the delayed option
    #     :param ll_longdel: float for the longest delay for the delayed option
    #     :param ss_smallrew: float for the smallest reward for the sooner option
    #     :param ll_rew: float for the largest reward for the delayed option
    #     :return: adopy engine object
    #     """
    #
    #     # use the hyperbolic discounting model
    #     model = ModelHyp()
    #
    #     # make a list to have the different delays for the delayed option
    #     timerange = [ll_shortdel]
    #
    #     # if there are more than two trials per block...
    #     if (self.get_trials() - 2) > 0:
    #
    #         # then for however many additional trials per block there are...
    #         for trial in range(self.get_trials() - 2):
    #             # add a random float between shortest and longest delay for the delayed option to the list of delays
    #             timerange.append(random.uniform(ll_shortdel, ll_longdel))
    #
    #     # now add the longest delay to the list of delay
    #     timerange.append(ll_longdel)
    #
    #     # make a design dictionary for ADOPy
    #     grid_design = {
    #         # e.g., for now, put [0]
    #         't_ss': [ss_del],
    #
    #         # e.g., [1 week, 2 weeks, ..., longdelay] in weeks
    #         't_ll': timerange,
    #
    #         # [smallreward, smallreward + $1, ..., bigreward]
    #         'r_ss': np.arange(ss_smallrew, ll_rew, .5),
    #
    #         # [bigreward]
    #         'r_ll': [ll_rew]
    #     }
    #
    #     # make a dictionary for the ADOPy model parameters
    #     grid_param = {
    #         # 50 points on [10^-5, ..., 1] in a log scale
    #         'k': np.logspace(-5, 0, 50, base=10),
    #
    #         # 10 points on (0, 5] in a linear scale
    #         'tau': np.linspace(0, 5, 11)[1:]
    #     }
    #
    #     # make a dictionary for the possible responses
    #     grid_response = {
    #         'choice': [0, 1]
    #     }
    #
    #     # Set up engine
    #     engine = Engine(task, model, grid_design, grid_param, grid_response)
    #
    #     # return the engine
    #     return engine

    def createstim(self, ss_del, ll_shortdel, ll_longdel, ss_smallrew, ll_rew):
        """
        creates list of stimuli for the delay discounting task, first creating the list of amounts for the sooner
        option, then the delay for the sooner option
        :param ss_del: float for the delay for the sooner option
        :param ll_shortdel: float for the shortest delay for the delayed option
        :param ll_longdel: float for the longest delay for the delayed option
        :param ss_smallrew: float for the smallest reward for the sooner option
        :param ll_rew: float for the largest reward for the delayed option
        """

        # make a list to have the different reward amounts for the sooner option
        amountrange = []

        # if there are more than two trials per block...
        if (self.get_trials() - 2) > 0:

            # then for however many additional trials per block there are...
            for trial in range(self.get_trials()):

                # add a random float between the smallest and largest amount for the sooner option to the amount list
                amountrange.append(random.uniform(ss_smallrew, ll_rew - .5))

        # otherwise, just put the min and max (minus $.5) in the list
        else:

            amountrange.append(ss_smallrew)
            amountrange.append(ll_rew - .5)

        # randomize the list items
        random.shuffle(amountrange)

        # add the list of sooner rewards to the stimuli list
        self.taskstimuli.append(amountrange)

        # add the delay for sooner rewards to the stimuli list
        self.taskstimuli.append(ss_del)

        # add the amount for later rewards to the stimuli list
        self.taskstimuli.append(ll_rew)

        # make a list to have the different delays for the delayed option
        timerange = [ll_shortdel]

        # if there are more than two trials per block...
        if (self.get_trials() - 2) > 0:

            # then for however many additional trials per block there are...
            for trial in range(self.get_trials() - 2):
                # add a random float between the shortest and longest delay for the delayed option to the list of delays
                timerange.append(random.uniform(ll_shortdel, ll_longdel))

        # now add the longest delay to the list of delay
        timerange.append(ll_longdel)

        # randomize the list items
        random.shuffle(timerange)

        # add the list of sooner rewards to the stimuli list
        self.taskstimuli.append(timerange)

    def get_timestring(self, startingweeks):
        """
        takes the float that the model kicks out for the delays and converts it to an understandable string
        :param startingweeks: float for the weeks kicked out by the engine
        :return: string that lists the years, months, weeks, and days that the original float was equal to
        """

        # make a blank string to start
        timestring = ''

        # convert the week float to days
        days = float(startingweeks * 7)

        # if there are more days than in a year...
        if days >= 365.2422:

            # get the number of years, rounded down to the closest integer
            years = int(days / 365.2422)

            # add the number of years and " years" to the string
            timestring = timestring + str(years) + ' years'

            # subtract the days in the years from the total days
            days = float(days - (years * 365.2422))

            # if the leftover days, rounded down, is still greater than 0, then add a comma to the string
            if int(days) > 0:

                timestring = timestring + ', '

            # otherwise, add a period
            else:

                timestring = timestring + '.'

        # if there are more days than in an average month...
        if days >= 30.437:

            # get the number of months, rounded down to the closest integer
            months = int(days / 30.437)

            # add the number of months and " months" to the string
            timestring = timestring + str(months) + ' months'

            # subtract the days in the months from the total days
            days = float(days - (months * 30.437))

            # if the leftover days, rounded down, is still greater than 0, then add a comma to the string
            if int(days) > 0:

                timestring = timestring + ', '

            # otherwise, add a period
            else:

                timestring = timestring + '.'

        # if there are more days than in a week...
        if days >= 7:

            # get the number of weeks, rounded down to the closest integer
            weeks = int(days / 7)

            # add the number of weeks and " weeks" to the string
            timestring = timestring + str(weeks) + ' weeks'

            # subtract the days in the weeks from the total days
            days = float(days - (weeks * 7))

            # if the leftover days, rounded down, is still greater than 0, then add a comma to the string
            if int(days) > 0:

                timestring = timestring + ', '

            # otherwise, add a period
            else:

                timestring = timestring + '.'

        # if there are any more full days left, then add them to the string
        if int(days) > 0:
            timestring = timestring + str(int(days)) + ' days.'

        # return the string
        return timestring

    def get_design_text(self):
        """
        takes the design from the ADOPy engine and turns it into strings for the left and right options
        :return: a list of two strings, one for the left option, and one for the right option
        """

        # makes sure the trial info list is empty
        self.trialinfo = []

        # pick a random integer so that we randomize the sides that the strings are on
        side = random.randint(1, 2)

        # # if you're using ADOPy, then pull trial info from the ADOPy design
        # if self.adopy == 'Yes':
        #
        #     self.trialinfo.append(float(self.design['r_ss']))
        #     self.trialinfo.append(float(self.design['t_ss']))
        #     self.trialinfo.append(float(self.design['r_ll']))
        #     self.trialinfo.append(float(self.design['t_ll']))
        #
        # # otherwise, pull trial info from the info list
        # else:

        self.trialinfo.append(self.taskstimuli[0].pop())
        self.trialinfo.append(self.taskstimuli[1])
        self.trialinfo.append(self.taskstimuli[2])
        self.trialinfo.append(self.taskstimuli[3].pop())

        # if the user wanted the immediate option to occur now, as opposed to also at a delay, use now  in the string
        if int(self.trialinfo[0]) == 0:
            shortstring = 'Getting $' + str('{:.2f}'.format(self.trialinfo[0])) + '\nnow'

        # otherwise, use the get_timestring function to have a string
        else:
            shortstring = 'Getting $' + str('{:.2f}'.format(self.trialinfo[0])) + '\nafter ' \
                          + self.get_timestring(self.trialinfo[1])

        # for the right string
        delaystring = 'Getting $' + str('{:.2f}'.format(self.trialinfo[2])) + '\nafter ' \
                      + self.get_timestring(self.trialinfo[3])

        # if the side integer is 1, then put the delay string on the right
        if side == 1:

            options = [shortstring, delaystring]

        # otherwise, put the delay string on the left
        else:

            options = [delaystring, shortstring]

        # return the strings as a list
        return options

    # def engineupdate(self, response):
    #     """
    #     updates the adopy engine (if used) with the participant's response and then sets up the new design
    #     :param response: 0 or 1 depending on if the participant took the immediate or delayed option
    #     """
    #
    #     # if you are using ADOPy, do this
    #     if self.adopy == 'Yes':
    #
    #         # Update engine with the response and current design
    #         self.engine.update(self.design, response)
    #
    #         # Generate new optimal design based on previous design and response
    #         self.design = self.engine.get_design('optimal')

    def nextround(self, blocks):
        """
        Called to get the text prompt for the next block
        :param blocks: an integer for the block that was just completed
        :return:
        """

        # if all of the blocks have been completed, thank the participant
        if blocks == self.rounds:

            prompt = 'Thank you! This task is complete.'

        # if there are still blocks to be completed, tell the participant to wait
        else:

            prompt = 'Please wait for the next round.'

            # if you don't use ADOPy, task stuff should be created again
            if self.adopy == 'No':

                # make the list for the stimuli
                self.taskstimuli = []

                # create the stimuli for the task
                self.createstim(self.userinput[0], self.userinput[1], self.userinput[2], self.userinput[3],
                                self.userinput[4])

        # return the prompt
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

        # make a dictionary of trial info
        df_trial = {
            'trial': [trial],
            'onset': [onset],
            'SSAmount': [self.trialinfo[0]],
            'LLAmount': [self.trialinfo[2]],
            'LLDelay': [self.trialinfo[3]],
            'response': [response],
            'reaction time': [time]
        }

        # if self.adopy == 'Yes':
        #     df_trial['mean_k'] = [self.engine.post_mean[0]]
        #     df_trial['mean_tau'] = [self.engine.post_mean[1]]
        #     df_trial['sd_k'] = [self.engine.post_sd[0]]
        #     df_trial['sd_tau'] = [self.engine.post_sd[1]]

        # turn that dictionary into a dataframe and use set_performance to add it to the overall dataframe
        df_trial = pd.DataFrame(data=df_trial)
        self.set_performance(df_trial)

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

        # grab the information that the user entered on the settings page
        self.rounds = int(rounds)
        self.design = design
        self.maximum = float(maximum)
        self.minimum = float(minimum)
        self.startmoney = float(money)
        self.outcomeopt = outcome

        # make empty lists for the trial design and outcomes that the participant chose (if the user wanted an outcome
        # randomly shown on screen
        self.trialdesign = []
        self.outcomelist = []

        # call the function to create the design
        self.create_design()

        # Experiment settingsguis output dataframe
        dict_tasksettings = {'Design': [design],
                             'Minimum Reward': [minimum],
                             'Maximum Reward': [maximum],
                             'Blocks': [rounds]
                             }

        # attach the task-specific settings to the task general settings
        self.set_settings(dict_tasksettings)

    def create_design(self):
        """
        If you want both gains and losses, then it creates a random order for gain and loss questions
        :return: Does not return a value, instead creates the class dictionaries and then calls set design text to make
        the first trial
        """

        # only if the user wanted gains and losses
        if self.design == 'Gains and Losses':
            # divide the number of trials by 2 because there are 2 types of trials
            multnum = int(self.get_trials() / 2)

            # list composed of 2 integers which are one half of the total trials
            multiplier = [multnum, multnum]

            # list composed of 2 strings for gains and losses
            gainlosscond = ['Gain', 'Loss']

            # the lists are multiplied so that you end up with a list of strings. Each string appears half of the trials
            self.order = sum([[s] * n for s, n in zip(gainlosscond, multiplier)], [])

            # randomize the list
            random.shuffle(self.order)

    def set_design_text(self):
        """
        Sets the actual text used in the design
        :return: Creates self.trialdesign
        """

        # generate random floats between the ranges for rewards and probabilities
        self.trialdesign = [
            random.uniform(self.minimum, self.maximum - .5),
            random.uniform(.01, .99)
        ]

    def get_design_text(self):
        """
        Looks at self.trialdesign and returns strings for the GUI
        :return: left text (sure), right text (gamble), and gamble probability
        """

        # if the user wanted both gains and losses
        if self.design == 'Gains and Losses':

            # pop the string out of the order list to figure out if the trial is a gain or loss one
            self.state = self.order.pop()

            # if the next trial is a gain trial
            if self.state == 'Gain':

                # Set up the left string for sure value
                leftstring = 'Win $' + str('{:.2f}'.format(self.trialdesign[0])) + ' for sure'

                # Set up the right string for risky gamble
                rightstring = 'A ' + str(round(self.trialdesign[1] * 100)) + '% chance to win $' + \
                              str('{:.2f}'.format(self.maximum))

                # Set the probability bar for the risky gamble
                barvalue = round(self.trialdesign[1] * 100)

            # if the next trial is a loss trial
            else:

                # Set up the left string for sure value
                leftstring = 'Lose $' + str('{:.2f}'.format(self.trialdesign[0])) + ' for sure'

                # Set up the right string for risky gamble
                rightstring = 'A ' + str(round(self.trialdesign[1] * 100)) + '% chance to lose $' + \
                              str('{:.2f}'.format(self.maximum))

                # Set the probability bar for the risky gamble
                barvalue = round((1 - self.trialdesign[1]) * 100)

        # if the user just wanted gains
        elif self.design == "Gains only":

            # indicate that the trial is a gain trial
            self.state = 'Gain'

            # Set up the left string for sure value
            leftstring = 'Win $' + str('{:.2f}'.format(self.trialdesign[0])) + ' for sure'

            # Set up the right string for risky gamble
            rightstring = 'A ' + str(round(self.trialdesign[1] * 100)) + '% chance to win $' + \
                          str('{:.2f}'.format(self.maximum))

            # Set the probability bar for the risky gamble
            barvalue = round(self.trialdesign[1] * 100)

        # if the user just wanted losses
        else:

            # indicate that the trial is a loss trial
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
        """
        Called to get the text prompt for the next block
        :param blocks: an integer for the block that was just completed
        :return:
        """

        # if all of the blocks have been completed, thank the participant
        if blocks == self.rounds:

            prompt = 'Thank you! This task is complete.'

        # if there are still blocks to be completed, tell the participant to wait
        else:

            prompt = 'Please wait for the next round.'

        # return the prompt
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

        # make a dictionary of trial info
        df_trial = {
            'trial': [trial],
            'cond': [self.state],
            'SureAmount': [str('{:.2f}'.format(self.trialdesign[0]))],
            'RiskyAmount': [self.maximum],
            'RiskyProbability': [str(self.trialdesign[1])],
            'onset': [onset],
            'response': [response],
            'reaction time': [time]
        }

        # turn that dictionary into a dataframe and use set_performance to add it to the overall dataframe
        df_trial = pd.DataFrame(data=df_trial)
        self.set_performance(df_trial)

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

                # if the user requested a random choice be output at the end, then tell the user how much starting money
                # is there
                if self.outcomeopt == 'Yes':

                    inst = 'You have $' + str('{:.2f}'.format(self.startmoney)) + ' in starting money. Your final ' \
                                                                                  'payment\nwill depend on the ' \
                                                                                  'choices you make in this task.'

                # otherwise, tell the participant to take the fictional money seriously
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

        # grab information from what the user entered in the settings
        self.rounds = int(rounds)
        self.version = version
        self.outcomeopt = outcome

        # make the modifier for rewards be equal to the max reward divided by 4
        self.modifier = float(maxrew) / 4

        # make an empty list for choices that the participant made in case the user wanted a random one output
        self.outcomelist = []

        # change the actual names of the tasks depending on what the user wanted to call them
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
        dict_tasksettings = {
            'Maximum Reward': [maxrew],
            'Version': [version]
        }

        # attach the task-specific settings to the task general settings
        self.set_settings(dict_tasksettings)

        # call the set structure function to set up what order things are presented in
        self.set_structure()

    def set_structure(self):
        """
        sets the structure for the trials depending on if the user wanted the original CogED task or the full one
        """

        # if the user wanted the alternate CogED...
        if self.version == 'Alternate':

            # divide the number of trials by 6 because there are 6 types of trials
            multnum = int((self.get_trials() * self.rounds) / 6)

            # list composed of 6 integers which are one sixth of the total trials
            multiplier = [multnum, multnum, multnum, multnum, multnum, multnum]

            # list composed of 6 strings for the 6 types of trials
            gainlosscond = ['1-2', '1-3', '1-4', '2-3', '2-4', '3-4']

            # the strings are multiplied so that you end up with a list of strings. Each string appears one sixth of the
            # time
            self.order = sum([[s] * n for s, n in zip(gainlosscond, multiplier)], [])

        # if the user wanted the standard CogED
        else:

            # divide the number of trials by 3 because there are 3 types of trials
            multnum = int((self.get_trials() * self.rounds) / 3)

            # list composed of 3 integers which are one third of the total trials
            multiplier = [multnum, multnum, multnum]

            # list composed of 3 strings for the 3 types of trials
            gainlosscond = ['1-2', '1-3', '1-4']

            # the strings are multiplied so that you end up with a list of strings. Each string appears one third of the
            # time
            self.order = sum([[s] * n for s, n in zip(gainlosscond, multiplier)], [])

        # shuffle the order
        random.shuffle(self.order)

    def set_design_text(self):
        """
        reads what type of trial is next and then sets the trial text accordingly
        """

        # pop a string from the order list to determine what trial is next
        self.state = self.order.pop()

        # pick a random integer to figure out which task will be on which side
        self.randomside = random.randint(1, 2)

        # do different things depending on the trial type
        match self.state:

            # if this is a 1- vs 2-back trial
            case '1-2':

                # increment the count of this type of trial
                self.onetwotrials += 1

                # if the east task should be on the left side...
                if self.randomside == 1:

                    # set the left task the the 1-back
                    self.lefttask = self.stimnames[0]

                    # set the left money to a string of the default amount plus the modifier for this trial type
                    self.leftmoney = str('{:.2f}'.format(self.onebackamount + self.onetwomodifier))

                    # set the right task the the 2-back
                    self.righttask = self.stimnames[1]

                    # set the right money to a string of the default amount
                    self.rightmoney = str('{:.2f}'.format(self.twohardamount))

                # if the hard task should be on the left side...
                else:

                    # set the left task the the 2-back
                    self.lefttask = self.stimnames[1]

                    # set the left money to a string of the default amount
                    self.leftmoney = str('{:.2f}'.format(self.twohardamount))

                    # set the right task the the 1-back
                    self.righttask = self.stimnames[0]

                    # set the right money to a string of the default amount plus the modifier for this trial type
                    self.rightmoney = str('{:.2f}'.format(self.onebackamount + self.onetwomodifier))

            # if this is a 1- vs 3-back trial
            case '1-3':

                # increment the count of this type of trial
                self.onethreetrials += 1

                # if the east task should be on the left side...
                if self.randomside == 1:

                    # set the left task the the 1-back
                    self.lefttask = self.stimnames[0]

                    # set the left money to a string of the default amount plus the modifier for this trial type
                    self.leftmoney = str('{:.2f}'.format(self.onebackamount + self.onethreemodifier))

                    # set the right task the the 3-back
                    self.righttask = self.stimnames[2]

                    # set the right money to a string of the default amount
                    self.rightmoney = str('{:.2f}'.format(self.threehardamount))

                # if the hard task should be on the left side...
                else:

                    # set the left task the the 3-back
                    self.lefttask = self.stimnames[2]

                    # set the left money to a string of the default amount
                    self.leftmoney = str('{:.2f}'.format(self.threehardamount))

                    # set the right task the the 1-back
                    self.righttask = self.stimnames[0]

                    # set the right money to a string of the default amount plus the modifier for this trial type
                    self.rightmoney = str('{:.2f}'.format(self.onebackamount + self.onethreemodifier))

            # if this is a 1- vs 4-back trial
            case '1-4':

                # increment the count of this type of trial
                self.onefourtrials += 1

                # if the east task should be on the left side...
                if self.randomside == 1:

                    # set the left task the the 1-back
                    self.lefttask = self.stimnames[0]

                    # set the left money to a string of the default amount plus the modifier for this trial type
                    self.leftmoney = str('{:.2f}'.format(self.onebackamount + self.onefourmodifier))

                    # set the right task the the 4-back
                    self.righttask = self.stimnames[3]

                    # set the right money to a string of the default amount
                    self.rightmoney = str('{:.2f}'.format(self.fourbackamount))

                # if the hard task should be on the left side...
                else:

                    # set the left task the the 4-back
                    self.lefttask = self.stimnames[3]

                    # set the left money to a string of the default amount
                    self.leftmoney = str('{:.2f}'.format(self.fourbackamount))

                    # set the right task the the 1-back
                    self.righttask = self.stimnames[0]

                    # set the right money to a string of the default amount plus the modifier for this trial type
                    self.rightmoney = str('{:.2f}'.format(self.onebackamount + self.onefourmodifier))

            # if this is a 2- vs 3-back trial
            case '2-3':

                # increment the count of this type of trial
                self.twothreetrials += 1

                # if the east task should be on the left side...
                if self.randomside == 1:

                    # set the left task the the 2-back
                    self.lefttask = self.stimnames[1]

                    # set the left money to a string of the default amount plus the modifier for this trial type
                    self.leftmoney = str('{:.2f}'.format(self.twoeasyamount + self.twothreemodifier))

                    # set the right task the the 3-back
                    self.righttask = self.stimnames[2]

                    # set the right money to a string of the default amount
                    self.rightmoney = str('{:.2f}'.format(self.threehardamount))

                # if the hard task should be on the left side...
                else:

                    # set the left task the the 3-back
                    self.lefttask = self.stimnames[2]

                    # set the left money to a string of the default amount
                    self.leftmoney = str('{:.2f}'.format(self.threehardamount))

                    # set the right task the the 2-back
                    self.righttask = self.stimnames[1]

                    # set the right money to a string of the default amount plus the modifier for this trial type
                    self.rightmoney = str('{:.2f}'.format(self.twoeasyamount + self.twothreemodifier))

            # if this is a 2- vs 4-back trial
            case '2-4':

                # increment the count of this type of trial
                self.twofourtrials += 1

                # if the east task should be on the left side...
                if self.randomside == 1:

                    # set the left task the the 2-back
                    self.lefttask = self.stimnames[1]

                    # set the left money to a string of the default amount plus the modifier for this trial type
                    self.leftmoney = str('{:.2f}'.format(self.twoeasyamount + self.twofourmodifier))

                    # set the right task the the 4-back
                    self.righttask = self.stimnames[3]

                    # set the right money to a string of the default amount
                    self.rightmoney = str('{:.2f}'.format(self.fourbackamount))

                # if the hard task should be on the left side...
                else:

                    # set the left task the the 4-back
                    self.lefttask = self.stimnames[3]

                    # set the left money to a string of the default amount
                    self.leftmoney = str('{:.2f}'.format(self.fourbackamount))

                    # set the right task the the 2-back
                    self.righttask = self.stimnames[1]

                    # set the right money to a string of the default amount plus the modifier for this trial type
                    self.rightmoney = str('{:.2f}'.format(self.twoeasyamount + self.twofourmodifier))

            # if this is a 3- vs 4-back trial
            case '3-4':

                # increment the count of this type of trial
                self.threefourtrials += 1

                # if the east task should be on the left side...
                if self.randomside == 1:

                    # set the left task the the 3-back
                    self.lefttask = self.stimnames[2]

                    # set the left money to a string of the default amount plus the modifier for this trial type
                    self.leftmoney = str('{:.2f}'.format(self.threeeasyamount + self.threefourmodifier))

                    # set the right task the the 4-back
                    self.righttask = self.stimnames[3]

                    # set the right money to a string of the default amount
                    self.rightmoney = str('{:.2f}'.format(self.fourbackamount))

                # if the hard task should be on the left side...
                else:

                    # set the left task the the 4-back
                    self.lefttask = self.stimnames[3]

                    # set the left money to a string of the default amount
                    self.leftmoney = str('{:.2f}'.format(self.fourbackamount))

                    # set the right task the the 3-back
                    self.righttask = self.stimnames[2]

                    # set the right money to a string of the default amount plus the modifier for this trial type
                    self.rightmoney = str('{:.2f}'.format(self.threeeasyamount + self.threefourmodifier))

            # otherwise, print panic
            case _:

                print('Panic!')

    def nextround(self, roundsdone):
        """
        At the block's completion, reset the counters and prompt the participant depending on if there are more blocks
        to go and if the user wanted to output a participant choice
        :param roundsdone: integer for how many rounds have been completed
        :return: string to prompt the participant at the round's completion
        """

        # reset trial counts for modifiers
        self.onetwotrials = 0
        self.onethreetrials = 0
        self.onefourtrials = 0
        self.twothreetrials = 0
        self.twofourtrials = 0
        self.threefourtrials = 0

        # if all the blocks have been completed
        if self.rounds == roundsdone:

            # if the user wanted one of the outcomes shown for the participant, display that
            if self.outcomeopt == 'Yes':

                prompt = 'Your outcome: ' + random.choice(self.outcomelist)

            # if not, just thank the participant
            else:

                prompt = 'Thank you! This task is complete.'

        # if there are still more blocks to go, tell the participant so
        else:

            prompt = 'Please wait for the next round.'

        # return the prompt
        return prompt

    def get_design_text(self):
        """
        sets up the trial strings with the trial's information and then returns them
        :return: a list of two strings,
        """

        leftstring = 'Doing extra rounds of the\n\"' + self.lefttask + '\" task for $' + self.leftmoney
        rightstring = 'Doing extra rounds of the\n\"' + self.righttask + '\" task for $' + self.rightmoney

        return [leftstring, rightstring]

    def updateoutput(self, trial, onset, fulltime, time, response=3):
        """
        records stats for the trial
        :param trial: the number of the trial that was just completed
        :param onset: onset time for the trial
        :param fulltime: onset time for when the full trial appeared
        :param time: participants's reaction time
        :param response: integer with either 0 or 1 depending on if the person chose left or right
        :return: updates the performance dataframe in the superclass
        """

        # make a dictionary of trial info
        df_trial = {
            'trial': [trial],
            'left task': [self.lefttask],
            'left value': [self.leftmoney],
            'right task': [self.righttask],
            'right value': [self.rightmoney],
            'onset': [onset],
            'full question displayed': [fulltime],
            'response': [response],
            'reaction time': [time]
        }

        # turn that dictionary into a dataframe and use set_performance to add it to the overall dataframe
        df_trial = pd.DataFrame(data=df_trial)
        self.set_performance(df_trial)

        # only do the following if the user wanted a random reward/loss at the end and the participant responded
        if (self.outcomeopt == 'Yes') & (response != 3):

            # Generate a random number of rounds to be done for that task
            randomrounds = random.randint(1, 10)

            # Add their choice (with the random number of rounds)
            # if they chose the left option, turn the left option into a string
            if response == 0:

                outcomestring = str(randomrounds) + ' rounds of the ' + self.lefttask + ' task for $' + self.leftmoney

            # if they chose the right option, turn the right option into a string
            else:

                outcomestring = str(randomrounds) + ' rounds of the ' + self.righttask + ' task for $' + self.rightmoney

            # add the string to the total list of outcomes
            self.outcomelist.append(outcomestring)

        # if the participant actuall responded
        if response != 3:

            # find out what type of trial just happened
            match self.state:

                # if it was a 1- vs 2-back trial...
                case '1-2':

                    # if the easier task was on the left side and the participant chose the left (or the easier was on
                    # the right and the participant chose that), then lessen the reward for the easier task in this type
                    # of trial
                    if ((self.randomside == 1) & (response == 0)) | ((self.randomside == 2) & (response == 1)):

                        self.onetwomodifier = self.onetwomodifier - (self.modifier / float(self.onetwotrials))

                    # otherwise, increase the reward for the easier task for this type of trial
                    else:

                        self.onetwomodifier = self.onetwomodifier + (self.modifier / float(self.onetwotrials))

                # if it was a 1- vs 3-back trial...
                case '1-3':

                    # if the easier task was on the left side and the participant chose the left (or the easier was on
                    # the right and the participant chose that), then lessen the reward for the easier task in this type
                    # of trial
                    if ((self.randomside == 1) & (response == 0)) | ((self.randomside == 2) & (response == 1)):

                        self.onethreemodifier = self.onethreemodifier - (self.modifier / float(self.onethreetrials))

                    # otherwise, increase the reward for the easier task for this type of trial
                    else:

                        self.onethreemodifier = self.onethreemodifier + (self.modifier / float(self.onethreetrials))

                # if it was a 1- vs 4-back trial...
                case '1-4':

                    # if the easier task was on the left side and the participant chose the left (or the easier was on
                    # the right and the participant chose that), then lessen the reward for the easier task in this type
                    # of trial
                    if ((self.randomside == 1) & (response == 0)) | ((self.randomside == 2) & (response == 1)):

                        self.onefourmodifier = self.onefourmodifier - (self.modifier / float(self.onefourtrials))

                    # otherwise, increase the reward for the easier task for this type of trial
                    else:

                        self.onefourmodifier = self.onefourmodifier + (self.modifier / float(self.onefourtrials))

                # if it was a 2- vs 3-back trial...
                case '2-3':

                    # if the easier task was on the left side and the participant chose the left (or the easier was on
                    # the right and the participant chose that), then lessen the reward for the easier task in this type
                    # of trial
                    if ((self.randomside == 1) & (response == 0)) | ((self.randomside == 2) & (response == 1)):

                        self.twothreemodifier = self.twothreemodifier - (self.modifier / float(self.twothreetrials))

                    # otherwise, increase the reward for the easier task for this type of trial
                    else:

                        self.twothreemodifier = self.twothreemodifier + (self.modifier / float(self.twothreetrials))

                # if it was a 2- vs 4-back trial...
                case '2-4':

                    # if the easier task was on the left side and the participant chose the left (or the easier was on
                    # the right and the participant chose that), then lessen the reward for the easier task in this type
                    # of trial
                    if ((self.randomside == 1) & (response == 0)) | ((self.randomside == 2) & (response == 1)):

                        self.twofourmodifier = self.twofourmodifier - (self.modifier / float(self.twofourtrials))

                    # otherwise, increase the reward for the easier task for this type of trial
                    else:

                        self.twofourmodifier = self.twofourmodifier + (self.modifier / float(self.twofourtrials))

                # if it was a 3- vs 4-back trial...
                case '3-4':

                    # if the easier task was on the left side and the participant chose the left (or the easier was on
                    # the right and the participant chose that), then lessen the reward for the easier task in this type
                    # of trial
                    if ((self.randomside == 1) & (response == 0)) | ((self.randomside == 2) & (response == 1)):

                        self.threefourmodifier = self.threefourmodifier - (self.modifier / float(self.threefourtrials))

                    # otherwise, increase the reward for the easier task for this type of trial
                    else:

                        self.threefourmodifier = self.threefourmodifier + (self.modifier / float(self.threefourtrials))

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

                # if the user wanted a participant choice output, then tell the participant so
                if self.outcomeopt == 'Yes':

                    inst = 'Any one of the choices you make could determine\nwhat task you complete extra rounds of ' \
                           'and how much\nyou are paid for completing that task.'

                # otherwise, skip towards the instruction to tell participants to take their time
                else:

                    inst = 'Take as much time as you need to choose. After a\nwhile, the decision will disappear, ' \
                           'but those choices\nwill be shown again at the end.'

            case 7:

                # if the user wanted a participant choice output, then tell the participant one will be chosen at random
                if self.outcomeopt == 'Yes':

                    inst = 'We will pick one of your choices at random. It does\nnot matter how well you do on the ' \
                           'task chosen. You\nwill be paid as long as you maintain your effort.'

                else:

                    inst = 'Let the experimenter know you are ready.'

            case 8:

                # if the user wanted a participant choice output, then now tell participants to take their time
                if self.outcomeopt == 'Yes':

                    inst = 'Take as much time as you need to choose. After a\nwhile, the decision will disappear, ' \
                           'but those choices\nwill be shown again at the end.'

                else:

                    inst = 'Let the experimenter know you are ready.'

            case _:

                inst = 'Let the experimenter know you are ready.'

        return inst
