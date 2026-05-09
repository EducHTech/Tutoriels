# 06 — Installer Arduino IDE + support ESP32

> **Pour qui :** Groupe B uniquement
> **Durée estimée :** 20 min
> **Prérequis :** [Git et dépôt](./05-installer-git-et-cloner.md)
> **Objectif :** avoir Arduino IDE prêt à programmer une carte ESP-WROOM-32

---

## C'est quoi Arduino IDE ?

Arduino IDE est un logiciel pour programmer des microcontrôleurs (des petits "cerveaux" électroniques).
On s'en sert ici pour programmer l'**ESP-WROOM-32**, la carte qui va faire office de robot.

> [!NOTE]
> Arduino IDE écrit du C++. Tu n'as pas besoin de tout connaître — les programmes sont fournis et expliqués étape par étape.

---

## Étape 1 — Télécharger Arduino IDE

Va sur : [https://www.arduino.cc/en/software](https://www.arduino.cc/en/software)

Clique sur **Windows Win 10 and newer, 64 bits**.

Lance l'installeur et clique sur **Next** / **I Agree** jusqu'à la fin.

---

## Étape 2 — Ajouter le support ESP32

Par défaut, Arduino IDE ne connaît pas l'ESP32. Il faut lui indiquer où trouver les fichiers.

### 2a. Ouvrir les Préférences

```
Fichier → Préférences
```

*(ou `Ctrl + ,`)*

### 2b. Ajouter l'URL des cartes ESP32

Dans le champ **"URL supplémentaires de gestionnaire de cartes"**, colle cette URL exactement :

```
https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
```

Clique sur **OK**.

### 2c. Installer les cartes ESP32

```
Outils → Type de carte → Gestionnaire de cartes
```

Dans la barre de recherche, tape :

```
esp32
```

Installe le paquet **esp32 by Espressif Systems** (clique sur **Installer**).

> [!WARNING]
> L'installation peut prendre plusieurs minutes car elle télécharge beaucoup de fichiers. Patiente !

---

## Étape 3 — Choisir la bonne carte

Connecte ton ESP-WROOM-32 en USB, puis :

```
Outils → Type de carte → esp32 → ESP32 Dev Module
```

> [!NOTE]
> L'**ESP-WROOM-32** (notre carte) est reconnue sous le nom **"ESP32 Dev Module"** dans Arduino IDE.

---

## Étape 4 — Choisir le port

```
Outils → Port
```

Sélectionne le port qui apparaît (généralement `COM3`, `COM4`, etc.).

> [!TIP]
> Si aucun port n'apparaît, débranche et rebranche la carte. Si ça ne fonctionne toujours pas, consulte la [page de dépannage](../99-annexes/depannage.md).

---

## Étape 5 — Vérifier avec le Moniteur Série

Le Moniteur Série permet de voir les messages envoyés par l'ESP32.

```
Outils → Moniteur série
```

En bas à droite du moniteur, configure la vitesse à :

```
115200
```

---

## Cases à cocher

- [ ] Arduino IDE est installé
- [ ] L'URL ESP32 est ajoutée dans les Préférences
- [ ] Les cartes ESP32 sont installées via le Gestionnaire de cartes
- [ ] La carte "ESP32 Dev Module" est sélectionnée dans Outils → Type de carte
- [ ] Le bon port COM est sélectionné

---

## Mini-quiz

**Question :** Pourquoi faut-il ajouter une URL dans les Préférences d'Arduino IDE ?

<details>
<summary>💡 Voir la réponse</summary>

Par défaut, Arduino IDE ne sait programmer que des cartes Arduino classiques. L'URL permet d'ajouter le support d'autres cartes (ici l'ESP32 de la marque Espressif). Sans ça, la carte ESP32 n'apparaîtrait pas dans la liste.

</details>

---

⬅ [Précédent — Installer Git](./05-installer-git-et-cloner.md) · [Suivant ➡ Bases communes](../01-bases-communes/01-introduction-projet.md)
