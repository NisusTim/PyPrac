import QtQuick 2.0  // set the source of QQuickView to url of *.qml

Rectangle {
  width: 200
  height: 200
  color: 'green'

  Text {
    text: "hello, world"
    anchors.centerIn: parent  // anchors: to align; parent: Rectangle
  }
}
