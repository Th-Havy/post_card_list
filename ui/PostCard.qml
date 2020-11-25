import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

import PostCard 1.0

Item {
    id: container

    property PostCardListModel model

    width: ListView.view.width
    height: 120

    Rectangle {
        id: backgroundRect
        anchors.fill: parent
        anchors.leftMargin: 10
        anchors.rightMargin: 10
        color: "#ecf5b0"
        radius: 20

        RowLayout {
            anchors.fill: parent

            Image {
                id: photoPreview
                Layout.fillHeight: true
                Layout.preferredWidth: container.height
                Layout.margins: 10
                source: photo
            }

            Text {
                text: '<b>Text:</b> ' + backText
            }

            Text {
                text: '<b>Recipient:</b> ' + recipient
            }
        }

        RoundButton {
            id: deleteButton
            width: parent.height * 0.5
            height: parent.height * 0.5
            anchors.horizontalCenter: parent.right
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenterOffset: -width
            text: "<b>x<b>"
            font.pointSize: 10
            onClicked: model.removePostCard(index)
        }
    }
}
