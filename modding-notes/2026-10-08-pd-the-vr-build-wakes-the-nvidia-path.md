# 2026-10-08 (`/pd`, dev PC): the VR build wakes the game's NVIDIA 3D path with a stand-in nvapi.dll

**The game was not launched, and nothing here has been run in the game.** Everything is read from `TombRaider.exe` on
disk with `static-disasm.py` and a scan for NvAPI function ids. Addresses are for the current Steam build (ASLR: live
address = module base + VA − 0x400000). Board row: "CHOOSE HOW TO WAKE THE GAME'S OWN TWO-EYE LOOP, AND DESIGN THE VR
BUILD ON IT" (`MODEL: FABLE`, done on Opus on the dev PC per Tefa's 2026-10-06 rule).

## The decision: the NVIDIA route, through a stand-in `nvapi.dll`

Three ways to wake the loop were on the table. Chosen: **answer the game's own NVIDIA 3D Vision calls with a stand-in
`nvapi.dll` beside the exe**, the way `hard-reset-vr` already does (its two eyes reach the OpenXR simulator).

- **It is the path the game expects.** Nothing in the exe is patched to switch stereo on; the game's own start-up
  chain, its own two-eye loop and its own per-eye projection all run as written.
- **It hands us the eye boundary for free.** The game calls `NvAPI_Stereo_SetActiveEye` before each eye's draw, so
  the stand-in knows which eye is being drawn and tells our picture dll (export `trvr_on_active_eye`), which copies
  each eye's picture when the eye changes. That is exactly Hard Reset's d3d9 design, which works.
- **It survives patches better** than writing renderer bytes: the NvAPI ids are fixed by NVIDIA; only the read-only
  watch in the stand-in uses game addresses.
- **Our PCs are NVIDIA.** The AMD route is only tried when the adapter reports AMD's vendor id (`0x640a8a`), so it
  needs a `d3d11.dll` proxy that lies about the vendor (the `/gr` notes report that EOS's overlay can make such a
  proxy recurse) plus a stand-in for AMD's quad-buffer extension interface. TombRaiderVR does that; we would have to
  write all of it ourselves, nothing copied.
- **Forcing the flags directly** (TombRaiderVR's other half: renderer `+0xc19`/`+0xc1a`, the projection hook) stays the
  fallback if the NVIDIA chain refuses to run in a window.

## What the game asks NVIDIA for, read from the code `[inferred-static 2026-10-08]`

19 NvAPI functions are looked up (one static-lib wrapper each): Initialize, Stereo_IsWindowedModeSupported, Enable,
Disable, IsEnabled, CreateHandleFromIUnknown, DestroyHandle, Activate, Deactivate, IsActivated, Get/SetSeparation,
Get/SetConvergence, GetSurfaceCreationMode, CaptureJpegImage, SetNotificationMessage, SetActiveEye, SetDriverMode,
GetEyeSeparation. Hard Reset's stand-in answered 12 of them.

The chain that turns the NVIDIA mode on:

1. `0x64061f`: `Initialize()`; success sets `[0x1b12661]`.
2. `0x640673`: `Stereo_IsEnabled(&b)`; if `b`, **`SetDriverMode(2)` = direct** (`0x640689`), and on success
   **device+0x1d8 = 1**.
3. `0x640ac3`: `CreateHandleFromIUnknown(device, &device+0x1d4)`, **`SetActiveEye(handle, 2 = LEFT)`**,
   `SetNotificationMessage(handle, window, 3000)`, then **device+0x1d9 = 1**.
4. The mode question `0x641b40` answers **4 = NVIDIA** when the "Stereo 3D" setting byte (+0xa4) is on and both
   device bytes are set (after the 3D-monitor check).
5. Every frame `0x6424a0`: `IsActivated(handle, &b)`; on success **device+0xe8 = b**, the game's own "stereo on".
   ⚠️ Hard Reset ignores this answer when it is an error; Tomb Raider copies it, so the stand-in answers **1** by
   default (`nvapi_fake_activated_flag.txt` / `..._error.txt` switch to the other behaviours for comparison).
6. The two-eye loop `0x627b28` (gated by a virtual call `[vtable+0x64]`, not traced): eye flag renderer+0xc1a = 1,
   `SetActiveEye(handle, 2 = LEFT)`, draw, composite; flag 0, `SetActiveEye(handle, 1 = RIGHT)`, draw. **So the eye
   flag 1 is the LEFT eye, drawn first** (NVIDIA: RIGHT = 1, LEFT = 2, `nvapi_lite_stereo.h`, checked 2026-10-08).

**Correction to the 2026-09-30 note:** it put `SetDriverMode(2)` at `0x640ac3`. That call is at `0x640689`; the call
at `0x640ac3` is `SetActiveEye(handle, LEFT)`. The rest of that note stands.

## What was built

`staging/tomb-raider-2013-vr/proxy-nvapi` `[compile-verified 2026-10-08]`, `nvapi.dll` `1ae3c9b7cc4e`: all 19
functions; pass-through by default; fake stereo with `nvapi_fake_stereo.txt`; separation and convergence kept so a Set
is answered by the next Get (`nvapi_stereo.ini` sets the start values); a once-a-second read-only watch of the setting
byte, `[0x1b12661]`, device+0x1d8/+0x1d9/+0xe8 and the handle. Its self-test runs the game's call order in four modes,
63 checks, all pass `[verified-numerically 2026-10-08]`. **Not installed**: the game has never been launched here, and
the first-run checks come first.

## The plan after this

| step | gate | what |
| --- | --- | --- |
| 1 | FLAT | First run as shipped, then with our logging file, then a 1280x720 window, music off (the standing first-run rule). Note where the settings live (`Software\Crystal Dynamics\Tomb Raider` in HKCU `[inferred-static]`). |
| 2 | FLAT | Stand-in + `nvapi_fake_stereo.txt`, "Stereo 3D" on. Read `nvapi_proxy_log.txt`: the watch line (setting, ready, loaded all 1), and `SetActiveEye per 5 s: left N, right N` with N about the frame rate. |
| 3 | PD | The picture dll: a `dxgi.dll`/`d3d11.dll` stand-in exporting `trvr_on_active_eye`, copying each eye at the change, and the OpenXR bridge ported from Metro/The Evil Within. |
| 4 | PD then FLAT | Each eye's projection: replace `0x604df0`'s small off-axis edit with the headset's own per-eye field of view. The 3D Vision edit with convergence 0 is a pure sideways eye shift, which is the VR case. |
| 5 | PD then FLAT | Head tracking: the gameplay camera build `0xf69a0` (from TombRaiderVR's read). |

Step 2's outcomes:

| log shows | means |
| --- | --- |
| watch all 1, left and right counts equal and climbing | the loop runs: build step 3 |
| ready 0 | IsEnabled or SetDriverMode never reached us: is the stand-in loaded? (first log line) |
| loaded 0 with ready 1 | CreateHandle or the notification failed: their lines say which |
| all 1 but no SetActiveEye lines | the loop's own gate `[vtable+0x64]` is off: maybe fullscreen-only. Try fullscreen once, then trace that function |
| setting 0 | the "Stereo 3D" option is off or hidden: find its registry value after step 1 |

## Not established

- Anything live. Every address is read, none stepped through.
- Whether the NVIDIA chain runs in a window. Hard Reset's needed one answer changed to stay windowed; Tomb Raider's
  gate `[vtable+0x64]` is untraced.
- Whether deferred lighting is right per eye. The game shipped 3D Vision, so its own path is presumably eye-correct
  `[hypothesis]`.
- The exact registry value name for the setting (`StereoEnabled` is read by `0x644770`; the subkey is unchecked).
