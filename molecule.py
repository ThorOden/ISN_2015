"""Classe molÃ©cule et dÃ©pendances"""

class OverLinked(Exception):
    pass

class Atome:
    def __init__(self, nom, nb_liaison, display_name_gui=True):
        self.liaisons = []
        self.nom = nom
        self.nb_liaison = nb_liaison
        self.nb_current_liaison = 0
        self.display_name_gui = display_name_gui
    def link(self, atome, n=1, relink=True):
        if self.nb_current_liaison+n > self.nb_liaison:
            raise OverLinked(''.join([self.nom, str(self.liaisons), str(atome), str(self.nb_liaison), str(n)]))
        else:
            self.nb_current_liaison += n
            self.liaisons.append([atome, n])
            if relink:
                atome.link(self, relink=False)
    def get_link(self):
        return list(self.liaisons)
    def __str__(self):
        return self.nom + ', liÃ© ' + str(len(self.liaisons))
    def get_nom_gui(self):
        if self.display_name_gui:
            return self.nom
        else:
            return ''
    def delink(self):
        self.nb_current_liaison = 0
        self.liaisons = []
    # def get_data(self):
    #     return (self.nom, self.)

CARBONE = lambda : Atome('C', 4, display_name_gui=False)
HYDROGENE = lambda : Atome('H', 1)
OXYGENE = lambda : Atome('O', 2)
AZOTE = lambda : Atome('N', 3)

class Molecule(list):
    def __init__(self, *atome):
        list.__init__(self)
        self.add_atome(atome)
    def add_atome(self, *atome):
        for i in atome[0]:
            self.append(i)
    def get_cleaned_link(self, ignore=''):
        r = []
        for x,i in enumerate(self):
            if not i.nom == ignore:
                for j in i.get_link():
                    if j.nom != ignore:
                        r.append((x, self.index(j)))

        return r

if __name__ == "__main__":

    c = CARBONE()
    h1 = HYDROGENE()
    h2 = HYDROGENE()
    o = OXYGENE()

    c.link(h1)
    c.link(h2)
    c.link(o, 2)