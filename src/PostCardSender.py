from datetime import datetime
from PySide2 import QtCore

from postcard_creator import postcard_creator

from Utils import Utils

class PostCardSender(QtCore.QObject):
    """Class to send cards."""

    def __init__(self, credentialManager, parent=None):
        super().__init__(parent)

        self.credentialManager = credentialManager
        self.creator = None

        self.credentialManager.loggedIn.connect(self.updateCreator)

    @QtCore.Slot()
    def updateCreator(self):
        """Fetch the token to send cards."""
        if self.credentialManager.isLogged():
            self.creator = postcard_creator.PostcardCreator(
                self.credentialManager.getToken())

    @QtCore.Slot(result=float)
    def getRemainingTimeForNextCard(self):
        """Return the duration in seconds before a next card can be sent."""

        if self.creator is not None:

            try:
                if self.creator.get_quota()['available']:
                    return 0.0
                else:
                    dateTimeNext = datetime.fromisoformat(self.creator.get_quota()['next'])
                    dateTimeNow = datetime.now(dateTimeNext.tzinfo)

                    return float((dateTimeNext - dateTimeNow).seconds)
            except:
                return -1.0
        else:
            return -1.0

    def sendPostCard(self, postCard, sender, recipient):
        """Send a postcard and return true if it was successfully sent.

        Keyword arguments:
        postCard -- PostCardModel, card to sent
        sender -- RecipientModel, sender of the card
        recipient -- RecipientModel, recipient of the card
        """
        if not self.getRemainingTimeForNextCard() == 0.0:
            return False

        cardToSend = postcard_creator.Postcard(
            message=postCard.backText,
            recipient=recipient.toPostCardCreatorRecipient(),
            sender=sender.toPostCardCreatorSender(),
            picture_stream=open(Utils().trimFileUrlPrefix(postCard.photo), 'rb'))

        try:
            self.creator.send_free_card(postcard=cardToSend, mock_send=False)
        except postcard_creator.PostcardCreatorException:
            return False

        return True
