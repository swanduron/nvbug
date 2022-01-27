from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from main_ui import *
import sys
from sqlalchemy import *
from sqlalchemy.orm import *
from dbmodel import *
from qdate_selector import *


class Casewindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(Casewindow, self).__init__()
        self.setupUi(self)
        self.appearanceAdjest()
        self.engine = create_engine('sqlite:///nvbug.db', echo=False)
        self.DBSession = sessionmaker(bind=self.engine)
        self.session = self.DBSession()
        self.caseListProcessor()


    def appearanceAdjest(self):
        # self.tabWidget.tabBar().setVisible(False)
        pass

    # CaseList operation
    def caseListProcessor(self):
        self.fillCaseList()
        self.listActionAttached()
        self.caseListAppearanceAdject()

    def caseListAppearanceAdject(self):
        self.pushButton_20.setDisabled(True)
        self.pushButton_21.setDisabled(True)
        self.pushButton_22.setDisabled(True)
        self.pushButton_23.setDisabled(True)
        self.lineEdit_9.setDisabled(True)
        self.lineEdit_10.setDisabled(True)
        self.lineEdit_10.setInputMask('0000-00-00')

    def listActionAttached(self):
        self.listWidget.clicked.connect(self.fillCaseInfo)
        self.pushButton_21.clicked.connect(self.createBlankCaseTmpl)
        self.pushButton_20.clicked.connect(self.saveCaseDescChanges)
        self.pushButton_22.clicked.connect(self.addNewCase)
        self.pushButton_5.clicked.connect(self.inputData)


    def fillCaseList(self):
        res = self.session.query(Case.case_id).all()
        filling_list = [i[0] for i in res]
        self.listWidget.addItems(filling_list)

    def fillCaseInfo(self, event):
        case_id = event.data()
        case = self.session.query(Case).filter_by(case_id=case_id).one()
        self.label_55.setText(case.case_id)
        self.label_59.setText(case.date)
        self.plainTextEdit_6.setPlainText(case.description)
        self.lineEdit_9.setText(case.case_id)
        self.lineEdit_9.setDisabled(True)
        self.lineEdit_10.setText(case.date)
        self.lineEdit_10.setDisabled(True)
        self.plainTextEdit_7.setPlainText(case.description)
        self.pushButton_20.setDisabled(False)
        self.pushButton_23.setDisabled(False)
        self.pushButton_21.setDisabled(False)
        self.pushButton_22.setDisabled(False)

    def createBlankCaseTmpl(self):
        self.pushButton_20.setDisabled(True)
        self.pushButton_23.setDisabled(True)
        self.lineEdit_9.setDisabled(False)
        self.lineEdit_9.setText('')
        self.lineEdit_10.setDisabled(False)
        self.lineEdit_10.setText('')
        self.plainTextEdit_7.setPlainText('')

    def saveCaseDescChanges(self):

        case_id = self.listWidget.currentItem().text()
        case = self.session.query(Case).filter_by(case_id=case_id).one()
        currentCaseDesc = self.plainTextEdit_7.toPlainText()
        if currentCaseDesc != case.description:
            res = QMessageBox.warning(self, 'Warning', 'The description of case will be override!',
                                      buttons=QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Ok)
            if res == QMessageBox.StandardButton.Cancel:
                return
            self.session.query(Case).filter_by(case_id=case_id).update({"description": currentCaseDesc})
            self.session.commit()

    def addNewCase(self):
        pass

    def inputData(self):
        dialogBox = dateSelector()
        dialogBox.exec()
        selectedDate = dialogBox.getDate().toPyDate()
        if dialogBox.result():
            self.lineEdit_10.setText(str(selectedDate))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Casewindow()
    window.show()
    sys.exit(app.exec())
