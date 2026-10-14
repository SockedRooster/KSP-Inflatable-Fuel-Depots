# CKAN Submission — RoosterWorks InflataDepot

This folder contains CKAN submission metadata and preparation notes. Merely storing a NetKAN file in this repository does not register the mod in CKAN.

## Current release

- Latest source/documentation version: **v1.0.5**, tested in KSP by the maintainer.
- GitHub releases: https://github.com/SockedRooster/KSP-Inflatable-Fuel-Depots/releases
- Attach the player installation archive named **`InflataDepot-v1.0.5.zip`** to a regular (non-prerelease) GitHub release tagged **`v1.0.5`**.
- Use [RELEASE_NOTES_v1.0.5.md](../RELEASE_NOTES_v1.0.5.md) for the release description.
- Do not use GitHub's automatic "Source code" archives as installation assets.

## CKAN submission

The [InflataDepot.netkan](InflataDepot.netkan) file targets GitHub release assets matching `InflataDepot-v<version>.zip`, installs the `InflataDepot` folder into `GameData`, and declares required `B9PartSwitch` and `ModuleManager` dependencies plus optional `VABOrganizer`.

After publishing the release, confirm that the downloadable asset matches the filename pattern and contains `GameData/InflataDepot` with the plugin, models, and part configs. Submit the metadata to https://github.com/KSP-CKAN/NetKAN following their contribution instructions. CKAN indexing depends on maintainer review and validation; it is not automatic merely because the file is committed here.

KSP compatibility is currently declared as **1.12.5**. Broader compatibility should not be claimed without testing.
