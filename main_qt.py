#!/usr/bin/python3

from PyQt5 import QtWidgets
from PyQt5 import Qt
import text_reader


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.createUI()

    def selectFile(self):
        imported_file = QtWidgets.QFileDialog.getOpenFileName(self, "File to import", ".", "Txt (*.txt)")[0]
        cur_piece = text_reader.Piece()
        cur_piece.Populate(imported_file)
        self.label = QtWidgets.QLabel(cur_piece.Title)
        self.label.setSizePolicy(Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Expanding)
        self.main_layout.addWidget(self.label)

    def createUI(self):
        self.setWindowTitle('Text reader')

        menu = self.menuBar().addMenu('File')
        action = menu.addAction('Open')
        action.triggered.connect(self.selectFile)
        self.main_widget = QtWidgets.QWidget(self)
        self.main_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.main_layout.sizeConstraint = QtWidgets.QLayout.SetDefaultConstraint
        self.main_layout.addWidget(self.main_widget)
        #form_widget has its own main_widget where I put all other widgets onto
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)
        self.show()


if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())
