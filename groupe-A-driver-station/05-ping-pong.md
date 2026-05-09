# A-05 — Ping / Pong (client / serveur)

> **Pour qui :** Groupe A
> **Durée estimée :** 15 min
> **Prérequis :** [Boucles UDP](./04-boucles-udp.md)
> **Objectif :** créer un échange question/réponse entre deux programmes Python

---

> [!IMPORTANT]
> **🔄 Point de synchro 1** — après cette étape, tu pourras tester avec le robot du Groupe B !
> Attends que le Groupe B ait terminé [B-03 — Recevoir UDP](../groupe-B-robot-esp32/03-recevoir-udp.md).

---

## L'idée

Jusqu'ici on envoyait des messages dans un seul sens. Dans un vrai système, il y a des **échanges** :

```text
CLIENT  ----  PING  ---->  SERVEUR
CLIENT  <---  PONG  ----   SERVEUR
```

Le client envoie une question → le serveur répond.

---

## Le serveur

Crée `server.py` :

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 4210))

print("Serveur démarré, en attente...")

while True:
    message, address = sock.recvfrom(1024)
    texte = message.decode()

    print("Reçu :", texte, "de", address)

    if texte == "PING":
        sock.sendto("PONG".encode(), address)
        print("PONG envoyé !")
```

---

## Le client

Crée `client.py` :

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Envoyer PING au serveur
sock.sendto("PING".encode(), ("127.0.0.1", 4210))
print("PING envoyé")

# Attendre la réponse
message, address = sock.recvfrom(1024)
print("Réponse reçue :", message.decode())
```

---

## Test

1. Terminal 1 → `python server.py`
2. Terminal 2 → `python client.py`

Résultat attendu dans le terminal 2 :

```text
PING envoyé
Réponse reçue : PONG
```

---

## Comprendre

### `address` dans `sendto()`

```python
sock.sendto("PONG".encode(), address)
```

Le serveur renvoie la réponse à l'**adresse de l'expéditeur** (récupérée via `recvfrom`).
Il n'a pas besoin de connaître l'adresse du client à l'avance !

---

## 🔄 Synchro 1 — Tester avec le vrai robot

Quand le Groupe B a terminé B-03, il t'a communiqué l'**adresse IP de son ESP32**.

Modifie `client.py` pour envoyer le PING au robot au lieu de `127.0.0.1` :

```python
sock.sendto("PING".encode(), ("192.168.X.XX", 4210))
```

Remplace `192.168.X.XX` par l'IP de l'ESP32 fournie par le Groupe B.

---

## Cases à cocher

- [ ] `server.py` répond PONG quand il reçoit PING
- [ ] `client.py` reçoit bien PONG
- [ ] (Synchro 1) J'ai testé avec l'IP réelle de l'ESP32

---

## Mini-quiz

**Question :** Comment le serveur sait-il où renvoyer sa réponse ?

<details>
<summary>💡 Voir la réponse</summary>

`recvfrom()` retourne `message, address`. La variable `address` contient l'IP et le port de l'expéditeur. Le serveur utilise cette adresse pour envoyer sa réponse avec `sendto(..., address)`.

</details>

---

⬅ [Précédent — Boucles UDP](./04-boucles-udp.md) · [Suivant ➡ Simulateur de robot](./06-simulateur-robot.md)
