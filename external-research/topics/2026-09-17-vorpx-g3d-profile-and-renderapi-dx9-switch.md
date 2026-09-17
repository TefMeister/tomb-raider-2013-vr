# vorpX has a Geometry-3D profile, which needs the game switched to DX9 with the `RenderAPI` registry value

**Status:** 🆕 new · **Priority:** medium. Complements `/sr`'s 2026-09-17 drop about the game's
official 3D Vision mode and geo-11 (in `engine-research/inbox/`), which is not repeated here.

## What is public

- vorpX ships a factory **Geometry 3D (G3D)** profile for Tomb Raider 2013, which **requires the DX9
  renderer**: set `HKEY_CURRENT_USER\Software\Crystal Dynamics\Tomb Raider\Graphics` →
  **`RenderAPI` = 9** `[reported]`.
- A Steam thread (koallalays, 2022-05-29) reports full VR with vorpX working, but aiming being hard, and
  prefers cinema mode `[reported]`.

## Why it matters here

1. **The renderer is a registry value.** The dossier's `SceneBuffer` and `StereoOffset` findings are
   from the D3D11 shaders; a DX9 run is a different path, and every test should record which API was
   active `[hypothesis]`.
2. It also means the windowed-mode and renderer options for the board's `[FLAT]` launch row likely live
   in the same registry key.

## Next step

Before the first launch, read the `Graphics` registry key and record `RenderAPI` and the window settings.

## Sources

- vorpX forum, "Can anyone confirm G3d for Tomb Raider 2013?" — <https://www.vorpx.com/forums/topic/can-anyone-confirm-g3d-for-tomb-raider-2013/>
- Steam discussion, "Tomb Raider 2013 with VR/3D - solved" — <https://steamcommunity.com/app/203160/discussions/0/3382778848135176500/>
