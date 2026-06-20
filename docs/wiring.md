# Wiring / Câblage

**[🇬🇧 English](#-english)** · **[🇫🇷 Français](#-français)**

---

## 🇬🇧 English

### Transmitter wiring (final build)

```
ESP32                  Discrete IR circuit
─────                  ──────────────────
5V / Vin  ──[47Ω]────► Anode (+, long leg)  TSAL6400
                        Cathode (−, short leg) ──► Collector (right pin)  ┐
                                                    2N2222 NPN              │
GPIO4     ──[470Ω]───► Base (middle pin)     ──────────────────────────────┤
                        Emitter (left pin)   ──────────────────────────────┘
GND       ◄────────────────────────────────────────────────────────────────┘
```

**2N2222 TO-92 pinout** (flat face toward you, pins pointing down):
```
Left = Emitter (E) · Middle = Base (B) · Right = Collector (C)
```

> **Note:** Solder or use a small breadboard for reliable connections — Dupont wires
> on bare component leads are fragile in long-term installation.

### Sniffer wiring (capture phase only)

```
ESP32                  KY-022 / VS1838B (IR RX)
─────                  ────────────────────────
3V3       ────────────► VCC (S pin on KY-022 carrier board)
GND       ────────────► GND
GPIO23    ◄──────────── OUT (signal pin)
```

> **Note:** The KY-022 signal output is active-low. The ESPHome config uses
> `inverted: true` on the pin to compensate.

### Combined wiring (sniffer + transmitter on same ESP32)

Both circuits can coexist on the same ESP32 during the capture phase:

```
ESP32 GPIO4  ──[470Ω]──► Base 2N2222 / [47Ω] ──► TSAL6400    (TX)
ESP32 GPIO23 ◄────────── KY-022 OUT                            (RX)
ESP32 5V     ──────────► TSAL6400 via 47Ω resistor
ESP32 3V3    ──────────► KY-022 VCC
ESP32 GND    ──────────► 2N2222 Emitter + KY-022 GND (common ground)
```

### Optional: multiple LEDs for wider coverage angle

The TSAL6400 has a narrow ±17° emission angle. Adding 2–3 LEDs in parallel, each
pointed at a slightly different angle, widens the coverage cone without changing the
ESP32 wiring or firmware.

```
                    ┌──[47Ω]──► LED1 anode (+) → cathode ──┐
5V ─────────────────┤                                        ├──► Collector (2N2222)
                    └──[47Ω]──► LED2 anode (+) → cathode ──┘
GPIO4 ──[470Ω]──► Base
GND  ◄─────────── Emitter
```

> Each LED must have its own series resistor (47Ω each) to balance current.
> Do not share a single resistor across parallel LEDs.
> With 2× TSAL6400: ~70mA peak per LED, well within 2N2222 limits (600mA total).

### Final installation tips

- Mount the ESP32 + Diymore module close to the AC indoor unit.
- Point the IR LED toward the AC receiver window (usually on the front panel).
- Power via USB (5V / 500mA minimum) or a 5V wall adapter.
- The IR signal is directional — test range and angle before finalizing placement.

---

## 🇫🇷 Français

### Câblage émetteur (montage final)

```
ESP32                  Circuit IR discret
─────                  ──────────────────
5V / Vin  ──[47Ω]────► Anode (+, longue patte)  TSAL6400
                        Cathode (−, courte patte) ──► Collector (patte droite)  ┐
                                                       2N2222 NPN                │
GPIO4     ──[470Ω]───► Base (patte milieu)       ──────────────────────────────┤
                        Emitter (patte gauche)    ──────────────────────────────┘
GND       ◄─────────────────────────────────────────────────────────────────────┘
```

**Brochage 2N2222 TO-92** (face plate vers toi, pattes vers le bas) :
```
Gauche = Emitter (E) · Milieu = Base (B) · Droite = Collector (C)
```

> **Note :** Souder ou utiliser une mini breadboard pour un montage fiable — les fils
> Dupont sur les pattes nues des composants sont fragiles pour une installation permanente.

### Câblage sniffer (phase de capture uniquement)

```
ESP32                  KY-022 / VS1838B (IR RX)
─────                  ────────────────────────
3V3       ────────────► VCC (broche S sur le module KY-022)
GND       ────────────► GND
GPIO23    ◄──────────── OUT (broche signal)
```

> **Note :** La sortie signal du KY-022 est active bas. La config ESPHome utilise
> `inverted: true` sur la broche pour compenser.

### Câblage combiné (sniffer + émetteur sur le même ESP32)

Les deux circuits peuvent coexister sur le même ESP32 pendant la phase de capture :

```
ESP32 GPIO4  ──[470Ω]──► Base 2N2222 / [47Ω] ──► TSAL6400    (TX)
ESP32 GPIO23 ◄────────── KY-022 OUT                            (RX)
ESP32 5V     ──────────► TSAL6400 via résistance 47Ω
ESP32 3V3    ──────────► KY-022 VCC
ESP32 GND    ──────────► Emitter 2N2222 + KY-022 GND (masse commune)
```

### Optionnel : plusieurs LEDs pour élargir l'angle de couverture

La TSAL6400 a un angle d'émission étroit de ±17°. Ajouter 2–3 LEDs en parallèle,
chacune orientée légèrement différemment, élargit le cône sans modifier le firmware
ni le câblage ESP32.

```
                    ┌──[47Ω]──► LED1 anode (+) → cathode ──┐
5V ─────────────────┤                                        ├──► Collector (2N2222)
                    └──[47Ω]──► LED2 anode (+) → cathode ──┘
GPIO4 ──[470Ω]──► Base
GND  ◄─────────── Emitter
```

> Chaque LED doit avoir sa propre résistance série (47Ω chacune) pour équilibrer le courant.
> Ne pas partager une seule résistance entre plusieurs LEDs en parallèle.
> Avec 2× TSAL6400 : ~70mA crête par LED, largement dans les limites du 2N2222 (600mA total).

### Conseils d'installation finale

- Monter l'ESP32 + module Diymore à proximité de l'unité intérieure du climatiseur.
- Orienter la LED IR vers la fenêtre de réception de la clim (généralement sur le panneau avant).
- Alimenter via USB (5V / 500mA minimum) ou une alimentation murale 5V.
- Le signal IR est directionnel — tester la portée et l'angle avant de fixer définitivement.
