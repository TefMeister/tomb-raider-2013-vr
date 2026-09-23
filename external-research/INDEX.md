# Research index

**Last `/gr` pass: 2026-09-23 (estate sweep) — FULL.** Checked against phunkaeg's *VR Modding Playbook*: DeusExHRVR drives a sibling Crystal-engine game's own stereo renderer; pointer dropped in `engine-research/inbox/` against the StereoOffset row.

_Previous: **Last `/gr` pass: 2026-09-17 (estate sweep) — CHECK-IN.** First pass: folder bootstrapped; one topic on the vorpX route (DX9 via the `RenderAPI` registry value) as a complement to `/sr`'s 3D Vision drop already in `engine-research/inbox/`._

Every research topic gathered for this project, newest first. Each row links to a self-contained
write-up in `topics/`. Status tags:

- 🆕 **new** — found, not yet acted on by the modding side.
- 👀 **looked at** — the modding side has read it; no verdict yet.
- ✅ **used / confirmed** — acted on, and it held.
- ❌ **dead end** — tried, and it did not work (kept so it is not re-proposed).

| Date | Topic | Status | Why it matters |
| --- | --- | --- | --- |
| 2026-09-23 | [DeusExHRVR drives a sibling game's own built-in stereo renderer, and gets both eyes in one frame](topics/2026-09-23-deusexhrvr-drives-a-sibling-games-own-stereo-renderer.md) | 🆕 | Strongest evidence yet that the shipped stereo path is a route, not just an oracle. |
| 2026-09-17 | [vorpX has a Geometry-3D profile, which needs the game switched to DX9 with the `RenderAPI` registry value](topics/2026-09-17-vorpx-g3d-profile-and-renderapi-dx9-switch.md) | 🆕 | A plain registry switch selects the renderer, which matters for every stereo experiment |
