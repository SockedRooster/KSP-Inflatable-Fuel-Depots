# CKAN Submission — InflataDepot

Files here are **submission preparation materials**, not a standalone CKAN registration.
The index does not accept a local directory uploaded to GitHub as an automatic listing.

1. Make sure the code and LICENSE are committed in the public project repository.
2. At https://github.com/SockedRooster/KSP-Inflatable-Fuel-Depots/releases/new create a
   **regular release** using tag **`v1.0.0`**, titled **RoosterWorks InflataDepot v1.0.0**.
3. Attach the **player asset `InflataDepot-v1.0.0.zip`** (NOT the developer/source ZIP)
   and paste the `RELEASE_DESCRIPTION.md` into the release notes.
4. Check that the publicly reachable GitHub asset filename matches the `$kref`
   asset_match pattern in `InflataDepot.netkan`.
5. Verify `ksp_version: 1.12.5` matches your KSP test installation. If not,
   update metadata to the tested version *before* submitting.
6. Submit **`InflataDepot.netkan`** to the public CKAN metadata index:
   https://github.com/KSP-CKAN/NetKAN (usually as a pull request; follow its CONTRIBUTING instructions).
7. Let CKAN maintainers' bot/CI generate and validate the versioned `.ckan` and
   review the installation. CKAN appearance is **not instantaneous or guaranteed**.

Dependencies are `B9PartSwitch` and `ModuleManager`; optional `VABOrganizer` provides
Fuel Tanks → Rocket Fuel categorization. This metadata installs the `InflataDepot`
folder into `GameData` and does not bundle third-party dependency files.
