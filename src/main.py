import sys
import os
import time
import random
from threading import Thread

from PySide2 import QtGui, QtQml, QtWidgets

from PostCardModel import PostCardListModel
from RecipientModel import RecipientListModel
from Utils import Utils

# Global variable for conveniences
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..")


def registerQmlCustomTypes():
    """Register the custom QML types for the app."""
    QtQml.qmlRegisterType(PostCardListModel, "PostCard",
                          1, 0, "PostCardListModel")
    QtQml.qmlRegisterType(Utils, "PostCard", 1, 0, "Utils")


def sendCards(checkStop, tray):
    """Send periodically a card.

    Keyword arguments:
    checkStop -- method for requesting the thread to stop
    tray -- Application tray (QSystemTrayIcon) for sending notifications
    """

    lastSendingTime = time.time()
    waitingInterval = 1.0

    while True:
        if checkStop():
            break

        # Sleep while no card cand be sent
        if time.time() - lastSendingTime < waitingInterval:
            time.sleep(1.0)
            continue

        # TODO: check if waitingInterval needs to be adjusted

        # TODO: send card

        notifTitle = "PostCardList"
        notifMessage = app.tr("A new postcard was sent.")
        tray.showMessage(notifTitle , notifMessage, msecs=1000)

        lastSendingTime = time.time()
        waitingInterval = 24 * 60 * 60 + random.uniform(10.0, 7 * 60 * 60)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    appIcon = QtGui.QIcon(os.path.join(PROJECT_ROOT, "resources/app_icon.png"))
    app.setWindowIcon(appIcon)
    app.setOrganizationName("Th-Havy")
    app.setOrganizationDomain("blablabla.com")
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

    stopAllThreads = False

    cardSendingThread = Thread(target=sendCards,
                               args=[lambda : stopAllThreads, tray])
    cardSendingThread.start()

    # TODO remove these lines
    model = PostCardListModel.fromFile(
                os.path.join(PROJECT_ROOT, "data/cards.csv"))
    #model.toCsvFile("../data/cards2.csv")
    recipientModel = RecipientListModel.fromFile(
                        os.path.join(PROJECT_ROOT, "data/recipients.csv"))
    #recipientModel.toCsvFile("../data/recipients2.csv")

    # Set listviews data
    engine.rootContext().setContextProperty("postCardModel", model)
    engine.load(os.path.join(PROJECT_ROOT, "ui/main.qml"))

    # Run Qt App
    if not engine.rootObjects():
        sys.exit(-1)
    app.exec_()

    # Stop the running threads
    stopAllThreads = True
    cardSendingThread.join()
