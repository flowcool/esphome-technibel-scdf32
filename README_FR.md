# ESPHome — Climatiseur Technibel SCDF32C5I

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![ESPHome](https://img.shields.io/badge/ESPHome-2026.x-blue)](https://esphome.io)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-compatible-41BDF5)](https://www.home-assistant.io)
[![Technibel](https://img.shields.io/badge/Technibel-SCDF32C5I-red)]()

> Protocole IR entièrement décodé par reverse engineering.
> C'est probablement la première documentation publique de ce protocole.

→ **[English version / Version anglaise : README.md](README.md)**

---

## Description

Ce dépôt contient tout le nécessaire pour piloter un climatiseur **Technibel SCDF32C5I**
depuis Home Assistant via un ESP32 émetteur IR.

Le protocole IR a été entièrement décodé — Technibel utilise un protocole propriétaire
48 bits non reconnu par IRremoteESP8266. La structure des trames, l'encodage et la
formule de checksum (qui intègre la température ambiante) sont documentés dans
[`docs/protocol.md`](docs/protocol.md).

## Contenu du dépôt

| Fichier | Description |
|---|---|
| `esphome/libraries/technibel_ir.h` | Constructeur de trames IR en C++ |
| `esphome/ir-technibel-clim.yaml` | Config ESPHome émetteur IR |
| `esphome/ir-clim-sniffer.yaml` | Config ESPHome récepteur (phase capture) |
| `homeassistant/climate-technibel-ha.yaml` | Package Home Assistant complet |
| `docs/protocol.md` | Documentation complète du protocole |
| `docs/bom.md` | Liste de matériel |
| `docs/wiring.md` | Schéma de câblage |

## Matériel requis

- ESP32 DevKit (30 ou 38 broches)
- Module émetteur IR Diymore PCB0100 (transistor + résistances intégrés)
- Condensateur 100µF 16V (filtrage alimentation)
- Câbles Dupont

Pour la phase de capture uniquement : récepteur IR KY-022 / VS1838B 38kHz.

## Installation rapide

1. Copier `esphome/libraries/technibel_ir.h` dans `config/libraries/` de votre ESPHome.
2. Flasher `esphome/ir-technibel-clim.yaml` sur l'ESP32.
3. Renseigner `wifi_ssid`, `wifi_password`, `ota_password` dans `secrets.yaml`.
4. Copier `homeassistant/climate-technibel-ha.yaml` dans le dossier `packages/` de HA.
5. **Remplacer** `sensor.YOUR_TEMPERATURE_SENSOR` par votre capteur de température.
6. Redémarrer Home Assistant → l'entité `climate.clim_sejour` apparaît.

## Protocole — résumé

Trame 6 octets : `D0 B1 B2 B3 03 B5`

- **B1** : température ambiante encodée (nibble haut) + mode (nibble bas : COOL=`0xC`, DRY=`0xA`, FAN=`0x9`, AUTO=`0xD`)
- **B2** : température encodée (nibble hi) + vitesse ventilo (nibble lo)
- **B3** : `0x18` allumé / `0x08` éteint
- **B4** : `0x03` fixe
- **B5** : checksum incluant la température ambiante

Trame OFF exemple : `D0 AC A8 08 03 A4` (consigne 25°C, ambiance 25°C)

→ Documentation complète : [`docs/protocol.md`](docs/protocol.md)

## Licence

MIT — voir [LICENSE](LICENSE).
