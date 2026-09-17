# Tomb Raider (2013) had a real, official 3D Vision mode, and geo-11 users report re-enabling it

**From:** `/sr` sweep, home PC, 2026-09-17.
**Answers:** dossier §"`StereoOffset` already exists in the shaders … whether anything still fills it
is unchecked, and the first thing to check" `[hypothesis]`.

## What is public

- **The game shipped official NVIDIA 3D Vision support**, widely described as exemplary at the time
  `[reported 2026-09-17]`. That is the likely writer of the `StereoOffset` term this project found in
  the `SceneBuffer` cbuffer.
- **A 2026-era how-to exists: "[geo-11] [HowTo] Tomb Raider 2013 - enable 3D with latest game
  version"** on the MTBS3D forum: <https://www.mtbs3d.com/forum/viewtopic.php?t=160557>.
  ⚠️ **It returned HTTP 403 to automated fetch.** That is not a negative result; open it in a
  browser. The title alone says the in-game stereo path can be brought back on the current build.
- **A Steam discussion reports an older route:** downgrade the game to build **743**, then change a
  `0` to `1` in **`3DVision_Config.xml`** to enable stereo `[reported 2026-09-17, search snippet
  only, thread not read]`: <https://steamcommunity.com/app/203160/discussions/0/1733210552682791600>.
- **geo-11's announcement lists Tomb Raider among games that work with it, "but will need a special
  texture map"** `[reported 2026-09-17]`:
  <https://helixmod.blogspot.com/2022/06/announcing-new-geo-11-3d-driver.html>.

## Why it matters here

1. **`3DVision_Config.xml` is a named, plain-text switch.** Check whether the Steam build's data or
   save folder carries it before any hooking. It may flip the engine's own stereo path, the one that
   fills `StereoOffset`.
2. **geo-11 is a D3D11 driver that talks to games' own 3D Vision paths**, so a working geo-11 setup
   is a live oracle: run it once, and whatever the game writes to `StereoOffset` per eye can be read
   back. Our own renderer then does not have to guess the sign or units.
3. The dossier's caution stands: 3D Vision stereo gives binocular depth, not head-tracked eye poses.
   See the library's "Dormant native stereo paths" cautions:
   <https://github.com/TefMeister/flat-to-vr-cross-engine-research/blob/main/docs/techniques/README.md#dormant-native-stereo-paths>

Nothing here was run or verified by us. Read the MTBS3D thread in a browser first.
