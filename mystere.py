import random
import sqlite3
from PyQt5.QtWidgets import QPushButton ,QWidget ,QLineEdit ,QLabel ,QApplication,QGridLayout, QMessageBox
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
conn=sqlite3.connect("questions.db")
curseur=conn.cursor()
global liste
liste=[]
global numero_question
numero_question=0


def melanger(mot):
 taille=len(mot)
 l=[]
 melange=""
 for i in range(taille):
  l.append(i)
 for i in range(taille):
  x=random.randrange(taille-i)
  melange+=mot[(l[x])]
  del l[x]
  i+=1
 return(melange)
  
def selection(num):
 curseur.execute("select mot from mots where numero= ?" ,(num,))
 res=(curseur.fetchone())[0]
 return(res)
def nombre_mots():
 
 curseur.execute("select * from mots")
 return(len(curseur.fetchall()))

class jeu(QWidget):
  def __init__(self,num):
     global numero_question
     numero_question+=1
     super().__init__()
     self.num=num 
     self.mot=selection(self.num)
     self.melange=melanger(self.mot)
     ch=""
     for i in range(len(self.mot)):
      ch+=(" - "+self.melange[i])
     self.text=QLabel("""Devinez la mot caché derriere 
     """+ch)
     self.ligne=QLineEdit()
     self.exp=QRegExp("[a-zA-Z]{1,}")
     self.validator=QRegExpValidator(self.exp)
     """    self.ligne.setValidator(self.validator)"""
     self.boutton=QPushButton("tester le mot")
     
     self.layout =QGridLayout()
     self.layout.addWidget(self.text,0,0)
     self.layout.addWidget(self.ligne,1,0)

     self.layout.addWidget(self.boutton,2,0)
     self.setLayout(self.layout)
     self.setFixedSize(300,300)
     self.boutton.clicked.connect(self.test)
  def showing(self):
    super().show()
  def test(self):
     pos=0
     res=(self.validator.validate(self.ligne.text(),pos))[0] 
     if(self.ligne.text()==""):
        QMessageBox.critical(self,"erreur","veuillez saisir un mot")
     elif(self.ligne.text()==self.mot):
       """  fermer la fenetre actuelle et ouvrir une autre
 self.jeu=jeu(6)
       self.jeu.showing()
       super().close()
       """
       self.message=QMessageBox(self)
       self.message.setText("bravo votre réponse est correcte")
       self.message.exec()
       super().close()
       global numero_question
       self. f=principale(numero_question)
       self. f.show()
     elif( res!=2):
        QMessageBox.critical(self,"erreur","veuillez saisir uniquement des lettres")
     elif(self.ligne.text()!=self.mot):
        QMessageBox.critical(self,"mystere","mot incorrect veuillez essayer une autre foix")

class principale(QWidget):
  def __init__(self,nb_questions):
    super().__init__()
    self.layout=QGridLayout()
    self.text=QLabel()
    self.boutton=QPushButton()
    if(nb_questions==0):
      self.text.setText("""Bonjour 
Pour lancer une partie cliquez sur le boutton suivant""") 
      self.boutton.setText("""Lancer une partie""")
    else:
      self.text.setText("""Felicitations vous avez trouve le mot
Pour lancer une autre partie 
cliquez sur le boutton suivant""")
      self.boutton.setText("Encore une partie ?")
    self.layout.addWidget(self.text,0,0)
    self.layout.addWidget(self.boutton,1,0,)
    self.setFixedSize(400,300)
    self.setLayout(self.layout)
    self.boutton.clicked.connect(self.lancer)
  def  lancer(self):
   num=random.randrange(nombre_mots())
   while num  in liste:
     num=random.randrange(nombre_mots())
   liste.append(num)
   self.jeu=jeu(num)
   self.jeu.showing()
   super().close()


app=QApplication([])
f=principale(0)
f.show()
app.exec()
