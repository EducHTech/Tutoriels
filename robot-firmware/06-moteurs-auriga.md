# 06 — Moteurs et Servos sur l'Auriga

> **Durée estimée :** 40 min  
> **Prérequis :** [Moteurs I2C ESP32](./04-moteurs-i2c.md) — tu connais déjà le principe I2C  
> **Matériel :** carte ME Auriga + module [Hiwonder 4-Channel Encoder Motor Driver](https://www.hiwonder.com/collections/vendors?q=Hiwonder) + servos  
> **👤 Étudiants B et C** — travail en parallèle  
> - **Étudiant B** : Étapes 4 et 5 (Encodeurs I2C + Moteurs I2C)  
> - **Étudiant C** : Étape 6 (Servos) — peut démarrer en parallèle

---

## Rappel rapide

Sur l'ESP32, tu utilisais un contrôleur moteur I2C à l'adresse `0x34` pour piloter les moteurs.  
Sur l'Auriga, les moteurs sont répartis en **deux groupes** :

| Groupe | Moteurs | Méthode de lecture |
|---|---|---|
| On-board | M1 et M2 (SLOT1/SLOT2) | Interruptions (Encodeur\_1 / Encodeur\_2) — étape 05 |
| Module Hiwonder | M3, M4, M5, M6 (4 canaux I2C) | Registres I2C à l'adresse `0x34` |

Le protocole I2C pour le module [Hiwonder 4-Channel Encoder Motor Driver](https://www.hiwonder.com/collections/vendors?q=Hiwonder) est **identique** à celui de l'ESP32 — même adresse, même registres.

---

## Étape 4 — Lire les encodeurs via I2C (module Hiwonder)

### 🎯 Objectif
Afficher les positions des 4 encodeurs du module Hiwonder dans le moniteur série.

### 🤔 Question de réflexion
> Le code `MiniRobot/test_i2c/test_i2c.ino` montre comment **écrire** une vitesse.  
> Mais pour **lire** les encodeurs, il faut un registre différent — et le fabricant fournit des exemples.
>
> Avant de coder : **quelle fonction Arduino permet de lire des octets depuis un périphérique I2C** ?  
> (Cherche dans la référence Arduino si tu ne sais pas.)

<details>
<summary>💡 Indice</summary>

Pour lire des données I2C :
```cpp
Wire.requestFrom(adresse, nb_octets); // Demande des octets
while (Wire.available()) {
  uint8_t b = Wire.read(); // Lit octet par octet
}
```

</details>

### 📌 Ta mission

1. **Lis le code de référence** `MiniRobot/test_i2c/test_i2c.ino` pour comprendre comment le module est initialisé (`MOTOR_TYPE_ADDR`, `MOTOR_ENCODER_POLARITY_ADDR`).

2. **Trouve les exemples officiels** dans le **Google Drive du fabricant Hiwonder** (demande le lien à ton prof).  
   Tu cherches : l'exemple de lecture d'encodeurs pour le `4-Channel Encoder Motor Driver`.

3. **Identifie** :
   - Le registre de lecture des encodeurs (quel numéro ?)
   - Le nombre d'octets à lire par moteur
   - L'ordre des octets (little-endian ou big-endian ?)

4. **Écris le code** qui affiche les 4 positions dans le moniteur série.  
   Utilise `Wire.requestFrom()` et `Wire.read()`.

### 🧪 Test attendu
- Tourne une roue à la main → le compteur correspondant change
- Les 3 autres compteurs ne bougent pas

### 🔍 Debug rapide
| Symptôme | Cause probable |
|---|---|
| Tous les compteurs à 0 | Module I2C non connecté, ou mauvaise adresse |
| Valeurs toutes identiques | Mauvais registre de lecture |
| Erreur I2C | Vérifier câbles SDA/SCL et alimentation du module |

---

## Étape 5 — Faire tourner les 4 moteurs (I2C)

### 🎯 Objectif
Envoyer une vitesse à chacun des 4 moteurs Hiwonder via I2C.

### 🤔 Question de réflexion
> Tu connais déjà ce registre depuis le TP ESP32 : `0x33` (MOTOR_FIXED_SPEED_ADDR).  
> Dans l'ancien code, on envoyait **plusieurs vitesses** en `int8_t` (−127 à +127).  
>
> Maintenant il y a **4 moteurs Hiwonder**. Qu'est-ce qui change dans le code ?

<details>
<summary>💡 Indice</summary>

Seulement le nombre d'octets à envoyer : **4 au lieu de 6**.  
Le reste (adresse I2C `0x34`, registre, format `int8_t`) est identique.

</details>

### ✅ Code à compléter

```cpp
#include <Wire.h>

#define I2C_ADDR             0x34
#define MOTOR_TYPE_ADDR      0x14
#define MOTOR_SPEED_ADDR     0x33
#define MOTOR_TYPE_JGB37     3

void robot_init() {
  Wire.begin();
  delay(200);

  // Configure le type de moteur (JGB37-520)
  int8_t type = MOTOR_TYPE_JGB37;
  Wire.beginTransmission(I2C_ADDR);
  Wire.write(MOTOR_TYPE_ADDR);
  Wire.write((uint8_t)type);
  Wire.endTransmission();
  delay(5);

  Serial.println("Contrôleur moteur I2C prêt");
}

void set_motors(int8_t m1, int8_t m2, int8_t m3, int8_t m4) {
  Wire.beginTransmission(I2C_ADDR);
  Wire.write(MOTOR_SPEED_ADDR);
  Wire.write(m1);
  Wire.write(m2);
  Wire.write(m3);
  Wire.write(m4);
  Wire.endTransmission();
}

void setup() {
  Serial.begin(115200);
  robot_init();
}

void loop() {
  // Test : avance 2 sec, stop 1 sec
  Serial.println("Avance !");
  set_motors(60, 60, 60, 60); // TODO : ajuste les signes selon ton câblage
  delay(2000);

  Serial.println("Stop");
  set_motors(0, 0, 0, 0);
  delay(1000);

  // TODO : essaie de faire tourner le robot (deux moteurs dans un sens, deux dans l'autre)
}
```

> 💡 Si un moteur tourne dans le mauvais sens, **inverse le signe** de sa vitesse.

### 🧪 Test attendu
- Les 4 roues tournent toutes dans le même sens → robot avance
- `set_motors(0,0,0,0)` → arrêt immédiat

### 🔍 Debug rapide
| Symptôme | Cause probable |
|---|---|
| Aucun moteur ne tourne | Module I2C non alimenté ou mauvaise adresse |
| Seulement 2 moteurs tournent | Connexion I2C intermittente |
| Robot tourne en cercle | Un ou plusieurs signes de vitesse inversés |

---

## Étape 6 — Contrôler 3 servos (D44, A3, A2)

### 🎯 Objectif
Envoyer des angles à 3 servomoteurs connectés aux pins **D44**, **A3** et **A2**.

### 🤔 Question de réflexion
> La bibliothèque `Servo.h` a une méthode `attach(pin)` et une méthode `write(angle)`.  
> L'angle va de **0 à 180 degrés**.  
>
> Quelle position correspond au **centre** d'un servo ?

<details>
<summary>💡 Indice</summary>

Le centre d'un servo = **90°** (milieu de la plage 0–180).  
C'est souvent la position de repos à utiliser dans `setup()`.

</details>

### ✅ Code à compléter

```cpp
#include <Servo.h>

Servo servo0; // Connecté à D44
Servo servo1; // Connecté à A3  (= pin 57 sur Mega)
Servo servo2; // Connecté à A2  (= pin 56 sur Mega)

void setup() {
  Serial.begin(115200);

  servo0.attach(44);  // D44
  servo1.attach(A3);  // A3
  servo2.attach(A2);  // A2

  // TODO : mettre les 3 servos en position centrale
  servo0.write(???);
  servo1.write(???);
  servo2.write(???);

  delay(500);
  Serial.println("Servos prêts");
}

void loop() {
  // Test : balayage 0° → 180° → 0°
  for (int angle = 0; angle <= 180; angle += 10) {
    servo0.write(angle);
    // TODO : applique le même angle aux deux autres servos
    delay(50);
  }

  for (int angle = 180; angle >= 0; angle -= 10) {
    servo0.write(angle);
    // TODO : applique le même angle aux deux autres servos
    delay(50);
  }
}
```

### 🧪 Test attendu
- Les 3 servos bougent de 0° à 180° puis reviennent
- Aucun servo ne vibre ou ne "force" en fin de course

### 🔍 Debug rapide
| Symptôme | Cause probable |
|---|---|
| Servo ne répond pas | Mauvaise pin (revérifie D44 vs A3 vs A2) |
| Servo vibre en permanence | Mauvais signal PWM, essaie `servo.detach()` puis `attach()` |
| Erreur `Servo.h not found` | Bibliothèque standard Arduino, doit être présente |
| Le Mega redémarre | Servo consomme trop → alimentation séparée nécessaire |

---

## ✅ Récap — ce que tu sais maintenant

- [x] Lire les encodeurs via I2C depuis le module Hiwonder
- [x] Envoyer des vitesses à 4 moteurs via I2C (registre `0x33`)
- [x] Contrôler 3 servos avec `Servo.h`

**Prochaine étape :** rejoins les autres étudiants pour l'[étape 08 — Firmware final](./08-firmware-final-auriga.md).
