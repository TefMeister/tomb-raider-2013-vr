# Research index

**Last `/gr` pass: 2026-10-26 — CHECK-IN.** Inbox empty; board unchanged since 10-08. farmerarmor's TombRaiderVR unchanged since v0.1.1 (2026-09-26). One search for the stand-in row: HelixVision users played the game's own 3D Vision path in a headset in 2020 with no shader fix, launched through the game's pop-up launcher; one topic.

_Previous: **Last `/gr` pass: 2026-10-11 (estate sweep) — CHECK-IN.** Inbox empty. The Epic sign-in prompt the first [FLAT] row watches for is a public 2021 change with two documented ways round it (unlink the accounts; pre-EOS beta branch); pointer dropped to engine-research/inbox._

_Previous: **Last `/gr` pass: 2026-10-04 (estate sweep) — CHECK-IN.** Inbox drained: the `/pd` correction ("no fake AMD driver") was checked against the whole TombRaiderVR repo and is withdrawn; the AMD stand-ins are built and installed, and the projection hook is real too. Both are now in the topic._

_Previous: **Last `/gr` pass: 2026-09-29 (estate sweep) — CHECK-IN.** Read farmerarmor's TombRaiderVR on GitHub: it wakes the game's own AMD HD3D stereo path with stand-in AMD driver DLLs on any GPU, which answers how the second eye is drawn for the top board row; pointer sent to `engine-research/inbox/`._

_Previous: **Last `/gr` pass: 2026-09-23 (estate sweep) — FULL.** Checked against phunkaeg's *VR Modding Playbook*: DeusExHRVR drives a sibling Crystal-engine game's own stereo renderer; pointer dropped in `engine-research/inbox/` against the StereoOffset row._

_Previous: **Last `/gr` pass: 2026-09-17 (estate sweep) — CHECK-IN.** First pass: folder bootstrapped; one topic on the vorpX route (DX9 via the `RenderAPI` registry value) as a complement to `/sr`'s 3D Vision drop already in `engine-research/inbox/`._

Every research topic gathered for this project, newest first. Each row links to a self-contained
write-up in `topics/`. Status tags:

- 🆕 **new** — found, not yet acted on by the modding side.
- 👀 **looked at** — the modding side has read it; no verdict yet.
- ✅ **used / confirmed** — acted on, and it held.
- ❌ **dead end** — tried, and it did not work (kept so it is not re-proposed).

| Date | Topic | Status | Why it matters |
| --- | --- | --- | --- |
| 2026-10-26 | [HelixVision played the game's own 3D Vision path in a headset, with no shader fix](topics/2026-10-26-helixvision-played-the-games-own-3d-vision-path-in-a-headset.md) | 🆕 | For the stand-in `nvapi.dll` row: once the driver says stereo is on, the game's own two-eye pictures were usable in a headset (2020, real driver); stereo is chosen through the game's pop-up launcher. |
| 2026-10-11 | [The Epic sign-in prompt is public, and has two ways round it](topics/2026-10-11-the-epic-sign-in-prompt-is-public-and-has-two-ways-round.md) | 🆕 | For the first live launch: unlink Steam/Epic, do not cancel the pop-up blind; beta branch as fallback |
| 2026-09-29 | [TombRaiderVR wakes the game's own HD3D stereo path with a fake AMD driver, on any GPU](topics/2026-09-29-tombraidervr-wakes-the-hd3d-path-with-a-fake-amd-driver.md) | 🆕 | Answers how the second eye is drawn (top `[PD]` row) and lists where the mod falls short (third `[PD]` row); two proxy hazards (Steam overlay, EOS); checked 2026-10-04: both the AMD stand-ins and a projection-function hook are used |
| 2026-09-23 | [DeusExHRVR drives a sibling game's own built-in stereo renderer, and gets both eyes in one frame](topics/2026-09-23-deusexhrvr-drives-a-sibling-games-own-stereo-renderer.md) | 🆕 | Strongest evidence yet that the shipped stereo path is a route, not just an oracle. |
| 2026-09-17 | [vorpX has a Geometry-3D profile, which needs the game switched to DX9 with the `RenderAPI` registry value](topics/2026-09-17-vorpx-g3d-profile-and-renderapi-dx9-switch.md) | 🆕 | A plain registry switch selects the renderer, which matters for every stereo experiment |
