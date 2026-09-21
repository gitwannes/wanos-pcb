<!-- --- file: docs/remotepcb.md --- -->

# Remote plant PCB — water meters + pipe temperatures (draft)

**Status:** design draft — not kicked off / not locked for implement.  
**Source:** consolidated from `remote PCB.txt` and architecture review.  
**Replaces:** cold & hot water pulse path on main **J4** → **U1** (YF-B6/B10). Adds four **DS18B20** pipe temperatures.

Canonical shipped water wiring today → [`field-wiring.md`](field-wiring.md) § 2a, [`io-expander-map.md`](io-expander-map.md) § 2. Working design note in `docs/` until behaviour is locked into the usual product homes on ship.

---

## 1. Intent

| Item | Decision |
|---|---|
| Role | One remote board near the bathrooms: **4× YF-B6** pulses + **4× DS18B20** pipe temps |
| Link to main | Single **Cat5 UTP ~6 m** → main **RJ45** (reuse designator **J4**) |
| I²C path | Main **J4** → **U5** TCA9548A channel **5** (`SD5` / `SC5`) @ **100 kHz** |
| Power | Main **`+5VA`** over Cat5 → remote **AP2112-3.3** for logic; YF-B6 VDD from remote **`+5VA`** |
| Interrupt | MCP23017 **INT** over Cat5 pair 4 → main PCB; **destination pin TBD** |
| Main J4 today | Current water RJ45 + `water_meters` front-end **removed**; label **J4** reused for this uplink |
| Expanders | Four water GPIOs leave **U1**; dropping a **PCA9554PW** is a separate ToDo (not automatic — § 9) |

---

## 2. System block

```
  Pi root I²C (R9/R10 2k2)
       |
       +-- U1 PCA9554 0x20  (doors / kWh; water P2–P5 removed after cutover)
       +-- U2 PCA9554 0x21  (buttons / 12 V mon)
       +-- U5 TCA9548A 0x70
       |      ch 0–4 : SHT31 plant (unchanged)
       |      ch 5   : NEW remote uplink (SD5/SC5) ---- Cat5 ~6 m ---- remote RJ45
       |      ch 6–7 : NC (unless reserved later)
       +-- J16 LCD (root, not muxed)

  Remote PCB:
       +5VA (from cable) -- TVS -- polyfuse(main) -- AP2112-3.3 -- DS2482-800 + MCP23017
       YF-B6 ×4  --> MCP23017 GPIOs (+ RC / TVS / activity LED)
       DS18B20 ×4 --> DS2482-800 1-Wire channels
       INT (OD) --> Cat5 pair 4 --> main (2k2 pull-up) --> TBD GPIO
```

---

## 3. Main PCB changes

### 3.1 Connector **J4** (redefined)

Remove today’s water-meter RJ45 function (four SIG + `+5VA` to YF over one Cat5 into **U1**).

New **J4** = uplink to remote PCB only:

| Net / pin group | Connection |
|---|---|
| **SDA** | **U5** channel **5** data (**`SD5`**) |
| **SCL** | **U5** channel **5** clock (**`SC5`**) |
| **`+5VA`** | Through **polyfuse** (new — see § 3.3) to jack |
| **GND** | Board GND (multiple returns on Cat5 — § 5) |
| **INT** | MCP23017 interrupt from remote; **2k2** pull-up to **`+3V3`** on main; **landing pin TBD** |

Jack: same class as current water **J4** preferred — TE **5556416-1** / Amphenol **54602**-class RJ45 TH, no magnetics, no jack LEDs (align with [`field-wiring.md`](../field-wiring.md) § 2a hardware).

**Pinout:** lock T568B table to match remote (§ 5). Do **not** use the old water SIG pin map.

### 3.2 Remove on-main water front-end

Drop with old **J4** water role:

- `water_meters.kicad_sch` channel parts (**R37–R44**, **C18–C21**, **D25–D29**, activity **D13–D16** / **R19–R22**, etc.)
- **U1** nets **P2–P5** water (`WM_B1_*` / `WM_B2_*`)

Doors (**J2/J3**) and kWh (**J6/J7**) stay on main unless a later remap consolidates expanders (§ 8).

### 3.3 Polyfuse on remote **`+5VA`** feed

Add a **dedicated polyfuse** on the main board between **`+5VA`** and **J4** pin **`+5VA`** so a short on the 6 m cable or remote does not take down the whole Pi rail.

- Value: **TBD** after power budget (§ 9) — start candidate class similar to other port protection (e.g. hundreds of mA, not the main **F1** 2 A).
- Keep bulk / ESD thinking at the jack (see checks: port TVS vs changing global **D1**).

### 3.4 INT landing (open)

TCA9548A does **not** mux INT. Pair 4 must land on a **named** input:

| Option | Notes |
|---|---|
| Free **Pi BCM** | Cleanest for edge IRQ in Linux; pick unused GPIO on **J40** |
| **U2** free pin (P3/P4/P5/P7) | Stays in expander world; U2 INT is NC today — would need polled GPIO or wire U2 INT |
| **U1** freed pin after water move | Same polling story as today’s PCA9554 |

**Lock before schematic:** BCM number or `EXP_*` net + interrupt strategy in WanOS.

### 3.5 Global **D1** note (from draft TXT)

TXT suggested replacing main **D1** `BZT52C5V6` with **SMF5.0A**. Treat as **open** — do not conflate:

- **D1** = whole-rail input OV shunt on `pi_power`
- Port clamp at **J4** = cable/remote fault / ESD (today water used **SMBJ5.0A** at jack)

Prefer a **port TVS** on the new **J4** `+5VA` (mirror old water **D29** idea) over silently changing **D1**. If **D1** changes, review leakage of a 5.0 V working-voltage TVS on a 5 V rail.

---

## 4. Remote PCB — electrical

### 4.1 Inputs / outputs

| Direction | Count | Device / path |
|---|---:|---|
| In | 4 | YF-B6 hall pulses → **MCP23017** GPIOs |
| In | 4 | DS18B20 → **DS2482-800** 1-Wire channels (4 of 8 used) |
| Out (uplink) | 1 bus | I²C SDA/SCL (+ INT, power, GND) over Cat5 to main **J4** / **U5 ch 5** |

### 4.2 Power

| Item | Spec |
|---|---|
| Cable feed | **`+5VA`** from main (post port polyfuse) |
| Local regulator | **AP2112-3.3** → **3.3 V** for DS2482-800 + MCP23017 (+ pull-ups / LEDs as designed) |
| YF-B6 VDD | Remote **`+5VA`** to meter reds (sensors need **DC 5–15 V**, min **~4.5 V**) — **must** be on JST pinouts |
| Input clamp | **ESD5Z6V0** (or reviewed equiv.) **`+5VA`** → GND at remote |
| Bulk / HF | **10 µF** + **100 nF** on **`+5VA`** at remote (main already has **100 µF** on rail) |
| Power LED | **Simple LED + series resistor** on **`+5VA`** (or 3V3) — **no** transistor / divider “4 V threshold” circuit |

### 4.3 ICs and addresses

| IC | Role |
|---|---|
| **DS2482-800** | 8-ch 1-Wire master (I²C) |
| **MCP23017** (prefer **A** die if sourcing) | 16-bit I/O expander |
| **AP2112-3.3** | LDO |

**I²C addresses for DS2482-800 and MCP23017 are TBD** (strap before schematic lock). Addressing hardware:

**DS2482-800**

| Item | Value |
|---|---|
| Address pins | Pin **11**, pin **10**, pin **9** |
| Formula | binary `0001 1 [11] [10] [9]` → base **`0x18`** |
| Selectable range | **`0x18`–`0x1F`** |

**MCP23017**

| Item | Value |
|---|---|
| Address pins | Pin **17**, pin **16**, pin **15** |
| Formula | binary `0100 [17] [16] [15]` → base **`0x20`** |
| Selectable range | **`0x20`–`0x27`** |

When **U5 ch 5** is selected, remote devices share the **same** I²C address space as root (**U1 `0x20`**, **U2 `0x21`**, **U5 `0x70`**, LCD backpacks). Final straps must avoid collisions (see § 9).

### 4.4 I²C

| Item | Spec |
|---|---|
| Speed | **100 kHz** (not 400 kHz) |
	in /boot/config.txt:
	```
	dtparam=i2c_arm=on,i2c_arm_baudrate=100000
	```
| Pull-ups | **2k2** on main root **R9/R10** only (same plant pattern as SHT31); **no** pull-ups on remote |
| Series | **22 Ω** on SDA and SCL **at remote** (damping) |
| Mux | Devices only visible when software selects **U5 channel 5** |

### 4.5 1-Wire

| Item | Spec |
|---|---|
| Pull-up | **2k2** to **`+3V3`** per **used** channel, close to DS2482-800 |
| Unused ch | No pull-ups on unused DS2482 channels |
| Probes | Mounting / paste / insulation / strain relief — § 7 |

### 4.6 Pulse inputs (per YF-B6 channel)

| Element | Value | Placement |
|---|---|---|
| Pull-up | **10 kΩ** → **`+3V3`** | IC side |
| Series | **470 Ω** | IC side |
| Debounce | **100 nF** to GND | IC side |
| TVS | **ESD5Z6V0** (or reviewed) SIG → GND | Sensor / connector side |
| Activity LED | LED + **1 kΩ** to **`+3V3`** | Prefer **IC side of series R** (see checks); draft TXT had LED on sensor side of 470 Ω |

Idle **HIGH**, pulse **LOW** (open-drain YF). Same logic family as current on-main water front-end (there: **330 Ω** series — optional align).

### 4.7 Decoupling / misc

- **100 nF** near each IC VCC  
- **10 µF** on **3V3** near DS2482 / MCP23017 cluster  
- MCP23017 INT: open-drain; **2k2** pull-up on **main** (not remote)

---

## 5. Cat5 UTP (~6 m)

Twisted-pair assignment (draft):

| Pair | Colors (T568B-oriented) | Signal |
|---|---|---|
| **1** | White/Green + Green | **SDA + GND** |
| **2** | White/Orange + Orange | **SCL + GND** |
| **3** | White/Blue + Blue | **`+5VA` + GND** |
| **4** | White/Brown + Brown | **MCP23017 INT + GND** |

Lock an 8P8C pin table (main **J4** ↔ remote RJ45) before fab — same wire both ends.

---

## 6. Physical (remote)

| Item | Draft |
|---|---|
| Size | **40 × 60 mm** |
| Connectors | **1× RJ45**; **8× JST** (4 pulse, 4 temp) |
| Placement | Short edge: RJ45. Opposite / long edge: JST row(s). Center: DS2482 + MCP23017 + AP2112 + passives per input group |
| Mech | 2–4 mounting holes with copper clearance; test pads; silkscreen per connector |
| Layout | Solid GND pour (esp. I²C / 1-Wire); short SDA/SCL RJ45 → ICs; ESD parts at connectors |

Density is tight — mechanical mock recommended before commit.

---

## 7. DS18B20 field mounting (operator notes)

- Thin thermal paste between probe and copper sleeve.  
- Spring must press sleeve firmly on pipe; clean paint/oxidation on contact patch.  
- Insulate sleeve + pipe (tape / Armaflex) against ambient.  
- Strain-relieve ~2 m leads.  
- Place on stable flow section — away from mixing, pumps, tight bends.

---

## 8. Software / WanOS impact

| Today | After cutover |
|---|---|
| Water pulses: **U1** P2–P5 via **J4** | Select **U5 ch 5**, then **MCP23017** GPIO / INT path |
| Pipe water temps | **New**: DS2482-800 + DS18B20 (not on current board) |
| Mux discipline | Always select ch 5 before remote I²C; do not leave conflicting assumptions vs SHT31 ch 0–4 |
| Legacy indices | Cold/hot WanOS idxs (WISC-era BCM map in [`gpio-interface.md`](gpio-interface.md)) need a new hardware backend |

Pulse counting: see § 10 (INTCAP is **not** a hardware counter).

---

## 9. To checks & remarks

Open items, risks, and recommendations. Resolve before kickoff lock / schematic.

### Architecture / main board

1. **Lock J4 8P8C pinout** (both ends) for SDA, SCL, `+5VA`, INT (if used), GND returns — replace old water colour table in product docs on ship.  
2. **Is INT needed / useful on the main PCB?** MCP23017 INT over Cat5 pair 4 costs a main GPIO (or wire-OR), pull-up, and software IRQ path. Alternatives: poll the expander when the mux channel is selected (no INT wire — free the pair for extra GND/`+5VA`/spare). Weigh: water edge rates (miss risk under Linux) vs kWh (slow pulses — INT likely low value) vs cabling/pin cost. If INT stays: lock destination (BCM vs expander pin) and IRQ vs poll-after-wake policy.  
3. **Is a polyfuse needed** on main `+5VA` → remote RJ45? Pros: cable short / remote fault does not collapse the whole Pi rail. Cons: extra drop, part, nuisance trip. Decide yes/no (and value if yes) after load estimate (YF + LDO + LEDs + ICs + cable); if two remotes, decide per port. Main **F1** alone may be enough — confirm explicitly.  
4. **Port TVS** on main J4 `+5VA` (SMBJ5.0A-class) vs changing global **D1** — decide explicitly; default recommendation = **port clamp**, leave **D1** unless a measured reason.  
5. **ToDo — dropping a PCA9554PW:** not automatic. Water leaving **U1** frees four pins only; doors + kWh still need an expander unless remapped (e.g. onto **U2** free pins). Decide later whether to consolidate or keep both chips.  
6. Confirm **U5 ch 5** (operator: SD5/SC5); keep ch 6–7 NC or reserve (second remote → likely ch 6).  
7. Update product docs on ship: [`field-wiring.md`](field-wiring.md), [`board-spec.md`](board-spec.md), [`io-expander-map.md`](io-expander-map.md), [`gpio-interface.md`](gpio-interface.md), [`component-selection.md`](component-selection.md).

### Addressing / bus

8. **TBD — DS2482-800 I²C address** in **`0x18`–`0x1F`** (pins 11/10/9; formula `0001 1 [11] [10] [9]`, base `0x18`).  
9. **TBD — MCP23017 I²C address** in **`0x20`–`0x27`** (pins 17/16/15; formula `0100 [17] [16] [15]`, base `0x20`). Must not collide with root when ch 5 is selected (**U1 `0x20`**, **U2 `0x21`**, LCD backpacks, etc.).  
10. Prefer **MCP23017A**; decide INTA/INTB mirror / which INT pin on the cable (only if INT is kept — see item 2).

### Power / sensors

11. Document **per-JST pinout**: pulse (SIG/GND/`+5VA` as needed) and temp (1-Wire/GND/`+3V3` or parasite — lock power mode).  
12. Confirm YF-B6 **red = remote `+5VA`**, black = GND, yellow = SIG.  
13. Cable IR drop at 6 m on pair 3: verify **≥ 4.5 V** at meters under max load.  
14. AP2112: EN tied, Cin/Cout per datasheet, thermal on 40×60.

### Pulse integrity

15. **kWh pulses ≠ water-flow pulses.** YF-B6: hall OD, supply 5–15 V, pull-up to **`+3V3`** into MCP is the current water story (~7–200 Hz possible). SDM72D-M (and similar): passive opto, wants **5–27 V** pulse rail, slow ~35 ms pulses — main-board target is pull-up to **`+5VA`**, not 3V3 alone ([`field-wiring.md`](field-wiring.md) § 2b). Do **not** assume one remote pulse front-end fits both; if a second remote carries kWh, lock a kWh-specific front-end (or prove 3V3 pull-up on the bench).  
16. Align series R with main heritage (**470 Ω** draft vs **330 Ω** on current water) — pick one (per sensor class if split).  
17. Move activity LED to **IC side** of series R (recommended) unless there is a reason to keep sensor-side.  
18. Harmonize SIG TVS family with main (**ESD5Z6V0** vs **PESD5V0S1BA**) for one BOM story if desired.  
19. **Pulse counting honesty:** MCP23017 has **no** pulse accumulator. INTCAP latches state at INT; Linux latency ≫ pulse period can **miss edges** under load. Accept best-effort for household 33–66 Hz, or plan stronger counting (MCU / counter IC). Do not claim INT “eliminates” missed pulses.  
20. Multi-channel INT: four meters can interrupt densely — ISR must drain / read GPIO carefully (or poll after wake). Moot if INT omitted (item 2).

### I²C / SI / schedule

21. **Priority schedule + bus speed — finetune.** With SHT31×5 + remote water (MCP + DS2482) + optional second remote (kWh ± temps), define WanOS order and periods, e.g.: (1) service water edges / read MCP when due, (2) kWh MCP, (3) DS18B20 conversions (slow), (4) SHT31 round-robin. Exclusive mux select only — never enable two remotes with identical addresses at once.  
22. **Is 100 kHz still best?** 100 kHz matches plant Cat5 + 2k2 pull-ups and is the safe default for ~6 m. 400 kHz only if scoped rise times on the **longest** remote stub still meet spec with margin — unlikely to be necessary for SHT31/temps; water pulse loss is dominated by **Linux/mux schedule**, not bit rate. Decide: stay 100 kHz vs try 400 kHz on root only / never on long stubs. Throughput fix = smarter polling priority, not faster I²C, until SI is proven.  
23. Scope **rise time** on remote SDA/SCL after first bring-up (~6 m + mux) at the chosen rate.  
24. Root-only 2k2 pull-ups through mux = same as SHT31 plant; acceptable if scoped OK.  
25. Unplug behaviour: if INT used, pull-up on main keeps line idle high; I²C NACK when remote absent — software must handle.

### Mechanical / process

26. **40×60** fit check: RJ45 + 8 JST + 3 ICs + per-channel RC/TVS/LED.  
27. Silkscreen: meter ID (B1 cold/hot, B2 cold/hot) + temp points.  
28. Pipeline: `triage` when ready to place a phase id; no KiCad until `kickoff` + `implement`.

### Cutover

29. Harness: old water Cat5 into main J4 vs new uplink + short tails from remote to meters/probes.  
30. WanOS: dual-path or hard cut; keep legacy idxs mapped to MCP23017 bits.  
31. Fab sequencing: main board rev that removes water front-end must ship with remote (or temporary dead water).

---

## 10. Design rationale (kept / corrected)

### 10.1 Power LED — simple LED (locked direction)

The transistor + divider “~4 V threshold” idea was never a real UVLO (turns on near ~1 V once Vbe conducts). **Replaced** by a normal LED + series resistor as a coarse “power present” indicator. Operational health remains “3V3 up + I²C responds.”

### 10.2 MCP23017 pulse sampling — acceptable with caveats

YF-B6 theoretical max ~200 Hz; household often ~33–66 Hz. RC cleans edges. INT + INTCAP can wake the Pi and help edge detection, but **software must still count edges** and **can miss pulses** if interrupt latency exceeds inter-edge time. Acceptable for non-billing household monitoring if risk is acknowledged; not a substitute for a hardware counter.

### 10.3 I²C over Cat5 — acceptable for this length

SDA/SCL each paired with GND, ~6 m, 100 kHz, 2k2 pull-ups, 22 Ω series at remote: same class as existing SHT31 plant runs. Validate on the bench; do not jump to 400 kHz.

---

## 11. Verbatim inbox

**2026-09-20** — operator (chat): remote I²C side connects to **U5**, replaces cold & hot water counters; main needs additional RJ45 (reuse **J4**); nets **`+5VA`**, GND, **SC5/SD5**, INT TBD; four outputs moved → possibly remove one PCA9554PW; add polyfuse; power LED = normal LED (drop transistor setup); consolidate TXT + review into this MD.

**Source file:** `docs/todo/remote PCB.txt` (kept as raw notes; this MD is the working summary).

---

## Related

- [`field-wiring.md`](field-wiring.md) — current J4 water + SHT31 mux  
- [`io-expander-map.md`](io-expander-map.md) — U1/U2/U5  
- [`gpio-interface.md`](gpio-interface.md) — software map  
- [`board-spec.md`](board-spec.md) — power / water / I²C  
- [`todo/pipeline.md`](todo/pipeline.md) — place via `triage` when scheduled  
