# A-04 — Boucles UDP

> **Pour qui :** Groupe A
> **Durée estimée :** 10 min
> **Prérequis :** [Émetteur UDP](./03-premier-udp-emetteur.md)
> **Objectif :** envoyer des messages en continu, toutes les X secondes

---

## Le problème

Pour l'instant, `sender.py` envoie **un seul message** puis s'arrête.

Un robot a besoin de recevoir des commandes **en permanence** (tant qu'on appuie sur le bouton, tant qu'on bouge le joystick, etc.).

Il faut une **boucle**.

---

## Le programme

Crée `sender_loop.py` :

```python
import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Envoi en boucle... (Ctrl+C pour arrêter)")

while True:
    sock.sendto("PING".encode(), ("127.0.0.1", 4210))
    print("PING envoyé")
    time.sleep(1)
```

Lance-le dans un terminal, et `receiver.py` dans un autre. Tu verras un PING arriver chaque seconde.

---

## Comprendre le code

### `while True:`

```python
while True:
    ...
```

Une **boucle infinie**. Le code à l'intérieur se répète indéfiniment.

`True` = vrai → la condition est toujours vraie → on ne sort jamais de la boucle.

Pour arrêter : `Ctrl + C` dans le terminal.

---

### `time.sleep(1)`

```python
time.sleep(1)
```

`time.sleep(n)` met le programme en **pause** pendant `n` secondes.

- `time.sleep(1)` → pause de 1 seconde
- `time.sleep(0.5)` → pause de 500 millisecondes
- `time.sleep(0.1)` → pause de 100 millisecondes (10 fois par seconde)

---

### `import time`

```python
import time
```

`time` est une bibliothèque Python intégrée. On l'importe pour utiliser `time.sleep()`.

---

## Exercice

Modifie le programme pour envoyer `"MOTOR:100"` toutes les **0.5 secondes**.

<details>
<summary>💡 Voir la solution</summary>

```python
import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    sock.sendto("MOTOR:100".encode(), ("127.0.0.1", 4210))
    print("MOTOR:100 envoyé")
    time.sleep(0.5)
```

</details>

---

## Défi bonus 🎯

Affiche le nombre de messages envoyés à côté du message :

```text
PING envoyé (message n°1)
PING envoyé (message n°2)
PING envoyé (message n°3)
...
```

<details>
<summary>💡 Voir la solution</summary>

```python
import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

compteur = 0

while True:
    compteur = compteur + 1
    sock.sendto("PING".encode(), ("127.0.0.1", 4210))
    print(f"PING envoyé (message n°{compteur})")
    time.sleep(1)
```

Le `f"..."` s'appelle une **f-string** : ça permet d'insérer une variable dans un texte avec `{variable}`.

</details>

---

## Cases à cocher

- [ ] J'ai créé `sender_loop.py`
- [ ] Le programme envoie des messages en boucle
- [ ] J'ai compris ce que fait `while True`
- [ ] J'ai compris ce que fait `time.sleep()`

---

⬅ [Précédent — Émetteur UDP](./03-premier-udp-emetteur.md) · [Suivant ➡ Ping/Pong](./05-ping-pong.md)
