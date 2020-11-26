import QtQuick 2.0
import QtQuick.Dialogs 1.0

FileDialog {
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
