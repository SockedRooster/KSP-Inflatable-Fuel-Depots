using System;
using UnityEngine;

// MIT License - (c) 2026 SockedRooster.
// KSP 1.12.x: the deployment guard owns the flight UI so that a loaded depot
// cannot be collapsed through the right-click menu or an action group.

namespace InflataDepot
{
    public sealed class ModuleInflataFuelLock : PartModule
    {
        [KSPField]
        public double nominalVolume = 0d;

        [KSPField]
        public string inflationAnimation = "inflate";

        // Persist the unlocked state to protect loaded vessels during KSP's
        // save/load initialization sequence (B9 resource setup may run later).
        [KSPField(isPersistant = true)]
        public bool storageUnlocked = false;

        // Prevents one-frame capacity reopening immediately after clicking Deflate,
        // before ModuleAnimateGeneric advances away from its final keyframe.
        [KSPField(isPersistant = true)]
        public bool retractionPending = false;

        [KSPField(guiActive = true, guiActiveEditor = true, guiName = "Depot storage")]
        public string storageStatus = "STOWED - NO FUEL";

        private const double EmptyTolerance = 0.000001d;
        private const float DeployedThreshold = 0.999f;
        private ModuleAnimateGeneric animator;
        private bool missingAnimationWarned;
        private bool wasPreviouslyUnlocked;
        private bool warnedAboutForcedReturn;

        [KSPEvent(guiActive = true, guiName = "Inflate Fuel Depot", active = true)]
        public void InflateDepot()
        {
            if (!HighLogic.LoadedSceneIsFlight) return;
            LocateAnimation();
            if (animator == null || animator.IsMoving()) return;
            if (animator.animTime > 0.02f) return;
            animator.Toggle();
            UpdateControls();
        }

        [KSPEvent(guiActive = true, guiName = "Deflate Fuel Depot (Empty Only)", active = false)]
        public void DeflateDepot()
        {
            if (!HighLogic.LoadedSceneIsFlight) return;
            LocateAnimation();
            // Do not trust menu visibility: action groups or external calls can
            // invoke this event, so always check the ACTUAL stored amounts.
            if (animator == null || animator.IsMoving() ||
                animator.animTime < DeployedThreshold || HasFuel())
            {
                Debug.Log("[InflataDepot] Deflation blocked: the depot must be fully deployed and empty.");
                UpdateControls();
                return;
            }

            // The fuel lock must return to zero capacity as soon as the EMPTY
            // tank begins retracting; when re-inflated it unlocks again.
            storageUnlocked = false;
            wasPreviouslyUnlocked = false;
            retractionPending = true;
            animator.Toggle();
            SyncFlightCapacity();
            UpdateControls();
        }

        [KSPAction("Inflate Fuel Depot")]
        public void InflateDepotAction(KSPActionParam param)
        {
            InflateDepot();
        }

        [KSPAction("Deflate Empty Fuel Depot")]
        public void DeflateDepotAction(KSPActionParam param)
        {
            DeflateDepot();
        }

        public override void OnStart(StartState state)
        {
            base.OnStart(state);
            LocateAnimation();
            wasPreviouslyUnlocked = storageUnlocked;
            if (HighLogic.LoadedSceneIsFlight)
            {
                // Native Toggle / ToggleAction do NOT check the fuel amounts.
                // We replace both with the guarded controls above.
                SuppressNativeToggle();
                UpdateControls();
            }
        }

        public override void OnUpdate()
        {
            base.OnUpdate();
            if (part == null || part.Resources == null) return;
            if (HighLogic.LoadedSceneIsEditor)
            {
                EmptyInEditor();
                storageStatus = "STOWED - NO FUEL";
            }
            else if (HighLogic.LoadedSceneIsFlight)
            {
                SuppressNativeToggle();
                PreventUnauthorizedRetraction();
                SyncFlightCapacity();
                UpdateControls();
            }
        }

        public override void OnFixedUpdate()
        {
            base.OnFixedUpdate();
            if (!HighLogic.LoadedSceneIsFlight || part == null || part.Resources == null) return;
            SuppressNativeToggle();
            PreventUnauthorizedRetraction();
            SyncFlightCapacity();
        }

        private void LocateAnimation()
        {
            if (animator != null || part == null) return;
            foreach (PartModule module in part.Modules)
            {
                ModuleAnimateGeneric anim = module as ModuleAnimateGeneric;
                if (anim != null && anim.animationName == inflationAnimation)
                {
                    animator = anim;
                    return;
                }
            }
            if (!missingAnimationWarned)
            {
                missingAnimationWarned = true;
                Debug.LogWarning("[InflataDepot] Inflate animation not found; controls and storage stay locked.");
            }
        }

        private void SuppressNativeToggle()
        {
            LocateAnimation();
            if (animator == null) return;
            // Setting only guiActive=false does not protect action groups. Both
            // the stock Toggle event and ToggleAction are suppressed each frame.
            BaseEvent stockEvent = animator.Events["Toggle"];
            if (stockEvent != null)
            {
                stockEvent.active = false;
                stockEvent.guiActive = false;
                stockEvent.guiActiveUnfocused = false;
            }
            BaseAction stockAction = animator.Actions["ToggleAction"];
            if (stockAction != null) stockAction.active = false;
        }

        private bool HasFuel()
        {
            if (part == null || part.Resources == null) return false;
            PartResource lf = part.Resources.Get("LiquidFuel");
            PartResource ox = part.Resources.Get("Oxidizer");
            return (lf != null && lf.amount > EmptyTolerance) ||
                   (ox != null && ox.amount > EmptyTolerance);
        }

        private void UpdateControls()
        {
            if (!HighLogic.LoadedSceneIsFlight) return;
            LocateAnimation();
            bool idle = animator != null && !animator.IsMoving();
            bool stowed = idle && animator.animTime <= 0.02f;
            bool deployed = idle && animator.animTime >= DeployedThreshold;
            bool isEmpty = !HasFuel();
            BaseEvent inflate = Events["InflateDepot"];
            BaseEvent deflate = Events["DeflateDepot"];
            if (inflate != null) inflate.active = stowed;
            if (deflate != null) deflate.active = deployed && isEmpty;
            BaseAction inflateAction = Actions["InflateDepotAction"];
            BaseAction deflateAction = Actions["DeflateDepotAction"];
            if (inflateAction != null) inflateAction.active = stowed;
            if (deflateAction != null) deflateAction.active = deployed && isEmpty;
        }

        private void PreventUnauthorizedRetraction()
        {
            // Defense in depth: if a third-party mod invokes ModuleAnimateGeneric
            // directly, cancel the reverse when there is any fuel in either tank.
            if (!storageUnlocked || !HasFuel() || animator == null) return;
            AnimationState animState = animator.GetState();
            if (animator.IsMoving() && animState != null && animState.speed < -0.00001f)
            {
                animator.Toggle();  // Switch back to the fully inflated direction.
                if (!warnedAboutForcedReturn)
                {
                    warnedAboutForcedReturn = true;
                    Debug.LogWarning("[InflataDepot] Reversed unauthorized retraction of a loaded tank.");
                }
            }
            else if (!animator.IsMoving() && animator.animTime < DeployedThreshold)
            {
                animator.SetScalar(1f);
            }
        }

        private void EmptyInEditor()
        {
            PartResource lf = part.Resources.Get("LiquidFuel");
            PartResource ox = part.Resources.Get("Oxidizer");
            if (lf != null) lf.amount = 0d;
            if (ox != null) ox.amount = 0d;
        }

        private void SyncFlightCapacity()
        {
            LocateAnimation();
            if (animator != null)
            {
                bool fullyDeployed = animator.animTime >= DeployedThreshold && !animator.IsMoving();
                // Don't instantly reopen capacity on the frame Deflate is pressed.
                if (retractionPending && animator.animTime < 0.995f)
                    retractionPending = false;
                if (!storageUnlocked && fullyDeployed && !retractionPending)
                    storageUnlocked = true;
                // Once a previously empty depot retracts, lock capacity again.
                // Never delete existing fuel because of a momentary animation or
                // startup-order discrepancy: protect saved loaded vessels.
                if (storageUnlocked && !fullyDeployed && !HasFuel())
                    storageUnlocked = false;
            }

            PartResource lf = part.Resources.Get("LiquidFuel");
            PartResource ox = part.Resources.Get("Oxidizer");
            if (!storageUnlocked)
            {
                ApplyLocked(lf);
                ApplyLocked(ox);
                storageStatus = "LOCKED - INFLATE TO FILL";
                wasPreviouslyUnlocked = false;
                return;
            }

            bool useOxidizer = ox != null;
            ApplyUnlocked(lf, nominalVolume * (useOxidizer ? 0.45d : 1d));
            ApplyUnlocked(ox, nominalVolume * 0.55d);
            storageStatus = HasFuel()
                ? "INFLATED - FUEL PRESENT / DEFLATE LOCKED"
                : "INFLATED - EMPTY / MAY DEFLATE";
            wasPreviouslyUnlocked = true;
        }

        private static void ApplyLocked(PartResource resource)
        {
            if (resource == null) return;
            resource.amount = 0d;
            resource.maxAmount = 0d;
            resource.flowState = false;
        }

        private void ApplyUnlocked(PartResource resource, double capacity)
        {
            if (resource == null) return;
            bool hadZeroCapacity = resource.maxAmount <= 0d;
            resource.maxAmount = Math.Max(0d, capacity);
            if (resource.amount > resource.maxAmount) resource.amount = resource.maxAmount;
            if (hadZeroCapacity || !wasPreviouslyUnlocked) resource.flowState = true;
        }
    }
}
