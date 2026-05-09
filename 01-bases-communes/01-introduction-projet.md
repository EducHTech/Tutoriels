# 01 — Introduction au projet

> **Pour qui :** les deux groupes
> **Durée estimée :** 10 min
> **Prérequis :** [Installation terminée](../00-setup/README.md)
> **Objectif :** comprendre ce qu'on va construire et qui fait quoi

---

## Ce qu'on va construire

On va créer un système pour contrôler un robot à distance via Wi-Fi.

Il y a deux parties :

```text
+-------------------------------+          +-------------------------------+
|     Driver Station            |          |          Robot                |
|     (ordinateur Windows)      |          |          (ESP-WROOM-32)       |
|                               |          |                               |
|  Python envoie des messages --+--Wi-Fi-->+-- ESP32 reçoit et agit       |
|                               |  UDP     |   LED s'allume                |
|  Reçoit les données capteurs <+----------+-- ESP32 renvoie des données  |
+-------------------------------+          +-------------------------------+
```

C'est exactement comme ça que fonctionnent les robots dans des compétitions comme **FRC** (FIRST Robotics) ou **VEX** : un ordinateur envoie des commandes, le robot exécute.

---

## Qui fait quoi ?

### Groupe A — Driver Station

Tu programmes le **tableau de bord de contrôle** sur l'ordinateur Windows.

Ce que tu vas faire :
- Envoyer des commandes au robot (`LED_ON`, `MOTOR:120`, ...)
- Recevoir les données du robot (`SENSOR:42`)
- Créer un menu de contrôle
- Connecter un joystick

### Groupe B — Robot

Tu programmes le **cerveau du robot** sur l'ESP-WROOM-32.

Ce que tu vas faire :
- Connecter l'ESP32 au Wi-Fi
- Recevoir les commandes
- Faire réagir la LED et les moteurs
- Renvoyer les données des capteurs

---

## Les règles

> [!IMPORTANT]
> **L'utilisation de l'IA (ChatGPT, Copilot, etc.) est interdite pendant ce TP.**
>
> Ce que tu peux utiliser :
> - La documentation officielle (Python, ESP32, Arduino)
> - Les forums (Stack Overflow, etc.)
> - Les recherches Google
> - Les pages de ce tutoriel

---

## Cases à cocher

- [ ] Je sais dans quel groupe je suis (A ou B)
- [ ] Je comprends le rôle de mon groupe dans le projet

---

⬅ [Retour setup](../00-setup/README.md) · [Suivant ➡ Adresse IP et port](./02-adresse-ip-et-port.md)
