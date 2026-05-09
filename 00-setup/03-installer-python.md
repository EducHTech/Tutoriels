# 03 — Installer Python

> **Durée estimée :** 10 min
> **Prérequis :** [VSCode installé](./02-installer-vscode.md)
> **Objectif :** avoir Python installé et accessible depuis le terminal

---

## Déjà installé ?

Ouvre le terminal VSCode (`Ctrl + ù`) et tape :

```bash
python --version
```

- Si tu vois quelque chose comme `Python 3.x.x` → déjà installé ✅, passe à [l'étape suivante](./04-extensions-vscode-python.md)
- Si tu vois une erreur → il faut l'installer

---

## Installation

### 1. Télécharger Python

Va sur : [https://www.python.org/downloads/](https://www.python.org/downloads/)

Clique sur le gros bouton jaune **Download Python 3.x.x**.

### 2. Lancer l'installeur

Double-clique sur le fichier `.exe` téléchargé.

> [!IMPORTANT]
> **ATTENTION** : avant de cliquer sur "Install Now", coche **absolument** cette case :
>
> ```
> ✅ Add Python.exe to PATH
> ```
>
> C'est la case tout en bas de la première fenêtre.
> Si tu ne la coches pas, Python ne fonctionnera pas depuis le terminal.

Ensuite clique sur **Install Now**.

### 3. Fin de l'installation

Clique sur **Close** quand c'est terminé.

---

## Vérifier l'installation

Ferme le terminal s'il était déjà ouvert (croix sur le terminal), puis rouvre-le avec `Ctrl + ù`.

Tape :

```bash
python --version
```

Tu dois voir :

```text
Python 3.x.x
```

Tape aussi :

```bash
pip --version
```

Tu dois voir quelque chose comme :

```text
pip 23.x.x from C:\...
```

`pip` est l'outil qui sert à installer des bibliothèques Python. On en aura besoin plus tard.

---

## Cases à cocher

- [ ] `python --version` affiche un numéro de version
- [ ] `pip --version` affiche un numéro de version

---

## Mini-quiz

**Question :** Pourquoi est-il important de cocher "Add Python to PATH" ?

<details>
<summary>💡 Voir la réponse</summary>

Sans cocher cette case, ton système d'exploitation ne sait pas où trouver Python. Quand tu tapes `python` dans le terminal, il répond "commande introuvable". En cochant "Add to PATH", on lui dit où chercher.

</details>

---

> [!WARNING]
> Si `python --version` affiche toujours une erreur après l'installation, réessaie en fermant puis rouvrant complètement VSCode.
> Si ça ne fonctionne toujours pas, consulte la [page de dépannage](../99-annexes/depannage.md).

---

⬅ [Précédent — Installer VSCode](./02-installer-vscode.md) · [Suivant ➡ Extension Python](./04-extensions-vscode-python.md)
