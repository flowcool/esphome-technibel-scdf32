# Guide autonome — travaux réalisables avant réception de la commande

Ce document permet d'exécuter et de consigner, sans assistance en direct, les tâches
Technibel IR V2 qui ne nécessitent pas les composants de qualité commandés le
10 août 2026 dans la [commande principale](bom-v2.md#1-commande-principale).

Il traduit les phases du [plan V2](plan-v2-validation.md) en manipulations physiques.
Le plan V2 reste l'autorité en cas de divergence. Ne jamais sauter une phase : chaque
résultat **PASS** déverrouille la suivante ; un résultat **STOP** ou **ÉCHEC** arrête
la progression et doit être rapporté pour analyse.

## Périmètre

| Ordre | Bead | Phases | Faisable avant livraison | Condition |
|---:|---|---:|---|---|
| 1 | `infra-8xg.1` | 1–3 | Oui | XIAO, LED visible, résistances disponibles |
| 2 | `infra-8xg.2` | 4–6 | Oui, prototype | Seulement après 1–3 |
| 3 | `infra-8xg.3` | 7 | Oui | Seulement après 4–6 |
| 4 | `infra-8xg.4` | 8 | Oui | Seulement après 7 |
| 5 | `infra-8xg.5` | 9 | Oui | Seulement après 8 |
| 6 | `infra-8xg.7` | 11–12 | Oui, conditionnel | Seulement après validation de la phase 9 |

Ne pas entreprendre maintenant :

- la phase 10 (`infra-8xg.6`), car la carte de référence durable attend notamment la
  résistance 47 Ω / 0,6 W et les condensateurs de qualité commandés ;
- les phases 13–17 (`infra-8xg.8` et `infra-8xg.9`), qui dépendent de la preuve
  d'isolation, d'un schéma B1 adapté aux mesures et d'une revue séparée ;
- tout déploiement sur la VM ESPHome, toute installation permanente et toute connexion
  électrique entre le XIAO et la climatisation.

Les BC337-40, TSAL6400 et résistances actuellement disponibles servent ici au
**prototype de validation**. Ils ne deviennent pas des composants de référence parce
qu'un test passe. La livraison permettra ensuite de remplacer les éléments douteux et
de construire la carte durable.

## Règles de travail et de compte rendu

1. Travailler sur une table dégagée et non conductrice.
2. Couper l'alimentation avant chaque modification de câblage.
3. Ne connecter l'USB qu'après une vérification visuelle du montage.
4. Photographier le montage entier puis chaque zone avant le premier démarrage.
5. Noter la valeur réellement mesurée des résistances, pas seulement leur code couleur.
6. Ne jamais utiliser le module MB102 comme alimentation de référence pour ce diagnostic.
7. Conserver les captures et journaux bruts ; ne transmettre ni résumé seul ni valeur
   « corrigée ».
8. En cas d'odeur, chauffe, fumée, redémarrage du XIAO ou résultat incohérent : débrancher
   l'USB, ne rien recâbler, photographier et consigner.

Pour chaque phase, recopier le bloc **Résultats à remplir**. Les réponses peuvent être
collées telles quelles pour analyse et mise à jour du Bead associé. Utiliser :

- `PASS` : tous les résultats attendus sont obtenus ;
- `ÉCHEC` : le montage fonctionne assez pour mesurer, mais un critère n'est pas atteint ;
- `STOP` : danger, ambiguïté matérielle ou prérequis absent ; ne pas continuer.

## Repères physiques des composants

### LED visible et TSAL6400

Sur une LED neuve non raccourcie :

- la **patte longue** est normalement le côté positif, à placer vers la résistance et
  l'alimentation ;
- la **patte courte** est normalement le côté négatif, à placer vers le transistor ou
  GND selon le montage ;
- le méplat du boîtier indique normalement aussi le côté de la patte courte.

Si les pattes ont déjà été coupées, ne pas deviner : utiliser le mode diode du multimètre.
La LED peut luire faiblement lorsque la pointe rouge est sur le côté positif et la noire
sur le côté négatif. Une TSAL6400 émet en infrarouge : vérifier au multimètre et avec une
caméra préalablement testée sur la télécommande d'origine.

### BC337-40

Tenir le transistor avec la **face plate vers soi** et les trois pattes vers le bas.
Nommer provisoirement les pattes `gauche`, `milieu`, `droite`. Ne pas attribuer de fonction
à ces positions avant la phase 4 : les composants actuels peuvent avoir un brochage ou un
marquage non fiable. Une fois les mesures terminées, coller une petite étiquette sur ce
transistor avec `E`, `B` et `C`.

### Résistances

Sortir chaque résistance du circuit et mesurer sa valeur au multimètre. Préparer et
étiqueter : `330 Ω`, `470 Ω`, `10 kΩ`, `47 Ω` et, si disponible, `100 Ω` d'au moins
0,5 W. Une résistance 47 Ω de 0,25 W est autorisée uniquement pour le bref test modulé
ou une mesure phase 6 très courte ; elle n'est pas adaptée à un allumage fixe prolongé.

### KY-022 / VS1838B

Utiliser les **marquages imprimés sur le module**, jamais une position mémorisée :

- `S` ou `OUT` : signal vers le GPIO du récepteur ;
- `+` ou `VCC` : alimentation 3,3 V ;
- `-` ou `GND` : masse.

Si ces marquages sont absents ou différents, faire une photo nette recto-verso et marquer
`STOP`. Ne pas alimenter le module en devinant son brochage.

## Phase 1 — démarrer un XIAO ESP32-C3 nu

**Bead :** `infra-8xg.1`
**But :** vérifier le démarrage, le Wi-Fi et l'API sans circuit externe.

### Prérequis

- un XIAO ESP32-C3 sans aucun fil connecté ;
- un câble USB-C **de données** connu comme fonctionnel ;
- accès à l'environnement ESPHome réellement utilisé pour compiler et flasher ;
- mécanisme de récupération USB/bootloader connu avant le flash ;
- ESPHome 2024.6 ou plus récent.

Le dépôt n'est pas automatiquement synchronisé avec la VM ESPHome. Identifier et noter
la machine, le chemin actif et le moyen de transférer le fichier avant de prétendre que
la configuration du dépôt est en service.

### Procédure

1. Poser le XIAO seul sur la table, sans breadboard ni composant.
2. Créer la configuration minimale `ir-technibel-clim-c3.yaml` selon la phase 1 du plan V2 :
   carte `seeed_xiao_esp32c3`, variante `esp32c3`, framework Arduino,
   `board_build.flash_mode: dio` et logger sur `UART0`.
3. Valider la configuration ESPHome avant le flash.
4. Flasher par USB-C.
5. Conserver le journal complet du démarrage, de la connexion Wi-Fi et de l'API.

### Résultat attendu

- le XIAO apparaît dans ESPHome ;
- le journal indique une connexion Wi-Fi ;
- Home Assistant ou le client API joint le nœud ;
- aucun redémarrage en boucle.

### Résultats à remplir

```text
Phase 1 — infra-8xg.1
Statut: PASS / ÉCHEC / STOP
Date et heure:
Version ESPHome:
Machine ESPHome et chemin actif:
Commande ou action de validation:
Résultat de validation:
Méthode de flash:
Wi-Fi connecté: oui / non
API accessible: oui / non
Redémarrages observés: oui / non
Extrait ou fichier du journal brut:
Photos/fichiers:
Questions ou anomalie exacte:
```

**Arrêt :** si le flash échoue ou si la carte redémarre, ne pas ajouter de matériel.
La récupération consiste à débrancher tout circuit et reflasher le dernier YAML minimal
connu comme valide par USB.

## Phase 2 — faire clignoter une LED directement avec GPIO3

**Bead :** `infra-8xg.1`
**Prérequis :** phase 1 `PASS`.

### Câblage hors tension

Préparer une LED rouge visible et une résistance mesurée proche de 330 Ω.

```text
XIAO GPIO3 / D1 ── résistance 330 Ω ── patte longue de la LED rouge
patte courte de la LED rouge ───────── XIAO GND
```

La résistance n'a pas de sens de montage. Ne pas utiliser 47 Ω avec la LED visible.

### Procédure

1. Débrancher l'USB.
2. Réaliser le câblage ci-dessus et le photographier.
3. Ajouter au YAML la sortie GPIO3 et une bascule toutes les 500 ms décrites dans le plan.
4. Valider, flasher, puis observer la LED.
5. Mesurer entre GPIO3 et GND : pointe noire sur GND, pointe rouge sur GPIO3. La mesure
   doit alterner entre environ 0 V et 3,3 V.

### Résultat attendu

La LED alterne environ 0,5 seconde allumée et 0,5 seconde éteinte, soit un cycle complet
par seconde. GPIO3 alterne entre 0 V et 3,3 V.

### Résultats à remplir

```text
Phase 2 — infra-8xg.1
Statut: PASS / ÉCHEC / STOP
Résistance mesurée hors circuit:
Orientation LED: patte longue vers résistance / autre (expliquer)
Clignotement observé: oui / non
Tension GPIO3 état bas:
Tension GPIO3 état haut:
Comportement au démarrage:
Photos du câblage:
Journal ou erreur ESPHome:
Questions ou anomalie exacte:
```

**Arrêt :** si la LED ne clignote pas, couper l'USB. Vérifier d'abord le sens de la LED,
la valeur de la résistance, le pin `GPIO3/D1` et les contacts. Ne passer à GPIO4 que pour
diagnostic et le noter ; la suite du plan reste conçue pour GPIO3.

## Phase 3 — vérifier le rail 5 V

**Bead :** `infra-8xg.1`
**Prérequis :** phase 2 `PASS`.

### Procédure

1. Retirer la LED et sa résistance, USB débranché.
2. Alimenter le XIAO par un chargeur USB-C stable d'au moins 500 mA, idéalement 1 A.
3. Multimètre en tension continue : pointe noire sur `GND`, pointe rouge sur `5V`.
4. Noter la tension sans charge.
5. Si une résistance **100 Ω d'au moins 0,5 W** est déjà disponible et confirmée au
   multimètre, la placer entre `5V` et `GND`, attendre cinq secondes, puis relever la
   tension. Couper l'alimentation et laisser refroidir la résistance.
6. Si cette résistance n'est pas disponible, noter « charge 100 Ω non réalisée ». Ne pas
   la remplacer par 47 Ω. La charge réelle sera observée avec le circuit IR en phase 6.

### Résultat attendu

Le rail mesure entre 4,8 V et 5,2 V, sans fluctuation notable ni redémarrage. Avec la
charge 100 Ω, il reste dans cette plage.

### Résultats à remplir

```text
Phase 3 — infra-8xg.1
Statut: PASS / ÉCHEC / STOP
Chargeur et courant nominal:
Tension 5V sans charge:
Résistance de charge mesurée / puissance / non disponible:
Tension 5V sous charge:
Durée de la mesure:
Redémarrage ou variation:
Photos:
Questions ou anomalie exacte:
```

**Décision :** sans charge 100 Ω, la phase 3 est `PASS provisoire` si la tension à vide
est correcte ; le Bead ne doit être considéré entièrement vérifié qu'après la mesure de
courant de la phase 6 ou après réception de la résistance 100 Ω / 0,6 W.

## Phase 4 — identifier les trois pattes du BC337-40

**Bead :** `infra-8xg.2`
**Prérequis :** phases 1–3 passées au moins provisoirement.

### Identifier la patte de commande au multimètre

1. Prendre un BC337-40 neuf du stock actuel, hors circuit.
2. Le tenir face plate vers soi, pattes vers le bas ; nommer les pattes gauche, milieu,
   droite sur une feuille.
3. Mettre le multimètre en mode diode.
4. Tester les six combinaisons de sens entre les trois pattes et remplir le tableau.
5. La patte de commande est celle qui donne environ 0,60–0,70 V vers chacune des deux
   autres lorsque la pointe rouge se trouve dessus. Elle sera désormais nommée `B`.

| Pointe rouge | Pointe noire | Valeur mesurée |
|---|---|---|
| gauche | milieu | |
| milieu | gauche | |
| gauche | droite | |
| droite | gauche | |
| milieu | droite | |
| droite | milieu | |

Si ce motif n'apparaît pas, marquer `STOP`, isoler ce transistor dans un sachet
« suspect » et tester un autre exemplaire.

### Distinguer les deux autres pattes par commutation

Nommer provisoirement les deux pattes restantes `X` et `Y`. Réaliser le premier montage
hors tension :

```text
XIAO 5V ── 330 Ω ── patte longue LED rouge
patte courte LED rouge ── X du BC337
Y du BC337 ────────────── XIAO GND
XIAO 3V3 ── 470 Ω ─────── B du BC337
```

Alimenter brièvement et mesurer la tension entre X et Y. Couper l'USB, échanger seulement
X et Y, puis refaire la mesure. L'orientation correcte est celle qui allume la LED et
donne la tension la plus basse, normalement moins de 0,3 V. Dans cette orientation,
la patte côté LED est `C` et la patte côté GND est `E`. L'autre orientation devrait
normalement dépasser 0,5 V.

### Résultats à remplir

```text
Phase 4 — infra-8xg.2
Statut: PASS / ÉCHEC / STOP
Marquage exact imprimé sur le transistor:
Tableau des six mesures diode complété: oui / non
Position physique de B, face plate vers soi:
Orientation A (X côté LED, Y côté GND), tension X-Y:
Orientation B (Y côté LED, X côté GND), tension Y-X:
Position physique finale de C:
Position physique finale de E:
LED éteinte lorsque 3V3 est déconnecté de 470 Ω: oui / non
Photos des deux orientations:
Questions ou anomalie exacte:
```

**Arrêt :** deux valeurs similaires, absence de différence nette, LED restant allumée
sans commande, ou composant chaud imposent l'essai d'un autre transistor. Ne jamais
déduire C et E uniquement du boîtier.

## Phase 5 — chaîne GPIO3, BC337 et LED visible

**Bead :** `infra-8xg.2`
**Prérequis :** phase 4 `PASS`, transistor étiqueté `B`, `C`, `E`.

### Câblage hors tension

Utiliser le YAML de clignotement à 1 Hz de la phase 2.

```text
XIAO 5V ── 330 Ω ── patte longue LED rouge
patte courte LED rouge ── C du BC337 identifié
E du BC337 identifié ───── XIAO GND
XIAO GPIO3/D1 ── 470 Ω ─── B du BC337 identifié
B du BC337 ───── 10 kΩ ──── E du BC337 / XIAO GND
```

Le fil 10 kΩ maintient le transistor éteint pendant le démarrage. Toutes les masses du
montage de table sont reliées au même `GND` du XIAO.

### Mesures

1. Vérifier et photographier chaque liaison, puis connecter l'USB.
2. Observer le clignotement.
3. Pointe noire sur `E/GND`, pointe rouge sur `B` : relever la tension à l'état allumé.
4. Pointe noire sur `E/GND`, pointe rouge sur `C` : relever la tension à l'état allumé.
5. Redémarrer une fois et observer la LED avant l'initialisation du GPIO.

### Résultat attendu

- la LED clignote à 1 Hz ;
- la tension B–E est proche de 0,7 V à l'état allumé ;
- la tension C–E est inférieure à 0,5 V à l'état allumé ;
- la LED reste éteinte pendant le démarrage avant l'initialisation.

### Résultats à remplir

```text
Phase 5 — infra-8xg.2
Statut: PASS / ÉCHEC / STOP
Valeur mesurée 330 Ω:
Valeur mesurée 470 Ω:
Valeur mesurée 10 kΩ:
Clignotement 1 Hz: oui / non
Tension B-E allumé:
Tension C-E allumé:
LED éteinte au démarrage: oui / non
Chauffe ou redémarrage: oui / non
Photos:
Questions ou anomalie exacte:
```

## Phase 6 — remplacer la LED visible par la TSAL6400

**Bead :** `infra-8xg.2`
**Prérequis :** phase 5 `PASS`.

### Câblage hors tension

Garder le BC337 et les résistances 470 Ω et 10 kΩ exactement en place. Remplacer :

- la LED rouge par une TSAL6400 : patte longue vers la résistance, patte courte vers `C` ;
- la résistance 330 Ω par une résistance mesurée proche de 47 Ω.

```text
XIAO 5V ── 47 Ω ── patte longue TSAL6400
patte courte TSAL6400 ── C du BC337
E du BC337 ───────────── XIAO GND
XIAO GPIO3/D1 ── 470 Ω ─ B du BC337
B du BC337 ───── 10 kΩ ── E du BC337 / XIAO GND
```

### Procédure limitée avec la résistance actuelle

1. Tester d'abord la caméra avec la télécommande Technibel d'origine.
2. Si la résistance 47 Ω actuelle ne fait que 0,25 W, ne laisser le clignotement 500 ms
   actif que le temps strictement nécessaire à la mesure, au maximum quelques cycles.
3. Mesurer directement aux deux extrémités de la résistance 47 Ω pendant l'état allumé.
4. Couper ensuite l'USB. Calculer le courant : `tension mesurée / valeur mesurée en ohms`.
5. Le KY-022 ne prouve rien ici : l'éclairage est continu pendant 500 ms et non modulé
   à 38 kHz.

### Résultat attendu

- la caméra, si elle détecte 940 nm, montre un faible éclat violet ou blanc ;
- la tension aux bornes de 47 Ω est normalement comprise entre 3,2 et 3,6 V ;
- le courant calculé est normalement compris entre 68 et 76 mA ;
- aucun redémarrage du XIAO et aucune chauffe anormale.

### Résultats à remplir

```text
Phase 6 — infra-8xg.2
Statut: PASS / ÉCHEC / STOP
Télécommande visible avec cette caméra: oui / non
TSAL6400 visible avec cette caméra: oui / non / caméra non concluante
Résistance mesurée:
Puissance nominale connue: 0,25 W / 0,5 W ou plus / inconnue
Tension mesurée aux bornes de la résistance pendant ON:
Courant calculé (V/R):
Tension 5V pendant ON:
Nombre/durée des cycles de test:
Chauffe ou redémarrage:
Photos:
Questions ou anomalie exacte:
```

**Arrêt :** hors de 3,2–3,6 V, couper l'alimentation et ne pas corriger au hasard.
Vérifier le sens de la TSAL6400, la valeur de la résistance et le rail 5 V. Une résistance
0,25 W ne sera pas réutilisée pour la carte finale.

## Phase 7 — émission NEC à 38 kHz et réception KY-022

**Bead :** `infra-8xg.3`
**Prérequis :** phases 4–6 `PASS`.

### Émetteur

Conserver le montage TSAL6400 de phase 6. Retirer du YAML la bascule à 1 Hz et configurer
`remote_transmitter` sur `GPIO3`, porteuse 50 %, `non_blocking: false` et
`rmt_symbols: 96`. Ajouter le service NEC adresse `0x1234`, commande `0x5678` exactement
comme dans le plan V2.

### Récepteur sur une seconde carte

Utiliser un second XIAO ou l'ancien ESP32 dont le 3,3 V fonctionne. USB débranché :

```text
Seconde carte 3V3 ── broche marquée + ou VCC du KY-022
Seconde carte GND ── broche marquée - ou GND du KY-022
GPIO choisi RX ───── broche marquée S ou OUT du KY-022
```

Ne pas reprendre les positions de broches d'une photo Internet. Orienter la partie noire
du récepteur vers la TSAL6400, d'abord à environ 5 cm.

### Analyseur logique, sur le montage de table uniquement

1. Relier la pince `GND` de l'analyseur au `GND` du XIAO émetteur.
2. Relier le canal 0 à `GPIO3/D1`, sur le côté XIAO de la résistance 470 Ω.
3. Relier l'analyseur au PC uniquement parce que ce montage est alimenté en USB et ne
   touche pas la climatisation.
4. Déclencher `test_nec` et capturer la fréquence et les durées.

### Résultat attendu

- le journal du récepteur décode NEC `0x1234` / `0x5678` ;
- l'analyseur montre une porteuse proche de 38 kHz pendant les marques ;
- le décodage reste fiable à 30 cm ;
- aucune erreur d'allocation RMT à la compilation.

### Résultats à remplir

```text
Phase 7 — infra-8xg.3
Statut: PASS / ÉCHEC / STOP
Carte et GPIO du récepteur:
Marquages physiques KY-022 utilisés:
Validation ESPHome émetteur:
Adresse NEC décodée:
Commande NEC décodée:
Fréquence porteuse mesurée:
Période mesurée:
Distance maximale fiable:
Nombre de succès / nombre d'essais à 30 cm:
Erreur RMT éventuelle exacte:
Fichier journal brut:
Fichier/capture PulseView:
Photos des deux montages:
Questions ou anomalie exacte:
```

**Arrêt :** ne pas modifier les constantes du protocole Technibel pour corriger un échec
NEC. Un échec ici concerne encore la chaîne matérielle, la porteuse ou la configuration RMT.

## Phase 8 — comparer la trame Technibel à la télécommande

**Bead :** `infra-8xg.4`
**Prérequis :** phase 7 `PASS`.

### Procédure

1. Activer le YAML Technibel et l'inclusion `libraries/technibel_ir.h` dans
   l'environnement ESPHome identifié en phase 1 ; valider avant de flasher.
2. Sans modifier la position du KY-022, capturer séparément :
   - la télécommande : COOL, 24 °C, ventilation AUTO ;
   - le XIAO : COOL, 24 °C, ventilation AUTO, température ambiante 25 °C.
3. Sauvegarder les deux journaux bruts dans deux fichiers distincts.
4. Pour chaque capture : retirer l'en-tête 6500 µs / 3300 µs, classer chaque espace
   supérieur à 1500 µs comme `1` et inférieur à 1500 µs comme `0`, puis regrouper les
   48 bits en six octets, bit de poids fort en premier.
5. La trame oracle du XIAO est `D0 AC 28 F8 43 AC`.
6. Pour la télécommande, ne pas accepter une différence de B5 sans calcul. Recalculer
   la température ambiante avec la formule du plan V2, vérifier qu'elle se situe entre
   15 et 40 °C, puis renvoyer une trame XIAO avec cette même valeur.
7. Comparer aussi chaque durée à celle de la télécommande. Ne modifier que les constantes
   physiques de durée si les mesures instrumentées dépassent ±10 %. L'encodage et le
   checksum restent gelés.

### Résultat attendu

- trame XIAO à 25 °C : `D0 AC 28 F8 43 AC` ;
- B0 à B4 identiques entre télécommande et XIAO ;
- B5 expliqué exactement par une température ambiante plausible ;
- trame XIAO identique à celle de la télécommande avec cette température ;
- durées dans ±10 %.

### Résultats à remplir

```text
Phase 8 — infra-8xg.4
Statut: PASS / ÉCHEC / STOP
Chemin du YAML réellement compilé:
Résultat de validation ESPHome:
Trame XIAO t_amb=25 en hex:
Trame télécommande en hex:
B0-B4 identiques: oui / non
B5 télécommande:
t_amb recalculée depuis B5:
Trame XIAO avec cette t_amb:
B5 identiques après recalcul: oui / non
Écart maximal des durées:
Fichier capture brute télécommande:
Fichier capture brute XIAO:
Méthode/script de décodage utilisé:
Questions ou anomalie exacte:
```

**Arrêt :** une trame incomplète, une température recalculée hors 15–40 °C, un checksum
non reproductible ou un écart de durée supérieur à 10 % interdit le test sur la clim.
Conserver les captures sans modifier l'encodage.

## Phase 9 — test optique sur la climatisation

**Bead :** `infra-8xg.5`
**Prérequis :** phase 8 `PASS` complet.

Ce test est externe : aucun fil, aucune masse et aucun instrument ne se connecte à la
carte de la climatisation. Le retour arrière consiste à débrancher le XIAO et utiliser
la télécommande d'origine.

### Procédure

1. Placer la TSAL6400 à environ 30 cm de la fenêtre IR de l'unité intérieure, bien en face.
2. Envoyer COOL, 24 °C, ventilation AUTO, avec la température réelle de la pièce.
3. Exécuter ensuite, dans l'ordre, le tableau ci-dessous et noter chaque résultat.

| Essai | Commande | Résultat attendu | Résultat observé |
|---:|---|---|---|
| 1 | COOL 24 °C AUTO | bip, démarrage, affichage 24 °C | |
| 2 | température 22 °C | affichage 22 °C | |
| 3 | DRY | passage en déshumidification | |
| 4 | FAN | ventilation seule | |
| 5 | AUTO | mode automatique | |
| 6 | OFF | bip puis arrêt/affichage éteint | |
| 7 | COOL 24 °C AUTO | redémarrage | |

4. Capturer un appui de la télécommande d'origine et compter le nombre de trames émises.
5. Si elle en émet plusieurs, rapporter le résultat avant de modifier la répétition YAML.
6. Envoyer dix fois une commande valide, avec un délai permettant à la clim de réagir,
   et compter les succès.

### Résultat attendu

La climatisation réagit au premier envoi à 30 cm, les quatre modes, OFF et la température
fonctionnent, puis dix essais sur dix réussissent. Le comportement de répétition de la
télécommande est documenté.

### Résultats à remplir

```text
Phase 9 — infra-8xg.5
Statut: PASS / ÉCHEC / STOP
Distance et angle approximatif:
Température ambiante envoyée:
Tableau des sept essais complété: oui / non
Premier envoi reçu: oui / non
COOL: PASS / échec observé
DRY: PASS / échec observé
FAN: PASS / échec observé
AUTO: PASS / échec observé
OFF: PASS / échec observé
Changement 24 vers 22 °C: PASS / échec observé
Répétition: nombre de succès / 10
Nombre de trames par appui de la télécommande:
Journaux/captures:
Vidéo ou photos:
Questions ou anomalie exacte:
```

**Arrêt :** si la première commande échoue, essayer une fois à 5 cm et noter le résultat,
mais ne modifier ni l'encodage ni plusieurs paramètres simultanément. Un deuxième
émetteur IR est un diagnostic ultérieur, pas une raison de contourner un gatekeeper.

## Phases 11–12 — inspection de la clim et preuve d'isolation

**Bead :** `infra-8xg.7`
**Prérequis impératif :** phase 9 `PASS`. La phase 10 n'est pas requise pour inspecter,
mais la Piste A validée doit rester disponible comme solution de repli.

> **Danger secteur.** Ces phases n'autorisent aucune mesure sous tension, aucune
> modification de la carte et aucune connexion d'un PC, XIAO, analyseur logique ou
> oscilloscope à la climatisation. Un multimètre ordinaire ne certifie pas l'isolation.

### Phase 11 — inspection visuelle seulement

1. Arrêter la clim normalement, puis couper son disjoncteur identifié.
2. Empêcher une remise sous tension accidentelle et vérifier l'absence de fonctionnement.
3. Attendre le temps de décharge du manuel de service. Sans manuel, cinq minutes ne sont
   qu'une précaution et non une preuve que tous les condensateurs sont déchargés.
4. Ouvrir l'unité sans toucher la zone d'alimentation. Photographier chaque étape avant
   de débrancher ou déplacer quoi que ce soit.
5. Photographier recto et verso accessibles de la carte, connecteurs et sérigraphies.
6. Repérer le petit récepteur IR noir à trois pattes et relever son marquage exact.
7. Rechercher sa fiche technique exacte avant d'attribuer `VCC`, `GND` et `Signal`.
8. Suivre visuellement la piste Signal vers le microcontrôleur sans sonde.
9. Relever les marquages de rails (`5V`, `12V`, `GND`, `VCC`) sans les mesurer.
10. Repérer transformateur, optocoupleurs, fente ou distance d'isolement, circuit
    d'alimentation et tout conducteur traversant la frontière présumée.

### Résultats phase 11 à remplir

```text
Phase 11 — infra-8xg.7
Statut: PASS / ÉCHEC / STOP
Disjoncteur coupé et remise sous tension empêchée: oui / non
Temps de décharge appliqué et source de ce temps:
Référence exacte du récepteur IR:
Lien ou fichier de la fiche technique exacte:
Patte VCC identifiée par fiche technique:
Patte GND identifiée par fiche technique:
Patte Signal identifiée par fiche technique:
Destination visible de la piste Signal:
Marquages des rails observés:
Éléments de la frontière d'isolation observés:
Tous les éléments traversant cette frontière:
Photos numérotées et légendées:
Connecteur déplacé: oui / non; lequel:
Questions ou ambiguïté exacte:
```

Si le récepteur, ses trois pattes ou la frontière ne sont pas identifiables, refermer à
l'identique d'après les photos et marquer `STOP`. La recherche documentaire peut se faire
ensuite sans laisser la clim ouverte.

### Phase 12 — confirmation documentaire puis résistances hors tension

Ne commencer que si la phase 11 permet de tracer une frontière cohérente.

1. Identifier la topologie de l'alimentation à partir des références exactes des
   composants, de leurs fiches techniques ou du manuel de service.
2. Énumérer chaque élément traversant la frontière : transformateur, optocoupleur,
   condensateur de sécurité, connecteur, blindage ou fixation.
3. Obtenir une confirmation documentaire que le secondaire logique est isolé. Une simple
   photo de transformateur est un indice fort, pas la confirmation complète.
4. Clim hors tension, disjoncteur coupé et temps de décharge respecté, mettre le
   multimètre en gamme MΩ. Ne pas toucher ni sonder la partie primaire interne.
5. Sur le bornier secteur identifié, mesurer séparément entre le `GND` logique et :
   - la borne `L` ;
   - la borne `N` ;
   - la borne `PE` de terre.
6. Noter la valeur initiale, la valeur stabilisée, la gamme et le modèle du multimètre.
   Ne faire aucune mesure de tension logique-secteur.

### Résultat attendu et décision

- `GND` logique vers `L` : supérieur à 1 MΩ ou `OL` ;
- `GND` logique vers `N` : supérieur à 1 MΩ ou `OL` ;
- `GND` logique vers `PE` : valeur relevée et tout chemin de faible résistance expliqué ;
- topologie isolée confirmée par documentation et chaque traversée comprise.

Les résistances ne sont qu'un contrôle complémentaire. La phase 12 ne passe que si
**la documentation confirme l'architecture isolée ET les mesures complémentaires sont
cohérentes**. Toute ambiguïté garde B1 bloquée.

### Résultats phase 12 à remplir

```text
Phase 12 — infra-8xg.7
Statut: PASS / ÉCHEC / STOP
Référence de la carte/alimentation:
Topologie identifiée:
Source documentaire confirmant le secondaire isolé:
Frontière d'isolation décrite:
Liste exhaustive des éléments qui la traversent:
Modèle du multimètre et gamme:
GND logique vers L, valeur initiale / stabilisée:
GND logique vers N, valeur initiale / stabilisée:
GND logique vers PE, valeur initiale / stabilisée:
Chemin expliquant la relation à PE:
Mesure instable ou inférieure/égale à 1 MΩ:
Photos annotées des points exacts de mesure:
Architecture confirmée ET contrôle cohérent: oui / non
Questions ou ambiguïté exacte:
```

### Arrêt et remise en état

Si l'isolation n'est pas intégralement confirmée :

- ne connecter **aucun** PC, USB, analyseur logique, oscilloscope de table, XIAO en
  masse commune ou interface BC337 à la carte de climatisation ;
- ne pas considérer un ordinateur sur batterie ou un chargeur USB « flottant » comme
  une isolation de sécurité ;
- conserver la Piste A externe et laisser B1 bloquée ;
- replacer tous les connecteurs et capots exactement d'après les photos, puis vérifier
  uniquement le fonctionnement normal avec la télécommande après fermeture complète.

## Bloc de retour global

Après une ou plusieurs phases, joindre ce résumé aux blocs détaillés :

```text
Guide travaux avant réception — retour global
Dernière phase entièrement PASS:
Phase actuellement bloquée:
Bead(s) concerné(s):
Montage actuellement alimenté: oui / non
Montage laissé assemblé: oui / non; description
Fichiers/captures/photos disponibles et chemins:
Modification firmware/YAML effectuée:
Modification physique de la clim: aucune / expliquer
Question prioritaire:
```

Ne pas fermer soi-même les Beads sur la seule base d'un résumé. Les valeurs, journaux,
captures et photos permettent ensuite d'analyser le gatekeeper, de poser les questions
ciblées et d'enregistrer la preuve exacte dans `infra-8xg.1` à `.5` ou `infra-8xg.7`.
