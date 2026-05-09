# A-01 — Hello Python

> **Pour qui :** Groupe A
> **Durée estimée :** 10 min
> **Prérequis :** [Quiz réseau](../01-bases-communes/04-quiz-reseau.md)
> **Objectif :** créer et lancer ton premier script Python dans le terminal VSCode

---

## Créer un fichier Python

Dans VSCode :

1. Clique sur **Fichier → Nouveau fichier**
2. Nomme-le `hello.py`
3. Enregistre-le dans ton dossier de travail

---

## Écrire le programme

Tape ce code dans `hello.py` :

```python
print("Bonjour, je suis le Groupe A !")
```

---

## Lancer le programme

Ouvre le terminal VSCode (**Terminal → New Terminal**) et tape :

```bash
python hello.py
```

Tu dois voir s'afficher :

```text
Bonjour, je suis le Groupe A !
```

---

## Comprendre le code

```python
print("Bonjour, je suis le Groupe A !")
```

- `print(...)` → une **fonction** : elle affiche du texte dans le terminal
- `"Bonjour..."` → une **chaîne de caractères** (du texte) entourée de guillemets

> [!NOTE]
> En Python, chaque ligne de code est une **instruction**. L'ordinateur les lit et les exécute dans l'ordre, de haut en bas.

---

## Exercice

Modifie le programme pour afficher ton prénom. Par exemple :

```text
Bonjour, je m'appelle Léa !
```

<details>
<summary>💡 Voir la solution</summary>

```python
print("Bonjour, je m'appelle Léa !")
```

Change simplement le texte entre guillemets.

</details>

---

## Défi bonus 🎯

Affiche 3 lignes différentes avec 3 `print()`. Par exemple :

```text
Ligne 1
Ligne 2
Ligne 3
```

<details>
<summary>💡 Voir la solution</summary>

```python
print("Ligne 1")
print("Ligne 2")
print("Ligne 3")
```

</details>

---

## Cases à cocher

- [ ] J'ai créé `hello.py`
- [ ] J'ai lancé le script avec `python hello.py`
- [ ] J'ai vu mon message s'afficher dans le terminal

---

⬅ [Retour parcours Groupe A](./README.md) · [Suivant ➡ Récepteur UDP](./02-premier-udp-recepteur.md)
