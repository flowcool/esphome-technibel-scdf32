# Dépannage circuit IR / IR Circuit Troubleshooting

**[🇫🇷 Français](#-français)** · **[🇬🇧 English](#-english)**

---

## 🇫🇷 Français

### Symptôme : la LED IR n'émet rien (caméra ne voit aucun flash)

> Note : le test caméra smartphone n'est **pas fiable** pour les LED IR à 940nm (TSAL6400).
> La plupart des téléphones modernes ont un filtre qui bloque cette longueur d'onde.
> Vérifier d'abord avec une télécommande TV : si la caméra ne voit pas non plus la télécommande, elle est inutilisable pour ce test.

---

### Étape 1 — Vérifier le transistor (hors circuit, multimètre mode diode ►|)

Retirer le transistor de la breadboard. Face plate vers soi, pattes vers le bas :

| Sonde rouge | Sonde noire | Valeur attendue |
|---|---|---|
| Base (milieu) | Emitter (gauche) | ~600–700 mV |
| Base (milieu) | Collector (droite) | ~600–700 mV |
| Toute autre combinaison | | OL (circuit ouvert) |

- Valeurs ~650 mV dans les deux premiers cas → **transistor OK**
- OL dans les deux premiers cas → **transistor mort**, le remplacer

---

### Étape 2 — Vérifier la LED IR (hors circuit, multimètre mode diode ►|)

| Sonde rouge | Sonde noire | Valeur attendue |
|---|---|---|
| Anode (longue patte) | Cathode (courte patte) | ~1.0–1.4 V |
| Cathode | Anode | OL |

- ~1.1–1.4 V dans le premier sens → **LED OK**
- OL dans les deux sens → **LED morte**, la remplacer

---

### Étape 3 — Vérifier le câblage (multimètre mode continuité, bip)

Tester chaque maillon de la chaîne séparément.

> ⚠️ Une résistance (47Ω ou 470Ω) ne bipe **pas** en mode continuité — c'est normal.
> Tester chaque côté de la résistance séparément.

| De | Vers | Attendu |
|---|---|---|
| Fil GND | Patte Emitter (gauche) du transistor | bip |
| Fil GPIO4 | Patte d'entrée de la résistance 470Ω | bip |
| Patte de sortie de la résistance 470Ω | Patte Base (milieu) du transistor | bip |
| Patte Collector (droite) du transistor | Cathode LED (courte patte) | bip |
| Fil 5V | Patte d'entrée de la résistance 47Ω | bip |
| Patte de sortie de la résistance 47Ω | Anode LED (longue patte) | bip |

Un bip manquant = connexion coupée à cet endroit (patte pas dans la bonne rangée breadboard, ou fil mal inséré).

---

### Étape 4 — Vérifier les tensions en circuit (multimètre DC, fil noir sur GND)

Alimenter l'ESP32 et envoyer une commande IR depuis Home Assistant pendant la mesure.

| Point de mesure | Valeur attendue | Si anormal |
|---|---|---|
| Fil 5V (avant résistance 47Ω) | ~5 V | Mauvaise broche ESP32 (Vin vs 3V3) |
| Base du transistor (patte milieu) | ~0.3–0.7 V (signal pulsé) | GPIO4 ne pilote pas le transistor |
| Collector du transistor (patte droite) | chute à ~0.2 V pendant IR | Transistor ne conduit pas |
| Anode LED (longue patte) | ~1.5 V pendant IR, ~5 V au repos | Circuit LED ouvert |

---

### Rappel brochage 2N2222A TO-92

```
Face plate avec inscription vers soi, pattes vers le bas :

┌──────────┐
│ 2N2222A  │
└──────────┘
  │    │    │
  E    B    C
(GND)(sig)(LED cathode)
```

---

## 🇬🇧 English

### Symptom: IR LED emits nothing (camera sees no flash)

> Note: smartphone camera test is **not reliable** for 940nm IR LEDs (TSAL6400).
> Most modern phones have an IR cut filter at this wavelength.
> First test with a TV remote: if the camera can't see the remote either, it cannot be used for this test.

---

### Step 1 — Check the transistor (out of circuit, multimeter diode mode ►|)

Remove transistor from breadboard. Flat face toward you, pins pointing down:

| Red probe | Black probe | Expected |
|---|---|---|
| Base (middle) | Emitter (left) | ~600–700 mV |
| Base (middle) | Collector (right) | ~600–700 mV |
| Any other combination | | OL (open circuit) |

- ~650 mV in first two cases → **transistor OK**
- OL in first two cases → **transistor dead**, replace it

---

### Step 2 — Check the IR LED (out of circuit, multimeter diode mode ►|)

| Red probe | Black probe | Expected |
|---|---|---|
| Anode (long leg) | Cathode (short leg) | ~1.0–1.4 V |
| Cathode | Anode | OL |

- ~1.1–1.4 V in forward direction → **LED OK**
- OL in both directions → **LED dead**, replace it

---

### Step 3 — Check wiring (multimeter continuity mode, beep)

Test each link in the chain separately.

> ⚠️ A resistor (47Ω or 470Ω) will **not** beep in continuity mode — this is normal.
> Test each side of the resistor separately.

| From | To | Expected |
|---|---|---|
| GND wire | Transistor Emitter (left pin) | beep |
| GPIO4 wire | Input leg of 470Ω resistor | beep |
| Output leg of 470Ω resistor | Transistor Base (middle pin) | beep |
| Transistor Collector (right pin) | LED Cathode (short leg) | beep |
| 5V wire | Input leg of 47Ω resistor | beep |
| Output leg of 47Ω resistor | LED Anode (long leg) | beep |

Missing beep = broken connection at that point (leg not in the same breadboard row, or wire not fully inserted).

---

### Step 4 — Check voltages in circuit (DC mode, black probe on GND)

Power the ESP32 and send an IR command from Home Assistant during measurement.

| Measurement point | Expected value | If abnormal |
|---|---|---|
| 5V wire (before 47Ω resistor) | ~5 V | Wrong ESP32 pin (Vin vs 3V3) |
| Transistor Base (middle pin) | ~0.3–0.7 V (pulsed signal) | GPIO4 not driving transistor |
| Transistor Collector (right pin) | drops to ~0.2 V during IR | Transistor not conducting |
| LED Anode (long leg) | ~1.5 V during IR, ~5 V idle | LED circuit open |

---

### 2N2222A TO-92 pinout reminder

```
Flat face with text toward you, pins pointing down:

┌──────────┐
│ 2N2222A  │
└──────────┘
  │    │    │
  E    B    C
(GND)(sig)(LED cathode)
```
