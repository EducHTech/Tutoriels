# Dépannage

---

## Problèmes Python / Groupe A

| Problème | Cause probable | Solution |
|---|---|---|
| `python` introuvable | Python mal installé ou PATH manquant | Réinstalle Python en cochant "Add to PATH" |
| `Address already in use` | Un autre programme utilise le port 4210 | Ferme tous les terminaux et relance |
| Pas de réponse au PING | Robot éteint ou mauvaise IP | Vérifie l'IP avec `ipconfig` et celle de l'ESP32 |
| `ModuleNotFoundError: pygame` | pygame non installé | `pip install pygame` dans le terminal |
| Joystick non détecté | Joystick non branché | Branche le joystick AVANT de lancer le script |

---

## Problèmes Arduino IDE / Groupe B

| Problème | Cause probable | Solution |
|---|---|---|
| Téléversement échoue (Connecting...) | Boot non déclenché | Appuie sur le bouton BOOT pendant le téléversement |
| Port COM absent | Drivers USB manquants | Installe les drivers CP2102 ou CH340 selon ta carte |
| Aucune carte ESP32 dans la liste | Boards non installées | Refaire l'étape gestionnaire de cartes |
| Wi-Fi ne se connecte pas | — | L'ESP32 crée son propre hotspot, pas besoin de routeur. Vérifie que le réseau `Robot-ESP32` apparaît dans la liste Wi-Fi. |
| Moniteur Série illisible | Mauvaise vitesse | Mets 115200 en bas à droite du moniteur |
| Caractères parasites dans le message | `\0` manquant | Ajoute `messageRecu[longueur] = '\0';` après `read()` |

---

## Commandes utiles

### Trouver son adresse IP (Windows)

```bash
ipconfig
```

Cherche la ligne "Adresse IPv4" sous l'interface Wi-Fi.

### Tester la connectivité réseau

```bash
ping 192.168.4.1
```

Remplace l'IP si besoin (mais en mode hotspot c'est toujours `192.168.4.1`).
Si tu reçois des réponses → ton PC est bien connecté au hotspot de l'ESP32.

### Vérifier Python

```bash
python --version
pip --version
```

### Vérifier Git

```bash
git --version
```

---

## L'ESP32 ne répond plus du tout

1. Débrancher / rebrancher l'ESP32
2. Appuyer sur le bouton **EN** (reset) de l'ESP32
3. Retéléverser le programme

---

## Je ne sais pas quelle est l'IP de l'ESP32

En mode hotspot, l'ESP32 a **toujours** l'adresse IP `192.168.4.1`. Pas besoin de la chercher.

Si tu veux le confirmer : ouvre le Moniteur Série (115200) et appuie sur le bouton **EN** de l'ESP32 pour le redémarrer. La ligne `Hotspot actif. IP : 192.168.4.1` s'affiche.

---

[⬅ Retour accueil](../README.md)
