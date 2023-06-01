from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QSpinBox, QLineEdit, QVBoxLayout, QDialog, \
    QCheckBox, QFormLayout, QFileDialog, QComboBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from os import path

from Guis import main


class DirErrorBox(QDialog):
    """
    This is a popup window that may come up after the settings window checks to see if the directory that the user
    selected is a valid directory. If not, this popup lets the user know that they goofed.
    """

    def __init__(self, dirtype):
        super().__init__()

        self.setWindowTitle('Error')

        # Make  layout
        dialayout = QVBoxLayout()

        # Make labels for text, changing the main error depending on if the working directory or picture directory (for
        # EGNG/Dwell was the problem
        if dirtype == 'WD':
            maintext = 'It looks like you entered an invalid working directory!'

        else:
            maintext = 'It looks like you entered an invalid picture directory!'

        self.mainerror = QLabel(maintext)
        self.mainerror.setStyleSheet('padding :5px')

        insttext = 'Make sure you can access the folder normally, and make sure that any network or wired connection' \
                   ' is secure.'

        self.instruction = QLabel(insttext)
        self.instruction.setStyleSheet('padding :5px')

        # Add stuff to overarching layout
        dialayout.addWidget(self.mainerror),
        dialayout.addWidget(self.instruction)

        self.setLayout(dialayout)


class FormatErrorBox(QDialog):
    """
    This is a popup window that may come up after the EGNG/Dwell settings window if there are no properly-formatted
    pictures found in the picture directory. This may be due to no pictures having the proper prefix (e.g., 'Angry_')
    or due to no pictures being in the PNG format
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Error')

        # Make  layout
        dialayout = QVBoxLayout()

        # Make labels for text
        self.mainerror = QLabel('I could not find any compatible pictures in your picture directory!')
        self.mainerror.setStyleSheet('padding :5px')

        text = 'First, make sure all pictures are in the PNG format.\nSecond, make sure all of the pictures have the' \
               'proper naming structure.\nFor example, if I had 10 pictures of angry faces made by white males, they ' \
               'would be named \"Angry_M_W_1.png.png\", \"Angry_M_W_2.png\",...\"Angry_M_W_10.png\".'

        self.instruction = QLabel(text)
        self.instruction.setStyleSheet('padding :5px')

        # Add stuff to overarching layout
        dialayout.addWidget(self.mainerror),
        dialayout.addWidget(self.instruction)

        self.setLayout(dialayout)


class FileErrorBox(QDialog):
    """
    This is a popup window that may come up after the settingsguis window checks to see if the file that the user
    will create alreaedy exists. If so, this popup lets the user know that they goofed and tells them to delete the
    old file or change their settings
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Error')

        # Make  layout
        dialayout = QVBoxLayout()

        # Make labels for text
        self.mainerror = QLabel('It looks like your file already exists!')
        self.mainerror.setStyleSheet('padding :5px')

        self.instruction = QLabel('Either delete the old file, pick a new directory, or change your ID, session name' +
                                  ', or task.')
        self.instruction.setStyleSheet('padding :5px')

        # Add stuff to overarching layout
        dialayout.addWidget(self.mainerror),
        dialayout.addWidget(self.instruction)

        self.setLayout(dialayout)


class SelectErrorBox(QDialog):
    """
    This is a popup window that may come up after the Emo Go/NoGo window checks to see if the user select any of the
    emotional faces. If not, it tells the user to do so.
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Error')

        # Make  layout
        dialayout = QVBoxLayout()

        # Make labels for text
        self.mainerror = QLabel('It looks like you didn\'t select an emotional face!')
        self.mainerror.setStyleSheet('padding :5px')

        text = 'Please select at least one of happy, sad, angry, or fearful.'

        self.instruction = QLabel(text)
        self.instruction.setStyleSheet('padding :5px')

        # Add stuff to overarching layout
        dialayout.addWidget(self.mainerror),
        dialayout.addWidget(self.instruction)

        self.setLayout(dialayout)


class MathErrorBox(QDialog):
    """
    This is a popup window that may come up after the settingsguis window checks to see if the math works out.
    Condition is determined by the settingsguis GUI that has the error and the settingsguis within that. For example,
    PBT needs to be divisible by 4 because there are four pictures. Framing needs to be divisible by 2 if gains and
    losses are enabled, divisible by 3 if FTT is enabled, and divisible by 6 if both are enabled.
    """

    def __init__(self, state):
        super().__init__()

        self.setWindowTitle('Input Error')

        # Make  layout
        dialayout = QVBoxLayout()

        # Make labels for text

        self.mainerror = QLabel('Your number of trials isn\'t compatible with the settings and/or task you chose!')
        self.mainerror.setStyleSheet('padding :5px')

        match state:

            case 1:

                followupstring = 'There are 4 pictures for stimuli, so the total number of trials must be ' \
                                 'divisible by 4.'

            case 2:

                followupstring = 'You enabled gains and losses, so your number of trials should be divisible by 2.'

            case 3:

                followupstring = 'You enabled FTT, so your number of trials should be divisible by 3.'

            case 4:

                followupstring = 'You enabled FTT and need gains and losses, so your number of trials should' \
                                 ' be divisible by 6 (minimum Gist, Mixed, and Verbatim version of 1 gain and' \
                                 ' 1 loss question.'

            case 5:

                followupstring = 'There are 4 task difficulty levels, so the total number of trials must be ' \
                                 'divisible by 3 (enough for 1 to be compared to 2, 3, and 4) in the original task.'

            case 6:

                followupstring = 'There are 4 task difficulty levels, so the total number of trials must be ' \
                                 'divisible by 6 (enough for each difficulty to be compared) in the alternate task.'

            case 7:

                followupstring = 'It seems that the number of high value and low trials you entered means that ' \
                                 'the participants could end up with less money than the minimum allowed.' \
                                 '\n(# of low value trials X $0.15) + (# of low value trials X $0.03) <= ' \
                                 'starting money - minimum money that a participants can leave with.'

            case 8:

                followupstring = 'To easily balance the number of neutral vs. emotional faces, please make sure your' \
                                 ' number of trials is divisible by 4.'

            case 9:

                followupstring = 'For the dwell task, make sure you have at least 16 pictures for each type of matrix' \
                                 ' you selected!'

            case 10:

                followupstring = 'For the stop signal task, we balance tasks for left and right arrows, so make sure ' \
                                 'your number of trial is divisible by 2.'

            case _:

                followupstring = 'I don\'t know what you put, but the math doesn\'t work out'

        self.followup = QLabel(followupstring)
        self.followup.setStyleSheet('padding :5px')

        # Add stuff to overarching layout
        dialayout.addWidget(self.mainerror),
        dialayout.addWidget(self.followup)

        self.setLayout(dialayout)


class CitationWindow(QDialog):
    """
    This is a popup window that will give the APA citation for the task that the user selected
    """

    def __init__(self, task):
        super().__init__()

        self.setWindowTitle('APA Citation')

        # Make  layout
        dialayout = QVBoxLayout()

        # Make labels for text

        self.description = QLabel('The following is the APA citation for the task:')
        self.description.setStyleSheet('padding :5px')

        match task:

            case str('DD'):

                followupstring = 'Du, W., Green, L., & Myerson, J. (2002). Cross-cultural comparisons of ' \
                                 'discounting delayed and probabilistic rewards. The Psychological Record, 52(4), ' \
                                 '479-492.'

            case str('PD'):

                followupstring = 'Madden, G.J., Petry, N.M., & Johnson, P.S. (2009). Pathological gamblers discount ' \
                                 'probabilistic rewards less steeply than matched controls. Experimental and ' \
                                 'Clinical Psychopharmacology, 17(5), 283–290. https://doi.org/10.1037/a0016806.'

            case str('CEDT'):

                followupstring = 'Westbrook, A., Kester, D., & Braver T.S. (2013). What is the subjective cost of ' \
                                 'cognitive effort? Load, trait, and aging effects revealed by economic preference.' \
                                 ' PLOS ONE, 8(7), e68210. https://doi.org/10.1371/journal.pone.0068210.'

            case str('ARTT'):

                followupstring = 'Agnieszka, T., Belmaker, L.A.R., Roy, A.K., Ruderman, L., Manson, K., Glimcher, ' \
                                 'P.W., & Levy, I. (2012). Adolescents’risk-taking behavior is driven by tolerance to' \
                                 ' ambiguity. Proceedings of the National Academy of Sciences, 109(42), 17135–17140. ' \
                                 'https://doi.org/10.1073/pnas.1207144109.'

            case str('RA'):

                followupstring = 'Kahneman, D. & Tversky, A. (1979). Prospect theory: An analysis of decision under ' \
                                 'risk. Econometrica, 47(2), 263-292.'

            case str('Framing'):

                followupstring = 'Broniatowski, D.A. & Reyna, V.F. (2018). A formal model of fuzzy-trace theory: ' \
                                 'Variations on framing effects and the Allais paradox. Decision (Washington, D.C.), ' \
                                 '5(4), 205–252. https://doi.org/10.1037/dec0000083.'

            case str('Beads'):

                followupstring = 'Moutoussis, M., Bentall, R.P., El-Deredy, W., & Dayan, P. (2011). Bayesian ' \
                                 'modelling of Jumping-to-Conclusions bias in delusional patients. Cognitive ' \
                                 'Neuropsychiatry, 16(5), 422-447. https://doi.org/10.1080/13546805.2010.548678.'

            case str('Dwell'):

                followupstring = 'Lazarov, A., Abend, R., & Bar-Haim, Y. (2016). Social anxiety is related to increased' \
                                 ' dwell time on socially threatening faces. Journal of Affective Disorders, 193, ' \
                                 '282-288. https://doi.org/10.1016/j.jad.2016.01.007.'

            case str('Stroop'):

                followupstring = 'MacLeod, C.M. (1991). Half a century of research on the Stroop effect: An ' \
                                 'integrative review. Psychological Bulletin, 109(2), 163–203. ' \
                                 'https://doi.org/10.1037/0033-2909.109.2.163.'

            case str('PBT'):

                followupstring = 'de Fockert, J.W. & Cooper, A. (2014). Higher levels of depression are associated ' \
                                 'with reduced global bias in visual processing. Cognition and Emotion, 28(3), ' \
                                 '541–549. https://doi.org/10.1080/02699931.2013.839939.'

            case str('NACT'):

                followupstring = 'Anderson, B.A., Faulkner, M.L., Rilee, J.J., Yantis, S., & Marvel, C.L. (2013). ' \
                                 'Attentional bias for nondrug reward is magnified in addiction. Experimental and ' \
                                 'Clinical Psychopharmacology, 21(6), 499–506. ' \
                                 'https://doi.org/10.1037/a0034575.'

            case str('SS'):

                followupstring = 'Logan, G.D. (1994). On the ability to inhibit thought and action: A user’s guide to' \
                                 ' the stop signal paradigm. In D. Dagenbach & T.H. Carr (Eds.), Inhibitory ' \
                                 'processes in attention, memory and language. Academic Press.'

            case str('PR'):

                followupstring = 'Brainerd, C.J., & Reyna, V.F. (2010). Recollective and Nonrecollective Recall. ' \
                                 'Journal of Memory and Language, 63(3), 425–445. ' \
                                 'https://doi.org/10.1016/j.jml.2010.05.002.'

            case str('DS'):

                followupstring = 'Ramsay, M.C., & Reynolds, C.R. (1995). Separate digits tests: A brief history, a' \
                                 ' literature review, and a reexamination of the factor structure of the Test of ' \
                                 'Memory and Learning (TOMAL). Neuropsychology Review, 5(3), 151–171. ' \
                                 'https://doi.org/10.1007/BF02214760.'

            case str('NB'):

                followupstring = 'Owen, A.M., McMillan, K.M., Laird, A.R., & Bullmore, E. (2005). N‐back working' \
                                 ' memory paradigm: A meta‐analysis of normative functional neuroimaging studies. ' \
                                 'Human brain mapping, 25(1), 46-59. https://doi.org/10.1002/hbm.20131.'

            case str('EGNG'):

                followupstring = 'Tottenham, N., Hare, T.A., & Casey, B.J. (2011). Behavioral assessment of ' \
                                 'emotion discrimination, emotion regulation, and cognitive control in childhood, ' \
                                 'adolescence, and adulthood. Frontiers in Psychology, 2, 1-9. ' \
                                 'https://doi.org/10.3389/fpsyg.2011.00039.'

            case str('GNG'):

                followupstring = 'Casey, B.J., Trainor, R.J., Orendi, J.L., Schubert, A.B., Nystrom, L.E., ' \
                                 'Giedd, J.N., Castellanos, F.X., Haxby, J.V., Noll, D.C., Cohen, J.D., Forman, ' \
                                 'S.D., Dahl, R.E., and Rapoport, J.L. (1997). A Developmental functional MRI ' \
                                 'study of prefrontal activation during performance of a go–no-go task. Journal of ' \
                                 'Cognitive Neuroscience, 9(6), 835–847. https://doi.org/10.1162/jocn.1997.9.6.835.'

            case _:

                followupstring = 'I have no idea what you chose or how to cite it...'

        self.followup = QLabel(followupstring)
        self.followup.setStyleSheet('padding :5px')

        # make sure the text wraps so the dialog isn't weird-looking
        self.followup.setWordWrap(True)
        self.followup.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        # Add stuff to overarching layout
        dialayout.addWidget(self.description),
        dialayout.addWidget(self.followup)

        self.setLayout(dialayout)


class Settings(QWidget):
    """
    Main class for the settingsguis window. This guy has all of the characteristics and things that every settingsguis
    window should have: A quit button, a submit settingsguis button, a minimum window size, a function for checking
    that the user inputted a valid directory, etc.
    """

    def __init__(self, task):
        super().__init__()

        # Window title
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # setting the geometry of window
        self.setGeometry(0, 0, 700, 400)

        # center window
        self.centerscreen()

        # Defaults for various tasks and options
        self.task = task
        self.outcome = 'No'
        self.eyetracking = 'No'
        self.fmri = 'No'
        self.feedback = 'No'
        self.ftt = 'No'
        self.stt = 'No'
        self.confidence = 'No'
        self.adopystate = 'No'

        # defaults for EGNG and Dwell
        self.happy = 'No'
        self.fear = 'No'
        self.angry = 'No'
        self.sad = 'No'
        self.neg = 'No'

        # balancing for Dwell task
        self.sexbalancing = 'No'
        self.racebalancing = 'No'

        # Default directory
        self.wd = ''

        # Default picture directory
        self.picd = ''

        # Make overarching layout
        self.over_layout = QVBoxLayout()

        # Make a label with instructions
        self.header = QLabel('Enter the appropriate values:', self)
        self.header.setFont(QFont('Helvetica', 30))
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add header to overarching layout
        self.over_layout.addWidget(self.header)

        # General settings
        # ID
        self.idform = QLineEdit()
        self.idform.setText('9999')

        # Session form
        self.sessionin = QLineEdit()
        self.sessionin.setText('Pretest')

        # Dropdown box for control options
        self.controls = QComboBox()
        self.controls.addItems(['Default (C & M)', 'Buttonbox (1 & 2)', 'Mouse'])

        # Trials input
        self.trialsin = QSpinBox()
        self.trialsin.setValue(5)
        self.trialsin.setRange(1, 1000)

        # Blocks input
        self.blocksin = QSpinBox()
        self.blocksin.setValue(1)
        self.blocksin.setMinimum(1)

        # WD input
        self.wdset = QPushButton('Select Directory')
        self.wdset.clicked.connect(self.fileselect)
        self.wdlabel = QLabel(self.wd)

        # Submit button
        self.submit = QPushButton('Submit')
        self.submit.clicked.connect(self.checksettings)

        # Main menu button
        self.menubutton = QPushButton('Main Menu')
        self.menubutton.clicked.connect(self.mainmenu)

        # Main menu button
        self.citationbutton = QPushButton('Get Task Citation')
        self.citationbutton.clicked.connect(self.citation)

        # Quit button
        self.quitbutton = QPushButton('Quit')
        self.quitbutton.clicked.connect(QApplication.instance().quit)
        self.quitbutton.resize(self.quitbutton.sizeHint())

        # fMRI checkbox
        self.fmritoggle = QCheckBox()
        self.fmritoggle.stateChanged.connect(self.clickbox)

        # Eyetracking checkbox
        # self.eyetrackingtoggle = QCheckBox()
        # self.eyetrackingtoggle.stateChanged.connect(self.clickbox)

        # Task specific things
        # Starting money input
        self.smoneyin = QSpinBox()
        self.smoneyin.setValue(25)
        self.smoneyin.setRange(0, 10000)

        # ADOPy checkbox
        # self.adopytoggle = QCheckBox()
        # self.adopytoggle.stateChanged.connect(self.clickbox)

        # FTT checkbox for framing task
        self.ftttoggle = QCheckBox()
        self.ftttoggle.stateChanged.connect(self.clickbox)

        # ST Trials checkbox for paired recall task
        self.stttoggle = QCheckBox()
        self.stttoggle.stateChanged.connect(self.clickbox)

        # ST Trials checkbox for paired recall task
        self.confidencetoggle = QCheckBox()
        self.confidencetoggle.stateChanged.connect(self.clickbox)

        # checkbox for getting a random outcome, specifically in decision tasks
        self.outcometoggle = QCheckBox()
        self.outcometoggle.stateChanged.connect(self.clickbox)

        # checkbox for getting feedback, in things like nback tasks
        self.feedtoggle = QCheckBox()
        self.feedtoggle.stateChanged.connect(self.clickbox)

        # things for EGNG/Dwell
        # picture directory input
        self.picdset = QPushButton('Select Picture Directory')
        self.picdset.clicked.connect(self.picdirselect)
        self.picdlabel = QLabel(self.picd)

        # Happy checkbox
        self.happytoggle = QCheckBox('Happy?')
        self.happytoggle.stateChanged.connect(self.clickbox)

        # Sad checkbox
        self.sadtoggle = QCheckBox('Sad?')
        self.sadtoggle.stateChanged.connect(self.clickbox)

        # Anger checkbox
        self.angertoggle = QCheckBox('Angry?')
        self.angertoggle.stateChanged.connect(self.clickbox)

        # Fear checkbox
        self.feartoggle = QCheckBox('Fearful?')
        self.feartoggle.stateChanged.connect(self.clickbox)

        # Negative checkbox
        self.negtoggle = QCheckBox('Negative (vs neutral) non-faces?')
        self.negtoggle.stateChanged.connect(self.clickbox)

        # Sex balancing checkbox
        self.sexbalancetoggle = QCheckBox('')
        self.sexbalancetoggle.stateChanged.connect(self.clickbox)

        # race balancing checkbox
        self.racebalancetoggle = QCheckBox('')
        self.racebalancetoggle.stateChanged.connect(self.clickbox)

        # Make form layout for all the settingsguis
        self.layout = QFormLayout()
        self.layout.addRow(self.menubutton, self.citationbutton)
        self.layout.addRow(QLabel('Subject ID:'), self.idform)
        self.layout.addRow(QLabel('Session name/number (enter \"Practice\" to not have output):'), self.sessionin)

        # only allow for controls selection for tasks other than the digit span
        if task != 'DS':
            self.layout.addRow(QLabel('What controls do you want to use?'), self.controls)

        # Show all elements
        self.show()

    def centerscreen(self):
        """
        Finds the geometry of the computer's screen and moves the window to the center of it
        """

        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def clickbox(self):
        """
        This is a function that will activate whenever you click on one of the checkboxes. When one box is clicked, the
        function will check the status of every box and edit the respective class variable based on the state of the
        box.
        """

        # outcome for decision tasks
        if self.outcometoggle.isChecked():
            self.outcome = 'Yes'
        else:
            self.outcome = 'No'

        # feedback for digit span
        if self.feedtoggle.isChecked():
            self.feedback = 'Yes'
        else:
            self.feedback = 'No'

        # eyetracking
        # if self.eyetrackingtoggle.isChecked():
        #     self.eyetracking = 'Yes'
        # else:
        #     self.eyetracking = 'No'

        # fmri timing option
        if self.fmritoggle.isChecked():
            self.fmri = 'Yes'
        else:
            self.fmri = 'No'

        # ADOPy
        # if self.adopytoggle.isChecked():
        #     self.adopystate = 'Yes'
        # else:
        #     self.adopystate = 'No'

        # FTT for framing
        if self.ftttoggle.isChecked():
            self.ftt = 'Yes'
        else:
            self.ftt = 'No'

        # FTT for framing
        if self.confidencetoggle.isChecked():
            self.confidence = 'Yes'
        else:
            self.confidence = 'No'

        # happy for EGNG/Dwell
        if self.happytoggle.isChecked():
            self.happy = 'Yes'
        else:
            self.happy = 'No'

        # sad for EGNG/Dwell
        if self.sadtoggle.isChecked():
            self.sad = 'Yes'
        else:
            self.sad = 'No'

        # angry for EGNG/Dwell
        if self.angertoggle.isChecked():
            self.angry = 'Yes'
        else:
            self.angry = 'No'

        # fearful for EGNG/Dwell
        if self.feartoggle.isChecked():
            self.fear = 'Yes'
        else:
            self.fear = 'No'

        # fearful for EGNG/Dwell
        if self.negtoggle.isChecked():
            self.neg = 'Yes'
        else:
            self.neg = 'No'

        # sex balancing for Dwell
        if self.sexbalancetoggle.isChecked():
            self.sexbalancing = 'Yes'
        else:
            self.sexbalancing = 'No'

        # race balancing for Dwell
        if self.racebalancetoggle.isChecked():
            self.racebalancing = 'Yes'
        else:
            self.racebalancing = 'No'

    def checksettings(self):
        """
        Once you hit submit, the following function is called, which figures out if the selected directory is valid. If
        not, it calls the directory error function. If the directory is valid, it then checks if a file exists in that
        location that would be overwritten. If there is, it calls the file error function. If there is not pre-existing
        file, then it calls the function that submits the settings.
        """

        if path.isdir(self.wd):

            if path.isfile(self.wd + '/' + self.idform.text() + '_' + self.task + '_' + self.sessionin.text() +
                           '.xlsx'):
                self.fileerrordialog()

            else:
                self.submitsettings()

        else:
            self.wderrordialog()

    def mainmenu(self):
        """
        sends the user back to the main menu
        :return:
        """

        self.w = main.SelectWindow()
        self.w.show()
        self.hide()

    def citation(self):
        """
        This function opens a text dialog that gives the citation for the task
        """

        cite = CitationWindow(self.task)

        cite.exec()

    def fileselect(self):
        """
        This function creates a dialog window to select a directory that will be the output directoty and then sets
        the class variable (and associated QLabel) for the working directory to the directory you chose
        """

        folder = QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.wd = str(folder)
        self.wdlabel.setText(self.wd)

    def picdirselect(self):
        """
        This function creates a dialog window to select a directory that has the pictures needed for the EGNG task
        """

        folder = QFileDialog.getExistingDirectory(self, 'Select Picture Directory')
        self.picd = str(folder)
        self.picdlabel.setText(self.picd)

    def wderrordialog(self):
        """
        This function activates if the output directory submitted is not valid
        """

        error = DirErrorBox('WD')

        error.exec()

    def fileerrordialog(self):
        """
        This function activates if the output directory is valid but a file exists there that would be overwritten if
        the program were to run with the selected task.
        """

        error = FileErrorBox()

        error.exec()

    def selecterror(self):
        """
        This function activates if no face type was selected
        """

        error = SelectErrorBox()

        error.exec()

    def picdirerrordialog(self):
        """
        This function activates if the picture directory submitted for EGNG/Dwell is not valid
        """

        error = DirErrorBox('Pic')

        error.exec()

    def formaterrordialog(self):
        """
        This function activates if there is a problem finding usable, properly-formatted pictures in the above directory
        """

        error = FormatErrorBox()

        error.exec()

    def matherrordialog(self, state):
        """
        This function activates if there is a problem with the settings such that the math doesn't work out. It takes
        one argument which determines the text of the resulting error dialog window.
        :param state: an integer that indicates what type of math error happened and what the resulting text in the
        error should be.
        """

        error = MathErrorBox(state)

        error.exec()

    def submitsettings(self):
        """
        This function activates if you hit submit on a settings window and both the directory is valid and a file
        doesn't already exist. Since the resulting actions will depend on the selected task, this is left blank here.
        """

        print('If you see this, panic')
