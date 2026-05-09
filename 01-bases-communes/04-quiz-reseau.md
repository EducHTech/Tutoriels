# 04 — Quiz réseau

> **Pour qui :** les deux groupes
> **Durée estimée :** 5 min
> **Prérequis :** [UDP vs TCP](./03-udp-vs-tcp.md)
> **Objectif :** vérifier qu'on a bien compris les bases réseau avant de coder

---

Réponds aux questions dans ta tête (ou sur une feuille), puis déroule les réponses pour vérifier.

---

## Question 1

Que signifient les lettres **IP** dans "adresse IP" ?

<details>
<summary>💡 Voir la réponse</summary>

**Internet Protocol** — c'est le protocole (la règle de communication) qui définit comment les adresses des appareils sont formatées sur un réseau.

</details>

---

## Question 2

Ton ordinateur a l'adresse IP `192.168.1.10`. Ton ESP32 a l'adresse IP `192.168.1.50`.
Tu veux envoyer un message à l'ESP32 sur le port 4210.
Quelle est la **destination** du message ?

<details>
<summary>💡 Voir la réponse</summary>

La destination est : **IP `192.168.1.50`, port `4210`**

L'adresse IP identifie l'appareil (l'ESP32), le port identifie le programme qui écoute sur cet appareil.

</details>

---

## Question 3

Quel protocole est le plus rapide : TCP ou UDP ? Pourquoi ?

<details>
<summary>💡 Voir la réponse</summary>

**UDP** est plus rapide. Il envoie le message sans attendre de confirmation. TCP doit attendre que le destinataire confirme la réception, ce qui prend du temps.

</details>

---

## Question 4

On contrôle un robot avec 20 commandes par seconde. Une commande est perdue.
Est-ce grave ? Explique.

<details>
<summary>💡 Voir la réponse</summary>

**Non, ce n'est pas grave.** La prochaine commande arrive dans 50 ms (1/20 de seconde). Le robot va s'adapter très vite. En robotique, mieux vaut recevoir une nouvelle commande un peu plus tard que d'attendre la confirmation d'une vieille commande.

</details>

---

## Question 5

Comment s'appelle un message UDP ?

<details>
<summary>💡 Voir la réponse</summary>

Un **datagramme**.

</details>

---

## Score

- 5/5 → 🚀 Tu peux avancer !
- 3-4/5 → 📖 Relis rapidement [UDP vs TCP](./03-udp-vs-tcp.md)
- 0-2/5 → 🔄 Relis les pages [02](./02-adresse-ip-et-port.md) et [03](./03-udp-vs-tcp.md)

---

## Cases à cocher

- [ ] J'ai répondu aux 5 questions
- [ ] Je comprends les concepts de base réseau

---

**Maintenant, rejoins le dossier de ton groupe !**

👉 [Je suis dans le **Groupe A** — Driver Station](../groupe-A-driver-station/README.md)
👉 [Je suis dans le **Groupe B** — Robot ESP32](../groupe-B-robot-esp32/README.md)

---

⬅ [Précédent — UDP vs TCP](./03-udp-vs-tcp.md)
