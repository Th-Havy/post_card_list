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
                    stackView.push(Qt.createComponent("LoginView.qml"), {
                        stackView: stackView,
                        credentialManager: credentialManager
                    })
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
    }


}
