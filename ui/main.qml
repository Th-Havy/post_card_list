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

        position: ToolBar.Header

        RowLayout {
            anchors.fill: parent
            ToolButton {
                text: qsTr("‹")
                //onClicked: stack.pop()
            }
            Label {
                text: mainWindow.title
                elide: Label.ElideRight
                horizontalAlignment: Qt.AlignHCenter
                verticalAlignment: Qt.AlignVCenter
                Layout.fillWidth: true
            }
            ToolButton {
                text: qsTr("⋮")
                //onClicked: menu.open()
            }
        }
    }

    MainView {
        utils: utils
    }

    /*StackView {
        id: stack
        initialItem: mainView
        anchors.fill: parent
    }*/


}
