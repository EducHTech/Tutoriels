# TP — Contrôle d'un robot par Wi-Fi avec Python et ESP32

> [!IMPORTANT]
> **Règle du TP** : L'utilisation de l'IA est **interdite** pendant ce TP.
> La documentation officielle, les forums et les recherches web sont autorisés.

---

## Qu'est-ce qu'on va construire ?

On va programmer un mini-robot contrôlé à distance par Wi-Fi.

```text
+-----------------------------------+          +-----------------------------------+
|       Driver Station              |          |           Robot                   |
|       (ton ordinateur)            |          |           (ESP32)                 |
|                                   |          |                                   |
|  Python envoie des commandes  ----+--Wi-Fi---+-->  ESP32 reçoit et agit         |
|                                   |  UDP     |     LED, moteurs, capteurs        |
+-----------------------------------+          +-----------------------------------+
```

---

## Qui fait quoi ?

| | **Groupe A — Driver Station** | **Groupe B — Robot** |
|---|---|---|
| Outil | Python (Windows) | Arduino IDE (ESP32) |
| Rôle | Envoyer des commandes | Recevoir et exécuter |
| Langage | Python | C++ |
| Résultat | Un tableau de bord de contrôle | Un robot qui réagit |

Les deux groupes doivent communiquer à des moments clés — ces moments sont appelés **points de synchro** 🔄.

---

## Parcours — par où commencer ?

```
Tout le monde
     │
     ▼
┌─────────────────────────────────────┐
│  00-setup/  ← INSTALLATION          │  ← Commencer ici si c'est ta première fois
│  (à faire une seule fois)           │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│  01-bases-communes/  ← THÉORIE      │  ← Lire en entier (les deux groupes)
│  Réseau, IP, UDP                    │
└─────────────────────────────────────┘
     │
     ├──────────────────┬──────────────────
     ▼                  ▼
┌──────────────┐  ┌──────────────┐
│  groupe-A-   │  │  groupe-B-   │
│  driver-     │  │  robot-      │
│  station/    │  │  esp32/      │
└──────────────┘  └──────────────┘
```

### Étape par étape

- [ ] **Étape 0** — [Installer les outils](./00-setup/README.md) *(à faire une seule fois)*
- [ ] **Étape 1** — [Comprendre le réseau](./01-bases-communes/01-introduction-projet.md) *(tout le monde)*
- [ ] **Étape 2** — Suivre le parcours de **ton** groupe :
  - 👉 [Je suis dans le **Groupe A** (Driver Station)](./groupe-A-driver-station/README.md)
  - 👉 [Je suis dans le **Groupe B** (Robot ESP32)](./groupe-B-robot-esp32/README.md)

---

## Points de synchro 🔄

Ce sont les moments où les deux groupes doivent travailler ensemble.

| N° | Groupe A attend… | Groupe B a terminé… |
|---|---|---|
| 🔄 Synchro 1 | [A-05 — Ping/Pong](./groupe-A-driver-station/05-ping-pong.md) | [B-03 — Recevoir UDP](./groupe-B-robot-esp32/03-recevoir-udp.md) |
| 🔄 Synchro 2 | [A-07 — Driver Station](./groupe-A-driver-station/07-driver-station-finale.md) | [B-04 — Contrôle LED](./groupe-B-robot-esp32/04-controle-led.md) |
| 🔄 Synchro 3 | [A-09 — Joystick](./groupe-A-driver-station/09-joystick-pygame.md) | [B-07 — Firmware final](./groupe-B-robot-esp32/07-robot-final.md) |

---

## J'ai fini en avance ?

Va voir les défis bonus de ton groupe ou aide le groupe partenaire !