# InflataDepot 1.0.1 - VAB inflation

Install: close KSP and replace GameData/InflataDepot with the folder from
InflataDepot-v1.0.1.zip. Keep ModuleManager and B9 Part Switch installed.

Right-click any of the three depots in the VAB or SPH, then select Inflate Fuel
Depot. Select Deflate Fuel Depot (Empty Only) to fold it again. Tanks remain
empty in the editor and at launch. Flight refueling and empty-only deflation
protections remain enabled.

Validation: compiled successfully against the installed KSP/Unity assemblies;
existing Source/test_assets.py checks pass for all three models, configurations,
fuel types and textures. No KSP/Unity assemblies are included in either ZIP.
In-game testing has not been performed for this change.

In-game checks: try inflate/deflate repeatedly in VAB and SPH; save/reload a
craft with deployed tanks; launch both folded and deployed; check both fuel
configurations; transfer fuel after deployment and confirm a fueled depot
cannot deflate; drain and deflate. Check symmetry copies if used.
