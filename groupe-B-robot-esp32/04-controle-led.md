# B-04 — Contrôle de la LED

> **Pour qui :** Groupe B
> **Durée estimée :** 15 min
> **Prérequis :** [Recevoir UDP](./03-recevoir-udp.md)
> **Objectif :** allumer et éteindre la LED selon les commandes UDP reçues

---

> [!IMPORTANT]
> **🔄 Point de synchro 2** — quand la LED répond à `LED_ON` et `LED_OFF`, préviens le Groupe A !
> Ils pourront tester avec leur Driver Station.

---

## Le programme

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

void setup()
{
    Serial.begin(115200);
    delay(500);

    pinMode(LED_PIN, OUTPUT);

    // Démarrer le hotspot Wi-Fi
    WiFi.softAP(WIFI_SSID, WIFI_PASSWORD);
    Serial.print("Hotspot actif. IP : ");
    Serial.println(WiFi.softAPIP());

    udp.begin(4210);
    Serial.println("UDP prêt.");
}

void loop()
{
    int taillePaquet = udp.parsePacket();

    if (taillePaquet > 0)
    {
        int longueur = udp.read(messageRecu, 254);
        messageRecu[longueur] = '\0';

        String commande = String(messageRecu);
        Serial.print("Commande : ");
        Serial.println(commande);

        if (commande == "LED_ON")
        {
            digitalWrite(LED_PIN, HIGH);
            Serial.println("→ LED allumée");
        }
        else if (commande == "LED_OFF")
        {
            digitalWrite(LED_PIN, LOW);
            Serial.println("→ LED éteinte");
        }
        else if (commande == "PING")
        {
            udp.beginPacket(udp.remoteIP(), udp.remotePort());
            udp.print("PONG");
            udp.endPacket();
            Serial.println("→ PONG envoyé");
        }
    }
}
```

---

## Test

1. Téléverse le programme
2. Ouvre le Moniteur Série — vérifie que tu vois `Hotspot actif. IP : 192.168.4.1`
3. Connecte ton PC au Wi-Fi `Robot-ESP32` (mot de passe : `robot1234`)
4. Depuis **Python** sur l'ordinateur, envoie des commandes :

```python
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto("LED_ON".encode(), ("192.168.4.1", 4210))
```

La LED doit s'allumer ! Teste aussi `LED_OFF` et `PING`.

---

## Comprendre

### `String commande = String(messageRecu)`

On convertit le tableau de caractères `char[]` en objet `String` de C++ pour pouvoir utiliser `==` pour comparer des textes.

```cpp
if (commande == "LED_ON")
```

### Répondre à un PING

```cpp
udp.beginPacket(udp.remoteIP(), udp.remotePort());
udp.print("PONG");
udp.endPacket();
```

- `udp.remoteIP()` → adresse IP de l'expéditeur (le Groupe A)
- `udp.remotePort()` → port de l'expéditeur
- `beginPacket` / `print` / `endPacket` → prépare et envoie le paquet

---

## Cases à cocher

- [ ] `LED_ON` allume la LED
- [ ] `LED_OFF` éteint la LED
- [ ] `PING` reçoit une réponse `PONG`
- [ ] Le Groupe A a testé avec sa Driver Station

---

## Mini-quiz

**Question :** Pourquoi convertit-on `messageRecu` (de type `char[]`) en `String` avant de faire la comparaison ?

<details>
<summary>💡 Voir la réponse</summary>

En C++, on ne peut pas utiliser `==` pour comparer deux `char[]` directement (ça comparerait les adresses mémoire, pas le contenu). En convertissant en `String`, l'opérateur `==` compare bien le contenu texte.

</details>

---

⬅ [Précédent — Recevoir UDP](./03-recevoir-udp.md) · [Suivant ➡ Commande moteur](./05-parser-commande-moteur.md)
