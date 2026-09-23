# A sibling Crystal-engine game was made VR through its OWN stereo path

**From:** `/gr` estate sweep, home PC, 2026-09-23.
**Answers:** board `[PD]` ⭐ "disassemble the shaders that read `SceneBuffer.StereoOffset` (+1344) …
that decides whether the shipped stereo term is live or vestigial".
**Topic:** `external-research/topics/2026-09-23-deusexhrvr-drives-a-sibling-games-own-stereo-renderer.md`

farmerarmor's **DeusExHRVR** (<https://github.com/farmerarmor/DeusExHRVR>, LGPL-2.1) makes Deus Ex:
Human Revolution DC playable in VR by **calling the game's own AMD HD3D stereo entry point**, which
renders both eyes in one frame as a stacked pair `[reported]`. Human Revolution used a modified
Crystal Dynamics engine, the lineage Tomb Raider 2013 comes from `[reported]`. Four per-eye fixes were
still needed afterwards: light/shadow transforms, shader camera inputs, lighting depth, HUD
`[reported]`.

**Suggested dossier change:** add under the `StereoOffset` finding that a shipped vendor stereo path
on a sibling engine has been driven successfully from a mod, so the static check should also look
for an HD3D or 3D Vision entry point in this executable's imports and strings. Keep it `[reported]`
until something of ours runs.
