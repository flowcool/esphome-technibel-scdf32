# BACKLOG — esphome-technibel-scdf32

## Priorité haute

- [ ] **Tester les 5 modes end-to-end** depuis HA : off / cool / dry / fan_only / auto
  + variations consigne (16–30°C) + vitesse fan (auto/low/med/high)
  → jamais validé depuis la session de reverse engineering (mai 2026)

- [ ] **IP statique pour l'ESP32** : réservation DHCP par adresse MAC dans le routeur
  → l'ESP était hors-ligne plusieurs jours suite à un changement d'IP (192.168.2.156 obsolète)

## Priorité moyenne

- [ ] **Installation permanente** : souder le circuit discret (TSAL6400 + 2N2222 + résistances),
  trouver le bon angle vers le récepteur IR de la clim, mettre en boîtier
  → câblage Dupont actuel fragile, angle ±17° critique

- [ ] **Aligner les YAMLs ESPHome** : la config production (`ir-clim-sniffer.yaml` dans ESPHome docker)
  a des options framework en plus (`minimum_chip_revision: 3.1`, `sram1_as_iram: true`)
  absentes du repo GitHub (`ir-technibel-clim.yaml`) → synchroniser

- [ ] **Renommer `ir-clim-sniffer.yaml`** dans ESPHome dashboard → `ir-technibel-clim.yaml`
  pour éviter la confusion (le fichier contient la config émetteur, pas le sniffer)

## Priorité basse / idées

- [ ] **Multi-LED** : ajouter une 2e TSAL6400 en parallèle (47Ω propre par LED)
  pour élargir le cône de couverture si le placement fixe reste sensible à l'angle
  → voir `docs/wiring.md` section "Optional: multiple LEDs"

- [ ] **Automations de confort** : horaires, seuils température (ex : cool auto à 17h30 si T° > 25°C)
  → à écrire dans `/homeassistant/packages/clim_sejour.yaml` quand le montage est finalisé
