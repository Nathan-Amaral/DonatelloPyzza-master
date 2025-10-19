# 🍕🐢 DonatelloPyzza – Agent Q-Learning Intelligent

## 🎯 Objectif

Ce projet met en œuvre un **agent d’apprentissage par renforcement (Q-Learning)** capable d’apprendre à naviguer dans un **labyrinthe généré automatiquement** pour atteindre une **pizza** 🍕.  
L’environnement est géré par la bibliothèque `donatellopyzza`, qui fournit :
- des environnements de labyrinthe,
- une tortue (agent) capable d’exécuter des actions,
- et un système de feedback pour guider l’apprentissage.

---

## 🧠 Principe du Q-Learning

Le **Q-Learning** est une méthode d’apprentissage par renforcement **hors politique**.  
L’agent apprend à associer à chaque état et action une valeur de qualité (*Q-value*), mise à jour à chaque étape selon l’équation de Bellman :

```
Q(s, a) ← Q(s, a) + α × [r + γ × max_a Q(s', a') − Q(s, a)]
```

- **s** : état actuel  
- **a** : action effectuée  
- **r** : récompense reçue  
- **s'** : état suivant  
- **α** : taux d’apprentissage  
- **γ** : facteur de réduction (discount factor)

L’agent explore aléatoirement au début (ε-greedy), puis apprend progressivement la meilleure stratégie pour atteindre la pizza.

---

## 🏗️ Structure du projet

```
donatellopyzza_qlearning/
│
├── generate_maze.py        # Code principal de l’agent Q-Learning
├── README.md                 # Documentation (ce fichier)
├── requirements.txt          # Dépendances Python
└── environments/             # Environnements de test (.maze, .json, etc.)
```

---

## ⚙️ Installation

### 1. Cloner le dépôt
```bash
git clone https://github.com/Nathan-Amaral/DonatelloPyzza-master.git
cd DonatelloPyzza-master
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate      # Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

**Exemple de contenu de `requirements.txt` :**
```
pygame
donatellopyzza
```

---

## 🚀 Utilisation

### 🧩 Exécution simple
Lance l’entraînement de l’agent sur un environnement de test :
```bash
python generate_maze.py
```

### ⚙️ Personnalisation
Tu peux modifier les paramètres directement dans la fonction `train_agent()` :
```python
agent = train_agent(
    environment_name="test",   # Nom du labyrinthe
    max_episodes=50,           # Nombre d'épisodes d'entraînement
    show_gui=True              # Afficher ou non la GUI pygame
)
```

---

## 🔍 Détails techniques

### États
Un état est défini par :
- la **position** (x, y),
- l’**orientation** (0 à 3),
- le **dernier feedback** (mur, pizza, vide…).

Exemple d’état :
```
pos_5_7_ori_1_wall
```

### Actions possibles
L’agent peut :
- 🟩 `MOVE_FORWARD` → avancer d’une case  
- 🔄 `TURN_LEFT` → tourner à gauche  
- 🔁 `TURN_RIGHT` → tourner à droite  
- ✋ `TOUCH` → vérifier la présence d’un obstacle ou de la pizza  

### Récompenses

| 🧾 Événement              | 💰 Récompense | 🧩 Description |
|---------------------------|---------------|----------------|
| 🍕 Pizza trouvée          | +100          | Objectif principal |
| 👃 Pizza détectée         | +50           | Proximité du but |
| 💥 Collision              | -15           | Heurter un mur |
| 🚧 Toucher un mur         | -8            | Pénalité mineure |
| 🗺️ Nouvelle case explorée | +8            | Bonus d’exploration |
| ⏳ Étape neutre           | -0.5          | Coût par action |
| 📡 Proximité de la pizza  | +3            | Encouragement |

---

## 📈 Suivi de l’apprentissage

Pendant l’entraînement, la console affiche :
```
Épisode   5 | Étapes:  42 | Récompense:  180.5 | Succès: True
Épisode  10 | Étapes:  31 | Récompense:  210.0 | Succès: True
...
Entraînement terminé. Meilleur chemin: 28 étapes.
```

---

## 🧪 Tests de performance (optionnel)

Une fois l’agent entraîné, tu peux le tester sur plusieurs parties **sans exploration** :
```python
from qlearning_agent import test_agent

test_agent(agent, environment_name="test", num_tests=5, show_gui=True)
```

---

## 💡 Conseils d’amélioration

- 📊 Ajouter une **visualisation des récompenses** au fil des épisodes avec `matplotlib`.  
- 💾 Sauvegarder et charger la **Q-table** avec `pickle`.  
- 🤖 Implémenter un **réseau de neurones (DQN)** pour une version plus avancée.  
- 🔄 Introduire des **obstacles dynamiques** ou des **bonus aléatoires** pour enrichir l’environnement.

---

## 👨‍💻 Auteur

**Projet DonatelloPyzza Q-Learning**  
Développé par *Nathan Amaral* – 2025  
Licence : **MIT**
