# 01 — Concevoir le protocole de communication

> **Durée estimée :** 20 min
> **Prérequis :** [Firmware final ESP32](../groupe-B-robot-esp32/07-robot-final.md)
> **Objectif :** définir un protocole clair entre le script Python de commande et le firmware du robot

---

## Pourquoi un protocole ?

Dans le firmware précédent, on envoyait des messages comme `LED_ON`, `MOTOR:120`, `GET_SENSOR`.
C'était bien pour apprendre, mais pour un vrai robot il faut quelque chose de plus **structuré** et de plus **complet**.

Un **protocole**, c'est un contrat :
- Le script Python (`fake_driver_station.py`) s'engage à envoyer les commandes dans un format précis.
- Le firmware ESP32 s'engage à répondre dans un format précis.
- Si tout le monde respecte le contrat, le système fonctionne.

> **Analogie :** quand tu commandes une pizza par téléphone, il y a un protocole implicite : tu donnes ton adresse, tes garnitures, ton numéro. Si tu parles dans n'importe quel ordre, le livreur est perdu.

---

## Ce que notre robot doit gérer

Notre robot a :

| Élément | Quantité | Direction | Description |
|---|---|---|---|
| Moteurs + encodeurs | 6 | ↕ bidirectionnel | On envoie la vitesse, on reçoit la position |
| Servos (PWM) | 3 | ↓ commande seulement | On envoie l'angle (0–180°) |
| Gyroscope | 1 | ↑ lecture seulement | On reçoit l'angle de rotation |

**Flux de données :**

```
fake_driver_station.py  ────────────────────►  Firmware ESP32
                          SET_MOTORS:v1,...,v6
                          SET_SERVOS:a1,a2,a3
                          PING

fake_driver_station.py  ◄────────────────────  Firmware ESP32
                          ENCODERS:p1,...,p6
                          GYRO:angle
                          PONG
```

---

## Le protocole en détail

### Commandes envoyées au robot (Driver Station → Robot)

#### `SET_MOTORS:v1,v2,v3,v4,v5,v6`

Définit la vitesse des 6 moteurs.  
Chaque valeur est un entier entre **-255** et **+255**.

```text
SET_MOTORS:100,100,-50,-50,0,0
```

- Positif = avant
- Négatif = arrière
- 0 = arrêt

#### `SET_SERVOS:a1,a2,a3`

Définit l'angle des 3 servomoteurs.  
Chaque valeur est un entier entre **0** et **180** (degrés).

```text
SET_SERVOS:90,45,120
```

#### `PING`

Vérifie que le robot est en vie. Le robot répond `PONG`.

---

### Réponses envoyées par le robot (Robot → Driver Station)

#### `ENCODERS:p1,p2,p3,p4,p5,p6`

Envoie la position actuelle des 6 encodeurs.  
Chaque valeur est un entier (nombre de ticks).

```text
ENCODERS:1024,-512,0,300,300,0
```

#### `GYRO:angle`

Envoie l'angle de rotation mesuré par le gyroscope.  
Valeur en dixièmes de degrés (pour éviter les flottants).

```text
GYRO:452
```
> Signifie 45.2 degrés.

#### `PONG`

Réponse au `PING`.

---

## Cycle de communication

Le robot tourne en boucle. À chaque cycle :

```
1. Y a-t-il un paquet UDP entrant ?
   ├─ Oui → parser la commande, l'exécuter, noter l'heure
   └─ Non → vérifier le watchdog

2. Watchdog : combien de temps depuis le dernier message ?
   ├─ < 500 ms  → tout va bien, continuer
   └─ ≥ 500 ms  → ARRÊT D'URGENCE (tous les moteurs à 0)

3. Envoyer les données de retour :
   - ENCODERS:...
   - GYRO:...
```

```
      ┌──────────────────────────────────────┐
      │               loop()                 │
      │                                      │
      │  ┌──────────────────────────────┐    │
      │  │  Lire paquet UDP             │    │
      │  │  ├─ reçu → parser + exécuter │    │
      │  │  └─ rien → vérifier watchdog │    │
      │  └──────────────────────────────┘    │
      │                                      │
      │  ┌──────────────────────────────┐    │
      │  │  Envoyer ENCODERS + GYRO     │    │
      │  └──────────────────────────────┘    │
      └──────────────────────────────────────┘
```

### Pourquoi un watchdog ?

Si le câble réseau se débranche, si le script Python plante, si le Wi-Fi coupe — le robot ne reçoit plus de commande. Sans protection, il continuerait à tourner à la dernière vitesse reçue indéfiniment. C'est dangereux.

Le **watchdog** (chien de garde) surveille le temps écoulé depuis le dernier message reçu. Au-delà de 500 ms de silence : **arrêt complet**.

---

## Pourquoi des entiers et pas des décimaux ?

Tu as peut-être remarqué que le gyro envoie `452` pour 45.2°.

En C++ (et dans les protocoles réseau), travailler avec des **nombres entiers** (`int`) est plus simple et plus fiable que les décimaux (`float`).

```cpp
// Décimal : fragile, encodage variable
float angle = 45.2;

// Entier : robuste, on divise à la réception
int angleTenths = 452;   // 45.2 * 10
```

Le script Python divise par 10 à la réception :

```python
angle = int(valeur) / 10.0   # → 45.2
```

---

## Cases à cocher

- [ ] Je comprends ce que fait `SET_MOTORS`
- [ ] Je comprends ce que fait `SET_SERVOS`
- [ ] Je comprends ce que renvoie `ENCODERS`
- [ ] Je comprends ce que renvoie `GYRO`
- [ ] J'ai lu le cycle de communication

---

## Mini-quiz

**Question :** Pourquoi envoie-t-on les 6 vitesses moteurs dans **un seul message** (`SET_MOTORS:v1,v2,...`) plutôt qu'en 6 messages séparés ?

<details>
<summary>💡 Voir la réponse</summary>

Si on envoyait 6 messages séparés, ils pourraient arriver dans un ordre différent, ou certains pourraient se perdre. Le robot pourrait exécuter une vitesse partielle. En regroupant tout dans un seul paquet UDP, soit tout arrive ensemble, soit rien n'arrive.

</details>

---

⬅ [Précédent — Firmware final ESP32](../groupe-B-robot-esp32/07-robot-final.md) · [Suivant ➡ Structure en fichiers .h/.cpp](./02-structure-projet.md)
