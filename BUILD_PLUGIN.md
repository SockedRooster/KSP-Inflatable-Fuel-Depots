# Building the plugin (developer workflow)

For players: **do not build anything**. The release ZIP already includes a compiled plugin DLL.

Developers on Windows may rebuild the DLL with `Build-Plugin.cmd` (or `Build-Plugin.ps1`)
from this repository root. You need a local KSP 1 installation because the script references
KSP's `Assembly-CSharp.dll` and Unity managed DLLs, including `UnityEngine.UI.dll`.
Those game assemblies are **not** distributed with this repository.

`Source/InflataDepotPlugin/ModuleInflataFuelLock.cs` implements the storage lock
and guarded inflate/deflate actions. The public release DLL was supplied and
in-game tested by the author; recompiling the source is optional for development.

`Source/build.py` generates models/assets. **Do not regenerate the released `.mu` files
for a tagged release**, as that would replace the in-game-tested binaries. Make model
changes in a new development version, then test that version in KSP before releasing.

To rebuild models and configurations, install Python, NumPy and Pillow, then run
`python Source/build.py` from the repository root. This **overwrites** the local
`GameData/InflataDepot` assets and creates `dist/InflataDepot-rebuilt.zip`.
The `dist/` archive is a developer artifact, **not** an official release.

`python Source/test_assets.py` performs static checks, not an in-game test.
Before publishing a player ZIP, run
`python CKAN/verify_release.py path/to/InflataDepot-v1.0.0.zip`
(or supply the appropriate release archive path). Keep the shipped plugin DLL,
but do not redistribute KSP or Unity game assemblies.
