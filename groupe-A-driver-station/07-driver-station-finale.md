# A-07 — Driver Station finale

> **Pour qui :** Groupe A
> **Durée estimée :** 20 min
> **Prérequis :** [Simulateur de robot](./06-simulateur-robot.md)
> **Objectif :** créer un menu de contrôle complet pour le robot

---

> [!IMPORTANT]
> **🔄 Point de synchro 2** — pour tester avec le vrai robot, attends que le Groupe B ait terminé [B-04 — Contrôle LED](../groupe-B-robot-esp32/04-controle-led.md).
> En attendant, tu peux tester avec le simulateur !

---

## Le programme

Crée `driver_station.py` :

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 4210))
sock.settimeout(0.5)  # Ne pas bloquer plus de 0.5s en attente de réponse

# Adresse IP du robot (ou 127.0.0.1 pour le simulateur)
ROBOT_IP = "127.0.0.1"
ROBOT_PORT = 4210

print("=== Driver Station ===")
print(f"Robot : {ROBOT_IP}:{ROBOT_PORT}")
print()

while True:
    print("--- Que veux-tu faire ? ---")
    print("1 - LED ON")
    print("2 - LED OFF")
    print("3 - PING (vérifier connexion)")
    print("4 - Lire capteur")
    print("q - Quitter")

    choix = input("Ton choix : ")

    if choix == "1":
        sock.sendto("LED_ON".encode(), (ROBOT_IP, ROBOT_PORT))
        print("→ Commande LED_ON envoyée")

    elif choix == "2":
        sock.sendto("LED_OFF".encode(), (ROBOT_IP, ROBOT_PORT))
        print("→ Commande LED_OFF envoyée")

    elif choix == "3":
        sock.sendto("PING".encode(), (ROBOT_IP, ROBOT_PORT))
        try:
            reponse, _ = sock.recvfrom(1024)
            print("→ Réponse :", reponse.decode())
        except:
            print("→ Pas de réponse (robot déconnecté ?)")

    elif choix == "4":
        sock.sendto("GET_SENSOR".encode(), (ROBOT_IP, ROBOT_PORT))
        try:
            reponse, _ = sock.recvfrom(1024)
            print("→ Valeur capteur :", reponse.decode())
        except:
            print("→ Pas de réponse")

    elif choix == "q":
        print("Au revoir !")
        break

    print()
```

---

## Tester avec le simulateur

Terminal 1 :

```bash
python robot_simulator.py
```

Terminal 2 :

```bash
python driver_station.py
```

Essaie chaque option du menu !

---

## 🔄 Synchro 2 — Tester avec le vrai robot

Quand le Groupe B signale que l'ESP32 répond à `LED_ON` / `LED_OFF` :

1. Note l'adresse IP de l'ESP32 (le Groupe B te la donne)
2. Modifie la ligne dans `driver_station.py` :

```python
ROBOT_IP = "192.168.X.XX"   # IP réelle de l'ESP32
```

3. Relance et teste — la LED doit s'allumer/s'éteindre pour de vrai !

---

## Comprendre

### `sock.settimeout(0.5)`

```python
sock.settimeout(0.5)
```

Sans timeout, `recvfrom()` bloquerait indéfiniment si le robot ne répond pas.
Avec `settimeout(0.5)`, on attend max 0.5 secondes et on continue.

### `try: ... except:`

```python
try:
    reponse, _ = sock.recvfrom(1024)
except:
    print("→ Pas de réponse")
```

Si le timeout est dépassé, Python lève une erreur. Le `try/except` l'attrape et affiche un message propre.

---

## Cases à cocher

- [ ] La Driver Station affiche bien le menu
- [ ] `LED_ON` et `LED_OFF` fonctionnent avec le simulateur
- [ ] `PING` reçoit `PONG`
- [ ] `GET_SENSOR` reçoit une valeur
- [ ] (Synchro 2) Testé avec le vrai robot ESP32

---

⬅ [Précédent — Simulateur](./06-simulateur-robot.md) · [Suivant ➡ Contrôle clavier](./08-controle-clavier.md)
