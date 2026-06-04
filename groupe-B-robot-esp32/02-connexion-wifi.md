# B-02 — Créer un hotspot Wi-Fi avec l'ESP32

> **Pour qui :** Groupe B
> **Durée estimée :** 20 min
> **Prérequis :** [Découverte Arduino IDE](./01-decouverte-arduino-ide.md)
> **Objectif :** transformer l'ESP32 en point d'accès Wi-Fi (hotspot), pour que le Groupe A puisse s'y connecter directement

---

## C'est quoi un hotspot ?

Quand tu actives le partage de connexion sur ton téléphone, tu crées un **hotspot** : ton téléphone devient lui-même un routeur Wi-Fi, et les autres appareils s'y connectent.

C'est exactement ce qu'on va faire avec l'ESP32. On appelle ça le mode **Point d'Accès** (ou **AP** pour *Access Point*).

```
┌─────────────────────────────────────────┐
│  Réseau Wi-Fi "Robot-ESP32"             │
│                                         │
│   [PC du Groupe A] ──────┐              │
│                          ▼              │
│                    [ESP32 / Robot]      │
│                   IP fixe : 192.168.4.1 │
└─────────────────────────────────────────┘
```

> **Avantage clé :** l'adresse IP de l'ESP32 est toujours `192.168.4.1`. Pas besoin de la noter, pas de surprise.

---

## Le programme

Copie ce code **tel quel** dans Arduino IDE, puis téléverse :

```cpp
#include <WiFi.h>

// === Paramètres du hotspot ===
const char* WIFI_SSID     = "Robot-ESP32";
const char* WIFI_PASSWORD = "robot1234";
// =============================

void setup()
{
    Serial.begin(115200);
    delay(500);

    Serial.println("Démarrage du hotspot Wi-Fi...");

    // Mettre l'ESP32 en mode Point d'Accès
    WiFi.softAP(WIFI_SSID, WIFI_PASSWORD);

    Serial.println("Hotspot actif !");
    Serial.print("Nom du réseau  : ");
    Serial.println(WIFI_SSID);
    Serial.print("Mot de passe   : ");
    Serial.println(WIFI_PASSWORD);
    Serial.print("Adresse IP     : ");
    Serial.println(WiFi.softAPIP());
}

void loop()
{
    // Rien pour l'instant
}
```

---

## Résultat attendu dans le Moniteur Série

Ouvre le Moniteur Série (icône loupe en haut à droite, ou `Ctrl+Shift+M`), vitesse **115200**.  
Après le téléversement, tu dois voir :

```text
Démarrage du hotspot Wi-Fi...
Hotspot actif !
Nom du réseau  : Robot-ESP32
Mot de passe   : robot1234
Adresse IP     : 192.168.4.1
```

> [!IMPORTANT]
> L'adresse IP `192.168.4.1` est **toujours la même** en mode hotspot. C'est cette adresse que le Groupe A devra utiliser pour envoyer des commandes au robot.

---

## Vérifier que ça marche vraiment

1. Sur **ton propre PC** (ou ton téléphone), ouvre la liste des réseaux Wi-Fi disponibles.
2. Tu dois voir apparaître un réseau nommé **`Robot-ESP32`**.
3. Connecte-toi avec le mot de passe `robot1234`.
4. Tu es maintenant sur le même réseau que le robot !

> [!NOTE]
> Quand tu es connecté au hotspot de l'ESP32, tu n'as plus accès à Internet. C'est normal : l'ESP32 n'est pas connecté à Internet, il crée juste un réseau local entre lui et toi.

---

## Comprendre le code

### `#include <WiFi.h>`

Charge la bibliothèque Wi-Fi intégrée à l'ESP32. Sans cette ligne, aucune fonction Wi-Fi n'existe.

### `WiFi.softAP(ssid, password)`

C'est la fonction clé. Elle dit à l'ESP32 :
> « Crée un réseau Wi-Fi avec ce nom et ce mot de passe. »

- `ssid` = le nom du réseau visible dans la liste Wi-Fi
- `password` = le mot de passe pour s'y connecter (minimum 8 caractères)

### `WiFi.softAPIP()`

Retourne l'adresse IP de l'ESP32 sur son propre hotspot.  
En mode AP, cette adresse est toujours **`192.168.4.1`** par défaut.

---

## Cases à cocher

- [ ] Le programme compile sans erreur
- [ ] Le programme se téléverse sur l'ESP32
- [ ] Le Moniteur Série affiche "Hotspot actif !"
- [ ] Je vois le réseau "Robot-ESP32" dans la liste Wi-Fi de mon PC
- [ ] Je me suis connecté au hotspot avec le mot de passe `robot1234`
- [ ] J'ai confirmé que l'adresse IP affichée est bien `192.168.4.1`

---

## Mini-quiz

**Question :** Quelle est la différence entre `WiFi.begin()` et `WiFi.softAP()` ?

<details>
<summary>💡 Voir la réponse</summary>

- `WiFi.begin()` → l'ESP32 se **connecte** à un réseau Wi-Fi existant (comme ton PC se connecte à une box).
- `WiFi.softAP()` → l'ESP32 **crée** son propre réseau Wi-Fi (comme ton téléphone quand tu actives le partage de connexion).

Dans notre projet, on utilise `softAP` pour que l'ESP32 soit autonome : pas besoin d'un routeur externe.

</details>

---

⬅ [Précédent — Arduino IDE](./01-decouverte-arduino-ide.md) · [Suivant ➡ Recevoir UDP](./03-recevoir-udp.md)
