<!-- --- file: projects/wanos-board/constraints.md -->

# PCB / schematic constraints — WanOS board

Applies to `projects/wanos-board/`. Update when **R1** / **S1** kickoff locks values.

---

## Board

- Default **2-layer** unless `design.yaml` says otherwise
- Board outline defined in PCB editor after **R1** form factor lock
- Pi HAT: respect 40-pin keep-out and mounting holes per Pi model (**R1**)
- Mounting holes >= 3.2 mm drill unless **R1** specifies otherwise

---

## Schematic

- Net names: uppercase with underscores (`GPIO_PULSE_KWH`, `GPIO_SAFETY`, `SHT11_D_SAUNA_HIGH`)
- One GND symbol style per sheet; single ground reference
- Map every net to BCM pin in [`docs/gpio-interface.md`](../../docs/gpio-interface.md) or document deviation in phase **R1**
- Decoupling: 100 nF per IC power pin; bulk cap on any local regulator output
- SSR / safety outputs: default **OFF** at power-up (hardware + software)

---

## Footprints

- Lock footprint library at **S1** kickoff (global / JLCPCB / project-local)
- Prefer LCSC-stocked parts when using JLC assembly
- Document LCSC C-number in `bom-targets.yaml`

---

## Design verification

- Run ERC after schematic changes (`kicad-cli sch erc`)
- Run DRC after PCB changes (`kicad-cli pcb drc`)
- Do not mark **S1** / **L1** complete until both pass or waivers are logged in the phase file

---

## Safety (sauna / IR)

- This board interfaces to high-power heating control in WanOS — treat SSR and safety nets as **critical**
- Creepage/clearance for mains-related fields is an **R1** lock (even if SSRs are off-board)
- Never mark **V1** done without verifying boot-time SSR idle state on real hardware

---

## KiCad paths (Windows — adjust per machine)

- KiCad config: `%APPDATA%/kicad/10.0/`
- CLI: `"C:/Program Files/KiCad/10.0/bin/kicad-cli.exe"`
- See [`docs/kicad-setup.md`](../../docs/kicad-setup.md)
