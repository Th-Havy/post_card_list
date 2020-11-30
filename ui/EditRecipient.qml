import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

import PostCard 1.0

Rectangle {

    property string title: qsTr("Edit recipient")
    property RecipientListModel model
    property int index
    property string firstName: ""
    property string lastName: ""
    property string address: ""
    property string city: ""
    property int zipCode: 0

    property var __qModelIndex: model.index(index, 0)

    Component.onDestruction: {
        model.setData(__qModelIndex, firstName, model.firstNameRole())
        model.setData(__qModelIndex, lastName, model.lastNameRole())
        model.setData(__qModelIndex, address, model.addressRole())
        model.setData(__qModelIndex, city, model.cityRole())
        model.setData(__qModelIndex, zipCode, model.zipCodeRole())
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 30

        Text {
            text: '<b>First name:</b> '
            padding: 10
        }

        TextField {
            id: firstNameField
            text: firstName
            Layout.fillWidth: true
            onEditingFinished: firstName = text
        }

        Text {
            text: '<b>Last name:</b> '
            padding: 10
        }

        TextField {
            id: lastNameField
            text: lastName
            Layout.fillWidth: true
            onEditingFinished: lastName = text
        }

        Text {
            text: '<b>Address:</b> '
            padding: 10
        }

        TextField {
            id: addressField
            text: address
            Layout.fillWidth: true
            onEditingFinished: address = text
        }

        Text {
            text: '<b>City:</b> '
            padding: 10
        }

        TextField {
            id: cityField
            text: city
            Layout.fillWidth: true
            onEditingFinished: city = text
        }

        Text {
            text: '<b>Zip code:</b> '
            padding: 10
        }

        TextField {
            id: zipCodeField
            text: zipCode
            Layout.fillWidth: true
            onEditingFinished: zipCode = text
            validator: IntValidator {bottom: 1000; top: 9999}
        }
    }
}
