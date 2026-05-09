# 05 — Installer Git et cloner le dépôt

> **Durée estimée :** 15 min
> **Prérequis :** [VSCode installé](./02-installer-vscode.md)
> **Objectif :** installer Git, comprendre ce qu'est un dépôt, et télécharger les fichiers du TP

---

## C'est quoi Git ?

Imagine que tu travailles sur un jeu vidéo et tu fais une sauvegarde toutes les heures.
Si tu fais une erreur, tu peux revenir à la sauvegarde précédente.

**Git, c'est un outil de sauvegarde pour le code.** Il permet de :
- garder l'historique de toutes les modifications
- travailler à plusieurs sur le même projet
- télécharger le code d'un projet partagé en ligne

> [!NOTE]
> Dans ce TP, on utilise Git uniquement pour **télécharger les fichiers** du projet (ce qu'on appelle "cloner un dépôt"). On ne commitera pas.

---

## Déjà installé ?

Ouvre le terminal VSCode (`Ctrl + ù`) et tape :

```bash
git --version
```

- Si tu vois `git version 2.x.x` → déjà installé ✅, passe directement à [Cloner le dépôt](#cloner-le-dépôt)
- Sinon → installe Git

---

## Installation de Git

### 1. Télécharger Git

Va sur : [https://git-scm.com/download/win](https://git-scm.com/download/win)

Le téléchargement démarre automatiquement.

### 2. Installer

Lance l'installeur. Tu peux laisser **toutes les options par défaut** et cliquer sur "Next" jusqu'à la fin.

> [!TIP]
> À l'étape "Choosing the default editor used by Git", tu peux choisir **Visual Studio Code** si c'est proposé dans la liste.

### 3. Vérifier

Ferme et rouvre VSCode, puis dans le terminal :

```bash
git --version
```

Tu dois voir un numéro de version.

---

## Cloner le dépôt

"Cloner" = télécharger une copie complète du projet sur ton ordinateur.

### 1. Aller dans le bon dossier

Dans le terminal, navigue vers ton dossier de travail. Par exemple :

```bash
cd C:\Users\TonPrénom\Documents
```

> [!TIP]
> `cd` signifie "change directory" = changer de dossier. C'est comme double-cliquer sur un dossier dans l'explorateur.

### 2. Cloner le dépôt

Tape la commande suivante :

```bash
git clone <URL_DU_DEPOT>
```

> [!NOTE]
> Remplace `<URL_DU_DEPOT>` par l'URL fournie par ton professeur. Elle ressemble à `https://github.com/xxx/yyy.git`

### 3. Ouvrir le projet dans VSCode

Un nouveau dossier a été créé. Ouvre-le dans VSCode :

```
Fichier → Ouvrir le dossier...
```

Sélectionne le dossier qui vient d'être créé.

### 4. Mettre à jour le projet (si besoin)

Si le prof modifie les fichiers en ligne, tu peux mettre à jour ta copie locale avec :

```bash
git pull
```

---

## Cases à cocher

- [ ] `git --version` affiche un numéro de version
- [ ] J'ai cloné le dépôt du TP
- [ ] J'ai ouvert le dossier dans VSCode

---

## Mini-quiz

**Question :** Quelle commande Git permet de télécharger un projet pour la première fois ?

<details>
<summary>💡 Voir la réponse</summary>

`git clone <URL>` — cette commande crée une copie locale complète du dépôt distant.

</details>

---

⬅ [Précédent — Extension Python](./04-extensions-vscode-python.md) · [Suivant ➡ Bases communes ➡](../01-bases-communes/01-introduction-projet.md)

*(Groupe B seulement : [Installer Arduino IDE ➡](./06-installer-arduino-ide-esp32.md))*
