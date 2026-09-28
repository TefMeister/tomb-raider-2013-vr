# 2026-09-28 — /pd: un-paused; `StereoOffset` is read by nothing, but the exe still carries both vendor stereo paths

Dev PC, `/pd`, no game launched, nothing run. The game is installed on the dev PC now
(`D:\Program Files (x86)\Steam\steamapps\common\Tomb Raider`); the 2026-09-14 "not installed" entry is stale.

## Why this project is running again

Tefa, 2026-09-28: the existing VR mods for this game are years old and not up to our standards, so the project is
**un-paused**. farmerarmor's TombRaiderVR stays a reference to learn from, not a reason to stop.

## What the shaders say

All 117 DXBC shaders were pulled out of `TombRaider.exe` (the `.shad` data) and disassembled (`dxbc-usage.py`).

- **`SceneBuffer.StereoOffset` (+1344, slot 84) is declared by 31 shaders and READ BY NONE of the 117**
  `[inferred-static 2026-09-28, n=117]`. In these shaders the term is vestigial: the compiler kept the
  declaration and no instruction touches it. This answers the old `[PD]` row for the exe's shaders.
- **`SceneBuffer.View` (+0) is not read by any of them either.** Where a vertex shader builds its screen position,
  the chain runs through `WorldBuffer` (`b0`): `ViewProject` (+128, slots 8–11) in 3 shaders, `World` (+64) in 2,
  with `SceneBuffer` `__CameraPositionForCorrection` (+1184) — i.e. camera-relative rendering — and
  `PrevViewProject` (+912) on the same chains (motion vectors). Two screen-space shaders use `ScreenMatrix` (+64)
  `[inferred-static 2026-09-28, n=117]`. So the old question "is `View` a view or a view-projection?" matters less
  than thought: the world path uses `WorldBuffer.ViewProject`.
- ⚠️ **These 117 are only the shaders compiled into the exe.** The bulk of the game's material shaders are most
  likely in the `bigfile.*.tiger` archives, unopened. Whether *those* read `StereoOffset` is still open.

## What the exe says

String scan of `TombRaider.exe` `[inferred-static 2026-09-28]`:
- **NVIDIA 3D Vision path:** `NvAPI_StereoSetDriverMode`, `NvAPI_Stereo_IsEnabled`, `m_nvStereoEnabled`.
- **AMD HD3D path:** `Loading AMD HD3D driver.`, `AmdDxExtCreate11`, `AMD Stereo Modes:` — the same kind of vendor
  entry point farmerarmor's DeusExHRVR drives on the sibling Crystal engine (inbox note from `/gr`, 2026-09-23).
- **Settings:** `StereoEnabled`, `StereoDepth`, `StereoStrength` (also as UTF-16 text, i.e. settings names, most
  likely registry values under the game's key; no key exists on the dev PC yet because it has never been launched).
- No `3DVision_Config.xml` in the install (the `/sr` note's downgrade-era route) `[inferred-static 2026-09-28]`.

## What it means

The stereo in this game was probably done by drawing the scene twice with a shifted camera, driven from the CPU
through the vendor path, not by a per-eye term inside the shaders `[hypothesis]`. That is the better news: it is
the route DeusExHRVR proved on the sibling engine.

## NOT established

- Whether the `bigfile` shaders read `StereoOffset`.
- Whether the HD3D path can be reached on a non-AMD card (DeusExHRVR's approach is the reference to read).
- Anything at all about the running game. It has never been launched on the dev PC.
