# TombRaiderVR wakes the game's own HD3D stereo path with a fake AMD driver, on any GPU

**Found:** 2026-09-29, `/gr` estate sweep (CHECK-IN), aimed at the board's top `[PD]` row
(*"find the code behind `StereoEnabled` and the AMD HD3D / NVIDIA stereo paths: what switches it on and
how it draws the second eye"*) and its third row (*"read farmerarmor's TombRaiderVR source"*).
**Source:** farmerarmor, *TombRaiderVR* — <https://github.com/farmerarmor/TombRaiderVR> (LGPL-2.1).
Read in GitHub's own viewer (README, file list, header comments); nothing downloaded, nothing copied.

## What it does, in our words

Everything below is `[reported]` — the author's README and source comments, not run by us.

1. **It does not render two eyes itself.** It makes the game believe an AMD HD3D stereo driver is
   present, so the game's **shipped** stereo renderer runs and draws both eyes in the same frame, the
   left eye in the top half and the right in the bottom half of a double-height target.
2. **Three small stand-in DLLs do the waking**, all derived from effcol's *wiz3D* (an iZ3D-based
   universal stereo wrapper, <https://github.com/effcol/wiz3D>):
   - a stand-in for AMD's driver extension DLL (`atidxx32.dll`) that answers the game's
     quad-buffer stereo interface, so the HD3D path turns on even on NVIDIA or Intel hardware;
   - a stand-in for the AMD display library (ADL);
   - a `d3d11.dll` proxy that makes every graphics adapter report AMD's vendor ID, and hooks the
     DXGI factory so the game's vendor check passes.
3. **A separate 64-bit host program** takes the finished pair and hands both eyes to OpenXR.
4. **One pinned executable**: Steam build 9573671, checked by SHA-256 at install; other builds are
   refused. It also patches how the game sizes its render targets so they match the headset's eye
   resolution. The game's own **Stereo 3D option must be switched on in its graphics menu.**
5. **What works (author's headset testing):** native stereo framing, HUD and menus, mouse/pad bow
   aiming, optional head aiming (added 2026-09-26), automatic switching between immersive VR in
   gameplay and a virtual screen for cutscenes, a fixed-height first-person toggle.
6. **What it lacks:** no motion-controller aiming; first-person camera does not follow crouching or
   hide Lara's body; occasional bright flashes tied to an unidentified graphics setting; scripted
   camera shake only partly suppressible.

## Why it matters for this project

- **It answers the "how does the second eye get drawn" half of our top `[PD]` row** from the outside:
  the switch is the game's AMD quad-buffer stereo interface, reached through the driver-extension
  DLL the exe already names (`AmdDxExtCreate11` is one of the strings on our board). So the static
  hunt can start from **what the exe calls in that DLL** rather than from `StereoEnabled` alone
  `[hypothesis]`.
- **Two hazards worth copying into our own notes:**
  - Steam's overlay loads the system `dxgi.dll` before the game's imports resolve, so a local
    `dxgi.dll` proxy is never loaded here; the author uses a `d3d11.dll` proxy instead `[reported]`.
  - Epic Online Services' overlay patches `d3d11.dll`'s export table; a proxy that looks exports up
    lazily can end up calling itself and **pushes the game into its DX9 fallback** `[reported]`. Our
    board already flags EOS as a hard import, so this matters for any proxy we build.
- **"Where it falls short of our standard" is now a short, sourced list** (point 6 above): motion
  controllers, a body-aware first-person camera, and flash-free rendering are the gaps.

⚠️ **One fact for the board owner, not a verdict:** the repo was **created on 2026-09-19** and its
first release commit is dated the same day `[measured 2026-09-29, GitHub API]`, so TombRaiderVR is
ten days old, not years old. The un-pause decision is Tefa's and this does not change it; it only
means the mod is young and actively moving (commits on 09-19, 09-22, 09-26).

## 2026-10-04: checked against the whole repo — BOTH mechanisms are real

The 2026-10-01 `/pd` read (README, `EngineDisplay.cpp`, `EngineCamera.cpp`, `Host.cpp`) found no AMD code and
filed a correction, but said itself that `vendor/`, `tools/` and the history were not checked. They are now:

- `vendor/` holds three stand-ins, **built and installed**: `CMakeLists.txt` builds `atidxx32` (AMD quad-buffer
  proxy), `atiadlxy` (ADL proxy) and `d3d11_proxy` (adapter vendor-ID proxy), and `install.ps1` copies
  `d3d11.dll`, `atidxx32.dll` and `atiadlxy.dll` into the game `[reported 2026-10-04, GitHub API, main as of
  2026-09-26]`. `THIRD_PARTY_NOTICES.md` says these derive from effcol's wiz3D (LGPL 2.1).
- The `/pd` read is also right: the mod hooks the per-eye projection function (`0x204df0`) and sets the renderer's
  stereo and eye flags (`+0xc19`, `+0xc1a`) `[reported]`.

So the fake AMD driver is how the game is persuaded its HD3D path is available; the projection hook and the flags
are how the mod then drives the two eyes. This topic's title stands; the 2026-10-01 correction is withdrawn.

## Next step

Static, `[PD]`: in `TombRaider.exe`, find the call site that loads the AMD driver-extension DLL and
the quad-buffer stereo interface it asks for; that is the switch this mod flips. Compare with what the
game does when the vendor ID is NVIDIA (the `NvAPI_Stereo_IsEnabled` path) to decide which of the two
vendor paths is cheaper for us to wake.

## Credits

farmerarmor (TombRaiderVR, DeusExHRVR); effcol (wiz3D); the iZ3D project it is based on.
