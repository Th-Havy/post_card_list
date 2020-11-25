import QtQuick 2.12
import QtQuick.Layouts 1.12

Item {
    id: container
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
            Text { text: '<b>Recipient:</b> ' + recipient }
        }
    }
}
