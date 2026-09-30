# 2026-09-30 (`/pd`, dev PC): how Tomb Raider's built-in 3D mode switches on and draws the second eye

**The game was not launched, and nothing here has been run.** Everything is read from `TombRaider.exe` on disk
(no protection on the code), with `static-disasm.py`. Addresses are for the current Steam build; the exe has ASLR,
so live addresses are module base + (VA − 0x400000).

## What switches it on

- **The setting.** "Stereo 3D" is a byte at **+0xa4 of the display-settings block** (`*(0x147c890) + 0x720`), read
  from the registry value `StereoEnabled` under HKCU by `0x644770` (called from `0x53d3f0`). `StereoDepth` is the
  float at +0xa8 and `StereoStrength` at +0xac (written back ×1000 by `0x643a00`) `[inferred-static 2026-09-30]`.
- **The mode question.** `0x641b40` (thiscall on the render device `*(0x1b12270)`) returns **0 unless that byte is
  set**, then: **1 = AMD HD3D** (the chosen display mode is one of AMD's stereo modes), **4 = NVIDIA** (3D Vision
  loaded at device+0x1d9 and enabled at +0x1d8), or **2 / 5 = a 3D monitor** (row-interleaved screens listed in
  `stereo_monitors.txt`) `[inferred-static 2026-09-30]`. Seven places in the renderer ask it.
- **AMD is only tried on an AMD card.** At device creation (`0x640a8a`) the adapter's vendor ID must be **0x1002
  or 0x1022** before "Loading AMD HD3D driver." runs `0x641e40`: `LoadLibrary("atidxx32.dll")` →
  `AmdDxExtCreate11(device, &ext)` (device+0x1cc) → `ext->GetExtInterface(2)` = the quad-buffer stereo interface
  (device+0x1d0) `[inferred-static 2026-09-30]`. This **confirms, from the code, how farmerarmor's TombRaiderVR works**:
  report AMD's vendor ID and supply a stand-in `atidxx32.dll` (dossier, `/gr` 2026-09-29, previously `[reported]`).
  `0x622275` then switches quad-buffer stereo on when the mode is 1.
- **NVIDIA uses DIRECT mode.** If NvAPI stereo is present (device+0x1d8), `0x640ac3` creates a stereo handle, calls
  `NvAPI_Stereo_SetDriverMode(2)` (2 = direct: the game draws each eye itself) and sets device+0x1d9
  ("m_nvStereoLoaded = true") `[inferred-static 2026-09-30]`.

## How it draws the second eye

- **The whole scene is drawn twice.** In `0x627b28` (the NVIDIA path): set the eye flag **renderer+0xc1a = 1**,
  `NvAPI_Stereo_SetActiveEye(handle, 2)`, draw the scene (`0x604100`), then flag = 0, `SetActiveEye(handle, 1)`, and
  draw again `[inferred-static 2026-09-30]`. The flag is also read by the final composite (`0x636b50`, per mode) and
  by a per-draw cache (`0x61bbbc`) that re-records state when the eye changes.
- **The camera change per eye is one small edit to the projection.** `0x604df0(matrix, eye, sep, conv)` writes
  `P[2][0] = ∓sep/1000` and `P[3][0] = ±|conv|` (sign by eye): a horizontal off-axis shift, the 3D-Vision style
  formula. It is called from `0x62a9ab` and `0x63394e` only when `sep` (renderer+0xc08) is not zero; `conv` is
  renderer+0xc0c. Defaults at renderer creation (`0x61668b`): **sep 5.0, conv 20.0**, eye flag 1
  `[inferred-static 2026-09-30]`.

## What it means for a VR mod

The game already has a working two-eye render loop, an eye flag, and a single function that sets each eye's
projection. A VR build does not need to invent stereo here; it needs to:

1. **wake the loop** without a 3D Vision driver or an AMD card (a stand-in for the part the game checks: a fake
   NvAPI stereo handle, or the fake-AMD route TombRaiderVR already proves), and
2. **replace each eye's projection** in `0x604df0` with the headset's own (off-centre field of view and the real
   eye distance), and **take each eye's picture** after its draw instead of letting a driver interleave them.

Which wake-up route is best, and whether the scene draw also needs the eye's position (not just its projection)
for lighting and reflections, is the design decision for the next session.

## Not established

- Anything live. Every address is read, none has been stepped through.
- Where sep and conv are updated after start-up (only the defaults and one write at `0x7243db` were found).
- Which eye value (1 or 2) NVIDIA treats as left; the code draws eye value 2 first.
- The AMD path's own per-eye loop (it may share `0x604df0`; not traced).
