# DeusExHRVR drives a sibling game's own built-in stereo renderer, and gets both eyes in one frame

**Found:** 2026-09-23, `/gr` estate sweep, through phunkaeg's *VR Modding Playbook* (`sources.yml` →
`DeusExHRVR`, code read by the playbook author on 2026-09-17).
**Source:** farmerarmor, *DeusExHRVR* — <https://github.com/farmerarmor/DeusExHRVR> (LGPL-2.1, v0.3.0).
Read on GitHub only; nothing copied.

## What it is

A VR mod for **Deus Ex: Human Revolution Director's Cut** (Steam 2.0.66.0, one pinned executable
hash). Instead of drawing the world twice itself, it **switches on the game's own AMD HD3D stereo
renderer**, which renders a double-height picture holding two complete headset-sized eyes, one above
the other. A 64-bit companion program hands that pair to OpenXR `[reported]`. The playbook's own code
read confirms the mod calls the game's native stereo entry point directly `[reported]`.

It still needed four per-eye fixes behind toggles: per-eye light/shadow transforms, per-eye shader
camera inputs, a shared lighting-depth correction (the second needs the third), and a HUD projected
through the recorded eye poses `[reported]`.

## Why it matters here

**Human Revolution runs on a modified Crystal Dynamics engine, the family Tomb Raider (2013) comes
from** `[reported]` (ModDB's Crystal Dynamics engine page and several graphics write-ups say DXHR used
it; that Tomb Raider 2013's "Foundation" is the same lineage is `[reported]`, not checked by us).

That makes it the closest evidence yet on our top `[PD]` row, *"is `SceneBuffer.StereoOffset` live or
vestigial?"*:

- Our dossier found a named `StereoOffset` term in the shipped shaders `[inferred-static 2026-09-14]`.
- The `/sr` drop of 2026-09-17 says the game shipped official 3D Vision support and that users
  re-enable it `[reported]`.
- DeusExHRVR now shows that **on a sibling engine, a shipped vendor stereo path could be driven from a
  mod to produce a real per-eye pair in one frame**, headset-usable, with a short, named list of what
  was still wrong afterwards.

So the shipped stereo path is worth treating as a **route**, not just an oracle `[hypothesis]`: if
Tomb Raider's 3D Vision or HD3D path can be woken, much of the "render twice" problem may already be
solved inside the game, and DeusExHRVR's four fixes are a checklist of what to expect next.

⚠️ **Deus Ex: Mankind Divided is not covered by this.** It runs on Eidos-Montréal's Dawn engine,
reported as derived from Glacier 2, not from the Crystal engine. Whether it kept a stereo path is
unknown.

## Next step

When the shader disassembly row is worked, look specifically for how `StereoOffset` is combined with
the view, and whether an HD3D or 3D Vision stereo entry point sits in the executable's imports or
strings (DeusExHRVR's route depended on one). Both are static checks.

## Credits

farmerarmor (DeusExHRVR); phunkaeg (*VR Modding Playbook*); ModDB's Crystal Dynamics engine page
<https://www.moddb.com/engines/crystal-dynamics-engine>.
