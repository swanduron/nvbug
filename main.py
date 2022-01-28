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
        self.engine = create_engine('sqlite:///nvbug.db', echo=False)
        self.DBSession = sessionmaker(bind=self.engine)
        self.session = self.DBSession()

        self.pushButton_2.clicked.connect(self.page2)
        self.pushButton_3.clicked.connect(self.page3)

    def page2(self):
        self.tabWidget.setCurrentIndex(1)
        self.caseListProcessor()
    def page3(self):
        self.tabWidget.setCurrentIndex(2)
        self.rmaTreeProcessor()


    def eventFilter(self, a0: 'QObject', a1: 'QEvent') -> bool:
        if a0 is self.lineEdit_10:
            if self.lineEdit_10.isEnabled():
                if a1.type() == 2:
                    self.caseInputData()
        elif a0 is self.lineEdit_6:
            if self.lineEdit_6.isEnabled():
                if a1.type() == 2:
                    self.rmaInitDate()
        elif a0 is self.lineEdit_7:
            if self.lineEdit_7.isEnabled():
                if a1.type() == 2:
                    self.rmaETDDate()
        elif a0 is self.lineEdit_8:
            if self.lineEdit_8.isEnabled():
                if a1.type() == 2:
                    self.rmaSrvDate()
        return super(Casewindow, self).eventFilter(a0, a1)


    # CaseList operation
    def caseListProcessor(self):
        self.fillCaseList()
        self.listActionAttached()
        self.caseListAppearanceAdject()

    def caseListAppearanceAdject(self):
        self.pushButton_20.setDisabled(True)
        self.pushButton_22.setDisabled(True)
        self.pushButton_23.setDisabled(True)
        self.lineEdit_9.setDisabled(True)
        self.lineEdit_9.setInputMask('00000000')
        self.lineEdit_10.setDisabled(True)
        self.lineEdit_10.setInputMask('0000-00-00')

    def listActionAttached(self):
        self.listWidget.clicked.connect(self.fillCaseInfo)
        self.pushButton_21.clicked.connect(self.createBlankCaseTmpl)
        self.pushButton_20.clicked.connect(self.saveCaseDescChanges)
        self.pushButton_22.clicked.connect(self.addNewCase)
        self.lineEdit_10.installEventFilter(self)


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

    def caseInputData(self):
        dialogBox = dateSelector()
        dialogBox.exec()
        selectedDate = dialogBox.getDate().toPyDate()
        if dialogBox.result():
            self.lineEdit_10.setText(str(selectedDate))

    # RMA operation


    def rmaTreeProcessor(self):
        self.fillTree()
        self.rmaActionAttached()
        self.rmaAppearanceAdjust()

    def rmaAppearanceAdjust(self):
        self.lineEdit_6.setInputMask('0000-00-00')
        self.lineEdit_7.setInputMask('0000-00-00')
        self.lineEdit_8.setInputMask('0000-00-00')
        self.pushButton_14.setDisabled(True)
        self.pushButton_15.setDisabled(True)
        self.pushButton_16.setDisabled(True)

    def rmaActionAttached(self):
        self.treeWidget_2.clicked.connect(self.fillRmainfo)
        self.lineEdit_6.installEventFilter(self)
        self.lineEdit_7.installEventFilter(self)
        self.lineEdit_8.installEventFilter(self)
        self.pushButton_18.clicked.connect(self.newARma)

    def fillTree(self):
        res = self.session.query(Case.case_id).all()
        case_id_list = [i[0] for i in res]
        self.treeWidget_2.clear()
        for case_id in case_id_list:
            root = QTreeWidgetItem(self.treeWidget_2)
            root.setText(0, case_id)
            parentCase = self.session.query(Case).filter_by(case_id=case_id).one()
            for rmaInstance in parentCase.rmas:
                child = QTreeWidgetItem(root)
                child.setText(1, rmaInstance.rma_id)

    def fillRmainfo(self):
        currentItem = self.treeWidget_2.currentItem()
        # If selected item has no column 0
        if not currentItem.text(0):
            rma_id = currentItem.text(1)
            self.pushButton_14.setDisabled(False)
            self.pushButton_15.setDisabled(False)
            self.pushButton_16.setDisabled(False)
            self.pushButton_18.setDisabled(False)
            rmaInstance = self.session.query(Rma).filter_by(rma_id=rma_id).one()
            # in View tab
            self.rma_dbid = rmaInstance.id
            self.label_35.setText(rmaInstance.case.case_id)
            self.label_37.setText(rma_id)
            self.label_41.setText(rmaInstance.date)
            self.label_43.setText(rmaInstance.rmaETD)
            self.label_45.setText(rmaInstance.rmaSrvDate)
            self.checkBox.setChecked(rmaInstance.componentsSendFlag)
            self.checkBox_2.setChecked(rmaInstance.componentsRecvFlag)
            self.checkBox_3.setChecked(rmaInstance.rmaCompFlag)
            self.checkBox_4.setChecked(rmaInstance.rmaReturnFlag)
            # in edit view
            res = self.session.query(Case.case_id).all()
            case_id_list = [i[0] for i in res]
            self.comboBox_2.clear()
            self.comboBox_2.addItems(case_id_list)
            self.lineEdit_4.setText(rma_id)
            self.lineEdit_6.setText(rmaInstance.date)
            self.lineEdit_7.setText(rmaInstance.rmaETD)
            self.lineEdit_8.setText(rmaInstance.rmaSrvDate)
            self.checkBox_5.setChecked(rmaInstance.componentsSendFlag)
            self.checkBox_7.setChecked(rmaInstance.componentsRecvFlag)
            self.checkBox_8.setChecked(rmaInstance.rmaCompFlag)
            self.checkBox_6.setChecked(rmaInstance.rmaReturnFlag)
        else:
            # Clicked a case instead of RMA
            self.pushButton_14.setDisabled(True)
            self.pushButton_15.setDisabled(True)
            self.pushButton_16.setDisabled(True)
            self.pushButton_18.setDisabled(False)
            self.label_35.setText('')
            self.label_37.setText('')
            self.label_41.setText('')
            self.label_43.setText('')
            self.label_45.setText('')
            self.checkBox.setChecked(False)
            self.checkBox_2.setChecked(False)
            self.checkBox_3.setChecked(False)
            self.checkBox_4.setChecked(False)

            self.comboBox_2.clear()
            self.lineEdit_4.setText('')
            self.lineEdit_6.setText('')
            self.lineEdit_7.setText('')
            self.lineEdit_8.setText('')
            self.checkBox_5.setChecked(False)
            self.checkBox_7.setChecked(False)
            self.checkBox_8.setChecked(False)
            self.checkBox_6.setChecked(False)

    def rmaInitDate(self):
        dialogBox = dateSelector()
        dialogBox.exec()
        selectedDate = dialogBox.getDate().toPyDate()
        if dialogBox.result():
            self.lineEdit_6.setText(str(selectedDate))

    def rmaETDDate(self):
        dialogBox = dateSelector()
        dialogBox.exec()
        selectedDate = dialogBox.getDate().toPyDate()
        if dialogBox.result():
            self.lineEdit_7.setText(str(selectedDate))

    def rmaSrvDate(self):
        dialogBox = dateSelector()
        dialogBox.exec()
        selectedDate = dialogBox.getDate().toPyDate()
        if dialogBox.result():
            self.lineEdit_8.setText(str(selectedDate))

    def newARma(self):
        self.pushButton_15.setDisabled(False)
        self.pushButton_14.setDisabled(True)
        self.pushButton_16.setDisabled(True)
        res = self.session.query(Case.case_id).all()
        case_id_list = [i[0] for i in res]
        self.comboBox_2.clear()
        self.comboBox_2.addItems(case_id_list)
        currentDay = str(QDate.currentDate().toPyDate())
        self.lineEdit_4.setText('')
        self.lineEdit_6.setText(currentDay)
        self.lineEdit_7.setText('')
        self.lineEdit_8.setText('')
        self.checkBox_5.setChecked(False)
        self.checkBox_7.setChecked(False)
        self.checkBox_8.setChecked(False)
        self.checkBox_6.setChecked(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Casewindow()
    window.show()
    sys.exit(app.exec())
