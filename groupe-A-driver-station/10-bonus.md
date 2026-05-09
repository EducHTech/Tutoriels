# A-10 — Défis bonus

> **Pour qui :** Groupe A — si tu as fini en avance
> **Prérequis :** [Joystick pygame](./09-joystick-pygame.md)

---

Bravo, tu as terminé le parcours principal ! Voici des défis pour aller plus loin.
Choisis ceux qui t'intéressent — ils sont indépendants.

---

## Défi 1 — Heartbeat (battement de cœur)

Un **heartbeat** est un message envoyé régulièrement pour dire "je suis encore là".

Le robot peut détecter une perte de connexion s'il ne reçoit plus de heartbeat.

**Ce que tu dois faire :**
- Envoyer un message `HEARTBEAT` toutes les secondes dans un thread séparé
- Afficher dans la Driver Station le temps depuis le dernier heartbeat reçu

<details>
<summary>💡 Piste</summary>

En Python, `threading.Thread` permet d'exécuter du code en parallèle. Cherche "python threading" dans la documentation.

</details>

---

## Défi 2 — Niveau de batterie

Ajoute une commande `GET_BATTERY` à la Driver Station et au simulateur.

Le simulateur renvoie `BATTERY:75` (valeur en pourcentage).

Affiche le niveau dans le terminal avec une barre visuelle :

```text
Batterie : [##########          ] 50%
```

<details>
<summary>💡 Piste</summary>

```python
niveau = 50
barre = "#" * (niveau // 5) + " " * (20 - niveau // 5)
print(f"Batterie : [{barre}] {niveau}%")
```

</details>

---

## Défi 3 — Détection de perte de connexion

Si le robot ne répond plus au `PING` pendant 3 secondes, affiche une alerte :

```text
⚠️ ROBOT DÉCONNECTÉ !
```

Et arrête d'envoyer des commandes moteur jusqu'à ce que la connexion revienne.

---

## Défi 4 — Interface graphique

Utilise `pygame` pour créer une fenêtre qui affiche :
- L'état de la LED (carré rouge/vert)
- La valeur du capteur (barre de progression)
- Les valeurs du joystick

---

## Défi 5 — Protocole binaire

Au lieu d'envoyer du texte (`"MOTOR:120"`), envoie des bytes bruts.

Par exemple : 2 bytes → `[1, 120]` où `1` = code commande moteur et `120` = valeur.

```python
import struct
data = struct.pack("Bb", 1, 120)   # 1 octet non signé + 1 octet signé
sock.sendto(data, (ROBOT_IP, ROBOT_PORT))
```

C'est plus compact et plus rapide. C'est ce que font de vrais systèmes robotiques.

---

⬅ [Précédent — Joystick](./09-joystick-pygame.md) · [Retour accueil](../README.md)
