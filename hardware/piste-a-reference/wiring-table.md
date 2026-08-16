# Piste A perfboard wiring table

Coordinate convention: component-side view, USB-C toward row 1. The solder-side drawing is mirrored by KiCad.

| Wire | Net | Color | Side | From | To | Straight length |
|---|---|---|---|---|---|---:|
| W01 | `GPIO3` | YELLOW | solder side | `B3` | `A3` | 2.5 mm |
| W02 | `GPIO3` | YELLOW | solder side | `A3` | `A11` | 20.3 mm |
| W03 | `GPIO3` | YELLOW | solder side | `A11` | `B11` | 2.5 mm |
| W04 | `BASE` | YELLOW | solder side | `E11` | `E18` | 17.8 mm |
| W05 | `BASE` | YELLOW | solder side | `E18` | `E20` | 5.1 mm |
| W06 | `+3V3` | YELLOW | solder side | `H6` | `I6` | 2.5 mm |
| W07 | `GND` | BLACK | solder side | `H7` | `I7` | 2.5 mm |
| W08 | `GND` | BLACK | solder side | `I7` | `I20` | 33.0 mm |
| W09 | `GND` | BLACK | solder side | `F18` | `I18` | 7.6 mm |
| W10 | `GND` | BLACK | solder side | `H20` | `I20` | 2.5 mm |
| W11 | `+5V` | RED | component-side jumper | `H8` | `J8` | 5.1 mm |
| W12 | `+5V` | RED | solder side | `J8` | `J21` | 33.0 mm |
| W13 | `IR_ANODE` | YELLOW | solder side | `F21` | `F23` | 5.1 mm |
| W14 | `IR_CATHODE` | YELLOW | solder side | `D18` | `C18` | 2.5 mm |
| W15 | `IR_CATHODE` | YELLOW | solder side | `C18` | `C24` | 15.2 mm |
| W16 | `IR_CATHODE` | YELLOW | solder side | `C24` | `G24` | 10.2 mm |
| W17 | `IR_CATHODE` | YELLOW | solder side | `G24` | `G23` | 2.5 mm |

## Component coordinates

| Ref | Value | Pin coordinates |
|---|---|---|
| U1 | XIAO ESP32-C3, 2x7 sockets | pin 2/D1/GPIO3=`B3`; pin 10/3V3=`H6`; pin 9/GND=`H7`; pin 8/5V=`H8`; all 14 pins represented |
| R1 | 470 ohm | 2/GPIO3=`B11`; 1/BASE=`E11` |
| Q1 | BC33740BU | 1/C=`D18`; 2/B=`E18`; 3/E=`F18` |
| R2 | 10 kohm | 1/BASE=`E20`; 2/GND=`H20` |
| C1 | 100 nF | 1/3V3=`I6`; 2/GND=`I7` |
| C2 | 100 nF | 2/GND=`I17`; 1/5V=`J17` |
| C3 | 100 uF | 2/GND=`I19`; 1/+5V=`J19` |
| R3 | 47 ohm / 0.6 W | 1/5V=`J21`; 2/IR_ANODE=`F21` |
| D1 | fresh TSAL6400 | 2/A=`F23`; 1/K=`G23` |
