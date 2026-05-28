# Bill of Materials / Liste de matériel

**[🇬🇧 English](#-english)** · **[🇫🇷 Français](#-français)**

---

## 🇬🇧 English

### Transmitter (final build)

| Component | Reference | Role | Notes |
|---|---|---|---|
| MCU | ESP32 DevKit 30-pin | Main controller | Any ESP32 board works |
| IR emitter | Diymore PCB0100 (2-channel) | Send IR to AC | Transistor + resistors built-in, no extra components needed |
| Capacitor | 100µF 16V electrolytic | Power filtering | Place close to TX module on 5V/GND |
| Cables | Dupont M/M + M/F | Wiring | 3 wires: 5V, GND, GPIO4 |
| Enclosure | Any | Optional | Protects the ESP32 |

### Sniffer (capture phase only — not needed in final build)

| Component | Reference | Role | Notes |
|---|---|---|---|
| IR receiver | KY-022 / VS1838B (38kHz) | Capture raw IR frames | Frequency must be 38kHz |
| Cables | Dupont M/F | Wiring | 3 wires: 3V3, GND, GPIO23 |

> The sniffer is used only during the reverse engineering phase to capture frames
> from the original Technibel remote control. It is not needed in the final installation.

### Sourcing tips

- **Diymore PCB0100**: available on AliExpress and Amazon. Search "Diymore IR transmitter PCB0100".
  Make sure to get the **2-channel version** — it has built-in transistor and resistors for 5V operation.
- **KY-022**: standard Arduino sensor kit component, available everywhere.
- **ESP32 DevKit**: any 30-pin or 38-pin ESP32 board works.

---

## 🇫🇷 Français

### Émetteur (montage final)

| Composant | Référence | Rôle | Notes |
|---|---|---|---|
| MCU | ESP32 DevKit 30 broches | Contrôleur principal | Tout ESP32 fonctionne |
| Émetteur IR | Diymore PCB0100 (2 canaux) | Envoyer IR vers clim | Transistor + résistances intégrés, aucun composant supplémentaire |
| Condensateur | 100µF 16V électrolytique | Filtrage alimentation | Placer près du module TX sur 5V/GND |
| Câbles | Dupont M/M + M/F | Câblage | 3 fils : 5V, GND, GPIO4 |
| Boîtier | Au choix | Optionnel | Protège l'ESP32 |

### Sniffer (phase de capture uniquement — inutile dans le montage final)

| Composant | Référence | Rôle | Notes |
|---|---|---|---|
| Récepteur IR | KY-022 / VS1838B (38kHz) | Capturer trames IR brutes | Fréquence obligatoirement 38kHz |
| Câbles | Dupont M/F | Câblage | 3 fils : 3V3, GND, GPIO23 |

> Le sniffer n'est utilisé que pendant la phase de reverse engineering pour capturer
> les trames de la télécommande Technibel originale. Il n'est pas nécessaire dans l'installation finale.

### Conseils d'achat

- **Diymore PCB0100** : disponible sur AliExpress et Amazon. Chercher "Diymore IR transmitter PCB0100".
  Prendre la **version 2 canaux** — elle intègre transistor et résistances pour une utilisation en 5V.
- **KY-022** : composant standard des kits capteurs Arduino, disponible partout.
- **ESP32 DevKit** : tout board 30 ou 38 broches convient.
