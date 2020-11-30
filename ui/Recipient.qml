import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

import PostCard 1.0

Item {
    id: container

    property RecipientListModel model
    property StackView stackView

    width: ListView.view.width
    height: 120

    Button {
        id: backgroundRect
        anchors.fill: parent
        anchors.leftMargin: 10
        anchors.rightMargin: 10

        onClicked: stackView.push(Qt.createComponent("EditRecipient.qml"), {
            model: model,
            index: index,
            firstName: firstName,
            lastName: lastName,
            address: address,
            city: city,
            zipCode: zipCode
        })

        Image {
            id: recipientIcon
            height: parent.height * 0.9
            fillMode: Image.PreserveAspectFit
            anchors.verticalCenter: parent.verticalCenter
            source: "../resources/recipient_icon.png"
        }

        RowLayout {
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.left: recipientIcon.right
            anchors.right: parent.right

            Text {
                text: firstName + " " + lastName
                Layout.alignment: Qt.AlignCenter
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
            onClicked: model.removeRecipient(index)
        }
    }
}
