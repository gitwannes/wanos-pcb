<!-- --- file: docs/remotepcb.md --- -->

# Remote plant PCB — universal pulse + 1-Wire

**Status:** design draft — not kicked off / not locked for implement. **No KiCad yet.**  
**Role:** universal remote module — **4×** opto pulse inputs + **4×** DS18B20 (1-Wire). Reusable for water, kWh S0, dry-contact doors, and pipe temps.

Today’s main-board water / kWh wiring → [`field-wiring.md`](field-wiring.md), [`io-expander-map.md`](io-expander-map.md).

---

## 1. Intent

| Item | Spec |
|---|---|
| Channels | **4×** universal pulse + **4×** DS18B20 (4 of 8 DS2482 channels) |
| Link to main | **Cat5 UTP ~6 m** → main **RJ45** (first uplink reuses **J4**) |
| I²C | **U5** TCA9548A channel **5** (`SD5` / `SC5`) @ **100 kHz** |
| Power | Main **`+12V`** → Cat5 → remote **VIN** → **AP2204K-3.3** → **3V3**; filtered **`S0_RAIL`** for opto LEDs |
| 12 V loss | Remote offline when plant 12 V is down (Pi may still run on 5 V) |
| Field connectors | **4× JST 3-pin** pulse + **4× JST 3-pin** temp; uplink **RJ45** |
| Activity LEDs | **4×** + **1×** SMD button (LEDs lit only while pressed) |
| Instances | ≥1 board; more remotes on mux ch **6+** if needed |

---

## 2. System block

```
  Pi root I²C (R9/R10 2k2)
       |
       +-- U1 PCA9554 0x20  (doors / kWh until remotes absorb; water P2–P5 removed after cutover)
       +-- U2 PCA9554 0x21  (buttons / 12 V mon)
       +-- U5 TCA9548A 0x70
       |      ch 0–4 : SHT31 plant (unchanged)
       |      ch 5   : remote uplink #1 (SD5/SC5) ---- Cat5 ---- remote RJ45
       |      ch 6–7 : NC or second remote later
       +-- J16 LCD (root, not muxed)

  Main J4: +12V (plant) -- PPTC -- SMBJ12A -- Cat5 ---- remote VIN

  Remote PCB:
       VIN (~12 V) -- input filter
            |-- AP2204K-3.3 --> +3V3 --> DS2482-800 + MCP23017 + logic RC/TVS/LED
            |-- small RC --> S0_RAIL --> R_LED ×4 --> TLP281-4 LEDs
       Field JST 3-pin ×4 pulse --> S0_RAIL / SIG / GND
       Field JST 3-pin ×4 temp  --> +3V3 / 1-Wire / GND
       INT (OD) --> Cat5 pair 4 --> main (2k2 pull-up) --> TBD GPIO
```

---

## 3. Main PCB changes

### 3.1 Connector **J4** (redefined)

Remove today’s water-meter RJ45 (four SIG + `+5VA` into **U1**).

New **J4** = uplink to remote #1:

| Net / pin group | Connection |
|---|---|
| **SDA** | **U5** **`SD5`** |
| **SCL** | **U5** **`SC5`** |
| **`+12V`** | Polyfuse (§ 3.3) from plant **`+12V`** (**J14** domain) |
| **GND** | Board GND (multiple returns — § 5) |
| **INT** | MCP23017 INT; **2k2** pull-up to **`+3V3`** on main; **landing pin TBD** |

Jack: TE **5556416-1** / Amphenol **54602**-class RJ45 TH, no magnetics, no jack LEDs.  
Do **not** put **`+5VA`** on this uplink. Lock 8P8C pinout with remote (§ 5).

### 3.2 Remove on-main water front-end (first cutover)

- Drop `water_meters.kicad_sch` channel parts  
- Drop **U1** **P2–P5** water nets  

Doors (**J2/J3**) and kWh (**J6/J7**) move to the same remote board type later (extra remotes / channels).

### 3.3 Port protection on remote **`+12V`** feed

| Part | Role | Spec |
|---|---|---|
| **PPTC** | Overcurrent | **Proposed: TECHFUSE `nSMD050-33V`** (LCSC **C70077**) — **500 mA** hold, **1 A** trip, **33 V** max, 1206, R≈150 mΩ |
| **SMBJ12A** | Port **TVS** | **`+12V`** → GND at **J4** (same as main **D3**) |

Order: plant **`+12V`** → **PPTC** → jack (TVS at connector).

**Why this PPTC:** remote load ≪ 150 mA (LDO + sensors + gated LEDs); **500 mA** hold avoids nuisance trips; **33 V** rating has margin on a 12 V rail (do **not** reuse main **F2** / typical 6–8 V 1206 PPTCs). Drop ≈ **15 mV** at 100 mA.

**Alternate:** BNstar **SMD1206-050C-16V** (LCSC **C2760267**) — same hold, only **16 V** max (tighter; rely more on **SMBJ12A**).

### 3.4 INT landing

Options: free **Pi BCM**, **U2** free pin, or freed **U1** pin after water move. Lock before schematic.

### 3.5 Rail clamps

Prefer **port TVS** on **J4 `+12V`**. Do not conflate with Pi **5 V** clamp (**D1**). Leave main **D3** / **J14** unless budget review says otherwise.

---

## 4. Remote PCB — electrical

### 4.1 I/O

| Direction | Count | Path |
|---|---:|---|
| In | 4 | Universal pulse → **TLP281-4** → **MCP23017** |
| In | 4 | DS18B20 → **DS2482-800** (4 of 8 ch) |
| Uplink | 1 | I²C + INT + **`+12V`** + GND over Cat5 |

### 4.2 Power

**Cable:** **`VIN` ≈ 11–13 V** = main **`+12V`** after PPTC / drop.

#### 4.2.1 **3V3** — **AP2204K-3.3**

```
VIN (11–13 V) → AP2204K-3.3 → +3V3
```

| Item | Spec |
|---|---|
| Part | **AP2204K-3.3** (SOT-23-5), e.g. **AP2204K-3.3TRG1** |
| Vin | **2.3–24 V** |
| Iout | **150 mA** |
| EN | Tie to **VIN** (always on) |
| Cin | **47–100 µF** electrolytic + **100 nF** ceramic |
| Cout | Per datasheet (≥ **2.2 µF** ceramic) + **22–47 µF** bulk; **100 nF** at each IC |

Dissipation at ~50 mA ≈ **0.44 W** — copper under SOT-23-5. Activity LEDs gated so continuous load stays low.

#### 4.2.2 **`S0_RAIL`**

```
VIN → R_S0 (10 Ω) → S0_RAIL →|| C_S0 (10 µF + 100 nF) → GND
                              └→ R_LED ×4 → TLP281-4 anodes
```

| Ref | Value | Role |
|---|---|---|
| **R_S0** | **10 Ω**, 1%, 0.125 W | Soft RC with **C_S0**; limits HF dump into rail |
| **C_S0** | **10 µF** (X5R/X7R or electrolytic) + **100 nF** ceramic | Bulk + HF at opto |

Drop at 4× ~2.3 mA ≈ **0.1 V** across **10 Ω** — fine. Keep **C_S0** and LED returns close to the TLP281-4; star field GND away from digital return.

Used for **R_LED** and pulse JST pin 1 (**VDD** / loop supply).

#### 4.2.3 No remote 5 V rail

YF-B6 VDD (**5–15 V**) = **`S0_RAIL`** on the pulse JST.

#### 4.2.4 Power LED (always on)

Separate from activity LEDs — **always glows** when board is powered.

| Option | Series R | Note |
|---|---|---|
| From **`+3V3`** (preferred) | **1 kΩ**–**2 kΩ** | Matches main indicator class; independent of 12 V LED domain |
| From **VIN** / **`S0_RAIL`** | **4.7 kΩ**–**6.8 kΩ** | Brightness match to 12 V (main **R30** = 6k8 on `+12V`) |

Not gated by the test button.

### 4.3 ICs

| IC | Role |
|---|---|
| **TLP281-4** | Quad optocoupler |
| **DS2482-800** | 1-Wire master — 4 channels used |
| **MCP23017A** | I/O expander — 4 pulse GPIOs (**A** die — see note) |
| **AP2204K-3.3** | 12 V → **3V3** |

**MCP23017 vs MCP23017A:** Microchip **A** revision fixes early-silicon register/BANK errata. Order **MCP23017A** (e.g. SOIC-28); do not buy unmarked legacy **MCP23017** if **A** is available.

I²C addresses **TBD** — must not collide with root when ch 5 selected (**U1 `0x20`**, **U2 `0x21`**, **U5 `0x70`**, LCD).

**DS2482-800:** pins 11/10/9 → `0001 1 [11][10][9]` → **`0x18`–`0x1F`**.  
**MCP23017A:** pins 17/16/15 → `0100 [17][16][15]` → **`0x20`–`0x27`**.

### 4.4 I²C

| Item | Spec |
|---|---|
| Speed | **100 kHz** |
| Pull-ups | **2k2** on main **R9/R10** only; **none** on remote |
| Series | **22 Ω** on SDA/SCL at remote |
| Mux | Visible only when **U5 ch 5** (or 6) selected |

### 4.5 1-Wire

| Item | Spec |
|---|---|
| Pull-up | **2k2** to **`+3V3`** per used channel, at DS2482 |
| Unused ch | No pull-ups |
| Power | Powered probes via temp JST **`+3V3`** (not parasite by default) |

### 4.6 Universal pulse (4× around one **TLP281-4**)

Same PCB channel for S0 kWh, YF-B6 / hall OD, and dry contacts. Idle **HIGH**, active **LOW** at MCP.

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

≈ **2.3 mA** at 12 V (Vf ≈ 1.2 V).

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
| Power LED | **Not** on this circuit — always on (§ 4.2.4) |

**Topology:** button closes a shared **anode rail** (`+3V3` → button → LED anodes). Each cathode → **1 kΩ** → **`PULSE_CHx`** (or LED + 1 kΩ in series to `PULSE_CHx`). While button open, no LED current. While held: channel active (MCP input low / opto on) → that LED lights.

**1 kΩ insight (from `+3V3`):** \(I \approx (3.3 - V_f) / 1\,\mathrm{k}\Omega\) → ~**1.3 mA** (red, Vf≈2.0 V) to ~**0.5 mA** (blue/white, Vf≈2.8 V). Fine for a brief press-to-test indicator; four LEDs lit ≈ **2–5 mA** total — negligible vs AP2204 budget. Do **not** use 1 kΩ from **12 V** into a 3.3 V-rated LED path.

#### 4.6.4 Per-channel BOM (×4) + shared

| Ref | Part |
|---|---|
| U? | **TLP281-4** (one IC, four channels) |
| R_IN / R_PU / C_RC / D_ESD / R_LED / D_ACT | as above |
| Shared | 1× SMD button |

### 4.7 Connection map

**KiCad (draft):** `Device:Optocoupler_4Channel`, `Device:R` / `C` / `D_TVS` / `LED`, switch, JST, `power:+3V3` / `GND`, nets **`VIN`**, **`S0_RAIL`**.  
Footprints: SOIC-16 opto; **0603** R/C; TVS **SOD-323**; JST XH (or plant family); RJ45 uplink.

**TLP281-4 (SO16):**

| Ch | LED A / C | Collector / Emitter |
|---|---|---|
| 1 | 1 / 2 | 10 / 9 |
| 2 | 3 / 4 | 12 / 11 |
| 3 | 5 / 6 | 14 / 13 |
| 4 | 7 / 8 | 16 / 15 |

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

### 4.8 Decoupling / misc

- **100 nF** at each IC VCC; bulk on **3V3** near DS2482 / MCP  
- MCP INT open-drain; **2k2** pull-up on **main**

---

## 5. Cat5 UTP (~6 m)

| Pair | Colors (T568B-oriented) | Signal |
|---|---|---|
| **1** | White/Green + Green | **SDA + GND** |
| **2** | White/Orange + Orange | **SCL + GND** |
| **3** | White/Blue + Blue | **`+12V` (VIN) + GND** |
| **4** | White/Brown + Brown | **MCP23017 INT + GND** |

Lock 8P8C pin table (main **J4** ↔ remote) before fab.

---

## 6. Physical

| Item | Spec |
|---|---|
| Size | **40 × 60 mm** (fit check required) |
| Connectors | **1× RJ45**; **8× JST 3-pin** (4 pulse + 4 temp) |
| Placement | RJ45 short edge; JST opposite / long edge; ICs center |
| Layout | Star / split GND for S0 returns; short I²C; ESD at connectors |

---

## 7. DS18B20 mounting

- Paste between probe and copper sleeve; firm spring contact; clean pipe surface  
- Insulate sleeve + pipe; strain-relieve ~2 m leads  
- Stable flow section — avoid mixing, pumps, tight bends  

---

## 8. Software / WanOS

| Topic | Spec |
|---|---|
| Water after cutover | **U5 ch 5** → **MCP23017** (opto) |
| Doors / kWh | Migrate to same remote type over time |
| Pipe temps | DS2482-800 + DS18B20 |
| Mux | Exclusive select vs SHT31 ch 0–4 |
| Idxs | Keep legacy idxs; change hardware backend |
| Counting | Software edges only — MCP has **no** hardware counter; INT does not eliminate miss risk under Linux |

---

## 9. Open items

1. Lock **J4** 8P8C pinout (both ends).  
2. **INT** destination (BCM vs expander) — or drop INT and poll only.  
3. Confirm PPTC: **`nSMD050-33V` / C70077** (proposal) vs **SMD1206-050C-16V / C2760267**. **SMBJ12A** = port TVS.  
4. Cable IR drop at 6 m under max load.  
5. **DS2482-800** and **MCP23017A** I²C addresses (no collision on ch 5).  
6. First remote **channel map**; how many remotes.  
7. Power LED rail: **`+3V3`** + 1–2 kΩ vs **VIN** + 4.7–6.8 kΩ.  
8. Cutover sequencing (water-only first vs wait for doors/kWh).  
9. **40×60** mechanical fit.  
10. Product docs on ship.  
11. Pipeline: `triage` when scheduled; no KiCad until `kickoff` + `implement`.

---

## 10. Design notes

- Opto + single **4.7 kΩ** from **`S0_RAIL`** covers S0, hall OD, and dry contact at plant 12 V.  
- **AP2204K-3.3** for 24 V Vin; activity LEDs gated; power LED always on.  
- Port: **PPTC** (overcurrent) + **SMBJ12A** (TVS) — different parts.  
- **`S0_RAIL`:** **10 Ω + 10 µF ‖ 100 nF**.  
- I²C over Cat5: 100 kHz, pair-with-GND, root 2k2, 22 Ω series at remote.

---

## Related

- [`field-wiring.md`](field-wiring.md)  
- [`io-expander-map.md`](io-expander-map.md)  
- [`gpio-interface.md`](gpio-interface.md)  
- [`board-spec.md`](board-spec.md)  
- [`todo/pipeline.md`](todo/pipeline.md)  
