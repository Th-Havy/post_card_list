import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import QtQuick.Dialogs 1.0

import PostCard 1.0

Item {
    id: recipientView

    property string title: qsTr("Recipient list")
    property StackView stackView

    ListView {
        id: recipientListView
        model: recipientModel
        anchors.fill: parent
        spacing: 10
        anchors.topMargin: spacing
        delegate: Recipient {
            stackView: recipientView.stackView
        }
    }

    RoundButton {
        id: newRecipientButton
        width: 80
        height: 80
        anchors.horizontalCenter: parent.right
        anchors.verticalCenter: parent.bottom
        anchors.horizontalCenterOffset: -width * 0.75
        anchors.verticalCenterOffset: -height * 0.75
        text: "<b>+<b>"
        font.pointSize: 18
        onClicked: {
            recipientModel.appendRecipient("", "", "", "", "")
            stackView.push(Qt.createComponent("EditRecipient.qml"), {
                title: qsTr("New recipient"),
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
