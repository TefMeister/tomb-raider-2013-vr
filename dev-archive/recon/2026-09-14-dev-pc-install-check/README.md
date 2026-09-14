# 2026-09-14 — Tomb Raider (2013) is NOT usable on the dev PC yet

**Machine:** dev PC `DESKTOP-V8GTSIR`. **No launch, no analysis** — this is an install check, and it
came back negative.

## What was found

There is **no `Tomb Raider` folder at all** under
`D:\Program Files (x86)\Steam\steamapps\common\` `[inferred-static 2026-09-14]`.

Steam has a manifest for the app (`appmanifest_203160.acf`) but it reads `StateFlags=18` with no
recorded download progress — the app is known to this library and the files are not there.

## What that means for this project

The 2026-09-13 `[PD]` row — *"finish the first static look: imports, what the `.shad` section holds,
which renderer is the default and how to pick one"* — **cannot run on this machine.** There is no
binary to read.

Of the six games the user asked about on 2026-09-14, this is the only one with **nothing on disk at
all**; The Witcher 2 at least has an empty folder and a queued download.

## What would change it

The user installs app 203160 on this PC (about 15 GB). Nothing else is blocked in the meantime — the
home PC has the game fully installed and can run that `[PD]` row today.
