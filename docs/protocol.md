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
| B1 | `0xAC` | Operating mode |
| B2 | `0x28` | Temperature (hi nibble) + fan speed (lo nibble) |
| B3 | `0xF8` | Power on/off flag |
| B4 | `0x43` | Fixed — always `0x43` |
| B5 | checksum | Computed from B2, B3, ambient temperature |

### Mode encoding (B1)

| Mode | B1 value |
|---|---|
| COOL | `0xAC` |
| DRY | `0xAA` |
| FAN only | `0xA9` |
| AUTO | `0xAD` |

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

| Fan speed | lo nibble |
|---|---|
| AUTO | `0x8` |
| LOW | `0xC` |
| MED | `0xE` |
| HIGH | `0xB` |

### B2 full formula

```
B2 = (temp_hi_nibble << 4) | fan_lo_nibble
```

Example: COOL, 24°C, AUTO fan → `B2 = (0x2 << 4) | 0x8 = 0x28`

### Power / change flag (B3)

| Value | Meaning |
|---|---|
| `0xF8` | Power ON (or command update while running) |
| `0x08` | Power OFF |

> Always use `0xF8` when sending a command from Home Assistant, even just to change
> the setpoint — the AC needs this flag to apply the new value.

### Checksum (B5)

```
B5 = reverseBits8(
       (reverseBits8(B2) + reverseBits8(B3) + T_ambient - 23) & 0xFF
     )
```

⚠️ The checksum includes the **ambient temperature** as read by the remote control.
Use a Home Assistant temperature sensor for best accuracy. A fixed value of `25`
works reliably for setpoints in the 18–26°C range.

### OFF frame (fixed)

```
D0 AC 28 08 43 64
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
| B1 | `0xAC` | Mode de fonctionnement |
| B2 | `0x28` | Température (nibble hi) + vitesse ventilo (nibble lo) |
| B3 | `0xF8` | Flag allumage/extinction |
| B4 | `0x43` | Fixe — toujours `0x43` |
| B5 | checksum | Calculé depuis B2, B3, température ambiante |

### Encodage des modes (B1)

| Mode | Valeur B1 |
|---|---|
| COOL | `0xAC` |
| DRY (déshumidification) | `0xAA` |
| FAN only (ventilation) | `0xA9` |
| AUTO | `0xAD` |

> OFF n'est pas une valeur de mode — il est encodé dans B3 (voir Flag d'alimentation).

### Encodage température (nibble hi de B2)

Formule : `temp_hi = (inverseBits8(consigne - 4) >> 4) & 0xF`

Voir tableau complet en section anglaise — valeurs identiques.

### Encodage vitesse ventilateur (nibble lo de B2)

| Vitesse | nibble lo |
|---|---|
| AUTO | `0x8` |
| LOW (faible) | `0xC` |
| MED (moyen) | `0xE` |
| HIGH (fort) | `0xB` |

### Formule complète de B2

```
B2 = (nibble_hi_temp << 4) | nibble_lo_ventilo
```

### Flag alimentation (B3)

| Valeur | Signification |
|---|---|
| `0xF8` | Allumage (ou mise à jour de consigne) |
| `0x08` | Extinction |

> Toujours utiliser `0xF8` depuis Home Assistant, même pour changer uniquement
> la consigne — le climatiseur nécessite ce flag pour appliquer la nouvelle valeur.

### Checksum (B5)

```
B5 = inverseBits8(
       (inverseBits8(B2) + inverseBits8(B3) + T_ambiant - 23) & 0xFF
     )
```

⚠️ Le checksum intègre la **température ambiante** lue par la télécommande.
Utiliser un capteur de température Home Assistant pour une meilleure précision.
Une valeur fixe de `25` fonctionne de manière fiable pour les consignes entre 18 et 26°C.

### Trame OFF (fixe)

```
D0 AC 28 08 43 64
```

Pré-calculée avec B3=`0x08` (extinction) et ambiant=25°C. Éteint le climatiseur
de manière fiable quel que soit le mode ou la consigne précédents.

### Notes de reverse engineering

- Capture réalisée avec ESP32 + récepteur KY-022 TSOP + ESPHome `remote_receiver` (`dump: all`)
- Décodage depuis le format Pronto hex dans les logs ESPHome
- Protocole confirmé **sans code tournant** — trames statiques, rejouables
- IRremoteESP8266 ne reconnaît pas ce protocole (rapporté comme UNKNOWN)
- La fonction `inverseBits8` est centrale dans l'encodage température et le checksum
