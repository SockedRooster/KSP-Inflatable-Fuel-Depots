# Changelog

## 1.0.5 - Remove staging options (2026-10-14)

- Disable docking-port staging and its editor/flight toggle on all three sizes.
- Restore previously saved staging-enabled ports to disabled through the stock API.
- Retain manual docking controls, always-on crossfeed, VAB deflation and colour variants.
- Plugin compilation and offline checks passed; v1.0.5 subsequently tested in-game by the maintainer.

## 1.0.4 - Always-on crossfeed (2026-10-14)

- Keep docking crossfeed enabled in the editor and flight, including older saved OFF states.
- Hide docking crossfeed menu events and Enable/Disable/Toggle action-group controls.
- Preserve deployment storage locks, VAB deflation and colour variants.
- Rebuilt against local KSP assemblies; offline checks passed, runtime verification pending.

## 1.0.3 - VAB deflate control (2026-10-14)

- Use the stock reversible Inflate/Deflate animation button in the VAB and SPH.
- Keep custom guarded deployment controls exclusive to flight.
- Refresh editor empty-tank state using Unity Update instead of the flight callback.
- Preserve Station Grey and Original finishes on all three sizes.
- Rebuilt plugin and passed offline checks; in-game verification pending.

## 1.0.2 - Station Grey (2026-10-13)

- Add Original and Station Grey stock colour variants to all three depot sizes.
- Match the station modules' blue-grey steel palette using a fabric material tint.
- Preserve fabric weave, branding, gold bands, fuel selection and VAB inflation.
- Keep Original as the default; no added dependencies or changes to capacity/mass.
- Static validation passed; in-game colour/variant checks remain pending.

## 1.0.1 - Editor inflation (2026-10-13)

- Add guarded Inflate and Deflate controls in the VAB and SPH for all three sizes.
- Allow repeated deployment/retraction and show the correct editor storage status.
- Keep editor tanks empty and preserve flight fuel-lock/empty-only deflation checks.
- Update the asset generator to retain repeatable animation controls.
- Rebuild against local KSP assemblies; in-game verification remains pending.

## 1.0.0 — Initial stable release (2026-10-08)

- First public release package based on the creator-tested v0.10.0 gameplay assets.
- Three pancake-to-cylinder inflatable propellant depots (1.25 m / 2.5 m / 3.75 m).
- Single bottom Clamp-O-Tron-compatible docking connection for each size.
- B9 Part Switch options for LF/Oxidizer and LF-only storage on the same VAB parts.
- Plugin-enforced zero capacity until fully deployed; deployed empty tanks accept transferred fuel.
- Deflation guard blocks the command while Liquid Fuel or Oxidizer is present.
- Collision hull on the deployed cylinder; persistent docking-base collision.
- RoosterWorks textures and branding, sealed end caps, stock FuelTank category,
  VAB Organizer Rocket Fuel subcategory, Advanced Fuel Systems career unlock.
- Includes tested compiled `InflataDepotPlugin.dll`, model assets and full mod source.

No gameplay asset/binary changes were made between the creator-tested 0.10.0 package
and the 1.0.0 release ZIP; this update adds public release documentation and metadata.
