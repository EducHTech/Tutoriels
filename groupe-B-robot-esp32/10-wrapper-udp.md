# B-10 — Wrapper UDP : la couche communication

> **Pour qui :** Groupe B
> **Durée estimée :** 40 min
> **Prérequis :** [Structure .h/.cpp](./09-structure-projet-lib.md)
> **Objectif :** écrire les modules `comm.h/.cpp` et `robot.h/.cpp`, puis assembler le firmware complet

---

## L'idée du wrapper

Un **wrapper** (enveloppe) est une couche de code qui **cache les détails** d'une technologie derrière une interface simple.

```
robot_esp32.ino
      │
      │  appelle  comm_sendEncoders(état)
      │            comm_sendGyro(état)
      │            comm_receive(&état)
      ▼
   comm.cpp   ←── contient le vrai code UDP / WiFi
```

**L'intérêt :** si un jour on passe de l'ESP32 (UDP/WiFi) à un Arduino MEGA (Bluetooth), on réécrit **seulement `comm.cpp`**. Le reste du programme ne change pas.

---

## `comm.h` — Déclaration de la couche communication

Crée `comm.h` et copie :

```cpp
// comm.h
// Interface de la couche communication (UDP sur ESP32)
// Pour passer au Bluetooth, on remplacera comm.cpp
// sans toucher au reste du projet.

#pragma once
#include "protocol.h"

// Initialise le hotspot Wi-Fi et le socket UDP
void comm_begin();

// Vérifie si un paquet est arrivé et remplit l'état si oui
// Retourne true si une commande a été reçue
bool comm_receive(RobotState* state);

// Envoie les positions des encodeurs vers le Driver Station
void comm_sendEncoders(const RobotState& state);

// Envoie l'angle du gyroscope vers le Driver Station
void comm_sendGyro(const RobotState& state);
```

### Notations importantes

- `RobotState*` (avec `*`) → un **pointeur** : on passe l'adresse de la structure pour que la fonction puisse la **modifier**.
- `const RobotState&` (avec `&`) → une **référence constante** : on passe la structure en lecture seule, sans la copier.

> [!NOTE]
> Tu n'as pas besoin de maîtriser les pointeurs et références pour l'instant. Retiens simplement : `*` = la fonction va écrire dedans, `const &` = la fonction va seulement lire.

---

## `comm.cpp` — Implémentation UDP

Crée `comm.cpp` et copie :

```cpp
// comm.cpp
// Implémentation de la communication par UDP (ESP32 en mode hotspot)

#include "comm.h"
#include <WiFi.h>
#include <WiFiUdp.h>

// --- Paramètres du hotspot ---
static const char* WIFI_SSID     = "Robot-ESP32";
static const char* WIFI_PASSWORD = "robot1234";

// --- Objets UDP ---
static WiFiUDP    udp;
static IPAddress  driverStationIP;   // IP du dernier expéditeur
static uint16_t   driverStationPort; // Port du dernier expéditeur
static char       rxBuffer[256];

// ----------------------------------------------------------------
void comm_begin()
{
    Serial.println("[COMM] Démarrage du hotspot...");
    WiFi.softAP(WIFI_SSID, WIFI_PASSWORD);
    Serial.print("[COMM] Hotspot actif. IP : ");
    Serial.println(WiFi.softAPIP());

    udp.begin(ROBOT_PORT);
    Serial.println("[COMM] UDP prêt sur port " + String(ROBOT_PORT));
}

// ----------------------------------------------------------------
bool comm_receive(RobotState* state)
{
    int packetSize = udp.parsePacket();
    if (packetSize == 0) return false;

    // Mémoriser l'expéditeur pour lui répondre
    driverStationIP   = udp.remoteIP();
    driverStationPort = udp.remotePort();

    int len = udp.read(rxBuffer, sizeof(rxBuffer) - 1);
    rxBuffer[len] = '\0';

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
        udp.beginPacket(driverStationIP, driverStationPort);
        udp.print("PONG");
        udp.endPacket();
        return false;   // Pas une commande de mouvement
    }

    return false;
}

// ----------------------------------------------------------------
void comm_sendEncoders(const RobotState& state)
{
    if (driverStationPort == 0) return;  // Personne n'a encore contacté le robot

    String msg = "ENCODERS:";
    for (int i = 0; i < NB_MOTORS; i++)
    {
        msg += String(state.encoderCounts[i]);
        if (i < NB_MOTORS - 1) msg += ",";
    }

    udp.beginPacket(driverStationIP, driverStationPort);
    udp.print(msg);
    udp.endPacket();
}

// ----------------------------------------------------------------
void comm_sendGyro(const RobotState& state)
{
    if (driverStationPort == 0) return;

    String msg = "GYRO:" + String(state.gyroAngleTenths);

    udp.beginPacket(driverStationIP, driverStationPort);
    udp.print(msg);
    udp.endPacket();
}
```

### Comprendre `static`

Les variables `udp`, `driverStationIP`, etc. sont déclarées `static` au niveau du fichier. Ça signifie qu'elles sont **privées à ce fichier** — aucun autre fichier ne peut y accéder directement. C'est comme déclarer que ces détails sont internes à `comm.cpp`.

---

## `robot.h` — Déclaration de la logique robot

Crée `robot.h` et copie :

```cpp
// robot.h
// Interface de la logique robot (moteurs, servos, capteurs)
// Le "vrai" branchement matériel sera fait dans robot.cpp

#pragma once
#include "protocol.h"

// Initialise les broches moteurs, servos, capteurs
void robot_begin();

// Applique les vitesses moteurs stockées dans l'état
void robot_applyMotors(const RobotState& state);

// Applique les angles servos stockés dans l'état
void robot_applyServos(const RobotState& state);

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

## `robot_esp32.ino` — Le fichier principal

Le fichier `.ino` devient très court : il orchestre les modules sans contenir de détails.

Remplace tout le contenu de `robot_esp32.ino` par :

```cpp
// robot_esp32.ino
// Firmware principal — orchestre comm + robot
//
// Ce fichier doit rester court et lisible.
// Les détails sont dans comm.cpp et robot.cpp.

#include "comm.h"
#include "robot.h"

RobotState state;   // L'état global du robot

void setup()
{
    Serial.begin(115200);
    delay(500);

    // Initialiser les modules
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

    // 2. Lire les capteurs et envoyer les données de retour
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

---

## Résumé de la structure finale

```
robot_esp32/
├── robot_esp32.ino   ← setup() + loop() : 30 lignes, très lisible
├── protocol.h        ← constantes + struct RobotState
├── comm.h            ← interface comm (4 fonctions)
├── comm.cpp          ← implémentation UDP hotspot
├── robot.h           ← interface robot (4 fonctions)
└── robot.cpp         ← implémentation simulée
```

---

## Tester avec le Fake Driver Station

Le Groupe A (ou toi depuis ton propre PC) peut utiliser le script Python fourni dans [fake_driver_station.py](../outils/fake_driver_station.py) pour tester chaque commande.

Connecte d'abord ton PC au Wi-Fi `Robot-ESP32` (mot de passe : `robot1234`), puis :

```bash
python fake_driver_station.py
```

Tu devrais voir dans le Moniteur Série :

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

- [ ] Les 5 fichiers sont créés et compilent sans erreur
- [ ] Le Moniteur Série affiche `=== Robot prêt ===`
- [ ] Le hotspot `Robot-ESP32` est visible
- [ ] Après connexion au hotspot, `fake_driver_station.py` s'exécute
- [ ] `SET_MOTORS` affiche les bonnes valeurs dans le Moniteur Série
- [ ] `SET_SERVOS` affiche les bons angles dans le Moniteur Série
- [ ] `PING` reçoit `PONG`
- [ ] Le script Python reçoit des `ENCODERS:...` et `GYRO:...`

---

## Pour aller plus loin : remplacer UDP par Bluetooth

Quand vous passerez à l'Arduino MEGA 2560 avec Bluetooth, vous devrez :

1. Créer `comm_bt.cpp` à la place de `comm.cpp`
2. Implémenter les mêmes 4 fonctions (`comm_begin`, `comm_receive`, `comm_sendEncoders`, `comm_sendGyro`) mais avec la bibliothèque Bluetooth
3. **Rien d'autre ne change** : `robot_esp32.ino`, `robot.h`, `robot.cpp`, `protocol.h` restent identiques

C'est la puissance du wrapper !

---

⬅ [Précédent — Structure .h/.cpp](./09-structure-projet-lib.md) · [Retour parcours Groupe B](./README.md)
