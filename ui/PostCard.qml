import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import QtQml 2.12

import PostCard 1.0

Item {
    id: container

    property StackView stackView
    property bool editableCard: true

    width: ListView.view.width
    height: 120

    Button {
        id: backgroundRect
        anchors.fill: parent
        anchors.leftMargin: 10
        anchors.rightMargin: 10
        enabled: editableCard

        onClicked: {
            if (!editableCard) {
                return
            }

            stackView.push(Qt.createComponent("EditCardView.qml"), {
                index: index,
                photo: photo,
                backText: backText,
                recipientId: recipientId
            })
        }

        RowLayout {
            anchors.fill: parent
            anchors.margins: 10
            spacing: 10

            Image {
                id: photoPreview
                Layout.fillHeight: true
                Layout.preferredWidth: container.height
                source: photo
                sourceSize.width: 512
                sourceSize.height: 512
                asynchronous: true
                fillMode: Image.PreserveAspectFit
            }

            ColumnLayout {

                Layout.fillWidth: true
                Layout.fillHeight: true

                Text {
                    text: backText
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    wrapMode: Text.Wrap
                    elide: Text.ElideRight
                }

                Text {
                    id: recipientNameText
                    property string recipientName: "Unknown"

                    function fetchRecipientName() {
                        var qModelIndex = recipientModel.index(recipientId, 0)
                        recipientName = recipientModel.data(qModelIndex, recipientModel.displayNameRole())
                    }

                    Component.onCompleted: fetchRecipientName()

                    text: recipientName
                    font.bold: true

                    Connections {
                        target: postCardModel
                        onDataChanged: {
                            recipientNameText.fetchRecipientName()
                        }
                    }
                }
            }

            RoundButton {
                id: deleteButton
                visible: editableCard
                Layout.preferredWidth: container.height * 0.5
                Layout.preferredHeight: Layout.preferredWidth
                text: "<b>x<b>"
                font.pointSize: 10
                onClicked: postCardModel.removePostCard(index)
            }
        }
    }
}
