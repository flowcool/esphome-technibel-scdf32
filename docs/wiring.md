# Wiring / Câblage

**[🇬🇧 English](#-english)** · **[🇫🇷 Français](#-français)**

---

## 🇬🇧 English

### Transmitter wiring (final build)

```
ESP32                  Diymore PCB0100 (IR TX)
─────                  ──────────────────────
5V / Vin  ────────────► VCC
GND       ────────────► GND
GPIO4     ────────────► IN1

         100µF capacitor
         + leg on 5V, − leg on GND
         Place as close as possible to the TX module.
```

> **Note:** Use IN1 on the Diymore PCB0100 for channel 1. IN2 is available for a
> second emitter if needed (e.g. pointing in a different direction).

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

Both modules can coexist on the same ESP32 during the capture phase:

```
ESP32 GPIO4  ──► Diymore PCB0100 IN1    (TX)
ESP32 GPIO23 ◄── KY-022 OUT             (RX)
ESP32 5V     ──► Diymore PCB0100 VCC
ESP32 3V3    ──► KY-022 VCC
ESP32 GND    ──► Diymore GND + KY-022 GND (common ground)
```

### Final installation tips

- Mount the ESP32 + Diymore module close to the AC indoor unit.
- Point the IR LED toward the AC receiver window (usually on the front panel).
- Power via USB (5V / 500mA minimum) or a 5V wall adapter.
- The IR signal is directional — test range and angle before finalizing placement.

---

## 🇫🇷 Français

### Câblage émetteur (montage final)

```
ESP32                  Diymore PCB0100 (IR TX)
─────                  ──────────────────────
5V / Vin  ────────────► VCC
GND       ────────────► GND
GPIO4     ────────────► IN1

         Condensateur 100µF
         + sur 5V, − sur GND
         Placer le plus près possible du module TX.
```

> **Note :** Utiliser IN1 sur le Diymore PCB0100 pour le canal 1. IN2 est disponible
> pour un second émetteur si nécessaire (ex : orienter dans une autre direction).

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

Les deux modules peuvent coexister sur le même ESP32 pendant la phase de capture :

```
ESP32 GPIO4  ──► Diymore PCB0100 IN1    (TX)
ESP32 GPIO23 ◄── KY-022 OUT             (RX)
ESP32 5V     ──► Diymore PCB0100 VCC
ESP32 3V3    ──► KY-022 VCC
ESP32 GND    ──► Diymore GND + KY-022 GND (masse commune)
```

### Conseils d'installation finale

- Monter l'ESP32 + module Diymore à proximité de l'unité intérieure du climatiseur.
- Orienter la LED IR vers la fenêtre de réception de la clim (généralement sur le panneau avant).
- Alimenter via USB (5V / 500mA minimum) ou une alimentation murale 5V.
- Le signal IR est directionnel — tester la portée et l'angle avant de fixer définitivement.
