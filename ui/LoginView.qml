import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

import PostCard 1.0

Rectangle {

    property string title: qsTr("Login")
    property StackView stackView
    property bool closeOnLogin: true

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 10
        spacing: 10

        TextField {
            id: usernameField
            Layout.fillWidth: true
            text: ""
            placeholderText: qsTr("Username")
        }

        TextField {
            id: passwordField
            Layout.fillWidth: true
            text: ""
            placeholderText: qsTr("Password")
            echoMode: TextField.Password
        }

        Button {
            id: loginButton
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignBottom
            text: qsTr("Login")
            onClicked: {
                if (credentialManager.setCredentials(usernameField.text, passwordField.text)) {
                    console.log("Valid credentials")
                    if (closeOnLogin) {
                        stackView.pop()
                    }
                }
                else {
                    console.log("Invalid credentials.")
                }
            }
        }
    }
}
