# Créé par levyfalk, le 02/02/2015 en Python 3.2
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys

from molecule import *

DOUBLE = 1
SIMPLE = 0

class Drawer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)

        self.draw_zone = DrawZone(self)

        self.editor = MoleculeEdit(self)

        self.btn = QPushButton("Ajouter un enfant")

        self.test = AtomeItem(CARBONE, self.editor)
        self.test3 = AtomeItem(HYDROGENE, self.editor, SIMPLE)
        self.test4 = AtomeItem(HYDROGENE, self.editor, SIMPLE)
        self.test5 = AtomeItem(AZOTE, self.editor, SIMPLE)
        self.test6 = AtomeItem(OXYGENE, self.editor, DOUBLE)
        self.test7 = AtomeItem(OXYGENE, self.editor, SIMPLE)
        self.test8 = AtomeItem(HYDROGENE, self.editor, SIMPLE)

        self.test5.addChild(self.test6)
        self.test5.addChild(self.test7)
        self.test7.addChild(self.test8)

        self.test.addChild(self.test3)
        self.test.addChild(self.test4)
        self.test.addChild(self.test5)

        self.editor.addTopLevelItem(self.test)

        self.test.createEditor()
        self.test3.createEditor()
        self.test4.createEditor()
        self.test5.createEditor()
        self.test6.createEditor()

        self.layout.addWidget(self.draw_zone)
        self.layout.addWidget(self.editor)

        self.setLayout(self.layout)


class DrawZone(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.scene.setSceneRect(0,0,400,400)
        self.current_atome = 'N'
        self.current_liaison = 'S'
        self.position_preced = None
    @pyqtSlot(str)
    def set_curent_atome(self, a):
        print(a)
        self.current_atome = a
    @pyqtSlot()
    def clear_draw(self):
        self.scene.clear()
    def set_curent_liaison(self, l):
        self.current_liaison = l
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pt = QPointF(self.mapToScene(event.pos()))
            print(self.position_preced, pt)
            if self.position_preced:
                self.scene.addLine(QLineF(pt, self.position_preced))
            if self.current_atome == 'H':
                t = QGraphicsTextItem('H')
                t.setPos(pt)
                self.scene.addItem(t)
            elif self.current_atome == 'O':
                t = QGraphicsTextItem('O')
                t.setPos(pt)
                self.scene.addItem(t)
            elif self.current_atome == 'N':
                t = self.scene.addText('N')
                t.setPos(pt)
                self.scene.addItem(t)
            elif self.current_atome == 'C':
                t = QGraphicsTextItem('C')
                t.setPos(pt)
                self.scene.addItem(t)


            self.position_preced = pt

            self.centerOn(event.pos().x(),event.pos().y())



class MoleculeEdit(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.first = None
        self.setHeaderLabels(["Atome", "", "Liaison à créer", "Atome à créer", ""])
    def buildMolecule(self):
        return Molecule(*self.first.getAndLinkAtome())

class AtomeItem(QTreeWidgetItem):
    def __init__(self, atome, molecule, liaison=None):
        super().__init__()
        self.atome = atome()
        self.childs = []
        self.setText(0, self.atome.nom)
        self.molecule = molecule

        if liaison == 0:
            self.setIcon(0, QIcon(QPixmap("simple.png")))
        elif liaison == 1:
            self.setIcon(0, QIcon(QPixmap("double.png")))

        self.delete = QPushButton(QIcon(QPixmap("list-remove.svg")), "")
        self.btn = QPushButton(QIcon(QPixmap("list-add.svg")),"")
        self.liaison = QComboBox()
        self.liaison.addItem("Simple")
        self.liaison.addItem("Double")

        self.nature = QComboBox()
        self.nature.addItem("C")
        self.nature.addItem("H")
        self.nature.addItem("O")
        self.nature.addItem("N")
    def createEditor(self):
        self.molecule.setItemWidget(self, 4, self.btn)
        self.molecule.setItemWidget(self, 2, self.liaison)
        self.molecule.setItemWidget(self, 3, self.nature)
        self.molecule.setItemWidget(self, 1, self.delete)
    def addChild(self, c):
        self.childs.append(c)
        super().addChild(c)
    def getAndLinkAtome(self):
        if len(self.childs) == 0:
            return self.atome
        else:
            voisins = []
            for i in self.childs:
                voisins = i.getAndLinkAtome() + voisins
                self.atome.link(voisins[0])
            return [self.atome] + voisins


class TextInput(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)

        self.button = QPushButton('Valider', self)
        self.input = QLineEdit(self)

        self.layout.addWidget(self.input)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)
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

        self.layout_text.addRow('Formule brute :',self.input_brute)
        self.layout_text.addRow('Formule nomenclature :', self.input_nomenc)
        self.input_nomenc.setText("méthanamide")

        self.layout.addLayout(self.layout_text)
        self.setLayout(self.layout)

if __name__ == '__main__':
    app=QApplication(sys.argv)
    t = Fenetre()
    t.show()
    sys.exit(app.exec_())