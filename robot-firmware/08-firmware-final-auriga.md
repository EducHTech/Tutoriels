# 08 — Firmware Final Auriga

> **Durée estimée :** 30 min  
> **Prérequis :** Étapes 05, 06, 07 terminées par les 3 étudiants  
> **👥 Toute l'équipe** — fusion du travail des 3 étudiants

---

## Contexte

Chaque étudiant a construit et testé un morceau :

| Étudiant | Réalisé |
|---|---|
| A | Gyro, batterie, encodeurs on-board |
| B | Encodeurs I2C + moteurs I2C (Hiwonder) |
| C | Servos + communication BLE |

Maintenant, on assemble tout dans **un seul firmware**.

---

## 🤔 Question de réflexion d'équipe

> Avant de coder quoi que ce soit, discutez entre vous :
>
> Dans `loop()`, il faudra faire 4 choses :
> 1. Lire les commandes BLE entrantes
> 2. Appliquer les commandes aux moteurs et servos
> 3. Lire les capteurs (gyro, encodeurs, batterie)
> 4. Envoyer les données capteurs au driver station
>
> **Est-ce qu'on peut tout mettre dans `loop()` sans structure ?**  
> Regardez comment `robot_esp32.ino` était organisé — qu'avez-vous retenu de ce modèle ?

<details>
<summary>💡 Indice</summary>

Le modèle ESP32 séparait le code en **fonctions** :
- `comm_receive()`, `comm_send()`
- `robot_applyMotors()`, `robot_readSensors()`

Faire pareil ici rend le code **lisible**, **testable**, et **facile à débugger**.

</details>

---

## Structure du firmware

Voici la structure à reproduire. Chaque fichier a un rôle précis :

```
robot_auriga/
├── robot_auriga.ino   ← fichier principal (très court)
├── protocol.h         ← structure RobotState (même que ESP32, 4 moteurs)
├── comm_ble.h/.cpp    ← couche BLE (étudiant C)
└── robot.h/.cpp       ← moteurs, servos, capteurs (étudiants A + B)
```

---

## Étape 8a — `protocol.h` (adapté pour l'Auriga)

### 🎯 Objectif
Adapter la structure `RobotState` pour 4 moteurs et 3 servos.

### 🤔 Question de réflexion
> Sur l'ESP32, `NB_MOTORS` était `6`. Sur l'Auriga, on a **4 moteurs I2C + 2 encodeurs on-board**.  
> Quelle valeur de `NB_MOTORS` choisir pour le firmware Auriga ?

<details>
<summary>💡 Indice</summary>

On commande **4 moteurs** via I2C.  
Les 2 encodeurs on-board (SLOT1/SLOT2) viennent **en plus** — ce sont les moteurs 1 et 2.  
Donc `NB_MOTORS = 4` pour les vitesses, mais on peut garder **6 compteurs d'encodeurs** si on veut tout tracer.

Pour rester simple : `NB_MOTORS = 4`.

</details>

### ✅ Fichier `protocol.h`

```cpp
// protocol.h — Auriga version
#pragma once

#define NB_MOTORS  4
#define NB_SERVOS  3

// Timeout sans commande → arrêt d'urgence (ms)
#define COMM_TIMEOUT_MS  500

struct RobotState {
  // Commandes reçues
  int motorSpeeds[NB_MOTORS]; // -255 à +255
  int servoAngles[NB_SERVOS]; // 0 à 180°

  // Données mesurées
  long encoderCounts[NB_MOTORS]; // ticks
  float gyroAngle;               // degrés
  int   batteryPercent;          // 0 à 100
};
```

---

## Étape 8b — `comm_ble.cpp` (couche communication)

### 🎯 Objectif
Lire les commandes BLE et encoder les données capteurs à renvoyer.

### ✅ Fichier `comm_ble.h`

```cpp
// comm_ble.h
#pragma once
#include "protocol.h"

void comm_begin();
bool comm_receive(RobotState* state); // Retourne true si une commande a été reçue
bool comm_isTimedOut();
void comm_sendSensors(const RobotState& state);
```

### ✅ Fichier `comm_ble.cpp`

```cpp
// comm_ble.cpp
#include "comm_ble.h"
#include <Arduino.h>

// ── Protocole Makeblock (envoi) ────────────────────────────────
static void writeHead() { Serial.write(0xff); Serial.write(0x55); }
static void writeEnd()  { Serial.println(); }

static void sendFloat_BLE(float v) {
  union { uint8_t b[4]; float f; } u;
  u.f = v;
  Serial.write(2); // Type FLOAT
  Serial.write(u.b, 4);
}

static void sendLong_BLE(long v) {
  union { uint8_t b[4]; long l; } u;
  u.l = v;
  Serial.write(6); // Type LONG
  Serial.write(u.b, 4);
}

static void sendByte_BLE(uint8_t v) {
  Serial.write(1); // Type BYTE
  Serial.write(v);
}

// ── Réception des commandes ────────────────────────────────────
static String    inputBuffer  = "";
static uint32_t  lastMsgMs    = 0;

void comm_begin() {
  Serial.begin(115200);
  lastMsgMs = millis();
}

bool comm_receive(RobotState* state) {
  bool gotCommand = false;

  while (Serial.available() > 0) {
    char c = (char)Serial.read();

    if (c == '\n') {
      inputBuffer.trim();

      if (inputBuffer.startsWith("SET_MOTORS:")) {
        // Exemple : SET_MOTORS:100,100,-100,-100
        String data = inputBuffer.substring(11);
        int speeds[NB_MOTORS] = {0};
        int idx = 0;
        while (idx < NB_MOTORS && data.length() > 0) {
          int comma = data.indexOf(',');
          String token = (comma >= 0) ? data.substring(0, comma) : data;
          speeds[idx++] = token.toInt();
          data = (comma >= 0) ? data.substring(comma + 1) : "";
        }
        for (int i = 0; i < NB_MOTORS; i++)
          state->motorSpeeds[i] = speeds[i];
        lastMsgMs  = millis();
        gotCommand = true;
      }

      else if (inputBuffer.startsWith("SET_SERVOS:")) {
        // Exemple : SET_SERVOS:90,45,135
        String data = inputBuffer.substring(11);
        int angles[NB_SERVOS] = {90, 90, 90};
        int idx = 0;
        while (idx < NB_SERVOS && data.length() > 0) {
          int comma = data.indexOf(',');
          String token = (comma >= 0) ? data.substring(0, comma) : data;
          angles[idx++] = token.toInt();
          data = (comma >= 0) ? data.substring(comma + 1) : "";
        }
        for (int i = 0; i < NB_SERVOS; i++)
          state->servoAngles[i] = angles[i];
        lastMsgMs  = millis();
        gotCommand = true;
      }

      else if (inputBuffer == "PING") {
        writeHead();
        Serial.write(4); Serial.write(4); Serial.print("PONG");
        writeEnd();
        lastMsgMs = millis();
      }

      inputBuffer = "";
    } else {
      inputBuffer += c;
    }
  }

  return gotCommand;
}

bool comm_isTimedOut() {
  return (millis() - lastMsgMs) > COMM_TIMEOUT_MS;
}

void comm_sendSensors(const RobotState& state) {
  // Frame : [FF 55] [gyro:float] [bat:byte] [enc0..3:long×4] [0A]
  writeHead();
  sendFloat_BLE(state.gyroAngle);
  sendByte_BLE((uint8_t)state.batteryPercent);
  for (int i = 0; i < NB_MOTORS; i++)
    sendLong_BLE(state.encoderCounts[i]);
  writeEnd();
}
```

---

## Étape 8c — `robot.cpp` (moteurs, servos, capteurs)

### 🎯 Objectif
Assembler le code des étapes 05 et 06 dans `robot.cpp`.

### ✅ Fichier `robot.h`

```cpp
// robot.h
#pragma once
#include "protocol.h"

void robot_begin();
void robot_applyMotors(const RobotState& state);
void robot_applyServos(const RobotState& state);
void robot_readSensors(RobotState* state);
void robot_emergencyStop(RobotState* state);
```

### ✅ Fichier `robot.cpp`

```cpp
// robot.cpp — Auriga
#include "robot.h"
#include <Arduino.h>
#include <Wire.h>
#include <Servo.h>
#include <MeAuriga.h>

// ── Moteurs I2C (Hiwonder 4-Channel Encoder Motor Driver) ─────────────────────────
#define I2C_ADDR         0x34
#define MOTOR_TYPE_ADDR  0x14
#define MOTOR_SPEED_ADDR 0x33
#define MOTOR_TYPE_JGB37 3

// ── Servos ────────────────────────────────────────────────────
static Servo servos[NB_SERVOS];
static const int SERVO_PINS[NB_SERVOS] = {44, A3, A2};

// ── Gyroscope ─────────────────────────────────────────────────
static MeGyro gyro(1, 0x69);

// ── Encodeurs on-board ────────────────────────────────────────
MeEncoderOnBoard Encoder_1(SLOT1);
MeEncoderOnBoard Encoder_2(SLOT2);

void isr_encoder1() {
  if (digitalRead(Encoder_1.getPortB()) == 0) Encoder_1.pulsePosMinus();
  else Encoder_1.pulsePosPlus();
}
void isr_encoder2() {
  if (digitalRead(Encoder_2.getPortB()) == 0) Encoder_2.pulsePosMinus();
  else Encoder_2.pulsePosPlus();
}

ISR(TIMER1_COMPA_vect) {
  Encoder_1.updateSpeed();
  Encoder_2.updateSpeed();
}

// ── Initialisation ─────────────────────────────────────────────
void robot_begin() {
  Wire.begin();
  delay(200);

  // Moteurs I2C
  int8_t type = MOTOR_TYPE_JGB37;
  Wire.beginTransmission(I2C_ADDR);
  Wire.write(MOTOR_TYPE_ADDR);
  Wire.write((uint8_t)type);
  Wire.endTransmission();

  // Servos
  for (int i = 0; i < NB_SERVOS; i++) {
    servos[i].attach(SERVO_PINS[i]);
    servos[i].write(90);
  }

  // Gyroscope
  gyro.begin();

  // Encodeurs + timer
  attachInterrupt(Encoder_1.getIntNum(), isr_encoder1, RISING);
  attachInterrupt(Encoder_2.getIntNum(), isr_encoder2, RISING);
  TCCR1A = _BV(WGM10);
  TCCR1B = _BV(CS11) | _BV(WGM12);
  TIMSK1 = _BV(OCIE1A);
  OCR1A  = 0xF9;

  Serial.println("[ROBOT] Auriga pret");
}

// ── Moteurs ────────────────────────────────────────────────────
void robot_applyMotors(const RobotState& state) {
  int8_t speeds[NB_MOTORS];
  for (int i = 0; i < NB_MOTORS; i++) {
    int v = state.motorSpeeds[i] / 2; // 255 → 127
    speeds[i] = (int8_t)constrain(v, -127, 127);
  }
  Wire.beginTransmission(I2C_ADDR);
  Wire.write(MOTOR_SPEED_ADDR);
  for (int i = 0; i < NB_MOTORS; i++) Wire.write((uint8_t)speeds[i]);
  Wire.endTransmission();
}

// ── Arrêt d'urgence ────────────────────────────────────────────
void robot_emergencyStop(RobotState* state) {
  for (int i = 0; i < NB_MOTORS; i++) state->motorSpeeds[i] = 0;
  robot_applyMotors(*state);
  Serial.println("[ROBOT] *** ARRET D URGENCE ***");
}

// ── Servos ─────────────────────────────────────────────────────
void robot_applyServos(const RobotState& state) {
  for (int i = 0; i < NB_SERVOS; i++) {
    int angle = constrain(state.servoAngles[i], 0, 180);
    servos[i].write(angle);
  }
}

// ── Capteurs ───────────────────────────────────────────────────
void robot_readSensors(RobotState* state) {
  // Gyroscope
  gyro.update();
  state->gyroAngle = gyro.getAngleZ();

  // Batterie
  float v = analogRead(A4) * 5.0 / 1023.0 * 10.0;
  float p = (v - 9.0) / (12.6 - 9.0) * 100.0; // LiPo 3S : 9.0V=0%, 12.6V=100%
  state->batteryPercent = (int)constrain(p, 0, 100);

  // Encodeurs on-board (moteurs 0 et 1)
  state->encoderCounts[0] = Encoder_1.getCurPos();
  state->encoderCounts[1] = Encoder_2.getCurPos();

  // Encodeurs I2C (moteurs 2 et 3) — lecture depuis le module Hiwonder
  Wire.requestFrom(I2C_ADDR, 16);
  for (int m = 0; m < NB_MOTORS; m++) {
    if (Wire.available() >= 4) {
      uint8_t b[4];
      for (int k = 0; k < 4; k++) b[k] = Wire.read();
      // Seulement écraser les indices 2 et 3 (on-board = 0 et 1 déjà lus)
      if (m >= 2) {
        state->encoderCounts[m] = (long)b[0] | ((long)b[1] << 8)
                                 | ((long)b[2] << 16) | ((long)b[3] << 24);
      }
    }
  }
}
```

---

## Étape 8d — `robot_auriga.ino` (fichier principal)

### 🎯 Objectif
Assembler les modules en un `loop()` propre et lisible.

### ✅ Fichier principal

```cpp
// robot_auriga.ino
// Firmware principal Auriga — structure identique à robot_esp32.ino

#include "comm_ble.h"
#include "robot.h"

RobotState state;

void setup() {
  memset(&state, 0, sizeof(state));

  // Servos en position centrale par défaut
  for (int i = 0; i < NB_SERVOS; i++)
    state.servoAngles[i] = 90;

  comm_begin();
  robot_begin();
}

void loop() {
  // 1. Recevoir et appliquer les commandes
  if (comm_receive(&state)) {
    robot_applyMotors(state);
    robot_applyServos(state);
  }

  // 2. Watchdog : arrêt si silence trop long
  if (comm_isTimedOut()) {
    robot_emergencyStop(&state);
  }

  // 3. Lire les capteurs et envoyer les données
  robot_readSensors(&state);
  comm_sendSensors(state);

  delay(20); // 50 Hz
}
```

> 💡 **Compare avec `robot_esp32.ino`** — la structure est quasi identique.  
> C'est exactement le but de l'architecture modulaire : changer de plateforme sans tout réécrire.

---

## 🧪 Test final complet

### Checklist avant de tester

- [ ] Firmware téléversé sur l'Auriga
- [ ] Auriga allumé + BLE actif
- [ ] Adresse MAC mise à jour dans `fake_driver_station_ble.py`
- [ ] `pip install bleak` fait

### Séquence de test

```
python fake_driver_station_ble.py
```

1. **PING** → doit répondre `PONG`
2. **SET_MOTORS:50,50,50,50** → les 4 roues tournent
3. **SET_MOTORS:0,0,0,0** → arrêt
4. **SET_SERVOS:0,90,180** → les 3 servos bougent
5. **Lire capteurs** → gyro ≈ 0°, batterie ≈ xx%, encodeurs augmentent quand le robot avance
6. **Couper la connexion Python** → le robot doit s'arrêter tout seul (watchdog)

### 🔍 Debug rapide

| Symptôme | Cause probable |
|---|---|
| Les moteurs ne répondent pas | Vérifier l'adresse I2C avec un scanner I2C |
| Les encodeurs on-board à 0 | Timer ISR non configuré, relire étape 05 |
| Pas de connexion BLE | Mauvaise adresse MAC ou firmware pas téléversé |
| Robot ne s'arrête pas au watchdog | `COMM_TIMEOUT_MS` ou `millis()` mal utilisé |
| Servo vibre | Alimentation insuffisante, utiliser alim séparée |

---

## 🎉 Félicitations !

Tu as construit un firmware professionnel pour un vrai robot :

- ✅ Architecture modulaire (`.h` / `.cpp`)
- ✅ 4 moteurs contrôlés via I2C
- ✅ 3 servos PWM
- ✅ Gyroscope, batterie, encodeurs
- ✅ Communication BLE bidirectionnelle
- ✅ Watchdog de sécurité
- ✅ Protocole commun avec le Groupe A (Driver Station)

**Et maintenant ?** → Vois les [bonus](../groupe-B-robot-esp32/08-bonus.md) pour aller plus loin.
