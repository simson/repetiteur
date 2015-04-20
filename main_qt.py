#!/usr/bin/python3


from PyQt5 import QtCore, QtWidgets, QtGui
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

    def fill_acte_box(self):
        self.acte_combobox.addItems(
            ["Acte " + cur_act.Number for cur_act in self.piece.Acts])

    def fill_scene_box(self):
        self.scene_combobox.disconnect()
        self.scene_combobox.clear()
        new_scenes = ["Scène " + scene.Number for scene
                      in self.piece.Acts[self.cur_acte_idx].Scenes]
        self.scene_combobox.addItems(new_scenes)
        self.update_text_box()
        self.scene_combobox.activated['QString'].connect(
            self.update_scene_box)

    def update_act_box(self):
        self.acte_combobox.disconnect()
        self.cur_acte_idx = self.acte_combobox.currentIndex()
        self.cur_replique_idx = 0
        self.fill_scene_box()
        self.update_text_box()
        self.scene_combobox.activated['QString'].connect(
            self.update_act_box)

    def update_scene_box(self):
        self.cur_scene_idx = self.scene_combobox.currentIndex()
        self.cur_replique_idx = 0
        self.update_text_box()

    def next_replique(self):
        self.cur_replique_idx += 1
        last_replique = len(self.piece.Acts[self.cur_acte_idx]
                            .Scenes[self.cur_scene_idx].Repliques)
        if self.cur_replique_idx == last_replique:
            self.cur_replique_idx = 0
            last_scene = len(self.piece.Acts[self.cur_acte_idx].Scenes)
            self.cur_scene_idx += 1
            if self.cur_scene_idx == last_scene:
                self.cur_scene_idx = 0
                self.cur_acte_idx += 1
                last_act = len(self.piece.Acts)
                if self.cur_acte_idx == last_act:
                    self.cur_acte_idx = 0

        self.update_text_box()

    def prev_replique(self):
        if self.cur_replique_idx == 0:
            if self.cur_scene_idx == 0:
                if self.cur_acte_idx != 0:
                    self.cur_replique_idx = len(self.piece.
                                                Acts[self.cur_acte_idx].
                                                Scenes[self.cur_scene_idx].
                                                Repliques)-1
                else:
                    self.cur_replique_idx = 0
            else:
                self.cur_scene_idx -= 1
                self.cur_replique_idx = len(self.piece.Acts[self.cur_acte_idx]
                                            .Scenes[self.cur_scene_idx]
                                            .Repliques)-1
        else:
            self.cur_replique_idx -= 1

        self.update_text_box()

    def update_text_box(self):
        self.acte_combobox.setCurrentIndex(self.cur_acte_idx)
        self.scene_combobox.setCurrentIndex(self.cur_scene_idx)
        self.character_value_label.setText(
            ", ".join(self.piece.Acts[self.cur_acte_idx]
                      .Scenes[self.cur_scene_idx]
                      .Repliques[self.cur_replique_idx].Characters))
        self.replique_value_label.setText(
            str(self.cur_replique_idx+1) + " / "
            + str(len(self.piece.Acts[self.cur_acte_idx]
                      .Scenes[self.cur_scene_idx].Repliques)))
        self.text_box.setText(self.piece.Acts[self.cur_acte_idx]
                              .Scenes[self.cur_scene_idx]
                              .Repliques[self.cur_replique_idx].text)
        if self.piece.Acts[self.cur_acte_idx].Scenes[self.cur_scene_idx].Repliques[self.cur_replique_idx].Characters.count(self.characters.currentText()) == 0:
            self.text_box.setFont(self.otherfont)
        else:
            self.text_box.setFont(self.myhiddenfont)
			

    def update_window_new_piece(self, imported_file):
        self.piece = text_reader.Piece()
        self.piece.Populate(imported_file)
        self.cur_replique_idx = 0
        self.cur_acte_idx = 0
        self.cur_scene_idx = 0

        self.title = QtWidgets.QLabel(self.piece.Title)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.main_layout.addWidget(self.title)
        self.status_hlayout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.status_hlayout)

        self.characters = QtWidgets.QComboBox()
        self.characters.addItems([character for character
                                  in self.piece.Characters])
        self.status_hlayout.addWidget(self.characters)
        self.acte_combobox = QtWidgets.QComboBox()
        self.acte_combobox.activated['QString'] \
            .connect(self.update_act_box)
        self.scene_combobox = QtWidgets.QComboBox()
        self.scene_combobox.activated['QString'] \
            .connect(self.update_scene_box)
        self.NextReplique = QtWidgets.QPushButton("Next Replique")
        self.status_hlayout.addWidget(self.acte_combobox)
        self.status_hlayout.addWidget(self.scene_combobox)
        self.status_hlayout.addWidget(self.NextReplique)
        self.NextReplique.clicked.connect(self.next_replique)

        self.cur_replique_hlayout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.cur_replique_hlayout)
        self.character_label = QtWidgets.QLabel("Personnage(s) :")
        self.character_label.setAlignment(QtCore.Qt.AlignLeft)
        self.character_value_label = QtWidgets.QLabel()
        self.character_value_label.setAlignment(QtCore.Qt.AlignLeft)
        self.replique_label = QtWidgets.QLabel("Replique :")
        self.replique_label.setAlignment(QtCore.Qt.AlignRight)
        self.replique_value_label = QtWidgets.QLabel()
        self.replique_value_label.setAlignment(QtCore.Qt.AlignRight)
        self.character_value_label.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed)

        self.cur_replique_hlayout.addWidget(self.character_label)
        self.cur_replique_hlayout.addWidget(self.character_value_label)
        self.cur_replique_hlayout.addWidget(self.replique_label)
        self.cur_replique_hlayout.addWidget(self.replique_value_label)

        self.text_box = QtWidgets.QLabel()
        self.text_box.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                    QtWidgets.QSizePolicy.Expanding)
# self.text_box.setStyleSheet("QLabel{ background-color : red; color : blue;}")
        self.text_box.setFont(QtGui.QFont("Arial", 36, QtGui.QFont.Bold))
        self.text_box.setAlignment(QtCore.Qt.AlignCenter)
        self.text_box.setWordWrap(True)
        self.main_layout.addWidget(self.text_box)

        self.fill_acte_box()
        self.fill_scene_box()

    def createUI(self):
        self.setWindowTitle('Text reader')
        menu = self.menuBar().addMenu('File')
        action = menu.addAction('Open')
        action.triggered.connect(self.open_play)
        self.main_widget = QtWidgets.QWidget(self)
        self.main_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.main_layout.setAlignment(QtCore.Qt.AlignHCenter
                                      | QtCore.Qt.AlignTop)
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)
        self.myhiddenfont = QtGui.QFont("Arial", 6, QtGui.QFont.Bold)
        self.otherfont = QtGui.QFont("Arial", 36, QtGui.QFont.Bold)

        self.show()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Right:
            self.next_replique()
        if e.key() == QtCore.Qt.Key_Left:
            self.prev_replique()
        if e.key() == QtCore.Qt.Key_Enter:
            if self.text_box.font() == self.otherfont:
                self.text_box.setFont(self.myhiddenfont)
            else:
                self.text_box.setFont(self.otherfont)


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
