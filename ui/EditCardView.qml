import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

import PostCard 1.0

Rectangle {

    property string title: qsTr("Edit card")
    property PostCardListModel model
    property RecipientListModel recipientListModel
    property int index
    property string photo: ""
    property string backText: ""
    property int recipientId: 0

    property var __qModelIndex: model.index(index, 0)

    Component.onDestruction: {
        model.setData(__qModelIndex, photo, model.photoRole())
        model.setData(__qModelIndex, backText, model.backTextRole())
        model.setData(__qModelIndex, recipientId, model.recipientIdRole())
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 30

        Image {
            id: photoEdit
            Layout.alignment: Qt.AlignCenter
            Layout.preferredWidth: parent.width * 0.75
            Layout.preferredHeight: Layout.preferredWidth * 0.75
            source: photo

            Item {
                id: changeImageHint
                anchors.fill: parent
                visible: false

                Rectangle {
                    id: changeImageRectHint
                    anchors.fill: parent
                    color: "black"
                    opacity: 0.6
                }

                Text {
                    anchors.centerIn: parent
                    text: qsTr("Change image")
                    color: "white"
                }
            }

            MouseArea {
                hoverEnabled: true
                anchors.fill: parent
                onEntered: photoEdit.state = "Hovering"
                onExited: photoEdit.state = ""
                onClicked: imagePicker.setVisible(true)
                onPressed: photoEdit.state = "Pressed"
                onReleased: {
                    if (containsMouse)
                        photoEdit.state="Hovering"
                    else
                        photoEdit.state=""
                }
            }

            states: [
                State {
                    name: "Hovering"
                    PropertyChanges { target: changeImageHint; visible: true}
                },
                State {
                    name: "Pressed"
                    PropertyChanges { target: changeImageHint; visible: true}
                    PropertyChanges { target: changeImageRectHint; opacity: 0.8}
                }
            ]
        }

        Text {
            id: backTextEdit
            text: '<b>Text</b>'
            padding: 10
        }

        TextField {
            text: backText
            Layout.fillWidth: true
            Layout.fillHeight: true
            onEditingFinished: backText = text
        }

        Text {
            text: '<b>Recipient</b>'
            padding: 10
        }

        ComboBox {
            id: recipientComboBox
            Layout.fillWidth: true
            currentIndex: 0
            model: recipientListModel
            textRole: "displayName"
            onActivated: recipientId = currentIndex
        }
    }

    ImagePicker {
        id: imagePicker
        selectMultiple: false
        onAccepted: photo = imagePicker.fileUrl
    }
}
