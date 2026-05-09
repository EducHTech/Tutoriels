# A-02 — Premier récepteur UDP

> **Pour qui :** Groupe A
> **Durée estimée :** 15 min
> **Prérequis :** [Hello Python](./01-hello-python.md)
> **Objectif :** créer un programme Python qui attend et reçoit un message UDP

---

## Le programme

Crée un fichier `receiver.py` et copie ce code :

```python
import socket

# Créer un socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Écouter sur le port 4210 (toutes les interfaces réseau)
sock.bind(("0.0.0.0", 4210))

print("En attente d'un message...")

# Attendre un message (bloque jusqu'à réception)
message, address = sock.recvfrom(1024)

print("Message reçu :", message.decode())
print("Vient de :", address)
```

---

## Lancer le programme

Dans le terminal :

```bash
python receiver.py
```

Le programme **se bloque** et affiche :

```text
En attente d'un message...
```

C'est normal ! Il attend qu'un message arrive. Pour l'instant il n'y a rien, on va régler ça à l'étape suivante.

Pour arrêter le programme : `Ctrl + C`

---

## Comprendre le code ligne par ligne

### `import socket`

```python
import socket
```

`socket` est une **bibliothèque** Python intégrée. Elle contient tout ce qu'il faut pour envoyer et recevoir des messages réseau.

`import` = "charge cette bibliothèque pour que je puisse l'utiliser".

---

### Créer un socket

```python
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
```

On crée un **socket** : c'est une sorte de "porte" réseau.

- `AF_INET` → on utilise IPv4 (adresses de type `192.168.x.x`)
- `SOCK_DGRAM` → on utilise UDP (Datagram)

---

### `bind()`

```python
sock.bind(("0.0.0.0", 4210))
```

On "attache" le socket à un port.

- `"0.0.0.0"` = écouter sur toutes les interfaces réseau (Wi-Fi, câble, etc.)
- `4210` = le port qu'on écoute

> [!TIP]
> `bind()` dit au système : "tous les messages qui arrivent sur le port 4210, donne-les à mon programme".

---

### `recvfrom()`

```python
message, address = sock.recvfrom(1024)
```

Cette ligne **attend** un message. Elle bloque l'exécution jusqu'à en recevoir un.

- `1024` = taille maximale du message en octets
- `message` = le contenu du message reçu (en bytes)
- `address` = l'adresse IP et le port de l'expéditeur

---

### `.decode()`

```python
message.decode()
```

Le message reçu est en **bytes** (données brutes). `.decode()` le convertit en texte lisible.

---

## Cases à cocher

- [ ] J'ai créé `receiver.py`
- [ ] J'ai lancé le programme et vu "En attente d'un message..."
- [ ] J'ai arrêté le programme avec `Ctrl + C`

---

## Mini-quiz

**Question :** Que fait `sock.bind(("0.0.0.0", 4210))` ?

<details>
<summary>💡 Voir la réponse</summary>

Cela dit au système : "attribue le port 4210 à mon programme". Tous les messages UDP qui arrivent sur ce port seront transmis à ce programme.

</details>

---

⬅ [Précédent — Hello Python](./01-hello-python.md) · [Suivant ➡ Émetteur UDP](./03-premier-udp-emetteur.md)
