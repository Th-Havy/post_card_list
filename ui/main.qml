import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

import PostCard 1.0

ApplicationWindow {
    id: mainWindow

    width: 480
    height: 720
    visible: appVisibility
    title: qsTr("PostCardList")

    Utils {
        id: utils
    }

    onClosing: {
        close.accepted = false
        appVisibility = false
        hide()
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
                onClicked: loginStateMachine.start()
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
                    stackView.push(Qt.createComponent("PostCardListView.qml"), {
                        title: qsTr("Sent cards"),
                        model: sentCardsModel,
                        stackView: stackView,
                        editable:false
                    })
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
        initialItem: PostCardListView {
            id: mainView
            title: mainWindow.title
            model: postCardModel
            stackView: stackView
        }

        Component.onCompleted: loginStateMachine.start()
    }

    LoginStateMachine {
        id: loginStateMachine
        stackView: stackView
        toolButton: toolButton
    }

}
