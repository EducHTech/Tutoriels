# 03 — Wrapper UDP : la couche communication

> **Durée estimée :** 40 min
> **Prérequis :** [Structure .h/.cpp](./02-structure-projet.md)
> **Objectif :** écrire les modules `comm.h/.cpp` et `robot.h/.cpp`, assembler le firmware complet et ajouter la protection watchdog

---

## L'idée du wrapper

Un **wrapper** (enveloppe) est une couche de code qui **cache les détails** d'une technologie derrière une interface simple.

```
robot_esp32.ino
      │
      │  appelle  comm_sendEncoders(état)
      │            comm_sendGyro(état)
      │            comm_receive(&état)
      │            comm_isTimedOut()
      ▼
   comm_udp.cpp   ←── contient le vrai code UDP / WiFi
```

**L'intérêt :** si un jour on passe de l'ESP32 (UDP/WiFi) à un Arduino MEGA (Bluetooth), on crée `comm_bt.cpp` avec les mêmes fonctions et on supprime `comm_udp.cpp`. Le reste du programme ne change pas.

---

## `comm.h` — Déclaration de la couche communication

Crée `comm.h` et copie :

```cpp
// comm.h
// Interface de la couche communication
// Ce fichier ne change JAMAIS : il décrit le contrat.
// Seul le fichier d'implémentation change (comm_udp.cpp → comm_bt.cpp).

#pragma once
#include "protocol.h"

// Initialise le hotspot Wi-Fi et le socket UDP
void comm_begin();

// Vérifie si un paquet est arrivé et remplit l'état si oui
// Retourne true si une commande a été reçue
bool comm_receive(RobotState* state);

// Retourne true si aucun message reçu depuis plus de COMM_TIMEOUT_MS
bool comm_isTimedOut();

// Envoie les positions des encodeurs vers le script de commande
void comm_sendEncoders(const RobotState& state);

// Envoie l'angle du gyroscope vers le script de commande
void comm_sendGyro(const RobotState& state);
```

### Notations importantes

- `RobotState*` (avec `*`) → un **pointeur** : on passe l'adresse de la structure pour que la fonction puisse la **modifier**.
- `const RobotState&` (avec `&`) → une **référence constante** : on passe la structure en lecture seule, sans la copier.

> [!NOTE]
> Tu n'as pas besoin de maîtriser les pointeurs et références pour l'instant. Retiens simplement : `*` = la fonction va écrire dedans, `const &` = la fonction va seulement lire.

---

## `comm_udp.cpp` — Implémentation UDP

Crée **`comm_udp.cpp`** (pas `comm.cpp` !) et copie :

```cpp
// comm_udp.cpp
// Implémentation de la communication par UDP (ESP32 en mode hotspot)
// Pour passer au Bluetooth : créer comm_bt.cpp avec les mêmes fonctions,
// supprimer ce fichier. Rien d'autre à modifier.

#include "comm.h"
#include <WiFi.h>
#include <WiFiUdp.h>

// --- Paramètres du hotspot ---
static const char* WIFI_SSID     = "Robot-ESP32";
static const char* WIFI_PASSWORD = "robot1234";

// --- Objets UDP ---
static WiFiUDP    udp;
static IPAddress  remoteIP;          // IP du script de commande
static uint16_t   remotePort = 0;    // Port du script de commande
static char       rxBuffer[256];

// --- Watchdog ---
static unsigned long lastReceivedMs = 0;

// ----------------------------------------------------------------
void comm_begin()
{
    Serial.println("[COMM] Démarrage du hotspot...");
    WiFi.softAP(WIFI_SSID, WIFI_PASSWORD);
    Serial.print("[COMM] Hotspot actif. IP : ");
    Serial.println(WiFi.softAPIP());

    udp.begin(ROBOT_PORT);
    Serial.println("[COMM] UDP prêt sur port " + String(ROBOT_PORT));

    lastReceivedMs = millis();   // Démarrer le watchdog dès le lancement
}

// ----------------------------------------------------------------
bool comm_isTimedOut()
{
    return (millis() - lastReceivedMs) > COMM_TIMEOUT_MS;
}

// ----------------------------------------------------------------
bool comm_receive(RobotState* state)
{
    int packetSize = udp.parsePacket();
    if (packetSize == 0) return false;

    // Mémoriser l'expéditeur pour lui répondre
    remoteIP   = udp.remoteIP();
    remotePort = udp.remotePort();

    int len = udp.read(rxBuffer, sizeof(rxBuffer) - 1);
    rxBuffer[len] = '\0';

    // Mettre à jour le watchdog
    lastReceivedMs = millis();

    String cmd = String(rxBuffer);
    Serial.print("[COMM] Reçu : ");
    Serial.println(cmd);

    // --- Parser SET_MOTORS:v1,v2,v3,v4,v5,v6 ---
    if (cmd.startsWith("SET_MOTORS:"))
    {
        String data = cmd.substring(11);  // après "SET_MOTORS:"
        for (int i = 0; i < NB_MOTORS; i++)
        {
            int sep = data.indexOf(',');
            String token = (sep >= 0) ? data.substring(0, sep) : data;
            state->motorSpeeds[i] = token.toInt();
            if (sep >= 0) data = data.substring(sep + 1);
        }
        return true;
    }

    // --- Parser SET_SERVOS:a1,a2,a3 ---
    if (cmd.startsWith("SET_SERVOS:"))
    {
        String data = cmd.substring(11);  // après "SET_SERVOS:"
        for (int i = 0; i < NB_SERVOS; i++)
        {
            int sep = data.indexOf(',');
            String token = (sep >= 0) ? data.substring(0, sep) : data;
            state->servoAngles[i] = token.toInt();
            if (sep >= 0) data = data.substring(sep + 1);
        }
        return true;
    }

    // --- PING ---
    if (cmd == "PING")
    {
        udp.beginPacket(remoteIP, remotePort);
        udp.print("PONG");
        udp.endPacket();
        return false;   // Pas une commande de mouvement
    }

    return false;
}

// ----------------------------------------------------------------
void comm_sendEncoders(const RobotState& state)
{
    if (remotePort == 0) return;  // Personne ne s'est encore connecté

    String msg = "ENCODERS:";
    for (int i = 0; i < NB_MOTORS; i++)
    {
        msg += String(state.encoderCounts[i]);
        if (i < NB_MOTORS - 1) msg += ",";
    }

    udp.beginPacket(remoteIP, remotePort);
    udp.print(msg);
    udp.endPacket();
}

// ----------------------------------------------------------------
void comm_sendGyro(const RobotState& state)
{
    if (remotePort == 0) return;

    String msg = "GYRO:" + String(state.gyroAngleTenths);

    udp.beginPacket(remoteIP, remotePort);
    udp.print(msg);
    udp.endPacket();
}
```

### Comprendre `static`

Les variables `udp`, `remoteIP`, etc. sont déclarées `static` au niveau du fichier. Ça signifie qu'elles sont **privées à ce fichier** — aucun autre fichier ne peut y accéder directement. C'est exactement ce qu'on veut : les détails UDP restent enfermés dans `comm_udp.cpp`.

---

## `robot.h` — Déclaration de la logique robot

Crée `robot.h` et copie :

```cpp
// robot.h
// Interface de la logique robot (moteurs, servos, capteurs)

#pragma once
#include "protocol.h"

// Initialise les broches moteurs, servos, capteurs
void robot_begin();

// Applique les vitesses moteurs stockées dans l'état
void robot_applyMotors(const RobotState& state);

// Applique les angles servos stockés dans l'état
void robot_applyServos(const RobotState& state);

// Arrêt d'urgence : remet toutes les vitesses à 0 et arrête les moteurs
void robot_emergencyStop(RobotState* state);

// Lit les encodeurs et le gyro, met à jour l'état
void robot_readSensors(RobotState* state);
```

---

## `robot.cpp` — Implémentation (simulée)

Pour l'instant, les moteurs et capteurs sont **simulés** : on affiche dans le Moniteur Série ce qu'on ferait, et on génère des valeurs de capteurs fictives. Tu brancheras le vrai matériel plus tard.

Crée `robot.cpp` et copie :

```cpp
// robot.cpp
// Logique robot — moteurs, servos, capteurs
// Version simulée : affichage Série + valeurs fictives
// Remplace les TODO par le vrai code matériel plus tard.

#include "robot.h"
#include <Arduino.h>

// Compteurs internes pour simuler les encodeurs
static long simulatedEncoders[NB_MOTORS] = {0};
static int  simulatedGyro = 0;

// ----------------------------------------------------------------
void robot_begin()
{
    Serial.println("[ROBOT] Initialisation (mode simulé)");
    // TODO : pinMode pour les broches moteurs, servos, etc.
}

// ----------------------------------------------------------------
void robot_applyMotors(const RobotState& state)
{
    Serial.print("[MOTORS]");
    for (int i = 0; i < NB_MOTORS; i++)
    {
        Serial.print(" M");
        Serial.print(i);
        Serial.print("=");
        Serial.print(state.motorSpeeds[i]);
    }
    Serial.println();

    // TODO : remplacer par digitalWrite/analogWrite sur les broches réelles
}

// ----------------------------------------------------------------
void robot_applyServos(const RobotState& state)
{
    Serial.print("[SERVOS]");
    for (int i = 0; i < NB_SERVOS; i++)
    {
        Serial.print(" S");
        Serial.print(i);
        Serial.print("=");
        Serial.print(state.servoAngles[i]);
        Serial.print("°");
    }
    Serial.println();

    // TODO : remplacer par servo.write() sur les vrais objets Servo
}

// ----------------------------------------------------------------
void robot_emergencyStop(RobotState* state)
{
    // Mettre toutes les vitesses moteurs à 0
    for (int i = 0; i < NB_MOTORS; i++)
        state->motorSpeeds[i] = 0;

    // Appliquer immédiatement
    robot_applyMotors(*state);

    Serial.println("[ROBOT] *** ARRET D'URGENCE (watchdog) ***");
}

// ----------------------------------------------------------------
void robot_readSensors(RobotState* state)
{
    // Simulation : les encodeurs accumulent les vitesses moteurs
    for (int i = 0; i < NB_MOTORS; i++)
    {
        simulatedEncoders[i] += state->motorSpeeds[i] / 10;
        state->encoderCounts[i] = simulatedEncoders[i];
    }

    // Simulation : le gyro dérive légèrement
    simulatedGyro += 1;
    if (simulatedGyro > 3600) simulatedGyro = 0;
    state->gyroAngleTenths = simulatedGyro;

    // TODO : remplacer par la vraie lecture I2C du gyroscope
}
```

---

## `protocol.h` — Ajouter la constante watchdog

Ouvre `protocol.h` et ajoute la ligne `COMM_TIMEOUT_MS` :

```cpp
// protocol.h
#pragma once

// --- Port réseau ---
#define ROBOT_PORT       4210

// --- Limites ---
#define NB_MOTORS        6
#define NB_SERVOS        3

// --- Watchdog : durée maximum sans message avant arrêt d'urgence ---
#define COMM_TIMEOUT_MS  500   // 500 ms = 0.5 seconde

struct RobotState
{
    int  motorSpeeds[NB_MOTORS];   // vitesses moteurs : -255 à +255
    int  servoAngles[NB_SERVOS];   // angles servos    : 0 à 180°
    long encoderCounts[NB_MOTORS]; // positions encodeurs (ticks)
    int  gyroAngleTenths;          // angle gyro en dixièmes de degrés
};
```

---

## `robot_esp32.ino` — Le fichier principal

Le fichier `.ino` devient très court : il orchestre les modules sans contenir de détails.

Remplace tout le contenu de `robot_esp32.ino` par :

```cpp
// robot_esp32.ino
// Firmware principal — orchestre comm + robot
//
// Ce fichier doit rester court et lisible.
// Les détails sont dans comm_udp.cpp et robot.cpp.

#include "comm.h"
#include "robot.h"

RobotState state;   // L'état global du robot

void setup()
{
    Serial.begin(115200);
    delay(500);

    memset(&state, 0, sizeof(state));  // Tout mettre à zéro
    comm_begin();
    robot_begin();

    Serial.println("=== Robot prêt ===");
}

void loop()
{
    // 1. Recevoir et traiter les commandes entrantes
    if (comm_receive(&state))
    {
        robot_applyMotors(state);
        robot_applyServos(state);
    }

    // 2. Watchdog : si plus aucun message depuis trop longtemps, arrêt d'urgence
    if (comm_isTimedOut())
    {
        robot_emergencyStop(&state);
    }

    // 3. Lire les capteurs et envoyer les données de retour
    robot_readSensors(&state);
    comm_sendEncoders(state);
    comm_sendGyro(state);

    delay(20);   // Cycle de 20 ms (50 Hz)
}
```

### Pourquoi `delay(20)` ?

On veut un cycle régulier à **50 fois par seconde** (50 Hz).
$50 \text{ Hz} = \frac{1}{50} \text{ s} = 20 \text{ ms}$

C'est suffisamment rapide pour contrôler un robot, sans surcharger le réseau.

### Pourquoi `comm_isTimedOut()` déclenche `robot_emergencyStop()` ?

Si le script Python plante, si le Wi-Fi coupe, si le câble se débranche — le robot ne reçoit plus de commande. Sans cette protection, il continuerait à tourner à la dernière vitesse reçue jusqu'à ce qu'on le débranche à la main. `comm_isTimedOut()` détecte le silence et `robot_emergencyStop()` remet tout à zéro.

---

## Résumé de la structure finale

```
robot_esp32/
├── robot_esp32.ino    ← setup() + loop() : ~35 lignes
├── protocol.h         ← constantes + COMM_TIMEOUT_MS + struct RobotState
├── comm.h             ← interface comm (5 fonctions) — ne change jamais
├── comm_udp.cpp       ← implémentation UDP   ⇐ REMPLACER PAR comm_bt.cpp pour Bluetooth
├── robot.h            ← interface robot (5 fonctions)
└── robot.cpp          ← implémentation simulée
```

---

## Tester avec le Fake Driver Station

Lance le script Python fourni :

```bash
# Connecte d'abord ton PC au Wi-Fi "Robot-ESP32" (mot de passe : robot1234)
python fake_driver_station.py
```

Referme le script ou déconnecte le Wi-Fi en cours de test : tu dois voir apparaitre dans le Moniteur Série :

```text
[ROBOT] *** ARRET D'URGENCE (watchdog) ***
[MOTORS] M0=0 M1=0 M2=0 M3=0 M4=0 M5=0
```

Normal pendant le test, tu devrais aussi voir :

```text
[COMM] Démarrage du hotspot...
[COMM] Hotspot actif. IP : 192.168.4.1
[COMM] UDP prêt sur port 4210
=== Robot prêt ===
[COMM] Reçu : PING
[COMM] Reçu : SET_MOTORS:50,50,-50,-50,0,0
[MOTORS] M0=50 M1=50 M2=-50 M3=-50 M4=0 M5=0
[COMM] Reçu : SET_SERVOS:90,45,120
[SERVOS] S0=90° S1=45° S2=120°
```

---

## Cases à cocher

- [ ] Les 6 fichiers sont créés et compilent sans erreur
- [ ] Le Moniteur Série affiche `=== Robot prêt ===`
- [ ] Le hotspot `Robot-ESP32` est visible
- [ ] Après connexion au hotspot, `fake_driver_station.py` s'exécute
- [ ] `SET_MOTORS` affiche les bonnes valeurs dans le Moniteur Série
- [ ] `SET_SERVOS` affiche les bons angles dans le Moniteur Série
- [ ] `PING` reçoit `PONG`
- [ ] Le script Python reçoit des `ENCODERS:...` et `GYRO:...`
- [ ] En coupant le script Python, le Moniteur Série affiche `ARRET D'URGENCE` après 500 ms

---

## Pour aller plus loin : remplacer UDP par Bluetooth

Quand vous passerez à l'Arduino MEGA 2560 avec Bluetooth :

1. Créer `comm_bt.cpp` dans le même dossier
2. Implémenter les 5 mêmes fonctions (`comm_begin`, `comm_isTimedOut`, `comm_receive`, `comm_sendEncoders`, `comm_sendGyro`) avec la bibliothèque Bluetooth
3. Supprimer `comm_udp.cpp`
4. **Rien d'autre ne change** : `robot_esp32.ino`, `comm.h`, `robot.h`, `robot.cpp`, `protocol.h` restent identiques

C'est la puissance du wrapper !

---

⬅ [Précédent — Structure .h/.cpp](./02-structure-projet.md) · [Retour accueil projet](./README.md)
