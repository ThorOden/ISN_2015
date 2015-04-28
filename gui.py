#! /usr/bin/python3

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys

from versBrute import *

from molecule import *

DOUBLE = 1
SIMPLE = 0

DRAW_LANGUAGE = {
    "avance_simple": 0,
    "avance_double": 6,
    "tourne": 1,
    "O": 2,
    "N": 3,
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

        self.btn = QPushButton("Travail !!!")

        self.layout.addWidget(self.draw_zone)
        self.layout.addWidget(self.editor)

        self.layout.addWidget(self.btn)

        self.setLayout(self.layout)

        QObject.connect(self.btn, SIGNAL('clicked()'), self.ready)

    def readyEmit(self):
        self.ready.emit()

    def getMolecule(self):
        print(self.editor.getDrawCode())
        return self.editor.buildMolecule()


class Stack:

    def __init__(self):
        self.data = []

    def add(self, pos):
        self.data.append(pos)

    def pop(self):
        r = self.data[-1]
        self.data = self.data[:-1]

    def reset(self):
        self.data = []


class DrawZone(QGraphicsView):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.stack = Stack()

    def draw(self, bytecode):
        self.stack.add((0,0))
        angle = 0
        for i in bytecode:
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
        return Molecule(*self.first.getAndLinkAtome())

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
        nouveau = AtomeItem(self.ATOME_TYPE[self.nature.currentText()], self.molecule, self.LIAISON_TYPE[
                            self.liaison.currentText()], len(self.childs), self)
        self.addChild(nouveau)
        nouveau.createEditor()
        self.molecule.setCurrentItem(nouveau)

    @pyqtSlot()
    def deleteAtome(self):
        for i in self.childs:
            i.delete()
        if self.base is not None:
            self.base.deleteChild(self.num)
            self.base.removeChild(self)

    def deleteChild(self, num):
        self.childs.pop(num)
        for i in range(num, len(self.childs)):
            self.childs[i].num = i

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
