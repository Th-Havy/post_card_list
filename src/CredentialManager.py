import time

from PySide2 import QtCore

from postcard_creator import postcard_creator

class CredentialManager(QtCore.QObject):
    """Class storing the credential for postcard_creator."""

    loggedIn = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.authentication_method = "swissid"
        self.username = ""
        self.password = ""
        self.__isLogged = False

    @QtCore.Slot(str, str, result=bool)
    def setCredentials(self, username, password):
        """Set the credentials, and check if they are valid."""
        token = postcard_creator.Token()

        try:
            if token.has_valid_credentials(username, password,
                                           self.authentication_method):
                self.username = username
                self.password = password
                self.__isLogged = True
                self.loggedIn.emit()
                return True
            else:
                self.username = ""
                self.password = ""
                self.__isLogged = False
                return False
        except:
            return False

    @QtCore.Slot(result=bool)
    def isLogged(self):
        """Return True if valid credentials are set."""
        return self.__isLogged

    def getToken(self):
        """Return the token necessary to order cards.

        setCredentials() must be called prior to this method."""

        if not self.__isLogged:
            return None

        token = postcard_creator.Token()

        trials = 5

        while trials > 0:
            trials -= 1
            try:
                token.fetch_token(self.username, self.password,
                                  self.authentication_method)
                return token
            except:
                time.sleep(3.0)

        return None

