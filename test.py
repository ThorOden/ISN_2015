# Dessiner en utilisant paintEvent
from PyQt4 import QtGui,QtCore
import sys

from molecule import *
from gui import *

# coor (COORDONNEES, COULEUR, NOM)

class ZoneDessin(QtGui.QWidget) :
    def __init__(self, parent=None) :
        super().__init__(parent)
        self.listepoints=[]
        self.lignes = []
    def addPoint(self, c):
        self.listepoints.append(c)
        self.repaint()
    def addLine(self, a, b):
        """Ajoute une ligne entre a et b"""
        self.lignes.append((a,b))
        self.repaint()
    def paintEvent(self,e) :
        p=QtGui.QPainter(self)
        for i in self.listepoints:
            print(i[2])
            p.drawText(i[0], i[1], i[2])
        for i in self.lignes:
            p.drawLine(self.listepoints[i[0]][0], self.listepoints[i[0]][1], self.listepoints[i[1]][0], self.listepoints[i[1]][1])

class Fenetre(QtGui.QMainWindow):
    def __init__(self,molecule, parent=None) :
        super().__init__(parent)
        self.molecule = molecule
        self.resize(420,420)
        self.setWindowTitle("Dessin painEvent")
        dessin=ZoneDessin(self)
        c = [0,0]
        compt = 0
        for i in molecule:
            if i.nom != 'H':
                c[0] += 20
                c[1] = (-1)**compt * 10 + 20
                compt += 1
                dessin.addPoint((c[0], c[1],i.get_nom_gui()))#(COORDONNEES, COULEUR, NOM)*
        for i in molecule.get_cleaned_link(ignore="H"):
            dessin.addLine(i[0], i[1])

        dessin.setGeometry(10,10,400,400)

app=QtGui.QApplication(sys.argv)

atome0 = CARBONE()
atome1 = CARBONE()
atome2 = CARBONE()
atome3 = OXYGENE()
atome4 = HYDROGENE()
atome5 = HYDROGENE()
atome6 = HYDROGENE()
atome7 = HYDROGENE()
atome8 = HYDROGENE()
atome9 = AZOTE()

atome1.link(atome4, atome5, atome0, atome2)
atome2.link(atome7, atome8, atome3)
atome3.link(atome9)

molecule = Molecule(atome0, atome1,atome2,atome3,atome4,atome5,atome6,atome7,atome8,atome9)

frame=Fenetres(molecule)
frame.show()


sys.exit(app.exec_())

