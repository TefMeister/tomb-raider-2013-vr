Supersedes: external-research/topics/2026-09-29-tombraidervr-wakes-the-hd3d-path-with-a-fake-amd-driver.md (the "fake AMD driver" mechanism claim only)

# TombRaiderVR's source drives stereo by hooking the projection function, not (visibly) by a fake AMD driver

From: `/pd`, 2026-10-01, reading `farmerarmor/TombRaiderVR` (README, `src/EngineDisplay.cpp`, `src/EngineCamera.cpp`,
`src/Host.cpp`) for the modding board. Detail: `tomb-raider-2013-vr/modding-notes/2026-10-01-pd-farmerarmors-tombraidervr-read.md`.

- The README and those three files do not mention AMD, HD3D, `atidxx32`, ADL or a vendor ID `[reported]`.
- Stereo is driven by hooking the game's per-eye projection function (offset `0x204df0`) and setting the native stereo
  flag and eye flag on the renderer (`+0xc19`, `+0xc1a`) directly; both eyes in one frame; a separate host process
  submits a shared D3D11 texture to the headset; rotation-only tracking `[reported]`.
- NOT checked: the rest of the repo (`vendor/`, `tools/`, history) for an AMD stand-in. The topic's mechanism
  sentence should be marked uncertain until someone checks.
