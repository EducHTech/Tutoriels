# A-06 — Simulateur de robot

> **Pour qui :** Groupe A
> **Durée estimée :** 15 min
> **Prérequis :** [Ping/Pong](./05-ping-pong.md)
> **Objectif :** simuler le robot sur ton ordinateur pour avancer sans attendre le Groupe B

---

## Pourquoi un simulateur ?

Parfois le Groupe B est en train de programmer l'ESP32, et tu ne peux pas encore tester avec le vrai robot.

Le simulateur **fait semblant d'être le robot** : il reçoit les mêmes commandes et répond de la même façon. Tu peux ainsi programmer ta Driver Station sans avoir besoin de matériel.

---

## Le programme

Crée `robot_simulator.py` :

```python
import socket
import random

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 4210))

print("=== Simulateur de robot démarré ===")
print("En attente de commandes...")

while True:
    message, address = sock.recvfrom(1024)
    texte = message.decode()

    print("Commande reçue :", texte)

    if texte == "PING":
        sock.sendto("PONG".encode(), address)
        print("  → PONG envoyé")

    elif texte == "LED_ON":
        print("  → [SIMULATION] LED allumée 💡")

    elif texte == "LED_OFF":
        print("  → [SIMULATION] LED éteinte")

    elif texte == "GET_SENSOR":
        valeur = random.randint(0, 100)
        reponse = "SENSOR:" + str(valeur)
        sock.sendto(reponse.encode(), address)
        print("  → Valeur capteur envoyée :", valeur)

    else:
        print("  → Commande inconnue")
```

---

## Lancer le simulateur

Terminal 1 :

```bash
python robot_simulator.py
```

Dans un autre terminal, envoie des commandes avec `client.py` ou `sender.py`.

---

## Tester manuellement

Tu peux créer un petit fichier `test_commandes.py` pour tester chaque commande :

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)  # Attendre max 2 secondes une réponse

def envoyer(commande):
    sock.sendto(commande.encode(), ("127.0.0.1", 4210))
    print("Envoyé :", commande)
    try:
        reponse, _ = sock.recvfrom(1024)
        print("Réponse :", reponse.decode())
    except:
        print("Pas de réponse (normal pour LED_ON/OFF)")

envoyer("PING")
envoyer("LED_ON")
envoyer("LED_OFF")
envoyer("GET_SENSOR")
```

---

## Cases à cocher

- [ ] Le simulateur tourne et attend des commandes
- [ ] `PING` → reçoit `PONG`
- [ ] `LED_ON` → affiche "LED allumée"
- [ ] `GET_SENSOR` → reçoit une valeur `SENSOR:XX`

---

> [!TIP]
> Ce simulateur te sera très utile pour développer et tester toute la Driver Station sans avoir besoin de l'ESP32 branché. Le vrai robot du Groupe B répondra exactement aux mêmes commandes.

---

⬅ [Précédent — Ping/Pong](./05-ping-pong.md) · [Suivant ➡ Driver Station finale](./07-driver-station-finale.md)
