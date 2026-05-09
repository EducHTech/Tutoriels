# 01 — C'est quoi le terminal ?

> **Durée estimée :** 10 min
> **Prérequis :** aucun
> **Objectif :** comprendre ce qu'est un terminal et savoir l'ouvrir dans VSCode

---

## Le terminal, c'est quoi ?

Tu es habitué à utiliser ton ordinateur avec la souris : tu cliques sur des icônes, tu ouvres des dossiers, tu double-cliques pour lancer des programmes.

Le terminal, c'est la même chose, mais **en texte**. Au lieu de cliquer, tu **tapes des commandes**.

```text
Exemple :
  Avec la souris → ouvrir l'explorateur de fichiers, naviguer dans les dossiers
  Avec le terminal → taper :  dir
  Résultat : la liste des fichiers s'affiche dans le terminal
```

> [!NOTE]
> Le terminal a plein de noms différents : **terminal**, **console**, **invite de commandes**, **shell**…
> C'est la même idée. Dans ce TP, on utilise toujours le terminal **intégré dans VSCode**.

---

## Pourquoi on utilise le terminal ?

Parce que pour programmer, on a souvent besoin de :
- **lancer un programme Python** (`python mon_script.py`)
- **installer une bibliothèque** (`pip install pygame`)
- **vérifier qu'un outil est installé** (`python --version`)

Ces actions se font beaucoup plus facilement en tapant une commande que par un clic.

---

## Comment ouvrir le terminal dans VSCode

Via le menu en haut :

```
Terminal  →  New Terminal
```

Une zone noire apparaît en bas de VSCode. C'est le terminal !

---

## À quoi ça ressemble ?

Une fois ouvert, tu verras quelque chose comme ça en bas de VSCode :

```text
PS C:\Users\TonPrénom\Documents\TP-Robot>
```

- **PS** = PowerShell (le type de terminal utilisé)
- **C:\Users\...** = là où tu te trouves dans les dossiers (comme une adresse)
- **>** = le curseur, là où tu tapes

---

## Essaie !

Ouvre le terminal et tape cette commande, puis appuie sur **Entrée** :

```bash
echo Bonjour le terminal !
```

Tu devrais voir s'afficher :

```text
Bonjour le terminal !
```

---

## Cases à cocher

- [ ] J'ai ouvert le terminal dans VSCode
- [ ] J'ai tapé `echo Bonjour le terminal !` et vu la réponse

---

## Mini-quiz

**Question 1 :** À quoi sert le terminal ?

<details>
<summary>💡 Voir la réponse</summary>

Le terminal permet d'envoyer des commandes texte à l'ordinateur, sans utiliser la souris. C'est indispensable pour lancer des programmes Python, installer des bibliothèques, etc.

</details>

**Question 2 :** Comment ouvre-t-on le terminal dans VSCode ?

<details>
<summary>💡 Voir la réponse</summary>

Via le menu **Terminal → New Terminal** en haut de VSCode.

</details>

---

> [!TIP]
> Si tu fais une faute de frappe dans une commande, le terminal affiche une erreur. C'est normal ! Relis la commande et réessaie. Ça arrive à tout le monde.

---

⬅ [Retour au setup](./README.md) · [Suivant ➡ Installer VSCode](./02-installer-vscode.md)
