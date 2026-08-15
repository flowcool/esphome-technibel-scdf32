# Technibel SCDF32C5I — IR Protocol Documentation

**[🇬🇧 English](#-english)** · **[🇫🇷 Français](#-français)**

---

## 🇬🇧 English

### Overview

The Technibel SCDF32C5I uses a **proprietary 48-bit IR protocol** at 38kHz carrier frequency.
It is **not recognized** by IRremoteESP8266 (reported as UNKNOWN). Frames are static and
replayable — no rolling code.

| Parameter | Value |
|---|---|
| Carrier frequency | 38kHz |
| Frame length | 48 bits (6 bytes) |
| Header pulse | 6500µs |
| Header space | 3300µs |
| Bit pulse | ~450µs |
| Bit 1 space | ~2200µs |
| Bit 0 space | ~900µs |
| Bit order | MSB first per byte |

### Frame Structure

```
[ HEADER ] [ B0 ] [ B1 ] [ B2 ] [ B3 ] [ B4 ] [ B5 ] [ final pulse ]
```

| Byte | Example | Description |
|---|---|---|
| B0 | `0xD0` | Device address — always fixed |
| B1 | `0xAC` | Ambient temperature high nibble + operating mode nibble |
| B2 | `0x28` | Temperature (hi nibble) + fan speed (lo nibble) |
| B3 | `0x18` | Power ON flag (`0x08` = OFF) |
| B4 | `0x03` | Fixed — always `0x03` |
| B5 | checksum | Computed from B1, B2, and B3 |

### Mode encoding (B1 low nibble)

| Mode | Low nibble |
|---|---|
| COOL | `0xC` |
| DRY | `0xA` |
| FAN only | `0x9` |
| AUTO | `0xD` |

The high nibble of B1 carries the ambient temperature using the same encoding
as B2: `(reverseBits8(T_ambient - 4) >> 4) & 0xF`. For example, ambient 25°C
with COOL gives `B1=0xAC`, ambient 26°C gives `B1=0x6C`, and ambient 27°C
gives `B1=0xEC`.

> OFF is not a mode value — it is encoded in B3 (see Power flag below).

### Temperature encoding (B2 hi nibble)

Formula: `temp_hi = (reverseBits8(consigne - 4) >> 4) & 0xF`

| Temp | B2 hi nibble (hex) | Verified |
|---|---|---|
| 16°C | `0x90` | generated |
| 17°C | `0x10` | generated |
| 18°C | `0x70` | ✅ captured |
| 19°C | `0xF0` | ✅ captured |
| 20°C | `0x08` | ✅ captured |
| 21°C | `0x88` | generated* |
| 22°C | `0x48` | ✅ captured |
| 23°C | `0xC8` | ✅ captured |
| 24°C | `0x28` | ✅ captured |
| 25°C | `0xA8` | ✅ captured |
| 26°C | `0x68` | ✅ captured |
| 27°C | `0xE8` | generated |
| 28°C | `0x18` | generated |
| 29°C | `0x98` | generated |
| 30°C | `0x58` | generated |

*21°C capture was corrupted (AC displayed 24°C at capture time) — value generated from formula.

### Fan speed encoding (B2 lo nibble)

| Remote level | lo nibble | Captured frame (FAN, 23°C, ambient 24°C) |
|---|---|---|
| AUTO | `0x8` | `D0 29 C8 18 03 51` |
| FAN 1 / LOW | `0xC` | `D0 29 CC 18 03 55` |
| FAN 2 | `0xA` | `D0 29 CA 18 03 53` |
| FAN 3 / MED | `0xE` | `D0 29 CE 18 03 57` |
| FAN 4 | `0x9` | `D0 29 C9 18 03 50` |
| FAN 5 | `0xD` | `D0 29 CD 18 03 54` |
| FAN 6 / HIGH | `0xB` | `D0 29 CB 18 03 52` |

All seven values were captured in one controlled campaign on 2026-08-15. The
complete raw timings are preserved in `captures/fan-campaign-2026-08-15.jsonl`.

### B2 full formula

```
B2 = (temp_hi_nibble << 4) | fan_lo_nibble
```

Example: COOL, 24°C, AUTO fan → `B2 = (0x2 << 4) | 0x8 = 0x28`

### Power / change flag (B3)

| Value | Meaning |
|---|---|
| `0x18` | Power ON (or command update while running) |
| `0x08` | Power OFF |

> Always use `0x18` when sending a command from Home Assistant, even just to change
> the setpoint — the AC needs this flag to apply the new value.

### Checksum (B5)

```
B5 = reverseBits8(
       (reverseBits8(B1) + reverseBits8(B2) + reverseBits8(B3) + 0xCB) & 0xFF
     )
```

The ambient temperature is included indirectly through the high nibble of B1,
and the operating mode through its low nibble. The former formula using
`T_ambient - 25` was a COOL-only reduction: for COOL, B1's low nibble is fixed
to `0xC`, so `reverseBits8(B1) + 0xCB` reduces to `T_ambient - 25` modulo 256.
It must not be used for DRY, FAN, or AUTO frames.

### OFF frame (fixed)

```
D0 AC A8 08 03 A4
```

This frame was pre-computed with B3=`0x08` (power off) and ambient=25°C.
It reliably turns off the AC regardless of the previous mode or setpoint.

### Reverse engineering notes

- Captured using ESP32 + KY-022 TSOP IR receiver + ESPHome `remote_receiver` (`dump: all`)
- Decoded from Pronto hex format dumped in ESPHome logs
- Protocol confirmed **NOT rolling-code** — static frames, fully replayable
- IRremoteESP8266 does not recognize this protocol (reported as UNKNOWN)
- The `reverseBits8` function is central to both temperature encoding and checksum

---

## 🇫🇷 Français

### Vue d'ensemble

Le Technibel SCDF32C5I utilise un **protocole IR propriétaire 48 bits** à 38kHz.
Il n'est **pas reconnu** par IRremoteESP8266 (renvoyé comme UNKNOWN). Les trames sont
statiques et rejouables — pas de code tournant.

| Paramètre | Valeur |
|---|---|
| Fréquence porteuse | 38kHz |
| Longueur de trame | 48 bits (6 octets) |
| Header pulse | 6500µs |
| Header space | 3300µs |
| Pulse par bit | ~450µs |
| Space bit 1 | ~2200µs |
| Space bit 0 | ~900µs |
| Ordre des bits | MSB en premier par octet |

### Structure de trame

```
[ HEADER ] [ B0 ] [ B1 ] [ B2 ] [ B3 ] [ B4 ] [ B5 ] [ pulse final ]
```

| Octet | Exemple | Description |
|---|---|---|
| B0 | `0xD0` | Adresse device — toujours fixe |
| B1 | `0xAC` | Nibble haut température ambiante + nibble bas mode |
| B2 | `0x28` | Température (nibble hi) + vitesse ventilo (nibble lo) |
| B3 | `0x18` | Flag marche (`0x08` = arrêt) |
| B4 | `0x03` | Fixe — toujours `0x03` |
| B5 | checksum | Calculé depuis B1, B2 et B3 |

### Encodage des modes (nibble bas de B1)

| Mode | Nibble bas |
|---|---|
| COOL | `0xC` |
| DRY (déshumidification) | `0xA` |
| FAN only (ventilation) | `0x9` |
| AUTO | `0xD` |

Le nibble haut de B1 encode la température ambiante avec la même formule que
B2 : `(inverseBits8(T_ambiant - 4) >> 4) & 0xF`. Ainsi, à 25°C en COOL,
`B1=0xAC`, à 26°C `B1=0x6C`, et à 27°C `B1=0xEC`.

> OFF n'est pas une valeur de mode — il est encodé dans B3 (voir Flag d'alimentation).

### Encodage température (nibble hi de B2)

Formule : `temp_hi = (inverseBits8(consigne - 4) >> 4) & 0xF`

Voir tableau complet en section anglaise — valeurs identiques.

### Encodage vitesse ventilateur (nibble lo de B2)

| Niveau télécommande | nibble lo | Trame capturée (FAN, 23°C, ambiante 24°C) |
|---|---|---|
| AUTO | `0x8` | `D0 29 C8 18 03 51` |
| FAN 1 / LOW | `0xC` | `D0 29 CC 18 03 55` |
| FAN 2 | `0xA` | `D0 29 CA 18 03 53` |
| FAN 3 / MED | `0xE` | `D0 29 CE 18 03 57` |
| FAN 4 | `0x9` | `D0 29 C9 18 03 50` |
| FAN 5 | `0xD` | `D0 29 CD 18 03 54` |
| FAN 6 / HIGH | `0xB` | `D0 29 CB 18 03 52` |

Les sept valeurs ont été capturées pendant une campagne contrôlée le 2026-08-15.
Les timings bruts complets sont conservés dans
`captures/fan-campaign-2026-08-15.jsonl`.

### Formule complète de B2

```
B2 = (nibble_hi_temp << 4) | nibble_lo_ventilo
```

### Flag alimentation (B3)

| Valeur | Signification |
|---|---|
| `0x18` | Allumage (ou mise à jour de consigne) |
| `0x08` | Extinction |

> Toujours utiliser `0x18` depuis Home Assistant, même pour changer uniquement
> la consigne — le climatiseur nécessite ce flag pour appliquer la nouvelle valeur.

### Checksum (B5)

```
B5 = inverseBits8(
       (inverseBits8(B1) + inverseBits8(B2) + inverseBits8(B3) + 0xCB) & 0xFF
     )
```

La température ambiante est incluse indirectement par le nibble haut de B1, et
le mode par son nibble bas. L'ancienne formule utilisant `T_ambiant - 25` était
une réduction valable uniquement en mode COOL : le nibble bas de B1 y vaut
toujours `0xC`, donc `inverseBits8(B1) + 0xCB` se réduit à `T_ambiant - 25`
modulo 256. Elle ne doit pas être utilisée pour les modes DRY, FAN ou AUTO.

### Trame OFF (fixe)

```
D0 AC A8 08 03 A4
```

Pré-calculée avec B3=`0x08` (extinction) et ambiant=25°C. Éteint le climatiseur
de manière fiable quel que soit le mode ou la consigne précédents.

### Notes de reverse engineering

- Capture réalisée avec ESP32 + récepteur KY-022 TSOP + ESPHome `remote_receiver` (`dump: all`)
- Décodage depuis le format Pronto hex dans les logs ESPHome
- Protocole confirmé **sans code tournant** — trames statiques, rejouables
- IRremoteESP8266 ne reconnaît pas ce protocole (rapporté comme UNKNOWN)
- La fonction `inverseBits8` est centrale dans l'encodage température et le checksum
