# B-06 — Lecture d'un capteur

> **Pour qui :** Groupe B
> **Durée estimée :** 15 min
> **Prérequis :** [Commande moteur](./05-parser-commande-moteur.md)
> **Objectif :** lire la valeur d'un capteur et la renvoyer au Groupe A

---

## Le principe

Le Groupe A envoie la commande `GET_SENSOR`.
L'ESP32 lit une valeur analogique et répond `SENSOR:XXX`.

```text
Groupe A  ---- GET_SENSOR ---->  ESP32
Groupe A  <--- SENSOR:427  ----  ESP32
```

---

## La lecture analogique

L'ESP32 a des entrées **analogiques** qui lisent une tension entre 0 V et 3.3 V et la convertissent en nombre entre **0 et 4095**.

La fonction :

```cpp
int valeur = analogRead(34);
```

lit la valeur sur la broche **GPIO 34** (une entrée analogique de l'ESP32).

> [!NOTE]
> Si tu n'as pas de capteur branché sur GPIO 34, tu peux quand même tester : la broche flottante va lire une valeur aléatoire. C'est suffisant pour tester la communication.

---

## Ajouter la gestion `GET_SENSOR`

Dans ta boucle `loop()`, ajoute :

```cpp
else if (commande == "GET_SENSOR")
{
    int valeur = analogRead(34);

    String reponse = "SENSOR:" + String(valeur);

    udp.beginPacket(udp.remoteIP(), udp.remotePort());
    udp.print(reponse);
    udp.endPacket();

    Serial.print("Capteur lu : ");
    Serial.println(valeur);
}
```

---

## Tester

Depuis Python :

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)

sock.sendto("GET_SENSOR".encode(), ("192.168.X.XX", 4210))

reponse, _ = sock.recvfrom(1024)
print(reponse.decode())   # Affiche : SENSOR:2341
```

---

## Comprendre

### Construire la réponse

```cpp
String reponse = "SENSOR:" + String(valeur);
```

- `valeur` est un `int` (ex: `2341`)
- `String(2341)` → `"2341"`
- `"SENSOR:" + "2341"` → `"SENSOR:2341"`

### Envoyer la réponse

```cpp
udp.beginPacket(udp.remoteIP(), udp.remotePort());
udp.print(reponse);
udp.endPacket();
```

Même mécanisme qu'avec PONG : on répond à l'adresse de l'expéditeur.

---

## Exercice

Ajoute une commande `GET_TEMP` qui renvoie une valeur simulée de température entre 20 et 30 (utilise `random(20, 31)`).

Format de réponse : `TEMP:25`

<details>
<summary>💡 Voir la solution</summary>

```cpp
else if (commande == "GET_TEMP")
{
    int temp = random(20, 31);
    String reponse = "TEMP:" + String(temp);

    udp.beginPacket(udp.remoteIP(), udp.remotePort());
    udp.print(reponse);
    udp.endPacket();

    Serial.print("Temp simulée : "); Serial.println(temp);
}
```

</details>

---

## Cases à cocher

- [ ] `GET_SENSOR` renvoie une valeur `SENSOR:XXX`
- [ ] Le Groupe A peut lire cette valeur depuis Python

---

⬅ [Précédent — Commande moteur](./05-parser-commande-moteur.md) · [Suivant ➡ Firmware final](./07-robot-final.md)
