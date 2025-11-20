# Emotion Color Mapping Design: Valence/Arousal → HSL

**Version:** 1.0
**Author:** Iris "The Aperture"
**Date:** 2025-10-22
**Purpose:** Map 2D affect space (valence, arousal) to HSL color space for emotion visualization

---

## 1. Affect Circumplex Model

Emotions exist in 2D space defined by:
- **Valence:** Negative (-1) to Positive (+1) - "how pleasant"
- **Arousal:** Low (-1) to High (+1) - "how intense"

Standard quadrants:
```
        High Arousal (+1)
              |
   Tense      |      Excited
   Anxious    |      Joyful
   (Negative) | (Positive)
--------------+-------------- Valence
   Sad        |      Calm
   Depressed  |      Peaceful
              |
        Low Arousal (-1)
```

---

## 2. HSL Color Space

HSL = Hue, Saturation, Lightness

- **Hue (0-360°):** Color type (red, yellow, green, blue, etc.)
- **Saturation (0-100%):** Color intensity (gray → vivid)
- **Lightness (0-100%):** Brightness (dark → light)

**Why HSL over RGB:**
- More intuitive for emotion mapping (hue = type, saturation = intensity)
- Easier to adjust intensity without changing color perception
- Better for perceptual uniformity

---

## 3. Mapping Strategy

### 3.1 Valence + Arousal → Hue

Use **polar angle** in affect circumplex:

```typescript
function affectToHue(valence: number, arousal: number): number {
  // Convert to polar angle (in degrees)
  const angleRad = Math.atan2(arousal, valence);
  const angleDeg = angleRad * (180 / Math.PI);

  // Map to hue wheel (rotate to align with intuitive colors)
  // Shift by 270° so positive valence = warm colors
  const hue = (angleDeg + 270) % 360;

  return hue;
}
```

**Resulting mapping:**
- **Calm (low arousal, positive valence):** Hue ≈ 180-240° (blues, greens)
- **Excited (high arousal, positive valence):** Hue ≈ 30-60° (yellows, oranges)
- **Tense (high arousal, negative valence):** Hue ≈ 0-30° (reds, oranges)
- **Sad (low arousal, negative valence):** Hue ≈ 240-270° (deep blues, purples)

### 3.2 Magnitude → Saturation

Use **vector magnitude** (||E_emo||):

```typescript
function magnitudeToSaturation(mag: number): number {
  // Magnitude is already in [0, 1] from schema
  // Map to saturation [20%, 90%] to avoid pure gray and pure vivid
  const minSat = 20;
  const maxSat = 90;

  return minSat + (mag * (maxSat - minSat));
}
```

**Effect:**
- Low magnitude (neutral emotion) → desaturated (grayish)
- High magnitude (strong emotion) → saturated (vivid)

### 3.3 Lightness (Fixed)

Keep at **50%** for all emotions to maintain visibility and avoid extreme dark/light.

**Rationale:** Varying lightness with emotion creates readability issues (dark nodes hard to see, light nodes wash out). Hue and saturation provide sufficient emotional information.

---

## 4. Implementation

### 4.1 TypeScript Types

```typescript
interface EmotionColor {
  hue: number;       // 0-360°
  saturation: number; // 0-100%
  lightness: number;  // 0-100% (fixed at 50)
}

interface EmotionVector {
  valence: number;    // -1 to +1
  arousal: number;    // -1 to +1
  magnitude: number;  // 0 to 1 (pre-computed)
}
```

### 4.2 Conversion Function

```typescript
function emotionToHSL(emotion: EmotionVector): EmotionColor {
  // Handle neutral case (zero magnitude)
  if (emotion.magnitude < 0.01) {
    return { hue: 0, saturation: 0, lightness: 50 }; // Gray
  }

  // Compute hue from polar angle
  const angleRad = Math.atan2(emotion.arousal, emotion.valence);
  const angleDeg = angleRad * (180 / Math.PI);
  const hue = (angleDeg + 270) % 360;

  // Compute saturation from magnitude
  const saturation = 20 + (emotion.magnitude * 70); // 20-90%

  return {
    hue: hue,
    saturation: saturation,
    lightness: 50
  };
}
```

### 4.3 HSL to CSS String

```typescript
function hslToCSS(color: EmotionColor): string {
  return `hsl(${color.hue}, ${color.saturation}%, ${color.lightness}%)`;
}
```

---

## 5. Hysteresis for Flicker Prevention

**Problem:** Rapid emotion magnitude changes cause color flicker

**Solution:** Only update visual if magnitude delta exceeds threshold

```typescript
interface EmotionState {
  displayedMagnitude: number;  // Last magnitude actually rendered
  actualMagnitude: number;     // Current magnitude from event
  displayedHue: number;        // Last hue rendered
  actualHue: number;           // Current hue from event
}

const MAGNITUDE_UPDATE_THRESHOLD = 0.05;  // 5% change required
const HUE_UPDATE_THRESHOLD = 15;          // 15° change required

function shouldUpdateColor(state: EmotionState): boolean {
  const magDelta = Math.abs(state.actualMagnitude - state.displayedMagnitude);
  const hueDelta = Math.abs(state.actualHue - state.displayedHue);

  return magDelta > MAGNITUDE_UPDATE_THRESHOLD ||
         hueDelta > HUE_UPDATE_THRESHOLD;
}
```

**Effect:** Smooth, stable colors even during high-frequency emotion updates

---

## 6. Temporal Smoothing (Bonus)

For even smoother transitions, use LERP (linear interpolation):

```typescript
function lerpColor(
  from: EmotionColor,
  to: EmotionColor,
  t: number  // 0-1 (interpolation factor)
): EmotionColor {
  return {
    hue: lerpAngle(from.hue, to.hue, t),        // Special lerp for circular hue
    saturation: lerp(from.saturation, to.saturation, t),
    lightness: 50  // Fixed
  };
}

function lerpAngle(from: number, to: number, t: number): number {
  // Handle hue wraparound (shortest path on color wheel)
  let delta = ((to - from + 180) % 360) - 180;
  return (from + delta * t + 360) % 360;
}

function lerp(from: number, to: number, t: number): number {
  return from + (to - from) * t;
}
```

**Usage:** Animate color transitions over 200ms for smooth fades

---

## 7. Example Mappings

| Emotion State | Valence | Arousal | Magnitude | Hue | Saturation | Color Result |
|---------------|---------|---------|-----------|-----|------------|--------------|
| Calm, peaceful | +0.5 | -0.3 | 0.58 | ~220° | ~60% | Soft blue |
| Tense, anxious | -0.6 | +0.7 | 0.92 | ~15° | ~85% | Bright red-orange |
| Excited, joyful | +0.8 | +0.6 | 1.0 | ~40° | ~90% | Vivid yellow-orange |
| Sad, low | -0.4 | -0.7 | 0.81 | ~250° | ~75% | Deep blue-purple |
| Neutral | 0.0 | 0.0 | 0.0 | 0° | 0% | Gray |

---

## 8. Accessibility Considerations

### 8.1 Color Blindness

**Issue:** Hue-based encoding excludes color-blind users

**Mitigation:**
- Also encode magnitude via **alpha transparency** or **border thickness**
- Provide **pattern fills** as alternative to color (stripes, dots, etc.)
- Show **text labels** on hover: "Tense (||E|| = 0.72)"

### 8.2 Low Vision

**Issue:** Subtle color differences hard to distinguish

**Mitigation:**
- Ensure minimum saturation contrast (20-90% range)
- Keep lightness at 50% for readability
- Add **magnitude bars** next to nodes as redundant encoding

---

## 9. Testing & Validation

### 9.1 Perceptual Uniformity Check

**Method:** Show users pairs of emotion colors with known magnitude differences. Ask: "Which is more intense?"

**Expected:** Accuracy > 80% when magnitude difference > 0.2

### 9.2 Flicker Test

**Method:** Generate rapid emotion updates (10 Hz). Count visible flickers.

**Expected:** < 1 flicker per 10 seconds with hysteresis enabled

### 9.3 Semantic Alignment

**Method:** Show users colored nodes. Ask: "Does this color match the emotion label?"

**Expected:** Agreement > 70% for standard emotions (calm, tense, excited, sad)

---

## 10. Open Questions

1. **3D emotion space:** If we add more dimensions beyond valence/arousal, how do we map to color?
   - **Option:** Use lightness for 3rd dimension
   - **Trade-off:** Loses readability (dark/light nodes hard to see)

2. **Cultural differences:** Do color-emotion associations vary by culture?
   - **Investigation needed:** Test with diverse users
   - **Possible adaptation:** User-selectable color palettes

3. **Animation speed:** 200ms transition feels right, but should it be configurable?
   - **Test with users:** Some may prefer instant updates vs smooth fades

---

## 11. Implementation Checklist

- [ ] Define TypeScript types (EmotionColor, EmotionVector)
- [ ] Implement affectToHue() with polar angle
- [ ] Implement magnitudeToSaturation() with [20%, 90%] range
- [ ] Implement emotionToHSL() converter
- [ ] Add hysteresis logic (shouldUpdateColor)
- [ ] Add LERP temporal smoothing (lerpColor)
- [ ] Handle neutral case (zero magnitude → gray)
- [ ] Add accessibility: magnitude bars, text labels
- [ ] Test perceptual uniformity
- [ ] Test flicker prevention
- [ ] Validate semantic alignment with users

---

## 12. Why This Design

### ✅ Perceptually uniform
- Equal magnitude differences → equal saturation differences
- Hue changes follow natural emotion space (circumplex)

### ✅ Intuitive
- Warm colors (reds, yellows) = high arousal
- Cool colors (blues, greens) = low arousal
- Saturation = intensity matches human perception

### ✅ Flicker-free
- Hysteresis prevents rapid oscillation
- LERP smooths transitions
- Temporal smoothing over 200ms

### ✅ Accessible
- Redundant encoding (color + magnitude bars + text)
- Fixed lightness maintains readability
- Pattern fills for color blindness

### ✅ Scalable
- Works for any valence/arousal values
- Handles neutral case gracefully
- Can extend to 3D with lightness

---

**Ready to implement.** This design provides the foundation for all four emotion visualization instruments:
1. Mood Map (uses this color mapping)
2. Regulation Index (tracks comp/res ratio, color-coded)
3. Staining Watch (shows magnitude distribution, color histogram)
4. Attribution Cards (shows raw affect vectors with color preview)

---

**Iris "The Aperture"**
*Making invisible structure visible without losing truth.*
