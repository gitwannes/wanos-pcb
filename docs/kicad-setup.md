<!-- --- file: docs/kicad-setup.md -->

# KiCad setup — wanos-pcb-v1

Local toolchain for `projects/wanos-board/`. Primary automation path: **KiCad 10 + Konnect + Cursor MCP**.

Upstream Konnect docs: [github.com/mixelpixx/Konnect](https://github.com/mixelpixx/Konnect) (do not copy README into this repo).

Optional reference: local [`kicad-cursor`](https://github.com/) at `C:/data/git/kicad-cursor`.

---

## Requirements

| Tool | Purpose |
|---|---|
| **KiCad 10** | Schematic + PCB editor |
| **Konnect** (PCM plugin) | MCP tools: schematic, PCB, DRC, JLC search, fab export |
| **Cursor** | Agent + MCP client |
| **kicad-cli** | ERC/DRC batch, Gerber export (also used by Konnect) |

**Not required for Konnect:** Python, Node.js, SWIG.

---

## 1. Install Konnect

1. Download `konnect-pcm-v<version>-windows.zip` from [Konnect Releases](https://github.com/mixelpixx/Konnect/releases).
2. KiCad 10 → **Tools → Plugin and Content Manager → Install from File**.
3. Restart KiCad.
4. Verify: **PCB Editor → Tools → External Plugins → Konnect**.

Binary path (typical):

```text
C:\Users\<YOU>\Documents\KiCad\10.0\3rdparty\plugins\com_github_mixelpixx_konnect\bin\konnect.exe
```

---

## 2. Enable KiCad IPC API

**KiCad → Preferences → Plugins → Enable KiCad API** (IPC API Server).

Restart KiCad. Keep KiCad running with the board loaded for live PCB MCP tools.

---

## 3. Cursor MCP

**Settings → MCP Servers → Add → Local command:**

```text
C:\Users\<YOU>\Documents\KiCad\10.0\3rdparty\plugins\com_github_mixelpixx_konnect\bin\konnect.exe
```

Test prompts: “List Konnect toolsets”, “Run DRC”, “Get board info”.

Pipeline: **kickoff** before design locks; **implement** before marking a phase coding.

---

## 4. Project layout

```text
projects/wanos-board/
  design.yaml
  constraints.md
  bom-targets.yaml
  components.xlsx          # BOM seed (LCSC)
  wanos-board.kicad_*      # Created at S1
  fabrication/
    JLCPCB_BOM_Template.xls
  datasheets/
```

Product spec → [`board-spec.md`](board-spec.md).

---

## 5. Verification commands

```powershell
$cli = "C:/Program Files/KiCad/10.0/bin/kicad-cli.exe"
$sch = "projects/wanos-board/wanos-board.kicad_sch"
$pcb = "projects/wanos-board/wanos-board.kicad_pcb"

& $cli sch erc $sch
& $cli pcb drc $pcb
```

Do not close **S1** / **L1** until ERC/DRC pass or waivers are in the phase file.

---

## 6. Notes

| Topic | Note |
|---|---|
| PCB tools | KiCad open + board loaded (IPC) |
| Schematic tools | Konnect can edit `.kicad_sch` without KiCad open |
| Freerouting | Konnect Specctra pipeline — lock HDMI nets first ([`hdmi-spi-eink.md`](hdmi-spi-eink.md)) |
| LCSC parts | Validate `components.xlsx` C-numbers at **J1** |

**Ops1** in [`todo/pipeline.md`](todo/pipeline.md) tracks machine setup completion.
