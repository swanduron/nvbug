from PyQt6.QtWidgets import *
import sys
from utils import *
import io, re

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

class pcieAddressFinder(QDialog):
    
    def __init__(self):
        super(pcieAddressFinder, self).__init__()
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle('PCIe Address Finder for DGXA100')
        vbox = QVBoxLayout()
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok)
        self.inputBox = QLineEdit()
        self.inputBox.textChanged.connect(self.dataFill)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.pcieInfoList = QListWidget()

        vbox.addWidget(self.inputBox)
        vbox.addWidget(self.pcieInfoList)
        vbox.addWidget(self.buttonBox)
        self.setLayout(vbox)
        self.dataFill()

    def dataFill(self, event=None):
        print(event)
        # io.StringIO is used to roll a string back to a file IO that gives many functions such as readlines
        infoData = [i.strip() for i in io.StringIO(pcieTree).readlines()]
        if event:
            infoData = [i for i in infoData if re.findall(event, i, re.I)]
        self.pcieInfoList.clear()
        self.pcieInfoList.addItems(infoData)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = pcieAddressFinder()
    window.show()
    sys.exit(app.exec())