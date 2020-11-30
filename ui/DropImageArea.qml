import QtQuick 2.12
import QtQuick.Window 2.12

import PostCard 1.0

DropArea {

    property Utils utils: Utils {}

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
                postCardModel.appendPostCard(image, "", 0)
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
