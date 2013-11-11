
from PyQt4 import QtGui, QtCore
import sys

class BlockCipher(QtGui.QWidget):

    def __init__(self):
        super(BlockCipher, self).__init__()
        self.createwindow()
        self.placeWindowElements()
        self.attachSignals()

    def createwindow(self):
        self.setWindowTitle("Block Ciphers")

        #center window
        qr = self.frameGeometry()
        center = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(center)
        self.move(qr.topLeft())

    def placeWindowElements(self):
        self.algoLabel = QtGui.QLabel("Algorithm")
        self.algoList = QtGui.QComboBox()
        self.algoList.addItem("DES")
        #self.algoList.addItem("AES")
        self.algolayout = QtGui.QHBoxLayout()
        self.algolayout.setSpacing(10)
        self.algolayout.addWidget(self.algoLabel)
        self.algolayout.addWidget(self.algoList)

        self.modeLabel = QtGui.QLabel("Mode")
        self.modeList = QtGui.QComboBox()
        self.modeList.addItem("ECB")
        self.modelayout = QtGui.QHBoxLayout()
        self.modelayout.setSpacing(10)
        self.modelayout.addWidget(self.modeLabel)
        self.modelayout.addWidget(self.modeList)

        self.keyLabel = QtGui.QLabel("Key")
        self.keyText = QtGui.QLineEdit()
        self.keyList = QtGui.QComboBox()
        self.keyList.addItem("HEX")
        self.keyList.addItem("ASCII")
        self.keylayout = QtGui.QHBoxLayout()
        self.keylayout.setSpacing(10)
        self.keylayout.addWidget(self.keyLabel)
        self.keylayout.addWidget(self.keyText)
        self.keylayout.addWidget(self.keyList)

        self.encryptText = QtGui.QPlainTextEdit()
        self.encryptButton = QtGui.QPushButton("Encrypt")
        self.encryptList = QtGui.QComboBox()
        self.encryptList.addItem("ASCII")
        self.encryptList.addItem("HEX")
        self.encrypthlayout = QtGui.QHBoxLayout()
        self.encrypthlayout.addWidget(self.encryptList)
        self.encrypthlayout.addWidget(self.encryptButton)
        self.encryptlayout = QtGui.QVBoxLayout()
        self.encryptlayout.addWidget(self.encryptText)
        self.encryptlayout.addLayout(self.encrypthlayout)

        self.decryptText = QtGui.QPlainTextEdit()
        self.decryptButton = QtGui.QPushButton("Decrypt")
        self.decryptList = QtGui.QComboBox()
        self.decryptList.addItem("HEX")
        self.decryptList.addItem("ASCII")
        self.decrypthlayout = QtGui.QHBoxLayout()
        self.decrypthlayout.addWidget(self.decryptList)
        self.decrypthlayout.addWidget(self.decryptButton)
        self.decryptlayout = QtGui.QVBoxLayout()
        self.decryptlayout.addWidget(self.decryptText)
        self.decryptlayout.addLayout(self.decrypthlayout)

        self.edlayout = QtGui.QHBoxLayout()
        self.edlayout.addLayout(self.encryptlayout)
        self.edlayout.addLayout(self.decryptlayout)

        self.statusLabel = QtGui.QLabel()
        self.statusLabel.setWordWrap(True);

        self.layout = QtGui.QVBoxLayout()
        self.layout.addLayout(self.algolayout)
        self.layout.addLayout(self.modelayout)
        self.layout.addLayout(self.keylayout)
        self.layout.addLayout(self.edlayout)
        self.layout.addWidget(self.statusLabel)

        self.setLayout(self.layout)
        self.show()

    def attachSignals(self):
        pass

    def setStatus(self, msg, color = 'red'):
        self.statusLabel.setText("<font color='%s'>%s</font>" % (color, msg))

def main():
    app = QtGui.QApplication(sys.argv)
    client = BlockCipher()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
