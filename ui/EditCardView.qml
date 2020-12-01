import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

import PostCard 1.0

Rectangle {

    property string title: qsTr("Edit card")
    property int index
    property string photo: ""
    property string backText: ""
    property int recipientId: 0

    property var __qModelIndex: postCardModel.index(index, 0)

    Component.onDestruction: {
        postCardModel.setData(__qModelIndex, photo, postCardModel.photoRole())
        postCardModel.setData(__qModelIndex, backText, postCardModel.backTextRole())
        postCardModel.setData(__qModelIndex, recipientId, postCardModel.recipientIdRole())
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 30

        Image {
            id: photoEdit
            Layout.alignment: Qt.AlignCenter
            Layout.preferredWidth: parent.width * 0.75
            Layout.preferredHeight: Layout.preferredWidth * 0.75
            Layout.maximumHeight: parent.height * 0.66
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
            text: qsTr("Text")
            padding: 10
        }

        TextArea  {
            id: backTextEdit

            property int maximumLength: 700

            text: backText
            onTextChanged: if (length > maximumLength) remove(maximumLength, length)
            placeholderText: qsTr("Text on the back of the letter.")
            Layout.fillWidth: true
            onEditingFinished: backText = text
        }

        Text {
            text: qsTr("Recipient")
            padding: 10
        }

        ComboBox {
            id: recipientComboBox
            Layout.fillWidth: true
            currentIndex: recipientId
            model: recipientModel
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
