import os

from PostCardModel import PostCardListModel
from RecipientModel import RecipientListModel


class Database:
    """Class handling the loading/storage of the card/recipient databases."""

    CARDS_FILE = "cards.csv"
    SENT_CARDS_FILE = "sent.csv"
    RECIPIENTS_FILE = "recipients.csv"

    def __init__(self, rootFolder, folder):
        self.rootFolder = rootFolder
        self.storageFolder = os.path.join(rootFolder, folder)
        self.cardsPath = os.path.join(self.storageFolder, self.CARDS_FILE)
        self.sentCardsPath = os.path.join(self.storageFolder, self.SENT_CARDS_FILE)
        self.recipientsPath = os.path.join(self.storageFolder, self.RECIPIENTS_FILE)

        os.makedirs(self.storageFolder, exist_ok=True)

        # Load or create recipient list
        if os.path.isfile(self.recipientsPath):
            self.recipientListModel = RecipientListModel.fromFile(self.recipientsPath)
        else:
            self.recipientListModel = RecipientListModel()
            self.recipientListModel.toCsvFile(self.recipientsPath)

        # Load or create card list
        if os.path.isfile(self.cardsPath):
            self.postCardListModel = PostCardListModel.fromFile(self.cardsPath)
        else:
            self.postCardListModel = PostCardListModel()
            self.postCardListModel.toCsvFile(self.cardsPath)

        # Load or create sent cards list
        if os.path.isfile(self.sentCardsPath):
            self.sentCardsListModel = PostCardListModel.fromFile(self.sentCardsPath)
        else:
            self.sentCardsListModel = PostCardListModel()
            self.sentCardsListModel.toCsvFile(self.sentCardsPath)

        self.postCardListModel.setSentCardsListModel(self.sentCardsListModel)

    def getPostCardListModel(self):
        """Get the list of postcards."""
        return self.postCardListModel

    def getSentCardsListModel(self):
        """Get the list of sent postcards."""
        return self.sentCardsListModel

    def getRecipientListModel(self):
        """Get the list of recipients"""
        return self.recipientListModel

    def saveDatabase(self):
        """Save the modifications to the database into files."""
        self.recipientListModel.toCsvFile(self.recipientsPath)
        self.postCardListModel.toCsvFile(self.cardsPath)
        self.sentCardsListModel.toCsvFile(self.sentCardsPath)
