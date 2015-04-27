# Créé par levyfalk, le 16/03/2015 en Python 3.2
#!/usr/bin/python
# -*- coding: utf-8 -*-

# par X. HINAULT - Mai 2013 - Tous droits réservés
# GPLv3 - www.mon-club-elec.fr

# modules a importer
from PyQt4.QtGui import *
from PyQt4.QtCore import *  # inclut QTimer..
import os,sys

from inter import * # fichier obtenu à partir QtDesigner et pyuic4

# +/- variables et objets globaux

class myApp(QWidget, Ui_Form): # la classe reçoit le Qwidget principal ET la classe définie dans test.py obtenu avec pyuic4
        def __init__(self, parent=None):
                QWidget.__init__(self) # initialise le Qwidget principal
                self.setupUi(parent) # Obligatoire

                # --- Variables de classe

                # --- Paramétrage des widgets de l'interface GUI si nécessaire ---

                # --- Connexions entre signaux des widgets et fonctions
                # connecte chaque signal utilisé des objets à l'appel de la fonction voulue

                self.connect(self.pushButtonEffacer, SIGNAL("clicked()"), self.pushButtonEffacerClicked)

                # --- Code actif initial  ---


                # Dessin avec QPixmap (affichage) et QImage (I/O, accès pixels)

                # création d'un QImage permettant l'accès aux pixels
                self.image=QImage(self.labelImage.size(),QImage.Format_RGB32) # crée image RGB 32 bits même taille que label

                #-- initialisation du QImage
                self.image.fill(QColor(255,255,255)) # fond blanc

                #-- Initialisation du QPixmap
                self.pixmap=QPixmap.fromImage(self.image) # initialise  le QPixmap...

                self.updatePixmap()

                #----- initialisation capture évènement souris du Qlabel
                self.labelImage.setMouseTracking(True) # active le suivi position souris
                self.labelImage.installEventFilter(self) # défini un objet dans cette classe pour "filtrer" les évènements en provenance de l'objet label - méthode classe Object

        # --- les fonctions appelées, utilisées par les signaux des widgets ---

        # pushButton
        def pushButtonEffacerClicked(self):
                print("Bouton Effacer cliqué")
                #-- initialisation du QImage
                self.image.fill(QColor(255,255,255)) # fond blanc
                self.updatePixmap()

        # --- les fonctions appelées, utilisées par les signaux hors widgets ---

        # fonction pour gérer filtrage évènements
        #def eventFilter(self, _, event): # fonction pour gérer filtrage évènements
        def eventFilter(self, srcEvent, event): # fonction pour gérer filtrage évènements - reçoit l'objet source de l'évènement
                print ("event ")
                #print srcEvent

                if srcEvent==self.labelImage: # teste si la source de l'évènement est bien le label - utile si plusieurs sources d'évènements activées
                        if event.type() == QEvent.MouseMove: # si évènement "mouvement de la souris"
                                x=event.pos().x() # coordonnée souris au moment évènement dans le widget source de l'évènement =
                                y=event.pos().y()
                                print ("MouseMove : x="+ str(x) + " y= " + str(y)) # affiche coordonnées


                                if event.buttons()==Qt.LeftButton: # ici on teste event.buttons (avec un s) qui renvoie état des boutons au moment de l'évènement
                                # event.buttons() est différent de event.button qui renvoie bouton déclencheur de l'événement ++
                                        self.drawLineImage(self.xo, self.yo, event.pos().x(), event.pos().y(), QColor(0,0,255)) # appelle fonction locale de classe tracé d'un pixel
                                        self.updatePixmap() # met à jour le pixmap

                                        self.xo=event.pos().x() # mémorise valeur nouveau point
                                        self.yo=event.pos().y()

                                elif event.buttons()==Qt.RightButton: # ici on teste event.buttons (avec un s) qui renvoie état des boutons au moment de l'évènement
                                # event.buttons() est différent de event.button qui renvoie bouton déclencheur de l'événement ++
                                        self.drawLineImage(self.xo, self.yo, event.pos().x(), event.pos().y(), QColor(255,0,0)) # appelle fonction locale de classe tracé d'un pixel
                                        self.updatePixmap() # met à jour le pixmap

                                        self.xo=event.pos().x() # mémorise valeur nouveau point
                                        self.yo=event.pos().y()


                        elif event.type()==QEvent.MouseButtonPress: # si évènement "bouton souris appuyé"
                                if event.button()==Qt.RightButton: # Qt.RightButton est une constante désignant bouton droit
                                        #print "Bouton droit : "
                                        self.drawPixelImage(event.pos().x(), event.pos().y(), QColor(255,0,0)) # rouge
                                        self.updatePixmap() # met à jour le pixmap

                                        self.xo=event.pos().x() # mémorise valeur nouveau point
                                        self.yo=event.pos().y()

                                elif event.button()==Qt.LeftButton:
                                        #print "Bouton gauche : "
                                        self.drawPixelImage(event.pos().x(), event.pos().y(), QColor(0,0,255)) # bleu
                                        self.updatePixmap() # met à jour le pixmap

                                        self.xo=event.pos().x() # mémorise valeur nouveau point
                                        self.yo=event.pos().y()

                                print ("x="+str(event.pos().x())+" y="+str(event.pos().y())) # affiche position


                        # pour la liste des QEvent : voir : http://pyqt.sourceforge.net/Docs/PyQt4/qevent.html
                        # Notamment :
                        #QEvent.MouseButtonDblClick     4       Mouse press again (QMouseEvent).
                        #QEvent.MouseButtonPress                2       Mouse press (QMouseEvent).
                        #QEvent.MouseButtonRelease              3       Mouse release (QMouseEvent).
                        #QEvent.MouseMove                               5       Mouse move (QMouseEvent).
                        #QEvent.MouseTrackingChange             109 The mouse tracking state has changed.

                return False # obligatoire...

        # --- fonctions de classes autres---

        # fonction de MAJ du QPixmap : chargement QImage +/- dessin + affichage dans QLabel
        def updatePixmap(self):

                # chargement du QImage dans le QPixmap
                self.pixmap.convertFromImage(self.image) # recharge le QImage dans le QPixmap existant - met à jour le QPixmap

                #-- affichage du QPixmap dans QLabel
                self.labelImage.setPixmap(self.pixmap) # met à jour le qpixmap affiché dans le qlabel

        def drawPixelImage(self, xIn, yIn, colorIn):

                #--- dessin sur QImage --
                self.painterImage=QPainter(self.image) # associe QPainter (classe de dessin) au Qimage

                self.painterImage.setPen(QPen(colorIn,1)) # fixe la couleur du crayon et la largeur pour le dessin - forme compactée
                self.painterImage.drawPoint(xIn,yIn) # trace un point drawPoint (self, int x, int y)

                # il existe d'autres possibilités de dessin (polygone, chemin, etc..) voir : http://pyqt.sourceforge.net/Docs/PyQt4/qpainter.html

                self.painterImage.end() # ferme le painter - n'est plus accessible après

                # -- fin dessin sur QImage

        def drawLineImage(self, xoIn, yoIn,xIn, yIn, colorIn):

                #--- dessin sur QImage --
                self.painterImage=QPainter(self.image) # associe QPainter (classe de dessin) au Qimage

                self.painterImage.setPen(QPen(colorIn,1)) # fixe la couleur du crayon et la largeur pour le dessin - forme compactée
                self.painterImage.drawLine(xoIn, yoIn, xIn,yIn) # trace un point drawPoint (self, int x, int y)

                # il existe d'autres possibilités de dessin (polygone, chemin, etc..) voir : http://pyqt.sourceforge.net/Docs/PyQt4/qpainter.html

                self.painterImage.end() # ferme le painter - n'est plus accessible après

                # -- fin dessin sur QImage
# -- Autres Classes utiles --

# -- Classe principale (lancement)  --
def main(args):
        a=QApplication(args) # crée l'objet application
        f=QWidget() # crée le QWidget racine
        c=myApp(f) # appelle la classe contenant le code de l'application
        f.show() # affiche la fenêtre QWidget
        r=a.exec_() # lance l'exécution de l'application
        return r

if __name__=="__main__": # pour rendre le code exécutable
        main(sys.argv) # appelle la fonction main
