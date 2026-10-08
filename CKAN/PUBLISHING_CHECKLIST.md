# GitHub -> CKAN workflow

Repository: https://github.com/SockedRooster/KSP-Inflatable-Fuel-Depots
Author: SockedRooster. MIT License identical to Quantum Relay.

1. **Do not publish the collision build as stable until the in-game collision test matrix passes.**
2. Upload the extracted project source files, GameData, LICENSE, README.md and documentation to main (not the whole ZIP as a single file).
3. Verify KSP version compatibility. The included NetKAN currently proposes KSP 1.12.5, which has not been independently tested.
4. After test results, tag a GitHub Release (e.g. v1.0.0) and attach the player-only `InflataDepot-v1.0.0.zip` containing `GameData/InflataDepot` and LICENSE. Do not rely on GitHub-generated source ZIP.
5. Ensure the release asset name matches the regular expression in CKAN/InflataDepot.netkan and does not include developer/source ZIP.
6. Submit `InflataDepot.netkan` to the KSP-CKAN/NetKAN repository following their mod-submission instructions. The file in this starter ZIP is for preparation; CKAN indexing is not automatic.
