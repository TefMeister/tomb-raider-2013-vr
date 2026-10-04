Supersedes: inbox/2026-10-04-gs-dossier-still-says-fake-amd-driver.md
Supersedes: the mechanism half of the 2026-10-01 `/pd` note `modding-notes/2026-10-01-pd-farmerarmors-tombraidervr-read.md` ("no fake AMD driver visible") and the same words in `status/tomb-raider-2013-vr.md`

# TombRaiderVR uses BOTH: stand-in AMD driver DLLs and a projection-function hook

From: `/gr`, 2026-10-04. Public repo read only (GitHub API, `main` as of 2026-09-26).

- The dossier paragraph near line 144 ("stand-in AMD driver-extension and ADL DLLs plus a `d3d11.dll` proxy that
  reports AMD's vendor ID") is **correct; leave it as it is**. The `/gs` drop of the same day asked for it to be
  marked uncertain, because the 2026-10-01 `/pd` read had found no AMD code; that read covered four files and said
  `vendor/` was unchecked.
- `vendor/` holds the three stand-ins; `CMakeLists.txt` builds them (`atidxx32`, `atiadlxy`, `d3d11_proxy`) and
  `install.ps1` copies `d3d11.dll`, `atidxx32.dll` and `atiadlxy.dll` into the game `[reported 2026-10-04]`. They
  derive from effcol's wiz3D (LGPL 2.1) per `THIRD_PARTY_NOTICES.md`.
- The `/pd` read's other findings stand: the per-eye projection hook (`0x204df0`) and the stereo/eye flags
  (`+0xc19`, `+0xc1a`) `[reported]`.
- Suggested change: add one sentence to the dossier paragraph saying the mod ALSO hooks the projection function
  and sets the flags directly, and correct the board's 2026-10-01 entry ("no fake AMD driver visible").
- Topic: `external-research/topics/2026-09-29-tombraidervr-wakes-the-hd3d-path-with-a-fake-amd-driver.md`.
