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
- **⭐ CHECKED 2026-09-28 (`/pd`, dev PC):** of the exe's 117 shaders, **31 declare `StereoOffset` and none reads
  it**; **`View` (+0) is read by none either**. Screen position comes from `WorldBuffer` (`b0`) `ViewProject` (+128)
  or `World` (+64) plus `SceneBuffer.__CameraPositionForCorrection` (+1184, camera-relative rendering)
  `[inferred-static 2026-09-28, n=117]`. ⚠️ The `bigfile.*.tiger` shaders are unopened. The exe still carries **both
  vendor stereo paths** — NVIDIA (`NvAPI_Stereo_IsEnabled`, `NvAPI_StereoSetDriverMode`) and **AMD HD3D**
  (`AmdDxExtCreate11`, "Loading AMD HD3D driver.") — plus `StereoEnabled` / `StereoDepth` / `StereoStrength`
  settings `[inferred-static 2026-09-28]`. So stereo was most likely CPU-driven (scene drawn twice), the route
  farmerarmor's DeusExHRVR drives on the sibling Crystal engine (`/gr` inbox 2026-09-23, `[reported]`); geo-11 users
  report re-enabling the 3D Vision path on the current build (`/sr` inbox 2026-09-17, `[reported]`, thread not
  read). Note: `modding-notes/2026-09-28-pd-unpaused-stereooffset-is-unread-but-hd3d-is-there.md`.
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

**2026-10-01 (`/pd`): farmerarmor's TombRaiderVR independently uses the same hook points** `[reported]`: the per-eye
projection function `0x604df0` (offset `0x204df0`), eye flag renderer `+0xc1a`, render device base + `0x1712270`;
and adds renderer `+0xc19` (native stereo on), `+0xb62` (projection dirty), `+0xa90`/`+0x990` (projection override /
fallback), scene creation `0x21c8b0`, draw `0x223bc0`, HUD matrix `0x238a90`, gameplay camera build `0xf69a0`.
Rotation-only, no controllers, separate host process. Note `modding-notes/2026-10-01-pd-farmerarmors-tombraidervr-read.md`.
**Corrected 2026-10-08:** TombRaiderVR ALSO ships the stand-in AMD DLLs (`vendor/`: `atidxx32`, `atiadlxy`, a `d3d11` proxy; from effcol's wiz3D, LGPL 2.1) `[reported 2026-10-04]`; the 10-01 read missed that folder. Both halves together are its route; the §"Inbox folds, 2026-09-29" paragraph stands.

**2026-10-01 (`/pd`): the `.tiger` shaders do not read `StereoOffset` either.** All 171,698 CDRM containers in
`bigfile.000–003.tiger` inflated with no error (`dev-archive/tools/tiger_cdrm_scan.py`): 25,047 DXBC shaders, 0 that
declare `StereoOffset` `[inferred-static 2026-10-01, n=25047]`. The material shaders' `SceneBuffer` is a smaller,
1,200-byte layout (`View` +0, `ScreenMatrix` +64, `__CameraPosition` +160, `CameraDirection` +176, `DepthToWorld`
+240, PSSM cascades, `PrevViewProject` +912, `ViewT` +1040, `__CameraPositionForCorrection` +1184) with no stereo
term `[inferred-static 2026-10-01]`. So the per-eye shift of the built-in 3D mode lives on the CPU side (the projection
edit at `0x604df0`), which is the hook route; nothing per eye needs patching in the shaders. Layout:
`dev-archive/recon/2026-10-01-tiger-shaders/`.

## ⭐ The built-in 3D mode, traced in the code (2026-09-30, `/pd`)

`[inferred-static 2026-09-30]` throughout; note `modding-notes/2026-09-30-pd-how-the-built-in-3d-mode-works.md`.
- **Switch:** `StereoEnabled` = byte at display-settings+0xa4 (`*(0x147c890)+0x720`; `StereoDepth` +0xa8,
  `StereoStrength` +0xac), from HKCU via `0x644770`. **Mode query `0x641b40`**: 0 unless enabled; 1 = AMD HD3D,
  4 = NVIDIA direct, 2/5 = 3D monitor.
- **AMD:** tried only when the adapter vendor ID is 0x1002/0x1022 (`0x640a8a`); `0x641e40` loads `atidxx32.dll`,
  `AmdDxExtCreate11`, then interface 2 (quad-buffer stereo) at device+0x1d0. This confirms TombRaiderVR's fake-AMD
  route from the code.
- **NVIDIA:** `NvAPI_Stereo_SetDriverMode(2)` = **direct mode** at `0x640689` (sets device+0x1d8); `0x640ac3` creates the handle, calls `SetActiveEye(LEFT)` and the notification, then device+0x1d9 = loaded (corrected 2026-10-08; the 09-30 read put SetDriverMode at `0x640ac3`).
- **Two-eye loop:** `0x627b28`: eye flag renderer+0xc1a = 1, `SetActiveEye(2)`, draw (`0x604100`); flag 0,
  `SetActiveEye(1)`, draw.
- **Per-eye projection:** `0x604df0(P, eye, sep, conv)` sets `P[2][0] = ∓sep/1000`, `P[3][0] = ±|conv|`; sep =
  renderer+0xc08 (default 5.0), conv = +0xc0c (default 20.0) (`0x61668b`); called from `0x62a9ab`, `0x63394e`.
- **VR route this opens:** wake the existing loop, replace `0x604df0`'s output with the headset's per-eye projection,
  capture each eye after its draw `[hypothesis]`.

## Inbox folds, 2026-09-29

**How TombRaiderVR switches on the shipped HD3D stereo path (`/gr` 2026-09-29).** The game's own stereo renderer draws the second eye (top-and-bottom in one double-height target, same frame); the mod wakes it with stand-in AMD driver-extension (`atidxx32.dll`) and ADL DLLs plus a `d3d11.dll` proxy that reports AMD's vendor ID on every adapter, so it works on NVIDIA/Intel; the in-game Stereo 3D option must be on; pinned to Steam build 9573671 `[reported]`. Hazards for any proxy of ours: a local `dxgi.dll` proxy never loads under Steam's overlay, and EOS's overlay can make a lazily-resolving `d3d11.dll` proxy recurse and drop the game to DX9 `[reported]`. ⚠️ The mod's repo was created 2026-09-19, not years ago as the board said. Topic: `external-research/topics/2026-09-29-tombraidervr-wakes-the-hd3d-path-with-a-fake-amd-driver.md`.

## ⭐ The VR build's wake-up route: the NVIDIA path through a stand-in nvapi.dll (2026-10-08, `/pd`)

`[inferred-static 2026-10-08]`; note `modding-notes/2026-10-08-pd-the-vr-build-wakes-the-nvidia-path.md`.
- **Chosen:** answer the game's 3D Vision calls with our `nvapi.dll` (the Hard Reset pattern). No exe patch to wake
  stereo; the game's `SetActiveEye` calls give our picture dll each eye's boundary (`trvr_on_active_eye`). AMD route
  rejected (vendor-id lie + quad-buffer stand-in, AMD cards only); flag-forcing kept as the fallback.
- **The exe looks up 19 NvAPI functions.** The chain: Initialize -> `[0x1b12661]`; IsEnabled -> SetDriverMode(2) ->
  device+0x1d8; CreateHandle -> SetActiveEye(LEFT) -> SetNotificationMessage(window, 3000) -> device+0x1d9; mode 4
  needs the setting byte and both device bytes. **Per frame IsActivated -> device+0xe8** (the game copies the answer,
  unlike Hard Reset), so the stand-in answers 1.
- **Eye order:** the loop sets eye flag 1 with `SetActiveEye(2)` = NVIDIA's LEFT, draws, then flag 0 with RIGHT (1)
  (`nvapi_lite_stereo.h`: RIGHT = 1, LEFT = 2). So **renderer+0xc1a = 1 is the left eye, drawn first**.
- **Built, not installed:** `staging/tomb-raider-2013-vr/proxy-nvapi` `1ae3c9b7cc4e` `[compile-verified 2026-10-08]`,
  self-test 63/63 in four modes `[verified-numerically 2026-10-08]`. The game has never been launched on either PC.
