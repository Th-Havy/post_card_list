from PySide2 import QtCore
from PySide2.QtCore import Qt
import pandas as pd


class RecipientModel():

    MODEL_FIELDS = ["firstName", "lastName", "address", "city", "zipCode"]
    MODEL_FIELDS_BYTE_LITERALS = [bytes(f, encoding="UTF-8")
                                  for f in MODEL_FIELDS]

    def __init__(self, firstName="", lastName="",
                 address="", city="", zipCode=""):
        self.firstName = firstName
        self.lastName = lastName
        self.address = address
        self.city = city
        self.zipCode = zipCode

    def toList(self):
        return [self.firstName, self.lastName,
                self.address, self.city, self.zipCode]


class RecipientListModel(QtCore.QAbstractListModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.recipientList = []

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.recipientList)

    def data(self, index, role):
        """Return the recipient data at the specified index."""
        if index.row() >= self.rowCount() or not index.isValid():
            return None

        if role in self.roleNames():
            roleName = self.roleNames()[role]
            element = self.postCardList[index.row()]

            if roleName == b"firstName":
                return element.firstName
            elif roleName == b"lastName":
                return element.lastName
            elif roleName == b"address":
                return element.address
            elif roleName == b"city":
                return element.city
            elif roleName == b"zipCode":
                return element.zipCode
        else:
            return None

    def headerData(self, section, orientation, role):
        """Return the header data."""
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            return RecipientModel.MODEL_FIELDS[section]
        else:
            return "{}".format(section)

    def roleNames(self):
        return {id: role for id, role in
                enumerate(RecipientModel.MODEL_FIELDS_BYTE_LITERALS,
                          start=Qt.UserRole)}

    def toCsvFile(self, filepath):
        """Save the recipient list to a csv File."""
        df = pd.DataFrame([r.toList() for r in self.recipientList],
                          columns=RecipientModel.MODEL_FIELDS)
        df.to_csv(filepath)

    @staticmethod
    def fromFile(filepath):
        """Create a recipient list from a csv file."""
        df = pd.read_csv(filepath)

        assert df.shape[1] == len(RecipientModel.MODEL_FIELDS) + 1, \
               "Wrong number of columns in contact data."

        # Remove duplicate names
        df.drop_duplicates(subset=["firstName", "lastName"],
                           inplace=True, ignore_index=True)

        contactList = df.values.tolist()

        listModel = RecipientListModel()
        listModel.recipientList = []

        for contact in contactList:
            listModel.recipientList.append(RecipientModel(*contact[1:]))

        return listModel
