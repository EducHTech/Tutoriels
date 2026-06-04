# 02 — Adresse IP et port

> **Pour qui :** les deux groupes
> **Durée estimée :** 10 min
> **Prérequis :** [Introduction projet](./01-introduction-projet.md)
> **Objectif :** comprendre l'adresse IP et le port, et trouver son IP sur le réseau

---

## L'adresse IP — l'adresse de l'appareil

Sur un réseau (Wi-Fi, câble…), chaque appareil a une **adresse IP**.
C'est comme l'adresse d'une maison : ça permet de savoir où envoyer un message.

Une adresse IP ressemble à ça :

```text
192.168.1.50
```

C'est 4 nombres séparés par des points.

### Analogie

```text
Réseau Wi-Fi  =  une ville
Adresse IP    =  l'adresse de ta maison dans cette ville
```

Ton ordinateur a une adresse IP. L'ESP32 en aura une aussi — et comme il crée son propre hotspot Wi-Fi, son adresse sera **toujours `192.168.4.1`**.

---

## Le port — la porte d'entrée

Un même ordinateur peut faire tourner plusieurs programmes réseau en même temps.
Le **port** permet de savoir à quel programme envoyer le message.

```text
IP   : 192.168.1.50   ← l'appareil
PORT : 4210           ← le programme sur cet appareil
```

### Analogie

```text
Adresse IP  =  l'immeuble
Port        =  le numéro de la porte dans l'immeuble
```

Dans ce TP, on utilisera toujours le port **4210**.

> [!NOTE]
> Les ports vont de 0 à 65535. Certains ports sont réservés (80 = web, 443 = web sécurisé, etc.). Pour nos tests, on utilise 4210 qui est libre.

---

## Trouver son adresse IP

Ouvre le terminal VSCode (**Terminal → New Terminal**) et tape :

```bash
ipconfig
```

Cherche la ligne **Adresse IPv4** dans la section Wi-Fi ou Ethernet. Par exemple :

```text
Adresse IPv4. . . . . . . . . . . : 192.168.1.42
```

> [!TIP]
> Note ton adresse IP quelque part, tu en auras besoin pendant le TP !
> Elle peut changer si tu déconnectes et reconnectes le Wi-Fi.

---

## Cases à cocher

- [ ] Je comprends ce qu'est une adresse IP
- [ ] Je comprends ce qu'est un port
- [ ] J'ai trouvé mon adresse IP avec `ipconfig`

---

## Mini-quiz

**Question 1 :** À quoi sert l'adresse IP ?

<details>
<summary>💡 Voir la réponse</summary>

L'adresse IP identifie un appareil sur le réseau. Sans adresse IP, impossible de savoir où envoyer un message.

</details>

**Question 2 :** Deux programmes sur le même ordinateur peuvent-ils tous les deux recevoir des messages réseau ?

<details>
<summary>💡 Voir la réponse</summary>

Oui ! Ils utilisent des **ports différents**. Par exemple, un programme écoute sur le port 4210, un autre sur le port 8080. Ils ont la même adresse IP (même ordinateur) mais des ports différents.

</details>

---

⬅ [Précédent — Introduction](./01-introduction-projet.md) · [Suivant ➡ UDP vs TCP](./03-udp-vs-tcp.md)
