# Engine Dossier — Tomb Raider (2013) (Foundation)

> One consolidated, living reference for this game's engine, filled in as the
> `PLAYBOOK.md` phases are worked. Chronological blow-by-blow belongs in the
> `dev-archive/` and `modding-notes/` folders; this file is the *distilled current
> truth*. Update it whenever a fact changes; correct false leads in place.

**Status:** M0, first static look (2026-09-13); the game has not been launched yet. · **VR-readiness verdict:** TBD. Nothing seen so far rules it out.

## 1. Identity
- Game / build / version: Tomb Raider (2013), Steam app 203160, exe `TombRaider.exe` (linked 2022-09-22, a late patch build, not the 2013 original). Ships with the DLC packs and the Survival Edition content folder.
- Platform & store; unofficial port? (extra fragility/legal notes): Steam (PC). Official release, not a fan port.
- Legitimacy: owned copy confirmed.

## 2. Engine lineage
- Family / base engine and how it was modified: Crystal Dynamics' Foundation engine `[reported]`. Scaleform strings are present in the exe `[inferred-static 2026-09-13]`.
- Middleware (animation, audio, physics, megatexture, CUDA, etc.):
- Distinctive file formats / build tags / symbol naming: Data lives in `.tiger` archives (`bigfile.*`, `patch*.*`, `title.*`, `DLC\PACK*.000.tiger`), not yet looked at. The exe also carries a `.shad` section (about 650 KB), whose contents are not yet known.

## 3. Binary & memory
- 32/64-bit, size, module base, ASLR behaviour (stable base? relocations?): **32-bit** (PE32), `TombRaider.exe` 19.2 MB, linked 2022-09-22. Ordinary sections plus `.shad`; no protection-shaped section `[inferred-static 2026-09-13]`.
- Renderer API (D3D11/12, DXGI, GL, Vulkan) with evidence: Direct3D 11 and Direct3D 9 are both named in the exe (`d3d11.dll`, `dxgi.dll`, `d3d9.dll`) `[inferred-static 2026-09-13]`; the game is known to offer both `[reported]`. Which one this install uses by default is not yet checked. NVAPI strings present.
- Developer console / cvar system present? how opened?: not yet investigated.

## 4. DRM / anti-debug & injection foothold
- DRM (CEG/Denuvo/GOG/none); launch-time-debugger behaviour: Steam API, plus an Epic Online Services SDK DLL (`EOSSDK-Win32-Shipping.dll`) shipped beside the exe `[inferred-static 2026-09-13]`. No Denuvo string or protection section found. Not tested live.
- Attach workflow that works: not yet tested.
- Injection vector that works (proxy DLL name / injector / framework): not yet tested.

## 5. Threading & frame structure
- Immediate context only, or deferred contexts + command lists?:
- Which thread(s) do what; render-thread name(s):
- One-frame walkthrough (record → replay → present):

## 6. Camera & projection delivery (the crucial section)
- How the world transform reaches the GPU (shared VP buffer / per-draw MVP /
  other), with **shader-reflection / disassembly evidence**:
- Exact constant-buffer slot, parameter name(s), byte offset(s), layout,
  handedness, row/column convention:
- Where projection `P` / FOV comes from:
- The per-eye override maths (`K_eye = …`):

## 7. Constant-buffer fill mechanism
- Map/DISCARD ring / UpdateSubresource / D3D11.1 offset / **persistent map +
  memcpy** (trap):
- Can source contents be read cheaply (captured CPU pointer) or need staging
  read-back?:
- The chosen override patch point and why:

## 8. Pass inventory (by render target)
- Main scene (res/formats):
- Shadow passes (depth-only sizes):
- Post / AA chain (SMAA/TAA/motion vectors; downscale sizes):
- UI / HUD (how it's kept separate):

## 9. cvar / console cheat sheet
| command / cvar | effect | use |
|---|---|---|
| | | |

## 10. Autonomous harness recipe (this game)
- Launch to a known scene (commands used):
- In-process input / camera drive method that worked:
- Frame-capture method; where images land:

## 11. Dead ends & false leads (save future time)
- none yet.

## 12. Open risks toward the North Star
- Nothing blocking seen yet. An unprotected 32-bit exe with a choice of Direct3D 9 or 11 gives two routes in, and this account has worked both.
- ⚠️ Whether the Epic Online Services piece wants an account sign-in at launch is unknown. Check it on the first launch (the Burnout Paradise lesson).
