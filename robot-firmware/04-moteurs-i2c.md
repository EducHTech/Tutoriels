# 04 — Contrôle des moteurs par I2C

> **Durée estimée :** 35 min
> **Prérequis :** [Wrapper UDP](./03-wrapper-udp.md) — `robot.cpp` en mode simulé qui tourne
> **Objectif :** remplacer la simulation des moteurs par la vraie commande I2C du contrôleur moteur

---

## Avant de commencer — lis vraiment ceci

> [!WARNING]
> Ce tuto contient du code à recopier. Mais **recopier sans comprendre ne sert à rien**.
> À chaque bloc de code, il y a une ou plusieurs questions. **Réponds-y dans ta tête** avant de continuer.
> Ton prof pourra te poser ces questions à n'importe quel moment.

---

## C'est quoi I2C ?

Dans le tuto précédent, le robot parlait à l'extérieur (Wi-Fi/UDP). Maintenant il faut qu'il parle à ses **propres composants** : le contrôleur moteur.

Le protocole utilisé s'appelle **I2C** (prononcer "I-deux-C", ou "I-carré-C"). C'est un bus de communication série très répandu dans l'électronique embarquée.

```
ESP32                     Contrôleur moteur
  │                           │
  │──── SDA (données) ────────┤
  │──── SCL (horloge) ────────┤
                              │
                    M1  M2  M3  M4  M5  M6
```

I2C fonctionne avec seulement **2 fils** :
- `SDA` : la ligne de données (Serial DAta)
- `SCL` : l'horloge qui synchronise (Serial CLock)

Plusieurs composants peuvent être branchés sur les mêmes fils. Chacun a une **adresse unique** qui permet de lui parler sans déranger les autres.

> **Notre contrôleur moteur a l'adresse `0x34`** (en hexadécimal).

---

### ⏸ Stop — question 1

> **Pourquoi faut-il une adresse sur le bus I2C ?**
> Réfléchis avant de continuer.

<details>
<summary>💡 Voir la réponse</summary>

Parce que plusieurs composants partagent les mêmes fils SDA/SCL. Sans adresse, tous les composants recevraient tous les messages en même temps et on ne pourrait pas les distinguer. L'adresse, c'est le numéro de porte de l'appartement sur le même palier.

</details>

---

## Les registres du contrôleur moteur

Le contrôleur moteur est un petit ordinateur autonome. Pour lui donner des ordres, on écrit dans ses **registres** : des cases mémoire internes identifiées par un numéro.

| Registre | Adresse | Rôle |
|---|---|---|
| `MOTOR_TYPE_ADDR` | `0x14` | Type de moteur installé |
| `MOTOR_ENCODER_POLARITY_ADDR` | `0x15` | Sens de comptage des encodeurs |
| `MOTOR_FIXED_SPEED_ADDR` | `0x33` | Vitesses des moteurs (commande) |
| `MOTOR_FIXED_PWM_ADDR` | `0x1F` | PWM direct (sans régulation) |

---

### ⏸ Stop — question 2

> **Quelle est la différence entre `MOTOR_FIXED_SPEED_ADDR` et `MOTOR_FIXED_PWM_ADDR` ?**
> L'un utilise un régulateur PID interne, l'autre envoie directement un rapport cyclique.
> Lequel choisis-tu pour un robot qui doit aller droit ? Pourquoi ?

<details>
<summary>💡 Voir la réponse</summary>

`MOTOR_FIXED_SPEED_ADDR` demande au contrôleur de maintenir une **vitesse** (tours/min). Le contrôleur ajuste lui-même le PWM pour compenser la charge, les frottements, la batterie faible. C'est plus précis.

`MOTOR_FIXED_PWM_ADDR` envoie un **rapport cyclique fixe** : le moteur tourne plus ou moins vite selon la charge. Si les deux roues du même côté ont des frottements différents, le robot ne va pas droit.

→ Pour un robot qu'on veut contrôler précisément : `MOTOR_FIXED_SPEED_ADDR`.

</details>

---

## La fonction `WireWriteDataArray`

Pour écrire dans un registre du contrôleur, on suit toujours la même séquence I2C :
1. Ouvrir la communication avec l'adresse du composant
2. Envoyer le numéro du registre cible
3. Envoyer les données
4. Fermer la communication

Plutôt que de répéter ces 4 étapes à chaque fois, on crée une **fonction utilitaire** :

```cpp
bool WireWriteDataArray(uint8_t reg, int8_t* val, unsigned int len)
{
    Wire.beginTransmission(I2C_ADDR);   // 1. Ouvrir avec l'adresse du contrôleur
    Wire.write(reg);                    // 2. Indiquer le registre cible
    for (unsigned int i = 0; i < len; i++)
        Wire.write(val[i]);             // 3. Envoyer les données (1 ou plusieurs octets)
    return (Wire.endTransmission() == 0); // 4. Fermer — retourne true si OK
}
```

### ⏸ Stop — question 3

> **Que retourne `WireWriteDataArray` si le contrôleur ne répond pas ?** (câble débranché, mauvaise adresse…)
> Regarde la ligne `return`.

<details>
<summary>💡 Voir la réponse</summary>

Elle retourne `false`. `Wire.endTransmission()` retourne `0` si tout s'est bien passé, autre chose en cas d'erreur. En retournant `false`, on peut détecter un problème et afficher un message d'erreur dans le Moniteur Série.

</details>

---

## Les types de données : `int` vs `int8_t`

> [!NOTE]
> Ce point est important. Lis-le attentivement.

Dans `RobotState`, les vitesses moteurs sont des `int` (entre -255 et +255).  
Le contrôleur moteur, lui, attend des `int8_t` (entre **-127 et +127**).

| Type | Taille | Plage |
|---|---|---|
| `int` (ESP32) | 32 bits | -2 147 483 648 à +2 147 483 647 |
| `int8_t` | **8 bits** | **-128 à +127** |

Pour convertir, on divise par 2 et on s'assure de ne jamais dépasser les limites :

```cpp
int v = state.motorSpeeds[i] / 2;   // -255..+255  →  -127..+127
if (v >  127) v =  127;             // sécurité haute
if (v < -127) v = -127;             // sécurité basse
speeds[i] = (int8_t)v;
```

### ⏸ Stop — question 4

> **Que se passerait-il si on envoyait directement `255` (un `int`) dans un `int8_t` sans conversion ?**

<details>
<summary>💡 Voir la réponse</summary>

`255` en `int8_t` signé donne `-1`. En binaire, `11111111` s'interprète comme `-1` en complément à deux sur 8 bits. Le moteur irait en sens inverse au lieu d'aller à fond ! Ce genre d'erreur de type est silencieuse : le code compile sans warning, mais le comportement est faux.

</details>

---

## Mise à jour de `robot.cpp`

Tu vas maintenant remplacer le contenu simulé de `robot.cpp` par la vraie commande I2C.  
**Lis le code entier avant de le copier.** Il contient des commentaires qui expliquent chaque étape.

```cpp
// robot.cpp
// Logique robot — commande moteurs par I2C
// Contrôleur : JGB37-520 à l'adresse I2C 0x34

#include "robot.h"
#include <Arduino.h>
#include <Wire.h>

// ── Constantes du contrôleur moteur ───────────────────────────────
#define I2C_ADDR                          0x34
#define MOTOR_TYPE_ADDR                   0x14
#define MOTOR_ENCODER_POLARITY_ADDR       0x15
#define MOTOR_FIXED_SPEED_ADDR            0x33

#define MOTOR_TYPE_JGB37_520_12V_110RPM   3

// ── Fonction utilitaire I2C ────────────────────────────────────────
// Écrit `len` octets dans le registre `reg` du contrôleur.
// Retourne true si le contrôleur a répondu, false sinon.
static bool WireWriteDataArray(uint8_t reg, int8_t* val, unsigned int len = 1)
{
    Wire.beginTransmission(I2C_ADDR);
    Wire.write(reg);
    for (unsigned int i = 0; i < len; i++)
        Wire.write(val[i]);
    return (Wire.endTransmission() == 0);
}

// ── Initialisation ─────────────────────────────────────────────────
void robot_begin()
{
    Wire.begin();   // Démarrer le bus I2C
    delay(200);     // Laisser le contrôleur démarrer

    // Configurer le type de moteur
    int8_t motorType = MOTOR_TYPE_JGB37_520_12V_110RPM;
    if (!WireWriteDataArray(MOTOR_TYPE_ADDR, &motorType))
        Serial.println("[ROBOT] ERREUR : contrôleur moteur I2C non trouvé !");
    delay(5);

    // Configurer la polarité des encodeurs (0 = sens normal)
    int8_t encoderPolarity = 0;
    WireWriteDataArray(MOTOR_ENCODER_POLARITY_ADDR, &encoderPolarity);

    Serial.println("[ROBOT] Contrôleur moteur I2C initialisé");
}

// ── Commande moteurs ───────────────────────────────────────────────
void robot_applyMotors(const RobotState& state)
{
    // Convertir les vitesses de int [-255, +255] vers int8_t [-127, +127]
    int8_t speeds[NB_MOTORS];
    for (int i = 0; i < NB_MOTORS; i++)
    {
        int v = state.motorSpeeds[i] / 2;
        if (v >  127) v =  127;
        if (v < -127) v = -127;
        speeds[i] = (int8_t)v;
    }

    // Envoyer les 6 vitesses en un seul paquet I2C
    if (!WireWriteDataArray(MOTOR_FIXED_SPEED_ADDR, speeds, NB_MOTORS))
        Serial.println("[ROBOT] ERREUR : envoi vitesses moteurs échoué");
}

// ── Arrêt d'urgence ────────────────────────────────────────────────
void robot_emergencyStop(RobotState* state)
{
    for (int i = 0; i < NB_MOTORS; i++)
        state->motorSpeeds[i] = 0;

    robot_applyMotors(*state);   // Applique immédiatement via I2C

    Serial.println("[ROBOT] *** ARRÊT D'URGENCE (watchdog) ***");
}

// ── Servos ─────────────────────────────────────────────────────────
void robot_applyServos(const RobotState& state)
{
    // TODO : servo.write() quand les servos sont branchés
    Serial.print("[SERVOS]");
    for (int i = 0; i < NB_SERVOS; i++)
    {
        Serial.print(" S"); Serial.print(i);
        Serial.print("="); Serial.print(state.servoAngles[i]); Serial.print("°");
    }
    Serial.println();
}

// ── Capteurs ───────────────────────────────────────────────────────
void robot_readSensors(RobotState* state)
{
    // TODO : lire les encodeurs via I2C et le gyro via I2C/SPI
    // Pour l'instant, valeurs simulées
    for (int i = 0; i < NB_MOTORS; i++)
        state->encoderCounts[i] += state->motorSpeeds[i] / 10;

    state->gyroAngleTenths = (state->gyroAngleTenths + 1) % 3600;
}
```

---

### ⏸ Stop — question 5

> **Pourquoi envoie-t-on les 6 vitesses en un seul appel `WireWriteDataArray(…, speeds, NB_MOTORS)` plutôt qu'en 6 appels séparés ?**

<details>
<summary>💡 Voir la réponse</summary>

Chaque appel I2C ouvre et ferme une transmission (beginTransmission / endTransmission). Si on fait 6 appels séparés, les 6 moteurs ne reçoivent pas leur consigne au même instant : les premiers ont déjà changé de vitesse quand les derniers reçoivent encore la leur. En envoyant les 6 valeurs en un seul paquet, la mise à jour est **atomique** — le contrôleur les applique tous ensemble.

</details>

---

## Ce qui ne change pas

`robot.h`, `comm.h`, `comm_udp.cpp`, `protocol.h` et `robot_esp32.ino` **n'ont pas bougé d'une ligne**.  
C'est précisément le but de l'architecture modulaire : on isole les changements dans un seul fichier.

---

## Vérifier que ça marche

1. Téléverse le firmware
2. Ouvre le Moniteur Série (115200)
3. Tu dois voir : `[ROBOT] Contrôleur moteur I2C initialisé`
4. Si tu vois `ERREUR : contrôleur moteur I2C non trouvé !` → vérifie les fils SDA/SCL et l'alimentation du contrôleur
5. Lance `fake_driver_station.py`, envoie `SET_MOTORS:50,50,-50,-50,0,0`
6. Les moteurs 0 et 1 doivent tourner dans un sens, 2 et 3 dans l'autre

---

## Cases à cocher

- [ ] J'ai remplacé `robot.cpp` par la version I2C
- [ ] Le firmware compile sans erreur
- [ ] Le Moniteur Série affiche `Contrôleur moteur I2C initialisé`
- [ ] Les moteurs réagissent à `SET_MOTORS`
- [ ] L'arrêt d'urgence (watchdog) coupe bien les moteurs via I2C

---

## 🎓 Questions pour le prof — à poser à l'oral

> [!NOTE]
> Cette section est pour le **professeur**. Pose ces questions au jeune sans lui montrer les réponses. S'il ne sait pas, c'est qu'il a copié sans lire.

---

**Q1 — Adresse I2C**
> *Quelle est l'adresse I2C du contrôleur moteur ? En décimal, ça donne quoi ?*

Réponse attendue : `0x34` = 52 en décimal. S'il ne sait pas lire l'hexadécimal : problème.

---

**Q2 — Registre de vitesse**
> *Si tu veux que le moteur 3 tourne à vitesse maximale en sens inverse, quelle valeur exacte envoies-tu dans le tableau `speeds` ?*

Réponse attendue : `-127` (ou `-128`, mais on a limité à -127). Il doit savoir que c'est un `int8_t` signé. Si il dit `-255`, il n'a pas compris la conversion.

---

**Q3 — Watchdog**
> *Je débranche le câble réseau. Que se passe-t-il sur le robot, et dans quel délai ?*

Réponse attendue : après 500 ms sans message (`COMM_TIMEOUT_MS`), `comm_isTimedOut()` retourne `true`, `robot_emergencyStop()` est appelée, toutes les vitesses passent à 0 et sont envoyées au contrôleur via I2C.

---

**Q4 — Architecture**
> *Je veux passer du Wi-Fi au Bluetooth. Quels fichiers est-ce que je modifie ? Lesquels est-ce que je ne touche pas ?*

Réponse attendue : je crée `comm_bt.cpp` et je supprime `comm_udp.cpp`. Je ne touche pas à `robot.cpp`, `robot.h`, `comm.h`, `protocol.h`, ni au `.ino`.

---

**Q5 — Type de données**
> *Pourquoi divise-t-on les vitesses moteurs par 2 avant de les envoyer au contrôleur ?*

Réponse attendue : le protocole interne stocke les vitesses en `int` sur [-255, +255]. Le contrôleur I2C attend un `int8_t` sur [-127, +127]. Pour éviter un débordement de type (overflow silencieux), on divise par 2 et on borne.

---

**Q6 — Erreur I2C**
> *Tu branches le robot, tu vois `ERREUR : contrôleur moteur I2C non trouvé !`. Cite 3 causes possibles.*

Réponses attendues (parmi) : fils SDA/SCL inversés, contrôleur non alimenté, mauvaise adresse I2C, fil débranché, conflit de résistances de pull-up.

---

⬅ [Précédent — Wrapper UDP](./03-wrapper-udp.md) · [Retour accueil projet](./README.md)
