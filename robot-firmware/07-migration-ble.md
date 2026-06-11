# 07 — Migration WiFi → Bluetooth BLE

> **Durée estimée :** 35 min  
> **Prérequis :** [Wrapper UDP](./03-wrapper-udp.md) — tu connais le protocole texte `SET_MOTORS:...`  
> **Matériel :** carte ME Auriga + PC avec Bluetooth  
> **👤 Étudiant C** — travail en parallèle avec les étapes 05 et 06

---

## Pourquoi changer de protocole réseau ?

Sur l'ESP32, la communication se faisait par **WiFi/UDP** (sans fil, rapide, local).  
Sur l'Auriga, il n'y a pas de WiFi. Il y a un module **Bluetooth BLE** Makeblock intégré.

> **Bonne nouvelle :** le protocole de commandes (`SET_MOTORS`, `SET_SERVOS`…) **ne change pas**.  
> Seule la **couche transport** change.

```
Avant (ESP32)  :   Python ──[UDP/WiFi]──► Firmware
Après (Auriga) :   Python ──[BLE]──────► Firmware
```

---

## Comment fonctionne le BLE Makeblock ?

### 🤔 Question de réflexion
> Sur l'Auriga, le module BLE est connecté à **Serial0** (RX0/TX0) du Mega.  
> Quand Python envoie des données BLE, le Mega les reçoit via… quoi ?

<details>
<summary>💡 Indice</summary>

Le module BLE agit comme un **pont UART ↔ BLE**.  
Ce que Python écrit en BLE arrive dans `Serial` sur l'Arduino.  
Ce que l'Arduino écrit dans `Serial` est transmis en BLE à Python.

→ Sur l'Arduino : `Serial.read()` et `Serial.write()`, comme si c'était un câble USB.

</details>

---

## Étape 7a — Préparer le firmware Arduino

### 🎯 Objectif
Recevoir des commandes texte via BLE et les afficher dans le moniteur série.

### ✅ Code à compléter

```cpp
// comm_ble.ino — test de réception BLE

void setup() {
  Serial.begin(115200); // BLE Makeblock = UART0 @ 115200 bps
  delay(500);
  Serial.println("BLE pret");
}

// Buffer pour assembler les commandes ligne par ligne
String inputBuffer = "";

void loop() {
  // Lire les octets BLE arrivant via Serial
  while (Serial.available() > 0) {
    char c = (char)Serial.read();

    if (c == '\n') {
      // Fin de ligne = commande complète reçue
      inputBuffer.trim();
      if (inputBuffer.length() > 0) {
        processCommand(inputBuffer);
      }
      inputBuffer = "";
    } else {
      inputBuffer += c;
    }
  }
}

void processCommand(const String& cmd) {
  Serial.print("[CMD] ");
  Serial.println(cmd); // Affiche la commande reçue

  if (cmd == "PING") {
    // TODO : renvoyer "PONG\n" au driver station
    // (utilise le protocole Makeblock pour envoyer une string)
    sendString_BLE("PONG");
  }
  // Les autres commandes seront ajoutées dans le firmware final
}
```

> 💡 Pour envoyer une réponse au driver station Python, utilise le protocole Makeblock :

```cpp
// Fonctions protocole Makeblock (copie dans ton fichier)
void writeHead()  { Serial.write(0xff); Serial.write(0x55); }
void writeEnd()   { Serial.println(); }

void sendString_BLE(const char* str) {
  writeHead();
  Serial.write(4);           // Type STRING
  Serial.write(strlen(str)); // Longueur
  Serial.print(str);
  writeEnd();
}
```

### 🧪 Test attendu
Avec `test_mega2560_bidirectional.py` (ou le Fake Driver Station BLE) :
```
[CMD] PING
[CMD] SET_MOTORS:50,50,-50,-50
```

---

## Étape 7b — Fake Driver Station BLE (Python)

### 🎯 Objectif
Tester le firmware depuis Python, sans avoir le vrai Driver Station du Groupe A.

### 🤔 Question de réflexion
> Le Fake Driver Station ESP32 utilisait `socket.sendto(message.encode(), ...)`.  
> Pour le BLE, quelle fonction Python utilise-t-on à la place ?

<details>
<summary>💡 Indice</summary>

Avec la bibliothèque **Bleak** (BLE pour Python) :
```python
await client.write_gatt_char(WRITE_UUID, data)
```
`data` doit être des **bytes**, pas une string.  
Pour envoyer `"SET_MOTORS:50,50,-50,-50\n"` :
```python
data = "SET_MOTORS:50,50,-50,-50\n".encode()
```

</details>

### ✅ Fake Driver Station BLE

Le fichier `fake_driver_station_ble.py` est disponible dans ce dossier.  
Voici ce qu'il fait :

```
┌─────────────────────────────────────────────┐
│           Fake Driver Station BLE            │
│  Robot BLE : ME_BLE (adresse MAC à changer)  │
├─────────────────────────────────────────────┤
│  1  →  PING                                  │
│  2  →  SET_MOTORS (4 moteurs)                │
│  3  →  SET_SERVOS (3 servos)                 │
│  4  →  Lire capteurs (1 cycle)               │
│  q  →  Quitter                               │
└─────────────────────────────────────────────┘
```

**Avant de l'utiliser :**

1. Installe la dépendance :
   ```bash
   pip install bleak
   ```

2. Cherche l'adresse MAC de ton Auriga :
   ```bash
   python -m bleak
   ```
   Note l'adresse du dispositif nommé `Makeblock` ou `ME_BLE`.

3. Mets à jour `DEVICE_MAC` dans `fake_driver_station_ble.py`.

4. Lance :
   ```bash
   python fake_driver_station_ble.py
   ```

### 🧪 Test attendu
```
[✓] Connecté à ME_BLE
→ Envoi : PING
← Reçu  : PONG
```

### 🔍 Debug rapide
| Symptôme | Cause probable |
|---|---|
| `Device not found` | Mauvaise adresse MAC ou Bluetooth désactivé |
| `Connection timeout` | Auriga non allumé ou firmware non téléversé |
| `PONG` ne s'affiche pas | Vérifier `sendString_BLE("PONG")` dans l'Arduino |
| Données reçues illisibles | Le parser Makeblock s'attend à `[0xff 0x55]` |

---

## Ce que tu passes au firmware final

À la fin de cette étape, tu disposes de :
- ✅ Un Arduino qui lit des commandes texte via `Serial` (= BLE)
- ✅ Un Python qui envoie des commandes et reçoit des réponses BLE
- ✅ Le protocole Makeblock pour envoyer des données structurées

**Prochaine étape :** [Firmware final](./08-firmware-final-auriga.md)
