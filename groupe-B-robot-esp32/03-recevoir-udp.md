# B-03 — Recevoir des messages UDP

> **Pour qui :** Groupe B
> **Durée estimée :** 20 min
> **Prérequis :** [Connexion Wi-Fi](./02-connexion-wifi.md)
> **Objectif :** recevoir des messages UDP envoyés par le Groupe A et les afficher dans le Moniteur Série

---

> [!IMPORTANT]
> **🔄 Point de synchro 1** — quand ce programme fonctionne, préviens le Groupe A !
> Donne-leur ton **adresse IP** et ils pourront t'envoyer des messages depuis leur `client.py`.

---

## Le programme

```cpp
#include <WiFi.h>
#include <WiFiUdp.h>

// === À MODIFIER ===
const char* WIFI_SSID = "NOM_DU_WIFI";
const char* WIFI_PASSWORD = "MOT_DE_PASSE";
// ==================

WiFiUDP udp;
char messageRecu[255];

void setup()
{
    Serial.begin(115200);
    delay(500);

    // Connexion Wi-Fi
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    Serial.print("Connexion Wi-Fi");
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }
    Serial.println();
    Serial.print("IP : ");
    Serial.println(WiFi.localIP());

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
3. Note l'IP affichée
4. **Préviens le Groupe A** de ton IP
5. Le Groupe A lance `client.py` avec ton IP → tu dois voir le message dans le Moniteur Série

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
- [ ] L'IP s'affiche dans le Moniteur Série
- [ ] J'ai communiqué l'IP au Groupe A
- [ ] Le message envoyé par le Groupe A apparaît dans le Moniteur Série

---

> [!TIP]
> Si tu veux tester sans le Groupe A, utilise `sender.py` depuis ton propre ordinateur en changeant l'IP destination par celle de ton ESP32.

---

⬅ [Précédent — Wi-Fi](./02-connexion-wifi.md) · [Suivant ➡ Contrôle LED](./04-controle-led.md)
