from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMessageBox

# ── état interne ──────────────────────────────────────────────────────────────
saisie    = ""
operateur = ""
premier   = None
nouveau   = True


def afficher(valeur):
    try:
        w.resultat.display(float(valeur))
    except Exception:
        w.resultat.display(0)


# ── chiffres ──────────────────────────────────────────────────────────────────
def chiffre(c):
    global saisie, nouveau
    if nouveau:
        saisie = ""
        nouveau = False
    if c == "." and "." in saisie:
        return
    saisie += c
    afficher(saisie)


# ── opérateurs ────────────────────────────────────────────────────────────────
def operation(op):
    global operateur, premier, saisie, nouveau
    try:
        premier = float(saisie) if saisie else 0.0
    except ValueError:
        premier = 0.0
    operateur = op
    nouveau = True


# ── égal (bouton "entrée") ────────────────────────────────────────────────────
def Calculer():
    global saisie, operateur, premier, nouveau
    if operateur == "" or premier is None:
        return
    try:
        second = float(saisie) if saisie else 0.0
        if   operateur == "+": res = premier + second
        elif operateur == "-": res = premier - second
        elif operateur == "*": res = premier * second
        elif operateur == "/":
            if second == 0:
                QMessageBox.warning(w, "Erreur", "Division par zéro !")
                saisie = ""; operateur = ""; premier = None; nouveau = True
                w.resultat.display(0)
                return
            res = premier / second
        else:
            return

        saisie = str(int(res)) if res == int(res) else str(round(res, 10))
        afficher(saisie)
        operateur = ""
        premier   = None
        nouveau   = True

    except Exception as e:
        QMessageBox.critical(w, "Erreur", str(e))


# ── effacer ───────────────────────────────────────────────────────────────────
def Effacer():
    global saisie, operateur, premier, nouveau
    saisie    = ""
    operateur = ""
    premier   = None
    nouveau   = True
    w.resultat.display(0)   # remet le LCD à 0


# ── lancement ─────────────────────────────────────────────────────────────────
app = QApplication([])
w   = loadUi("Calculatrice.ui")
w.show()

# Chiffres
w.zero.clicked.connect   (lambda: chiffre("0"))
w.un.clicked.connect     (lambda: chiffre("1"))
w.deux.clicked.connect   (lambda: chiffre("2"))
w.trois.clicked.connect  (lambda: chiffre("3"))
w.quatre.clicked.connect (lambda: chiffre("4"))
w.cinq.clicked.connect   (lambda: chiffre("5"))
w.six.clicked.connect    (lambda: chiffre("6"))
w.sept.clicked.connect   (lambda: chiffre("7"))
w.huit.clicked.connect   (lambda: chiffre("8"))
w.neuf.clicked.connect   (lambda: chiffre("9"))
w.virgule.clicked.connect(lambda: chiffre("."))

# Opérateurs  (les textes dans ton .ui : "+" "-" "*" "/")
w.plus.clicked.connect  (lambda: operation("+"))
w.moins.clicked.connect (lambda: operation("-"))
w.fois.clicked.connect  (lambda: operation("*"))
w.sur.clicked.connect   (lambda: operation("/"))

# Égal
w.entree.clicked.connect(Calculer)

# Effacer
w.effacer.clicked.connect(Effacer)

app.exec_()
