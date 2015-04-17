#!/usr/bin/python3
import regex as re

regex_acte = re.compile(".*Acte(?P<NB_Acte>.*)\s+", re.VERBOSE)
regex_scene = re.compile("Scène (?P<NB_Scene>.*)", re.VERBOSE)
regex_character = re.compile("(?P<name>[A-Z]{2,})", re.VERBOSE)


class Piece:
    def __init__(self, title="", acts=[]):
        self.Title = title
        self.Acts = acts

    def Populate(self, filename):
        with open(filename) as f:
            for num, line in enumerate(f, 1):
                match = regex_acte.match(line)
                if match:
                    cur_acte = Acte(match.group("NB_Acte").strip())
                    cur_piece.Acts.append(cur_acte)

                else:
                    match = regex_scene.match(line)
                    if match:
                        cur_scene = Scene(match.group("NB_Scene").strip())
                        cur_acte.Scenes.append(cur_scene)

                    else:
                        match = regex_character.match(line)
                        if match:
                            info = [i.replace('\n', '')
                                    for i in re.split(", |\. ", line)]
                            personnage = [x for x in info if x.isupper()]
                            didascalie = [x for x in info if not x.isupper()]
                            cur_replique = Replique(personnage, didascalie)
                            cur_scene.Repliques.append(cur_replique)
                        else:
                            if line and 'cur_replique' in locals():
                                cur_replique.text += line


class Acte:
    def __init__(self, Number=""):
        self.Number = Number
        self.Scenes = []


class Scene:
    def __init__(self, Number="", Actors=[]):
        self.Number = Number
        self.Actors = Actors
        self.Repliques = []


class Actor:
    def __init__(self, Name):
        self.Name = Name


class Replique:
    def __init__(self, Actors=[], didascalie="", text=""):
        self.Actors = Actors
        self.text = text
        self.didascalie = didascalie

    def __str__(self):
        return ", ".join(self.Actors) + " " + ", ".join(self.didascalie) + \
            "\n" + self.text


cur_piece = Piece()
cur_piece.Populate("georges_dandin.txt")
