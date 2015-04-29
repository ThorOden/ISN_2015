﻿#! /usr/bin/python3

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys

from versBrute import *

from molecule import *

from math import *

DOUBLE = 1
SIMPLE = 0

DRAW_LANGUAGE = {
    "avance_simple": 0,
    "avance_double": 6,
    "tourne": 1,
    "O": 2,
    "N": 3,
    "C": 7,
    "branche": 4,
    "finbranche": 5,
}


class Drawer(QWidget):
    ready = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)

        self.draw_zone = DrawZone(self)

        self.editor = MoleculeEdit(self)

        self.btn_export = QPushButton("Exporter")
        self.btn_reset = QPushButton("Effacer")
        self.btn_ready = QPushButton("Convertir")
        self.btn_add_hydro = QPushButton("Ajouter les hydrogènes")
        self.btn_remove_hydro = QPushButton("Enlever les hydrogènes")

        self.layout_btn = QVBoxLayout(self)
        self.layout_btn.addWidget(self.btn_add_hydro)
        self.layout_btn.addWidget(self.btn_remove_hydro)
        self.layout_btn.addWidget(self.btn_reset)
        self.layout_btn.addWidget(self.btn_export)
        self.layout_btn.addWidget(self.btn_ready)

        self.layout.addWidget(self.draw_zone)
        self.layout.addWidget(self.editor)

        self.layout.addLayout(self.layout_btn)

        self.setLayout(self.layout)

        QObject.connect(self.btn_ready, SIGNAL('clicked()'), self.ready)
        QObject.connect(self.btn_reset, SIGNAL('clicked()'), self.reset)
        QObject.connect(self.btn_export, SIGNAL('clicked()'), self.export)
        QObject.connect(self.btn_add_hydro, SIGNAL('clicked()'), self.editor.addHydro)
        QObject.connect(self.btn_remove_hydro, SIGNAL('clicked()'), self.editor.removeHydro)

    def getMolecule(self):
        print(self.editor.getDrawCode())
        self.draw_zone.reset()
        self.draw_zone.draw(self.editor.getDrawCode())
        return self.editor.buildMolecule()

    @pyqtSlot()
    def reset(self):
        self.editor.reset()
        self.draw_zone.reset()

    @pyqtSlot()
    def export(self):
        fichier = QFileDialog.getSaveFileName(self, "Enregistrer la formule topologique", "", "*.png")
        self.draw_zone.save(fichier)
        QMessageBox.information(self, "Information", "Formule sauvegardée dans {}".format(fichier))


class Stack:

    def __init__(self):
        self.data = []

    def add(self, pos):
        self.data.append(pos)

    def look(self):
        return self.data[-1]

    def pop(self):
        r = self.data[-1]
        self.data = self.data[:-1]
        return r

    def reset(self):
        self.data = []

# DRAW_LANGUAGE = {
#     "avance_simple": 0,
#     "avance_double": 6,
#     "tourne": 1,
#     "O": 2,
#     "N": 3,
#     "C": 7,
#     "branche": 4,
#     "finbranche": 5,
# }


class DrawZone(QGraphicsView):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.pos_stor = Stack()
        self.angle_stor = Stack()
        self.fact_stor = Stack()
        self.current_pos = (0, 0)
        self.current_angle = 0

        self.fact = 1

    def draw(self, bytecode):
        self.pos_stor.add(self.current_pos)
        self.angle_stor.add((0, 0))
        for i in bytecode:
            if i in [DRAW_LANGUAGE["O"], DRAW_LANGUAGE["N"], DRAW_LANGUAGE["C"]]:
                self.draw_atome(i)
            elif i in [DRAW_LANGUAGE["avance_simple"], DRAW_LANGUAGE["avance_double"]]:
                self.draw_line(i)
            elif i is DRAW_LANGUAGE["branche"]:
                self.pos_stor.add(self.current_pos)
                self.angle_stor.add(self.current_angle)
                self.fact_stor.add(self.fact)
                self.current_angle += pi / 3 * self.fact
                self.fact *= -1
            elif i is DRAW_LANGUAGE["finbranche"]:
                self.current_pos = self.pos_stor.pop()
                self.current_angle = self.angle_stor.pop()
                self.fact = - self.fact_stor.pop()
                # self.current_angle += pi / 3 * self.fact
        self.setScene(self.scene)

    def draw_atome(self, atome):
        pos = self.current_pos
        if atome is DRAW_LANGUAGE["C"]:
            self.scene.addEllipse(pos[0], pos[1], 1, 1)
        elif atome is DRAW_LANGUAGE["O"]:
            t = self.scene.addText("O")
            t.setPos(pos[0], pos[1])
        elif atome is DRAW_LANGUAGE["N"]:
            t = self.scene.addText("N")
            t.setPos(pos[0], pos[1])

    def draw_line(self, line):
        pos = self.pos_stor.look()
        deplacement = (
            cos(self.current_angle) * 70, sin(self.current_angle) * 70)
        new_pos = (pos[0] + deplacement[0], pos[1] + deplacement[1])

        self.scene.addLine(pos[0], pos[1], new_pos[0], new_pos[1])

        if line is DRAW_LANGUAGE["avance_double"]:
            self.scene.addLine(
                pos[0], pos[1] + 10, new_pos[0], new_pos[1] + 10)
        self.current_pos = new_pos

    def reset(self):
        self.pos_stor.reset()
        self.angle_stor.reset()
        self.scene.clear()
        self.setScene(self.scene)
        self.current_angle = 0
        self.current_pos = (0, 0)
        self.fact = 1
    def save(self, fichier):
        pass


class MoleculeEdit(QTreeWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.first = AtomeItem(CARBONE, self)
        self.first.createEditor()

        self.setHeaderLabels(
            ["Atome", "", "Liaison à créer", "Atome à créer", ""])
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        QObject.connect(
            self, SIGNAL('customContextMenuRequested(QPoint)'), self.contextMenu)

    def buildMolecule(self):
        self.addHydro()
        return Molecule(*self.first.getAndLinkAtome())

    def reset(self):
        self.first.deleteAllChilds()

    @pyqtSlot(QPoint)
    def contextMenu(self, point):
        selected = self.itemAt(point)
        if selected is None:
            return
        menu = QMenu("Renommer en ...")
        menu.addAction("C")
        menu.addAction("H")
        menu.addAction("O")
        menu.addAction("N")
        menu.addSeparator()
        menu.addAction("Simple")
        menu.addAction("Double")

        action = menu.exec(self.mapToGlobal(point))
        if action is not None:
            if action.text() in "CHON":
                selected.changeName(action.text())
            else:
                selected.changeLiaison(action.text())

    def getDrawCode(self):
        return self.first.getDrawCode()

    @pyqtSlot()
    def addHydro(self):
        self.first.addHydro()
    @pyqtSlot()
    def removeHydro(self):
        self.first.removeHydro()


class AtomeItem(QTreeWidgetItem):
    ATOME_TYPE = {
        "C": CARBONE,
        "H": HYDROGENE,
        "O": OXYGENE,
        "N": AZOTE,
    }
    LIAISON_TYPE = {
        "Simple": 0,
        "Double": 1,
    }

    def __init__(self, atome, molecule, liaison=None, num=None, base=None):
        super().__init__()
        self.atome = atome()
        self.childs = []
        self.setText(0, self.atome.nom)
        self.molecule = molecule

        self.nb_hydro = 0

        if liaison == 0:
            self.setIcon(0, QIcon(QPixmap("simple.png")))
            self.liaison_type = 0
        elif liaison == 1:
            self.setIcon(0, QIcon(QPixmap("double.png")))
            self.liaison_type = 1
        else:
            molecule.addTopLevelItem(self)
            self.liaison_type = -1

        if num is not None:
            self.num = num
        else:
            self.num = None
        if base is not None:
            self.base = base
        else:
            self.base = None

        self.delete = QPushButton(QIcon(QPixmap("list-remove.png")), "")
        self.btn = QPushButton(QIcon(QPixmap("list-add.png")), "")
        self.liaison = QComboBox()
        self.liaison.addItem("Simple")
        self.liaison.addItem("Double")

        self.nature = QComboBox()
        self.nature.addItem("C")
        self.nature.addItem("H")
        self.nature.addItem("O")
        self.nature.addItem("N")

        QObject.connect(self.btn, SIGNAL('clicked()'), self.createChild)
        QObject.connect(self.delete, SIGNAL('clicked()'), self.deleteAtome)

    @pyqtSlot()
    def createChild(self):
        if self.ATOME_TYPE[self.nature.currentText()]:
            self.nb_hydro += 1
        nouveau = AtomeItem(self.ATOME_TYPE[self.nature.currentText()], self.molecule, self.LIAISON_TYPE[
                            self.liaison.currentText()], len(self.childs), self)
        self.addChild(nouveau)
        nouveau.createEditor()
        self.molecule.setCurrentItem(nouveau)

    @pyqtSlot()
    def deleteAtome(self):
        for i in self.childs:
            i.deleteAtome()
        if not self.base is None:
            self.base.deleteChild(self.num)
            self.base.removeChild(self)

    def deleteChild(self, num):
        if self.childs[num].atome.nom is "H":
            self.nb_hydro -= 1
        self.childs.pop(num)
        for i in range(num, len(self.childs)):
            self.childs[i].num = i

    @pyqtSlot()
    def deleteAllChilds(self):
        while len(self.childs) > 0:
            self.childs[0].deleteAllChilds()
            self.childs[0].deleteAtome()

    def createEditor(self):
        self.molecule.setItemWidget(self, 4, self.btn)
        self.molecule.setItemWidget(self, 2, self.liaison)
        self.molecule.setItemWidget(self, 3, self.nature)
        self.molecule.setItemWidget(self, 1, self.delete)

    def addChild(self, c):
        self.childs.append(c)
        super().addChild(c)

    def getAndLinkAtome(self):
        self.atome.delink()
        if len(self.childs) == 0:
            return [self.atome]
        else:
            voisins = []
            for i in self.childs:
                a = i.getAndLinkAtome()
                voisins = a + voisins
                self.atome.link(voisins[0])
            return [self.atome] + voisins

    def changeName(self, name):
        self.atome = self.ATOME_TYPE[name]()
        if self.atome.nom is "H" and not self.base is None:
            self.base.nb_hydro += 1
        self.setText(0, self.atome.nom)

    def changeLiaison(self, liaison):
        if self.liaison_type == -1:
            return
        self.liaison_type = self.LIAISON_TYPE[liaison]
        if self.liaison_type == 0:
            self.setIcon(0, QIcon(QPixmap("simple.png")))
        elif self.liaison_type == 1:
            self.setIcon(0, QIcon(QPixmap("double.png")))

    def getDrawCode(self):
        r = []
        if self.atome.nom is "H":
            return r
        if self.liaison_type is not -1:
            r.append(DRAW_LANGUAGE["branche"])
        if self.liaison_type is self.LIAISON_TYPE["Simple"]:
            r.append(DRAW_LANGUAGE["avance_simple"])
        if self.liaison_type is self.LIAISON_TYPE["Double"]:
            r.append(DRAW_LANGUAGE["avance_double"])
        if self.atome.nom in ["O", "N", "C"]:
            r.append(DRAW_LANGUAGE[self.atome.nom])
        for i in self.childs:
            r += i.getDrawCode()
        if self.liaison_type is not -1:
            r.append(DRAW_LANGUAGE["finbranche"])
        return r

    def addHydro(self):
        for i in self.childs:
            i.addHydro()

        borne=0
        if self.base is None and len(self.childs) < self.atome.nb_liaison:
            borne = self.atome.nb_liaison - len(self.childs)
        elif self.liaison_type is self.LIAISON_TYPE["Simple"] and (len(self.childs) + 1) < self.atome.nb_liaison:
            borne = self.atome.nb_liaison - (len(self.childs) + 1)
        elif self.liaison_type is self.LIAISON_TYPE["Simple"] and (len(self.childs) + 2) < self.atome.nb_liaison:
            borne = self.atome.nb_liaison - (len(self.childs) + 2)

        self.nb_hydro += borne
        for i in range(borne):
            nouveau = AtomeItem(self.ATOME_TYPE["H"], self.molecule, self.LIAISON_TYPE[
                    "Simple"], len(self.childs), self)
            self.addChild(nouveau)
            nouveau.createEditor()
    def removeHydro(self):
        for i in self.childs:
            i.removeHydro()
        i = 0
        while self.nb_hydro > 0 and i < len(self.childs):
            if self.childs[i].atome.nom is "H":
                self.childs[i].deleteAtome()
            else:
                i += 1 


class TextInput(QWidget):
    ready = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)

        self.button = QPushButton('Valider', self)
        self.input = QLineEdit(self)

        self.layout.addWidget(self.input)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)
        QObject.connect(self.button, SIGNAL('clicked()'), self.ready)

    def setText(self, s):
        self.input.setText(s)


class Fenetre(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout_text = QFormLayout(self)

        self.input_brute = TextInput(self)
        self.input_nomenc = TextInput(self)

        self.draw = Drawer(self)

        self.layout.addWidget(self.draw)

        self.layout_text.addRow('Formule brute :', self.input_brute)
        self.layout_text.addRow('Formule nomenclature :', self.input_nomenc)
        self.input_nomenc.setText("méthanamide")

        self.layout.addLayout(self.layout_text)
        self.setLayout(self.layout)

        QObject.connect(self.draw, SIGNAL('ready()'), self.fromGraph)

    @pyqtSlot()
    def fromGraph(self):
        try:
            m = self.draw.getMolecule()
            self.input_brute.setText(versFormuleBrute(m))
        except OverLinked as e:
            QMessageBox.critical(self, "Erreur", str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    t = Fenetre()
    t.show()
    sys.exit(app.exec_())