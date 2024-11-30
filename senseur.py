import numpy as np
import matplotlib.pyplot as plt
def init_probabilities(N, mode="edges"):
    """
    Initialise les probabilités a priori pour chaque case de la grille.
    Mode "uniform" : probabilité uniforme sur toutes les cases.
    Mode "center" : probabilité plus élevée au centre de la grille.
    Mode "edges" : probabilité plus élevée sur les bords.
    """
    if mode == "uniform":
        return np.ones(N) / N
    elif mode == "center":
        x = np.arange(1, N + 1)
        center = (N + 1) / 2
        prob = 1 / (1 + np.abs(x - center))
        return prob / np.sum(prob)  # normalisation
    elif mode == "edges":
        prob = np.zeros(N)
        for i in range(N):
            if i < N * 0.25 or i > N * 0.75:
                prob[i] = 2  # bords
            else:
                prob[i] = 1  # milieu
        return prob / np.sum(prob)  # normalisation
    else:
        raise ValueError("Mode inconnu")

def update_probabilities(pi, k, ps):
    """
    Met à jour les probabilités après avoir sondé la case k avec un échec (Z_k = 0).
    """
    # Probabilité totale de non-détection dans la case k
    P_Zk_0 = (1 - ps) * pi[k] + (1 - pi[k])
    
    # Mise à jour de la probabilité pour la case sondée (k)
    pi[k] = (1 - ps) * pi[k] / P_Zk_0
    
    # Mise à jour des probabilités pour les autres cases
    for i in range(len(pi)):
        if i != k:
            pi[i] = pi[i] / P_Zk_0

def search_object(N, ps, max_iterations=100, mode="uniform"):
    """
    Algorithme de recherche d'objet perdu sur une grille de N cases.
    ps : probabilité de détection du capteur.
    max_iterations : nombre maximal de sondages.
    """
    # Initialisation des probabilités a priori
    pi = init_probabilities(N, mode)
    
    # Choisir aléatoirement la case où se trouve l'objet
    true_position = np.random.randint(0, N)
    
    print(f"L'objet est dans la case {true_position} (caché)")
    
    # Recherche
    for t in range(max_iterations):
        # Sélectionner la case avec la plus grande probabilité
        k = np.argmax(pi)
        
        print(f"Sondage de la case {k} avec probabilité a priori {pi[k]:.4f}")
        
        # Simuler la détection
        if k == true_position:
            if np.random.rand() < ps:
                print(f"Objet trouvé en case {k} après {t+1} sondages.")
                return k, t+1
            else:
                print(f"Échec de détection en case {k}. Mise à jour des probabilités...")
        else:
            print(f"L'objet n'est pas en case {k}. Mise à jour des probabilités...")
        
        # Mise à jour des probabilités après échec
        update_probabilities(pi, k, ps)
    
    print(f"Objet non trouvé après {max_iterations} sondages.")
    return None, max_iterations

# Paramètres
N = 100  # Nombre de cases
ps = 0.6  # Probabilité de détection du capteur
max_iterations = 50  # Nombre maximal de sondages

# Exécution de l'algorithme avec une distribution uniforme
found_position, iterations = search_object(N, ps, max_iterations, mode="uniform")

def simulate_searches(N, ps, max_iterations, mode, num_simulations):
    results = []
    for _ in range(num_simulations):
        found_position, iterations = search_object(N, ps, max_iterations, mode)
        results.append(iterations)
    return results

def plot_distributions(N, ps, max_iterations, num_simulations):
    modes = ["uniform", "center", "edges"]
    plt.figure(figsize=(10, 6))
    
    for mode in modes:
        results = simulate_searches(N, ps, max_iterations, mode, num_simulations)
        plt.hist(results, bins=range(max_iterations), alpha=0.5, label=mode)
    
    plt.title("Distribution des itérations pour chaque mode")
    plt.xlabel("Nombre d'itérations")
    plt.ylabel("Fréquence")
    plt.legend()
    plt.grid(True)
    plt.show()


num_simulations = 1000  # Nombre de simulations pour chaque mode

# Générer les graphiques
plot_distributions(N, ps, max_iterations, num_simulations)
