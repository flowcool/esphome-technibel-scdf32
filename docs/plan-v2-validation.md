# Technibel IR V2 — Step-by-step Validation Plan

## Context

### What exists

The Technibel SCDF32C5I air conditioner uses a proprietary 48-bit IR protocol at 38kHz,
not recognized by IRremoteESP8266. The protocol was fully reverse-engineered by capturing
frames from the original remote using an ESP32 + KY-022 TSOP receiver + ESPHome
`remote_receiver`. The result:

- `esphome/libraries/technibel_ir.h` — C++ IR frame builder (mode, temp, fan, power, checksum)
- `esphome/ir-technibel-clim.yaml` — ESPHome config with `remote_transmitter` and API service
- `docs/protocol.md` — full protocol documentation (frame structure, encoding, checksum formula)
- `docs/wiring.md` — hardware wiring (TSAL6400 + 2N2222 discrete circuit)
- `docs/control-strategies.md` — three installation strategies (A: external IR, B1: TSOP injection, B2: bus interception)

The protocol implementation is considered correct and stable. It will not be modified.

### What failed

The original prototype (ESP32 DevKit generic + 2N2222 + TSAL6400 on breadboard) never
reliably controlled the AC unit. Symptoms:

- IR LED invisible to smartphone camera (while the original remote IS visible)
- ESP32 DevKit lost its 5V output (3.3V still works)
- Multiple IR modules burned out
- Diagnosis: hardware chain failure (not software) — transistor pinout, wiring, or power issue

Root cause was never definitively identified because debugging was done blind (no logic
analyzer, mixed old/new components, breadboard contact issues).

### Available hardware

All components are now available:

| Component | Source | Qty | Status |
|---|---|---|---|
| Seeed XIAO ESP32-C3 | AliExpress (official Seeed store) | 3 | Received |
| Seeed XIAO ESP32-C6 | AliExpress | 1+ | Received |
| BC337-40 NPN (TO-92) | AliExpress | 100 | Received |
| TSAL6400 Vishay 940nm | AliExpress | 10+ | Received |
| USB Logic Analyzer 8ch 24MHz | AliExpress | 1 | Received |
| PCB FR4 double-sided (assorted) | AliExpress | 10 | Received |
| KY-022 / VS1838B IR receiver | Already owned | 1 | Working |
| Technibel original remote | Already owned | 1 | Working |
| Multimeter | Already owned | 1 | Working |
| Go Tronic GT1087 IR module | Go Tronic | 1 | Received |
| Resistors (47Ω, 470Ω, 330Ω, assorted) | Already owned + AliExpress | Many | Available |
| LED assortment (red, green, blue, yellow, white) | AliExpress | Kit | Received |
| Silicone wire 22/24 AWG (red, black, yellow) | AliExpress | 3×3m | Received |
| Soldering flux NC-559 | AliExpress | 1 | Received |
| Desoldering braid | AliExpress | 1 | Received |
| Headers male/female 2.54mm | AliExpress | Assorted | Received |
| Tact switches 6×6mm | AliExpress | 50 | Received |
| MB102 breadboard + power module | AliExpress | 2 | Received |
| Mouser reference components | Mouser | See `docs/bom-v2.md` | Received 2026-08-14 |

The Mouser order provides known-origin reference parts for the validation: Vishay
TSAL6400 emitters, onsemi BC33740BU transistors, the required resistors, decoupling
capacitors, reservoir capacitors, and conditional Schottky diodes. Exact manufacturer
and Mouser references are maintained in `docs/bom-v2.md`.

For every hardware gate, record only the component source needed to reproduce the
result: `Mouser`, `AliExpress`, or `legacy/unknown stock`. Prefer Mouser reference parts
for the main validation path. AliExpress or legacy parts remain useful for comparison
when diagnosing a failure; do not mix their results without recording the source.

Phases 2–9 are breadboard validation. Do not solder the validated Piste A circuit until
Phase 9 passes; soldering starts in Phase 10.

### Goals

1. **Piste A** — Validate external IR emission: ESP32 sends a frame, AC unit responds
2. **Piste B1** — Migrate to direct TSOP injection inside the AC unit (endgame)

Sequential: A first (proves protocol works end-to-end), then B1 (eliminates IR optics).
Piste A hardware is kept intact as a reference/fallback after B1 migration.

### Platform choice: XIAO ESP32-C3

Rationale:
- Seeed's own "XIAO IR Mate" product validates this exact use case (ESPHome + remote_transmitter + IR LED on GPIO3)
- ESPHome board: `seeed_xiao_esp32c3`, variant: `esp32c3`
- 5V pin available when powered via USB-C (USB voltage passthrough)
- RMT v2: 2 TX channels + 2 RX channels (dedicated), sufficient for IR TX
- Requires: `board_build.flash_mode: dio`, `logger.hardware_uart: UART0`
- GPIO3 (D1) for IR TX, GPIO4 (D2) for IR RX — proven by XIAO IR Mate

**IMPORTANT: ESP32-C3 GPIOs are NOT 5V-tolerant.** Maximum input voltage is 3.6V
(Espressif datasheet). This affects Phase 10 design — the GPIO must never be directly
exposed to a 5V signal line.

**Power budget**: the XIAO 5V pin is USB passthrough. WiFi produces current spikes
well above average draw. Use a USB power supply rated ≥500mA (not 200mA).
When powering from an internal AC rail, prevent simultaneous USB power (use a diode,
jumper, or explicit disconnect procedure before connecting USB for flashing/debug).

### Key constraint: protocol encoding is frozen

Frame encoding and checksum logic in `technibel_ir.h` do not change. Physical timing
constants may change only after an instrumented comparison with the original remote.
All other work is in YAML configuration and hardware.

---

## Plan: phases with gatekeepers

Each phase has a **gatekeeper** — a pass/fail test that must succeed before advancing.
If a gate fails, the failure action column tells you what to try. You never move forward
on a failed gate.

---

### Phase 1 — Flash a bare XIAO C3

**Goal**: prove the board boots, connects to WiFi, and responds on ESPHome API.

**Actions**:

1. Create `esphome/ir-technibel-clim-c3.yaml` — minimal config (WiFi + logger + API + OTA, NO IR yet)
2. Required boilerplate for C3:
   ```yaml
   esp32:
     board: seeed_xiao_esp32c3
     variant: esp32c3
     framework:
       type: arduino

   esphome:
     name: ir-technibel-clim
     friendly_name: Clim Séjour IR
     platformio_options:
       board_build.flash_mode: dio

   logger:
     level: DEBUG
     hardware_uart: UART0

   ota:
     - platform: esphome
       password: !secret ota_password
   ```
3. Flash via USB-C (first time only — OTA available after this)
4. Check ESPHome logs: boot OK, WiFi connected, API accessible

**Minimum ESPHome version**: 2024.6+ recommended for RMT v2 support on C3.

**Gatekeeper 1**:

| Test | Pass | Fail action |
|------|------|-------------|
| Board visible in ESPHome dashboard | Continue | Check USB cable, try another port, verify flash_mode: dio |
| Logs show "WiFi connected" | Continue | Check SSID/password in secrets |
| API accessible from HA | Continue | Check network, firewall |

---

### Phase 2 — GPIO toggle: prove the pin works

**Goal**: verify GPIO3 (D1) toggles correctly, with NO IR components. Just a visible LED.

**Actions**:

1. Solder female headers onto the XIAO C3 (so it can be removed from any PCB later)
2. Wire a **red visible LED** + **330Ω** between GPIO3 and GND (direct, no transistor)
   - I = (3.3V − 2.0V) / 330Ω ≈ 4mA — safe for any standard LED
   - Do NOT use 47Ω here — that resistor is sized for the TSAL6400 on a 5V rail
3. Add to YAML:
   ```yaml
   output:
     - platform: gpio
       pin: GPIO3
       id: test_gpio

   interval:
     - interval: 500ms
       then:
         - output.toggle: test_gpio
   ```
4. Flash and observe: red LED must blink at ~1Hz

**Gatekeeper 2**:

| Test | Pass | Fail action |
|------|------|-------------|
| Red LED blinks at ~1Hz | GPIO3 works | Try GPIO4 (D2), check solder joints |
| Multimeter GPIO3: alternates 0V ↔ 3.3V | Confirmed | Wrong pin number or dead pin |

After validation: remove the test YAML block (output + interval).

---

### Phase 3 — Power: confirm 5V rail

**Goal**: prove the XIAO 5V pin delivers ~5V when USB-C powered.

**Actions**:

1. Plug XIAO via USB-C to a good charger (≥500mA, ideally ≥1A)
2. Multimeter DC between 5V pin and GND
3. Load test: use a 100Ω resistor rated ≥0.5W (I=50mA, P=0.25W).
   Do NOT use 47Ω directly between 5V and GND: I=106mA, P=0.53W → exceeds ¼W rating.
   The real load test happens naturally in Phase 6 when the TSAL6400 circuit draws ~74mA.

**Gatekeeper 3**:

| Test | Pass | Fail action |
|------|------|-------------|
| Multimeter reads 4.8V – 5.2V | 5V rail OK | Try different USB-C cable, try stronger charger |
| Stable under load | Supply OK | Charger too weak |

---

### Phase 4 — Transistor: validate BC337-40 in isolation

**Goal**: confirm BC337-40 pinout and function BEFORE integrating into the circuit.

**Actions**:

1. Take a fresh onsemi BC33740BU from the Mouser reference lot
2. **Expected pinout** (flat face toward you, pins pointing down): E (left) – B (middle) – C (right).
   **However**: the reference printed on the component and the actual manufacturer's datasheet
   take precedence. If an AliExpress transistor is tested for comparison, record its
   source because its pinout or marking may differ.
3. Multimeter diode mode to identify Base (the pin that shows ~650mV to both others):

   | Red probe | Black probe | Expected (NPN) |
   |---|---|---|
   | Base | Emitter | ~600–700 mV |
   | Base | Collector | ~600–700 mV |
   | Any other combination | | OL (open) |

   This identifies Base reliably but does NOT distinguish Collector from Emitter.

4. **Switching test in both orientations** to confirm C vs E:
   - Orientation A: 3.3V → 470Ω → Base, 5V → **330Ω** → Red LED → pin X (presumed Collector), pin Y → GND
   - Orientation B: swap pin X and pin Y
   - Measure VCE (voltage between Collector candidate and Emitter candidate) in both orientations.
     The correct orientation gives lower VCE (deeper saturation, ~0.1–0.2V).
     Inverted orientation gives higher VCE (~0.5–1V) because the transistor operates in reverse mode.
   - If multimeter has hFE function: use it to confirm C/E directly

**Gatekeeper 4**:

| Test | Pass | Fail action |
|------|------|-------------|
| Diode mode: ~650mV from Base to both others | Base identified | Not NPN — discard, try another |
| Switching test: one orientation has VCE < 0.3V, the other > 0.5V | C/E confirmed | Both similar → try another transistor |
| LED OFF when Base disconnected | No leakage | Short circuit — discard transistor |

---

### Phase 5 — Full chain on breadboard: GPIO → BC337 → visible LED

**Goal**: prove the complete chain ESP → resistor → transistor → LED works with the toggle YAML.

**Wiring**:

```
XIAO C3              Circuit
─────────             ──────
5V  ──────[330Ω]───► Anode (+) RED LED ──► Cathode (−) ──► Collector BC337
GPIO3 ──[470Ω]──┬─► Base BC337
                │
              [10kΩ]   ← pull-down: keeps BC337 OFF during ESP32 boot
                │
GND  ◄──────────┴──── Emitter BC337
```

Notes:
- **330Ω** for visible LED test (I ≈ (5−2−0.2)/330 ≈ 8.5mA — safe for any 5mm LED)
- **10kΩ base-emitter pull-down**: ensures transistor stays OFF when GPIO floats at boot
- The 47Ω resistor is reserved for the TSAL6400 (Phase 6)

**Actions**:

1. Wire on breadboard with the **red visible LED** (NOT the TSAL6400 yet)
2. Restore the 1Hz toggle YAML from Phase 2
3. Red LED must blink through the transistor

**Gatekeeper 5**:

| Test | Pass | Fail action |
|------|------|-------------|
| Red LED blinks via transistor at 1Hz | Full chain OK | Multimeter on Base (~0.7V when ON), Collector (~0.2V when ON) |
| Collector voltage during ON: < 0.5V | BC337 saturates properly | Base resistor too high, or wrong C/E orientation |
| LED stays OFF at ESP32 boot (before GPIO init) | Pull-down works | Check 10kΩ connection |

---

### Phase 6 — Swap in TSAL6400

**Goal**: same circuit, same YAML, but replace visible LED with IR LED and use correct resistor.

**Actions**:

1. Replace red LED with a fresh TSAL6400 (anode = long leg toward resistor, cathode toward Collector)
2. Replace 330Ω with **47Ω** (I ≈ (5−1.35−0.2)/47 ≈ 74mA — within TSAL6400 100mA continuous max)
3. Toggle YAML still active at 1Hz
4. Verification methods (in order of preference):
   - a) Smartphone front camera: TSAL6400 should flash faintly (violet/white glow).
     First validate the camera can see IR: point the original Technibel remote at it.
     If the remote is visible but the TSAL6400 is not → LED problem.
     If neither is visible → camera filters 940nm, skip to electrical verification.
   - b) Electrical verification (primary proof): measure voltage across the 47Ω resistor
     during ON state. I = V_across_47Ω / 47. Expect ~3.4V → ~72mA.
     This proves the LED is conducting the correct current.
   - **Do NOT use KY-022 at this phase.** The KY-022/VS1838B is a demodulating receiver
     tuned to 38kHz. A 1Hz toggle (DC illumination) is not a 38kHz-modulated signal.
     The receiver may produce a transient but it is not a reliable proof of emission.
     Optical validation with KY-022 happens in Phase 7 with proper 38kHz carrier.

**Note on resistor rating**: 47Ω at 74mA = 0.26W. Marginal for a ¼W resistor at 500ms ON.
Use a ½W resistor, or move quickly to Phase 7 (modulated pulses, much lower duty cycle).

**Gatekeeper 6**:

| Test | Pass | Fail action |
|------|------|-------------|
| Smartphone sees TSAL6400 flash (camera pre-validated with remote) | IR LED emits | Swap LED polarity, try another TSAL |
| V across 47Ω ≈ 3.2–3.6V during ON | Current ~68–76mA, LED conducting | Wrong resistor value or 5V supply issue |

---

### Phase 7 — 38kHz carrier: remote_transmitter with NEC test

**Goal**: send a real modulated IR signal and capture it with the KY-022.

This test validates the **hardware IR chain** (GPIO → RMT → transistor → LED → optical path → receiver).
If NEC works, the hardware is validated. The Technibel protocol itself is validated separately in Phase 8.

**Actions**:

1. Remove toggle YAML, add `remote_transmitter` config:
   ```yaml
   remote_transmitter:
     id: ir_tx
     pin: GPIO3
     carrier_duty_percent: 50%
     non_blocking: false    # explicit — default is true in current ESPHome
     rmt_symbols: 96        # C3 has 96 symbols total (2 blocks of 48)
                            # Technibel frame = 99 raw values ≈ 50 RMT symbols
   ```
2. Add a test service:
   ```yaml
   api:
     services:
       - service: test_nec
         then:
           - remote_transmitter.transmit_nec:
               address: 0x1234
               command: 0x5678
   ```
3. Set up KY-022 sniffer on a **second board** (another XIAO, or the old ESP32 DevKit if 3.3V works)
   with the sniffer YAML adapted for the board
4. Place KY-022 facing TSAL6400 at ~5cm
5. Trigger `test_nec` from ESPHome dashboard (Developer Tools → Services)
6. Check sniffer logs: NEC frame must appear with address 0x1234, command 0x5678

**Logic analyzer verification** (parallel, safe on bench — no mains voltage involved):

- Connect channel 0 to GPIO3 (XIAO C3)
- Trigger test_nec
- In PulseView: verify 38kHz carrier modulation, correct NEC timing

**Gatekeeper 7**:

| Test | Pass | Fail action |
|------|------|-------------|
| KY-022 decodes NEC in logs | Hardware IR chain validated | Check carrier_duty_percent, try esp-idf framework |
| Logic analyzer shows 38kHz on GPIO3 | RMT works on C3 | Note exact error, check ESPHome version ≥2024.6, try esp-idf framework, verify no other component uses TX RMT channels |
| Range > 30cm from KY-022 | Sufficient for Piste A at close range | Add 2nd TSAL6400 in parallel (each with own 47Ω). 1m+ range is nice-to-have, not a gate. |
| Compiles without RMT error | Symbol allocation OK | Keep rmt_symbols: 96, check ESPHome version, check for conflicting RMT users |

**Optional**: test with GT1087 Go Tronic module as a secondary data point. However,
the GT1087 has its own unknown characteristics (input polarity, driver stage, LED spec)
that must be verified independently before drawing conclusions. It is NOT a drop-in
replacement for the discrete circuit — treat it as a separate experiment, not a control.

---

### Phase 8 — Technibel protocol: full frame comparison

**Goal**: send a real Technibel frame and compare it with the original remote.

**Actions**:

1. Activate the full YAML with `technibel_ir.h` include and `send_command` service:
   ```yaml
   esphome:
     includes:
       - ./libraries/technibel_ir.h
   ```
   Verify the `includes:` path resolves correctly in the dedicated VM's live ESPHome environment, not just in the repository.

2. Capture two frames with the KY-022 sniffer:
   - a) **Original remote**: COOL, 24°C, FAN AUTO
   - b) **ESP32 C3**: `send_command` with mode=COOL, consigne=24, fan=AUTO, t_amb=25

3. **Decoding procedure** (the sniffer outputs raw/Pronto, NOT hex bytes):
   - a) Capture the raw timing sequence from ESPHome logs
   - b) Strip the header pulse (6500µs mark + 3300µs space)
   - c) Classify each space: > 1500µs → bit 1, < 1500µs → bit 0
   - d) Group into 6 bytes, MSB first per byte
   - e) Display as hex: B0 B1 B2 B3 B4 B5
   - f) **Save both raw captures as validation artifacts** (paste into a file)

4. Compare the 6 bytes

**Expected frame** for COOL 24°C FAN_AUTO power_ON t_amb=25:

```
B0 = 0xD0  (fixed device address)
B1 = 0xAC  (COOL mode)
B2 = 0x28  (temp_hi=0x2 for 24°C, fan_lo=0x8 for AUTO)
B3 = 0xF8  (power ON)
B4 = 0x43  (fixed)
B5 = 0xAC  (checksum: reverse(reverse(0x28) + reverse(0xF8) + 25 - 23)
           = reverse(0x14 + 0x1F + 2) = reverse(0x35) = 0xAC)
```

**Oracle test frame: `D0 AC 28 F8 43 AC`**

**Comparing with the original remote** — the `t_amb` problem:

The remote uses its own temperature sensor, which won't be exactly 25°C.
A B5 difference must NEVER be accepted without explanation. Procedure:

1. From the remote's captured B5, reverse-compute t_amb:
   ```
   t_amb = (reverse(B5_captured) - reverse(B2) - reverse(B3) + 23) & 0xFF
   ```
2. Verify the result is an integer and physically plausible (15–40°C)
3. Re-generate B5 from this t_amb value — it must match the captured B5 exactly
4. Use this same t_amb in the ESP32's `send_command` and verify B5 matches

If step 2 gives an implausible value or step 3 doesn't match, there is a protocol
error — do not attribute it to "temperature difference".

**Gatekeeper 8**:

| Test | Pass | Fail action |
|------|------|-------------|
| B0–B4 identical between ESP32 and remote | Protocol encoding correct | Debug encoding (should not happen — code is frozen) |
| B5 from remote reverse-computed to plausible t_amb (15–40°C) | Checksum formula correct | Formula error — re-verify against protocol.md |
| ESP32 B5 matches remote B5 when using same reverse-computed t_amb | End-to-end checksum validated | Bit error — compare raw captures bit by bit |
| ESP32 frame matches oracle `D0 AC 28 F8 43 AC` (with t_amb=25) | Independent verification | Check t_amb value used |
| Timings within ±10% of remote | Acceptable by AC | Timing constants may be adjusted (see note below) |

**Note on `technibel_ir.h` freeze scope**: the frame builder (encoding, checksum) is frozen.
The timing constants (header/bit pulse/space durations) may be adjusted if instrumented
comparison shows they differ from the original remote by more than 10%. This is the only
permitted modification.

---

### Phase 9 — Live test on the AC unit: Piste A validation

**Goal**: the AC unit responds to an IR command from the ESP32.

**Actions**:

1. Position XIAO + TSAL6400 at ~30cm facing the AC receiver window
2. Send: COOL, 24°C, FAN AUTO, t_amb = actual room temperature
3. Observe: AC must beep and change mode
4. Test all 4 modes + OFF systematically:

| # | Command | Expected AC response |
|---|---------|---------------------|
| 1 | COOL 24°C FAN_AUTO | AC starts cooling, display shows 24°C |
| 2 | Change to 22°C | Display changes to 22°C |
| 3 | DRY mode | AC switches to dehumidification |
| 4 | FAN mode | AC switches to fan only |
| 5 | AUTO mode | AC switches to auto |
| 6 | OFF | AC turns off (beep, display off) |
| 7 | COOL 24°C again | AC turns back on |

5. **Frame repeat test**:
   - Capture the original remote with the sniffer: does it send 1 frame or 2-3 per button press?
   - If remote sends multiple frames: add repeat in the YAML service (send twice with 40ms gap)
   - If remote sends once: current implementation is correct

**Gatekeeper 9**:

| Test | Pass | Fail action |
|------|------|-------------|
| AC beeps on first command | **Signal received** | Move closer (5cm), add 2nd LED, check angle |
| All 4 modes + OFF work | **PISTE A VALIDATED** | Debug failing mode individually |
| ON/OFF works | Power control OK | Check B3 encoding (0xF8/0x08) |
| Temperature change works | Temp encoding OK | Check B2 hi nibble encoding |
| Repeat 10× without failure | Reliable | Check timing drift, power stability, frame repeats |

---

### Phase 10 — Preserve Piste A as reference

**Goal**: keep the validated Piste A hardware intact as fallback/reference.

**Actions**:

1. Solder the Piste A circuit onto a dedicated PCB FR4 (5×7cm):
   - Female headers for XIAO (replaceable)
   - BC337-40 with 10kΩ base-emitter pull-down
   - 47Ω (½W) + TSAL6400 (optionally 2× LEDs, each with own 47Ω)
   - 470Ω (base resistor)
   - 100nF ceramic decoupling cap near the XIAO
   - 100nF + 10–100µF near the IR driver
   - Power connector (JST-XH 2-pin or screw terminal)
2. Re-test: repeat Phase 7 (NEC) and Phase 9 (AC test)
3. Label and store — this is your known-good reference

This board is NOT installed inside the AC. It stays on the bench.

**Gatekeeper 10**:

| Test | Pass | Fail action |
|------|------|-------------|
| NEC test via KY-022: passes | Solder OK | Visual inspect, continuity test |
| Technibel AC test: passes | PCB validated | Reflow suspect joints |
| No abnormal heat after 10min | No short | Check for solder bridges |

---

### Phase 11 — AC unit inspection (power OFF)

**Goal**: open the AC indoor unit and identify the IR receiver and power rails, WITHOUT
connecting any instruments yet.

**SAFETY**: Do NOT connect any instruments (logic analyzer, oscilloscope, multimeter
ground clip) to the AC PCB at this stage. This phase is visual inspection only.

**Actions**:

1. **Cut power to the AC unit** at the breaker
2. Open the indoor unit cover
3. **Photograph everything** before touching anything
4. Locate the internal IR receiver (small black 3-pin component)
5. Note the component marking (e.g., TSOP38438, TSOP4838, VS1838B, etc.)
6. Identify the 3 pins from the datasheet: VCC, GND, Signal
7. Trace the Signal pin to the AC main MCU (follow the PCB trace visually)
8. Identify potential power rails (look for markings: +5V, +12V, GND, VCC)
9. Look for an isolation boundary on the PCB (transformer, optocoupler, creepage gap)
   between mains-side and logic-side

**Gatekeeper 11**:

| Test | Pass | Fail action |
|------|------|-------------|
| TSOP component identified + reference noted | Continue | Look harder — may be hidden behind a panel |
| 3 pins identified from datasheet | Continue | Unknown component — photograph and research |
| Power rail markings found | Continue | No markings — will need probing in Phase 12 |
| Isolation boundary identified or reasoned about | Continue | See Phase 12 safety gate |

---

### Phase 12 — Electrical safety verification

**Goal**: determine whether the AC logic board's ground is safely isolated from mains
BEFORE connecting any USB-connected instrument (logic analyzer, PC, oscilloscope de table).

**WHY THIS MATTERS**: some appliance power supplies have logic referenced to mains
(non-isolated SMPS). Connecting a USB logic analyzer (which shares ground with your PC
and potentially mains earth) to a non-isolated GND can cause short circuits, equipment
damage, or electric shock.

**Method**: inspection-first, documentation-second, resistance measurement only as a
supporting check. A standard multimeter cannot certify galvanic isolation or insulation
integrity. Do not perform live measurements between logic and mains as part of this plan.

**Step 1 — Inspection (AC unit powered OFF and breaker locked OFF)**:

Wait at least the discharge time specified by the service manual. In the absence of a
service manual, waiting 5 minutes is a precaution, not proof that every capacitor is
discharged. Do not touch or probe the primary-side power supply section.

1. Photograph the AC unit's main PCB power supply section
2. Identify the power supply topology:
   - Look for a **transformer** (mains-side isolation component). A visible transformer
     with separate primary/secondary windings = strong evidence of isolation.
   - Look for **optocouplers** (feedback isolation for the voltage regulator)
   - Look for a **creepage gap** — a visible slot or unmilled area on the PCB separating
     the mains side from the logic side. Many isolated SMPS designs have this.
   - Note component references: the SMPS IC reference can confirm isolated vs non-isolated topology
3. If a clear isolation boundary is visible, identify every conductor crossing it
   (transformer, optocoupler, safety capacitor, connector, shield or mounting hardware)
   and confirm the power-supply topology from component datasheets or the service manual.
   Then proceed to Step 2 for a supporting check.
4. If no isolation boundary is found, or if the topology is unclear:
   → **treat the logic as mains-referenced. Do NOT proceed to voltage measurements.**

**Step 2 — Resistance check (AC unit powered OFF, breaker OFF, caps discharged)**:

1. Set multimeter to resistance mode (MΩ range)
2. Measure between:
   - AC board logic GND and mains PE (earth) terminal on the AC unit's terminal block
   - AC board logic GND and mains L terminal
   - AC board logic GND and mains N terminal
3. Readings from logic GND to L and N should normally be > 1MΩ (often open/OL).
   A lower reading is a stop condition until its path is understood. Logic GND to PE
   may be low in an intentionally earth-bonded isolated secondary, but that bond must
   be traced and documented rather than treated automatically as a failure. An OL reading is only supporting
   evidence: a DMM uses a low test voltage and cannot prove insulation strength, and
   safety capacitors may appear open in a DC resistance test.

**Gatekeeper 12**:

| Test | Pass | Fail action |
|------|------|-------------|
| Isolation boundary and every crossing conductor identified | Strong isolation evidence | Unclear topology → treat as non-isolated |
| Datasheet/service information confirms an isolated secondary | Architecture confirmed | No confirmation → treat as non-isolated |
| Resistance logic GND to L and N: both > 1MΩ | Supporting check passes | ≤1MΩ or unstable reading → **STOP and explain the path** |
| Logic GND to PE measured and any low-resistance bond explained | Earth relationship known | Unexplained path → **STOP** |
| Architecture confirmed AND supporting check passes | Eligible for low-voltage USB probing | Either condition missing → no USB instrument |

**If isolation is NOT confirmed**:

- **Do NOT connect** PC, USB logic analyzer, or bench oscilloscope to the AC board.
- All subsequent measurements require **genuinely isolated equipment**: a differential
  probe rated for the voltage category (CAT II minimum for appliance internals),
  or a battery-powered oscilloscope whose inputs, probes, enclosure and connectors
  are rated for the expected voltage. "Battery-powered" alone is not sufficient —
  the probe and input ratings must match the hazard.
- **Consider engaging a qualified electrician** to verify the supply topology.
- If isolation cannot be established, continue with Piste A (external IR). B1 is halted
  unless a qualified person designs a complete galvanically isolated interface and
  isolated power solution. A common-ground BC337 interface is forbidden in that case.

---

### Phase 13 — TSOP signal characterization

**Goal**: probe the TSOP output signal and determine the output stage architecture.

**Prerequisites**: Phase 12 passed (isolation confirmed), or isolated measurement equipment
rated for the voltage category.

**Part A — Signal capture with logic analyzer**:

1. Connect logic analyzer GND to AC board GND (safe only if Phase 12 passed)
2. Connect logic analyzer channel 0 to TSOP Signal pin
3. Power on the AC unit
4. Send a command with the **original remote**
5. Capture and note:
   - Idle state (HIGH or LOW?)
   - Active state during IR reception
   - Timing — compare with Phase 8 captures

This tells us polarity and timing. It does NOT reliably tell us the output type
(open-collector vs push-pull). A logic analyzer shows voltage levels but cannot
distinguish between "actively driven HIGH" and "pulled HIGH through a resistor".

Before connecting channel 0, verify the analyzer's absolute maximum input voltage and
logic thresholds from its actual documentation. If the signal may exceed that rating,
use a correctly calculated divider or buffer. "24 MHz USB logic analyzer" does not by
itself imply 5V-tolerant inputs.

A digital logic analyzer does not measure analog amplitude. Measure receiver VCC and
the idle HIGH voltage separately with a suitable multimeter or oscilloscope only after
Phase 12 has passed; do not infer 3.3V versus 5V from the analyzer trace display.

**Part B — Output type determination (in order of reliability)**:

1. **Datasheet** (best): identify the exact receiver reference from Phase 11 and read
   its output-stage description or internal block diagram. Do not infer the architecture
   from a similar-looking TSOP38xxx or VS1838B clone.

2. **PCB inspection** (if datasheet insufficient): examine the circuit around the
   TSOP output pin on the AC board (AC unit OFF, caps discharged):
   - Is there an external pull-up resistor between Signal and VCC? → supports, but does
     not prove, an open-collector/open-drain hypothesis
   - Is there a series resistor between Signal and the MCU input? → common with push-pull
   - Is the trace direct from TSOP to MCU? → likely push-pull, relying on TSOP's driver

3. **Resistance measurement** (AC unit OFF, caps discharged, component in-circuit):
   - Measure resistance from TSOP Signal pin to VCC: if you read a discrete value
     (1kΩ–100kΩ), there may be an external pull-up or another parallel path.
   - If you read very high/OL, no external pull-up has been demonstrated.
   - Caveat: in-circuit resistance includes parallel paths through the MCU input.
     Use this as supporting evidence, not definitive proof.

**Gatekeeper 13**:

| Test | Pass | Fail action |
|------|------|-------------|
| Signal visible on logic analyzer during remote command | Signal pin correct | Wrong pin — re-check |
| Idle = HIGH, marks = LOW (active-low) | Standard TSOP behavior | Note actual polarity for firmware config |
| Receiver VCC and idle HIGH measured with suitable instrument | Level known | Unexpected level — investigate |
| Timing matches reverse engineering captures | TSOP = demodulated protocol | Different timing — re-analyze |
| Output type determined (datasheet or inspection) | Architecture known | If still ambiguous, assume push-pull (safer assumption for circuit design) |

---

### Phase 14 — B1 interface circuit design (measurement-driven)

**Goal**: choose the correct injection circuit based on actual measurements from Phase 13.

**The ESP32-C3 GPIO is NOT 5V-tolerant** (max 3.6V per Espressif datasheet).
The GPIO must NEVER be directly connected to a line that can reach 5V, regardless of
open_drain mode (open_drain prevents driving 5V, but does not prevent receiving 5V —
ESD protection diodes inside the chip will conduct and damage it).

**Interface A — only if the receiver output is confirmed open-collector/open-drain:**

Use a BC337 as an additional open-collector level shifter.

```
ESP32 GPIO3 ──[470Ω]──┬── Base BC337
                       │
                     [10kΩ]  ← pull-down (OFF at boot)
                       │
GND ──────────────────┴── Emitter BC337

TSOP Signal line to AC MCU ── Collector BC337
```

The BC337 acts as an external open-collector output:
- GPIO HIGH → BC337 conducts → Collector pulled LOW (mark)
- GPIO LOW → BC337 off → Collector floats, pulled HIGH by existing circuit
- No voltage from the AC signal line ever reaches the ESP32 GPIO
- The collector can interface with a 3.3V or 5V pulled-up signal, within BC337 ratings
- This does not provide galvanic isolation; ESP32 and AC logic grounds are common

**Firmware**:

```yaml
remote_transmitter:
  pin:
    number: GPIO3
    inverted: false       # NOTE: BC337 inverts the signal (GPIO HIGH → line LOW)
                          # so inverted must be set based on testing — see below
  carrier_duty_percent: 100
  non_blocking: false
  rmt_symbols: 96
```

**Determining `inverted`**: The BC337 adds a logical inversion.
- TSOP mark = signal line LOW. We want marks to pull the line LOW.
- GPIO HIGH → BC337 on → line LOW = mark. So GPIO HIGH = mark.
- In ESPHome, mark = the "active" state. With `inverted: false`, mark = HIGH.
- Therefore: start with `inverted: false`. If the AC doesn't respond, try `inverted: true`.

**Coexistence with original remote**:

If TSOP output is **open-collector**: no modification needed. The TSOP and BC337
both sink on the same line; pull-up provides HIGH. Both can pull LOW independently.

If the receiver output is **push-pull**, do not connect the BC337 collector directly
to the intact line: the receiver actively drives HIGH when idle and would contend with
the BC337 during marks. Required approach:
- Cut the trace between TSOP output and MCU input
- Insert both sources through diodes into the MCU input with a pull-up (wired-OR)
- The exact topology depends on PCB layout — decide after Phase 13 measurements

**Gatekeeper 14**:

This phase produces a design decision, not a test result.

| Decision | Based on |
|----------|----------|
| TSOP VCC = 3.3V or 5V | Phase 13 measurement |
| TSOP output type: OC or push-pull | Phase 13 analysis |
| Need to cut TSOP trace? | Yes if push-pull and coexistence required |
| Pull-up needed? | Yes if OC, or if trace cut |
| Final schematic drawn and reviewed | Before any soldering |

---

### Phase 15 — B1 bench test

**Goal**: validate the injection circuit BEFORE permanent installation.

**Power safety**: this phase is authorized only after Phase 12 has confirmed an isolated
low-voltage logic domain. A floating USB charger or battery-powered laptop does not make
a mains-referenced common ground safe; connecting it can raise the XIAO, USB connector,
laptop chassis and programming cable to a hazardous potential.

- Use a dedicated, reputable USB charger with no PC data connection during the test.
- Do not connect a desktop PC, laptop or USB logic analyzer while the B1 common-ground
  interface is attached to the AC.
- If Phase 12 did not pass, do not perform this phase with the BC337 circuit. Return to
  Piste A or obtain a reviewed galvanically isolated interface and isolated power design.

If the XIAO needs OTA flashing during this phase, flash first via the safe USB source
(charger + WiFi OTA), then disconnect USB and power from the charger only.

**Actions**:

1. Build the B1 circuit on a small PCB (separate from Piste A board)
2. Use a second XIAO C3 (keep Piste A hardware intact on the first one)
3. Flash the B1 YAML via USB before connecting to the AC
4. Power the XIAO from a dedicated USB charger (no PC connection)
5. Connect: BC337 collector → AC TSOP signal line, common GND
6. Test all 4 modes + OFF
7. Verify the original remote still works

**Gatekeeper 15**:

| Test | Pass | Fail action |
|------|------|-------------|
| AC responds to injected command | Injection works | Check inverted, polarity, BC337 orientation |
| Original remote still works | Coexistence OK | Contention — need trace cut / wired-OR |
| All 4 modes + OFF work | **B1 INJECTION VALIDATED** | Debug mode by mode |
| AC boots normally after ESP32 power cycle | No boot glitch | Check 10kΩ pull-down |

---

### Phase 16 — Permanent installation study

**Goal**: design the permanent installation inside the AC unit.

**Actions**:

1. Identify power source:
   - Internal 5V rail with ≥500mA headroom → connect to XIAO 5V pin via Schottky diode
     (prevents backfeed from USB during debug sessions)
   - 12V only → add buck 12V→5V module
   - Nothing → external USB power (Piste A style)

2. **Dual-power protection**: if using internal AC power AND occasionally connecting USB for
   reflash/debug, add a Schottky diode (e.g., SS14) between internal 5V and XIAO 5V pin
   (cathode toward XIAO). This prevents current flowing from USB back into the AC rail.
   Alternatively, use a jumper or switch to disconnect internal power before plugging USB.

3. Mechanical integration requirements:
   - Insulating enclosure or standoffs (no exposed copper traces)
   - Locked connectors (not just friction-fit headers) for permanent install
   - Strain relief on all wires
   - Distance from mains wiring, motors, moving parts
   - Distance from condensate tray and condensation zones
   - Temperature check at chosen location (ESP32 max ambient: 85°C, but WiFi degrades above ~60°C)

**Gatekeeper 16**:

| Test | Pass | Fail action |
|------|------|-------------|
| Power source identified and tested | Continue | Fall back to external USB |
| No simultaneous USB+internal power possible | Safe | Add diode or disconnect mechanism |
| Mounting location chosen, photographed | Continue | Reconsider location |
| Temperature at location < 50°C during AC operation | Continue | Move board further from heat source |

---

### Phase 17 — Long-term validation

**Goal**: prove reliability over time.

**Actions**:

1. Install B1 board permanently
2. Test cycle:
   - 24h continuous operation: send commands every hour, verify AC responds
   - Power cycle the AC: verify ESP32 reconnects and AC doesn't glitch
   - Simultaneous remote use: verify no interference
   - WiFi disconnection/reconnection: verify recovery
   - Several days of normal operation

**Gatekeeper 17**:

| Test | Pass | Fail action |
|------|------|-------------|
| 24h, no missed commands | Reliable | Check WiFi, power, watchdog |
| AC power cycle: ESP32 recovers | Boot OK | Check GPIO pull-down, OTA |
| Remote coexistence: no conflicts | Coexistence OK | Review wired-OR / trace cut |
| 1 week normal use | **INSTALLATION COMPLETE** | Investigate intermittent issues |

---

## Phase summary

| Phase | Goal | Key gatekeeper | Blocking |
|-------|------|-----------------|----------|
| 1 | XIAO C3 boots | WiFi + API OK | Yes |
| 2 | GPIO toggles | Red LED blinks (330Ω) | Yes |
| 3 | 5V available | Multimeter 4.8–5.2V | Yes |
| 4 | BC337 validated | Switching test both orientations | Yes |
| 5 | Chain GPIO→transistor→visible LED | Red LED blinks via BC337 | Yes |
| 6 | IR LED emits | V across 47Ω confirms ~72mA, smartphone sees flash | Yes |
| 7 | 38kHz carrier works | KY-022 decodes NEC | Yes |
| 8 | Technibel frames match remote | Decoded bytes match oracle `D0 AC 28 F8 43 AC` | Yes |
| 9 | AC responds + frame repeat test | Beep + all 4 modes + OFF | Yes |
| 10 | Piste A soldered as reference | Same tests pass on PCB | Recommended |
| 11 | AC unit visual inspection | TSOP identified, photographed | Yes |
| 12 | Electrical safety verification | Isolated architecture confirmed + resistance check supports it | Yes |
| 13 | TSOP signal characterized | Polarity, amplitude known; output type from datasheet | Yes |
| 14 | B1 circuit designed from measurements | Schematic reviewed (BC337 level shifter) | Yes |
| 15 | B1 bench test (only on confirmed isolated logic) | AC responds via injection | Yes |
| 16 | Permanent install designed | Power, mechanical, thermal OK | Yes |
| 17 | Long-term validation | 1 week stable operation | Yes |

## Files to create or modify

| File | Action | Phase |
|------|--------|-------|
| `esphome/ir-technibel-clim-c3.yaml` | Create — XIAO C3 config | 1 |
| `esphome/ir-clim-sniffer-c3.yaml` | Create — sniffer for 2nd XIAO (if needed) | 7 |
| `docs/wiring.md` | Update — add XIAO C3 wiring section, fix old diode schematic | 5 |
| `docs/bom.md` | Update — add XIAO C3, BC337-40, decoupling caps, pull-down resistor | 1 |
| `docs/control-strategies.md` | Update — make B1 interface conditional and remove direct GPIO injection | 14 |
| `esphome/ir-technibel-clim.yaml` | Keep as-is — ESP32 DevKit reference | — |
| `esphome/libraries/technibel_ir.h` | **DO NOT TOUCH** | — |

## Rollback strategy

- Each phase is independent: failure returns to previous phase
- Original ESP32 DevKit YAML preserved unchanged
- `technibel_ir.h` never modified
- Piste A hardware preserved intact on its own PCB (Phase 10) as known-good reference
- Piste B1 rollback: if no trace was cut, disconnect the BC337 collector wire from the
  TSOP signal line. If a trace was cut, re-bridge it with a wire. Document the exact
  rollback procedure when the B1 circuit design is finalized (Phase 14).
- XIAO C3 on female headers: replaceable in 30 seconds
