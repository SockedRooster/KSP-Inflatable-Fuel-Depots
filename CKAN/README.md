# CKAN integration — InflataDepot

**Status:** GitHub v1.0.0 is already published. This repository contains proposed
NetKAN metadata; the files here do not automatically list the mod in CKAN.

## Files

- `InflataDepot.netkan` — proposed CKAN metadata.
- `verify_release.py` — structural checks for a player release ZIP.

## CKAN submission

1. Verify the release has a player archive named `InflataDepot-v<version>.zip`,
   containing `GameData/InflataDepot` (not a developer/source ZIP).
2. Run `python CKAN/verify_release.py path/to/InflataDepot-v1.0.0.zip`,
   substituting the applicable release filename.
3. Review `InflataDepot.netkan` for the tested KSP version, GitHub asset pattern,
   dependencies and installation path.
4. Follow the [CKAN guide](https://github.com/KSP-CKAN/CKAN/wiki/Adding-a-mod-to-the-CKAN)
   to submit metadata to [KSP-CKAN/NetKAN](https://github.com/KSP-CKAN/NetKAN),
   typically with a pull request adding the file under their `NetKAN/` directory.
   CKAN maintainers validate and review submissions; indexing is not automatic.

## Player packaging

- Only `GameData/InflataDepot` installs into the game's `GameData` directory.
- B9 Part Switch and ModuleManager are required; VAB Organizer is optional.
- Never bundle third-party mod dependencies or KSP game DLLs.
- Do not include this `CKAN/` directory, source/build scripts, or development
  archives in the player installer.
- For future versions, attach a correctly named release ZIP and update metadata
  when compatibility or dependencies change.

NetKAN contributions follow that project's contribution requirements separately
from the mod's MIT code license.
