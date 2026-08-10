# Technibel IR V2 — Liste de matériel

Cette nomenclature couvre la validation de la **Piste A** (émission IR externe),
la réalisation d'un montage de référence durable et une partie du matériel pouvant
être utile à la **Piste B1** (injection sur la ligne du récepteur IR).

Les références indiquées sont des références fabricant exactes et traçables. Elles
peuvent être commandées chez Mouser France ou recherchées à l'identique chez Farnell,
RS ou un autre distributeur agréé.

> Ne pas acheter le circuit d'interface B1 définitif avant d'avoir identifié le
> récepteur IR, le niveau logique, son type de sortie et l'isolation électrique de
> la carte du climatiseur.

## 1. Commande principale

| Qté | Fonction | Fabricant | Référence fabricant | Caractéristiques | Usage |
|---:|---|---|---|---|---|
| 10 | Résistance LED IR | Vishay / BC Components | `MRS25000C4709FRP00` | 47 Ω, 1 %, 0,6 W, traversante | Piste A |
| 5 | Charge de test 5 V | Vishay / BC Components | `MRS25000C1000FRP00` | 100 Ω, 1 %, 0,6 W, traversante | Validation |
| 20 | Résistance de base BC337 | Yageo | `MFR-50SFRF52-470R` | 470 Ω, 1 %, 0,5 W, AEC-Q200 | A et B1 |
| 20 | Résistance LED visible | Yageo | `MFR-25FBF52-330R` | 330 Ω, 1 %, 0,25 W | Validation |
| 20 | Pull-down base-émetteur | Yageo | `MFR-25FBF52-10K` | 10 kΩ, 1 %, 0,25 W | A et B1 |
| 10 | Pull-up éventuel | Yageo | `MFR-25FBF52-4K7` | 4,7 kΩ, 1 %, 0,25 W | B1 conditionnel |
| 10 | Protection/test signal | Yageo | `MFR-25FBF52-1K` | 1 kΩ, 1 %, 0,25 W | B1 conditionnel |
| 20 | Découplage local | Vishay / BC Components | `K104K15X7RF5TL2` | 100 nF, 50 V, X7R, radial | A et B1 |
| 10 | Réservoir alimentation | Panasonic | `EEU-FR1E101` | 100 µF, 25 V, 105 °C, low ESR | A et B1 |
| 10 | Diode Schottky alimentation | Vishay | `1N5817-E3/54` | 1 A, traversante | Alimentation conditionnelle |
| 10 | Diode Schottky signal | Vishay | `BAT41-TR` | 100 V, 100 mA, DO-35 traversant | B1 conditionnel |
| 10 | Transistor NPN authentique | onsemi | `BC33740BU` | BC337-40, 45 V, 800 mA, TO-92, conditionnement vrac | Référence A et B1 |
| 10 | LED IR authentique | Vishay | `TSAL6400` | 940 nm, angle ±25°, traversante | Piste A |

### Pourquoi conserver des composants authentiques de référence

Les BC337-40 et TSAL6400 déjà disponibles peuvent être utilisés. Quelques composants
provenant d'un distributeur agréé servent cependant d'étalons : en cas d'échec, ils
permettent d'écarter rapidement un faux marquage, un mauvais brochage ou un composant
hors spécification.

### Dimensionnement important

- La résistance de `47 Ω` est réservée à la TSAL6400 alimentée en 5 V.
- Utiliser une puissance nominale d'au moins 0,5 W pour la résistance de `47 Ω`.
- Ne pas utiliser `47 Ω` avec une LED visible standard ; utiliser `330 Ω`.
- La résistance de charge `100 Ω / 0,6 W` dissipe environ 0,25 W sous 5 V.
- Placer un `100 nF` au plus près de l'alimentation du XIAO.
- Placer un `100 nF` et un `100 µF` près du driver IR.
- Respecter la polarité du condensateur électrolytique.

## 2. Connectique JST-XH

Pour les liaisons basse tension nécessitant un connecteur démontable :

| Qté | Élément | Fabricant | Référence fabricant |
|---:|---|---|---|
| 5 | Embase PCB verticale, 2 positions | JST | `B2B-XH-A-BK(LF)(SN)` |
| 5 | Boîtier femelle, 2 positions | JST | `XHP-2` |
| 20 | Contact femelle pour fil | JST | `SXH-002T-P0.6` |

Un sertissage mal réalisé est moins fiable qu'une soudure correcte. Utiliser une pince
adaptée aux contacts JST-XH ou acheter des fils présertis. Pour une installation
permanente, ajouter un soulagement de traction ; le connecteur ne doit pas reprendre
les efforts mécaniques du câble.

## 3. Alimentation USB de test

Utiliser une alimentation USB-C stable et authentique, capable de fournir au moins
500 mA. Une alimentation de 1 A ou plus donne une marge confortable pour les pointes
de courant Wi-Fi.

Exemple robuste :

| Qté | Produit | Référence | Caractéristiques |
|---:|---|---|---|
| 1 | Alimentation officielle Raspberry Pi USB-C EU | `SC0873` | 5,1 V, 3 A, prise européenne |

Prévoir également un câble USB-C **de données** fiable et identifié pour le flash.
Ne pas utiliser le module MB102 comme alimentation de référence lors d'un diagnostic.

## 4. Conversion 12 V vers 5 V — achat anticipé facultatif

Si la clim ne fournit qu'un rail basse tension de 12 V, un convertisseur industriel
est préférable à un module ajustable sans marque.

| Qté | Fabricant | Référence fabricant | Entrée | Sortie | Remarque |
|---:|---|---|---|---|---|
| 2 | TRACO Power | `TSR 1-2450` | 6,5–36 V CC | 5 V / 1 A | SIP-3, non isolé |

> Le `TSR 1-2450` est **non isolé**. Il ne doit être utilisé que si le rail qui
> l'alimente a déjà été identifié comme une basse tension sûre et correctement isolée
> du secteur. Il ne rend pas une alimentation dangereuse sûre.

Ne pas installer ce convertisseur avant d'avoir mesuré la tension réelle et vérifié
la capacité du rail interne.

## 5. Matériel mécanique

Les dimensions exactes dépendront de l'emplacement retenu, mais prévoir :

- gaine thermorétractable 2:1 : 1,6 mm, 3,2 mm et 6,4 mm ;
- entretoises nylon M2 ou M2.5 : hauteurs 6 mm et 10 mm ;
- vis et écrous nylon assortis ;
- colliers polyamide et embases de retenue ;
- petit boîtier isolant à brides, environ 60 × 40 × 20 mm ;
- passe-fil ou serre-câble ;
- mini-grabbers isolés pour les mesures basse tension ;
- plaque à pastilles étamées double face de bonne qualité ;
- supports femelles 7 contacts, pas 2,54 mm, si les supports actuels maintiennent mal le XIAO.

Dans la clim, ne pas compter sur un adhésif seul. La carte doit être fixée
mécaniquement, protégée des parties conductrices, des vibrations, de la condensation,
des moteurs et du câblage secteur.

## 6. Matériel déjà disponible et réutilisable

D'après l'inventaire du projet :

- Seeed XIAO ESP32-C3 ;
- Seeed XIAO ESP32-C6 comme solution de repli ;
- BC337-40 ;
- TSAL6400 ;
- résistances 47 Ω, 330 Ω et 470 Ω ;
- LED visibles ;
- KY-022 / VS1838B ;
- analyseur logique USB 24 MHz ;
- multimètre ;
- plaques FR4 ;
- fil silicone 22/24 AWG ;
- headers 2,54 mm ;
- breadboards ;
- matériel de soudure.

Avant de commander, vérifier les résistances déjà disponibles au multimètre et lire
leur puissance nominale. Les résistances `47 Ω` de 0,25 W restent utilisables pour des
essais brefs, mais pas comme choix final avec la TSAL6400 à environ 74 mA.

## 7. Achats à différer jusqu'à l'inspection de la clim

Ne pas choisir avant la caractérisation de la carte :

- optocoupleur ;
- isolateur numérique ;
- buffer ou porte logique ;
- convertisseur DC/DC isolé ;
- valeur définitive du pull-up de la ligne IR ;
- circuit wired-OR définitif ;
- connecteur correspondant à la carte de la clim ;
- équipement de mesure isolé spécialisé.

Le choix dépendra de :

1. l'isolation réelle de la logique par rapport au secteur ;
2. la tension d'alimentation du récepteur IR ;
3. la tension de la ligne Signal côté MCU ;
4. la topologie de sortie du récepteur IR ;
5. la tension et la capacité du rail utilisé pour alimenter le XIAO.

## 8. Liens de vérification

- [Vishay MRS25 — 47 Ω, 0,6 W](https://www.mouser.fr/ProductDetail/Vishay-BC-Components/MRS25000C4709FRP00)
- [Vishay MRS25 — 100 Ω, 0,6 W](https://www.mouser.fr/ProductDetail/Vishay-BC-Components/MRS25000C1000FRP00)
- [Yageo 10 kΩ, 0,25 W, 1 %](https://www.mouser.fr/fr/ProductDetail/YAGEO/MFR-25FBF52-10K)
- [Yageo MFR-50SFRF52-470R — 470 Ω, 0,5 W, 1 %, AEC-Q200](https://www.mouser.fr/ProductDetail/YAGEO/MFR-50SFRF52-470R)
- [Vishay 100 nF, 50 V, X7R](https://www.mouser.fr/ProductDetail/Vishay-BC-Components/K104K15X7RF5TL2)
- [Panasonic FR 100 µF, 25 V](https://www.mouser.fr/fr/ProductDetail/Panasonic/EEU-FR1E101)
- [onsemi BC33740BU — BC337-40 traversant](https://www.mouser.fr/ProductDetail/onsemi/BC33740BU)
- [Vishay BAT41-TR — Schottky signal traversante](https://www.mouser.fr/ProductDetail/Vishay-Semiconductors/BAT41-TR)
- [Vishay TSAL6400](https://www.mouser.fr/ProductDetail/Vishay-Semiconductors/TSAL6400)
- [JST série XH](https://www.mouser.fr/c/connectors/?series=XH)
- [TRACO Power TSR 1-2450](https://www.mouser.fr/ProductDetail/TRACO-Power/TSR-1-2450)
