# Stratégies de pilotage / Control Strategies

**[🇫🇷 Français](#-français)** · **[🇬🇧 English](#-english)**

---

## 🇫🇷 Français

Ce document compare les différentes approches pour piloter la clim Technibel depuis Home Assistant,
du plus simple au plus invasif.

---

### ⚡ Prérequis — Alimentation de l'ESP32

**C'est le point d'entrée de tout.** Avant de choisir une piste, il faut savoir d'où vient le jus.

L'unité intérieure a toujours une alimentation interne pour son propre MCU et récepteur IR :

```
220V ──► SMPS interne ──► 12V  (moteur ventilateur)
                      └──► 5V ou 3.3V  (logique MCU, TSOP, afficheur)
```

**À faire à la première ouverture de la clim :**
1. Couper au disjoncteur, attendre 5 min (condensateurs)
2. Ouvrir le capot
3. Vérifier l'isolation secteur/logique (voir plan phase 12)
4. Mesurer les tensions disponibles sur le PCB (chercher les rails d'alimentation, souvent marqués +5V, +12V, GND)
5. Évaluer la capacité du rail (≥500mA de marge pour un XIAO avec WiFi)

| Rail trouvé | Solution alimentation ESP32 |
|---|---|
| 5V interne, capacité suffisante | Brancher sur la broche 5V du XIAO via diode Schottky (SS14, anode côté rail, cathode côté XIAO — recommandation Seeed pour alimentation externe par broche 5V). **Ne JAMAIS brancher 5V sur la broche 3V3** — cela détruit le régulateur. |
| 12V uniquement | Ajouter un module buck 12V→5V (~1€, taille timbre-poste) → broche 5V via diode |
| Rien d'accessible | Revenir à la Piste A (prise externe) |

**Si l'alim interne est exploitable → installation 100% intégrée :**
- Zéro multiprise
- Zéro câble visible
- L'ESP32 vit dans la clim et s'alimente depuis la clim

---

### Piste A — ESP32 monté derrière/sous la clim

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
┌──────────────────────────────┐
│  photodiode → filtre 38kHz   │
│  → démodulateur → sortie     │
└──────────────────────────────┘
  VCC     GND     Signal (OUT)
                      ↑
               brancher ici
```

> **Note :** Le TSOP n'a pas de broche "entrée" électrique accessible — la photodiode est
> à l'intérieur du boîtier. Le seul point d'injection électrique réaliste est la broche
> Signal (sortie), côté MCU de la clim.

**Avantages :**
- Zéro contrainte optique (angle, distance, faisceau)
- Télécommande d'origine **préservée** — le TSOP reste actif et reçoit toujours l'IR
- Signal électrique direct = fiabilité maximale
- Réversible : débrancher 3 fils suffit à revenir à l'état d'origine

**Protection de l'ESP32 et isolation de niveau :**

⚠️ Les GPIO de l'ESP32-C3 ne sont **PAS tolérants 5V** (max 3.6V, datasheet Espressif).
Le GPIO ne doit JAMAIS être directement connecté à une ligne pouvant atteindre 5V,
même en mode open_drain (open_drain empêche de sourcer, mais n'empêche pas de recevoir
du 5V via les diodes ESD internes → dommage au chip).

**Circuit recommandé : BC337 comme sortie open-collector de translation de niveau.**

```
ESP32 GPIO ──[470Ω]──┬── Base BC337
                      │
                    [10kΩ] ← pull-down (OFF au boot)
                      │
GND ─────────────────┴── Emitter BC337

Ligne Signal vers MCU clim ── Collector BC337
```

Le BC337 agit comme une sortie open-collector externe :
- GPIO HIGH → BC337 conducteur → ligne tirée LOW (mark)
- GPIO LOW → BC337 coupé → ligne flottante, tirée HIGH par le circuit existant
- Aucune tension de la clim n'arrive sur le GPIO ESP32
- Fonctionne quel que soit le VCC du TSOP (3.3V ou 5V)

**Coexistence avec la télécommande :** dépend du type de sortie du TSOP.
- TSOP open-collector : pas de modification. Les deux sinkent sur la même ligne.
- TSOP push-pull : contention possible. Couper la piste TSOP→MCU et recombiner
  via wired-OR (deux diodes + pull-up). Le circuit exact dépend du PCB — à décider
  après mesures (voir plan de validation, phases 13-14).

**Étapes câblage :**
1. Vérifier l'isolation électrique de la logique clim (voir plan, phase 12)
2. Ouvrir le capot de l'unité intérieure (vis cachées sous les grilles ou caches)
3. Localiser le module récepteur IR (petit composant noir 3 broches)
4. Identifier les 3 broches : VCC, GND, Signal (datasheet du composant identifié)
5. Mesurer la tension VCC du récepteur (3.3V ou 5V)
6. Caractériser la sortie Signal avec analyseur logique (niveau idle, amplitude, type OC/PP)
7. Brancher le Collector du BC337 sur la ligne Signal
8. Brancher les GND ensemble
9. **Ne pas alimenter le TSOP depuis l'ESP32** — le laisser alimenté par le board clim

**Modification firmware :**

Changer uniquement la config `remote_transmitter` dans le YAML — `technibel_ir.h` ne change pas :

```yaml
remote_transmitter:
  pin:
    number: GPIO3
    inverted: false       # le BC337 ajoute une inversion logique :
                          # GPIO HIGH → transistor ON → ligne LOW (mark)
                          # à déterminer expérimentalement — essayer false puis true
  carrier_duty_percent: 100   # signal DC, pas de porteuse 38kHz
  non_blocking: false
  rmt_symbols: 96
```

`carrier_duty_percent: 100` est un usage officiel ESPHome, documenté pour les émetteurs RF
433MHz — même principe : timings bruts sans porteuse sur GPIO direct.

**Points d'attention :**
- Couper l'alimentation de la clim au disjoncteur avant toute intervention
- Ne pas toucher aux condensateurs ni aux circuits haute tension
- **Ne PAS supposer que la logique de l'unité intérieure est isolée du secteur** — certaines
  alimentations d'électroménager référencent la masse logique au secteur. Vérifier l'isolation
  avant de connecter tout instrument USB (analyseur logique, oscilloscope) — voir plan phase 12
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

### ⚡ Prerequisite — Powering the ESP32

**This is the entry point for everything.** Before choosing an option, find out where the power comes from.

The indoor unit always has an internal power supply for its own MCU and IR receiver:

```
220V ──► Internal SMPS ──► 12V  (fan motor)
                       └──► 5V or 3.3V  (MCU logic, TSOP, display)
```

**To do on first opening of the AC unit:**
1. Cut power at the breaker, wait 5 min (capacitors)
2. Open the cover
3. Verify mains/logic isolation (see validation plan phase 12)
4. Measure available voltages on the PCB (look for power rails, often labeled +5V, +12V, GND)
5. Evaluate rail capacity (≥500mA headroom needed for XIAO with WiFi)

| Rail found | ESP32 power solution |
|---|---|
| Internal 5V, sufficient capacity | Connect to XIAO 5V pin via Schottky diode (SS14, anode toward rail, cathode toward XIAO — per Seeed recommendation for external power via 5V pin). **NEVER connect 5V to the 3V3 pin** — this destroys the regulator. |
| 12V only | Add a 12V→5V buck module (~€1, stamp-sized) → 5V pin via diode |
| Nothing accessible | Fall back to Option A (external outlet) |

**If the internal supply works → 100% integrated install:**
- No power strip
- No visible cables
- ESP32 lives inside the AC and feeds from the AC

---

### Option A — ESP32 mounted behind/under the AC unit

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
┌──────────────────────────────┐
│  photodiode → 38kHz filter   │
│  → demodulator → output      │
└──────────────────────────────┘
  VCC     GND     Signal (OUT)
                      ↑
               connect here
```

> **Note:** The TSOP has no accessible electrical "input" pin — the photodiode is inside the package.
> The only practical electrical injection point is the Signal (output) pin, on the AC MCU side.

**Advantages:**
- Zero optical constraints (angle, distance, beam)
- Original remote control **preserved** — TSOP stays active and still receives IR
- Direct electrical signal = maximum reliability
- Reversible: disconnect 3 wires to restore original state

**ESP32 protection and level isolation:**

⚠️ ESP32-C3 GPIOs are **NOT 5V-tolerant** (max 3.6V, Espressif datasheet).
The GPIO must NEVER be directly connected to a line that can reach 5V, even in
open_drain mode (open_drain prevents sourcing, but does not prevent receiving 5V
through internal ESD diodes → chip damage).

**Recommended circuit: BC337 as open-collector level-shifting output.**

```
ESP32 GPIO ──[470Ω]──┬── Base BC337
                      │
                    [10kΩ] ← pull-down (OFF at boot)
                      │
GND ─────────────────┴── Emitter BC337

Signal line to AC MCU ── Collector BC337
```

The BC337 acts as an external open-collector output:
- GPIO HIGH → BC337 conducts → line pulled LOW (mark)
- GPIO LOW → BC337 off → line floats, pulled HIGH by existing circuit
- No voltage from the AC signal line ever reaches the ESP32 GPIO
- Works regardless of whether TSOP VCC is 3.3V or 5V

**Remote coexistence:** depends on TSOP output type.
- TSOP open-collector: no modification needed. Both sink on the same line.
- TSOP push-pull: contention possible. Cut the TSOP→MCU trace and recombine
  via wired-OR (two diodes + pull-up). Exact topology depends on PCB — decide
  after measurements (see validation plan, phases 13-14).

**Wiring steps:**
1. Verify electrical isolation of the AC logic board (see plan, phase 12)
2. Open the indoor unit cover (screws hidden under grilles or covers)
3. Locate the IR receiver module (small black 3-pin component)
4. Identify the 3 pins: VCC, GND, Signal (from identified component's datasheet)
5. Measure VCC voltage (3.3V or 5V)
6. Characterize Signal output with logic analyzer (idle level, amplitude, OC/PP type)
7. Connect BC337 Collector to the Signal line
8. Connect GNDs together
9. **Do not power the TSOP from the ESP32** — leave it powered by the AC board

**Firmware change:**

Only the `remote_transmitter` config changes — `technibel_ir.h` stays untouched:

```yaml
remote_transmitter:
  pin:
    number: GPIO3
    inverted: false       # BC337 adds a logic inversion:
                          # GPIO HIGH → transistor ON → line LOW (mark)
                          # determine experimentally — try false then true
  carrier_duty_percent: 100   # DC signal, no 38kHz carrier
  non_blocking: false
  rmt_symbols: 96
```

`carrier_duty_percent: 100` is an official ESPHome feature, documented for 433MHz RF transmitters —
same principle: raw timings on a GPIO with no carrier modulation.

**Watch out for:**
- Cut power to the AC unit at the breaker before any intervention
- Do not touch capacitors or high-voltage circuits
- **Do NOT assume the indoor unit's logic is isolated from mains** — some appliance PSUs
  reference logic ground to mains. Verify isolation before connecting any USB instrument
  (logic analyzer, oscilloscope) — see validation plan phase 12
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
