# InflataDepot roadmap

## Release blocker: collision validation
The previous beta intentionally had docking-base collision only. The experimental build adds a compact **convex non-trigger mesh collider** as a child of `InflatableAssembly`, so it follows the exact same 20-second scale animation. It is smaller than the visible cylinder to prevent false-positive surface contacts. This is *not tested inside KSP yet*. Before stable release, verify:

1. Collisions against ship parts in flight (after fully deploying).
2. Kerbals on EVA cannot pass through deployed wall; no interaction glitches.
3. Save and reload a deployed station and verify collider still matches the visual tank.
4. Warp/physics-warp and proximity to station parts; avoid inflation intersecting attached hardware.
5. Dock, decouple, redock and verify port remains functional.
6. Check all three sizes separately.
7. Watch KSP.log for rigidbody/convex collider errors.

Animated colliders are experimental and may apply forces during growth. Be careful with docking vessels and keep distance. If this does not work reliably, use a custom PartModule/Unity DLL to switch from a collapsed collision mesh to a full-size deployed hull after animation completes (future option).

## Future fuel selection expansion (do not enable without balancing)
- Oxidizer-only, Monopropellant, XenonGas, Ore (stock resources).
- Conditional Cryogenic/LH2 or mod-resource presets: only when corresponding resource definition and mod integration is present.
- Balance mass, capacity in physical storage-volume terms (B9 ratios), cost, boiloff/thermal traits and Kerbalism compatibility by resource.
- Keep **one part per tank diameter**, with the `Fuel Configuration` selector. No extra VAB duplicates.
- Optional: add fuel transfer/deployment lock if a safe compatible module is developed.
