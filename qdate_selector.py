from PyQt6.QtWidgets import *
import sys

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

    def __init__(self):
        super(textSelector, self).__init__()
        self.setupUi()

    def setupUi(self):
        self.resize(400, 300)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textBox = QPlainTextEdit(self)
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = dateSelector()
    window.show()
    sys.exit(app.exec())