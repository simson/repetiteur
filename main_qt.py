#!/usr/bin/python3
#
# helloworld.py
# Un simple exemple de traditionnel ”Hello World”

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys

def main(args) :
     #chaque programme doit disposer d'une instance de QApplication gérant l'ensemble des widgets
     app=QApplication(args)
     #un nouveau bouton
     button=QPushButton("Hello World !", None)
     #qu'on affiche
     button.show()
     #fin de l'application lorsque toutes les fenêtres sont fermées
     app.connect(app,SIGNAL("lastWindowClosed()"),app,SLOT("quit()"))
     #fin de l'application lorsque l'utilisateur clique sur le bouton
     app.connect(button, SIGNAL("clicked()"),app,SLOT("quit()"))
     #boucle principale de traitement des évènements
     app.exec_()

if __name__ == "__main__" :
    main(sys.argv)




