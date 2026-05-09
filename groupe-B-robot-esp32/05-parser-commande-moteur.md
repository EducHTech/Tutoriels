# B-05 — Parser une commande moteur

> **Pour qui :** Groupe B
> **Durée estimée :** 15 min
> **Prérequis :** [Contrôle LED](./04-controle-led.md)
> **Objectif :** décoder le format `MOTOR:120` pour extraire la valeur de vitesse

---

## Le format de commande moteur

Le Groupe A envoie des commandes comme :

```text
MOTOR:120
MOTOR:-50
MOTOR:0
```

L'ESP32 doit extraire la valeur numérique (`120`, `-50`, `0`) pour l'utiliser.

Cette opération s'appelle **parser** (analyser/découper) une chaîne de texte.

---

## Les outils C++ nécessaires

### `startsWith()`

```cpp
commande.startsWith("MOTOR:")
```

Renvoie `true` si le texte commence par `"MOTOR:"`.

### `substring(n)`

```cpp
commande.substring(6)
```

Renvoie le texte à partir du caractère n°6 (on saute les 6 premiers caractères de `"MOTOR:"`).

```text
"MOTOR:120"
 012345
       → substring(6) → "120"
```

### `toInt()`

```cpp
String("120").toInt()
```

Convertit le texte `"120"` en entier `120`.

---

## Ajouter le parsing à ton programme

Dans la boucle `loop()`, ajoute après le bloc `LED_OFF` :

```cpp
else if (commande.startsWith("MOTOR:"))
{
    // Extraire la valeur après "MOTOR:"
    String valeurTexte = commande.substring(6);
    int vitesse = valeurTexte.toInt();

    Serial.print("Vitesse moteur reçue : ");
    Serial.println(vitesse);

    // Ici tu brancheras ton vrai moteur !
    // Pour l'instant on affiche juste la valeur.
}
```

---

## Tester

Depuis Python, envoie :

```python
sock.sendto("MOTOR:120".encode(), ("192.168.X.XX", 4210))
sock.sendto("MOTOR:-50".encode(), ("192.168.X.XX", 4210))
```

Le Moniteur Série doit afficher :

```text
Vitesse moteur reçue : 120
Vitesse moteur reçue : -50
```

---

## Cas avancé — deux moteurs (différentiel)

Le Groupe A peut envoyer :

```text
MOTOR:120:80
```

`120` = moteur gauche, `80` = moteur droit.

Pour découper ça, utilise `indexOf()` :

```cpp
else if (commande.startsWith("MOTOR:"))
{
    String valeurs = commande.substring(6);   // "120:80"
    int separateur = valeurs.indexOf(':');

    if (separateur > 0)
    {
        // Deux moteurs
        int gauche = valeurs.substring(0, separateur).toInt();
        int droite = valeurs.substring(separateur + 1).toInt();
        Serial.print("Gauche : "); Serial.print(gauche);
        Serial.print(" | Droite : "); Serial.println(droite);
    }
    else
    {
        // Un seul moteur
        int vitesse = valeurs.toInt();
        Serial.print("Vitesse : "); Serial.println(vitesse);
    }
}
```

---

## Cases à cocher

- [ ] `MOTOR:120` affiche la valeur `120` dans le Moniteur Série
- [ ] `MOTOR:-50` affiche `-50`
- [ ] (Bonus) `MOTOR:120:80` affiche les deux valeurs séparément

---

## Mini-quiz

**Question :** Que retourne `"MOTOR:255".substring(6)` ?

<details>
<summary>💡 Voir la réponse</summary>

`"255"` — on saute les 6 premiers caractères (`M`, `O`, `T`, `O`, `R`, `:`), il reste `"255"`.

</details>

---

⬅ [Précédent — Contrôle LED](./04-controle-led.md) · [Suivant ➡ Lecture capteur](./06-lecture-capteur.md)
