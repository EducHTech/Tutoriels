# 05 — Capteurs de l'Auriga

> **Durée estimée :** 30 min  
> **Prérequis :** [Moteurs I2C](./04-moteurs-i2c.md) terminé  
> **Matériel :** carte ME Auriga (Mega 2560)  
> **👤 Étudiant A** — travail en parallèle avec les étapes 06 et 07

---

## Avant de commencer — Installer la bibliothèque MeAuriga

La bibliothèque MeAuriga est déjà dans le repo, dans le dossier `MiniRobot/Auriga-Firmware/src/`.
Pas besoin de la télécharger : il suffit de la copier au bon endroit.

**Installation en 3 étapes :**

1. Crée un dossier `MeAuriga` dans ton dossier de bibliothèques Arduino :  
   `Documents/Arduino/libraries/MeAuriga/`

2. Copie **tous** les fichiers `.h` et `.cpp` depuis `MiniRobot/Auriga-Firmware/src/` dans ce dossier.

3. Redémarre l'Arduino IDE. La bibliothèque doit apparaître dans `Croquis > Inclure une bibliothèque > MeAuriga`.

> ✅ **Vérifie** en ouvrant l'exemple `Fichier > Exemples > MeAuriga` — s'il apparaît, c'est bon.

---

## Vue d'ensemble

Sur l'Auriga, trois capteurs sont déjà intégrés sur la carte :

| Capteur | Interface | Adresse |
|---|---|---|
| Gyroscope MPU-6050 | I2C | `0x69` |
| Tension batterie | ADC | Pin `A4` |
| 2 encodeurs moteur | Interruptions matérielles | SLOT1 / SLOT2 |

Dans ce module, tu vas lire ces 3 capteurs et les afficher dans le moniteur série.  
Aucun moteur n'est nécessaire pour ce module.

---

## Étape 1 — Gyroscope (angle de rotation)

### 🎯 Objectif
Afficher l'angle Z (lacet) du robot dans le moniteur série.

### 🤔 Question de réflexion
> L'angle Z change quand le robot **tourne sur lui-même** (comme une toupie).  
> Quelle valeur attends-tu si la carte est posée sur la table et **ne bouge pas** ?

<details>
<summary>💡 Indice</summary>

Le gyroscope mesure la rotation **cumulée** depuis le démarrage.  
Si le robot n'a pas bougé → l'angle devrait rester proche de **zéro**.

</details>

### ✅ Code à compléter

Crée un nouveau sketch et complète les `???` :

```cpp
#include <MeAuriga.h>

MeGyro gyro(1, 0x69); // Gyro intégré à l'Auriga, adresse 0x69

void setup() {
  Serial.begin(115200);
  gyro.begin();
  delay(1000); // Laisse le gyro se calibrer
  Serial.println("Gyro prêt");
}

void loop() {
  gyro.update(); // Recalcule les angles internes

  float z = gyro.getAngleZ(); // Angle de rotation Z en degrés

  Serial.print("AngleZ = ");
  Serial.print(???);    // TODO : affiche z avec 1 décimale
  Serial.println(" deg");

  delay(100);
}
```

> 💡 Pour afficher un `float` avec 1 décimale : `Serial.print(z, 1)`

### 🧪 Test attendu
```
AngleZ = 0.0 deg
AngleZ = 0.1 deg
AngleZ = 0.0 deg
```
Tourne la carte à la main de 90° → tu dois voir l'angle atteindre environ `90.0`.

### 🔍 Debug rapide
| Symptôme | Cause probable |
|---|---|
| Rien ne s'affiche | Vitesse du moniteur série ≠ 115200 |
| Angle dérive tout seul | Normal au démarrage, attends 2 sec |
| Erreur de compilation `MeAuriga not found` | Bibliothèque non installée |

---

## Étape 2 — Niveau de batterie (%)

### 🎯 Objectif
Afficher la tension et le niveau de batterie en pourcentage.

### 🤔 Question de réflexion
> `analogRead(A4)` retourne un nombre entre **0 et 1023**.  
> Comment transforme-t-on ce nombre en **volts** ?

<details>
<summary>💡 Indice 1 — de l'ADC au volt</summary>

La référence de l'ADC est 5 V. Donc `1023` ↔ 5 V.

```
tension_pin = analogRead(A4) × 5.0 / 1023.0
```

</details>

<details>
<summary>💡 Indice 2 — diviseur de tension</summary>

L'Auriga protège la pin ADC avec un diviseur de tension ×10.  
La vraie tension batterie = `tension_pin × 10.0`

</details>

<details>
<summary>💡 Indice 3 — vers le pourcentage</summary>

Batterie LiPo **3S** :
- **9.0 V** → 0 % (seuil de coupure de sécurité)
- **12.6 V** → 100 % (pleinement chargée)

```
percent = (tension - 9.0) / (12.6 - 9.0) × 100
```

</details>

### ✅ Code à compléter

```cpp
void loop() {
  float tension_pin = analogRead(A4) * 5.0 / 1023.0;
  float tension     = tension_pin * 10.0;

  // TODO : calcule le pourcentage avec la formule de l'indice 3 (LiPo 3S)
  float percent = ???;

  // Bloque entre 0 et 100
  if (percent < 0)   percent = 0;
  if (percent > 100) percent = 100;

  Serial.print("Batterie : ");
  Serial.print(tension, 1);
  Serial.print(" V  (");
  Serial.print((int)percent);
  Serial.println("%)");

  delay(1000);
}
```

### 🧪 Test attendu
```
Batterie : 11.4 V  (67%)
```
La valeur doit rester stable (variation < ±0.1 V).  
Une batterie 3S chargée à fond affiche ~12.5 V (98–100 %).

### 🔍 Debug rapide
| Symptôme | Cause probable |
|---|---|
| Affiche toujours `0%` | Oubli de `× 10.0` ou batterie très faible |
| Affiche toujours `100%` | Erreur dans la formule de pourcentage |
| Valeur saute partout | Mauvais contact sur la batterie |

---

## Étape 3 — Encodeurs sur la carte (SLOT1 / SLOT2)

### 🎯 Objectif
Lire la position des 2 encodeurs intégrés à la carte Auriga.

### 🤔 Question de réflexion
> Sur l'ESP32, les encodeurs étaient **simulés** (on ajoutait la vitesse au compteur).  
> Sur l'Auriga, ils sont **réels** et utilisent des **interruptions matérielles**.  
>
> Qu'est-ce qu'une interruption ? Pourquoi c'est mieux qu'une lecture dans `loop()` ?

<details>
<summary>💡 Indice</summary>

Sans interruption : le Mega lit l'encodeur **entre deux tours de `loop()`** → si `loop()` est lente, il **rate des impulsions**.

Avec interruption : dès qu'une impulsion arrive, le Mega **arrête tout**, incrémente le compteur, et reprend. **Aucune impulsion n'est perdue.**

</details>

### ✅ Code fourni — à lire et comprendre

```cpp
#include <MeAuriga.h>

MeEncoderOnBoard Encoder_1(SLOT1);
MeEncoderOnBoard Encoder_2(SLOT2);

// ↓ Ces fonctions sont appelées AUTOMATIQUEMENT à chaque tick d'encodeur
void isr_process_encoder1(void) {
  if (digitalRead(Encoder_1.getPortB()) == 0)
    Encoder_1.pulsePosMinus();
  else
    Encoder_1.pulsePosPlus();
}

void isr_process_encoder2(void) {
  if (digitalRead(Encoder_2.getPortB()) == 0)
    Encoder_2.pulsePosMinus();
  else
    Encoder_2.pulsePosPlus();
}

void setup() {
  Serial.begin(115200);

  // Attache les interruptions aux bonnes pins d'encodeur
  attachInterrupt(Encoder_1.getIntNum(), isr_process_encoder1, RISING);
  attachInterrupt(Encoder_2.getIntNum(), isr_process_encoder2, RISING);

  // Configure le timer 1 pour mettre à jour la vitesse (ne pas modifier)
  TCCR1A = _BV(WGM10);
  TCCR1B = _BV(CS11) | _BV(WGM12);
  TIMSK1 = _BV(OCIE1A);
  OCR1A  = 0xF9;

  Serial.println("Encodeurs prêts");
}

// ↓ Appelé automatiquement par le timer (ne pas modifier)
ISR(TIMER1_COMPA_vect) {
  Encoder_1.updateSpeed();
  Encoder_2.updateSpeed();
}

void loop() {
  long pos1 = Encoder_1.getCurPos();
  long pos2 = Encoder_2.getCurPos();

  Serial.print("E1 = "); Serial.print(pos1);
  Serial.print("  |  E2 = "); Serial.println(pos2);

  delay(200);
}
```

> ⚠️ **Attention :** les `ISR(...)` et le bloc `TCCR1A/TCCR1B/TIMSK1` sont du code bas niveau pour le timer. Tu n'as pas besoin de les modifier — mais essaie de comprendre leur rôle en lisant les commentaires.

### 🧪 Test attendu
- Tourne une roue à la main → le compteur augmente ou diminue
- Tourne dans l'autre sens → le compteur revient vers zéro

### 🔍 Debug rapide
| Symptôme | Cause probable |
|---|---|
| Compteurs restent à 0 | Encodeurs branchés dans le mauvais slot |
| Compteur saute de grandes valeurs | Interruptions sur la mauvaise pin |
| Erreur à la compilation | Bibliothèque MeAuriga non installée dans l'IDE |

---

## ✅ Récap — ce que tu sais maintenant

- [x] Lire l'angle Z du gyroscope (`gyro.getAngleZ()`)
- [x] Calculer la tension et le pourcentage batterie
- [x] Utiliser des interruptions pour compter les ticks d'encodeur

**Prochaine étape :** rejoins les autres étudiants pour l'[étape 08 — Firmware final](./08-firmware-final-auriga.md).
