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
        self.pushButton_4.clicked.connect(self.page4)

    def page2(self):
        self.tabWidget.setCurrentIndex(1)
        self.caseListProcessor()
    def page3(self):
        self.tabWidget.setCurrentIndex(2)
        self.rmaTreeProcessor()
    def page4(self):
        self.tabWidget.setCurrentIndex(3)
        self.supporterProcessor()


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
            return
        elif not addDate or not case_id:
            QMessageBox.warning(self, 'Warning', 'Not all of fields were filled, please check it!',
                                buttons=QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Ok)
            return
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
        self.pushButton_18.clicked.connect(self.createBlankRma)
        self.pushButton_15.clicked.connect(self.saveNewRma)
        self.pushButton_14.clicked.connect(self.updateRma)

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
        self.comboBox_2.setDisabled(True)
        currentItem = self.treeWidget_2.currentItem()
        # If selected item has no column 0
        if not currentItem.text(0):
            rma_id = currentItem.text(1)
            self.pushButton_14.setDisabled(False)
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

    def createBlankRma(self):
        self.comboBox_2.setDisabled(False)
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

    def saveNewRma(self):
        rma_id = self.lineEdit_4.text()
        rmaDup = self.session.query(Rma).filter_by(rma_id=rma_id).all()
        if rmaDup:
            res = QMessageBox.warning(self, 'Duplicate RMA ID', 'You input RMA ID is duplicated!',
                                      buttons=QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Ok)
            return
        if not rma_id:
            QMessageBox.warning(self, 'Insufficient Information', 'RMA ID is mandatory Field!')
            return
        initDate = self.lineEdit_6.text()
        rmaETD = self.lineEdit_7.text()
        rmaSrvDate = self.lineEdit_8.text()
        componentSend =self.checkBox_5.isChecked()
        componentRecv = self.checkBox_7.isChecked()
        rmaComp = self.checkBox_8.isChecked()
        rmaReturn = self.checkBox_6.isChecked()
        parentCaseID = self.comboBox_2.currentText()
        rma = Rma(rma_id=rma_id, date=initDate, rmaETD=rmaETD, rmaSrvDate=rmaSrvDate,
                  componentsSendFlag=componentSend, componentsRecvFlag=componentRecv,
                  rmaCompFlag=rmaComp, rmaReturnFlag=rmaReturn)
        parentCase = self.session.query(Case).filter_by(case_id=parentCaseID).one()
        parentCase.rmas.append(rma)
        self.session.commit()
        self.fillTree()

    def updateRma(self):
        # This function is used to update a rma information
        rma_id = self.lineEdit_4.text()
        initDate = self.lineEdit_6.text()
        rmaETD = self.lineEdit_7.text()
        rmaSrvDate = self.lineEdit_8.text()
        componentSend = self.checkBox_5.isChecked()
        componentRecv = self.checkBox_7.isChecked()
        rmaComp = self.checkBox_8.isChecked()
        rmaReturn = self.checkBox_6.isChecked()

        res = QMessageBox.warning(self, 'Warning', 'The contents of RMA will be override!',
                                  buttons=QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Ok)
        if res == QMessageBox.StandardButton.Cancel:
            return

        self.session.query(Rma).filter_by(rma_id=rma_id).update({
            "date": initDate, "rmaETD": rmaETD, "rmaSrvDate": rmaSrvDate, "componentsSendFlag": componentSend,
            "componentsRecvFlag": componentRecv, "rmaCompFlag": rmaComp, "rmaReturnFlag": rmaReturn})
        self.session.commit()


    # Information collector
    # Service provider and Engineer
    def supporterProcessor(self):
        self.supporterActionAttached()
        self.supporterAppearanceAdjust()
        self.fillSupporterTree()

    def supporterAppearanceAdjust(self):
        self.pushButton_8.setDisabled(True)
        self.pushButton_9.setDisabled(True)
        self.pushButton_10.setDisabled(True)
        self.pushButton_11.setDisabled(True)
        self.pushButton_12.setDisabled(True)
        self.pushButton_13.setDisabled(True)

    def supporterActionAttached(self):
        self.pushButton_9.clicked.connect(self.addNewSupporter)
        self.pushButton_12.clicked.connect(self.addNewEngineer)
        self.treeWidget.clicked.connect(self.fillSupEngInfo)
        self.pushButton_19.clicked.connect(self.newSupporterTmpl)
        self.pushButton_24.clicked.connect(self.newEngineerTmpl)

    def fillSupporterTree(self):
        self.pushButton_9.setDisabled(True)
        self.pushButton_12.setDisabled(True)
        res = self.session.query(Supporter.name).all()
        supportNameList = [i[0] for i in res]
        self.treeWidget.clear()
        for supportName in supportNameList:
            root = QTreeWidgetItem(self.treeWidget)
            root.setText(0, supportName)
            supporter = self.session.query(Supporter).filter_by(name=supportName).one()
            for engineerInstance in supporter.engineers:
                child = QTreeWidgetItem(root)
                child.setText(1, engineerInstance.name)
                # Please pay attention that the type of setText function must be str
                child.setText(2, str(engineerInstance.id))
        self.comboBox.clear()
        nameList = self.session.query(Supporter.name).all()
        caseIdList = [i[0] for i in nameList]
        self.comboBox.addItems(caseIdList)

    def addNewSupporter(self):
        supporterName = self.lineEdit.text()
        currentDate = str(QDate.currentDate().toPyDate())
        description = self.plainTextEdit_2.toPlainText()
        if self.session.query(Supporter).filter_by(name=supporterName).all():
            QMessageBox.warning(self, 'Warning', 'The supporter name is duplicated!',
                                      buttons=QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Ok)
            return
        if not supporterName:
            QMessageBox.warning(self, 'Warning', 'Supporter name is mandatory field!')
            return
        supporter = Supporter(name=supporterName, date=currentDate, description=description)
        self.session.add(supporter)
        self.session.commit()
        self.fillSupporterTree()
        self.lineEdit.setText('')
        self.plainTextEdit_2.setPlainText('')

    def addNewEngineer(self):
        engineerName = self.lineEdit_2.text()
        supporterName = self.comboBox.currentText()
        currentDate = str(QDate.currentDate().toPyDate())
        description = self.plainTextEdit_3.toPlainText()
        if not engineerName:
            QMessageBox.warning(self, 'Warning', 'Engineer name is mandatory field!')
        parentSupporter = self.session.query(Supporter).filter_by(name=supporterName).one()
        engineer = Engineer(name=engineerName, date=currentDate, description=description)
        parentSupporter.engineers.append(engineer)
        self.session.commit()
        self.fillSupporterTree()
        self.lineEdit_2.setText('')
        self.plainTextEdit_3.setPlainText('')

    def fillSupEngInfo(self):
        self.pushButton_9.setDisabled(True)
        self.pushButton_12.setDisabled(True)
        currentItem = self.treeWidget.currentItem()
        if currentItem.text(0):
            # Supporter
            self.pushButton_8.setDisabled(False)
            self.pushButton_10.setDisabled(False)
            self.pushButton_9.setDisabled(True)
            self.pushButton_11.setDisabled(True)
            self.pushButton_12.setDisabled(True)
            self.pushButton_13.setDisabled(True)
            supporterInstance = self.session.query(Supporter).filter_by(name=currentItem.text(0)).one()
            self.lineEdit.setText(supporterInstance.name)
            self.label_26.setText(supporterInstance.date)
            self.plainTextEdit_2.setPlainText(supporterInstance.description)
        else:
            # Engineer
            self.pushButton_11.setDisabled(False)
            self.pushButton_13.setDisabled(False)
            self.pushButton_8.setDisabled(True)
            self.pushButton_10.setDisabled(True)
            self.pushButton_9.setDisabled(True)
            self.pushButton_12.setDisabled(True)
            engineerInstance = self.session.query(Engineer).filter_by(id=int(currentItem.text(2))).one()
            self.lineEdit_2.setText(engineerInstance.name)
            self.label_31.setText(engineerInstance.date)
            self.plainTextEdit_3.setPlainText(engineerInstance.description)
            self.comboBox.setCurrentText(engineerInstance.supporter.name)

    def newSupporterTmpl(self):
        self.pushButton_9.setDisabled(False)
        self.pushButton_8.setDisabled(True)
        self.pushButton_10.setDisabled(True)
        self.lineEdit.setText('')
        self.label_26.setText('')
        self.plainTextEdit_2.setPlainText('')

    def newEngineerTmpl(self):
        self.pushButton_12.setDisabled(False)
        self.pushButton_11.setDisabled(True)
        self.pushButton_13.setDisabled(True)
        self.lineEdit_2.setText('')
        self.label_31.setText('')
        self.plainTextEdit_3.setPlainText('')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Casewindow()
    window.show()
    sys.exit(app.exec())
