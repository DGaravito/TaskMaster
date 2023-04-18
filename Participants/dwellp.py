import pandas as pd
import random
import glob

from Participants import participant


class DwellParticipant(participant.Participant):

    def __init__(self, expid, trials, session, outdir, task, blocks, happy, happylen, sad, sadlen, angry, angrylen,
                 fear, fearlen, neulen, neg, neglen, neunflen, sex, race, picd, eyetracking):
        super().__init__(expid, trials, session, outdir, task, eyetracking)

        # copy if sex/race balancing was requested
        self.sexbalancing = sex
        self.racebalancing = race

        # make length variables for the picture lists
        self.happylength = happylen
        self.sadlength = sadlen
        self.angrylength = angrylen
        self.fearlength = fearlen
        self.neulength = neulen
        self.neglength = neglen
        self.neunlength = neunflen

        # make the picture directory a class variable
        self.picturedir = picd

        # set how many blocks are needed and set the blocks done to 0
        self.blocks = int(blocks)
        self.blocksdone = 0

        # make an empty list for the blocks
        self.matrixtypes = []

        # each of the following if statements checks to see if the user checks any of these emotions. If so, it adds the
        # emotion and the reverse round to the block structure
        if happy == 'Yes':
            self.matrixtypes.append('Happy')

        if sad == 'Yes':
            self.matrixtypes.append('Sad')

        if angry == 'Yes':
            self.matrixtypes.append('Angry')

        if fear == 'Yes':
            self.matrixtypes.append('Fearful')

        if neg == 'Yes':
            self.matrixtypes.append('Negative')

        # copy the original list to get an order for the task
        self.blockorder = list(self.matrixtypes)

        # shuffle the order
        random.shuffle(self.blockorder)

        # make an empty list for the first matrix
        self.matrix = []

        # Experiment settingsguis output dataframe
        dict_tasksettings = {
            'Blocks': [blocks],
            'Faces': [self.matrixtypes],
            '# of Happy Faces': [happylen],
            '# of Sad Faces': [sadlen],
            '# of Angry Faces': [angrylen],
            '# of Fearful Faces': [fearlen],
            '# of Neutral Faces': [neulen],
            '# of Negative Non-Faces': [neglen],
            '# of Neutral Non-Faces': [neunflen]
        }

        # attach the task-specific settings to the task general settings
        self.set_settings(dict_tasksettings)

    def set_structure(self, matrixtype):
        """
        Takes in a string to describe the block about to occur and then sets up a list of strings
        :param matrixtype: a string for the matrix type that is about to occur
        """

        # make an empty list
        self.piclist = []

        # find out which block is occuring...
        match matrixtype:

            # when you find the block type...
            case 'Happy':

                # add those types of pictures to the list of pictures...
                self.piclist.append('Happy_')
                self.piclist.append('Neutral_')

            case 'Sad':
                self.piclist.append('Sad_')
                self.piclist.append('Neutral_')

            case 'Angry':
                self.piclist.append('Angry_')
                self.piclist.append('Neutral_')

            case 'Fearful':
                self.piclist.append('Fearful_')
                self.piclist.append('Neutral_')

            case _:
                self.piclist.append('NFNegative_')
                self.piclist.append('NFNeutral_')

    def nextround(self):
        """
        Each block is composed of emotional and reversed rounds of trials. This function checks to see if all of those
        rounds have been completed. If not, prompt the user that they will be doing a new round and to focus on a face.
        If so, check to see if all the blocks have been completed. If so, tell the participant that we'll be starting
        again. If not, then thank the partipant
        :return: list: string for participant instruction; integer to tell the gui whether there are still trials to do
        """

        # if there are still rounds to go in this block...
        if len(self.blockorder) > 0:

            # pop the next round
            self.blocktype = self.blockorder.pop()

            # set the structure for that round
            self.set_structure(self.blocktype)

            prompt = 'Please get ready for the next round.'

        # if all rounds in this block are done...
        else:

            # increment the block counter
            self.blocksdone += 1

            # if all blocks requested have been completed, thank the participant
            if self.blocksdone == self.blocks:

                prompt = 'Thank you! This task is complete.'

            # if there are still more blocks to go...
            else:

                # copy the list of rounds to a new list of rounds and then shuffle it
                self.blockorder = list(self.matrixtypes)
                random.shuffle(self.blockorder)

                # tell the participant that another block is starting
                prompt = 'You will now repeat the task you just completed.\nPress \"G\".'

        # return the list
        return prompt

    def set_matrix(self):
        """
        Setter function for the matrix
        """

        # start with empty list for the frame, center, and final matrix
        frame = []
        center = []
        self.matrix = []

        # make lists for the next set of for loops
        stimtype = ['emotional', 'neutral']
        picsex = ['male', 'female']
        picrace = ['white', 'nonwhite']

        for emoneu in stimtype:

            if (self.sexbalancing == 'Yes') & (self.racebalancing == 'Yes') & (self.piclist[0] != 'NFNegative_'):

                # get the strings for all of the white male emotional pictures in the picture directory
                emowmfilelist = glob.glob(self.picturedir + self.piclist[0] + 'M_' + 'W_' + '*.png')

                # get the strings for all of the white male neutral pictures in the picture directory
                neutralwmfilelist = glob.glob(self.picturedir + self.piclist[1] + 'M_' + 'W_' + '*.png')

                # get the strings for all of the white female emotional pictures in the picture directory
                emowffilelist = glob.glob(self.picturedir + self.piclist[0] + 'F_' + 'W_' + '*.png')

                # get the strings for all of the white female neutral pictures in the picture directory
                neutralwffilelist = glob.glob(self.picturedir + self.piclist[1] + 'F_' + 'W_' + '*.png')

                # get the strings for all of the nonwhite male emotional pictures in the picture directory
                emonwmfilelist = glob.glob(self.picturedir + self.piclist[0] + 'M_' + 'NW_' + '*.png')

                # get the strings for all of the nonwhite male neutral pictures in the picture directory
                neutralnwmfilelist = glob.glob(self.picturedir + self.piclist[1] + 'M_' + 'NW_' + '*.png')

                # get the strings for all of the nonwhite female emotional pictures in the picture directory
                emonwffilelist = glob.glob(self.picturedir + self.piclist[0] + 'F_' + 'NW_' + '*.png')

                # get the strings for all of the nonwhite female neutral pictures in the picture directory
                neutralnwffilelist = glob.glob(self.picturedir + self.piclist[1] + 'F_' + 'NW_' + '*.png')

                # repeat for each sex
                for sex in picsex:

                    # repeat for each race
                    for race in picrace:

                        # get 3 frame pictures for each 1 center picture
                        for pic in range(3):

                            # depending on what type of picture you want, pop it from the respective list, then remove
                            # the same face from the other (neutral vs emotional) list so you don't get duplicated in
                            # the same matrix, then append the picture to the list of pictures in the frame
                            if (emoneu == 'emotional') & (sex == 'male') & (race == 'white'):

                                face = emowmfilelist.pop()

                                neutralwmfilelist = [x for x in neutralwmfilelist if face[-6:] != x[-6:]]

                                frame.append(face)

                            elif (emoneu == 'neutral') & (sex == 'male') & (race == 'white'):

                                face = neutralwmfilelist.pop()

                                emowmfilelist = [x for x in emowmfilelist if face[-6:] != x[-6:]]

                                frame.append(face)

                            elif (emoneu == 'emotional') & (sex == 'female') & (race == 'white'):

                                face = emowffilelist.pop()

                                neutralwffilelist = [x for x in neutralwffilelist if face[-6:] != x[-6:]]

                                frame.append(face)

                            elif (emoneu == 'neutral') & (sex == 'female') & (race == 'white'):

                                face = neutralwffilelist.pop()

                                emowffilelist = [x for x in emowffilelist if face[-6:] != x[-6:]]

                                frame.append(face)

                            elif (emoneu == 'emotional') & (sex == 'male') & (race == 'nonwhite'):

                                face = emonwmfilelist.pop()

                                neutralnwmfilelist = [x for x in neutralnwmfilelist if face[-6:] != x[-6:]]

                                frame.append(face)

                            elif (emoneu == 'neutral') & (sex == 'male') & (race == 'nonwhite'):

                                face = neutralnwmfilelist.pop()

                                emonwmfilelist = [x for x in emonwmfilelist if face[-6:] != x[-6:]]

                                frame.append(face)

                            elif (emoneu == 'emotional') & (sex == 'female') & (race == 'nonwhite'):

                                face = emonwffilelist.pop()

                                neutralnwffilelist = [x for x in neutralnwffilelist if face[-6:] != x[-6:]]

                                frame.append(face)

                            else:

                                face = neutralnwffilelist.pop()

                                emonwffilelist = [x for x in emonwffilelist if face[-6:] != x[-6:]]

                                frame.append(face)

                        # do the same as the above but appending the pictures to the center as opposed to frame
                        if (emoneu == 'emotional') & (sex == 'male') & (race == 'white'):

                            face = emowmfilelist.pop()

                            neutralwmfilelist = [x for x in neutralwmfilelist if face[-6:] != x[-6:]]

                            center.append(face)

                        elif (emoneu == 'neutral') & (sex == 'male') & (race == 'white'):

                            face = neutralwmfilelist.pop()

                            emowmfilelist = [x for x in emowmfilelist if face[-6:] != x[-6:]]

                            center.append(face)

                        elif (emoneu == 'emotional') & (sex == 'female') & (race == 'white'):

                            face = emowffilelist.pop()

                            neutralwffilelist = [x for x in neutralwffilelist if face[-6:] != x[-6:]]

                            center.append(face)

                        elif (emoneu == 'neutral') & (sex == 'female') & (race == 'white'):

                            face = neutralwffilelist.pop()

                            emowffilelist = [x for x in emowffilelist if face[-6:] != x[-6:]]

                            center.append(face)

                        elif (emoneu == 'emotional') & (sex == 'male') & (race == 'nonwhite'):

                            face = emonwmfilelist.pop()

                            neutralnwmfilelist = [x for x in neutralnwmfilelist if face[-6:] != x[-6:]]

                            center.append(face)

                        elif (emoneu == 'neutral') & (sex == 'male') & (race == 'nonwhite'):

                            face = neutralnwmfilelist.pop()

                            emonwmfilelist = [x for x in emonwmfilelist if face[-6:] != x[-6:]]

                            center.append(face)

                        elif (emoneu == 'emotional') & (sex == 'female') & (race == 'nonwhite'):

                            face = emonwffilelist.pop()

                            neutralnwffilelist = [x for x in neutralnwffilelist if face[-6:] != x[-6:]]

                            center.append(face)

                        else:

                            face = neutralnwffilelist.pop()

                            emonwffilelist = [x for x in emonwffilelist if face[-6:] != x[-6:]]

                            center.append(face)

            # just sex balancing
            elif (self.sexbalancing == 'Yes') & (self.piclist[0] != 'NFNegative_'):

                # get the strings for all of the emotional pictures in the picture directory
                emomfilelist = glob.glob(self.picturedir + self.piclist[0] + 'M_' + '*.png')

                # get the strings for all of the neutral pictures in the picture directory
                emoffilelist = glob.glob(self.picturedir + self.piclist[0] + 'F_' + '*.png')

                # get the strings for all of the emotional pictures in the picture directory
                neutralmfilelist = glob.glob(self.picturedir + self.piclist[1] + 'M_' + '*.png')

                # get the strings for all of the neutral pictures in the picture directory
                neutralffilelist = glob.glob(self.picturedir + self.piclist[1] + 'F_' + '*.png')

                # repeat this 2 times so that you get 4 x 4 pictures in the matrix
                for halves in range(2):

                    # repeat for each sex
                    for sex in picsex:

                        # get 3 frame pictures for each 1 center picture
                        for pic in range(3):

                            # depending on what type of picture you want, pop it from the respective list, then remove
                            # the same face from the other (neutral vs emotional) list so you don't get duplicated in
                            # the same matrix, then append the picture to the list of pictures in the frame
                            if (emoneu == 'emotional') & (sex == 'male'):

                                face = emomfilelist.pop()

                                neutralmfilelist = [x for x in neutralmfilelist if face[-6:] != x[-6:]]

                                frame.append(face)

                            elif (emoneu == 'neutral') & (sex == 'male'):

                                face = neutralmfilelist.pop()

                                emomfilelist = [x for x in emomfilelist if face[-6:] != x[-6:]]

                                frame.append(face)

                            elif (emoneu == 'emotional') & (sex == 'female'):

                                face = emoffilelist.pop()

                                neutralffilelist = [x for x in neutralffilelist if face[-6:] != x[-6:]]

                                frame.append(face)

                            else:

                                face = neutralffilelist.pop()

                                emoffilelist = [x for x in emoffilelist if face[-6:] != x[-6:]]

                                frame.append(face)

                        # do the same as the above but appending the pictures to the center as opposed to frame
                        if (emoneu == 'emotional') & (sex == 'male'):

                            face = emomfilelist.pop()

                            neutralmfilelist = [x for x in neutralmfilelist if face[-6:] != x[-6:]]

                            center.append(face)

                        elif (emoneu == 'neutral') & (sex == 'male'):

                            face = neutralmfilelist.pop()

                            emomfilelist = [x for x in emomfilelist if face[-6:] != x[-6:]]

                            center.append(face)

                        elif (emoneu == 'emotional') & (sex == 'female'):

                            face = emoffilelist.pop()

                            neutralffilelist = [x for x in neutralffilelist if face[-6:] != x[-6:]]

                            center.append(face)

                        else:

                            face = neutralffilelist.pop()

                            emoffilelist = [x for x in emoffilelist if face[-6:] != x[-6:]]

                            center.append(face)

            # just race balancing
            elif (self.racebalancing == 'Yes') & (self.piclist[0] != 'NFNegative_'):

                # get the strings for all of the emotional pictures in the picture directory
                emowfilelist = glob.glob(self.picturedir + self.piclist[0] + '*_' + 'W_' + '*.png')

                # get the strings for all of the neutral pictures in the picture directory
                emonwfilelist = glob.glob(self.picturedir + self.piclist[0] + '*_' + 'NW_' + '*.png')

                # get the strings for all of the emotional pictures in the picture directory
                neutralwfilelist = glob.glob(self.picturedir + self.piclist[1] + '*_' + 'W_' + '*.png')

                # get the strings for all of the neutral pictures in the picture directory
                neutralnwfilelist = glob.glob(self.picturedir + self.piclist[1] + '*_' + 'NW_' + '*.png')

                # repeat this 2 times so that you get 4 x 4 pictures in the matrix
                for halves in range(2):

                    # repeat for white and nonwhite
                    for race in picrace:

                        # get 3 frame pictures for each 1 center picture
                        for pic in range(3):

                            # depending on what type of picture you want, pop it from the respective list, then remove
                            # the same face from the other (neutral vs emotional) list so you don't get duplicated in
                            # the same matrix, then append the picture to the list of pictures in the frame
                            if (emoneu == 'emotional') & (race == 'white'):

                                face = emowfilelist.pop()

                                neutralwfilelist = [x for x in neutralwfilelist if face[-6:] != x[-6:]]

                                frame.append(face)

                            elif (emoneu == 'neutral') & (race == 'white'):

                                face = neutralwfilelist.pop()

                                emowfilelist = [x for x in emowfilelist if face[-6:] != x[-6:]]

                                frame.append(face)

                            elif (emoneu == 'emotional') & (race == 'nonwhite'):

                                face = emonwfilelist.pop()

                                neutralnwfilelist = [x for x in neutralnwfilelist if face[-6:] != x[-6:]]

                                frame.append(face)

                            else:

                                face = neutralnwfilelist.pop()

                                emonwfilelist = [x for x in emonwfilelist if face[-6:] != x[-6:]]

                                frame.append(face)

                        # do the same as the above but appending the pictures to the center as opposed to frame
                        if (emoneu == 'emotional') & (race == 'white'):

                            face = emowfilelist.pop()

                            neutralwfilelist = [x for x in neutralwfilelist if face[-6:] != x[-6:]]

                            center.append(face)

                        elif (emoneu == 'neutral') & (race == 'white'):

                            face = neutralwfilelist.pop()

                            emowfilelist = [x for x in emowfilelist if face[-6:] != x[-6:]]

                            center.append(face)

                        elif (emoneu == 'emotional') & (race == 'nonwhite'):

                            face = emonwfilelist.pop()

                            neutralnwfilelist = [x for x in neutralnwfilelist if face[-6:] != x[-6:]]

                            center.append(face)

                        else:

                            face = neutralnwfilelist.pop()

                            emonwfilelist = [x for x in emonwfilelist if face[-6:] != x[-6:]]

                            center.append(face)

            # no non-default balancing because non-face
            else:

                # get the strings for all of the emotional pictures in the picture directory
                emofilelist = glob.glob(self.picturedir + self.piclist[0] + '*.png')

                # get the strings for all of the neutral pictures in the picture directory
                neutralfilelist = glob.glob(self.picturedir + self.piclist[1] + '*.png')

                # repeat this 4 times so that you get 4 x 4 pictures in the matrix
                for quarters in range(4):

                    # repeat this 3 times so that you get 3 frame pics
                    for pic in range(3):

                        # depending on which picture you're currently selecting, pop an emotional or neutral picture
                        if emoneu == 'emotional':

                            picture = emofilelist.pop()

                            frame.append(picture)

                        else:

                            picture = neutralfilelist.pop()

                            frame.append(picture)

                    # do the same as above but only once and for the center, not frame
                    if emoneu == 'emotional':

                        picture = emofilelist.pop()

                        center.append(picture)

                    else:

                        picture = neutralfilelist.pop()

                        center.append(picture)

        # shuffle the pictures in the center and frame lists for extra randomization
        random.shuffle(frame)
        random.shuffle(center)

        # go through the following for loops to make the entire matrix
        for firstframecell in range(5):
            self.matrix.append(frame.pop())

        for firstcentercell in range(2):
            self.matrix.append(center.pop())

        for secondframecell in range(2):
            self.matrix.append(frame.pop())

        for lastcentercell in range(2):
            self.matrix.append(center.pop())

        for lastframecell in range(5):
            self.matrix.append(frame.pop())

    def get_matrix(self):
        """
        Getter function for the matrix
        :return: list of picture names for the matrix
        """

        return self.matrix

    def updateoutput(self, trial, onset):
        """
        Consolidates what was just shown in the trial and updates the performance dataframe
        in the superclass
        :param trial: the number of the trial that was just completed
        :param onset: onset time for the trial
        """

        # make a dictionary of trial info
        df_trial = {
            'trial': [trial],
            'block type': [self.blocktype],
            'matrix': [self.get_matrix()],
            'onset': [onset],
        }

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

                inst = 'In this task, sets of pictures will appear\non the screen.'

            case 2:

                inst = 'You do not have to push any buttons or click\nthe mouse during this task.'

            case 3:

                inst = 'Some pictures will be of faces. Other pictures\nwill be of places, objects, etc.'

            case _:

                inst = 'Let the experimenter know when you are ready.'

        return inst
