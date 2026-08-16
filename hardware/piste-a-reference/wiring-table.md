# Piste A perfboard wiring table

Coordinate convention: component-side view, USB-C toward row 1. The solder-side drawing is mirrored by KiCad.

| Wire | Net | Color | Side | From | To | Straight length |
|---|---|---|---|---|---|---:|
| W01 | `GPIO3` | YELLOW | solder side | `B3` | `A3` | 2.5 mm |
| W02 | `GPIO3` | YELLOW | solder side | `A3` | `A11` | 20.3 mm |
| W03 | `GPIO3` | YELLOW | solder side | `A11` | `B11` | 2.5 mm |
| W04 | `BASE` | YELLOW | solder side | `E11` | `E18` | 17.8 mm |
| W05 | `BASE` | YELLOW | solder side | `E18` | `E20` | 5.1 mm |
| W06 | `+3V3` | YELLOW | solder side | `H4` | `I4` | 2.5 mm |
| W07 | `GND` | BLACK | solder side | `H3` | `I3` | 2.5 mm |
| W08 | `GND` | BLACK | solder side | `I3` | `G3` | 5.1 mm |
| W09 | `GND` | BLACK | solder side | `F18` | `G18` | 2.5 mm |
| W10 | `GND` | BLACK | solder side | `H20` | `G20` | 2.5 mm |
| W11 | `+5V` | RED | component-side jumper | `H2` | `J2` | 5.1 mm |
| W12 | `+5V` | RED | solder side | `J2` | `J21` | 48.3 mm |
| W13 | `IR_ANODE` | YELLOW | solder side | `F21` | `F23` | 5.1 mm |
| W14 | `IR_CATHODE` | YELLOW | solder side | `D18` | `C18` | 2.5 mm |
| W15 | `IR_CATHODE` | YELLOW | solder side | `C18` | `C24` | 15.2 mm |
| W16 | `IR_CATHODE` | YELLOW | solder side | `C24` | `G24` | 10.2 mm |
| W17 | `IR_CATHODE` | YELLOW | solder side | `G24` | `G23` | 2.5 mm |
| W18 | `GND` | BLACK | solder side | `G3` | `G18` | 38.1 mm |
| W19 | `GND` | BLACK | solder side | `G18` | `I18` | 5.1 mm |
| W20 | `GND` | BLACK | solder side | `G18` | `G20` | 5.1 mm |
| W21 | `GND` | BLACK | solder side | `I17` | `I18` | 2.5 mm |
| W22 | `GND` | BLACK | solder side | `I18` | `I19` | 2.5 mm |

## Component coordinates

| Ref | Value | Pin coordinates |
|---|---|---|
| U1 | XIAO ESP32-C3, 2x7 sockets | pin 2/D1/GPIO3=`B3`; pin 8/5V=`H2`; pin 9/GND=`H3`; pin 10/3V3=`H4`; all 14 pins represented |
| R1 | 470 ohm | 2/GPIO3=`B11`; 1/BASE=`E11` |
| Q1 | BC33740BU | 1/C=`D18`; 2/B=`E18`; 3/E=`F18` |
| R2 | 10 kohm | 1/BASE=`E20`; 2/GND=`H20` |
| C1 | 100 nF | 2/GND=`I3`; 1/3V3=`I4` |
| C2 | 100 nF | 2/GND=`I17`; 1/5V=`J17` |
| C3 | 100 uF | 2/GND=`I19`; 1/+5V=`J19` |
| R3 | 47 ohm / 0.6 W | 1/5V=`J21`; 2/IR_ANODE=`F21` |
| D1 | fresh TSAL6400 | 2/A=`F23`; 1/K=`G23` |
