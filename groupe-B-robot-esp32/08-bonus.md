# B-08 — Défis bonus

> **Pour qui :** Groupe B — si tu as fini en avance
> **Prérequis :** [Firmware final](./07-robot-final.md)

---

Bravo ! Tu as terminé le parcours principal. Voici des défis pour aller plus loin.

---

## Défi 1 — Ajouter un buzzer

Branche un buzzer sur une broche GPIO (ex. GPIO 5).

Ajoute les commandes `BUZZER_ON` et `BUZZER_OFF` :

```cpp
const int BUZZER_PIN = 5;
pinMode(BUZZER_PIN, OUTPUT);
```

```cpp
else if (commande == "BUZZER_ON")
{
    digitalWrite(BUZZER_PIN, HIGH);
}
else if (commande == "BUZZER_OFF")
{
    digitalWrite(BUZZER_PIN, LOW);
}
```

---

## Défi 2 — Deux moteurs indépendants

Si tu as un driver moteur L298N ou DRV8833 :

Ajoute deux broches de contrôle (ex. GPIO 25 et GPIO 26) et utilise `analogWrite()` pour la vitesse.

Cherche dans la documentation Arduino : "ESP32 analogWrite" ou "ESP32 ledc".

---

## Défi 3 — Heartbeat côté robot

Si le robot ne reçoit plus de `HEARTBEAT` depuis plus de 2 secondes → arrêter les moteurs automatiquement.

```cpp
unsigned long dernierHeartbeat = 0;

// Dans loop(), vérifier régulièrement :
if (millis() - dernierHeartbeat > 2000)
{
    // Arrêt d'urgence !
    Serial.println("TIMEOUT - Arrêt d'urgence !");
}

// Quand on reçoit HEARTBEAT :
else if (commande == "HEARTBEAT")
{
    dernierHeartbeat = millis();
}
```

> [!TIP]
> `millis()` retourne le nombre de millisecondes depuis le démarrage de l'ESP32. C'est l'équivalent de `time.time()` en Python.

---

## Défi 4 — Indicator LED (état du robot)

Fais clignoter la LED différemment selon l'état :

- Pas de Wi-Fi → clignotement rapide (100 ms)
- Wi-Fi connecté, pas de message → clignotement lent (1 s)
- Message reçu → LED allumée 200 ms puis éteinte

---

## Défi 5 — Niveau "batterie" simulé

Renvoi une valeur simulée de batterie qui **diminue progressivement** :

```cpp
int niveauBatterie = 100;

// Dans traiterCommande :
else if (commande == "GET_BATTERY")
{
    if (niveauBatterie > 0) niveauBatterie--;   // Simuler la décharge
    String reponse = "BATTERY:" + String(niveauBatterie);
    udp.beginPacket(udp.remoteIP(), udp.remotePort());
    udp.print(reponse);
    udp.endPacket();
}
```

---

⬅ [Précédent — Firmware final](./07-robot-final.md) · [Retour accueil](../README.md)
