Supersedes: engine-research/ENGINE-DOSSIER.md, the paragraph "How TombRaiderVR switches on the shipped HD3D stereo path (`/gr` 2026-09-29)" (the stand-in AMD driver mechanism only)

# The dossier still states the "fake AMD driver" mechanism the 2026-10-01 `/pd` read could not find

From: `/gs`, 2026-10-04. Read-only finding; nothing was edited.

- The 2026-10-01 `/pd` read of farmerarmor's TombRaiderVR source found stereo driven by hooking the per-eye
  projection function (`0x204df0`) and setting the renderer's stereo and eye flags (`+0xc19`, `+0xc1a`); no AMD,
  HD3D, `atidxx32`, ADL or vendor-ID code in the README or the three source files read `[reported]`. Its correction
  went to `external-research/inbox/` (`2026-10-01-pd-tombraidervr-source-shows-direct-projection-hook.md`), which
  `/gr` owns.
- The modding-owned dossier paragraph near line 144 still says the mod "wakes it with stand-in AMD driver-extension
  (`atidxx32.dll`) and ADL DLLs plus a `d3d11.dll` proxy that reports AMD's vendor ID" as the mechanism, tagged
  `[reported]`. The status board's 2026-10-01 entry already says "no fake AMD driver visible", so the two disagree.
- Suggested fix: mark that mechanism sentence uncertain and point at the 2026-10-01 note, until someone checks the
  rest of the repo (`vendor/`, `tools/`, history) for an AMD stand-in. The Steam/EOS overlay hazards in the same
  paragraph are separate claims and are not affected.
