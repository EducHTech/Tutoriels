# B-09 — Organiser son code : fichiers `.h` et `.cpp`

> **Pour qui :** Groupe B
> **Durée estimée :** 25 min
> **Prérequis :** [Protocole de communication](./08-protocole-robot.md)
> **Objectif :** comprendre pourquoi et comment séparer son code en plusieurs fichiers

---

## Le problème du fichier unique

Jusqu'ici, tout notre code tenait dans un seul fichier `.ino`.  
Pour un petit programme, c'est parfait. Pour un robot complet avec 6 moteurs, 3 servos, un gyro et une couche réseau, ça devient vite illisible.

Imagine un livre où toutes les pages se suivent sans chapitres, sans table des matières. Tu ne t'y retrouverais pas.

**La solution :** séparer le code en **modules**.

---

## Les fichiers `.h` et `.cpp`

En C++, un module se compose de deux fichiers :

| Fichier | Rôle | Analogie |
|---|---|---|
| `.h` (header) | La **liste de ce que le module offre** | La table des matières |
| `.cpp` | Le **code qui fait vraiment le travail** | Le contenu des chapitres |

Le `.h` dit *quoi*. Le `.cpp` dit *comment*.

### Exemple simple

`led.h` — ce que le module offre :
```cpp
// led.h
void ledOn();
void ledOff();
```

`led.cpp` — comment ça marche :
```cpp
// led.cpp
#include "led.h"
#include <Arduino.h>

void ledOn()  { digitalWrite(2, HIGH); }
void ledOff() { digitalWrite(2, LOW);  }
```

Ton `.ino` principal utilise le module :
```cpp
// robot.ino
#include "led.h"

void setup() { ledOn(); }
void loop()  {}
```

---

## La structure du projet

Voici l'organisation que l'on va construire :

```
robot_esp32/
├── robot_esp32.ino       ← fichier principal (setup/loop)
├── protocol.h            ← définitions du protocole (constantes, struct)
├── comm.h                ← déclaration de la couche communication
├── comm.cpp              ← implémentation UDP (ou Bluetooth plus tard)
├── robot.h               ← déclaration de la logique robot
└── robot.cpp             ← implémentation moteurs, servos, capteurs
```

> [!TIP]
> Tous ces fichiers doivent être dans le **même dossier**. Arduino IDE les compilera tous ensemble automatiquement.

---

## Créer la structure dans Arduino IDE

1. Dans Arduino IDE, crée un nouveau sketch : **Fichier → Nouveau**
2. Sauvegarde-le immédiatement : **Fichier → Enregistrer sous** → nomme-le `robot_esp32`
3. Arduino IDE crée un dossier `robot_esp32/` avec `robot_esp32.ino` dedans
4. Pour ajouter un fichier `.h` ou `.cpp` : clique sur la **flèche ▾** en haut à droite de l'onglet des fichiers, puis **Nouvel onglet**

> [!NOTE]
> Quand Arduino IDE te demande le nom, écris bien l'extension : `comm.h`, `comm.cpp`, etc.

---

## `protocol.h` — Les définitions partagées

Ce fichier contient les constantes et la structure de données utilisées **partout** dans le projet. On le crée en premier.

Crée `protocol.h` et copie :

```cpp
// protocol.h
// Définitions du protocole de communication Robot <-> Driver Station
//
// Ce fichier est inclus par tous les autres modules.
// Il ne contient que des définitions, pas de code exécutable.

#pragma once   // Évite les inclusions multiples

// --- Port réseau ---
#define ROBOT_PORT 4210

// --- Limites ---
#define NB_MOTORS  6
#define NB_SERVOS  3

// --- Structure des données du robot ---
// Regroupe tout ce que le robot connaît de lui-même

struct RobotState
{
    // Commandes reçues
    int  motorSpeeds[NB_MOTORS];   // vitesses moteurs : -255 à +255
    int  servoAngles[NB_SERVOS];   // angles servos    : 0 à 180°

    // Données mesurées
    long encoderCounts[NB_MOTORS]; // positions encodeurs (ticks)
    int  gyroAngleTenths;          // angle gyro en dixièmes de degrés
};
```

### Qu'est-ce que `#pragma once` ?

Si plusieurs fichiers incluent `protocol.h`, sans protection on pourrait l'inclure deux fois et avoir des erreurs. `#pragma once` dit au compilateur : « inclus ce fichier **une seule fois**, peu importe combien de fois on le demande. »

### Qu'est-ce qu'une `struct` ?

Une `struct` (structure) regroupe plusieurs variables sous un seul nom.

```cpp
struct RobotState état;
état.gyroAngleTenths = 452;    // 45.2°
état.motorSpeeds[0] = 100;     // moteur 0 à 100
```

C'est comme une fiche technique : toutes les infos du robot au même endroit.

---

## Cases à cocher

- [ ] J'ai créé le dossier `robot_esp32/` et le fichier `robot_esp32.ino`
- [ ] J'ai créé `protocol.h` avec le contenu ci-dessus
- [ ] Je comprends le rôle de `#pragma once`
- [ ] Je comprends ce qu'est une `struct`

---

## Mini-quiz

**Question :** Pourquoi sépare-t-on le fichier `.h` du fichier `.cpp` ?

<details>
<summary>💡 Voir la réponse</summary>

Le `.h` expose **l'interface** (ce que le module peut faire) sans révéler les détails internes. Les autres fichiers n'ont besoin que du `.h` pour utiliser le module. Le `.cpp` contient l'implémentation — si on la change (par exemple, remplacer UDP par Bluetooth), les autres fichiers n'ont pas besoin d'être modifiés.

</details>

---

⬅ [Précédent — Protocole](./08-protocole-robot.md) · [Suivant ➡ Wrapper UDP](./10-wrapper-udp.md)
