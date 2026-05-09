# A-03 — Premier émetteur UDP

> **Pour qui :** Groupe A
> **Durée estimée :** 15 min
> **Prérequis :** [Récepteur UDP](./02-premier-udp-recepteur.md)
> **Objectif :** envoyer un message UDP et recevoir sa réponse dans le récepteur

---

## Le programme

Crée un fichier `sender.py` :

```python
import socket

# Créer un socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Le message à envoyer
message = "Bonjour depuis Python !"

# Envoyer le message à 127.0.0.1 port 4210
sock.sendto(message.encode(), ("127.0.0.1", 4210))

print("Message envoyé !")
```

---

## Tester avec deux terminaux

Pour voir la communication, il faut **deux terminaux ouverts en même temps**.

### Terminal 1 — Lancer le récepteur

```bash
python receiver.py
```

Laisse-le tourner (il attend un message).

### Terminal 2 — Ouvrir un second terminal

Dans VSCode, clique sur le **+** à droite du nom du terminal, ou via :

```
Terminal → Nouveau terminal
```

Puis lance l'émetteur :

```bash
python sender.py
```

### Résultat attendu

Dans le terminal 1 (récepteur) :

```text
En attente d'un message...
Message reçu : Bonjour depuis Python !
Vient de : ('127.0.0.1', XXXXX)
```

Dans le terminal 2 (émetteur) :

```text
Message envoyé !
```

---

## Comprendre le code

### `127.0.0.1`

```python
sock.sendto(message.encode(), ("127.0.0.1", 4210))
```

`127.0.0.1` est une adresse spéciale : c'est **ton propre ordinateur**.

On l'appelle aussi **localhost** : "envoie le message à moi-même".

> [!NOTE]
> C'est parfait pour tester ! On n'a pas encore besoin de l'ESP32. Les deux programmes (émetteur et récepteur) tournent sur le même ordinateur.

### `.encode()`

```python
message.encode()
```

Le réseau transporte des **bytes**, pas du texte. `.encode()` convertit le texte en bytes.

C'est l'inverse de `.decode()` qu'on avait vu côté récepteur.

---

## Exercice

Modifie `sender.py` pour envoyer le message `TEST UDP OK` et vérifie qu'il apparaît bien dans `receiver.py`.

<details>
<summary>💡 Voir la solution</summary>

```python
message = "TEST UDP OK"
```

Remplace juste la ligne du message.

</details>

---

## Cases à cocher

- [ ] J'ai créé `sender.py`
- [ ] J'ai ouvert deux terminaux dans VSCode
- [ ] `receiver.py` a bien reçu le message de `sender.py`

---

> [!WARNING]
> Si `receiver.py` répond "Address already in use", c'est qu'un autre programme utilise déjà le port 4210. Vérifie que tu n'as pas un autre terminal avec `receiver.py` déjà lancé.

---

⬅ [Précédent — Récepteur UDP](./02-premier-udp-recepteur.md) · [Suivant ➡ Boucles UDP](./04-boucles-udp.md)
