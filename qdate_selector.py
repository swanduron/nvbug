from PyQt6.QtWidgets import *
import sys
from utils import *

class dateSelector(QDialog):

    def __init__(self):
        super(dateSelector, self).__init__()
        self.setupUi()

    def setupUi(self):
        self.resize(400, 300)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.calendarWidget = QCalendarWidget(self)
        self.calendarWidget.setObjectName("calendarWidget")
        self.verticalLayout.addWidget(self.calendarWidget)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def getDate(self):
        return self.calendarWidget.selectedDate()

class textSelector(QDialog):

    def __init__(self, rmaInstance):
        super(textSelector, self).__init__()
        self.rmaInstance = rmaInstance
        self.resize(600, 500)
        self.setupUi()

    def setupUi(self):
        self.resize(400, 300)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        displayMessage = ''
        self.showtextBox = QPlainTextEdit(self)
        logMessages = self.rmaInstance.logs
        for log in logMessages:
            displayMessage += f'\n----------{log.date}-----------\n' \
                              f'{log.content}\n'
        self.showtextBox.setPlainText(displayMessage)
        self.textBox = QPlainTextEdit(self)
        self.verticalLayout.addWidget(self.showtextBox)
        self.verticalLayout.addWidget(self.textBox)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def getText(self):
        return self.textBox.toPlainText()

class pickupWindow(QDialog):

    def __init__(self, info):
        super(pickupWindow, self).__init__()
        self.setWindowTitle('Pick up information template')
        infoBox = QPlainTextEdit()
        infoBox.setPlainText(info)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok)
        vbox = QVBoxLayout()
        vbox.addWidget(infoBox)
        vbox.addWidget(self.buttonBox)
        self.setLayout(vbox)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

class pcieAddressFinder(QWidget):
    
    def __init__(self):
        super(pcieAddressFinder, self).__init__()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = dateSelector()
    window.show()
    sys.exit(app.exec())