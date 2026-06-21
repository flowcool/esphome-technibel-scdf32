# Stratégies de pilotage / Control Strategies

**[🇫🇷 Français](#-français)** · **[🇬🇧 English](#-english)**

---

## 🇫🇷 Français

Ce document compare les différentes approches pour piloter la clim Technibel depuis Home Assistant,
du plus simple au plus invasif.

---

### Piste A — ESP32 monté derrière/sous la clim ✅ (recommandée)

**Principe :** installer une double prise derrière l'unité intérieure, y brancher un adaptateur USB,
et coller la LED IR directement sous le récepteur de la clim.

**Avantages :**
- Distance LED → récepteur : ~5 cm → aucun problème de puissance ni d'angle
- N'importe quelle LED 940nm 5mm suffit (y compris la TSAL6400 actuelle)
- Non invasif, entièrement réversible
- Câblage identique au schéma principal (`docs/wiring.md`)

**Matériel supplémentaire :**
- 1 double prise électrique (faible courant USB suffit — 500 mA)
- 1 adaptateur secteur → USB 5V
- Éventuellement un peu de velcro ou de double face pour fixer l'ESP32

**Points d'attention :**
- Vérifier que la prise peut être installée derrière la clim sans gêner la fixation murale
- Laisser un accès pour éventuellement reflasher l'ESP32 via USB

---

### Piste B1 — Injection directe sur le récepteur IR interne

**Principe :** à l'intérieur de l'unité intérieure se trouve un récepteur IR (composant TSOP,
3 broches : VCC, GND, Signal). On branche l'ESP32 directement sur la broche Signal et on
envoie les trames électriquement, sans émission IR physique.

```
TSOP interne
┌──────────┐
│  VCC     │ ← 3.3V ou 5V (selon le board clim)
│  GND     │ ← GND commun avec ESP32
│  Signal  │ ← brancher ici la sortie GPIO de l'ESP32
└──────────┘
```

**Avantages :**
- Zéro contrainte optique (angle, distance, faisceau)
- Signal électrique direct = fiabilité maximale
- Réversible : débrancher les 3 fils suffit à revenir à l'état d'origine

**Étapes :**
1. Ouvrir le capot de l'unité intérieure (vis cachées sous les grilles ou caches)
2. Localiser le module récepteur IR (petit composant noir 3 broches sur une petite carte ou directement sur le PCB principal)
3. Identifier les 3 broches : VCC, GND, Signal (datasheet TSOP38438 ou équivalent)
4. Mesurer la tension VCC du récepteur (3.3V ou 5V) pour configurer l'ESP32
5. Brancher la sortie GPIO4 de l'ESP32 sur la broche Signal du TSOP
6. Brancher les GND ensemble
7. **Ne pas alimenter le TSOP depuis l'ESP32** — le laisser alimenté par le board clim

**Points d'attention :**
- Couper l'alimentation de la clim avant toute intervention
- Ne pas toucher aux condensateurs ni aux circuits haute tension (partie compresseur)
- L'unité intérieure (évaporateur) est basse tension (12V ou 5V logique) — la partie dangereuse est l'unité extérieure ou le tableau électrique
- Faire une photo du câblage original avant de toucher quoi que ce soit

---

### Piste B2 — Interception du bus interne PCB

**Principe :** identifier le protocole de communication entre le récepteur IR et le
microcontrôleur principal de la clim (souvent UART, I²C ou un bus propriétaire),
puis s'y intercaler pour envoyer des commandes directement au MCU.

**Avantages :**
- Contournement total du récepteur IR
- Contrôle potentiellement plus riche (lecture d'état, températures internes, etc.)

**Inconvénients :**
- Nécessite du reverse engineering sur le PCB (oscilloscope recommandé)
- Protocole potentiellement propriétaire et non documenté
- Risque de brick du board clim si mauvaise manipulation
- Beaucoup plus long à mettre en œuvre

**Quand l'envisager :** uniquement si la Piste B1 échoue ou si on veut lire des données
internes (température du serpentin, état du compresseur, etc.) non disponibles via IR.

---

### Tableau récapitulatif

| Critère | Piste A | Piste B1 | Piste B2 |
|---|---|---|---|
| Difficulté | Facile | Moyenne | Avancée |
| Invasif | Non | Légèrement | Oui |
| Réversible | Oui | Oui | Partiellement |
| Fiabilité | Bonne | Excellente | Excellente |
| Temps d'installation | 30 min | 1–2h | Plusieurs jours |
| Risque matériel | Aucun | Faible | Modéré |

---

## 🇬🇧 English

This document compares the different approaches to control the Technibel AC unit from Home Assistant,
from simplest to most invasive.

---

### Option A — ESP32 mounted behind/under the AC unit ✅ (recommended)

**Principle:** install a power outlet behind the indoor unit, plug in a USB adapter,
and stick the IR LED directly under the AC receiver window.

**Advantages:**
- LED to receiver distance: ~5 cm → no power or angle issues whatsoever
- Any 940nm 5mm LED works (including the current TSAL6400)
- Non-invasive, fully reversible
- Same wiring as the main schematic (`docs/wiring.md`)

**Additional hardware:**
- 1 electrical outlet (low current — 500 mA USB is enough)
- 1 mains → USB 5V adapter
- Some velcro or double-sided tape to mount the ESP32

**Watch out for:**
- Make sure the outlet can fit behind the AC without blocking the wall mount
- Leave USB access for reflashing the ESP32 if needed

---

### Option B1 — Direct injection into the internal IR receiver

**Principle:** inside the indoor unit there is an IR receiver (TSOP component, 3 pins: VCC, GND, Signal).
Connect the ESP32 directly to the Signal pin and send frames electrically, with no physical IR emission.

```
Internal TSOP
┌──────────┐
│  VCC     │ ← 3.3V or 5V (depending on AC board)
│  GND     │ ← common GND with ESP32
│  Signal  │ ← connect ESP32 GPIO output here
└──────────┘
```

**Advantages:**
- Zero optical constraints (angle, distance, beam)
- Direct electrical signal = maximum reliability
- Reversible: disconnect 3 wires to restore original state

**Steps:**
1. Open the indoor unit cover (screws hidden under grilles or covers)
2. Locate the IR receiver module (small black 3-pin component on a sub-board or main PCB)
3. Identify the 3 pins: VCC, GND, Signal (TSOP38438 datasheet or equivalent)
4. Measure the VCC voltage (3.3V or 5V) to configure the ESP32 accordingly
5. Connect ESP32 GPIO4 output to the TSOP Signal pin
6. Connect GNDs together
7. **Do not power the TSOP from the ESP32** — leave it powered by the AC board

**Watch out for:**
- Cut power to the AC unit before any intervention
- Do not touch capacitors or high-voltage circuits (compressor side)
- The indoor unit (evaporator) is low voltage (12V or 5V logic) — the dangerous parts are the outdoor unit and the electrical panel
- Photograph original wiring before touching anything

---

### Option B2 — Internal PCB bus interception

**Principle:** identify the communication protocol between the IR receiver and the AC's main
microcontroller (often UART, I²C, or a proprietary bus), then insert the ESP32 in-line
to send commands directly to the MCU.

**Advantages:**
- Completely bypasses the IR receiver
- Potentially richer control (state readback, internal temperatures, etc.)

**Disadvantages:**
- Requires PCB reverse engineering (oscilloscope recommended)
- Protocol may be proprietary and undocumented
- Risk of bricking the AC board if mishandled
- Much longer to implement

**When to consider:** only if Option B1 fails, or if you need to read internal data
(coil temperature, compressor state, etc.) not available via IR.

---

### Summary table

| Criteria | Option A | Option B1 | Option B2 |
|---|---|---|---|
| Difficulty | Easy | Medium | Advanced |
| Invasive | No | Slightly | Yes |
| Reversible | Yes | Yes | Partially |
| Reliability | Good | Excellent | Excellent |
| Install time | 30 min | 1–2h | Several days |
| Hardware risk | None | Low | Moderate |
