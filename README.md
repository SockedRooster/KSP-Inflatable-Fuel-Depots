# RoosterWorks InflataDepot

**Version 1.0.0 — Kerbal Space Program 1**  
**Author:** SockedRooster  
**License:** MIT © 2026 SockedRooster

InflataDepot adds three inflatable orbital propellant depot parts. Each launches as a compact, empty disc (“pancake”) and expands into a cylindrical tank for use with refueling stations and spacecraft. A single bottom connection functions as a stock-compatible docking port.

## Parts and capacities

| VAB part | Launch diameter | Docking compatibility | LF + Oxidizer (units) | LF only (units) |
|---|---:|---|---|---:|
| RoosterWorks ID-125 Inflatable Depot | 1.25 m | Clamp-O-Tron Jr. (size0) | 1,012.5 LF + 1,237.5 OX | 2,250 LF |
| RoosterWorks ID-250 Inflatable Depot | 2.5 m | Clamp-O-Tron (size1) | 8,100 LF + 9,900 OX | 18,000 LF |
| RoosterWorks ID-375 Inflatable Depot | 3.75 m | Clamp-O-Tron Sr. (size2) | 27,337.5 LF + 33,412.5 OX | 60,750 LF |

Each size is **one VAB part** with a **Fuel Configuration** selector (B9 Part Switch): **LF + Oxidizer** or **Liquid Fuel Only**.

## Gameplay features

- Folds compactly for launch and inflates into a cylinder in flight (approximately 20 seconds).
- Launches empty: **cannot hold or receive fuel while folded or inflating**; full empty storage capacity becomes available only when fully deployed.
- **Deflation is disabled while either Liquid Fuel or Oxidizer remains aboard.** Drain the tank completely before retracting it.
- Solid cylinder collision when deployed, with a separate permanent docking-base collider. Avoid inflating through an existing structure.
- High-resolution RoosterWorks fabric and nameplate textures; sealed end caps.
- All parts appear under **Fuel Tanks** in the stock VAB. With **VAB Organizer**, they appear in **Fuel Tanks → Rocket Fuel**.
- In Career mode, unlocked by **Advanced Fuel Systems** (`advFuelSystems`, 160-science tier).

## Dependencies

Required (install separately; CKAN installs these automatically):
- **B9 Part Switch** (`B9PartSwitch`)
- **ModuleManager** (`ModuleManager`)

Optional:
- **VAB Organizer** (`VABOrganizer`) for the Rocket Fuel subcategory.

## Manual installation

1. Quit KSP and back up saves and craft using older beta versions.
2. Remove the **old** `GameData/InflataDepot` folder. Do not merge test builds.
3. Extract **`InflataDepot-v1.0.0.zip`** into the **Kerbal Space Program installation directory**. The correct result is `GameData/InflataDepot/Plugins/InflataDepotPlugin.dll`.
4. Install the required dependencies if not already installed.
5. In the VAB, select a depot under Fuel Tanks and choose the desired B9 fuel configuration. Launch it empty; inflate it in flight; transfer fuel once fully deployed.

**Note:** People installing from CKAN need only select this mod; CKAN will manage the listed dependencies and files.

## Compatibility and cautions

- Intended for **KSP 1.12.5**. Other KSP or mod combinations, including Kerbalism, have not been independently certified.
- The creator confirmed the v0.10.0 baseline in-game: fuel locking, empty-only deflation, animation, docking, and deployed-cylinder collision. **v1.0.0 uses the same gameplay assets and binary as that tested baseline.**
- Deploy in clear space: activating the deployed collider against an overlapping spacecraft can cause physics forces.
- Save files or craft containing older beta part identifiers (including separate `_LF` variants) may need manual migration; keep backups.
- Actions assigned to the older stock animation Toggle may need reassignment to **Inflate Fuel Depot** / **Deflate Empty Fuel Depot**.
- A bottom docking interface already attached to a stack part is not simultaneously available as a free docking interface.

## Support, licensing and source

- Repository: https://github.com/SockedRooster/KSP-Inflatable-Fuel-Depots
- Issues: https://github.com/SockedRooster/KSP-Inflatable-Fuel-Depots/issues
- License: [MIT](LICENSE), copyright © 2026 SockedRooster
- Mod source: `Source/InflataDepotPlugin/` (C#), `Source/build.py` (asset generator), and `Source/test_assets.py`.

This package does not bundle third-party dependency binaries or KSP/Unity game libraries.
