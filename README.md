# InflataDepot — Pancake-to-Cylinder Orbital Fuel Depots

**KSP1 | Version 0.9.1-collision-test | Experimental collision-testing build**

InflataDepot adds three deployable orbital propellant storage modules. Launch them as compact pancakes, attach via a single rigid bottom port, and inflate in space into large cylindrical fuel bladders.

## Parts

| VAB part | Docking compatibility | LF + Oxidizer storage | LF-only storage |
| --- | --- | --- | --- |
| ID-125 — 1.25 m | Clamp-O-Tron Jr. (size0) | 1,012.5 LF + 1,237.5 OX | 2,250 LF |
| ID-250 — 2.5 m | Clamp-O-Tron (size1) | 8,100 LF + 9,900 OX | 18,000 LF |
| ID-375 — 3.75 m | Clamp-O-Tron Sr. (size2) | 27,337.5 LF + 33,412.5 OX | 60,750 LF |

Each is **one VAB part**, with a B9 Part Switch **Fuel Configuration** selector for LF/OX or LF only. Both configurations initially contain zero fuel. Inflation takes approximately 20 seconds and is one-way.

## Dependencies — install separately

- B9 Part Switch (`B9PartSwitch` in CKAN)
- ModuleManager (`ModuleManager` in CKAN)

Do not install another copy of these dependencies from this archive; they are not bundled.

## Manual installation

1. Back up your existing saves and craft files.
2. Remove older `GameData/InflataDepot` folders, **especially from early beta releases**; do not merge versions.
3. Copy this release's `GameData/InflataDepot` folder into the game's `GameData` folder.
4. Install B9 Part Switch and ModuleManager separately.
5. In the VAB, find the three ID-series fuel tanks, select **Fuel Configuration** in the part menu, and build your station.
6. Launch with an empty tank, select **Inflate Fuel Depot** in flight, attach/dock via the **only bottom docking port**, and transfer fuel from tankers.

## Known limitations

- Inflation is **visual only**: the tank holds its full resource capacity even when stowed; the game does not enforce orbit-only use or empty launch. Players can fill tanks in the editor/flight before deploying if they choose.
- **Experimental:** The inflatable membrane now includes a convex collision hull that scales with deployment. This has not been validated in KSP yet. Deploy only in open space until tested; collisions during expansion may push or damage other spacecraft.
- The docking interface is occupied when connected to another stack part; undock/decouple before using it as a free docking interface.
- This is a release candidate, not a final 1.0. Docking and animation have been successfully tested by the creator in their modded KSP1 installation, but broad compatibility, career balance and Kerbalism-specific behavior have not been verified.
- Older pre-switch beta craft using separate `_LF` part identifiers may not migrate automatically. Preserve backups.

## Community and license

**Author:** SockedRooster. **License:** MIT (Copyright © 2026 SockedRooster). **Repository:** https://github.com/SockedRooster/KSP-Inflatable-Fuel-Depots. Source and mod assets are distributed under the repository LICENSE. The experimental collision update requires in-game verification before submission to CKAN.

## Source

The code used to generate the .mu models, textures and configs is included separately in the source-and-CKAN kit. This candidate modifies the three .mu model files to add collision geometry. The base configuration, docking and B9 options are retained.
