<!-- --- file: docs/remotepcb.md --- -->

# Remote plant PCB — universal pulse + 1-Wire

**Status:** schematic **v0.1** in [`projects/wanos-remote/`](../projects/wanos-remote/). **Next (operator):** clean schematic pin attachments + run ERC + check vs this doc — pipeline **Ops-Remote1**. **No layout yet.** Main carrier layout (**L1**) follows remote schematic check; main PCB *cutover* changes still after remote bring-up.  
**Role:** universal remote module — **4×** opto pulse inputs + **4×** DS18B20 (1-Wire). Same PCB for water and kWh instances.

Today’s main-board water / kWh wiring → [`field-wiring.md`](field-wiring.md), [`io-expander-map.md`](io-expander-map.md).

---

## 1. Intent

| Item | Spec |
|---|---|
| Channels (PCB) | **4×** universal pulse + **4×** DS18B20 footprints (4 of 8 DS2482 channels brought out) |
| Instances | **2×** identical remotes |
| Remote **#1** | **4×** water flow + **2×** pipe temp (2× temp JST unused) |
| Remote **#2** | **2×** kWh S0 + **1×** temp (2× pulse + 3× temp JST unused) |
| Link | **Cat5 UTP ~6 m** → main **RJ45** (#1 reuses **J4**; #2 = second RJ45 on main later) |
| I²C | **U5** TCA9548A — #1 on **ch 5**, #2 on **ch 6** @ **100 kHz** |
| Power | Main **`+12V`** → Cat5 → remote **VIN** → **AP2204K-3.3** → **3V3**; filtered **`S0_RAIL`** for opto + power LED |
| VIN at remote | Target ≈ **12 V**; **minimum 11.5 V** after cable / PPTC (plant supply may be raised to achieve this) |
| 12 V loss | Remote offline when plant 12 V is down (Pi may still run on 5 V) |
| Field connectors | **4× JST 3-pin** pulse + **4× JST 3-pin** temp; uplink **RJ45** |
| Activity LEDs | **4×** + **1×** SMD button (LEDs lit only while pressed) |
| Power LED | Always on from **`S0_RAIL`** |
| MCP INT | **Not used** — no INT wire; WanOS **polls** when mux channel selected |
| MCP GPIO | **GPA0–GPA3** = pulse ch 1–4; remaining GPIO **no nets** (firmware: outputs LOW) |
| DS2482 IO | **IO0–IO3** → temp J6–J9; **IO4–IO7** **NC** (do not tie to GND) |
| VIN TVS | **SMBJ12A** on remote **VIN→GND** at RJ45 (in addition to main port TVS) |
| KiCad project | [`projects/wanos-remote/`](../projects/wanos-remote/) (create on implement) |
| Bring-up | Remote first on **12 V lab supply**; main PCB changes after |

---

## 2. System block

```
  Pi root I²C (R9/R10 2k2)
       |
       +-- U1 PCA9554 0x20  (doors; water/kWh removed after remotes cut over)
       +-- U2 PCA9554 0x21  (buttons / 12 V mon)
       +-- U5 TCA9548A 0x70
       |      ch 0–4 : SHT31 plant (unchanged)
       |      ch 5   : remote #1 (water)  ---- Cat5 ---- RJ45
       |      ch 6   : remote #2 (kWh)    ---- Cat5 ---- RJ45
       |      ch 7   : NC / spare
       +-- J16 LCD (root, not muxed)

  Main per uplink: +12V (plant) -- PPTC -- SMBJ12A -- Cat5 ---- remote VIN

  Remote PCB (identical hardware both instances):
       VIN (≥11.5 V, nom ~12 V) -- input filter
            |-- AP2204K-3.3 --> +3V3 --> DS2482-800 + MCP23017A + logic
            |-- R_S0 / C_S0 --> S0_RAIL --> R_LED ×4 --> TLP281-4
            |                              --> power LED + series R
       Field JST 3-pin ×4 pulse --> S0_RAIL / SIG / GND
       Field JST 3-pin ×4 temp  --> +3V3 / 1-Wire / GND
       (MCP INT pin: NC on board / no Cat5 pair — poll only)
```

---

## 3. Main PCB changes (after remote)

### 3.1 Connectors

| Jack | Role |
|---|---|
| **J4** (redefined) | Uplink remote **#1** → **U5 SD5/SC5** + **`+12V`** + GND |
| Second RJ45 (designator TBD) | Uplink remote **#2** → **U5 SD6/SC6** + **`+12V`** + GND |

Remove today’s water-meter **J4** function (four SIG + `+5VA` into **U1**).  
Jack class: TE **5556416-1** / Amphenol **54602**-class RJ45 TH, no magnetics, no jack LEDs.  
Do **not** put **`+5VA`** on these uplinks. Pair map → § 5 (no INT).

### 3.2 Remove on-main front-ends (cutover)

- Water: drop `water_meters` parts; **U1** **P2–P5**  
- kWh: drop **J6/J7** front-ends; **U1** **P6/P7** when remote #2 is live  
- Doors (**J2/J3**) stay on main for now unless later remapped  

### 3.3 Port protection (locked)

Per remote RJ45 on main:

| Part | Role | Spec |
|---|---|---|
| **PPTC** | Overcurrent | TECHFUSE **`nSMD050-33V`** (LCSC **C70077**) — **500 mA** hold, **1 A** trip, **33 V** max, 1206, R≈150 mΩ |
| **SMBJ12A** | Port **TVS** | **`+12V`** → GND at jack |

Order: plant **`+12V`** → **PPTC** → jack (TVS at connector).

Remote load ≪ 150 mA; **500 mA** hold avoids nuisance trips; **33 V** rating has margin on 12 V (do **not** reuse typical 6–8 V 1206 PPTCs). Drop ≈ **15 mV** at 100 mA.

### 3.4 No INT landing

MCP23017 **INT** not brought to main. No GPIO / pull-up reserved for remote IRQ.

### 3.5 Rail clamps

Port **SMBJ12A** on each uplink **`+12V`**. Do not conflate with Pi **5 V** clamp (**D1**).

---

## 4. Remote PCB — electrical

### 4.1 I/O

| Direction | Count | Path |
|---|---:|---|
| In | 4 | Universal pulse → **TLP281-4** → **MCP23017A** |
| In | 4 | DS18B20 → **DS2482-800** (4 of 8 ch brought out; populate as needed) |
| Uplink | 1 | I²C + **`+12V`** + GND over Cat5 (**no INT**) |

### 4.2 Power

**Cable:** **`VIN` ≥ 11.5 V**, nominal ~**12 V** = main **`+12V`** after PPTC + Cat5 (raise plant PSU if needed).

**VIN clamp (remote):** **SMBJ12A** **VIN → GND** at RJ45 entry (same class as main port TVS). Does not replace main PPTC/SMBJ; local protection for lab bring-up and cable ESD.

#### 4.2.1 **3V3** — **AP2204K-3.3**

```
VIN (11.5–13 V class) → AP2204K-3.3 → +3V3
```

| Item | Spec |
|---|---|
| Part | **AP2204K-3.3** (SOT-23-5), e.g. **AP2204K-3.3TRG1** |
| Vin | **2.3–24 V** (11.5 V min is fine) |
| Iout | **150 mA** |
| EN | Tie to **VIN** (always on) |
| Cin | **47–100 µF** electrolytic + **100 nF** ceramic |
| Cout | Per datasheet (≥ **2.2 µF** ceramic) + **22–47 µF** bulk; **100 nF** at each IC |

Dissipation at ~50 mA ≈ **0.44 W** — copper under SOT-23-5. Activity LEDs gated so continuous load stays low.

#### 4.2.2 **`S0_RAIL`**

```
VIN → R_S0 (10 Ω) → S0_RAIL →|| C_S0 (10 µF + 100 nF) → GND
                              └→ R_LED ×4 → TLP281-4 anodes
                              └→ power LED + series R
```

| Ref | Value | Role |
|---|---|---|
| **R_S0** | **10 Ω**, 1%, 0.125 W | Soft RC with **C_S0**; limits HF dump into rail |
| **C_S0** | **10 µF** + **100 nF** | Bulk + HF at opto / power LED |

Drop at 4× ~2.3 mA ≈ **0.1 V** across **10 Ω** — fine. Keep **C_S0** and LED returns close to the TLP281-4; star field GND away from digital return.

Used for **R_LED**, pulse JST pin 1 (**VDD** / loop supply), and **power LED**.

#### 4.2.3 No remote 5 V rail

YF-B6 VDD (**5–15 V**) = **`S0_RAIL`** on the pulse JST.

#### 4.2.4 Power LED (always on)

From **`S0_RAIL`** — shows plant loop supply present (tracks opto / meter domain).

| Item | Spec |
|---|---|
| Series R | **4.7 kΩ**–**6.8 kΩ** (brightness class vs main **R30** on `+12V`) |
| Gating | **Not** gated by test button |

### 4.3 ICs and addresses (**locked**)

| IC | Role | I²C addr |
|---|---|---|
| **TLP281-4** | Quad optocoupler | — |
| **DS2482-800** | 1-Wire master | **`0x18`** (AD2/AD1/AD0 = 0) |
| **MCP23017A** | I/O expander | **`0x22`** (A2/A1/A0 strapped; avoid `0x20`/`0x21`) |
| **AP2204K-3.3** | 12 V → **3V3** | — |

Same straps on **both** remotes. Safe because only one of **U5 ch 5 / ch 6** is enabled at a time.  
**Never** enable ch 5 and ch 6 together (same addresses → bus fight).

**MCP23017A:** order **A** die (SOIC-28); avoid unmarked legacy **MCP23017**.  
**INTA/INTB:** **NC**.  
**Address straps for `0x22`:** A2=0, A1=1, A0=0 (hard-tie).  
**GPIO:** **GPA0–GPA3** → `PULSE_CH1`–`PULSE_CH4`; other GPA/GPB pins **no copper nets** (init as outputs LOW in firmware).

**DS2482-800:** AD2/AD1/AD0 = 0 → **`0x18`**. **IO0–IO3** → temp JST data; **IO4–IO7** leave **unconnected** (1-Wire open-drain ports — do **not** tie to GND).

Address formulas (reference): DS2482 `0001 1 [11][10][9]` → `0x18`–`0x1F`; MCP `0100 [17][16][15]` → `0x20`–`0x27`.

### 4.4 I²C

| Item | Spec |
|---|---|
| Speed | **100 kHz** |
| Pull-ups | **2k2** on main **R9/R10** only; **none** on remote |
| Series | **22 Ω** on SDA/SCL at remote |
| Mux | #1 visible on **ch 5**; #2 on **ch 6** |

### 4.5 1-Wire

| Item | Spec |
|---|---|
| Active IO | **IO0–IO3** → J6–J9 data |
| Pull-up | **2k2** to **`+3V3`** on IO0–IO3 at DS2482 |
| Unused IO | **IO4–IO7** **NC** (unconnected — not GND) |
| Power | Powered probes via temp JST **`+3V3`** (not parasite by default) |

### 4.6 Universal pulse (4× around one **TLP281-4**)

Same PCB channel for S0 kWh, YF-B6 / hall OD, and dry contacts. Idle **HIGH**, active **LOW** at MCP. WanOS **polls** GPIO (no INT).

#### 4.6.1 Logic side (per channel)

| Ref | Value | Role |
|---|---|---|
| Opto | **TLP281-4** one ch | Isolation |
| **R_IN** | **470 Ω**, 1%, 0.125 W | Series to MCP |
| **R_PU** | **10 kΩ**, 1%, 0.125 W | Pull-up to **`+3V3`** |
| **C_RC** | **100 nF**, X7R, 50 V | Debounce (optional 220 nF) |
| **D_ESD** | **ESD5B5.0ST5G** (or equiv.) | `PULSE_CHx` → GND |

- Emitter → GND  
- Collector → **R_IN** → **`PULSE_CHx`** → MCP GPIO  
- **`PULSE_CHx`** → **R_PU** → **`+3V3`**; → **C_RC** → GND; → **D_ESD** → GND  

#### 4.6.2 Field side (12 V LED)

| Ref | Value |
|---|---|
| **R_LED** | **4.7 kΩ**, 1%, **0.25 W** from **`S0_RAIL`** to opto LED anode |

≈ **2.3 mA** at 12 V (Vf ≈ 1.2 V); still OK at **11.5 V** VIN / `S0_RAIL`.

| Source | Wiring |
|---|---|
| **S0 kWh** | Cathode → meter S0 out; other terminal → GND / loop return per meter |
| **YF-B6** | JST VDD = **`S0_RAIL`**; cathode → SIG; sensor OD → GND |
| **Dry contact** | Cathode → contact → GND |

#### 4.6.3 Activity LEDs + test button

| Item | Spec |
|---|---|
| LEDs | **4×** SMD activity — sense **`PULSE_CHx`** (active LOW) |
| Button | **1×** SMD tactile — enables activity-LED supply only |
| Series R | **1 kΩ** per activity LED |
| Power LED | From **`S0_RAIL`** — § 4.2.4 |

**Topology:** button closes a shared **anode rail** (`+3V3` → button → LED anodes). Each cathode → **1 kΩ** → **`PULSE_CHx`**. While button open, no activity-LED current.

### 4.7 Connection map

**Pulse JST — 3-pin:**

| Pin | Net |
|---|---|
| 1 | **`S0_RAIL`** (VDD / loop supply) |
| 2 | **SIG** (opto LED cathode) |
| 3 | **GND** |

**Temp JST — 3-pin:**

| Pin | Net |
|---|---|
| 1 | **`+3V3`** |
| 2 | **1-Wire data** |
| 3 | **GND** |

**TLP281-4 (SO16):**

| Ch | LED A / C | Collector / Emitter |
|---|---|---|
| 1 | 1 / 2 | 10 / 9 |
| 2 | 3 / 4 | 12 / 11 |
| 3 | 5 / 6 | 14 / 13 |
| 4 | 7 / 8 | 16 / 15 |

### 4.8 Decoupling / misc

- **100 nF** at each IC VCC; bulk on **3V3** near DS2482 / MCP  
- MCP **INTA/INTB**: **NC** (unused)

---

## 5. Cat5 UTP (~6 m) — pair map (**locked**)

| Pair | Colors (T568B-oriented) | Signal |
|---|---|---|
| **1** | White/Green + Green | **SDA + GND** |
| **2** | White/Orange + Orange | **SCL + GND** |
| **3** | White/Blue + Blue | **`+12V` (VIN) + GND** |
| **4** | White/Brown + Brown | **GND + GND** (ex-INT pair — both to GND; improves return) |

Same map both remotes. **Logical** assignment is colour/pair above; **numeric** RJ45 pin 1–8 depends on the jack footprint’s pad numbering (KiCad `RJ45_Amphenol_54602-x08_Horizontal` / TE **5556416-1**) — lock pad↔net in schematic when the footprint is placed, not before.

---

## 6. Channel map (**locked**)

### 6.1 U5 mux

| U5 ch | Use |
|---|---|
| 0–4 | SHT31 plant |
| **5** | Remote **#1** (water) |
| **6** | Remote **#2** (kWh) |
| 7 | NC / spare |

### 6.2 Remote #1 — water

| Pulse JST | Function | Temp JST | Function |
|---|---|---|---|
| 1 | Bath 1 cold (YF) | 1 | Pipe temp A |
| 2 | Bath 1 hot (YF) | 2 | Pipe temp B |
| 3 | Bath 2 cold (YF) | 3 | **Unused** |
| 4 | Bath 2 hot (YF) | 4 | **Unused** |

### 6.3 Remote #2 — kWh

| Pulse JST | Function | Temp JST | Function |
|---|---|---|---|
| 1 | kWh main (S0) | 1 | Temp probe |
| 2 | kWh aux (S0) | 2 | **Unused** |
| 3 | **Unused** | 3 | **Unused** |
| 4 | **Unused** | 4 | **Unused** |

---

## 7. Physical

| Item | Spec |
|---|---|
| Size | **40 × 60 mm** (**hold** — fit check later) |
| Connectors | **1× RJ45**; **8× JST 3-pin** (4 pulse + 4 temp) |
| Placement | RJ45 short edge; JST opposite / long edge; ICs center |
| Layout | Star / split GND for S0 returns; short I²C; ESD at connectors |

---

## 8. DS18B20 mounting

- Paste between probe and copper sleeve; firm spring contact; clean pipe surface  
- Insulate sleeve + pipe; strain-relieve ~2 m leads  
- Stable flow section — avoid mixing, pumps, tight bends  

---

## 9. Software / WanOS

| Topic | Spec |
|---|---|
| Remote #1 | **U5 ch 5** → MCP **`0x22`** (water) + DS2482 **`0x18`** (2 temps) |
| Remote #2 | **U5 ch 6** → same addresses (kWh + 1 temp) |
| Mux | **Exclusive** select — never ch 5+6 together |
| Counting | **Poll** MCP GPIO; software edges only |
| Schedule | Prefer water poll cadence for edge capture; kWh slow; temps/SHT31 lower priority |
| Idxs | Keep legacy idxs; change hardware backend |

---

## 9a. KiCad / BOM

| Item | Path |
|---|---|
| KiCad project | [`projects/wanos-remote/`](../projects/wanos-remote/) |
| BOM | [`components.xlsx`](../projects/wanos-board/components.xlsx) — `board=remote` |
| Regenerate sch | `python projects/wanos-remote/_regen_schematic.py` |

## 10. Open items

1. **Hold** — **40×60** mechanical fit / layout.  
2. KiCad **ERC cleanup** — attach global labels to IC pins (generator places labels nearby).  
3. RJ45 **pad↔net** verify vs footprint when laying out.  
4. Power LED brightness on bench (R18 **6k8**).  
5. Verify / fill **LCSC** for **DS2482-800** and JST **B3B-XH-A**.  
6. Product docs on main cutover (`field-wiring`, `board-spec`, `io-expander-map`, `gpio-interface`).  
7. Main: second RJ45 + per-port **PPTC/SMBJ12A** when main work starts.  
8. Pipeline: `triage` when scheduled.

---

## 11. Design notes / VIN check

- **11.5 V min at remote VIN:** OK for **AP2204K-3.3**, YF (**5–15 V** on `S0_RAIL`), S0 (**5–27 V**), and opto LED current with **4.7 kΩ**. Raising plant 12 V to compensate Cat5/PPTC drop is fine; keep remote VIN **≤ ~15 V** practical headroom for YF on `S0_RAIL` (YF abs max 15 V — do not crank plant so high that `S0_RAIL` exceeds sensor rating).  
- Opto + single **4.7 kΩ** from **`S0_RAIL`** covers S0, hall OD, and dry contact.  
- Port: **PPTC** + **SMBJ12A**. **`S0_RAIL`:** **10 Ω + 10 µF ‖ 100 nF**.  
- I²C: 100 kHz, pair-with-GND, root 2k2, 22 Ω series; **no INT**.  
- Bring-up: **12 V lab PSU** into remote VIN pins / RJ45 before main respin.

---

## 12. Verbatim locks

**2026-09-21**

- UTP pair map = § 5; remove INT altogether; PPTC **nSMD050-33V** + **SMBJ12A** OK.  
- VIN at remote close to 12 V, **≥ 11.5 V** OK (raise plant 12 V as needed).  
- Addresses **`0x18` + `0x22`** locked both remotes.  
- Mux ch 5 / 6; #1 = 4 water + 2 temp; #2 = 2 kWh + 1 temp.  
- Power LED from **`S0_RAIL`**; bench on **12 V lab supply**; remote board before main PCB.

**2026-09-21 (schematic readiness)**

- MCP **GPA0–GPA3** = pulses; other GPIO no nets / firmware LOW.  
- DS2482 **IO0–IO3** → temps; **IO4–IO7** unconnected (not GND).  
- Project path **`projects/wanos-remote/`**.  
- **SMBJ12A** TVS on remote VIN as well as main.

---

## Related

- [`field-wiring.md`](field-wiring.md)  
- [`io-expander-map.md`](io-expander-map.md)  
- [`gpio-interface.md`](gpio-interface.md)  
- [`board-spec.md`](board-spec.md)  
- [`todo/pipeline.md`](todo/pipeline.md)  
