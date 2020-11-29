import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

import PostCard 1.0

Rectangle {

    property string title: qsTr("Login")
    property StackView stackView
    property CredentialManager credentialManager

    ColumnLayout {
        anchors.fill: parent
        spacing: 30

        Text {
            text: qsTr("Username")
            padding: 10
        }

        TextField {
            id: usernameField
            text: ""
            Layout.fillWidth: true
        }

        Text {
            text: qsTr("Password")
            padding: 10
        }

        TextField {
            id: passwordField
            text: ""
            Layout.fillWidth: true
            echoMode: TextField.Password
        }

        Button {
            id: loginButton
            Layout.alignment: Qt.AlignCenter
            text: qsTr("Login")
            onClicked: {
                if (credentialManager.setCredentials(usernameField.text, passwordField.text)) {
                    console.log("Valid credentials")
                    stackView.pop()
                }
                else {
                    console.log("Invalid credentials.")
                }
            }
        }
    }
}
