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
        # self.pushButton_21.setDisabled(False)
        self.pushButton_22.setDisabled(True)
        self.pushButton_23.setDisabled(True)
        self.lineEdit_9.setDisabled(True)
        self.lineEdit_9.setInputMask('00000000')
        self.lineEdit_10.setDisabled(True)
        self.lineEdit_10.setInputMask('0000-00-00')
        self.pushButton_5.setDisabled(True)

    def listActionAttached(self):
        self.listWidget.clicked.connect(self.fillCaseInfo)
        self.pushButton_21.clicked.connect(self.createBlankCaseTmpl)
        self.pushButton_20.clicked.connect(self.saveCaseDescChanges)
        self.pushButton_22.clicked.connect(self.addNewCase)
        self.pushButton_5.clicked.connect(self.inputData)
        self.lineEdit_10.installEventFilter(self)
    # below is a eventFilter to add additional action when the lineEdit is pushed
    def eventFilter(self, a0: 'QObject', a1: 'QEvent') -> bool:
        if a0 is self.lineEdit_10:
            if self.lineEdit_10.isEnabled():
                if a1.type() == 2:
                    self.inputData()
        return super(Casewindow, self).eventFilter(a0, a1)
    

    def fillCaseList(self):
        res = self.session.query(Case.case_id).all()
        filling_list = [i[0] for i in res]
        self.listWidget.clear()
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


    def createBlankCaseTmpl(self):
        self.pushButton_20.setDisabled(True)
        self.pushButton_23.setDisabled(True)
        self.pushButton_22.setDisabled(False)
        self.pushButton_5.setDisabled(False)
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
        addDate = self.lineEdit_10.text()
        case_id = self.lineEdit_9.text()
        description = self.plainTextEdit_7.toPlainText()
        if self.session.query(Case).filter_by(case_id=case_id).all():
            QMessageBox.warning(self, 'Warning', 'The Case ID is duplicated, please check it!',
                                buttons=QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Ok)
        elif not addDate or not case_id:
            QMessageBox.warning(self, 'Warning', 'Not all of fields were filled, please check it!',
                                buttons=QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Ok)
        else:
            case = Case(case_id=case_id, date=addDate, description=description)
            self.session.add(case)
            self.session.commit()
            self.fillCaseList()
            self.caseListAppearanceAdject()

    def inputData(self):
        dialogBox = dateSelector()
        dialogBox.exec()
        selectedDate = dialogBox.getDate().toPyDate()
        if dialogBox.result():
            self.lineEdit_10.setText(str(selectedDate))

    # RMA operation


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Casewindow()
    window.show()
    sys.exit(app.exec())
