# État des lieux historique & TODO (2026-07-04)

> Note : ce document est un suivi de session de debug, en français uniquement
> (contrairement aux autres docs du repo qui sont bilingues). À nettoyer/fusionner
> dans `troubleshooting.md` une fois le problème matériel résolu.
>
> Mise à jour d'architecture (2026-08-10) : les mentions NAS et chemins
> `/volume1/...` ci-dessous décrivent uniquement l'ancien environnement. Le live
> ESPHome/Home Assistant est désormais sur une VM dédiée. Ses chemins et son mode
> de déploiement doivent être vérifiés avant toute action.

## Ce qui fonctionne (validé de bout en bout)

La chaîne logicielle complète a été testée avec succès :

```
Carte Mushroom (climate.clim_sejour)
  → entité MQTT climate (packages/clim_sejour.yaml)
  → automatisation "Clim Séjour — Envoyer commande IR"
  → service esphome.ir_technibel_clim_send_command
  → firmware ir-technibel-clim.yaml (lambda + technibel_ir.h)
  → remote_transmitter → GPIO4
```

Log de confirmation obtenu (via logs série USB) :
```
[technibel] IR sent: mode=COOL temp=21 fan=LOW amb=24 power=ON
```

Le calcul de trame (`technibel_ir.h`) a été vérifié manuellement contre l'exemple
documenté dans `protocol.md` (trame OFF `D0 AC 28 08 43 64`) — checksum et
encodage température corrects.

## Bugs logiciels trouvés et corrigés pendant cette session

1. **IP obsolète en cache côté HA** — l'intégration ESPHome pour `ir-technibel-clim`
   gardait `host: 192.168.2.156` alors que l'ESP32 (pas d'IP statique, DHCP) avait
   changé d'adresse. Résultat : `Errno 113 (No route to host)` en boucle dans
   `home-assistant.log`, aucun appel de service n'atteignait jamais l'ESP32.
2. **Automatisation désactivée** — "Clim Séjour — Envoyer commande IR" était
   basculée off dans l'UI HA, indépendamment du problème réseau ci-dessus. Son
   état (on/off) est stocké dans le registre HA (`.storage`), pas dans le YAML —
   donc un simple redémarrage HA ne la réactive pas automatiquement.

## Tentative de refonte annulée

Essai de remplacer MQTT + automatisation par un `climate: platform: template`
natif ESPHome (pour supprimer un point de défaillance). **Ce composant n'existe
pas** dans ESPHome — vérifié directement dans le conteneur : le composant
`template` ne fournit pas de plateforme `climate` (seulement sensor, switch,
fan, cover, number, etc.). Erreur : `Platform not found: 'climate.template'`.

Tout a été annulé et restauré à l'identique :
- `esphome/ir-technibel-clim.yaml` (repo + NAS)
- `homeassistant/climate-technibel-ha.yaml` (repo)
- `packages/clim_sejour.yaml` (NAS)

Le firmware sur l'ESP32 n'a **jamais été reflashé** avec la version cassée
(la compilation a échoué avant tout flash) — le device tourne toujours la
version fonctionnelle testée plus haut.

**Si on veut retenter un jour** : la seule vraie voie native pour un protocole
IR custom est un composant `climate_ir` (vraie classe C++ héritant de
`climate_ir::ClimateIR`, structure `external_component` complète) — plus
lourd qu'un simple template YAML. Toujours valider avec `esphome config`
avant de dire que c'est prêt.

## Découverte annexe historique : repo git ≠ ancien dossier live NAS

`~/claude_project/esphome-technibel-scdf32` (ce repo) et
`/volume1/docker/homeassistant/esphome/` (dossier monté dans le conteneur
ESPHome, ce que voit réellement le dashboard) sont **deux copies séparées**.
Avant cette session, `ir-technibel-clim.yaml` n'existait que dans le repo,
pas côté NAS (seule `libraries/technibel_ir.h` avait été copiée). À garder
en tête : toute modif du repo doit être copiée manuellement vers le NAS pour
être prise en compte par le dashboard.

## Problème matériel non résolu : pas de bip de la clim

Point bloquant actuel. Une fois le logiciel confirmé fonctionnel (log "IR
sent"), l'ESP32 remis en position devant la climatisation **ne déclenche
aucun bip**. Ce qui a été vérifié bon pendant cette session :

- LED TSAL6400 : tension directe ~1.3V cohérente (diode test)
- Transistor 2N2222 : bon hors circuit (Base-Emitter ~650mV, Base-Collector
  ~650mV, Collector-Emitter OL)
- Continuité câblage 3V3 → R22Ω → anode → cathode → collector : bonne (après
  avoir retrouvé et réparé un lien Collector↔Cathode décroché)
- Alimentation 3V3 : ~3V confirmé

Ce qui reste non concluant :
- Tension du collecteur au repos incohérente selon le calibre du multimètre
  (0V/OL sur calibre 4V, 6V sur calibre 40V) — probablement une limite du
  multimètre sur ce nœud, jamais totalement élucidé
- Pas de test caméra possible (le téléphone ne voit même pas une télécommande
  TV classique — caméra inutilisable pour ce diagnostic)
- Câblage jamais re-vérifié après le dernier déplacement physique du montage
  devant la clim — `wiring.md` signale explicitement la fragilité des fils
  Dupont sur pattes nues en cas de manipulation

## TODO pour repartir propre

1. Redémarrer HA pour recharger `packages/clim_sejour.yaml` (restauré)
2. Vérifier/réactiver manuellement l'automatisation dans l'UI HA après le
   redémarrage (Paramètres → Automatisations)
3. Retester une commande réelle pour confirmer le retour à l'état
   fonctionnel d'avant l'incident
4. Refaire la continuité **après le dernier déplacement du montage** :
   - Collector (droite) ↔ Cathode LED
   - Emitter (gauche) ↔ GND
   - Base (milieu) ↔ sortie résistance 470Ω
5. Vérifier l'orientation de la LED et son alignement/distance par rapport
   à la fenêtre réceptrice IR de la climatisation
6. Envisager une IP statique (`wifi: manual_ip:`) dans
   `ir-technibel-clim.yaml` pour éviter de reperdre la connexion HA au
   prochain reboot/reflash
7. Se souvenir de copier tout futur changement du repo vers le dossier live
   NAS (`/volume1/docker/homeassistant/esphome/`) — les deux ne se
   synchronisent pas automatiquement
