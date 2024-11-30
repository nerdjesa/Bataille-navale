import numpy as np
import matplotlib.pyplot as plt


# Dictionnaire des tailles de bateaux
bateaux_taille = {1: 5, 2: 4, 3: 3, 4: 3, 5: 2}

# Classe représentant un bateau
class Bateau:
    def __init__(self, id_):
        self.id_ = id_
        self.taille = bateaux_taille[id_]
    def nb_placement(self):
        return 2*10*(10-self.taille+1)
# Classe représentant la grille
class Grille:
    def __init__(self):
        self.longueur = 10
        self.largeur = 10
        self.grille = np.zeros((10, 10))

    # Vérifie si un bateau peut être placé à une position donnée
    def peut_placer(self, bateau, position, direction):
        l, c = position
        if direction == 2:  # Vertical
            if l + bateau.taille > self.longueur:
                return False
            for i in range(l, l + bateau.taille):
                if self.grille[i][c] != 0:
                    return False
        elif direction == 1:  # Horizontal
            if c + bateau.taille > self.largeur:
                return False
            for i in range(c, c + bateau.taille):
                if self.grille[l][i] != 0:
                    return False
        return True

    # Place un bateau dans la grille
    def place(self, bateau, position, direction):
        l, c = position
        if self.peut_placer(bateau, position, direction):
            if direction == 2:  # Vertical
                for i in range(l, l + bateau.taille):
                    self.grille[i][c] = bateau.id_
            elif direction == 1:  # Horizontal
                for i in range(c, c + bateau.taille):
                    self.grille[l][i] = bateau.id_
        return self.grille

    # Place un bateau aléatoirement
    def place_alea(self, bateau):
        placed = False
        while not placed:
            l, c = np.random.randint(0, self.longueur), np.random.randint(0, self.largeur)
            direction = np.random.randint(1, 3)  # 1: horizontal, 2: vertical
            if self.peut_placer(bateau, (l, c), direction):
                self.place(bateau, (l, c), direction)
                placed = True

    # Retire un bateau de la grille
    def retire_bateau(self, bateau, position, direction):
        l, c = position
        if direction == 2:  # Vertical
            for i in range(l, l + bateau.taille):
                self.grille[i][c] = 0
        elif direction == 1:  # Horizontal
            for i in range(c, c + bateau.taille):
                self.grille[l][i] = 0


    # Affiche la grille
    def affiche(self):
        plt.imshow(self.grille, cmap='Blues', interpolation='none')
        plt.show()

    # Compare deux grilles
    def eq(self, grilleB):
        return np.array_equal(self.grille, grilleB.grille)

    



# Compte le nombre de placement d'une liste de bateaux
def nb_placement_liste(grille_obj, liste_bateaux):
    if len(liste_bateaux) == 0:
        return 1  # Cas de base : plus de bateaux à placer

    nb_possible = 0
    bateau = liste_bateaux[0]
    
    for ligne in range(grille_obj.longueur):
        for colonne in range(grille_obj.largeur):
            for direction in [1, 2]:  # 1 = Horizontal, 2 = Vertical
                if grille_obj.peut_placer(bateau, (ligne, colonne), direction):
                    # Placer le bateau
                    grille_obj.place(bateau, (ligne, colonne), direction)
                    
                    # Récursion sur le reste de la liste
                    nb_possible += nb_placement_liste(grille_obj, liste_bateaux[1:])
                    
                    # Retirer le bateau pour essayer d'autres positions
                    grille_obj.retire_bateau(bateau, (ligne, colonne), direction)
    
    return nb_possible

# Génère une grille avec des bateaux placés aléatoirement
def genere_grille():
    grille = Grille()
    for id_ in bateaux_taille.keys():
        bateau = Bateau(id_)
        grille.place_alea(bateau)
    return grille
#avec la liste complète 
def nb_grilles_genere(grille_cible):
    grille_actuelle = genere_grille()
    nb_grilles_generes = 1

    while not grille_cible.eq(grille_actuelle):
        grille_actuelle = genere_grille()  # Génère une nouvelle grille aléatoirement avec la liste complète 
        nb_grilles_generes += 1
    return nb_grilles_generes


# Génère une grille avec des bateaux placés aléatoirement en donnant une liste avec moins de 5 bateaux 
def genere_grille2(liste_bateaux):
    grille = Grille()
    for b in liste_bateaux:
        grille.place_alea(b)
    return grille


#en considérant pour la loi géométrique p=1/n  les événements équiprobables
def nb_grilles_genere2(grille_cible,liste_bateaux):
    grille_actuelle = genere_grille2(liste_bateaux)
    nb_grilles_generes = 1

    while not grille_cible.eq(grille_actuelle):
        grille_actuelle = genere_grille2(liste_bateaux)  # Génère une nouvelle grille aléatoirement
        nb_grilles_generes += 1

    return nb_grilles_generes

def estimer_esperance(nb_simulations,cible,liste_bateaux):
    nb_grilles_total=0 
    for _ in range(nb_simulations):
        nb_grilles_generees = nb_grilles_genere2(cible,liste_bateaux)
        nb_grilles_total += nb_grilles_generees
    return nb_grilles_total / nb_simulations
