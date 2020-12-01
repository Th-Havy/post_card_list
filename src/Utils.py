import os
from PySide2 import QtCore
from PySide2.QtCore import Qt


class Utils(QtCore.QObject):
    """Class exposing utility functions to QML app."""

    IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')

    def __init__(self, parent=None):
        super().__init__(parent)

    @QtCore.Slot(str, result=bool)
    def isValidImage(self, path):
        """Check if the provided path corresponds to a valid image."""
        if os.path.isfile(path):
            return path.lower().endswith(Utils.IMAGE_EXTENSIONS)

        return False

    @QtCore.Slot(str, result=bool)
    def isValidDroppedImage(self, url):
        """Check if the provided url corresponds to a valid image."""
        dropFilePrefix = "file:///"

        if url.lower().startswith(dropFilePrefix):
            path = self.trimFileUrlPrefix(url)

            return self.isValidImage(path)

        return False

    @QtCore.Slot(str, result=str)
    def trimFileUrlPrefix(self, url):
        """Check if the provided url corresponds to a valid image."""
        dropFilePrefix = "file:///"

        return url.replace(dropFilePrefix, "", 1)
