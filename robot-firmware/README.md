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
    │  Écrire comm.h / comm.cpp / robot.h / robot.cpp
    │  Assembler le firmware complet
    │  Tester avec fake_driver_station.py
    ▼
  🎉 Firmware structuré et testable !
```

- [ ] [01 — Concevoir le protocole de communication](./01-protocole.md) *~20 min*
- [ ] [02 — Organiser le code : fichiers .h et .cpp](./02-structure-projet.md) *~25 min*
- [ ] [03 — Wrapper UDP : la couche communication](./03-wrapper-udp.md) *~40 min*

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
