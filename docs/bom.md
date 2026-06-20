# Bill of Materials / Liste de matériel

**[🇬🇧 English](#-english)** · **[🇫🇷 Français](#-français)**

---

## 🇬🇧 English

### Transmitter (final build)

| Component | Reference | Role | Notes |
|---|---|---|---|
| MCU | ESP32 DevKit 30-pin | Main controller | Any ESP32 board works |
| IR LED | TSAL6400 (5mm, 940nm) | IR emission | Any 940nm 5mm IR LED works |
| Transistor | 2N2222 NPN (TO-92) | LED driver | BC337 also works |
| Resistor | 47Ω | LED current limiting | 33Ω–68Ω acceptable |
| Resistor | 470Ω | Transistor base | 330Ω–560Ω acceptable |
| Cables | Dupont M/M + M/F | Wiring | 5 connections total |
| Enclosure | Any | Optional | Protects the ESP32 |

### Sniffer (capture phase only — not needed in final build)

| Component | Reference | Role | Notes |
|---|---|---|---|
| IR receiver | KY-022 / VS1838B (38kHz) | Capture raw IR frames | Frequency must be 38kHz |
| Cables | Dupont M/F | Wiring | 3 wires: 3V3, GND, GPIO23 |

> The sniffer is used only during the reverse engineering phase to capture frames
> from the original Technibel remote control. It is not needed in the final installation.

### Sourcing tips

- **TSAL6400**: available on AliExpress and Amazon. Search "TSAL6400 940nm IR LED". Any 940nm 5mm IR emitter is a drop-in substitute.
- **2N2222**: included in most BJT transistor assortment kits. BC337 is a common alternative.
- **KY-022**: standard Arduino sensor kit component, available everywhere.
- **ESP32 DevKit**: any 30-pin or 38-pin ESP32 board works.

---

## 🇫🇷 Français

### Émetteur (montage final)

| Composant | Référence | Rôle | Notes |
|---|---|---|---|
| MCU | ESP32 DevKit 30 broches | Contrôleur principal | Tout ESP32 fonctionne |
| LED IR | TSAL6400 (5mm, 940nm) | Émission IR | Toute LED IR 940nm 5mm convient |
| Transistor | 2N2222 NPN (TO-92) | Driver LED | BC337 convient aussi |
| Résistance | 47Ω | Limitation courant LED | 33Ω–68Ω acceptables |
| Résistance | 470Ω | Base transistor | 330Ω–560Ω acceptables |
| Câbles | Dupont M/M + M/F | Câblage | 5 connexions au total |
| Boîtier | Au choix | Optionnel | Protège l'ESP32 |

### Sniffer (phase de capture uniquement — inutile dans le montage final)

| Composant | Référence | Rôle | Notes |
|---|---|---|---|
| Récepteur IR | KY-022 / VS1838B (38kHz) | Capturer trames IR brutes | Fréquence obligatoirement 38kHz |
| Câbles | Dupont M/F | Câblage | 3 fils : 3V3, GND, GPIO23 |

> Le sniffer n'est utilisé que pendant la phase de reverse engineering pour capturer
> les trames de la télécommande Technibel originale. Il n'est pas nécessaire dans l'installation finale.

### Conseils d'achat

- **TSAL6400** : disponible sur AliExpress et Amazon. Chercher "TSAL6400 940nm IR LED". Toute LED IR 940nm 5mm est interchangeable.
- **2N2222** : inclus dans la plupart des kits de transistors BJT. BC337 est une alternative courante.
- **KY-022** : composant standard des kits capteurs Arduino, disponible partout.
- **ESP32 DevKit** : tout board 30 ou 38 broches convient.
