from PyQt4 import QtGui, QtCore

class OptionsDialog(QtGui.QDialog):
    '''
    Argentum Options Dialog
    '''

    optionsToAdd = {'horizontal_offset': 'Distance between cartridges',
                    'vertical_offset': 'Misalignment of print heads on cartridges',
                    'print_overlap': 'Distance to move between lines',
                    'dilate_count': 'Extra thickness of asorbic'}
    created = {}

    def __init__(self, parent=None, options=None):

        QtGui.QWidget.__init__(self, parent)

        self.parent = parent
        self.options = options

        #--Layout Stuff---------------------------#
        mainLayout = QtGui.QVBoxLayout()

        if self.options:
            self.addOptions(mainLayout, self.options)

        #--The Button------------------------------#
        layout = QtGui.QHBoxLayout()
        button = QtGui.QPushButton("Save") #string or icon
        #self.connect(button, QtCore.SIGNAL("clicked()"), self.close)
        button.clicked.connect(self.gatherValues)
        layout.addWidget(button)

        mainLayout.addLayout(layout)
        self.setLayout(mainLayout)

        self.resize(400, 60)
        self.setWindowTitle('Printer Options')

    def createOptionWidget(self, parentLayout, optionName, defaultValue):
        # Create a Sub-Layout for this option
        #layout = QtGui.QHBoxLayout()

        self.addLabel(parentLayout, self.optionsToAdd[optionName])

        # Make sure it's a string with str(...)
        optionLineEdit = QtGui.QLineEdit(str(defaultValue))
        parentLayout.addWidget(optionLineEdit)

        return optionLineEdit

    def addOptions(self, parentLayout, options):
        for optionName in self.optionsToAdd:
            if optionName in self.options:
                defaultValue = self.options[optionName]
            else:
                defaultValue = 0

            layout = QtGui.QHBoxLayout()

            widget = self.createOptionWidget(layout, optionName, defaultValue)

            self.created[optionName] = widget

            parentLayout.addLayout(layout)

    def addLabel(self, layout, labelText):
        label = QtGui.QLabel()
        label.setText(labelText)
        layout.addWidget(label)

    def gatherValues(self):
        options = self.options

        for name, widget in self.created.items():
            options[name] = str(widget.text())

        self.parent.updatePrinterOptions(options)

        self.close()


class InputDialog(QtGui.QDialog):
   '''
   this is for when you need to get some user input text
   '''

   def __init__(self, parent=None, title='user input', label='comment', text=''):

       QtGui.QWidget.__init__(self, parent)

       #--Layout Stuff---------------------------#
       mainLayout = QtGui.QVBoxLayout()

       layout = QtGui.QHBoxLayout()
       self.label = QtGui.QLabel()
       self.label.setText(label)
       layout.addWidget(self.label)

       self.text = QtGui.QLineEdit(text)
       layout.addWidget(self.text)

       mainLayout.addLayout(layout)

       #--The Button------------------------------#
       layout = QtGui.QHBoxLayout()
       button = QtGui.QPushButton("okay") #string or icon
       #self.connect(button, QtCore.SIGNAL("clicked()"), self.close)
       button.clicked.connect(self.close)
       layout.addWidget(button)

       mainLayout.addLayout(layout)
       self.setLayout(mainLayout)

       self.resize(400, 60)
       self.setWindowTitle(title)


class CommandLineEdit(QtGui.QLineEdit):
    submit_keys = [QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return]

    # Order must be up, down
    arrow_keys = [QtCore.Qt.Key_Up, QtCore.Qt.Key_Down]

    command_history = []
    history_index = -1
    last_content = ''

    def __init__(self, *args):
        QtGui.QLineEdit.__init__(self, *args)

    def event(self, event):
        if (event.type() == QtCore.QEvent.KeyPress):
            key = event.key()

            if key in self.submit_keys:
                self.emit(QtCore.SIGNAL("enterPressed"))

                # We leave the signal catcher to call self.submit_command()

                return True

            if key in self.arrow_keys:
                if len(self.command_history) < 1:
                    return True

                if self.history_index < 0:
                    self.last_content = str(self.text())

                if key == self.arrow_keys[0]:
                    self.history_index = min(self.history_index + 1, len(self.command_history) - 1)
                else:
                    self.history_index = max(self.history_index - 1, -1)

                if self.history_index < 0:
                    command = self.last_content
                else:
                    command = self.command_history[self.history_index]

                self.setText(command)

                return True

        return QtGui.QLineEdit.event(self, event)

    def submit_command(self):
        command = str(self.text())

        self.history_index = -1
        self.command_history.insert(0,command)

        self.setText("")

class RollerCalibrationDialog(QtGui.QDialog):
    '''
    Roller Calibration Dialog
    '''

    def __init__(self, controller, parent=None):

        QtGui.QWidget.__init__(self, parent)

        self.controller = controller
        self.parent = parent

        #--Layout Stuff---------------------------#
        mainLayout = QtGui.QVBoxLayout()

        # Controls Here
        row = QtGui.QHBoxLayout()
        self.addButton(row, "Disable Rollers", self.disableRollers)
        self.addButton(row, "Enable Rollers", self.enableRollers)
        mainLayout.addLayout(row)

        row = QtGui.QHBoxLayout()
        self.addButton(row, "Up ^", self.rollerUp)
        self.addButton(row, "Retract", self.rollerRetract)
        mainLayout.addLayout(row)

        row = QtGui.QHBoxLayout()
        self.addButton(row, "Down v", self.rollerDown)
        self.addButton(row, "Deploy", self.rollerDeploy)
        mainLayout.addLayout(row)

        row = QtGui.QHBoxLayout()
        self.addButton(row, "Set Retract Position", self.setRetractPosition)
        self.addButton(row, "Set Deploy Position", self.setDeployPosition)
        mainLayout.addLayout(row)

        #--The Button------------------------------#
        layout = QtGui.QHBoxLayout()
        button = QtGui.QPushButton("Close")
        self.connect(button, QtCore.SIGNAL("clicked()"), self.close)
        layout.addWidget(button)
        saveButton = self.addButton(layout, "Save", self.save)
        mainLayout.addLayout(layout)

        self.setLayout(mainLayout)

        self.resize(200, 60)
        self.setWindowTitle('Roller Calibration')

        saveButton.setDefault(True)
        saveButton.setFocus()
        self.enableRollers()

    def disableRollers(self):
        if self.controller:
            self.controller.rollerCommand('e')

    def enableRollers(self):
        if self.controller:
            self.controller.rollerCommand('E')

    def rollerUp(self):
        if self.controller:
            self.controller.rollerCommand('+')

    def rollerDown(self):
        if self.controller:
            self.controller.rollerCommand('-')

    def rollerRetract(self):
        if self.controller:
            self.controller.rollerCommand('r')

    def rollerDeploy(self):
        if self.controller:
            self.controller.rollerCommand('d')

    def setRetractPosition(self):
        if self.controller:
            self.controller.rollerCommand('R')

    def setDeployPosition(self):
        if self.controller:
            self.controller.rollerCommand('D')

    def save(self):
        if self.controller:
            self.controller.printer.command("!write")
        self.close()

    def addButton(self, parent, label, function):
        button = QtGui.QPushButton(label) #string or icon
        self.connect(button, QtCore.SIGNAL("clicked()"), function)
        parent.addWidget(button)
        return button

    def createOptionWidget(self, parentLayout, optionName, defaultValue):
        # Create a Sub-Layout for this option
        #layout = QtGui.QHBoxLayout()

        # Make sure it's a string with str(...)
        optionLineEdit = QtGui.QLineEdit(str(defaultValue))
        parentLayout.addWidget(optionLineEdit)

        return optionLineEdit

    def addOptions(self, parentLayout, options):
        for optionName, defaultValue in options.items():
            layout = QtGui.QHBoxLayout()

            widget = self.createOptionWidget(layout, optionName, defaultValue)

            self.created[optionName] = widget

            parentLayout.addLayout(layout)
