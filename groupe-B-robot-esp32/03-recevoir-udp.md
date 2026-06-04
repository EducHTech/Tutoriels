# B-03 — Recevoir des messages UDP

> **Pour qui :** Groupe B
> **Durée estimée :** 20 min
> **Prérequis :** [Connexion Wi-Fi](./02-connexion-wifi.md)
> **Objectif :** recevoir des messages UDP envoyés par le Groupe A et les afficher dans le Moniteur Série

---

> [!IMPORTANT]
> **🔄 Point de synchro 1** — quand ce programme fonctionne, préviens le Groupe A !
> Dis-leur de se connecter au hotspot Wi-Fi **`Robot-ESP32`** (mot de passe : `robot1234`) — l'IP de l'ESP32 est toujours **`192.168.4.1`**.

---

## Le programme

```cpp
#include <WiFi.h>
#include <WiFiUdp.h>

// === Paramètres du hotspot ===
const char* WIFI_SSID     = "Robot-ESP32";
const char* WIFI_PASSWORD = "robot1234";
// =============================

WiFiUDP udp;
char messageRecu[255];

void setup()
{
    Serial.begin(115200);
    delay(500);

    // Démarrer le hotspot Wi-Fi
    WiFi.softAP(WIFI_SSID, WIFI_PASSWORD);
    Serial.print("Hotspot actif. IP : ");
    Serial.println(WiFi.softAPIP());

    // Démarrer UDP sur le port 4210
    udp.begin(4210);
    Serial.println("UDP prêt, en attente de messages...");
}

void loop()
{
    // Vérifier si un paquet est arrivé
    int taillePaquet = udp.parsePacket();

    if (taillePaquet > 0)
    {
        // Lire le message
        int longueur = udp.read(messageRecu, 254);
        messageRecu[longueur] = '\0';   // Terminer la chaîne

        Serial.print("Message reçu : ");
        Serial.println(messageRecu);
        Serial.print("De : ");
        Serial.println(udp.remoteIP());
    }
}
```

---

## Test

1. Téléverse ce programme
2. Ouvre le Moniteur Série (115200)
3. Vérifie que tu vois `Hotspot actif. IP : 192.168.4.1`
4. **Préviens le Groupe A** : dis-leur de connecter leur PC au Wi-Fi `Robot-ESP32` (mot de passe : `robot1234`)
5. Le Groupe A lance `client.py` en ciblant l'IP `192.168.4.1` → tu dois voir le message dans le Moniteur Série

---

## Comprendre le code

### `#include <WiFiUdp.h>`

Charge la bibliothèque pour la communication UDP sur Wi-Fi.

### `WiFiUDP udp`

Crée un objet `udp` qu'on utilisera pour envoyer et recevoir des paquets UDP.

### `udp.begin(4210)`

Démarre l'écoute UDP sur le port 4210.

### `udp.parsePacket()`

Vérifie si un paquet UDP est arrivé. Retourne :
- `0` → aucun paquet
- un nombre > 0 → taille du paquet reçu

### `udp.read(messageRecu, 254)`

Lit le contenu du paquet dans le tableau `messageRecu`, maximum 254 caractères.

### `messageRecu[longueur] = '\0'`

En C++, une chaîne de caractères se termine par le caractère spécial `\0`.
Sans ça, `Serial.println(messageRecu)` pourrait afficher des caractères parasites.

### `char messageRecu[255]`

Un **tableau de 255 caractères**. En C++, les textes sont stockés ainsi (pas comme en Python où `str` gère tout automatiquement).

---

## Cases à cocher

- [ ] Le programme se téléverse
- [ ] Le Moniteur Série affiche `Hotspot actif. IP : 192.168.4.1`
- [ ] Le réseau Wi-Fi `Robot-ESP32` est visible depuis mon PC
- [ ] J'ai prévenu le Groupe A (connectez-vous à `Robot-ESP32`, mot de passe `robot1234`)
- [ ] Le message envoyé par le Groupe A apparaît dans le Moniteur Série

---

> [!TIP]
> Si tu veux tester sans le Groupe A : connecte **ton propre PC** au hotspot `Robot-ESP32`, puis lance `sender.py` en ciblant l'IP `192.168.4.1`.

---

⬅ [Précédent — Wi-Fi](./02-connexion-wifi.md) · [Suivant ➡ Contrôle LED](./04-controle-led.md)
