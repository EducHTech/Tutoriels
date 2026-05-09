# A-09 — Contrôle joystick avec pygame

> **Pour qui :** Groupe A
> **Durée estimée :** 20 min
> **Prérequis :** [Contrôle clavier](./08-controle-clavier.md)
> **Objectif :** lire un joystick USB et envoyer ses valeurs au robot

---

> [!IMPORTANT]
> **🔄 Point de synchro 3** — pour tester avec le vrai robot, attends que le Groupe B ait terminé [B-07 — Firmware final](../groupe-B-robot-esp32/07-robot-final.md).

---

## Installer pygame

`pygame` est une bibliothèque Python qui permet de lire des joysticks (et de faire des jeux).

Dans le terminal :

```bash
pip install pygame
```

Attends que l'installation se termine.

Vérifie :

```bash
python -c "import pygame; print('pygame OK')"
```

---

## Le programme

Crée `joystick_control.py` :

```python
import pygame
import socket
import time

# Initialisation pygame
pygame.init()
pygame.joystick.init()

# Vérifier qu'un joystick est connecté
if pygame.joystick.get_count() == 0:
    print("Aucun joystick détecté ! Branche-en un et relance.")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"Joystick détecté : {joystick.get_name()}")

# Socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

ROBOT_IP = "127.0.0.1"   # Changer pour l'IP de l'ESP32
ROBOT_PORT = 4210

print("Contrôle joystick actif. Ctrl+C pour arrêter.")

while True:
    pygame.event.pump()  # Mettre à jour les événements joystick

    # Lire les axes (entre -1.0 et 1.0)
    gauche = joystick.get_axis(1)   # Axe vertical gauche
    droite = joystick.get_axis(3)   # Axe vertical droit

    # Convertir en entiers -255 à 255
    val_gauche = int(gauche * 255)
    val_droite = int(droite * 255)

    # Construire et envoyer la commande
    commande = f"MOTOR:{val_gauche}:{val_droite}"
    sock.sendto(commande.encode(), (ROBOT_IP, ROBOT_PORT))

    print(f"Envoyé : {commande}", end="\r")   # \r écrase la ligne précédente

    time.sleep(0.05)  # 20 fois par seconde
```

---

## Comprendre

### `pygame.event.pump()`

```python
pygame.event.pump()
```

Met à jour l'état interne des joysticks. À appeler au début de chaque tour de boucle.

### `joystick.get_axis(n)`

```python
gauche = joystick.get_axis(1)
```

Lit la valeur d'un axe analogique. Retourne un flottant entre **-1.0** et **1.0**.

- `-1.0` = joystick poussé complètement vers le haut/gauche
- `0.0` = joystick au centre
- `1.0` = joystick poussé complètement vers le bas/droite

### Numéros des axes

Les numéros varient selon les joysticks. Essaie ces valeurs courantes :

| Axe | Signification habituelle |
|---|---|
| 0 | Horizontal gauche |
| 1 | Vertical gauche |
| 2 | Horizontal droit |
| 3 | Vertical droit |

### `int(gauche * 255)`

On multiplie par 255 pour obtenir une valeur entre -255 et 255, puis on convertit en entier.

---

## Format de commande moteur différentiel

```text
MOTOR:gauche:droite
```

Exemple : `MOTOR:-120:120` → tourner sur place (gauche en arrière, droite en avant).

---

## 🔄 Synchro 3 — Tester avec le vrai robot

Quand le Groupe B a son firmware final opérationnel :

```python
ROBOT_IP = "192.168.X.XX"   # IP réelle de l'ESP32
```

---

## Cases à cocher

- [ ] pygame est installé
- [ ] Un joystick est détecté
- [ ] Les valeurs des axes s'affichent en temps réel dans le terminal
- [ ] (Synchro 3) Testé avec le vrai robot

---

## Défi bonus 🎯

Affiche uniquement quand les valeurs changent (pas à chaque itération). Ça évite le flood de messages.

<details>
<summary>💡 Piste de solution</summary>

Mémorise les valeurs précédentes dans des variables `prev_gauche` et `prev_droite`.
N'envoie la commande que si les valeurs ont changé de plus de 5.

</details>

---

⬅ [Précédent — Contrôle clavier](./08-controle-clavier.md) · [Suivant ➡ Défis bonus](./10-bonus.md)
