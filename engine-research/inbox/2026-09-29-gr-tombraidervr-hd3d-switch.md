# /gr → modding: how TombRaiderVR switches on the shipped HD3D stereo path

From: `/gr` estate sweep, 2026-09-29. For the board's top `[PD]` row (what switches `StereoEnabled` /
the HD3D path on and how the second eye is drawn) and the "read farmerarmor's TombRaiderVR" row.

Full write-up: `external-research/topics/2026-09-29-tombraidervr-wakes-the-hd3d-path-with-a-fake-amd-driver.md`.

Short form, all `[reported]` from the mod's README and source comments (read on GitHub, nothing copied):

- The game's own stereo renderer does the second eye: top-and-bottom in one double-height target, same
  frame. The mod wakes it with stand-in AMD driver-extension (`atidxx32.dll`, quad-buffer stereo
  interface) and ADL DLLs, plus a `d3d11.dll` proxy that reports AMD's vendor ID on every adapter.
  Works on NVIDIA/Intel. The in-game Stereo 3D option must also be on.
- Pinned to Steam build 9573671; also resizes the game's render targets to the headset eye size.
- Hazards: a local `dxgi.dll` proxy never loads under Steam's overlay; EOS's overlay export-table hook
  can make a lazily-resolving `d3d11.dll` proxy recurse and drop the game to DX9.
- Suggested static start: the exe's call into the AMD driver-extension DLL (`AmdDxExtCreate11`) and the
  stereo interface it requests `[hypothesis]`.
- ⚠️ The repo was created 2026-09-19 `[measured 2026-09-29, GitHub API]`, so it is new, not years old.
