import grille1 as grille
import numpy as np
import matplotlib.pyplot as plt

class Bataille:
    def __init__(self):
        self.grille = grille.genere_grille()
        self.tirs = [] # Coups victorieux
        self.coups_joues =[] # Coups joués 
        self.coups_joues_grille =np.zeros((10, 10)) # Coups positionnés sur la grille
        self.bateaux_restants = grille.bateaux_taille.copy()  # Liste des bateaux avec le nombres de cases restantes pour qu'ils coulent
    def joue(self, position):
        (l, c) = position
        if (l, c) in self.coups_joues:
            return False  # Empêche de rejouer la même case

        self.coups_joues.append(position)
        bateau = self.grille.grille[l][c]  # Récupère l'identifiant du bateau à cette position
        
        if bateau > 0:  # Si un bateau est présent sur la case
            
            self.tirs.append(position) # Mise à jour correcte des tirs 
            self.bateaux_restants[bateau] -= 1  # Mise à jour correcte des cases restantes du bateau
            self.grille.grille[l][c] = 0  # Marque la case comme touchée sur la grille 

            if self.bateaux_restants[bateau] == 0:
                self.coups_joues_grille[l][c] = -2
                return "coulé" 
            else:
                self.coups_joues_grille[l][c] = -1
                return "touché"
        else:
            self.coups_joues_grille[l][c] = 1
            return "vide"  

    def victoire(self):
        # Vérifie si tous les bateaux ont été coulés
        return sum(self.bateaux_restants.values()) == 0

    def reset(self):
        # Réinitialise la partie
        self.__init__()

class Joueur_s_aleatoire:
    def __init__(self):
        self.bataille=Bataille()
    # fonction qui joue aleatoirement au jeu
    def jouer(self):
        while not self.bataille.victoire():
            ligne, colonne = np.random.randint(0, 10), np.random.randint(0, 10)
            self.bataille.joue((ligne, colonne))
        return len(self.bataille.coups_joues)
    
# En considérant tous les événements équiprobables
# Nombre de coups possibles
n_coups = 100 - 17 + 1  # de 17 à 100, inclus

# Probabilité pour chaque nombre de coups
probabilite = 1 / n_coups

# Somme des nombres de coups
somme_coups = sum(range(17, 101))

# Espérance
esperance = probabilite * somme_coups
print(f"Espérance théorique (aléatoire): {esperance}")


def estimer_esperance(nb_simulations,classe):
    total_coups = 0
    for _ in range(nb_simulations):
        joueur = classe()
        total_coups += joueur.jouer()
    return total_coups / nb_simulations

# Simuler plusieurs parties et enregistrer le nombre de coups nécessaires
def simuler_parties(nb_simulations, Joueur_class):
    coups_necessaires = []
    for _ in range(nb_simulations):
        joueur = Joueur_class()
        coups = joueur.jouer()
        coups_necessaires.append(coups)
    return coups_necessaires

class Joueur_s_heuristique:
    def __init__(self):
        self.bataille = Bataille()
       
    def jouer(self):
        while not self.bataille.victoire():
            tirs = self.bataille.tirs
            coups = self.bataille.coups_joues
            if tirs :
                dernier_tir = tirs[-1]
                voisins = []

                # Générer les voisins valides (dans les limites de la grille et non joués)
                for d in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    voisin = (dernier_tir[0] + d[0], dernier_tir[1] + d[1])
                    if 0 <= voisin[0] < 10 and 0 <= voisin[1] < 10 and voisin not in coups:
                        voisins.append(voisin)

                if voisins:
                    for cible in voisins:
                        self.bataille.joue(cible)       
                else:
                    # Si aucun voisin valide, tirer aléatoirement
                    ligne, colonne = np.random.randint(0, 10), np.random.randint(0, 10)
                    self.bataille.joue((ligne, colonne))

                tirs.pop()
            else:
                # Tir aléatoire si aucun tir précédent ou le dernier coup n'était pas touché
                ligne, colonne = np.random.randint(0, 10), np.random.randint(0, 10)
                self.bataille.joue((ligne, colonne))

        return len(self.bataille.coups_joues)
    
class Joueur_s_heuristique2:
    def __init__(self):
        self.bataille = Bataille()    
    def jouer(self):
        while not self.bataille.victoire():
            tirs = self.bataille.tirs
            coups = self.bataille.coups_joues

            if tirs and (tirs[-1] == coups[-1]):
                dernier_tir = tirs[-1]
                voisins = []

                # Générer les voisins valides (dans les limites de la grille et non joués)
                for d in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    voisin = (dernier_tir[0] + d[0], dernier_tir[1] + d[1])
                    if 0 <= voisin[0] < 10 and 0 <= voisin[1] < 10 and voisin not in coups:
                        voisins.append(voisin)

                if voisins:
                    # Choisir un voisin aléatoire parmi les valides
                    cible = voisins[np.random.randint(0, len(voisins))]
                    joue = self.bataille.joue(cible)

                    # Si le coup est vide, ne plus considérer cette case
                    while (joue == "vide" or joue == False) and voisins:
                        voisins.remove(cible)
                        if voisins:
                            cible = voisins[np.random.randint(0, len(voisins))]
                            joue = self.bataille.joue(cible)
                else:
                    # Si aucun voisin valide, tirer aléatoirement
                    ligne, colonne = np.random.randint(0, 10), np.random.randint(0, 10)
                    self.bataille.joue((ligne, colonne))
            else:
                # Tir aléatoire si aucun tir précédent ou le dernier coup n'était pas touché
                ligne, colonne = np.random.randint(0, 10), np.random.randint(0, 10)
                self.bataille.joue((ligne, colonne))

        return len(self.bataille.coups_joues)
    
class Joueur_s_probabiliste:
    def __init__(self):
        self.bataille = Bataille()

    def calculer_probabilites(self):
        probabilites = np.zeros((10, 10))  # Grille de probabilités
        
        for bateau_id, cases_restantes in self.bataille.bateaux_restants.items():
            if cases_restantes > 0:  # Si le bateau est encore présent
                    for l in range(10):
                        for c in range(10):
                            g=self.bataille.coups_joues_grille
                            taille=grille.bateaux_taille[bateau_id]

                            # Vérifier si le bateau peut être placé horizentalement
                            if c + taille <= 10:
                                # Vérifier les cases: 

                                # Cas 1 : cases qu'on n'a pas encore exploré que des 0
                                if all(g[l][c + i] == 0  for i in range(taille)) :
                                    for i in range(taille) :
                                        probabilites[l][c + i] += 1

                                # Cas 2 : cases non vides et non coulées ayant au moins une case touché 
                                if not (any(g[l][c + i] == -2 for i in range(taille)) or any(g[l][c + i] == 1 for i in range(taille))) :
                                    for i in range(taille) :
                                        if g[l][c + i] == 0 :
                                            probabilites[l][c + i] += 1

                            # Vérifier si le bateau peut être placé verticalement
                            if l + taille <= 10:
                                if all(g[l + i][c] == 0 for i in range(taille)) :
                                        for i in range(taille) :
                                            probabilites[l + i][c] += 1  
                            
                                if not (any(g[l + i][c] == -2  for i in range(taille)) or any(g[l + i][c] == 1  for i in range(taille)) ):
                                    for i in range(taille) :
                                        if g[l+i][c] == 0 :
                                            probabilites[l + i][c] += 1
                            
        return probabilites

    def jouer(self):
        while not self.bataille.victoire():
            probabilites = self.calculer_probabilites()
            # Choisir la case avec la probabilité maximale
            l, c = np.unravel_index(np.argmax(probabilites), probabilites.shape)
            self.bataille.joue((l, c))
        return len(self.bataille.coups_joues)
      

print(f"Espérance pratique alea: {estimer_esperance(1000,Joueur_s_aleatoire)}")  

print(f"Espérance pratique heuristique: {estimer_esperance(1000,Joueur_s_heuristique)}")  

print(f"Espérance pratique heuristique 2: {estimer_esperance(1000,Joueur_s_heuristique2)}")

print(f"Espérance pratique probabiliste : {estimer_esperance(1000,Joueur_s_probabiliste)}")  



# Nombre de simulations
nb_simulations = 1000
coups_aleatoire = simuler_parties(nb_simulations, Joueur_s_aleatoire)
coups_heuristique = simuler_parties(nb_simulations, Joueur_s_heuristique)
coups_heuristique2 = simuler_parties(nb_simulations, Joueur_s_heuristique2)
coups_probabiliste = simuler_parties(nb_simulations, Joueur_s_probabiliste)



# Tracer les histogrammes
plt.figure(figsize=(14, 6))

plt.subplot(1, 4, 1)
plt.hist(coups_aleatoire, bins=range(min(coups_aleatoire), max(coups_aleatoire) + 1), density=True, alpha=0.75, color='blue')
plt.xlabel('Nombre de coups nécessaires (aléatoire)')
plt.ylabel('Fréquence relative')
plt.title('Distribution du nombre de coups (Aléatoire)')

plt.subplot(1, 4, 2)
plt.hist(coups_heuristique, bins=range(min(coups_heuristique), max(coups_heuristique) + 1), density=True, alpha=0.75, color='green')
plt.xlabel('Nombre de coups nécessaires (heuristique)')
plt.ylabel('Fréquence relative')
plt.title('Distribution du nombre de coups (Heuristique)')

plt.subplot(1, 4, 3)
plt.hist(coups_heuristique2, bins=range(min(coups_heuristique2), max(coups_heuristique2) + 1), density=True, alpha=0.75, color='red')
plt.xlabel('Nombre de coups nécessaires (heuristique 2)')
plt.ylabel('Fréquence relative')
plt.title('Distribution du nombre de coups (Heuristique 2)')

plt.subplot(1, 4, 4)
plt.hist(coups_probabiliste, bins=range(min(coups_probabiliste), max(coups_probabiliste) + 1), density=True, alpha=0.75, color='yellow')
plt.xlabel('Nombre de coups nécessaires (probabiliste)')
plt.ylabel('Fréquence relative')
plt.title('Distribution du nombre de coups (probabiliste)')


plt.tight_layout()
plt.show()

