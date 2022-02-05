from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys
from dbmodel import *

class serviceSelector(QDialog):

    def __init__(self, dbcursor, rmaID, parent=None):
        super().__init__(parent)
        self.dbcursor = dbcursor
        self.rmaID = rmaID
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle('Service Selector')
        self.resize(450, 600)
        self.labelEngineer = QLabel('Engineer Selector:', self)
        self.labelContact = QLabel('Contact Selector:', self)
        self.treeViewEngineer = QTreeWidget(self)
        # select mode
        self.treeViewEngineer.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.treeViewEngineer.headerItem().setText(0, 'Supporter')
        self.treeViewEngineer.headerItem().setText(1, 'Engineer')
        self.treeViewEngineer.headerItem().setText(2, 'ID')
        self.treeViewContact = QTreeWidget(self)
        self.treeViewContact.headerItem().setText(0, 'Customer')
        self.treeViewContact.headerItem().setText(1, 'Contact')
        self.treeViewContact.headerItem().setText(2, 'ID')
        self.treeViewContact.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        vbox = QVBoxLayout()
        vbox.addWidget(self.labelEngineer)
        vbox.addWidget(self.treeViewEngineer)
        vbox.addWidget(self.labelContact)
        vbox.addWidget(self.treeViewContact)
        vbox.addWidget(self.buttonBox)
        self.setLayout(vbox)

        self.dataRender(self.dbcursor, self.rmaID)

    def dataRender(self, dbcursor, rmaID):
        rmaInstance = dbcursor.query(Rma).filter_by(rma_id=rmaID).one()
        engineerIDList = [i.id for i in rmaInstance.engineers]
        contactIDList = [i.id for i in rmaInstance.contacts]
        customerList = dbcursor.query(Customer).all()
        self.treeViewContact.clear()
        for customer in customerList:
            root = QTreeWidgetItem(self.treeViewContact)
            root.setText(0, customer.name)
            root.setText(2, str(customer.id))
            for contact in customer.contacts:
                child = QTreeWidgetItem(root)
                child.setText(1, contact.name)
                child.setText(2, str(contact.id))
                if contact.id in contactIDList:
                    child.setSelected(True)

        supporterList = dbcursor.query(Supporter).all()
        self.treeViewEngineer.clear()
        for supporter in supporterList:
            root = QTreeWidgetItem(self.treeViewEngineer)
            root.setText(0, supporter.name)
            root.setText(2, str(supporter.id))
            for engineer in supporter.engineers:
                child = QTreeWidgetItem(root)
                child.setText(1, engineer.name)
                child.setText(2, str(engineer.id))
                if engineer.id in engineerIDList:
                    child.setSelected(True)
        self.treeViewContact.expandAll()
        self.treeViewEngineer.expandAll()

    def scanResult(self):
        # Return a list of QTreeWidgetItem
        engTreeViewResult = [i for i in self.treeViewEngineer.selectedItems() if i.text(1)]
        conTreeViewResult = [i for i in self.treeViewContact.selectedItems() if i.text(1)]
        return engTreeViewResult, conTreeViewResult


