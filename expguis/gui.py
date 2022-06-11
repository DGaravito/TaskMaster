from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QApplication, QLabel
from PyQt6.QtCore import Qt, QDir, QTimer
from PyQt6.QtGui import QFont

from pathlib import Path


class Experiment(QWidget):
    def __init__(self, person):
        super().__init__()

        # Set defaults for starting variables for the majority of tasks
        self.response = 0
        self.person = person
        self.trialsdone = 0
        self.roundsdone = 0
        self.inst = 0

        # eyetracking setup
        if self.person.eyetracking == 'Yes':
            print('eyetracking time yay')

        # Window title
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # center window
        self.centerscreen()

        # Add the assets folder for pictures
        toassets = str(Path('..').resolve())
        QDir.addSearchPath('assets', toassets)

        # Prepare all the elements that most/all tasks have
        self.defaultelements()

        # Prepare all the elements for the specific task
        self.elements()

        # Attach keyboard keys to the keyaction function
        self.keyPressed.connect(self.keyaction)

        # Make timer to indicate when someone to start a new trial
        self.ititimer = QTimer()
        self.ititimer.timeout.connect(self.generatenext)

        # Make timer to indicate when someone took too long
        self.timer = QTimer()
        self.timer.timeout.connect(self.timeout)

        # Make timer for resetting after the above warning (only in non-fmri experiments)
        self.trialresettimer = QTimer()
        self.trialresettimer.timeout.connect(self.responsereset)

    def centerscreen(self):
        """
        All this does is get the geometry of the screen and then make the window that size
        """

        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def keyPressEvent(self, keyevent):
        """
        This tells PyQt to return the text of a key when a key is pressed
        """

        self.keyPressed.emit(keyevent.text())

    def defaultelements(self):
        """
        This function will add in the default elements. Anything in here would be stuff that most or all tasks use
        """

        # Make overarching layout
        self.instquitlayout = QVBoxLayout()

        # Quit button
        self.quitbutton = QPushButton('Quit')
        self.quitbutton.clicked.connect(QApplication.instance().quit)
        self.quitbutton.setFixedWidth(40)
        self.quitbutton.setFixedHeight(20)

        # Instructions - default is blank, of course
        self.instructions = QLabel('')

        # setting instructions font style and size and centering
        self.instructions.setFont(QFont('Helvetica', 30))
        self.instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # add the middle, which will always have the same starting text
        self.middle = QLabel('Press \"G\" to start, \"I\" for instructions')
        self.middle.setFont(QFont('Helvetica', 40))

        # center middle
        self.middle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.middle.setScaledContents(True)

    def elements(self):
        """
        This is a function to create task-specific elements that, obviously, will completely change depending on
        the specific task. So it's blank for a reason
        """

    def iti(self):
        """
        This is a default inter-trial-interval function. By default, this will just set the middle to a fixation cross
        """

        self.middle.setText('+')

    def generatenext(self):
        """
        This is a default function to move to a new trial for a task. This, obviously, will completely change
        depending on the specific task. So it's blank for a reason
        """

    def timeout(self):
        """
        This is a default function that activates if a participant takes too long to respond. What happens because of
        that is, obviously, task specific, so it's blank for a reason
        """

    def responsereset(self):
        """
        This is a default function that activates if the task is run without the fmri mode on. It resets the trial
        after a participant takes too long to respond. Again, this is very task specific, so it's blank for a reason
        """

    def keyaction(self, key):
        """
        This function will execute when a key is pressed. This is basically empty because the individual tasks will
        change what happens when the key is pressed
        :param key: the text returned when that key is pressed
        """
        print(key)
