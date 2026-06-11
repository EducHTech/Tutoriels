# Projet Robot — Firmware professionnel

> **Pour qui :** tous ceux qui ont terminé le TP Groupe A / Groupe B
> **Prérequis :** [Firmware final ESP32](../groupe-B-robot-esp32/07-robot-final.md) terminé
> **Durée totale estimée :** ~1h30

---

## Contexte

Tu as terminé le TP de découverte : l'ESP32 reçoit des commandes par Wi-Fi et y répond.
C'était bien pour apprendre les bases. Maintenant on passe sur quelque chose de **sérieux**.

Le vrai robot embarque :

- **6 moteurs à courant continu** avec encodeurs
- **3 servomoteurs** (PWM)
- **1 gyroscope**
- Une couche réseau qui devra fonctionner sur **ESP32 (UDP/Wi-Fi)** aujourd'hui, et sur **Arduino MEGA 2560 (Bluetooth)** demain

Un vrai projet ne tient pas dans un seul fichier `.ino` de 200 lignes.
On va donc apprendre à **structurer le code** comme dans l'industrie.

---

## Objectifs

À la fin de ce projet, tu seras capable de :

- [ ] Définir et documenter un **protocole de communication** entre deux systèmes
- [ ] Séparer le code en **modules** avec des fichiers `.h` et `.cpp`
- [ ] Écrire un **wrapper** qui isole la couche réseau du reste du code
- [ ] Simuler le comportement du robot pour tester sans matériel
- [ ] Tester le firmware depuis Python avec un **Fake Driver Station**
- [ ] Contrôler de vrais moteurs via **I2C**
- [ ] Comprendre **pourquoi** cette architecture permet de changer de plateforme sans tout réécrire

---

## Parcours

```
01-protocole.md
    │  Définir le "contrat" de communication
    │  SET_MOTORS, SET_SERVOS, ENCODERS, GYRO
    ▼
02-structure-projet.md
    │  Organiser le code en .h / .cpp
    │  Créer protocol.h et la struct RobotState
    ▼
03-wrapper-udp.md
    │  Écrire comm.h / comm_udp.cpp / robot.h / robot.cpp
    │  Assembler le firmware complet
    │  Tester avec fake_driver_station.py
    ▼
04-moteurs-i2c.md
    │  Remplacer la simulation par la vraie commande I2C
    │  Contrôleur JGB37, registres, conversion de types
    ▼
  🎉 Firmware réel sur ESP32 — et maintenant : migration Auriga !
    ▼
05-capteurs-auriga.md  (Étudiant A)
    │  Gyroscope, batterie, encodeurs on-board
    ▼
06-moteurs-auriga.md  (Étudiants B + C)
    │  Encodeurs I2C + 4 moteurs Hiwonder + 3 servos
    ▼
07-migration-ble.md  (Étudiant C)
    │  Remplacer WiFi/UDP par Bluetooth BLE
    │  Fake Driver Station BLE (Python)
    ▼
08-firmware-final-auriga.md  (Toute l'équipe)
    │  Assembler les 3 parties en un firmware complet
    ▼
  🎉 Robot Auriga contrôlé par BLE !
```

### Parcours ESP32 (étapes 01–04)

- [ ] [01 — Concevoir le protocole de communication](./01-protocole.md) *~20 min*
- [ ] [02 — Organiser le code : fichiers .h et .cpp](./02-structure-projet.md) *~25 min*
- [ ] [03 — Wrapper UDP : la couche communication](./03-wrapper-udp.md) *~40 min*
- [ ] [04 — Contrôle des moteurs par I2C](./04-moteurs-i2c.md) *~35 min*

### Migration Auriga — ME Mega 2560 + BLE (étapes 05–08)

> **Organisation :** les étapes 05, 06 et 07 se font **en parallèle** (3 étudiants simultanément), puis l'étape 08 rassemble tout.

| Étudiant | Étapes | Durée |
|---|---|---|
| **A** | [05 — Capteurs Auriga](./05-capteurs-auriga.md) | ~30 min |
| **B** | [06 — Moteurs Auriga](./06-moteurs-auriga.md) (étapes 4 et 5) | ~25 min |
| **C** | [06 — Servos](./06-moteurs-auriga.md) (étape 6) + [07 — Migration BLE](./07-migration-ble.md) | ~35 min |
| **Tous** | [08 — Firmware final Auriga](./08-firmware-final-auriga.md) | ~30 min |

---

## Ce qu'on construit

```
robot_esp32/
├── robot_esp32.ino   ← setup() + loop() : orchestration seulement
├── protocol.h        ← définitions partagées (struct, constantes)
├── comm.h / comm.cpp ← couche réseau UDP  ← à remplacer pour Bluetooth
├── robot.h / robot.cpp ← logique moteurs, servos, capteurs
└── ...
```

Le fichier `.ino` principal fera **moins de 30 lignes**. Toute la complexité est dans des modules séparés, testables indépendamment.

---

## Outil fourni

[fake_driver_station.py](./fake_driver_station.py) — script Python interactif pour tester chaque commande du protocole sans avoir besoin du vrai Driver Station.

```bash
# Connecte d'abord ton PC au Wi-Fi "Robot-ESP32" (mot de passe : robot1234)
python fake_driver_station.py
```

---

## Et ensuite ?

Une fois ce firmware validé sur ESP32, le passage au MEGA 2560 + Bluetooth ne nécessite de réécrire **qu'un seul fichier** : `comm.cpp`. Le reste du projet est inchangé. C'est ça, une bonne architecture.

---

[⬅ Retour accueil](../README.md)
