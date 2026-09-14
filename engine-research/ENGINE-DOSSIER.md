# Engine Dossier — Tomb Raider (2013) (Foundation)

> One consolidated, living reference for this game's engine, filled in as the
> `PLAYBOOK.md` phases are worked. Chronological blow-by-blow belongs in the
> `dev-archive/` and `modding-notes/` folders; this file is the *distilled current
> truth*. Update it whenever a fact changes; correct false leads in place.

**Status:** M0, full static pass done (2026-09-13 home, 2026-09-14 dev PC after Tefa downloaded it); the game has **not** been launched. · **VR-readiness verdict:** ⭐ **the strongest of the 2026-09-13 batch on paper.** Its shipped shaders carry a named `StereoOffset` constant alongside the view matrix, inverse projection and camera position — all readable off disk. Nothing has been run, and a deferred renderer plus an Epic Online Services hard import are the two real complications.

## 1. Identity
- Game / build / version: Tomb Raider (2013), Steam app 203160, exe `TombRaider.exe` (linked 2022-09-22, a late patch build, not the 2013 original). Ships with the DLC packs and the Survival Edition content folder.
- Platform & store; unofficial port? (extra fragility/legal notes): Steam (PC). Official release, not a fan port.
- Legitimacy: owned copy confirmed.

## 2. Engine lineage
- Family / base engine and how it was modified: Crystal Dynamics' Foundation engine `[reported]`; **internally the namespace is `cdc` throughout** `[inferred-static 2026-09-14]`. Scaleform strings are present in the exe `[inferred-static 2026-09-13]`.
- Middleware (animation, audio, physics, megatexture, CUDA, etc.):
- Distinctive file formats / build tags / symbol naming: Data lives in `.tiger` archives (`bigfile.*`, `patch*.*`, `title.*`, `DLC\PACK*.000.tiger`), **still not opened**. ⭐ **The `.shad` section is no longer unknown: it holds 117 DXBC shaders with their reflection data intact** (79 constant-table chunks, 86 shader chunks) `[inferred-static 2026-09-14]` — which is what made §6 answerable with nothing running. ⚠️ 117 is small for a game this size, so these are probably a core subset with the rest inside the `.tiger` archives.

## 3. Binary & memory
- 32/64-bit, size, module base, ASLR behaviour (stable base? relocations?): **32-bit** (PE32), `TombRaider.exe` 19.2 MB, linked 2022-09-22. Ordinary sections plus `.shad`; no protection-shaped section `[inferred-static 2026-09-13]`.
- Renderer API (D3D11/12, DXGI, GL, Vulkan) with evidence: ⚠️ **CORRECTED 2026-09-14.** `d3d11.dll`, `dxgi.dll`, `d3d9.dll` and `nvapi.dll` are named in the exe **as strings only — none of them is in the import table, which contains no graphics API at all** `[inferred-static 2026-09-14]`. The renderer is therefore resolved **dynamically at runtime**.
  - ⭐ Same shape as **Alan Wake** on this account; `staging/alan-wake-vr/proxy-d3d9/README.md` records what that cost. A same-named proxy DLL in the game folder can still work (the exe's own directory is searched first for `LoadLibrary` too), but it cannot be assumed the way a static import can, and *which* API the game picks is a runtime decision.
  - The actual pipeline is **deferred DX11**, with its passes named in the binary: `PCDX11DeferredShadingPassCallbacks`, `PCDX11DepthPassCallbacks`, `PCDX11CompositePassCallbacks`, `PCDX11AlphaBloomFSXPassCallbacks`, `PCDX11DecalApplyPassCallbacks`, plus `PCDX11ConstantBuffer`, `PCDX11ComputeShader`, `PCDX11DefaultRenderTarget`, `PCDX11DepthBuffer` `[inferred-static 2026-09-14]`.
- Developer console / cvar system present? how opened?: The exe imports `AllocConsole`, `FreeConsole`, `GetConsoleWindow` and `SetConsoleScreenBufferSize`, so it **can** open a Windows console `[inferred-static 2026-09-14]`. ⚠️ Nothing found says a player can reach one. Cheat strings exist (`Skew Cheat Enabled!`, `Skew Cheat Disabled, reverting to Default Gravity.`, `evControlCheat`).

## 4. DRM / anti-debug & injection foothold
- DRM (CEG/Denuvo/GOG/none); launch-time-debugger behaviour: Steam API, plus an Epic Online Services SDK DLL (`EOSSDK-Win32-Shipping.dll`) shipped beside the exe `[inferred-static 2026-09-13]`. No Denuvo string or protection section found. Not tested live.
- Attach workflow that works: not yet tested.
- Injection vector that works (proxy DLL name / injector / framework): not yet tested.

## 5. Threading & frame structure
- Immediate context only, or deferred contexts + command lists?:
- Which thread(s) do what; render-thread name(s):
- One-frame walkthrough (record → replay → present):

## 6. Camera & projection delivery (the crucial section)

⭐ **Answered statically on 2026-09-14, off disk, with no game running** — evidence and method:
`dev-archive/recon/2026-09-14-dev-pc-static-pass/`.

- How the world transform reaches the GPU: a **shared per-frame constant buffer named `SceneBuffer`**, used by 31 of the 117 shaders embedded in the exe's `.shad` section `[inferred-static 2026-09-14]`. The `.shad` section holds **117 DXBC shaders with their reflection data intact** (79 constant-table chunks), which is why names and offsets are available without a capture.
- Exact constant-buffer slot, parameter name(s), byte offset(s): `SceneBuffer`, 1360 bytes —

  | offset | name | size |
  | --- | --- | --- |
  | +0 | `View` | 4x4 |
  | +64 | `ScreenMatrix` | 4x4 |
  | +160 | `__CameraPosition` | float3 |
  | +176 | `CameraDirection` | float3 |
  | +240 | `DepthToWorld` | 4x3 |
  | +288 | `DepthToView` | float4 |
  | +336 | `ClipPlane` | float4 |
  | +848 | `WorldToPSSM0` | 4x4 |
  | +912 | `PrevViewProject` | 4x4 |
  | +976 | `PrevWorld` | 4x4 |
  | +1040 | `ViewT` | 4x4 |
  | +1280 | `InverseProjection` | 4x4 |
  | **+1344** | **`StereoOffset`** | **float4** |

  Reproduce with `flat-to-vr-RE-toolkit/tools/dxbc-reflect.py <shad-dump> find SceneBuffer`.
- ⭐ **`StereoOffset` already exists in the shaders.** This game shipped in the 3D-Vision era and its renderer was built able to shift the view for an eye. ⚠️ **That proves the shaders have a stereo term; it proves nothing about whether anything still fills it.** The code that wrote it may be gone, disabled, or permanently zero in this 2022 patch build — **unchecked, and the first thing to check** `[hypothesis]`.
- ⚠️ **`View` at +0 is a name, not a proof of contents.** `PrevViewProject` being explicitly a view-*projection* is weak evidence that plain `View` is view-only, but nothing here settles it. One frame, or the maths checked against a known camera, would.
- The per-eye override maths (`K_eye = …`): not derived. ⚠️ **A deferred renderer complicates it** — lighting reconstructs world position from depth, so `DepthToWorld`, `DepthToView` and `InverseProjection` must move in step with any per-eye view shift. Not fatal, but more work than a forward renderer.

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
- ⭐ **The best static starting position of the 2026-09-13 batch:** named camera constants with byte offsets, and a `StereoOffset` term already in the shaders — all obtained with nothing running `[inferred-static 2026-09-14]`.
- ⚠️ **`EOSSDK-Win32-Shipping.dll` is a HARD static import, 108 functions** `[inferred-static 2026-09-14]` — Windows resolves it before any game code runs. This is this project's equivalent of Dead Space 2's activation layer. Whether it demands an account at startup is untested, and it is the Burnout Paradise lesson's question.
- ⚠️ **ASLR is ON**, so addresses are valid within one run only — resolve by module base + offset.
- ⚠️ **The renderer is not a static import**, so the injection route is less certain than for Witcher 2, Hard Reset or Dead Space 2. See §3.
- ⚠️ **Deferred shading** means a per-eye view shift is not enough on its own; the depth-reconstruction terms must move with it.
- 117 shaders is small for a game this size, so these are probably a core subset with the rest inside the `.tiger` archives. Unchecked.
