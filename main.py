from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from main_ui import *
import sys
from sqlalchemy import *
from sqlalchemy.orm import *
from dbmodel import *
from qdate_selector import *
from service_selector import *
from utils import *


class Casewindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(Casewindow, self).__init__()
        self.setupUi(self)
        self.engine = create_engine('sqlite:///nvbug.db', echo=False)
        self.DBSession = sessionmaker(bind=self.engine)
        self.session = self.DBSession()
        self.pushButton.clicked.connect(self.page1)
        self.pushButton_2.clicked.connect(self.page2)
        self.pushButton_3.clicked.connect(self.page3)
        self.pushButton_4.clicked.connect(self.page4)
        self.tabWidget.tabBar().hide()
        self.page1()

    def page1(self):
        self.tabWidget.setCurrentIndex(0)

    def page2(self):
        self.tabWidget.setCurrentIndex(1)
        self.caseListProcessor()
    def page3(self):
        self.tabWidget.setCurrentIndex(2)
        self.rmaTreeProcessor()
    def page4(self):
        self.tabWidget.setCurrentIndex(3)
        self.supporterProcessor()
        self.customerProcessor()


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
        self.listWidget.itemSelectionChanged.connect(self.caseSelectChangedDetector)
        self.pushButton_21.clicked.connect(self.createBlankCaseTmpl)
        self.pushButton_20.clicked.connect(self.saveCaseDescChanges)
        self.pushButton_22.clicked.connect(self.addNewCase)
        self.lineEdit_10.installEventFilter(self)

    def caseSelectChangedDetector(self):
        # This function is used to track the keyboard operation of arrow up and down. Demo works in Win
        index = self.listWidget.currentIndex()
        item = self.listWidget.itemFromIndex(index)
        self.fillCaseInfo(index)
        # print(f'Item changed!, Current Item is {item.text()}')

    def fillCaseList(self):
        res = self.session.query(Case.case_id).order_by(desc(Case.date)).all()
        filling_list = [i[0] for i in res]
        self.listWidget.clear()
        self.listWidget.addItems(filling_list)

    def fillCaseInfo(self, index):
        case_id = index.data()
        case = self.session.query(Case).filter_by(case_id=case_id).one()
        self.tabWidget_5.setCurrentIndex(0)
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
        self.pushButton_7.setDisabled(True)
        self.pushButton_6.setDisabled(True)
        # change treeWidget colume width
        self.treeWidget_2.setColumnWidth(0, 150)

    def rmaActionAttached(self):
        self.treeWidget_2.clicked.connect(self.fillRmainfo)
        self.treeWidget_2.itemSelectionChanged.connect(self.rmaSelectChangedDetector)
        self.treeWidget_2.setAnimated(True)
        self.lineEdit_6.installEventFilter(self)
        self.lineEdit_7.installEventFilter(self)
        self.lineEdit_8.installEventFilter(self)
        self.pushButton_18.clicked.connect(self.createBlankRma)
        self.pushButton_15.clicked.connect(self.saveNewRma)
        self.pushButton_14.clicked.connect(self.updateRma)
        self.pushButton_6.clicked.connect(self.selectServiceInfo)
        self.pushButton_7.clicked.connect(self.showServiceInfo)

    def rmaSelectChangedDetector(self):
        # This function is used to track the keyboard operation of arrow up and down. Demo works in Win
        index = self.treeWidget_2.currentIndex()
        item = self.treeWidget_2.itemFromIndex(index)
        self.fillRmainfo(index)

    def selectServiceInfo(self):
        try:
            self.pushButton_6.clicked.disconnect()
        except:
            pass
        rmaID = self.label_37.text()
        dialogBox = serviceSelector(self.session, rmaID, self)
        dialogBox.exec()
        engineerInfo, contactInfo = dialogBox.scanResult()
        # Below function is used to assess whether the engineers and contacts records of DB need to be updated.
        engineerIDList = [int(i.text(2)) for i in engineerInfo]
        engineerIDList.sort()
        contactIDList = [int(i.text(2)) for i in contactInfo]
        contactIDList.sort()
        rmaInstance = self.session.query(Rma).filter_by(rma_id=rmaID).one()
        currentEngineerIDList = [i.id for i in rmaInstance.engineers]
        currentEngineerIDList.sort()
        currentContactIDList = [i.id for i in rmaInstance.contacts]
        currentContactIDList.sort()
        if dialogBox.result(): # if dialogBox click OK, OK returns 1, cancel returns 0
            if engineerIDList != currentEngineerIDList:
                rmaInstance.engineers.clear()
                for engineer in engineerInfo:
                    engineerInstance = self.session.query(Engineer).filter_by(id=int(engineer.text(2))).one()
                    rmaInstance.engineers.append(engineerInstance)
                # Need to add Logger here
            if contactIDList != currentContactIDList:
                rmaInstance.contacts.clear()
                for contact in contactInfo:
                    contactInstance = self.session.query(Contact).filter_by(id=int(contact.text(2))).one()
                    rmaInstance.contacts.append(contactInstance)
                # Need to add Logger here
            self.session.commit()
        ##demo code for index
        index = self.treeWidget_2.currentIndex()
        self.fillRmainfo(index)
        self.pushButton_6.clicked.connect(self.selectServiceInfo)

    def showServiceInfo(self):
        try:
            self.pushButton_7.clicked.disconnect()
        except:
            pass
        rmaID = self.label_37.text()
        dialogBox = serviceSelectorRO(self.session, rmaID, self)
        dialogBox.exec()
        self.pushButton_7.clicked.connect(self.showServiceInfo)


    def fillTree(self):
        res = self.session.query(Case.case_id).order_by(desc(Case.date)).all()
        case_id_list = [i[0] for i in res]
        self.treeWidget_2.clear()
        for case_id in case_id_list:
            root = QTreeWidgetItem(self.treeWidget_2)
            root.setText(0, case_id)
            parentCase = self.session.query(Case).filter_by(case_id=case_id).one()
            for rmaInstance in parentCase.rmas:
                child = QTreeWidgetItem(root)
                child.setText(1, rmaInstance.rma_id)
        self.treeWidget_2.expandAll()

    def fillRmainfo(self, index):
        self.comboBox_2.setDisabled(True)
        currentItem = self.treeWidget_2.itemFromIndex(index)
        # If selected item has no column 0
        if not currentItem.text(0):
            # RMA
            self.pushButton_7.setDisabled(False)
            self.pushButton_6.setDisabled(False)
            self.tabWidget_4.setCurrentIndex(0)
            rma_id = currentItem.text(1)
            self.pushButton_14.setDisabled(False)
            self.pushButton_16.setDisabled(False)
            self.pushButton_18.setDisabled(False)
            rmaInstance = self.session.query(Rma).filter_by(rma_id=rma_id).one()
            engineerInfo = engineerInfoGenerator(rmaInstance.engineers)
            contactInfo = contactInfoGenerator(rmaInstance.contacts)
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
            self.plainTextEdit.setPlainText(engineerInfo)
            self.plainTextEdit_2.setPlainText(contactInfo)
            # in edit/new tab
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
            self.plainTextEdit_4.setPlainText(engineerInfo)
            self.plainTextEdit_5.setPlainText(contactInfo)
        else:
            # Clicked a case instead of RMA
            self.pushButton_7.setDisabled(True)
            self.pushButton_6.setDisabled(True)
            self.tabWidget_4.setCurrentIndex(0)
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
            self.plainTextEdit.setPlainText('')
            self.plainTextEdit_2.setPlainText('')

            self.comboBox_2.clear()
            self.lineEdit_4.setText('')
            self.lineEdit_6.setText('')
            self.lineEdit_7.setText('')
            self.lineEdit_8.setText('')
            self.checkBox_5.setChecked(False)
            self.checkBox_7.setChecked(False)
            self.checkBox_8.setChecked(False)
            self.checkBox_6.setChecked(False)
            self.plainTextEdit_4.setPlainText('')
            self.plainTextEdit_5.setPlainText('')

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
        self.rmaAppearanceAdjust()

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
        self.treeWidget.setColumnWidth(0, 250)
        self.treeWidget.setColumnHidden(2, True)

    def supporterActionAttached(self):
        self.pushButton_9.clicked.connect(self.addNewSupporter)
        self.pushButton_12.clicked.connect(self.addNewEngineer)
        self.treeWidget.clicked.connect(self.fillSupEngInfo)
        self.treeWidget.itemSelectionChanged.connect(self.supporterSelectChangedDetector)
        self.pushButton_19.clicked.connect(self.newSupporterTmpl)
        self.pushButton_24.clicked.connect(self.newEngineerTmpl)
        self.pushButton_8.clicked.connect(self.updateSupporter)
        self.pushButton_11.clicked.connect(self.updateEngineer)

    def supporterSelectChangedDetector(self):
        # This function is used to track the keyboard operation of arrow up and down. Demo works in Win
        index = self.treeWidget.currentIndex()
        item = self.treeWidget.itemFromIndex(index)
        self.fillSupEngInfo(index)

    def fillSupporterTree(self):
        self.pushButton_9.setDisabled(True)
        self.pushButton_12.setDisabled(True)
        res = self.session.query(Supporter.name).all()
        supportNameList = [i[0] for i in res]
        self.treeWidget.clear()
        for supportName in supportNameList:
            root = QTreeWidgetItem(self.treeWidget)
            root.setText(0, supportName)
            supporterInstance = self.session.query(Supporter).filter_by(name=supportName).one()
            root.setText(2, str(supporterInstance.id))
            supporter = self.session.query(Supporter).filter_by(name=supportName).one()
            for engineerInstance in supporter.engineers:
                child = QTreeWidgetItem(root)
                child.setText(1, engineerInstance.name)
                # Below code is used to show the multiple checkbox for each line, it displays the checkbox but has no
                # affect of selection
                # child.setCheckState(1, Qt.CheckState.Unchecked)
                # Please pay attention that the type of setText function must be str
                child.setText(2, str(engineerInstance.id))
        self.comboBox.clear()
        nameList = self.session.query(Supporter.name).all()
        caseIdList = [i[0] for i in nameList]
        self.comboBox.addItems(caseIdList)
        self.treeWidget.expandAll()

    def addNewSupporter(self):
        supporterName = self.lineEdit.text()
        currentDate = str(QDate.currentDate().toPyDate())
        description = self.plainTextEdit_90.toPlainText()
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
        self.plainTextEdit_90.setPlainText('')
        self.supporterAppearanceAdjust()

    def addNewEngineer(self):
        engineerName = self.lineEdit_2.text()
        supporterName = self.comboBox.currentText()
        currentDate = str(QDate.currentDate().toPyDate())
        description = self.plainTextEdit_3.toPlainText()
        if not engineerName:
            QMessageBox.warning(self, 'Warning', 'Engineer name is mandatory field!')
            return
        parentSupporter = self.session.query(Supporter).filter_by(name=supporterName).one()
        engineer = Engineer(name=engineerName, date=currentDate, description=description)
        parentSupporter.engineers.append(engineer)
        self.session.commit()
        self.fillSupporterTree()
        self.lineEdit_2.setText('')
        self.plainTextEdit_3.setPlainText('')
        self.supporterAppearanceAdjust()

    def fillSupEngInfo(self, itemIndex):
        self.pushButton_9.setDisabled(True)
        self.pushButton_12.setDisabled(True)
        # Below is the simple for getting widget item from index. In this function, the itemIndex(QModelIndex) is
        # general fall-back parameter of signal when click the treewidget
        currentItem = self.treeWidget.itemFromIndex(itemIndex)
        if currentItem.text(0):
            # Supporter
            # Change current page to appropriate sub page
            self.tabWidget_3.setCurrentIndex(0)
            self.pushButton_8.setDisabled(False)
            self.pushButton_10.setDisabled(False)
            self.pushButton_9.setDisabled(True)
            self.pushButton_11.setDisabled(True)
            self.pushButton_12.setDisabled(True)
            self.pushButton_13.setDisabled(True)
            supporterInstance = self.session.query(Supporter).filter_by(name=currentItem.text(0)).one()
            self.lineEdit.setText(supporterInstance.name)
            self.label_26.setText(supporterInstance.date)
            self.plainTextEdit_90.setPlainText(supporterInstance.description)
        else:
            # Engineer
            self.tabWidget_3.setCurrentIndex(1)
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
        self.plainTextEdit_90.setPlainText('')

    def newEngineerTmpl(self):
        self.pushButton_12.setDisabled(False)
        self.pushButton_11.setDisabled(True)
        self.pushButton_13.setDisabled(True)
        self.lineEdit_2.setText('')
        self.label_31.setText('')
        self.plainTextEdit_3.setPlainText('')

    def updateEngineer(self):
        currentEngineer = self.treeWidget.currentItem()
        if currentEngineer.text(0):
            QMessageBox.warning(self, 'Warning', 'Cursor does not point to Engineer.\nPlease refresh data.')
            return
        engineerID = int(currentEngineer.text(2))
        engineerName = self.lineEdit_2.text()
        engineerDesc = self.plainTextEdit_3.toPlainText()
        res = QMessageBox.warning(self, 'Warning', 'The Engineer information is going to update, please confirm!',
                                  buttons=QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Ok)
        if res == QMessageBox.StandardButton.Cancel:
            return
        else:
            self.session.query(Engineer).filter_by(id=engineerID).update({
                "name": engineerName, "description": engineerDesc
            })
            self.session.commit()


    def updateSupporter(self):
        currentSupporter = self.treeWidget.currentItem()
        if currentSupporter.text(1):
            QMessageBox.warning(self, 'Warning', 'Cursor does not point to Supporter.\nPlease refresh data.')
            return
        supporterDesc = self.plainTextEdit_90.toPlainText()
        supporterName = self.lineEdit.text()
        supporterID = int(self.treeWidget.currentItem().text(2))
        res = QMessageBox.warning(self, 'Warning', 'The Supporter information is going to update, please confirm!',
                                  buttons=QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Ok)
        if res == QMessageBox.StandardButton.Cancel:
            return
        else:
            self.session.query(Supporter).filter_by(id=supporterID).update({
                "name": supporterName, "description": supporterDesc
            })
            self.session.commit()


    # Customer and Contacts
    def customerProcessor(self):
        self.customerActionAttached()
        self.customerAppearanceAdjust()
        self.fillCustomerTree()

    def customerAppearanceAdjust(self):
        self.pushButton_17.setDisabled(True)
        self.pushButton_26.setDisabled(True)
        self.pushButton_27.setDisabled(True)
        self.pushButton_28.setDisabled(True)
        self.pushButton_30.setDisabled(True)
        self.pushButton_31.setDisabled(True)
        self.treeWidget_3.setColumnWidth(0, 250)
        self.treeWidget_3.setColumnHidden(2, True)

    def customerActionAttached(self):
        self.pushButton_26.clicked.connect(self.addNewCustomer)
        self.pushButton_30.clicked.connect(self.addNewContact)
        self.treeWidget_3.clicked.connect(self.fillCusConInfo)
        self.treeWidget_3.itemSelectionChanged.connect(self.customerSelectChangedDetector)
        self.pushButton_25.clicked.connect(self.newCustomerTmpl)
        self.pushButton_29.clicked.connect(self.newContactTmpl)
        self.pushButton_17.clicked.connect(self.updateCustomer)
        self.pushButton_28.clicked.connect(self.updateContact)


    def customerSelectChangedDetector(self):
        # This function is used to track the keyboard operation of arrow up and down. Demo works in Win
        index = self.treeWidget_3.currentIndex()
        item = self.treeWidget_3.itemFromIndex(index)
        self.fillCusConInfo(index)

    def fillCustomerTree(self):
        self.pushButton_30.setDisabled(True)
        self.pushButton_26.setDisabled(True)
        customerList = self.session.query(Customer).all()
        self.treeWidget_3.clear()
        for customer in customerList:
            root = QTreeWidgetItem(self.treeWidget_3)
            root.setText(0, customer.name)
            root.setText(2, str(customer.id))
            for contact in customer.contacts:
                child = QTreeWidgetItem(root)
                child.setText(1, contact.name)
                child.setText(2, str(contact.id))
        self.comboBox_3.clear()
        customerNameList = [i.name for i in customerList]
        self.comboBox_3.addItems(customerNameList)
        self.treeWidget_3.expandAll()

    def addNewCustomer(self):
        customerName = self.lineEdit_3.text()
        currentDate = str(QDate.currentDate().toPyDate())
        description = self.plainTextEdit_91.toPlainText()
        if self.session.query(Customer).filter_by(name=customerName).all():
            QMessageBox.warning(self, 'Warning', 'The Customer name is duplicated!',
                                buttons=QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Ok)
            return
        if not customerName:
            QMessageBox.warning(self, 'Warning', 'Customer name is mandatory field!')
            return
        customer = Customer(name=customerName, date=currentDate, description=description)
        self.session.add(customer)
        self.session.commit()
        self.fillCustomerTree()
        self.lineEdit_3.setText('')
        self.plainTextEdit_91.setPlainText('')
        self.customerAppearanceAdjust()


    def addNewContact(self):
        contactName = self.lineEdit_5.text()
        customerName = self.comboBox_3.currentText()
        currentDate = str(QDate.currentDate().toPyDate())
        description = self.plainTextEdit_8.toPlainText()
        if not contactName:
            QMessageBox.warning(self, 'Warning', 'Contact name is mandatory field!')
            return
        parentCustomer = self.session.query(Customer).filter_by(name=customerName).one()
        contact = Contact(name=contactName, date=currentDate, description=description)
        parentCustomer.contacts.append(contact)
        self.session.commit()
        self.fillCustomerTree()
        self.lineEdit_5.setText('')
        self.plainTextEdit_3.setPlainText('')
        self.customerAppearanceAdjust()


    def fillCusConInfo(self, itemIndex):
        self.pushButton_30.setDisabled(True)
        self.pushButton_26.setDisabled(True)
        currentItem = self.treeWidget_3.itemFromIndex(itemIndex)
        if currentItem.text(0):
            # customer
            self.tabWidget_6.setCurrentIndex(0)
            self.pushButton_17.setDisabled(False)
            self.pushButton_27.setDisabled(False)
            self.pushButton_26.setDisabled(True)
            self.pushButton_28.setDisabled(True)
            self.pushButton_30.setDisabled(True)
            self.pushButton_31.setDisabled(True)
            customerInstance = self.session.query(Customer).filter_by(id=int(currentItem.text(2))).one()
            self.lineEdit_3.setText(customerInstance.name)
            self.label_67.setText(customerInstance.date)
            self.plainTextEdit_91.setPlainText(customerInstance.description)

        else:
            # contact
            self.tabWidget_6.setCurrentIndex(1)
            self.pushButton_28.setDisabled(False)
            self.pushButton_31.setDisabled(False)
            self.pushButton_17.setDisabled(True)
            self.pushButton_27.setDisabled(True)
            self.pushButton_30.setDisabled(True)
            self.pushButton_26.setDisabled(True)
            contactInstance = self.session.query(Contact).filter_by(id=int(currentItem.text(2))).one()
            self.lineEdit_5.setText(contactInstance.name)
            self.comboBox_3.setCurrentText(contactInstance.customer.name)
            self.label_72.setText(contactInstance.date)
            self.plainTextEdit_8.setPlainText(contactInstance.description)

    def newCustomerTmpl(self):
        self.pushButton_26.setDisabled(False)
        self.pushButton_17.setDisabled(True)
        self.pushButton_27.setDisabled(True)
        self.lineEdit_3.setText('')
        self.label_67.setText('')
        self.plainTextEdit_91.setPlainText('')

    def newContactTmpl(self):
        self.pushButton_30.setDisabled(False)
        self.pushButton_28.setDisabled(True)
        self.pushButton_31.setDisabled(True)
        self.lineEdit_5.setText('')
        self.label_72.setText('')
        self.plainTextEdit_8.setPlainText('')

    def updateCustomer(self):
        currentCustomer = self.treeWidget_3.currentItem()
        if not currentCustomer.text(0):
            QMessageBox.warning(self, 'Warning', 'Cursor does not point to Customer.\nPlease refresh data.')
            return
        customerID = int(currentCustomer.text(2))
        customerName = self.lineEdit_3.text()
        description = self.plainTextEdit_91.toPlainText()
        res = QMessageBox.warning(self, 'Warning', 'The Customer information is going to update, please confirm!',
                            buttons=QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Ok)
        if res == QMessageBox.StandardButton.Cancel:
            return
        else:
            self.session.query(Customer).filter_by(id=customerID).update({
                "name": customerName, "description": description
            })
            self.session.commit()


    def updateContact(self):
        currentContact = self.treeWidget_3.currentItem()
        if not currentContact.text(1):
            QMessageBox.warning(self, 'Warning', 'Cursor does not point to Contact.\nPlease refresh data.')
            return
        contactID = int(currentContact.text(2))
        contactName = self.lineEdit_5.text()
        description = self.plainTextEdit_8.toPlainText()
        res = QMessageBox.warning(self, 'Warning', 'The Contact information is going to update, please confirm!',
                                  buttons=QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Ok)
        if res == QMessageBox.StandardButton.Cancel:
            return
        else:
            self.session.query(Contact).filter_by(id=contactID).update({
                "name": contactName, "description": description
            })
            self.session.commit()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Casewindow()
    window.show()
    sys.exit(app.exec())
