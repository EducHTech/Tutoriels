# Tutoriel UDP avec Python et ESP32
## Découverte des communications réseau pour la robotique

---

# Table des matières

- [1. Introduction](#1-introduction)
- [2. Découverte réseau](#2-découverte-réseau)
- [3. Installation outils Windows](#3-installation-outils-windows)
- [4. Installation ESP32](#4-installation-esp32)
- [5. Premier programme Python](#5-premier-programme-python)
- [6. Premier UDP minimal](#6-premier-udp-minimal)
- [7. Boucles UDP](#7-boucles-udp)
- [8. Client / serveur UDP Python](#8-client--serveur-udp-python)
- [9. Wi-Fi ESP32](#9-wi-fi-esp32)
- [10. UDP ESP32](#10-udp-esp32)
- [11. Contrôle LED](#11-contrôle-led)
- [12. Contrôle moteur](#12-contrôle-moteur)
- [13. Lecture capteur](#13-lecture-capteur)
- [14. Version finale serveur Windows](#14-version-finale-serveur-windows)
- [15. Version finale client Windows](#15-version-finale-client-windows)
- [16. Version finale ESP32](#16-version-finale-esp32)
- [17. Version joystick clavier](#17-version-joystick-clavier)
- [18. Version joystick pygame](#18-version-joystick-pygame)
- [19. Architecture finale robot](#19-architecture-finale-robot)
- [20. Exercices bonus](#20-exercices-bonus)
- [21. Annexes](#21-annexes)

---

# 1. Introduction

## Objectif du projet

Dans ce projet, nous allons construire une petite architecture réseau robotique utilisant :

- un ordinateur Windows
- un ESP32 connecté en Wi‑Fi
- une communication UDP

L'objectif est de comprendre :

- comment deux machines communiquent
- comment envoyer des messages réseau
- comment contrôler un robot à distance
- comment transmettre des données de capteurs

---

## Architecture finale

```text
+-------------------+
| Driver Station    |
| Windows + Python  |
| Serveur UDP       |
+---------+---------+
          |
          | Wi‑Fi UDP
          |
+---------+---------+
| ESP32 Robot       |
| Client UDP        |
| LED + Capteurs    |
+-------------------+
```

---

## Organisation pédagogique

Deux groupes travaillent séparément.

### Groupe A

Développe :

- le serveur Windows
- les outils de test
- les commandes UDP

### Groupe B

Développe :

- le client ESP32
- le Wi‑Fi
- les réactions du robot

---

> [!IMPORTANT]
> L'utilisation d'IA pendant le TP est interdite.
>
> La documentation officielle, les forums et les recherches web sont autorisés.

---

# 2. Découverte réseau

## Qu'est-ce qu'une adresse IP ?

Une adresse IP est l'adresse d'un appareil sur le réseau.

Exemple :

```text
192.168.1.50
```

Chaque appareil possède une adresse différente.

---

## Qu'est-ce qu'un port ?

Le port permet d'identifier un programme.

Exemple :

```text
IP : 192.168.1.50
PORT : 4210
```

On peut imaginer :

- l'adresse IP = l'immeuble
- le port = le numéro de porte

---

## UDP

UDP signifie :

```text
User Datagram Protocol
```

UDP permet d'envoyer rapidement de petits messages.

UDP :

- est rapide
- simple
- faible latence
- ne garantit pas la réception

---

## TCP vs UDP

| TCP | UDP |
|---|---|
| Fiable | Rapide |
| Vérifie réception | Pas de vérification |
| Plus lent | Très rapide |
| Web | Robotique |

---

## Pourquoi UDP en robotique ?

En robotique :

- la vitesse est importante
- on préfère les données récentes
- perdre un message n'est pas dramatique

Exemple :

```text
MOTOR:120
```

Si une commande est perdue, la suivante arrive très vite.

---

## Datagrammes

Un message UDP est appelé :

```text
Datagramme
```

---

## Latence

La latence représente le temps nécessaire pour transmettre une information.

En robotique :

- faible latence = meilleur contrôle

---

## Questionnaire

1. Que signifie IP ?
2. À quoi sert un port ?
3. Pourquoi UDP est-il rapide ?
4. Pourquoi UDP est-il utilisé en robotique ?
5. Quelle différence entre TCP et UDP ?

---

# 3. Installation outils Windows

## Installer Python

Télécharger Python :

```text
https://www.python.org/downloads/
```

Pendant l'installation :

- cocher :

```text
Add Python to PATH
```

---

## Vérifier Python

Ouvrir le terminal :

```bash
python --version
```

Résultat attendu :

```text
Python 3.x.x
```

---

## Installer VSCode

Télécharger :

```text
https://code.visualstudio.com/
```

---

## Installer l'extension Python

Dans VSCode :

- Extensions
- rechercher :

```text
Python
```

Installer l'extension officielle.

---

## Premier fichier

Créer :

```text
hello.py
```

---

# 4. Installation ESP32

## Installer Arduino IDE

Télécharger :

```text
https://www.arduino.cc/en/software
```

---

## Ajouter le support ESP32

Dans Arduino IDE :

```text
Fichier
→ Préférences
```

Ajouter :

```text
https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
```

Puis :

```text
Outils
→ Type de carte
→ Gestionnaire de cartes
```

Installer ESP32.

---

## Choisir le port série

```text
Outils
→ Port
```

---

## Moniteur série

Ouvrir :

```text
Outils
→ Moniteur série
```

Vitesse :

```text
115200
```

---

# 5. Premier programme Python

## Hello World

```python
print("Bonjour UDP")
```

---

## Exécution

Dans le terminal :

```bash
python hello.py
```

---

## Explication

```python
print("Bonjour UDP")
```

- `print()` affiche du texte
- le texte est entre guillemets

---

## Questionnaire

1. À quoi sert `print()` ?
2. Comment exécuter un script Python ?
3. Quel est le rôle du terminal ?

---

# 6. Premier UDP minimal

## receiver.py

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind(("0.0.0.0", 4210))

print("En attente...")

message, address = sock.recvfrom(1024)

print("Message reçu :")
print(message.decode())
print(address)
```

---

## sender.py

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = "Bonjour ESP32"

sock.sendto(message.encode(), ("127.0.0.1", 4210))

print("Message envoyé")
```

---

## Explication détaillée

### Création du socket

```python
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
```

- `AF_INET` = IPv4
- `SOCK_DGRAM` = UDP

---

### bind()

```python
sock.bind(("0.0.0.0", 4210))
```

Le programme écoute sur le port 4210.

---

### recvfrom()

```python
message, address = sock.recvfrom(1024)
```

- reçoit un message
- maximum 1024 octets

---

## Exercice

Modifier le message envoyé.

---

## Corrigé

```python
message = "TEST UDP"
```

---

# 7. Boucles UDP

## Émission périodique

```python
import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    sock.sendto("PING".encode(), ("127.0.0.1", 4210))
    print("PING envoyé")
    time.sleep(1)
```

---

## Explication

### while True

Boucle infinie.

---

### time.sleep(1)

Pause de 1 seconde.

---

## Exercice

Envoyer un message toutes les 0.5 secondes.

---

## Corrigé

```python
time.sleep(0.5)
```

---

# 8. Client / serveur UDP Python

## server.py

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind(("0.0.0.0", 4210))

print("Serveur démarré")

while True:
    message, address = sock.recvfrom(1024)

    text = message.decode()

    print("Client :", text)

    if text == "PING":
        sock.sendto("PONG".encode(), address)
```

---

## client.py

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.sendto("PING".encode(), ("127.0.0.1", 4210))

message, address = sock.recvfrom(1024)

print(message.decode())
```

---

## Architecture

```text
CLIENT ---- PING ----> SERVEUR
CLIENT <--- PONG ----- SERVEUR
```

---

## Questionnaire

1. Quel message envoie le client ?
2. Quel message renvoie le serveur ?
3. Quel rôle joue `recvfrom()` ?

---

# 9. Wi‑Fi ESP32

## Connexion Wi‑Fi

```cpp
#include <WiFi.h>

const char* ssid = "VOTRE_WIFI";
const char* password = "MOTDEPASSE";

void setup()
{
    Serial.begin(115200);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }

    Serial.println();
    Serial.println("Connecté !");
    Serial.println(WiFi.localIP());
}

void loop()
{
}
```

---

## Explication détaillée

### WiFi.begin()

Démarre la connexion Wi‑Fi.

---

### WiFi.status()

Vérifie si la connexion est terminée.

---

### WiFi.localIP()

Affiche l'adresse IP de l'ESP32.

---

# 10. UDP ESP32

## Réception UDP

```cpp
#include <WiFi.h>
#include <WiFiUdp.h>

const char* ssid = "VOTRE_WIFI";
const char* password = "MOTDEPASSE";

WiFiUDP udp;

char incomingPacket[255];

void setup()
{
    Serial.begin(115200);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
    }

    udp.begin(4210);

    Serial.println("UDP prêt");
}

void loop()
{
    int packetSize = udp.parsePacket();

    if (packetSize)
    {
        int len = udp.read(incomingPacket, 255);

        if (len > 0)
        {
            incomingPacket[len] = 0;
        }

        Serial.print("Message : ");
        Serial.println(incomingPacket);
    }
}
```

---

## Explication

### parsePacket()

Vérifie si un paquet est arrivé.

---

### read()

Lit le message UDP.

---

### char[]

Tableau de caractères.

---

# 11. Contrôle LED

## Programme ESP32

```cpp
#include <WiFi.h>
#include <WiFiUdp.h>

const int LED_PIN = 2;

WiFiUDP udp;

char incomingPacket[255];

void setup()
{
    Serial.begin(115200);

    pinMode(LED_PIN, OUTPUT);

    WiFi.begin("VOTRE_WIFI", "MOTDEPASSE");

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
    }

    udp.begin(4210);
}

void loop()
{
    int packetSize = udp.parsePacket();

    if (packetSize)
    {
        int len = udp.read(incomingPacket, 255);

        if (len > 0)
        {
            incomingPacket[len] = 0;
        }

        String command = String(incomingPacket);

        if (command == "LED_ON")
        {
            digitalWrite(LED_PIN, HIGH);
        }

        if (command == "LED_OFF")
        {
            digitalWrite(LED_PIN, LOW);
        }
    }
}
```

---

## Test Python

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

robot_ip = "192.168.1.50"

sock.sendto("LED_ON".encode(), (robot_ip, 4210))
```

---

# 12. Contrôle moteur

## Commande moteur

```text
MOTOR:120
```

---

## Parsing

```cpp
String command = String(incomingPacket);

if (command.startsWith("MOTOR:"))
{
    String valueText = command.substring(6);

    int speed = valueText.toInt();

    Serial.print("Vitesse moteur : ");
    Serial.println(speed);
}
```

---

## Explication détaillée

### startsWith()

Vérifie le début du message.

---

### substring(6)

Récupère le texte après `MOTOR:`.

---

### toInt()

Convertit le texte en nombre.

---

# 13. Lecture capteur

## ESP32

```cpp
if (command == "GET_SENSOR")
{
    int value = analogRead(34);

    String response = "SENSOR:" + String(value);

    udp.beginPacket(udp.remoteIP(), udp.remotePort());
    udp.print(response);
    udp.endPacket();
}
```

---

## Python

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.sendto("GET_SENSOR".encode(), ("192.168.1.50", 4210))

message, address = sock.recvfrom(1024)

print(message.decode())
```

---

# 14. Version finale serveur Windows

## server_final.py

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind(("0.0.0.0", 4210))

sock.settimeout(0.1)

robot_ip = "192.168.1.50"

print("Driver Station démarrée")

while True:

    print()
    print("1 - LED ON")
    print("2 - LED OFF")
    print("3 - PING")
    print("4 - GET SENSOR")

    choice = input("Choix : ")

    if choice == "1":
        sock.sendto("LED_ON".encode(), (robot_ip, 4210))

    if choice == "2":
        sock.sendto("LED_OFF".encode(), (robot_ip, 4210))

    if choice == "3":
        sock.sendto("PING".encode(), (robot_ip, 4210))

    if choice == "4":
        sock.sendto("GET_SENSOR".encode(), (robot_ip, 4210))

    try:
        message, address = sock.recvfrom(1024)
        print("Réponse :", message.decode())

    except:
        pass
```

---

# 15. Version finale client Windows

## robot_simulator.py

```python
import socket
import random

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind(("0.0.0.0", 4210))

print("Robot simulé prêt")

while True:

    message, address = sock.recvfrom(1024)

    text = message.decode()

    print(text)

    if text == "PING":
        sock.sendto("PONG".encode(), address)

    if text == "GET_SENSOR":

        value = random.randint(0, 100)

        response = "SENSOR:" + str(value)

        sock.sendto(response.encode(), address)
```

---

# 16. Version finale ESP32

## robot_udp_final.ino

```cpp
#include <WiFi.h>
#include <WiFiUdp.h>

const char* ssid = "VOTRE_WIFI";
const char* password = "MOTDEPASSE";

WiFiUDP udp;

char incomingPacket[255];

const int LED_PIN = 2;

void setup()
{
    Serial.begin(115200);

    pinMode(LED_PIN, OUTPUT);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
    }

    udp.begin(4210);

    Serial.println(WiFi.localIP());
}

void loop()
{
    int packetSize = udp.parsePacket();

    if (packetSize)
    {
        int len = udp.read(incomingPacket, 255);

        if (len > 0)
        {
            incomingPacket[len] = 0;
        }

        String command = String(incomingPacket);

        Serial.println(command);

        if (command == "PING")
        {
            udp.beginPacket(udp.remoteIP(), udp.remotePort());
            udp.print("PONG");
            udp.endPacket();
        }

        if (command == "LED_ON")
        {
            digitalWrite(LED_PIN, HIGH);
        }

        if (command == "LED_OFF")
        {
            digitalWrite(LED_PIN, LOW);
        }

        if (command == "GET_SENSOR")
        {
            int sensor = analogRead(34);

            String response = "SENSOR:" + String(sensor);

            udp.beginPacket(udp.remoteIP(), udp.remotePort());
            udp.print(response);
            udp.endPacket();
        }
    }
}
```

---

# 17. Version joystick clavier

## keyboard_control.py

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

robot_ip = "192.168.1.50"

while True:

    value = input("Vitesse moteur : ")

    command = "MOTOR:" + value

    sock.sendto(command.encode(), (robot_ip, 4210))
```

---

# 18. Version joystick pygame

## Installation pygame

```bash
pip install pygame
```

---

## Architecture

```text
Joystick USB
      |
      v
+----------------+
| Python pygame  |
| Lecture axes   |
+--------+-------+
         |
         | UDP
         v
+----------------+
| ESP32 Robot    |
+----------------+
```

---

## joystick_server.py

```python
import pygame
import socket
import time

pygame.init()
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

robot_ip = "192.168.1.50"

print("Joystick prêt")

while True:

    pygame.event.pump()

    left = joystick.get_axis(1)
    right = joystick.get_axis(3)

    left_value = int(left * 255)
    right_value = int(right * 255)

    command = f"MOTOR:{left_value}:{right_value}"

    print(command)

    sock.sendto(command.encode(), (robot_ip, 4210))

    time.sleep(0.1)
```

---

## Explication

### get_axis()

Lit une valeur analogique du joystick.

---

### int()

Convertit la valeur flottante en entier.

---

# 19. Architecture finale robot

```text
+---------------------------+
| Driver Station Windows    |
| Python UDP                |
| Joystick USB              |
+-------------+-------------+
              |
              | Wi‑Fi UDP
              |
+-------------+-------------+
| ESP32 Robot               |
| UDP                       |
| LED                       |
| Moteurs                   |
| Capteurs                  |
+---------------------------+
```

---

# 20. Exercices bonus

## Exercices

1. Ajouter un buzzer
2. Ajouter deux moteurs
3. Créer un heartbeat
4. Ajouter un niveau batterie
5. Détecter la perte connexion
6. Créer un protocole binaire

---

## Exemple heartbeat

```text
HEARTBEAT
```

Le serveur envoie régulièrement un message.

Le robot vérifie si les messages arrivent encore.

---

# 21. Annexes

## Wireshark

Wireshark permet d'observer les paquets réseau.

Téléchargement :

```text
https://www.wireshark.org/
```

---

## Commandes terminal utiles

### Adresse IP Windows

```bash
ipconfig
```

---

### Ping

```bash
ping 192.168.1.50
```

---

## Problèmes fréquents

| Problème | Solution |
|---|---|
| Aucun message | Vérifier IP |
| Timeout | Vérifier Wi‑Fi |
| ESP32 absent | Vérifier port USB |
| Aucun upload | Vérifier drivers |

---

# Références utiles

## Documentation Python

```text
https://docs.python.org/3/library/socket.html
```

---

## Documentation ESP32

```text
https://docs.espressif.com/projects/arduino-esp32/en/latest/
```

---

## Documentation Arduino

```text
https://www.arduino.cc/reference/en/
```

---

# Vidéos utiles

## UDP Python

```text
https://www.youtube.com/results?search_query=python+udp+tutorial
```

---

## ESP32 Wi‑Fi

```text
https://www.youtube.com/results?search_query=esp32+wifi+udp
```

---

# Conclusion

Dans ce tutoriel, nous avons appris :

- les bases du réseau
- UDP
- Python réseau
- Wi‑Fi ESP32
- communication robotique
- architecture client/serveur

Nous avons construit une mini Driver Station robotique capable de :

- envoyer des commandes
- recevoir des données
- contrôler un robot
- transmettre des capteurs

---

> [!TIP]
> Continuer le projet avec :
>
> - plusieurs robots
> - caméra Wi‑Fi
> - télémétrie
> - contrôle temps réel
> - protocole binaire optimisé

