import sys
import os
import time
import random
from threading import Thread

from PySide2 import QtGui, QtQml, QtWidgets
from PySide2.QtCore import Qt

from PostCardModel import PostCardListModel
from RecipientModel import RecipientListModel
from Database import Database
from Utils import Utils
from CredentialManager import CredentialManager
from PostCardSender import PostCardSender

# Global variable for conveniences
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..")


def registerQmlCustomTypes():
    """Register the custom QML types for the app."""

    QtQml.qmlRegisterType(PostCardListModel, "PostCard",
                          1, 0, "PostCardListModel")
    QtQml.qmlRegisterType(RecipientListModel, "PostCard",
                          1, 0, "RecipientListModel")
    QtQml.qmlRegisterType(Utils, "PostCard", 1, 0, "Utils")
    QtQml.qmlRegisterType(CredentialManager, "PostCard",
                          1, 0, "CredentialManager")


def sendCards(checkStop, tray, postCardListModel, sentCardsListModel, postCardSender):
    """Send periodically a card.

    Keyword arguments:
    checkStop -- method for requesting the thread to stop
    tray -- Application tray (QSystemTrayIcon) for sending notifications
    postCardSender -- PostCardSender, for sending cards
    """

    threadSleepDuration = 2.5
    lastSendingTime = time.time()
    waitingInterval = 5.0

    while True:
        if checkStop():
            break

        if not postCardSender.credentialManager.isLogged():
            time.sleep(threadSleepDuration)
            continue

        # Sleep while no card cand be sent
        if time.time() - lastSendingTime < waitingInterval:
            time.sleep(threadSleepDuration)
            continue

        # Check if waitingInterval needs to be adjusted
        remainingTime = postCardSender.getRemainingTimeForNextCard()
        if remainingTime < 0:
            # Not logged in
            continue
        elif remainingTime > 0:
            waitingInterval += remainingTime + threadSleepDuration
            continue

        # TODO: send card

        # Remove top-most card from list
        postCardListModel.requestRemovePostCard.emit(0)

        # Send notification that card was sent
        notifTitle = "PostCardList"
        notifMessage = app.tr("A new postcard was sent.")
        tray.showMessage(notifTitle, notifMessage, msecs=1000)

        # Wait 24h + some random time before sending a new card
        lastSendingTime = time.time()
        waitingInterval = 24 * 60 * 60 + random.uniform(10.0, 7 * 60 * 60)


if __name__ == "__main__":

    # Create qml application
    QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QtWidgets.QApplication.setOrganizationName("Th-Havy")
    QtWidgets.QApplication.setOrganizationDomain("blablabla.com")

    # Non-existent in PySide2: QQuickStyle.setStyle("material")
    sys_argv = sys.argv
    sys_argv += ['--style', 'material']

    app = QtWidgets.QApplication(sys_argv)
    appIcon = QtGui.QIcon(os.path.join(PROJECT_ROOT, "resources/app_icon.png"))
    app.setWindowIcon(appIcon)
    engine = QtQml.QQmlApplicationEngine()
    registerQmlCustomTypes()

    # Tray menu
    menu = QtWidgets.QMenu()
    settingAction = menu.addAction("setting")
    exitAction = menu.addAction("exit")
    exitAction.triggered.connect(app.quit)

    tray = QtWidgets.QSystemTrayIcon()
    tray.setIcon(appIcon)
    tray.setContextMenu(menu)
    tray.setToolTip(app.tr("PostCardList is running in the background."))
    tray.show()

    # Create/load database
    database = Database(PROJECT_ROOT, "data")

    # TODO: handle credentials
    credentialManager = CredentialManager()
    postCardSender = PostCardSender(credentialManager)

    # Set listviews data and load UI
    engine.rootContext().setContextProperty("postCardModel", database.getPostCardListModel())
    engine.rootContext().setContextProperty("sentCardsModel", database.getSentCardsListModel())
    engine.rootContext().setContextProperty("recipientModel", database.getRecipientListModel())
    engine.rootContext().setContextProperty("credentialManager", credentialManager)
    engine.load(os.path.join(PROJECT_ROOT, "ui/main.qml"))

    # Start threads
    stopAllThreads = False
    cardSendingThread = Thread(target=sendCards, args=[
        lambda : stopAllThreads, tray, database.getPostCardListModel(),
                 database.getSentCardsListModel(), postCardSender])
    cardSendingThread.start()

    # Run Qt App
    if not engine.rootObjects():
        sys.exit(-1)
    app.exec_()

    # Stop the running threads
    stopAllThreads = True
    cardSendingThread.join()

    # Save the changes to the database
    database.saveDatabase()
