import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

import PostCard 1.0

ApplicationWindow {
    id: mainWindow

    width: 480
    height: 720
    visible: true
    title: qsTr("PostCardList")

    Utils {
        id: utils
    }

    Drawer {
        id: drawer
        width: 0.66 * mainWindow.width
        height: mainWindow.height
        interactive: stackView.depth == 1

        onInteractiveChanged: {
            drawer.close()
        }

        Column {
            anchors.fill: parent

            Button {
                id: loginButton
                width: parent.width
                text: "Log in"
                onClicked: {
                    stackView.push(Qt.createComponent("LoginView.qml"), {
                        stackView: stackView
                    })
                }
            }

            Button {
                id: recipientListButton
                width: parent.width
                text: "Recipients"
                onClicked: {
                    stackView.push(Qt.createComponent("RecipientListView.qml"), {
                        stackView: stackView
                    })
                }
            }

            Button {
                id: sentCardListButton
                width: parent.width
                text: "Sent cards"
                onClicked: {
//                    stackView.push(Qt.createComponent("LoginView.qml"), {
//                        stackView: stackView
//                    })
                }
            }
        }
    }

    header: ToolBar {
        id: toolBar
        contentHeight: toolButton.implicitHeight

        ToolButton {
            id: toolButton
            text: stackView.depth > 1 ? "\u25C0" : "\u2630"
            font.pixelSize: Qt.application.font.pixelSize * 1.6
            onClicked: {
                if (stackView.depth > 1) {
                    stackView.pop()
                }
                else {
                    drawer.open()
                }
            }
        }

        Label {
            text: stackView.currentItem.title
            anchors.centerIn: parent
        }
    }

    StackView {
        id: stackView
        anchors.fill: parent
        initialItem: MainView {
            id: mainView
            title: mainWindow.title
            utils: utils
            stackView: stackView
        }

        // Create the default recipient (sender) if none exists
        Component.onCompleted: {
            if (recipientModel.rowCount() == 0) {
                recipientModel.appendRecipient("", "", "", "", "")
                stackView.push(Qt.createComponent("EditRecipient.qml"), {
                    title: qsTr("Your coordinates"),
                    index: (recipientModel.rowCount() - 1),
                    firstName: "firstName",
                    lastName: "lastName",
                    address: "address",
                    city: "city",
                    zipCode: 9999
                })
            }
        }
    }

}
