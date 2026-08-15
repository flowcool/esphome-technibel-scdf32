[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![ESPHome](https://img.shields.io/badge/ESPHome-2026.x-blue)](https://esphome.io)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-compatible-41BDF5)](https://www.home-assistant.io)
[![Technibel](https://img.shields.io/badge/Technibel-SCDF32C5I-red)]()

**[🇬🇧 English](#-english)** · **[🇫🇷 Français](#-français)**

---

# ESPHome — Technibel SCDF32C5I IR Climate

> Fully reverse-engineered IR protocol + complete ESPHome / Home Assistant integration.  
> Protocole IR entièrement décodé + intégration ESPHome / Home Assistant complète.

---

## 🇬🇧 English

### What this is

This repository provides everything needed to control a **Technibel SCDF32C5I**
split air conditioner from Home Assistant using an ESP32 as an IR blaster.

The IR protocol was fully reverse-engineered from raw captures — Technibel uses a
**proprietary 48-bit protocol** that is not recognized by IRremoteESP8266. The frame
structure, encoding, and checksum formula are documented in [`docs/protocol.md`](docs/protocol.md).

**What you get:**
- `technibel_ir.h` — C++ IR frame builder (48-bit, checksum included)
- `ir-technibel-clim.yaml` — ESPHome transmitter config exposing a `send_command` service
- `ir-clim-sniffer.yaml` — ESPHome receiver config for capturing raw IR frames (debug use)
- `climate-technibel-ha.yaml` — Home Assistant MQTT climate entity (full package)

### Hardware (BOM)

See [`docs/bom.md`](docs/bom.md) for the full bill of materials.

| Component | Reference | Notes |
|---|---|---|
| MCU | ESP32 DevKit 30-pin | Any ESP32 board works |
| IR emitter | Diymore PCB0100 (2-channel) | Transistor + resistors built-in |
| IR receiver | KY-022 / VS1838B 38kHz | Sniffer phase only, not needed in final build |
| Capacitor | 100µF 16V electrolytic | Power filtering near TX module |

### Wiring

See [`docs/wiring.md`](docs/wiring.md) for the full ASCII diagram.

```
ESP32 GPIO4  ──► Diymore PCB0100 IN1   (IR transmitter)
ESP32 GPIO23 ◄── KY-022 OUT            (IR receiver — sniffer only)
```

### Installation

1. Copy `esphome/libraries/technibel_ir.h` to your ESPHome `config/libraries/` directory.
2. Flash `esphome/ir-technibel-clim.yaml` to your ESP32.
3. Add your `wifi_ssid`, `wifi_password`, and `ota_password` to your `secrets.yaml`.
4. In Home Assistant, add `homeassistant/climate-technibel-ha.yaml` to your packages directory.
5. Restart Home Assistant. The `climate.clim_sejour` entity will appear.

> **Note:** Adjust `sensor.thermometre_espace_de_vie_temperature` in `climate-technibel-ha.yaml`
> to match your own ambient temperature sensor entity ID.

### Usage in Home Assistant

Once installed, `climate.clim_sejour` supports:

| Feature | Values |
|---|---|
| HVAC modes | `off`, `cool`, `dry`, `fan_only`, `auto` |
| Fan modes | `auto`, `low`, `med`, `high` |
| Temperature range | 16°C – 30°C (1°C step) |
| Current temperature | From your HA temperature sensor |

Every state change (mode, temperature, fan speed) automatically sends the full IR
command to the AC via the ESP32.

### Protocol overview

The Technibel SCDF32C5I uses a proprietary 48-bit IR protocol at 38kHz.
Frame: `B0 B1 B2 B3 B4 B5` (6 bytes). Checksum includes ambient temperature.

→ Full details in [`docs/protocol.md`](docs/protocol.md)

---

## 🇫🇷 Français

### Description

Ce dépôt contient tout le nécessaire pour piloter un climatiseur **Technibel SCDF32C5I**
depuis Home Assistant via un ESP32 émetteur IR.

Le protocole IR a été entièrement décodé par reverse engineering — Technibel utilise un
**protocole propriétaire 48 bits** non reconnu par IRremoteESP8266. C'est probablement
la première documentation publique de ce protocole.

**Contenu :**
- `technibel_ir.h` — constructeur de trames IR en C++ (48 bits, checksum inclus)
- `ir-technibel-clim.yaml` — config ESPHome émetteur, expose un service `send_command`
- `ir-clim-sniffer.yaml` — config ESPHome récepteur pour capture de trames brutes (debug)
- `climate-technibel-ha.yaml` — entité climate MQTT pour Home Assistant (package complet)

### Matériel (BOM)

Voir [`docs/bom.md`](docs/bom.md) pour la liste complète.

| Composant | Référence | Notes |
|---|---|---|
| MCU | ESP32 DevKit 30 broches | N'importe quel ESP32 fonctionne |
| Émetteur IR | Diymore PCB0100 (2 canaux) | Transistor + résistances intégrés |
| Récepteur IR | KY-022 / VS1838B 38kHz | Phase sniffer uniquement, inutile en prod |
| Condensateur | 100µF 16V électrolytique | Filtrage alim près du module TX |

### Câblage

Voir [`docs/wiring.md`](docs/wiring.md) pour le schéma ASCII complet.

```
ESP32 GPIO4  ──► Diymore PCB0100 IN1   (émetteur IR)
ESP32 GPIO23 ◄── KY-022 OUT            (récepteur IR — sniffer uniquement)
```

### Installation

1. Copier `esphome/libraries/technibel_ir.h` dans le dossier `config/libraries/` de votre ESPHome.
2. Flasher `esphome/ir-technibel-clim.yaml` sur votre ESP32.
3. Ajouter vos `wifi_ssid`, `wifi_password` et `ota_password` dans `secrets.yaml`.
4. Dans Home Assistant, ajouter `homeassistant/climate-technibel-ha.yaml` dans votre dossier `packages/`.
5. Redémarrer Home Assistant. L'entité `climate.clim_sejour` apparaît.

> **Note :** Remplacer `sensor.thermometre_espace_de_vie_temperature` dans `climate-technibel-ha.yaml`
> par l'entity_id de votre propre capteur de température ambiante.

### Utilisation dans Home Assistant

L'entité `climate.clim_sejour` une fois installée supporte :

| Fonction | Valeurs |
|---|---|
| Modes HVAC | `off`, `cool`, `dry`, `fan_only`, `auto` |
| Vitesses ventilateur | `auto`, `low`, `med`, `high` |
| Plage température | 16°C – 30°C (pas 1°C) |
| Température courante | Depuis votre capteur HA |

### Aperçu du protocole

Le Technibel SCDF32C5I utilise un protocole IR propriétaire 48 bits à 38kHz.
Trame : `B0 B1 B2 B3 B4 B5` (6 octets). Le checksum intègre la température ambiante.

→ Documentation complète dans [`docs/protocol.md`](docs/protocol.md)

---

## Protocol summary / Résumé protocole

| Byte | Value | Description |
|---|---|---|
| B0 | `0xD0` | Device address (fixed / fixe) |
| B1 | ambient+mode | High nibble = ambient temperature, low nibble: COOL=`0xC`, DRY=`0xA`, FAN=`0x9`, AUTO=`0xD` |
| B2 | temp+fan | hi nibble = temp encoded, lo nibble = fan speed |
| B3 | `0x18`/`0x08` | Power ON / OFF |
| B4 | `0x03` | Fixed / Fixe |
| B5 | checksum | Includes ambient temperature / Intègre T° ambiante |

→ [`docs/protocol.md`](docs/protocol.md) for full encoding tables and checksum formula.
