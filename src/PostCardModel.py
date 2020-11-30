import os
import copy
from PySide2 import QtCore
from PySide2.QtCore import Qt
import pandas as pd


class PostCardModel():
    """Class representing a postcard."""

    def __init__(self, photo="", backText="", recipient=""):
        self.photo = photo
        self.backText = backText
        self.recipient = recipient

    def toList(self):
        return [self.photo, self.backText, self.recipient]


class PostCardListModel(QtCore.QAbstractListModel):
    """Class representing a list of postcards."""

    MODEL_FIELDS = ["photo", "backText", "recipient"]

    PHOTO_ROLE = Qt.UserRole + 1
    BACK_TEXT_ROLE = Qt.UserRole + 2
    RECIPIENT_ROLE = Qt.UserRole + 3

    ROLE_NAMES = {
        PHOTO_ROLE: b"photo",
        BACK_TEXT_ROLE: b"backText",
        RECIPIENT_ROLE: b"recipient"
    }

    # Modification of the list can only be done in the GUI thread,
    # hence a signal mirrors the removePostCard() method
    requestRemovePostCard = QtCore.Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.postCardList = []

        self.requestRemovePostCard.connect(self.removePostCard)

    def rowCount(self, parent=QtCore.QModelIndex()):
        """Return the number of elements in the list."""
        return len(self.postCardList)

    def flags(self, index):
        """Return the flags of the items."""
        if index.row() >= self.rowCount() or not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def data(self, index, role):
        """Return the card data (with given role) at the specified index."""
        if index.row() >= self.rowCount() or not index.isValid():
            return None

        if role in self.roleNames():
            element = self.postCardList[index.row()]

            if role == self.PHOTO_ROLE:
                return element.photo
            elif role == self.BACK_TEXT_ROLE:
                return element.backText
            elif role == self.RECIPIENT_ROLE:
                return element.recipient
        else:
            return None

    def setData(self, index, value, role):
        """Set the card data (with given role) at the specified index."""
        if index.row() >= self.rowCount() or not index.isValid():
            return False

        if role in self.roleNames():
            element = copy.copy(self.postCardList[index.row()])

            # TODO: check if values are valid
            if role == self.PHOTO_ROLE:
                element.photo = value
            elif role == self.BACK_TEXT_ROLE:
                element.backText = value
            elif role == self.RECIPIENT_ROLE:
                element.recipient = value

            self.postCardList[index.row()] = element
            self.dataChanged.emit(index, index, [role])

            return True
        else:
            return False

    def roleNames(self):
        """Return the role names for Qt."""
        return self.ROLE_NAMES

    @QtCore.Slot(result=int)
    def photoRole(self):
        """Return the photo role."""
        return self.PHOTO_ROLE

    @QtCore.Slot(result=int)
    def backTextRole(self):
        """Return the back text role."""
        return self.BACK_TEXT_ROLE

    @QtCore.Slot(result=int)
    def recipientRole(self):
        """Return the recipient role."""
        return self.RECIPIENT_ROLE

    def removeRows(self, row, count, parent=QtCore.QModelIndex()):
        """Remove rows from the list."""

        if row < 0 or count < 0 or (row + count) > self.rowCount():
            return False

        self.beginRemoveRows(parent, row, row + count - 1)
        del self.postCardList[row:(row + count)]
        self.endRemoveRows()

        return True

    @QtCore.Slot(int)
    def removePostCard(self, index):
        """Remove a postcard from the list."""
        self.removeRows(index, 1)

    # TODO change slot to provide correct API
    @QtCore.Slot(str)
    def appendPostCard(self, postCard):
        """Append a postcard to the list."""
        self.beginInsertRows(QtCore.QModelIndex(),
                             self.rowCount(),
                             self.rowCount())

        testCard = PostCardModel(postCard, "test", "Titi")
        self.postCardList.append(testCard)
        self.endInsertRows()

    def toCsvFile(self, filepath):
        """Save the card list to a csv File."""
        df = pd.DataFrame([p.toList() for p in self.postCardList],
                          columns=self.MODEL_FIELDS)
        df.to_csv(filepath)

    @classmethod
    def fromFile(cls, filepath):
        """Create a card list from a csv file."""
        df = pd.read_csv(filepath)

        assert df.shape[1] == len(cls.MODEL_FIELDS) + 1, \
               "Wrong number of columns in cards data."

        # Remove cards if specified image does not exist
        valid_cards = df["photo"].apply(lambda p: os.path.isfile(p))
        df = df[valid_cards]

        # TODO: Remove cards if recipient does not exist

        cardList = df.values.tolist()

        listModel = PostCardListModel()
        listModel.postCardList = []

        for card in cardList:
            listModel.postCardList.append(PostCardModel(*card[1:]))

        return listModel
