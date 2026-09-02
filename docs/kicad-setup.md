<!-- --- file: docs/kicad-setup.md -->

# KiCad setup — wanos-pcb-v1

Local toolchain for `projects/wanos-board/`. Primary automation path: **KiCad 10 + Konnect + Cursor MCP**.

Upstream Konnect docs: [github.com/mixelpixx/Konnect](https://github.com/mixelpixx/Konnect) (do not copy README into this repo).

Optional reference: local `kicad-cursor` repo if present on your machine.

**WISC reference boards** (read-only in repo): [`reference/wisc-board/`](reference/wisc-board/) — Konnect can inspect them; do not edit KiCad sources there.

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

## End-to-end checklist (verified on Windows)

Work through in order. **Ops1** closed **2026-09-01** when steps 1–8 pass (verified on WISC `wisc2-6-4` reference — `open_project` → `ipc_available: true` with KiCad PCB Editor open).

| Step | Action | Pass criterion |
|---:|---|---|
| 1 | Install Konnect via PCM (§ 1) | **PCB Editor → Tools → External Plugins → Konnect** exists |
| 2 | Enable KiCad API (§ 2) | Preferences shows **Listening at ipc://…** |
| 3 | Open a `.kicad_pcb` in **PCB Editor** (§ 3) | Board visible in layout — not Project Manager only |
| 4 | Configure Cursor MCP (§ 4) | **Customize → MCPs → konnect** = Connected |
| 5 | Wire IPC socket to Konnect (§ 5) | `KICAD_API_SOCKET` in `.cursor/mcp.json` **or** Konnect settings saved |
| 6 | Reload Cursor | `Ctrl+Shift+P` → **Developer: Reload Window** |
| 7 | Keep KiCad running with board open | Same KiCad session as step 2–3 |
| 8 | Agent test: **`open_project`** (§ 6) | `ipc_available: true`, `kicad_ui_running: true` |

---

## 1. Install Konnect

1. Download `konnect-pcm-v<version>-windows.zip` from [Konnect Releases](https://github.com/mixelpixx/Konnect/releases).
2. KiCad 10 → **Tools → Plugin and Content Manager → Install from File**.
3. Restart KiCad.
4. Open any project → open **PCB Editor** (double-click the `.kicad_pcb` or use the PCB icon).
5. Verify: **PCB Editor → Tools → External Plugins → Konnect**.

**Note:** Plugin and Content Manager (**Installed** tab) only shows that Konnect is installed. It does **not** configure IPC or MCP — that is separate (§ 4–5).

Binary path (typical):

```text
C:\Users\<YOU>\Documents\KiCad\10.0\3rdparty\plugins\com_github_mixelpixx_konnect\bin\konnect.exe
```

Konnect plugin directory (Python launcher + optional `settings.json`):

```text
C:\Users\<YOU>\Documents\KiCad\10.0\3rdparty\plugins\com_github_mixelpixx_konnect\
```

---

## 2. Enable KiCad IPC API server

1. **KiCad → Preferences → Plugins** (KiCad API section).
2. Check **Enable KiCad API**.
3. **Python interpreter:** use **Detect Automatically** (typical: `C:\Program Files\KiCad\10.0\bin\pythonw.exe`, Python 3.11.x).
4. Click **OK**. If the API was off at launch, **restart KiCad** once.
5. Re-open **Preferences → Plugins** and confirm the status line:

```text
Listening at ipc://C:\Users\<YOU>\AppData\Local\Temp\kicad\api.sock
```

That full `ipc://…` string is the IPC address. Copy it for § 5.

### Windows: no `api.sock` file in Explorer?

Normal. On Windows, KiCad’s IPC uses an **NNG named pipe**, not a regular disk file. The `%TEMP%\kicad\` folder may exist while **`api.sock` is absent** in Explorer or `Test-Path`. Trust the **Listening at …** line in Preferences, not file existence.

If the listening line is **missing** after restart: enable the checkbox again, restart KiCad, then open **PCB Editor** with a board loaded (§ 3).

---

## 3. Open the board in PCB Editor (required for live IPC)

KiCad 10 runs as one **`kicad.exe`** process — you will not see separate `pcbnew` / `eeschema` processes.

For Konnect **live** PCB tools and `open_project`:

1. Open the project (Project Manager is fine to start).
2. **Open PCB Editor** — load the `.kicad_pcb` (e.g. reference `docs/reference/wisc-board/211201 wisc2-5-3/wisc-v5.kicad_pcb`).
3. Leave **PCB Editor** open while using Cursor Agent.

**Project Manager alone is not enough** for `open_project` to list an open board.

**External Plugins → Konnect** is available from **PCB Editor → Tools** (and schematic editor when open). Use it for Konnect **settings** (IPC socket path, optional Start Server from KiCad). Cursor uses its own `konnect.exe` via MCP (§ 4) — you do not need **Start Server** in KiCad for Cursor Agent.

---

## 4. Cursor MCP (Konnect) — JSON only

On current Cursor builds, **+ New** under **Customize → MCPs** opens (or creates) a JSON file — there is **no separate stdio form**.

### Steps

1. Open **Customize** → **MCPs** tab.
2. Click **+ New** → choose **wanos-pcb** (workspace) or **User** (global).
3. Cursor opens **`.cursor/mcp.json`** (workspace) or **`%USERPROFILE%\.cursor\mcp.json`** (user).
4. Paste the block in § 5 (includes IPC env var).
5. **Save** the JSON file.
6. **Customize → MCPs** should list **konnect** with **Connected** / green status after reload (step 6 of checklist).

**Command Palette:** `Ctrl+Shift+P` → **Open MCPs** jumps to the same tab.

### Workspace config (this repo)

File: [`.cursor/mcp.json`](../.cursor/mcp.json)

Use doubled backslashes (`\\`) in JSON on Windows. Replace `<YOU>` with your Windows user name.

---

## 5. Wire Konnect to KiCad IPC

Two hops must both work:

| Layer | What you see | Meaning |
|---|---|---|
| **Cursor → Konnect** | MCPs → **konnect Connected** | `konnect.exe` runs over stdio |
| **Konnect → KiCad** | `open_project` → **`ipc_available: true`** | Konnect knows the socket path **and** KiCad IPC is up |

**MCP Connected ≠ KiCad IPC connected.**

Cursor-launched Konnect does **not** receive `KICAD_API_SOCKET` from KiCad automatically (that env var is set when KiCad launches **plugins**, not when Cursor spawns `konnect.exe`).

### Option A — `.cursor/mcp.json` (recommended for Cursor)

Add `env.KICAD_API_SOCKET` with the **exact** address from Preferences (§ 2):

```json
{
  "mcpServers": {
    "konnect": {
      "command": "C:\\Users\\<YOU>\\Documents\\KiCad\\10.0\\3rdparty\\plugins\\com_github_mixelpixx_konnect\\bin\\konnect.exe",
      "env": {
        "KICAD_API_SOCKET": "ipc://C:\\Users\\<YOU>\\AppData\\Local\\Temp\\kicad\\api.sock"
      }
    }
  }
}
```

After editing: **Developer: Reload Window**. KiCad must stay running; if you restart KiCad, re-check the listening line — the path can change per session.

### Option B — Konnect settings dialog (KiCad UI)

1. **PCB Editor → Tools → External Plugins → Konnect**.
2. **Advanced → IPC Socket:** paste the same `ipc://…` address.
3. **Save** → creates:

```text
...\com_github_mixelpixx_konnect\settings.json
```

Example keys: `ipc_socket_path`, `kicad_cli`, `transport`, `log_level`.

Option A alone is enough for Cursor. Option B helps when starting Konnect from KiCad.

**Not configured in:** Plugin and Content Manager (install only).

### 5.1 — kicad-cli path (ERC/DRC from Agent)

KiCad installs `kicad-cli.exe` under `Program Files` — it is **not** on PATH by default. The **MCP** `konnect.exe` (Cursor) reads **`%APPDATA%\konnect\config.json`**, not the KiCad plugin `settings.json`.

**Fix (pick one):**

1. **Konnect user config (recommended)** — ask the agent to set `kicad_cli`, or edit:

```json
{
  "kicad_cli": "C:/Program Files/KiCad/10.0/bin/kicad-cli.exe"
}
```

in `%APPDATA%\konnect\config.json` (merge with existing keys). **Reload Cursor** after edit.

2. **System PATH** — add `C:\Program Files\KiCad\10.0\bin` to user or system PATH; restart Cursor.

3. **KiCad plugin settings** — `…\3rdparty\plugins\com_github_mixelpixx_konnect\settings.json` already has `kicad_cli` for Konnect started **from KiCad**; the MCP server in `.cursor/mcp.json` uses the Roaming config above.

**Verify:**

```powershell
& "C:/Program Files/KiCad/10.0/bin/kicad-cli.exe" --version
& "C:/Program Files/KiCad/10.0/bin/kicad-cli.exe" sch erc projects/wanos-board/wanos-board.kicad_sch
```

---

## 6. Verify in Agent chat

With KiCad running, **PCB Editor** open, MCP connected, and IPC env set:

### `open_project` (IPC smoke test)

Ask the agent to run **`open_project`**. Expected:

```json
{
  "kicad_ui_running": true,
  "ipc_available": true,
  "ipc_address": "ipc://C:\\Users\\<YOU>\\AppData\\Local\\Temp\\kicad\\api.sock",
  "open_board_count": 1,
  "open_boards": ["...\\something.kicad_pcb"]
}
```

Optional: pass a project path to check a specific board is open:

```text
open_project on docs/reference/wisc-board/211201 wisc2-5-3/wisc-v5.kicad_pro
```

→ `requested_open: true` when that PCB is the one loaded in PCB Editor.

### Other checks

- **List Konnect toolsets** — expect ~20 toolsets / 200+ tools after `list_toolboxes`.
- **`get_project_info`** — works on `.kicad_pro` paths without IPC (file read).
- **Live PCB edits / save via IPC** — require § 2–3 + § 5.

**File-only mode:** schematic file edits and some reads work **without** IPC. Live PCB undo integration and open-board checks **require** IPC.

---

## 7. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| MCP **Connected** but `ipc_available: false` | Konnect has no socket path | Add § 5 Option A or B; reload Cursor |
| `ipc_address: ""` | Same | Same |
| `open_board_count: 0` | PCB Editor not open or no board loaded | Open `.kicad_pcb` in layout (§ 3) |
| No **Listening at …** in Preferences | API off or KiCad started before enable | Restart KiCad; re-check § 2 |
| `api.sock` missing in `%TEMP%\kicad\` | Windows named pipe (§ 2) | Ignore; use Preferences line |
| Konnect not in Agent tools | MCP not loaded | Reload Cursor; check `.cursor/mcp.json` syntax |
| `settings.json` missing | Never saved Konnect dialog | Normal if using Option A only |
| `run_erc` / `Failed to spawn kicad-cli` | MCP Konnect cannot find CLI on PATH | Set `kicad_cli` in `%APPDATA%\\konnect\\config.json` (see § 5.1) **or** add KiCad `bin` to system PATH; reload Cursor |

Enable tracing (optional): KiCad env `KICAD_ENABLE_TRACE=1`, `WXTRACE=KICAD_API` — see [KiCad IPC docs](https://dev-docs.kicad.org/en/apis-and-binding/ipc-api/for-addon-developers/index.html).

---

## 8. Project layout

```text
projects/wanos-board/
  design.yaml
  constraints.md
  bom-targets.yaml
  components.xlsx          # BOM seed (LCSC)
  wanos-board.kicad_*      # Created at S1
  fabrication/
    JLCPCB_BOM_Template.xls
```

Datasheet PDFs → [`reference/datasheets/`](reference/datasheets/README.md) (lowercase filenames; gitignored).

Product spec → [`board-spec.md`](board-spec.md). WISC reference summaries → [`reference/wisc-board/`](reference/wisc-board/).

---

## 9. Verification commands (kicad-cli)

```powershell
$cli = "C:/Program Files/KiCad/10.0/bin/kicad-cli.exe"
$sch = "projects/wanos-board/wanos-board.kicad_sch"
$pcb = "projects/wanos-board/wanos-board.kicad_pcb"

& $cli sch erc $sch
& $cli pcb drc $pcb
```

Do not close **S1** / **L1** until ERC/DRC pass or waivers are in the phase file.

---

## 10. Notes

| Topic | Note |
|---|---|
| PCB tools | KiCad open + board in **PCB Editor** (IPC) |
| Schematic tools | Konnect can edit `.kicad_sch` without KiCad open |
| WISC reference | Read-only under `docs/reference/wisc-board/` — see [`.cursor/rules/wisc-boards-readonly.mdc`](../.cursor/rules/wisc-boards-readonly.mdc) |
| Freerouting | Konnect Specctra pipeline — lock HDMI nets first ([`hdmi-spi-eink.md`](hdmi-spi-eink.md)) |
| LCSC parts | Validate `components.xlsx` C-numbers at **J1** |
| MCP UI | **+ New** opening JSON only is expected — edit `.cursor/mcp.json` |
| Pipeline | **kickoff** before design locks; **implement** before KiCad edits on wanos-pcb-v1 |

| Pipeline | **Ops1** Done **2026-09-01** — [`todo/pipeline.md`](todo/pipeline.md) |
