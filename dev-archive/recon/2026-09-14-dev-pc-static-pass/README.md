# 2026-09-14 — Tomb Raider (2013), dev-PC static pass (NO LAUNCH)

**Machine:** dev PC `DESKTOP-V8GTSIR`. Tefa downloaded the game this afternoon after the morning's
install check found nothing on disk. **Install:** `D:\Program Files (x86)\Steam\steamapps\common\Tomb Raider`,
Steam app 203160, fully installed `[inferred-static 2026-09-14]`.

**The game was not launched.** Everything here is PE headers, section data and shader reflection read
off disk.

## Files here

| File | What it is |
| --- | --- |
| `pe-imports.txt` | PE header, sections and the full import table |
| `cdc-engine-classes.txt` | the engine's own class names in the `cdc` namespace |
| `renderer-classes.txt` | the DX11 renderer's named passes and resources |
| `console-and-cheat-strings.txt` | console and cheat strings |
| `install-listing.txt` | install root contents |

## ⭐⭐ The headline: the shaders carry a `StereoOffset`, and the whole scene buffer is readable off disk

The 2026-09-13 board asked what the `.shad` section holds. **It holds 117 Direct3D shaders with
their reflection data intact** — 79 constant-table chunks among them `[inferred-static 2026-09-14]`.
That is the single most valuable kind of find in the static toolbox, because reflection data carries
**names and byte offsets** rather than anonymous registers.

Reflecting them gives the engine's main per-frame constant buffer, `SceneBuffer`, used by 31 of the
117 shaders, 1360 bytes:

```
+0     View                             4x4 matrix
+64    ScreenMatrix                     4x4 matrix
+160   __CameraPosition                 float3
+176   CameraDirection                  float3
+240   DepthToWorld                     4x3 matrix
+848   WorldToPSSM0                     4x4 matrix
+912   PrevViewProject                  4x4 matrix
+976   PrevWorld                        4x4 matrix
+1040  ViewT                            4x4 matrix
+1280  InverseProjection                4x4 matrix
+1344  StereoOffset                     float4        <-- !!
```

(Full listing reproducible with `flat-to-vr-RE-toolkit/tools/dxbc-reflect.py <dump> find SceneBuffer`.)

⭐ **`StereoOffset` is the thing to notice.** A per-eye offset term already exists *inside the
shaders* — this game shipped in the 3D-Vision era and its renderer was built to be able to shift the
view for an eye. Alongside it sit everything else the job needs, by name and at a known offset:
the view matrix, the inverse projection, the camera position and the camera direction.

⚠️ **What that does NOT mean, and this matters.** The constant existing proves the **shaders** have a
stereo term. It proves nothing about whether anything still *fills* it — the code that wrote it may
be gone, disabled, or permanently zero in this 2022 patch build. **Unchecked, and it is the first
thing to check.** `[hypothesis]`

⚠️ Also: `View` at +0 is a name, not a proof of contents. `PrevViewProject` at +912 being explicitly
called a view-*projection* is weak evidence that plain `View` is view-only, but nothing here
establishes which. That needs one frame captured, or the maths checked against a known camera.

## The engine

The `cdc` namespace throughout is Crystal Dynamics' own engine core `[inferred-static 2026-09-14]`.
The renderer is a **deferred DX11 pipeline** with its passes named in the binary:
`PCDX11DeferredShadingPassCallbacks`, `PCDX11DepthPassCallbacks`, `PCDX11CompositePassCallbacks`,
`PCDX11AlphaBloomFSXPassCallbacks`, `PCDX11DecalApplyPassCallbacks`,
`PCDX11DepthDependentPassCallbacks`, plus `PCDX11ConstantBuffer`, `PCDX11ComputeShader`,
`PCDX11DefaultRenderTarget`, `PCDX11DepthBuffer`.

⚠️ **Deferred shading is a real complication for stereo work**, and worth flagging at the start
rather than discovering later: a deferred renderer reconstructs world position from depth, so a
naive per-eye view-matrix shift leaves the lighting reading from the wrong eye's depth buffer.
`DepthToWorld`, `DepthToView` and `InverseProjection` in `SceneBuffer` are exactly the terms that
would have to move in step. **This is not a fatal problem, but it is more work than a forward
renderer.**

## Binary facts

| | |
| --- | --- |
| `TombRaider.exe` | **32-bit**, linked 2022-09-22 `[inferred-static 2026-09-14]` |
| Module base | `0x400000`, **ASLR ON**, NX on — addresses valid within one run only |
| Sections | usual set plus `.shad` (649 KB, executable-marked, holds the shaders), `.gfids`, `_RDATA`, `CPADinfo` |
| **Renderer imports** | ⚠️ **none.** `d3d11.dll`, `dxgi.dll`, `d3d9.dll` and `nvapi.dll` appear only as **strings**, not in the import table |
| Online | ⚠️ **`EOSSDK-Win32-Shipping.dll` is a HARD static import — 108 functions** |
| Other imports | `steam_api.dll` (15), `binkw32.dll`, `WININET`, `CRYPT32`, `dbghelp`, `faultrep` |
| Console | `AllocConsole`, `FreeConsole`, `GetConsoleWindow`, `SetConsoleScreenBufferSize` — it can open a Windows console |
| Cheats | `Skew Cheat Enabled!`, `Skew Cheat Disabled, reverting to Default Gravity.`, `evControlCheat` |

⚠️ **CORRECTION to the 2026-09-13 note**, which read *"Direct3D 11 and Direct3D 9 are both named in
the exe (`d3d11.dll`, `dxgi.dll`, `d3d9.dll`)"*. They are named, but **they are not imported** — the
import table contains no graphics API at all `[inferred-static 2026-09-14]`. The renderer is therefore
loaded **dynamically at runtime**.

⭐ That is a familiar shape on this account: **Alan Wake does the same thing**, and
`staging/alan-wake-vr/proxy-d3d9/README.md` documents what it cost there. A same-named proxy DLL in
the game folder can still work (an exe's own directory is searched first, for `LoadLibrary` too), but
it cannot be assumed the way it can for a static import, and *which* API the game picks is a runtime
decision.

⚠️ **The Epic Online Services import is the launch risk here**, the equivalent of Dead Space 2's
activation layer: 108 statically imported functions means Windows resolves that DLL before any game
code runs. Whether it demands an account at startup is untested.

## What this does NOT establish

- Nothing has been run.
- No shader was disassembled — only its reflection metadata read. The *use* of `StereoOffset` inside
  the shader code is unexamined.
- Whether the `.tiger` archives hold more shaders than the 117 in the exe is unchecked; 117 is small
  for a game this size, so these are probably a core subset with the rest in the archives.
- The console strings show the game *can* open a console; nothing found says a player can.
