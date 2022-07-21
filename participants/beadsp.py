from Participants import participant

import pandas as pd
import random


class BeadsParticipant(participant.Participant):

    def __init__(self, expid, rounds, session, outdir, task, eyetracking):
        super().__init__(expid, rounds, session, outdir, task, eyetracking)

        # set up the jars as lists of beads, one with 80 red and one with 90 blue
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
        """
        takes an int that represents the round that was completed and returns the approriate text. Also, it randomly
        selects a jar to draw from for each round
        :param completedround:
        :return: either a blank string if there are still rounds to be completed or a thank you string
        """

        # if the number of completed rounds is the same as the number that was requested, set the prompt to the thank
        # you string
        if completedround == self.get_trials():

            prompt = 'Thank you! This task is complete.'

        # if there are still rounds to be completed...
        else:

            # randomly select one or two to represent either jar
            jarint = random.randint(1, 2)

            # if you got 1...
            if jarint == 1:

                # you will draw from the blue jar
                self.jarname = 'Blue'
                self.jar = self.blue_jar

            # if you got 2...
            else:

                # you will draw from the red jar
                self.jarname = 'Red'
                self.jar = self.red_jar

            # set the prompt to the empty string
            prompt = ''

        # return the prompt
        return prompt

    def get_bead(self):
        """
        simple getter function to randomly draw a bead from the jar and return it
        :return: a string for the bead drawn
        """

        # randomly choose a picture string for a bead from the jar
        self.pic = random.choice(self.jar)

        # return the picture string
        return self.pic

    def updateoutput(self, currentround, beadspicked, response=0, pick='None', conf=0):
        """
        updates the performance dataframe for each trial, and if they chose to pick a jar, were they correct
        :param currentround: the number of the current round
        :param beadspicked: the number of the trial that was just completed
        :param response: integer with either 0 or 1 depending on if the person chose to draw a bead or pick a jar
        :param pick: if they picked a jar, what jar did they pick
        :param conf: if they picked a jar, how confident were they
        :return: updates the performance dataframe in the superclass
        """

        # set correct to 0 as default
        correct = 0

        # if the particpant chose a jar...
        if response == 1:

            # and the jar they picked was the same as the jar that the program was drawing from
            if pick == self.jarname:

                # then the participant is marked as correct
                correct = 1

        # set up a dictionary with this trial's info
        df_simultrial = {
            'round': [currentround],
            'beads': [beadspicked],
            'last bead': [self.pic],
            'response': [response],
            'jar picked': [pick],
            'confidence': [conf],
            'correct': [correct]
        }

        # turn the dictionary into a dataframe
        df_simultrial = pd.DataFrame(data=df_simultrial)

        # add the dataframe to the main one
        self.set_performance(df_simultrial)

    def get_instructions(self, instint):
        """
        Takes in an int and returns the appropriate instructions string
        :param instint: an int that is supplied and incremented by the expguis
        :return: a string containing the appropriate instructions that the expguis puts up
        """

        match instint:

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

                inst = 'The computer will take beads from ONE jar and\nwill show you the color of the bead it took ' \
                       'out from that jar.'

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
