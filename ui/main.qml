import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Dialogs 1.0

import PostCard 1.0

Window {
    id: mainWindow

    width: 480
    height: 720
    visible: true
    title: qsTr("PostCardList")

    Utils {
        id: utils
    }

    FileDialog {
        id: imagePicker
        visible: false
        title: "Select an image"
        folder: shortcuts.home
        nameFilters: [ "Image files (*.jpg *.jpeg *.png *.bmp)"]
        selectExisting: true
        selectFolder: false
        selectMultiple: true
        onAccepted: {
            for (var image of imagePicker.fileUrls) {
                postCardModel.appendPostCard(image)
            }
        }
    }

    ListView {
        id: postCardListView
        model: postCardModel
        anchors.fill: parent
        spacing: 10
        delegate: PostCard {
            model: postCardModel
        }
    }

    RoundButton {
        id: newCardButton
        width: 80
        height: 80
        anchors.horizontalCenter: parent.right
        anchors.verticalCenter: parent.bottom
        anchors.horizontalCenterOffset: -width
        anchors.verticalCenterOffset: -height
        text: "<b>+<b>"
        font.pointSize: 18
        onClicked: imagePicker.setVisible(true)
    }

    DropArea {
        id: dropImageArea;
        anchors.fill: parent
        onEntered: {
            var validImage = false

            // Check if a valid image is among the dragged data
            for (var image of drag.urls) {
                validImage = validImage || utils.isValidDroppedImage(image)
            }

            dropAreaHint.state = validImage ? "VALID_DRAG" : "INVALID_DRAG"
        }
        onDropped: {
            for (var image of drop.urls) {
                if (utils.isValidDroppedImage(image)) {
                    postCardModel.appendPostCard(image)
                }
            }

            dropAreaHint.state = ""
        }
        onExited: {
            dropAreaHint.state = ""
        }

        Item {
            id: dropAreaHint
            anchors.fill: parent
            visible: false

            Rectangle {
                id: dropAreaHintRectangle
                anchors.fill: parent
                color: "black"
                opacity: 0.6
            }

            Text {
                id: dropAreaHintText
                anchors.centerIn: parent
                text: qsTr("Import images")
                font.pointSize: 20
                color: "white"
            }

            states: [
                State {
                    name: "VALID_DRAG"
                    PropertyChanges { target: dropAreaHint; visible: true}
                },
                State {
                    name: "INVALID_DRAG"
                    PropertyChanges { target: dropAreaHint; visible: true}
                    PropertyChanges { target: dropAreaHintText; text: qsTr("Invalid content")}
                    PropertyChanges { target: dropAreaHintRectangle; color: "#ffa4a4"}
                }
            ]
        }
    }
}
