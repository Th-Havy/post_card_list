from datetime import datetime
from PySide2 import QtCore

from postcard_creator import postcard_creator

class PostCardSender(QtCore.QObject):
    """Class to send cards."""

    def __init__(self, credentialManager, parent=None):
        super().__init__(parent)

        self.credentialManager = credentialManager

    @QtCore.Slot(result=float)
    def getRemainingTimeForNextCard(self):
        """Return the duration in seconds before a next card can be sent."""

        if self.credentialManager.isLogged():

            creator = postcard_creator.PostcardCreator(self.credentialManager.getToken())

            if creator.get_quota()['available']:
                return 0.0
            else:
                dateTimeNext = datetime.fromisoformat(creator.get_quota()['next'])
                dateTimeNow = datetime.now(dateTimeNext.tzinfo)

                return float((dateTimeNext - dateTimeNow).seconds)
        else:
            return -1.0
