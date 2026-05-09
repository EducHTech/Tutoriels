# 03 — UDP vs TCP

> **Pour qui :** les deux groupes
> **Durée estimée :** 10 min
> **Prérequis :** [Adresse IP et port](./02-adresse-ip-et-port.md)
> **Objectif :** comprendre pourquoi on utilise UDP pour la robotique

---

## Deux façons d'envoyer un message réseau

Il existe deux grands protocoles pour envoyer des données sur un réseau : **TCP** et **UDP**.

---

## TCP — fiable mais lent

**TCP** (Transmission Control Protocol) vérifie que le message est bien arrivé.

Imagine envoyer une lettre recommandée :
1. Tu envoies la lettre
2. Le destinataire signe une confirmation
3. Tu reçois la confirmation que la lettre est arrivée

C'est fiable, mais ça prend plus de temps.

**Utilisé pour :** naviguer sur le web, envoyer des emails, télécharger des fichiers.

---

## UDP — rapide mais sans garantie

**UDP** (User Datagram Protocol) envoie le message **sans vérifier** qu'il est arrivé.

Imagine envoyer un message dans une bouteille à la mer :
- Tu envoies
- Tu ne sais pas s'il est arrivé
- Tu n'attends pas de confirmation

C'est très rapide, mais le message peut se perdre.

**Utilisé pour :** streaming vidéo, jeux en ligne, robotique.

---

## Comparaison

| | TCP | UDP |
|---|---|---|
| Fiabilité | ✅ Garanti | ❌ Pas garanti |
| Vitesse | Lent | **Rapide** |
| Confirmation | Oui | Non |
| Usage | Web, email | Robots, jeux, vidéo |

---

## Pourquoi UDP pour la robotique ?

En robotique, on envoie des commandes **très fréquemment** (ex : 20 fois par seconde).

Si une commande `MOTOR:120` se perd, ce n'est pas grave : la suivante va arriver dans 50 ms. Il vaut mieux recevoir une commande récente un peu tard qu'une vieille commande "garantie".

> [!NOTE]
> Un message UDP s'appelle un **datagramme**. C'est juste le nom technique d'un paquet UDP.

---

## La latence

La **latence** c'est le temps entre l'envoi et la réception d'un message.

```text
Faible latence = réaction rapide du robot
Haute latence  = robot qui répond en retard (mauvais pour le contrôle !)
```

UDP a une latence plus faible que TCP, ce qui le rend idéal pour contrôler un robot en temps réel.

---

## Cases à cocher

- [ ] Je comprends la différence entre TCP et UDP
- [ ] Je sais pourquoi on utilise UDP en robotique

---

## Mini-quiz

**Question 1 :** Quelle différence principale entre TCP et UDP ?

<details>
<summary>💡 Voir la réponse</summary>

TCP vérifie que chaque message arrive (fiable mais lent). UDP envoie sans vérification (rapide mais sans garantie de livraison).

</details>

**Question 2 :** Pourquoi préfère-t-on UDP en robotique plutôt que TCP ?

<details>
<summary>💡 Voir la réponse</summary>

En robotique, la vitesse est prioritaire sur la fiabilité. Si une commande se perd, la suivante va arriver très vite. UDP réduit la latence, ce qui améliore la réactivité du robot.

</details>

---

⬅ [Précédent — IP et port](./02-adresse-ip-et-port.md) · [Suivant ➡ Quiz réseau](./04-quiz-reseau.md)
