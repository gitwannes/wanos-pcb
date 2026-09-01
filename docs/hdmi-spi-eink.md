<!-- --- file: docs/hdmi-spi-eink.md -->

# wanos-pcb-v1 — HDMI to SPI (WISC e-ink)

The HDMI Type-A connector on **wanos-pcb-v1** is repurposed as a proprietary SPI header for the **WISC** e-ink display (not TMDS video).

**Board context:** [`board-spec.md`](board-spec.md) § 4.2 · **Part:** Molex 208658-1052 → [`component-selection.md`](component-selection.md)

**Legacy WISC reference:** [`reference/wisc-board/wisc-v2-6-4-hdmi.md`](reference/wisc-board/wisc-v2-6-4-hdmi.md)

---

## Legacy WISC / motivation to redesign

**Deployed today (operator, 2026-09-01):** the [**WISC 2.6.4 HDMI board**](reference/wisc-board/wisc-v2-6-4-hdmi.md) is in use on the **Raspberry Pi connected to the LCD screens**. The **HDMI cable is not connected** — the board **only powers that Pi**. **E-ink over HDMI worked in the past** but **does not work any more**; replacing this **HDMI / e-ink** arrangement is **one of the drivers** for **wanos-pcb-v1**.

**wanos-pcb-v1** should treat the legacy HDMI-cable + repurposed-TMDS approach as **failed field history**, not a silent copy target. Lock connector, wiring, and software against verification on the **new** integrated carrier ([`board-spec.md`](board-spec.md) § 4.2).

---

## HDMI to SPI pin mapping

| HDMI pin | Standard HDMI function | Repurposed signal | Engineering rationale |
|---:|---|---|---|
| 10 | TMDS Clock+ | **SCK** | Best-coupled pair → clean edges for SPI clock |
| 12 | TMDS Clock− | **GND (SCK return)** | Tight return path |
| 11 | TMDS Clock Shield | **GND** | Extra ground |
| 7 | TMDS Data0+ | **MOSI (SDI)** | Second-best pair → ideal for MOSI |
| 9 | TMDS Data0− | **GND (MOSI return)** | Tight return path |
| 8 | TMDS Data0 Shield | **GND** | Extra ground |
| 4 | TMDS Data1+ | **DC** | Low-speed |
| 6 | TMDS Data1− | **RST** | Low-speed |
| 5 | TMDS Data1 Shield | **GND** | Ground reference |
| 1 | TMDS Data2+ | **CS** | Low-speed |
| 3 | TMDS Data2− | **BUSY** | Panel status input |
| 2 | TMDS Data2 Shield | **GND** | Ground reference |
| 18 | +5V Power | **VCC (5V)** | Safe for power input |
| 17 | DDC/CEC Ground | **GND** | Power-adjacent ground |
| 13 | CEC | **spare / INT** | Future interrupt |
| 15 | SCL | **spare (future I²C)** | Optional sensor |
| 16 | SDA | **spare (future I²C)** | Optional sensor |
| 14 | Reserved | **spare** | Free conductor |
| 19 | Hot Plug Detect | **panel-present sense** | Detect display presence |

---

## Engineering notes

- Place **SCK** and **MOSI** on the best TMDS differential pairs for minimal crosstalk and clean edges.
- Convert all “minus” and shield pins to **GND** for stable return paths and reduced EMI.
- DC, RST, CS, BUSY are low-speed control/status signals on lower-quality pairs.
- Use HDMI pin 18 (+5 V) as panel 5 V input only after verifying the WISC board regulator and that the cable has no AC-coupling.
- Keep spare pins for future I²C or interrupt expansion.

---

## Verification requirements (before final release)

1. **Check HDMI cable continuity** — ensure the installed HDMI cable does not include AC-coupling capacitors on TMDS pairs.
2. **Check WISC board conditioning** — ensure the e-ink panel board does not expect TMDS signalling or include series AC coupling.
3. **Confirm voltage domains** — verify WISC logic levels (3.3 V) and that powering via HDMI pin 18 is acceptable.

**Layout:** Lock HDMI/SPI nets before Freerouting ([`board-spec.md`](board-spec.md) § 7.1, § 7.5).
