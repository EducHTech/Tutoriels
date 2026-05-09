# B-02 — Connexion Wi-Fi

> **Pour qui :** Groupe B
> **Durée estimée :** 20 min
> **Prérequis :** [Découverte Arduino IDE](./01-decouverte-arduino-ide.md)
> **Objectif :** connecter l'ESP32 au Wi-Fi et afficher son adresse IP

---

## Le programme

Copie ce code dans Arduino IDE, **modifie le nom et le mot de passe du Wi-Fi**, puis téléverse :

```cpp
#include <WiFi.h>

// === À MODIFIER ===
const char* WIFI_SSID = "NOM_DU_WIFI";
const char* WIFI_PASSWORD = "MOT_DE_PASSE";
// ==================

void setup()
{
    Serial.begin(115200);
    delay(500);

    Serial.println("Connexion au Wi-Fi...");

    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

    // Attendre la connexion (timeout : 20 secondes)
    int tentatives = 0;
    while (WiFi.status() != WL_CONNECTED && tentatives < 40)
    {
        delay(500);
        Serial.print(".");
        tentatives++;
    }

    if (WiFi.status() == WL_CONNECTED)
    {
        Serial.println();
        Serial.println("Connecté !");
        Serial.print("Adresse IP de l'ESP32 : ");
        Serial.println(WiFi.localIP());
    }
    else
    {
        Serial.println();
        Serial.println("Échec de connexion. Vérifie le nom et mot de passe Wi-Fi.");
    }
}

void loop()
{
    // Rien pour l'instant
}
```

---

## Résultat attendu dans le Moniteur Série

```text
Connexion au Wi-Fi...
.....
Connecté !
Adresse IP de l'ESP32 : 192.168.1.50
```

> [!IMPORTANT]
> **Note l'adresse IP affichée !** Tu en auras besoin pour les étapes suivantes, et tu devras la communiquer au Groupe A lors des synchros.

---

## Comprendre le code

### `#include <WiFi.h>`

Charge la bibliothèque Wi-Fi intégrée à l'ESP32. Sans cette ligne, `WiFi.begin()` n'existe pas.

### `WiFi.begin(ssid, password)`

Lance la connexion Wi-Fi avec le nom du réseau et le mot de passe.

### `WiFi.status() != WL_CONNECTED`

Vérifie si la connexion est établie.

- `WL_CONNECTED` = "connecté avec succès"

On attend dans une boucle jusqu'à ce que ce soit le cas.

### `WiFi.localIP()`

Retourne l'adresse IP attribuée par le routeur à l'ESP32.

---

## Cases à cocher

- [ ] J'ai modifié le nom et le mot de passe du Wi-Fi dans le code
- [ ] Le programme compile et se téléverse
- [ ] Le Moniteur Série affiche "Connecté !"
- [ ] J'ai noté l'adresse IP de l'ESP32

---

## Mini-quiz

**Question :** Pourquoi utilise-t-on une boucle `while` avec un compteur de tentatives plutôt que `while (WiFi.status() != WL_CONNECTED)` sans fin ?

<details>
<summary>💡 Voir la réponse</summary>

Si le Wi-Fi n'est pas disponible (mauvais mot de passe, réseau hors portée...), une boucle sans fin bloquerait l'ESP32 indéfiniment. Avec un compteur de tentatives, on peut afficher un message d'erreur et continuer l'exécution.

</details>

---

> [!WARNING]
> L'ESP32 ne peut se connecter qu'à des réseaux **2.4 GHz**. Les réseaux 5 GHz ne fonctionnent pas. Si tu vois "Échec de connexion", vérifie que le réseau est bien en 2.4 GHz.

---

⬅ [Précédent — Arduino IDE](./01-decouverte-arduino-ide.md) · [Suivant ➡ Recevoir UDP](./03-recevoir-udp.md)
