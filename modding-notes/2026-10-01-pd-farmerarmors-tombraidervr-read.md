# 2026-10-01 (`/pd`, dev PC): farmerarmor's TombRaiderVR, read

**Read only, from the public repository (`github.com/farmerarmor/TombRaiderVR`, LGPL-2.1); nothing was copied and
nothing was run.** Learn from it, copy nothing (estate rule for others' mods).

## What it does `[reported]` (from its README and the source files read: `EngineDisplay.cpp`, `EngineCamera.cpp`, `Host.cpp`)

- **Synchronous stereo, both eyes in one game frame**, by driving the game's own stereo path: it hooks the
  per-eye projection function at program offset **`0x204df0`** (VA `0x604df0`) and uses renderer fields **`+0xc1a`**
  (eye, 0 = left / 1 = right), **`+0xc19`** (the game's native stereo-on flag), **`+0xb62`** (projection dirty),
  **`+0xa90` / `+0x990`** (projection override / fallback), plus hooks on scene creation (`0x21c8b0`), the draw path
  (`0x223bc0`, to know when both eyes are done), the HUD matrix (`0x238a90`) and the gameplay camera build
  (`0xf69a0`). The display code resizes the game's targets to the headset's eye size through the render-device object
  at base + `0x1712270`.
- **Head tracking is rotation only**: the headset rotation is applied to the camera's world matrix around the
  camera origin; no position.
- **No motion controllers** ("keyboard/mouse or the game's normal gamepad controls"); head-aim helpers instead.
- **A separate host process** drives the headset: the game side shares a D3D11 texture holding the eye pair
  (shared handle + keyed mutex), the host copies and submits it. Frame-paced on the game; no reprojection seen in the
  host. Runtime hidden behind its own `NativeBridge` layer.
- **First person is a fixed standing camera** that does not hide Lara's head or body; HUD on a virtual screen
  (`HUDScale`); pinned to Steam build **9573671**, checked by SHA-256.

## Where it agrees with our own static trace (independent confirmation)

Our 2026-09-30 trace found the same function (`0x604df0`, per-eye `P[2][0]`/`P[3][0]`), the same eye flag
(`+0xc1a`) and the same render-device global (`0x1b12270` = base + `0x1712270`), without having read this source.
Two independent readings now agree `[inferred-static 2026-09-30]` + `[reported]`. New to us: `+0xc19` native-stereo
flag, `+0xb62` projection-dirty (we had seen it set in the eye loop), `+0xa90`/`+0x990` projection override.

## Where it falls short of our standard (what ours should start past)

- **6DoF**: position tracking, not rotation only.
- **Motion controllers and hands**: aiming with the controllers; a visible body/hands rather than a floating head.
- **First person that follows the player** (not a fixed standing camera) and hides Lara's head.
- **In-process submission** (OpenXR, the estate default) instead of a second process copying a shared texture each
  frame, which adds a copy and a sync point per frame.
- **Not pinned to one exe hash**: refuse unknown builds by prologue checks, as our hooks do, but survive patches.

## Correction to our research note

The `/gr` topic of 2026-09-29 says the mod wakes the HD3D path with a stand-in AMD driver. The README and the three
source files read do not mention AMD, HD3D, `atidxx32` or ADL; they drive stereo by hooking the projection function
and setting the native stereo flag directly. Whether the AMD stand-in exists elsewhere in the repo (e.g. `vendor/`)
was not checked. Sent to the research lane as an inbox note.
