import os
from PySide2 import QtCore
from PySide2.QtCore import Qt
import pandas as pd


class PostCardModel():

    MODEL_FIELDS = ["photo", "backText", "recipient"]
    MODEL_FIELDS_BYTE_LITERALS = [bytes(f, encoding="UTF-8")
                                  for f in MODEL_FIELDS]

    def __init__(self, photo=None, backText="", recipient=None):
        self.photo = photo
        self.backText = backText
        self.recipient = recipient

    def toList(self):
        return [self.photo, self.backText, self.recipient]


class PostCardListModel(QtCore.QAbstractListModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.postCardList = []

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.postCardList)

    def data(self, index, role):
        """Return the card data at the specified index."""
        if index.row() >= self.rowCount() or not index.isValid():
            return None

        if role in self.roleNames():
            roleName = self.roleNames()[role]
            element = self.postCardList[index.row()]

            if roleName == b"photo":
                return element.photo
            elif roleName == b"backText":
                return element.backText
            elif roleName == b"recipient":
                return element.recipient
        else:
            return None

    def headerData(self, section, orientation, role):
        """Return the header data."""
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            return PostCardModel.MODEL_FIELDS[section]
        else:
            return "{}".format(section)

    def roleNames(self):
        return {id: role for id, role in
                enumerate(PostCardModel.MODEL_FIELDS_BYTE_LITERALS,
                          start=Qt.UserRole)}

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
                          columns=PostCardModel.MODEL_FIELDS)
        df.to_csv(filepath)

    @staticmethod
    def fromFile(filepath):
        """Create a card list from a csv file."""
        df = pd.read_csv(filepath)

        assert df.shape[1] == len(PostCardModel.MODEL_FIELDS) + 1, \
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
