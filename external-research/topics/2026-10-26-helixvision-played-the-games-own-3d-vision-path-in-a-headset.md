# HelixVision played the game's own 3D Vision path in a headset, with no shader fix

*For the `[FLAT]` ⭐⭐⭐ row "does the stand-in wake the two-eye loop?" (our `nvapi.dll` answers the game's NVIDIA 3D
calls, the Hard Reset pattern; dossier, "Chosen").*

## What was found

A 2020 Steam discussion on **HelixVision** (bo3b's player that shows 3D Vision games in a VR headset, built on the
real NVIDIA 3D Vision driver) covers Tomb Raider 2013 `[reported]`:

- bo3b (21 Feb 2020): the 2013 game "should be working fine", but it uses "a special launch technique because it's
  a native 3D game"; the launch goes through the game's own pop-up launcher, where you press Play to continue.
- bo3b (22 Feb 2020): it "doesn't need a fix, or any other tool outside of the 3D Vision Driver".
- FastLawyer (21 Feb 2020): played it the same way, no 3D fix or wrapper installed.
- A third user (DAN-di-WARhol) got a white picture in the headset while the monitor showed the game; bo3b's advice
  was to check the game in 3D on its own first, without SteamVR, and to run the driver's stereo test.

## Why it matters here

- It is outside evidence that the game's **own** NVIDIA two-eye path draws a correct stereo pair once the driver
  says stereo is on: players saw it in a headset with no shader edits. That fits our static finding that none of the
  25,047 archive shaders reads `StereoOffset` and the per-eye shift is done on the CPU (dossier, 2026-10-01).
- So if the stand-in wakes the loop, the two pictures it produces should already be usable, and a wrong picture would
  more likely point at the stand-in's answers than at the game.
- The launcher detail is a reminder for the first `[FLAT]` run: the stereo choice and Play may sit in the game's
  pop-up launcher, not only in the in-game options. The board row already says to turn "Stereo 3D" on in the options.
- Caveat: this is the real driver on 2020-era drivers (3D Vision was dropped after driver 425.31), five-plus years
  old, and from forum posts, not a measurement.

## Sources

- Steam Community, HelixVision discussion "Tomb Raider" (posts by bo3b, FastLawyer, DAN-di-WARhol, February 2020) —
  https://steamcommunity.com/app/1127310/discussions/0/1746771454434847186
