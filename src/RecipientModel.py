import copy
from PySide2 import QtCore
from PySide2.QtCore import Qt
import pandas as pd
from postcard_creator import postcard_creator


class RecipientModel():
    """Class representing a recipient of a postcard."""

    def __init__(self, firstName="", lastName="",
                 address="", city="", zipCode=""):
        self.firstName = firstName
        self.lastName = lastName
        self.address = address
        self.city = city
        self.zipCode = zipCode

    def toList(self):
        """Return the fields in a list"""
        return [self.firstName, self.lastName,
                self.address, self.city, self.zipCode]

    def toPostCardCreatorRecipient(self):
        """Return the recipient as a postcard_creator Recipient object."""
        return postcard_creator.Recipient(prename=self.firstName, lastname=self.lastName,
                            street=self.address, place=self.city, zip_code=self.zipcode)


class RecipientListModel(QtCore.QAbstractListModel):
    """Class representing a list of recipients."""

    MODEL_FIELDS = ["firstName", "lastName", "address", "city", "zipCode"]

    FIRST_NAME_ROLE = Qt.UserRole + 1
    LAST_NAME_ROLE = Qt.UserRole + 2
    ADDRESS_ROLE = Qt.UserRole + 3
    CITY_ROLE = Qt.UserRole + 4
    ZIP_CODE_ROLE = Qt.UserRole + 5

    # Only for the comboboxes
    DISPLAY_NAME_ROLE = Qt.UserRole + 6

    ROLE_NAMES = {
        FIRST_NAME_ROLE: b"firstName",
        LAST_NAME_ROLE: b"lastName",
        ADDRESS_ROLE: b"address",
        CITY_ROLE: b"city",
        ZIP_CODE_ROLE: b"zipCode",
        DISPLAY_NAME_ROLE: b"displayName"
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.recipientList = []

    def rowCount(self, parent=QtCore.QModelIndex()):
        """Return the number of elements in the list."""
        return len(self.recipientList)

    def flags(self, index):
        """Return the flags of the items."""
        if index.row() >= self.rowCount() or not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def data(self, index, role):
        """Return the recipient data at the specified index."""
        if index.row() >= self.rowCount() or not index.isValid():
            return None

        if role in self.roleNames():
            element = self.recipientList[index.row()]

            if role == self.FIRST_NAME_ROLE:
                return element.firstName
            elif role == self.LAST_NAME_ROLE:
                return element.lastName
            elif role == self.ADDRESS_ROLE:
                return element.address
            elif role == self.CITY_ROLE:
                return element.city
            elif role == self.ZIP_CODE_ROLE:
                return element.zipCode
            elif role == self.DISPLAY_NAME_ROLE:
                if index.row() == 0:
                    return "Myself"
                else:
                    return element.firstName + " " + element.lastName

        return None

    def setData(self, index, value, role):
        """Set the recipient data (with given role) at the specified index."""
        if index.row() >= self.rowCount() or not index.isValid():
            return False

        if role in self.roleNames():
            element = copy.copy(self.recipientList[index.row()])

            # TODO: check if values are valid
            if role == self.FIRST_NAME_ROLE:
                element.firstName = value
            elif role == self.LAST_NAME_ROLE:
                element.lastName = value
            elif role == self.ADDRESS_ROLE:
                element.address = value
            elif role == self.CITY_ROLE:
                element.city = value
            elif role == self.ZIP_CODE_ROLE:
                element.zipCode = value
            else:
                return False

            self.recipientList[index.row()] = element
            self.dataChanged.emit(index, index, [role, "self.DISPLAY_NAME_ROLE"])

            return True
        else:
            return False

    def roleNames(self):
        """Return the role names for Qt."""
        return self.ROLE_NAMES

    @QtCore.Slot(result=int)
    def firstNameRole(self):
        """Return the first name role."""
        return self.FIRST_NAME_ROLE

    @QtCore.Slot(result=int)
    def lastNameRole(self):
        """Return the last name role."""
        return self.LAST_NAME_ROLE

    @QtCore.Slot(result=int)
    def addressRole(self):
        """Return the address role."""
        return self.ADDRESS_ROLE

    @QtCore.Slot(result=int)
    def cityRole(self):
        """Return the city role."""
        return self.CITY_ROLE

    @QtCore.Slot(result=int)
    def zipCodeRole(self):
        """Return the zip code role."""
        return self.ZIP_CODE_ROLE

    @QtCore.Slot(result=int)
    def displayNameRole(self):
        """Return the display name role."""
        return self.DISPLAY_NAME_ROLE

    def removeRows(self, row, count, parent=QtCore.QModelIndex()):
        """Remove rows from the list."""

        if row < 0 or count < 0 or (row + count) > self.rowCount():
            return False

        self.beginRemoveRows(parent, row, row + count - 1)
        del self.recipientList[row:(row + count)]
        self.endRemoveRows()

        return True

    @QtCore.Slot(int)
    def removeRecipient(self, index):
        """Remove a recipient from the list."""
        self.removeRows(index, 1)

    @QtCore.Slot(str, str, str, str, int)
    def appendRecipient(self, firstName, lastName, address, city, zipCode):
        """Append a recipient to the list."""
        self.beginInsertRows(QtCore.QModelIndex(),
                             self.rowCount(),
                             self.rowCount())

        recipient = RecipientModel(firstName, lastName, address, city, zipCode)
        self.recipientList.append(recipient)
        self.endInsertRows()

    def toCsvFile(self, filepath):
        """Save the recipient list to a csv File."""
        df = pd.DataFrame([r.toList() for r in self.recipientList],
                          columns=self.MODEL_FIELDS)
        df.to_csv(filepath)

    @classmethod
    def fromFile(cls, filepath):
        """Create a recipient list from a csv file."""
        df = pd.read_csv(filepath)

        assert df.shape[1] == len(cls.MODEL_FIELDS) + 1, \
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
