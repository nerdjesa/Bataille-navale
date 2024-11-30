import grille1 as grille
from grille1 import estimer_esperance

# ----------------------
# TESTS DES FONCTIONS
# ----------------------

# Test de l'initialisation d'un bateau
bateau_test = grille.Bateau(1)
print(f"Bateau ID: {bateau_test.id_}, Taille: {bateau_test.taille}")  # Doit afficher "Bateau ID: 1, Taille: 5"

# Test de l'initialisation de la grille
grille_test = grille.Grille()
print("Grille vide initialisée :")
print(grille_test.grille)  # Doit afficher une grille 10x10 de zéros

# Test de placement d'un bateau horizontalement
print("\nTest de placement horizontal (bateau de taille 4 en (0,0)) :")
grille_test.place(grille.Bateau(2), (0, 0), 1)  # Horizontal
print(grille_test.grille)

# Test de placement d'un bateau verticalement
print("\nTest de placement vertical (bateau de taille 3 en (2,2)) :")
grille_test.place(grille.Bateau(3), (2, 2), 2)  # Vertical
print(grille_test.grille)

# Test de génération aléatoire de la grille
print("\nGénération d'une grille avec des placements aléatoires :")
grille_alea = grille.genere_grille()
grille_alea.affiche()  # Doit afficher la grille avec des bateaux aléatoirement placés

# Test de calcul de nombre de placements pour un bateau donné dans une grille
print("\nTest de calcul de nombre de placement:")
bateau_test1 = grille.Bateau(1)
print(f"Bateau ID: {bateau_test1.id_}, Taille: {bateau_test1.taille}")  
print(f"Nombre de placement possible pour le bateau 1: {bateau_test1.nb_placement()}")

#Test de calcule de nombre de placement d'une liste de bateaux
new1=grille.Grille()
new2=grille.Grille()
new3=grille.Grille()

liste_bateau1=[grille.Bateau(1)]
liste_bateau2=[grille.Bateau(3),grille.Bateau(4)]
liste_bateau3=[grille.Bateau(1),grille.Bateau(5),grille.Bateau(3)]
print(f"Nombre de placement possible pour la liste 1 (contenant que le bateau 1): {grille.nb_placement_liste(new1,liste_bateau1)}")
print(f"Nombre de placement possible pour la liste 2 : {grille.nb_placement_liste(new2,liste_bateau2)}")
print(f"Nombre de placement possible pour la liste 3: {grille.nb_placement_liste(new3,liste_bateau3)}")



# Test de la fonction pour le nombre de grille généré
grille_test1 = grille.genere_grille2(liste_bateau1)
# On calcule le nombre de grilles générées jusqu'à retrouver la grille cible
nb_grilles_ap1 = grille.nb_grilles_genere2(grille_test1,liste_bateau1)
print(f"Nombre de grilles générées jusqu'à retrouver la grille cible 1 : {nb_grilles_ap1}")

grille_test2 = grille.genere_grille2(liste_bateau2)
nb_grilles_ap2 = grille.nb_grilles_genere2(grille_test2,liste_bateau2)
print(f"Nombre de grilles générées jusqu'à retrouver la grille cible 2 : {nb_grilles_ap2}")

nb_simulations=50
print(f"Nombre de placement possible approximé pour la liste 1: {estimer_esperance(nb_simulations,grille_test1,liste_bateau1)}")
print(f"Nombre de placement possible approximé pour la liste 2 : {estimer_esperance(nb_simulations,grille_test2,liste_bateau2)}")


