# First static look (2026-09-13)

Read from the installed Steam copy on the home PC, without launching the game. Every claim
below is `[inferred-static 2026-09-13]` unless tagged otherwise: it comes from reading file headers
and strings, not from running anything.

- **Install:** `Tomb Raider`, 15 GB.
- **Identity:** Tomb Raider (2013), Steam app 203160, exe `TombRaider.exe` (linked 2022-09-22, a late patch build, not the 2013 original). Ships with the DLC packs and the Survival Edition content folder.
- **Engine:** Crystal Dynamics' Foundation engine `[reported]`. Scaleform strings are present in the exe `[inferred-static 2026-09-13]`.
- **Binary:** **32-bit** (PE32), `TombRaider.exe` 19.2 MB, linked 2022-09-22. Ordinary sections plus `.shad`; no protection-shaped section `[inferred-static 2026-09-13]`.
- **Renderer:** Direct3D 11 and Direct3D 9 are both named in the exe (`d3d11.dll`, `dxgi.dll`, `d3d9.dll`) `[inferred-static 2026-09-13]`; the game is known to offer both `[reported]`. Which one this install uses by default is not yet checked. NVAPI strings present.
- **Protection:** Steam API, plus an Epic Online Services SDK DLL (`EOSSDK-Win32-Shipping.dll`) shipped beside the exe `[inferred-static 2026-09-13]`. No Denuvo string or protection section found. Not tested live.
- **Other files:** Data lives in `.tiger` archives (`bigfile.*`, `patch*.*`, `title.*`, `DLC\PACK*.000.tiger`), not yet looked at. The exe also carries a `.shad` section (about 650 KB), whose contents are not yet known.

## Method

PE headers read with a short script: machine type, link timestamp, section names and sizes.
Then a case-insensitive search of each binary for renderer DLL names (`d3d9`, `d3d11`, `d3d12`,
`dxgi`, `vulkan-1`, `opengl32`), protection markers (`denuvo`, `securom`, `.bind`) and middleware
names. A string match shows a name is present in the file, not that the code path is used.

## Risks noted

- Nothing blocking seen yet. An unprotected 32-bit exe with a choice of Direct3D 9 or 11 gives two routes in, and this account has worked both.
- ⚠️ Whether the Epic Online Services piece wants an account sign-in at launch is unknown. Check it on the first launch (the Burnout Paradise lesson).
