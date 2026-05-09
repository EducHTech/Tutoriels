# B-01 — Découverte d'Arduino IDE

> **Pour qui :** Groupe B
> **Durée estimée :** 15 min
> **Prérequis :** [Arduino IDE installé](../00-setup/06-installer-arduino-ide-esp32.md)
> **Objectif :** créer et téléverser ton premier programme sur l'ESP-WROOM-32

---

## L'interface d'Arduino IDE

Quand tu ouvres Arduino IDE, voici les zones principales :

```text
+--------------------------------------------------+
|  Barre de menu (Fichier, Outils...)              |
+--------------------------------------------------+
|  ✓ (Vérifier)   → (Téléverser)  | Moniteur Série|
+--------------------------------------------------+
|                                                  |
|  Zone de code ← tu écris ici                     |
|                                                  |
+--------------------------------------------------+
|  Zone de messages (erreurs, progression...)      |
+--------------------------------------------------+
```

- **✓ Vérifier** → compile le code (cherche les erreurs) sans envoyer sur la carte
- **→ Téléverser** → compile et envoie sur l'ESP32
- **Moniteur Série** → affiche les messages envoyés par l'ESP32

---

## Structure d'un programme Arduino

Tout programme Arduino a cette structure :

```cpp
void setup()
{
    // Code exécuté UNE FOIS au démarrage
}

void loop()
{
    // Code exécuté EN BOUCLE indéfiniment
}
```

C'est comme ça à chaque fois. Tu n'as jamais besoin de changer cette structure de base.

---

## Premier programme — Faire clignoter la LED

L'ESP-WROOM-32 a une petite LED bleue intégrée sur la broche **GPIO 2**.

Copie ce code dans Arduino IDE :

```cpp
const int LED_PIN = 2;  // GPIO 2 = LED intégrée

void setup()
{
    Serial.begin(115200);          // Démarrer la communication série
    pinMode(LED_PIN, OUTPUT);      // LED en mode sortie

    Serial.println("ESP32 démarré !");
}

void loop()
{
    digitalWrite(LED_PIN, HIGH);   // Allumer la LED
    Serial.println("LED ON");
    delay(500);                    // Pause 500 ms

    digitalWrite(LED_PIN, LOW);    // Éteindre la LED
    Serial.println("LED OFF");
    delay(500);
}
```

---

## Téléverser sur l'ESP32

1. Branche l'ESP32 en USB
2. Vérifie : **Outils → Type de carte → ESP32 Dev Module**
3. Vérifie : **Outils → Port → COM X** (choisir le bon port)
4. Clique sur **→ Téléverser**
5. Attends la barre de progression
6. Ouvre le **Moniteur Série** (icône en haut à droite)
7. Règle la vitesse sur **115200**

Tu dois voir la LED clignoter et dans le Moniteur Série :

```text
ESP32 démarré !
LED ON
LED OFF
LED ON
...
```

---

## Comprendre le code

### `Serial.begin(115200)`

Démarre la communication avec l'ordinateur via le câble USB, à la vitesse 115200 bauds.

### `pinMode(LED_PIN, OUTPUT)`

Configure la broche GPIO 2 en **sortie** : on va lui envoyer du courant.

### `digitalWrite(LED_PIN, HIGH/LOW)`

- `HIGH` = allumer (envoi de courant sur la broche)
- `LOW` = éteindre

### `delay(500)`

Pause de 500 millisecondes (= 0.5 seconde).

---

## Cases à cocher

- [ ] Arduino IDE est ouvert avec la bonne carte et le bon port
- [ ] Le programme compile sans erreur (bouton ✓)
- [ ] Le programme est téléversé sur l'ESP32
- [ ] La LED clignote
- [ ] Le Moniteur Série affiche les messages

---

> [!WARNING]
> Si le téléversement échoue avec une erreur "Connecting...", appuie sur le **bouton BOOT** de l'ESP32 au moment où les points `....` apparaissent dans la zone de messages.

---

⬅ [Retour parcours Groupe B](./README.md) · [Suivant ➡ Connexion Wi-Fi](./02-connexion-wifi.md)
