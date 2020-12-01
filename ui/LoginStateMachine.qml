import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import QtQml.StateMachine 1.12 as DSM

DSM.StateMachine {
    id: loginStateMachine

    property StackView stackView
    property ToolButton toolButton

    initialState: loginState
    running: false

    DSM.State {
        id: loginState

        DSM.SignalTransition {
            targetState: cancelledLoginState
            signal: toolButton.clicked
        }

        DSM.SignalTransition {
            targetState: justLoggedState
            signal: credentialManager.loggedIn
        }

        // Open login page
        onEntered: {
            stackView.push(Qt.createComponent("LoginView.qml"), {
                stackView: stackView,
                closeOnLogin: false
            })
        }
    }

    DSM.State {
        id: justLoggedState

        signal triggered()

        DSM.SignalTransition {
            targetState: addSenderCoordinatesState
            signal: justLoggedState.triggered
            guard: recipientModel.rowCount() == 0
        }

        DSM.SignalTransition {
            targetState: readyState
            signal: justLoggedState.triggered
            guard: recipientModel.rowCount() > 0
        }

        onEntered: {
            triggered()
            if (recipientModel.rowCount() > 0) {
                stackView.pop()
            }
        }
    }

    DSM.State {
        id: addSenderCoordinatesState

        DSM.SignalTransition {
            targetState: readyState
            signal: toolButton.clicked
        }

        // Create the default recipient (sender)
        onEntered: {
            recipientModel.appendRecipient("", "", "", "", "")
            stackView.replace(Qt.createComponent("EditRecipient.qml"), {
                title: qsTr("Your coordinates"),
                index: (recipientModel.rowCount() - 1),
                firstName: "firstName",
                lastName: "lastName",
                address: "address",
                city: "city",
                zipCode: 9999
            })
        }
    }

    DSM.FinalState {
        id: cancelledLoginState
    }

    DSM.FinalState {
        id: readyState
    }
}
