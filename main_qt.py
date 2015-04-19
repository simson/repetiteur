#!/usr/bin/python3


from PyQt5 import QtCore, QtWidgets
import text_reader


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.createUI()

    def open_play(self):
        self.selectFile()
        self.update_window_new_piece(self.imported_file)

    def selectFile(self):
        self.imported_file = QtWidgets.QFileDialog. \
            getOpenFileName(self, "File to import", ".", "Txt (*.txt)")[0]

    def update_window_new_piece(self, imported_file):
        cur_piece = text_reader.Piece()
        cur_piece.Populate(imported_file)
        self.title = QtWidgets.QLabel(cur_piece.Title)
        self.main_layout.addWidget(self.title)

        self.status_bar = QtWidgets.QStatusBar()
        self.main_layout.addWidget(self.status_bar)
        self.acte = QtWidgets.QComboBox()
        self.acte.addItems(
            ["Acte " + cur_act.Number for cur_act in cur_piece.Acts])
        self.actors = QtWidgets.QComboBox()
        self.status_bar.addWidget(self.actors)
        self.status_bar.addWidget(self.acte)

    def createUI(self):
        self.setWindowTitle('Text reader')

        menu = self.menuBar().addMenu('File')
        action = menu.addAction('Open')
        action.triggered.connect(self.open_play)
        self.main_widget = QtWidgets.QWidget(self)
        self.main_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.main_layout.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)
        self.show()


if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
#   Debug only
    window.imported_file = "georges_dandin.txt"
    window.update_window_new_piece(window.imported_file)
#
    sys.exit(app.exec_())
