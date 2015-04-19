import regex as re

regex_acte = re.compile(".*Acte(?P<NB_Acte>.*)\s+", re.VERBOSE)
regex_scene = re.compile("Scène (?P<NB_Scene>.*)", re.VERBOSE)
regex_character = re.compile("(?P<name>[A-Z]{2,})", re.VERBOSE)


class Piece:
    def __init__(self, title="", acts=[], Actors=set()):
        self.Title = title
        self.Acts = acts
        self.Actors = Actors

    def Populate(self, filename):
        with open(filename) as f:
            for num, line in enumerate(f, 1):
                if num == 1:
                    self.Title = line
                    continue

                match = regex_acte.match(line)
                if match:
                    cur_acte = Acte(match.group("NB_Acte").strip())
                    self.Acts.append(cur_acte)

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
                            self.Actors.add(tuple(personnage))
                            cur_replique = Replique(personnage, didascalie)
                            cur_scene.Repliques.append(cur_replique)
                        else:
                            if line and 'cur_replique' in locals():
                                cur_replique.text += line

    def __str__(self):
        piece = self.Title + "\n"
        for acte in self.Acts:
            piece += str(acte)

        return piece


class Acte:
    def __init__(self, Number=""):
        self.Number = Number
        self.Scenes = []

    def __str__(self):
        acte = "Acte " + self.Number + "\n"
        for scene in self.Scenes:
            acte += str(scene)

        return acte


class Scene:
    def __init__(self, Number="", Actors=[]):
        self.Number = Number
        self.Actors = Actors
        self.Repliques = []

    def __str__(self):
        scene = "Scene " + self.Number + "\n"
        for replique in self.Repliques:
            scene += str(replique)

        return scene


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
