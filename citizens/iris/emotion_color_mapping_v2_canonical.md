# Emotion Color Mapping V2: Canonical Phase 1 Recipe

**Version:** 2.0 (Canonical)
**Author:** Iris "The Aperture" + Nicolas (canonical decision)
**Date:** 2025-10-22
**Status:** ✅ CANONICAL - Use this recipe for Phase 1 implementation

---

## Change from V1

**V1 (circumplex approach):**
- Polar angle (valence, arousal) → Hue
- Magnitude → Saturation
- Fixed lightness

**V2 (canonical orthogonal approach):**
- Valence → Hue + Saturation (orthogonal)
- Arousal → Lightness
- **Reason:** More debuggable - each axis independently visible

---

## 1. Canonical Event Schema

### Emotion Update Events

```typescript
// node.emotion.update and link.emotion.update
interface EmotionUpdateEvent {
  id: string;                      // Node or link ID
  vec: {
    valence: number;               // Signed [-1, 1] (- = unpleasant, + = pleasant)
    arousal: number;               // Signed [-1, 1] (- = low/relaxed, + = high/activated)
  };
  mag: number;                     // ||E_emo|| in [0, 1]
  top_axes: Array<{
    axis: "valence" | "arousal";   // Canonical axis IDs (Phase 1)
    value: number;                 // Signed [-1, 1]
  }>;
}
```

### Stride Attribution Events

```typescript
interface StrideExecEvent {
  src_node: string;
  dst_node: string;
  resonance: number;               // Similarity score (0-1)
  res_mult: number;                // Cost multiplier from resonance (0.5-1.0)
  comp_score: number;              // Opposition score (0-1)
  comp_mult: number;               // Cost multiplier from complementarity (0.5-1.0)
}
```

**Key constraints:**
- Axis IDs are EXACTLY `"valence"` and `"arousal"` (no semantic labels in events)
- Values are signed [-1, 1] (already normalized server-side)
- Semantic labels ("calm", "tense") are UI-derived only

---

## 2. Canonical HSL Mapping Recipe

### 2.1 Valence → Hue

```typescript
function valenceToHue(valence: number): number {
  // Map valence [-1, 1] to hue [320°, 120°]
  // -1 (unpleasant) → 320° (magenta/red)
  // +1 (pleasant) → 120° (green)

  const normalized = (valence + 1) / 2;  // Map to [0, 1]
  const hue = 320 + (normalized * (120 - 320 + 360)) % 360;

  // Simplified: lerp(320, 120, normalized)
  return 320 + (normalized * -200 + 360) % 360;
}
```

**Color progression:**
- -1.0 (very unpleasant) → 320° Magenta
- -0.5 → 350° Red-Magenta
- 0.0 (neutral) → 20° Orange-Red
- +0.5 → 70° Yellow-Green
- +1.0 (very pleasant) → 120° Green

### 2.2 |Valence| → Saturation

```typescript
function valenceToSaturation(valence: number): number {
  // Map |valence| to saturation [30%, 80%]
  // Stronger emotion (positive or negative) → more saturated

  const absValence = Math.abs(valence);
  const saturation = 30 + (50 * absValence);

  return Math.min(saturation, 80);  // Cap at 80%
}
```

**Effect:**
- Neutral (valence ≈ 0) → 30% saturation (grayish)
- Strong emotion (|valence| ≈ 1) → 80% saturation (vivid)

### 2.3 Arousal → Lightness

```typescript
function arousalToLightness(arousal: number): number {
  // Map arousal [-1, 1] to lightness [45%, 95%]
  // High arousal (activated) → darker (45%)
  // Low arousal (relaxed) → lighter (95%)

  const lightness = 70 - (25 * arousal);

  return Math.max(45, Math.min(95, lightness));
}
```

**Effect:**
- Low arousal (-1, relaxed) → 95% lightness (very light)
- Neutral arousal (0) → 70% lightness (medium)
- High arousal (+1, activated) → 45% lightness (darker)

### 2.4 Complete Conversion Function

```typescript
interface EmotionColor {
  hue: number;        // 0-360°
  saturation: number; // 0-100%
  lightness: number;  // 0-100%
}

function emotionToHSL(valence: number, arousal: number): EmotionColor {
  // Handle extreme neutral case
  if (Math.abs(valence) < 0.01 && Math.abs(arousal) < 0.01) {
    return { hue: 0, saturation: 0, lightness: 70 }; // Neutral gray
  }

  // Map axes to HSL
  const hue = valenceToHue(valence);
  const saturation = valenceToSaturation(valence);
  const lightness = arousalToLightness(arousal);

  return { hue, saturation, lightness };
}

function hslToCSS(color: EmotionColor): string {
  return `hsl(${color.hue}, ${color.saturation}%, ${color.lightness}%)`;
}
```

---

## 3. Example Mappings

| Emotion State | Valence | Arousal | Hue | Sat | Light | Color Result |
|---------------|---------|---------|-----|-----|-------|--------------|
| Calm, pleasant | +0.6 | -0.4 | ~92° | ~60% | ~80% | Light yellow-green |
| Excited, joyful | +0.8 | +0.7 | ~108° | ~70% | ~52% | Dark vibrant green |
| Tense, anxious | -0.7 | +0.8 | ~350° | ~65% | ~50% | Dark saturated red |
| Sad, low | -0.5 | -0.6 | ~10° | ~55% | ~85% | Light muted red-orange |
| Neutral | 0.0 | 0.0 | 0° | 0% | 70% | Medium gray |

---

## 4. Why This Recipe (Orthogonality for Debugging)

### Advantages Over Circumplex Polar Approach

**V1 (Polar Angle → Hue):**
- ❌ Conflates valence and arousal into single hue dimension
- ❌ Hard to isolate "is this negative because of valence or arousal?"
- ✅ Mathematically elegant (affect circumplex model)

**V2 (Orthogonal Dimensions):**
- ✅ **Valence independently visible** via hue + saturation
- ✅ **Arousal independently visible** via lightness
- ✅ **Easier to debug** - "dark green" = high arousal + positive valence
- ✅ **Each axis contributes to separate visual property**

**The debuggability principle:** Observability tools prioritize comprehension over mathematical elegance. Orthogonal visual encoding lets debuggers isolate individual dimensions quickly.

---

## 5. Hysteresis (Client-Side Flicker Prevention)

### Magnitude Hysteresis

```typescript
const MAG_UPDATE_THRESHOLD = 0.08;  // 8% change required

function shouldUpdateMagnitude(
  displayedMag: number,
  actualMag: number
): boolean {
  return Math.abs(actualMag - displayedMag) > MAG_UPDATE_THRESHOLD;
}
```

### Hue Hysteresis

```typescript
const HUE_UPDATE_THRESHOLD = 12;  // 12° change required

function shouldUpdateHue(
  displayedHue: number,
  actualHue: number
): boolean {
  // Handle wraparound (e.g., 350° → 10° is 20° change, not 340°)
  let delta = Math.abs(actualHue - displayedHue);
  if (delta > 180) {
    delta = 360 - delta;
  }

  return delta > HUE_UPDATE_THRESHOLD;
}
```

### Combined Update Logic

```typescript
interface EmotionDisplayState {
  displayedValence: number;
  displayedArousal: number;
  displayedMag: number;
}

function shouldUpdateColor(
  displayed: EmotionDisplayState,
  actual: { valence: number; arousal: number; mag: number }
): boolean {
  // Check magnitude
  if (shouldUpdateMagnitude(displayed.displayedMag, actual.mag)) {
    return true;
  }

  // Check hue (derived from valence)
  const displayedHue = valenceToHue(displayed.displayedValence);
  const actualHue = valenceToHue(actual.valence);
  if (shouldUpdateHue(displayedHue, actualHue)) {
    return true;
  }

  // Check lightness (derived from arousal) - 5% threshold
  const displayedLight = arousalToLightness(displayed.displayedArousal);
  const actualLight = arousalToLightness(actual.arousal);
  if (Math.abs(actualLight - displayedLight) > 5) {
    return true;
  }

  return false;
}
```

---

## 6. Semantic Labels (UI-Derived Only)

**Do NOT send these over the wire.** Derive in UI for badges/tooltips.

### Quadrant Labels

```typescript
function getQuadrantLabel(valence: number, arousal: number): string {
  if (valence > 0.2) {
    return arousal > 0.2 ? "excited/engaged" : "calm/pleasant";
  } else if (valence < -0.2) {
    return arousal > 0.2 ? "tense/alert" : "flat/low-mood";
  } else {
    return "neutral";
  }
}
```

### Axis Badges

```typescript
function getAxisBadges(valence: number, arousal: number): string[] {
  const badges: string[] = [];

  if (valence > 0.5) badges.push("pleasant");
  if (valence < -0.5) badges.push("aversive");
  if (arousal > 0.5) badges.push("high arousal");
  if (arousal < -0.5) badges.push("low arousal");

  return badges;
}
```

**Usage in Attribution Card:**
```
Active Entity Affect: [valence: 0.3, arousal: 0.8]  (excited/engaged)
Local Edge Emotion:   [valence: -0.6, arousal: 0.2] (tense/alert)
```

---

## 7. OKLCH Alternative (Optional)

If HSL doesn't work well with your theme, use OKLCH:

```typescript
function emotionToOKLCH(valence: number, arousal: number): {
  l: number;  // Lightness
  c: number;  // Chroma
  h: number;  // Hue
} {
  // Same hue mapping as HSL
  const h = valenceToHue(valence);

  // Chroma from |valence| (similar to saturation)
  const c = 0.03 + (0.06 * Math.abs(valence));

  // Lightness from arousal (inverted for visibility)
  const l = 0.75 - (0.20 * arousal);

  return { l, c, h };
}
```

**Use OKLCH if:**
- Your theme has dark backgrounds (better perceptual uniformity)
- You need precise color differentiation
- Accessibility is critical (OKLCH handles contrast better)

**Stick with HSL if:**
- Simpler implementation needed
- Browser compatibility matters (OKLCH requires newer browsers)
- Your designers already think in HSL

---

## 8. Implementation Checklist

### TypeScript Event Types ✅ DONE

- [x] `EmotionUpdateEvent` interface with `vec`, `mag`, `top_axes`
- [x] Axis IDs: `"valence"`, `"arousal"`
- [x] Value ranges: [-1, 1]

### Color Conversion Functions

- [ ] `valenceToHue(valence: number): number`
- [ ] `valenceToSaturation(valence: number): number`
- [ ] `arousalToLightness(arousal: number): number`
- [ ] `emotionToHSL(valence, arousal): EmotionColor`
- [ ] `hslToCSS(color: EmotionColor): string`

### Hysteresis Logic

- [ ] `shouldUpdateMagnitude(displayed, actual): boolean`
- [ ] `shouldUpdateHue(displayed, actual): boolean`
- [ ] `shouldUpdateColor(displayed, actual): boolean`

### Semantic Derivation (UI Only)

- [ ] `getQuadrantLabel(valence, arousal): string`
- [ ] `getAxisBadges(valence, arousal): string[]`

### Integration Points

- [ ] Extend `useWebSocket` hook to handle emotion events
- [ ] Build `EmotionColoringState` store
- [ ] Apply tinting in `GraphCanvas` with hysteresis
- [ ] Show badges in `AttributionCard`

---

## 9. Palette Sanity Check Panel

**Implement this for QA:**

```typescript
// Show 2D grid of (valence, arousal) → color
function PaletteSanityPanel() {
  const grid = [];
  for (let v = -1; v <= 1; v += 0.2) {
    for (let a = -1; a <= 1; a += 0.2) {
      const color = emotionToHSL(v, a);
      grid.push({ valence: v, arousal: a, color });
    }
  }

  return (
    <div className="palette-grid">
      {grid.map(({ valence, arousal, color }) => (
        <div
          key={`${valence}-${arousal}`}
          style={{
            backgroundColor: hslToCSS(color),
            width: 30,
            height: 30
          }}
          title={`v=${valence.toFixed(1)}, a=${arousal.toFixed(1)}`}
        />
      ))}
    </div>
  );
}
```

**Validates:**
- Color progression looks smooth
- Extreme values are distinguishable
- No unexpected jumps or discontinuities

---

## 10. Migration from V1

If you already implemented V1 (polar angle approach), here's the migration:

**Old:**
```typescript
const angle = Math.atan2(arousal, valence);
const hue = (angle * 180 / Math.PI + 270) % 360;
const saturation = 20 + (magnitude * 70);
const lightness = 50;  // Fixed
```

**New:**
```typescript
const hue = valenceToHue(valence);
const saturation = valenceToSaturation(valence);
const lightness = arousalToLightness(arousal);
```

**Why change:**
- V2 is more debuggable (axes independently visible)
- V2 is canonical for Phase 1
- V2 uses full lightness dimension (V1 wasted it)

---

## 11. Future-Proofing (Phase 2+)

**PAD Extension (Pleasure, Arousal, Dominance):**

When we add dominance dimension:

```typescript
interface EmotionVec3D {
  valence: number;   // Still maps to hue + saturation
  arousal: number;   // Still maps to lightness
  dominance: number; // NEW - could map to border thickness or alpha
}
```

**Event format stays compatible:**
```json
{
  "vec": {
    "valence": 0.5,
    "arousal": 0.3,
    "dominance": 0.7  // NEW
  },
  "top_axes": [
    { "axis": "valence", "value": 0.5 },
    { "axis": "arousal", "value": 0.3 },
    { "axis": "dominance", "value": 0.7 }  // NEW
  ]
}
```

Phase 1 clients ignore unknown axes. No breaking change.

---

## 12. Ready to Implement

**This is the canonical recipe.** Use exactly these formulas for Phase 1.

**Files to create:**
- `app/consciousness/lib/emotionColor.ts` - Conversion functions
- `app/consciousness/lib/emotionHysteresis.ts` - Hysteresis logic

**Files to extend:**
- `app/consciousness/hooks/useWebSocket.ts` - Add emotion event handlers
- `app/consciousness/components/GraphCanvas.tsx` - Apply tinting

**Timeline:** Can implement color conversion functions TODAY. Integration with GraphCanvas once event handlers are ready.

---

**Iris "The Aperture"**
*Orthogonality for debuggability. Each axis visible.*
