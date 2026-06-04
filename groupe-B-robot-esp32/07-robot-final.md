# B-07 — Firmware final

> **Pour qui :** Groupe B
> **Durée estimée :** 20 min
> **Prérequis :** [Lecture capteur](./06-lecture-capteur.md)
> **Objectif :** assembler toutes les fonctionnalités en un seul firmware complet

---

> [!IMPORTANT]
> **🔄 Point de synchro 3** — quand ce firmware tourne, préviens le Groupe A !
> C'est le test final : joystick → robot → capteurs → Driver Station.

---

## Le firmware complet

```cpp
#include <WiFi.h>
#include <WiFiUdp.h>

// === Paramètres du hotspot ===
const char* WIFI_SSID     = "Robot-ESP32";
const char* WIFI_PASSWORD = "robot1234";
// =============================

const int LED_PIN = 2;

WiFiUDP udp;
char messageRecu[255];

void traiterCommande(String commande);

void setup()
{
    Serial.begin(115200);
    delay(500);

    pinMode(LED_PIN, OUTPUT);

    // Démarrer le hotspot Wi-Fi
    Serial.println("Démarrage du hotspot...");
    WiFi.softAP(WIFI_SSID, WIFI_PASSWORD);
    Serial.print("Hotspot actif. IP : ");
    Serial.println(WiFi.softAPIP());

    // Démarrer UDP
    udp.begin(4210);
    Serial.println("Robot prêt !");
}

void loop()
{
    int taillePaquet = udp.parsePacket();

    if (taillePaquet > 0)
    {
        int longueur = udp.read(messageRecu, 254);
        messageRecu[longueur] = '\0';

        String commande = String(messageRecu);
        Serial.print("< ");
        Serial.println(commande);

        traiterCommande(commande);
    }
}

void traiterCommande(String commande)
{
    if (commande == "PING")
    {
        udp.beginPacket(udp.remoteIP(), udp.remotePort());
        udp.print("PONG");
        udp.endPacket();
    }
    else if (commande == "LED_ON")
    {
        digitalWrite(LED_PIN, HIGH);
    }
    else if (commande == "LED_OFF")
    {
        digitalWrite(LED_PIN, LOW);
    }
    else if (commande.startsWith("MOTOR:"))
    {
        String valeurs = commande.substring(6);
        int sep = valeurs.indexOf(':');

        if (sep > 0)
        {
            int gauche = valeurs.substring(0, sep).toInt();
            int droite = valeurs.substring(sep + 1).toInt();
            Serial.print("Moteurs : G="); Serial.print(gauche);
            Serial.print(" D="); Serial.println(droite);
            // TODO : brancher les vrais moteurs ici
        }
        else
        {
            int vitesse = valeurs.toInt();
            Serial.print("Moteur : "); Serial.println(vitesse);
        }
    }
    else if (commande == "GET_SENSOR")
    {
        int valeur = analogRead(34);
        String reponse = "SENSOR:" + String(valeur);
        udp.beginPacket(udp.remoteIP(), udp.remotePort());
        udp.print(reponse);
        udp.endPacket();
    }
    else
    {
        Serial.println("Commande inconnue");
    }
}
```

---

## Pourquoi une fonction `traiterCommande()` ?

Au lieu de tout mettre dans `loop()`, on crée une **fonction séparée**.

```cpp
void traiterCommande(String commande)
{
    ...
}
```

Avantages :
- `loop()` reste courte et lisible
- La logique est regroupée au même endroit
- Facile d'ajouter de nouvelles commandes

---

## Test complet

1. Téléverse ce firmware
2. Vérifie dans le Moniteur Série : `Hotspot actif. IP : 192.168.4.1` puis `Robot prêt !`
3. **Préviens le Groupe A** → ils connectent leur PC au Wi-Fi `Robot-ESP32` (mot de passe : `robot1234`) et lancent leur `driver_station.py` ou `joystick_control.py`
4. Teste toutes les commandes :
   - PING → réponse PONG
   - LED_ON / LED_OFF → LED réagit
   - MOTOR:120 → valeur affichée dans le Moniteur Série
   - GET_SENSOR → valeur capteur renvoyée

---

## Cases à cocher

- [ ] Le firmware compile et se téléverse
- [ ] Toutes les commandes fonctionnent
- [ ] Le Groupe A peut contrôler la LED
- [ ] Le Groupe A reçoit les valeurs du capteur
- [ ] Le Groupe A peut envoyer des commandes moteur

---

> [!TIP]
> Pour ajouter le contrôle réel des moteurs, tu auras besoin d'un driver moteur (L298N, DRV8833…) et d'utiliser `analogWrite()` ou `ledcWrite()`. Demande à ton prof pour le câblage.

---

⬅ [Précédent — Lecture capteur](./06-lecture-capteur.md) · [Suivant ➡ Défis bonus](./08-bonus.md)
