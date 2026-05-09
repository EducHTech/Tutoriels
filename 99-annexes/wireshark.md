# Wireshark — Observer les paquets réseau

> **Facultatif** — outil de curiosité pour voir ce qui circule sur le réseau

---

## C'est quoi Wireshark ?

Wireshark est un outil qui **capture et affiche tous les paquets réseau** qui passent par ta carte réseau. C'est comme mettre une caméra sur le câble réseau.

Téléchargement : [https://www.wireshark.org/](https://www.wireshark.org/)

---

## Comment filtrer pour voir uniquement UDP port 4210

Dans la barre de filtre de Wireshark, tape :

```
udp.port == 4210
```

Tu verras alors uniquement les paquets de ton TP.

---

## Ce que tu peux observer

- Les paquets `PING` / `PONG` entre Python et l'ESP32
- L'adresse IP source et destination
- Le contenu en clair du message (UDP n'est pas chiffré)
- La latence entre l'envoi et la réponse

---

> [!NOTE]
> Wireshark est un outil utilisé par les professionnels de la sécurité informatique et les ingénieurs réseau. Le voir dans ta liste d'outils, ça fait son effet !

---

[⬅ Retour accueil](../README.md)
