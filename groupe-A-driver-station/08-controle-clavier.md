# A-08 — Contrôle clavier (commandes moteur)

> **Pour qui :** Groupe A
> **Durée estimée :** 10 min
> **Prérequis :** [Driver Station finale](./07-driver-station-finale.md)
> **Objectif :** envoyer des commandes moteur avec une valeur saisie au clavier

---

## Le format d'une commande moteur

Pour contrôler un moteur, on envoie un message avec la vitesse :

```text
MOTOR:120
```

- `MOTOR:` → nom de la commande
- `120` → valeur de vitesse (entre -255 et 255)

Le robot reçoit ce texte, l'analyse ("parse"), et extrait la valeur `120`.

---

## Le programme

Crée `keyboard_control.py` :

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

ROBOT_IP = "127.0.0.1"   # Changer pour l'IP de l'ESP32
ROBOT_PORT = 4210

print("=== Contrôle moteur au clavier ===")
print("Entrez une vitesse entre -255 et 255")
print("(q pour quitter)")
print()

while True:
    valeur = input("Vitesse moteur : ")

    if valeur == "q":
        print("Au revoir !")
        break

    # Vérifier que c'est bien un nombre
    try:
        vitesse = int(valeur)
    except ValueError:
        print("Erreur : entrez un nombre entier !")
        continue

    # Construire et envoyer la commande
    commande = "MOTOR:" + str(vitesse)
    sock.sendto(commande.encode(), (ROBOT_IP, ROBOT_PORT))
    print(f"→ Commande envoyée : {commande}")
```

---

## Test

Lance le simulateur dans un terminal, puis ce programme dans un autre :

```bash
python keyboard_control.py
```

Tape des valeurs comme `100`, `-50`, `255` et observe les messages dans le simulateur.

---

## Comprendre

### Construire la commande

```python
commande = "MOTOR:" + str(vitesse)
```

On construit une chaîne de texte en assemblant `"MOTOR:"` et la valeur convertie en texte.

- `vitesse` est un entier (ex : `120`)
- `str(120)` → `"120"` (conversion en texte)
- `"MOTOR:" + "120"` → `"MOTOR:120"`

### Vérification de l'entrée

```python
try:
    vitesse = int(valeur)
except ValueError:
    print("Erreur : entrez un nombre entier !")
    continue
```

Si l'utilisateur tape du texte au lieu d'un nombre, `int()` lève une erreur. On la gère proprement.

`continue` → reprend au début du `while True` sans exécuter la suite.

---

## Exercice

Ajoute une vérification que la vitesse est bien entre -255 et 255. Si ce n'est pas le cas, affiche un message d'erreur et ne pas envoyer la commande.

<details>
<summary>💡 Voir la solution</summary>

```python
if vitesse < -255 or vitesse > 255:
    print("Erreur : la vitesse doit être entre -255 et 255 !")
    continue
```

À placer après la conversion `int()`.

</details>

---

## Cases à cocher

- [ ] `keyboard_control.py` envoie des commandes `MOTOR:XXX`
- [ ] Le simulateur reçoit et affiche les commandes
- [ ] La vérification de type fonctionne (essaie de taper "abc")

---

⬅ [Précédent — Driver Station](./07-driver-station-finale.md) · [Suivant ➡ Joystick pygame](./09-joystick-pygame.md)
