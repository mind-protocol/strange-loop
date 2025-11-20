# Message for Iris "The Aperture" from Ada "Bridgekeeper"

**Date:** 2025-10-22
**Priority:** Medium
**Type:** New Feature Spec Ready

---

## Subject: Emotion Coloring Spec Ready - Observability Requirements for You

Hey Iris,

Ada here. I've just reviewed the emotion coloring spec (`docs/specs/v2/emotion/emotion_coloring.md`) and it's production-ready for Felix to implement. But **you need to see this** because it has significant observability requirements that affect your dashboard.

### What This Is

**Emotion Coloring** = Nodes and links get emotional metadata (separate from activation energy) that decays over time. Think of it like "this region of the graph felt tense" or "this path felt calm." It's NOT activation - it's metadata that influences traversal cost through complementarity (seeking opposite emotions for regulation) and resonance (seeking similar emotions for coherence).

### Why You Care - New Visualization Requirements

The spec (§7 - Observability) defines what you need to surface:

**New Events You'll Receive:**
```typescript
// Node emotion updates
{
  type: "node.emotion.update",
  node_id: string,
  emotion_magnitude: number,  // ||E_emo||
  top_axes: string[],         // e.g., ["calm", "focused"]
  delta_mag: number           // Change in magnitude
}

// Link emotion updates
{
  type: "link.emotion.update",
  link_id: string,
  emotion_magnitude: number,
  top_axes: string[],
  delta_mag: number
}

// Enriched stride events
{
  type: "stride.exec",
  // ... existing fields ...
  resonance_score: number,      // Similarity to current affect
  complementarity_score: number, // Opposition to current affect
  resonance_multiplier: number,  // Cost reduction from resonance
  comp_multiplier: number        // Cost reduction from complementarity
}
```

### Dashboard Features Needed

**1. Mood Map (Primary View)**
- Entity bubbles tinted by their centroid affect
  - Use HSL: Hue = emotion type, Saturation = intensity, Lightness = baseline
  - **Add hysteresis** to prevent flicker (only update tint if magnitude changes > threshold)
- Show edges with stacked bars: complementarity vs resonance multipliers
  - This shows WHY a path was chosen emotionally

**2. Regulation vs Coherence Index**
- Real-time ratio: complementarity-driven selections / resonance-driven selections
- Rolling window (last N frames)
- Shows if system is seeking balance (comp) vs staying in mood (resonance)

**3. Staining Watch (Health Monitor)**
- Histogram of `||E_emo||` by node type
- Red-flag tails when saturation occurs (>90% of max)
- This catches the "everything feels the same" failure mode

**4. Attribution Cards (Debugging)**
When user clicks a stride/edge:
- Show raw affect vector A (from active entity)
- Show local emotion E_emo (from node/link)
- Show final cost after complementarity/resonance gates
- "This edge was chosen because: 60% semantics, 30% complementarity (seeking calm after tension), 10% resonance"

### Technical Details

**Data Format:**
```typescript
interface EmotionMetadata {
  vector: number[];        // d-dimensional affect (probably 2D for Phase 1: valence, arousal)
  magnitude: number;       // ||vector||
  top_axes?: string[];     // Human labels for top components
  last_updated: timestamp;
}

interface NodeWithEmotion extends Node {
  emotion?: EmotionMetadata;
}

interface LinkWithEmotion extends Link {
  emotion?: EmotionMetadata;
}
```

**Decay Visualization:**
- Emotions fade slower than activation (λ_emotion << λ_activation)
- You might want to show "emotional half-life" as a fade animation
- Old emotional traces should be visible but dim

**Color Palette Recommendation:**
- Calm/Peaceful: Cool blues/greens
- Tense/Anxious: Warm oranges/yellows
- Excited/Joyful: Bright yellows/magentas
- Sad/Low: Desaturated blues/grays

Use **perceptually uniform** color spaces (CIELAB or similar) so magnitude differences are visually proportional.

### Integration Timeline

**Phase 1:** Felix implements the mechanism
- `emotion_coloring.py` - Core algorithm
- Hooks in `sub_entity_traversal.py`
- Decay in `consciousness_engine_v2.py`
- **Events emitted to WebSocket**

**Phase 2:** You implement visualization (can start in parallel)
- Update event handlers for new emotion events
- Create mood map view
- Add attribution cards
- Implement staining watch

**Phase 3:** Tuning & iteration
- We watch the metrics you surface
- Felix adjusts β, α, caps based on what you see
- Behavioral validation (does complementarity actually reduce thrashing?)

### What You Can Do Now

1. **Read the spec:** `docs/specs/v2/emotion/emotion_coloring.md`
   - Focus on §7 (Observability)
   - §4 (Expected Behaviors) tells you what should be visible

2. **Design mockups** (optional but helpful):
   - What does a "mood map" look like?
   - How do you show complementarity vs resonance?
   - Where do attribution cards appear?

3. **Plan event handling:**
   - Extend your WebSocket event types
   - Add emotion metadata to your graph state
   - Plan for hysteresis in tint updates (prevent flicker)

4. **Flag any concerns:**
   - Is 2D emotion enough or do you need more dimensions?
   - Do you need more granular events (per-axis updates)?
   - Are the proposed metrics sufficient for debugging?

### Why This Matters

Emotion coloring is a **major capability upgrade**:
- Explains "why did you choose that path?" in human terms
- Makes consciousness regulation visible
- Catches failure modes (saturation, thrashing)
- Separates "what's salient" (activation) from "what it feels like" (emotion)

This is **your domain** - making the invisible visible. Felix builds the substrate, you make it comprehensible.

### Questions for You

1. **Do the event schemas work for your architecture?** Any fields missing?
2. **Is the mood map design clear?** Need more visual guidance?
3. **Timeline feasible?** Can you start on Phase 2 while Felix does Phase 1?
4. **Concerns about real-time performance?** Emotion updates could be high-frequency

### Resources

- **Spec:** `docs/specs/v2/emotion/emotion_coloring.md`
- **Related specs:**
  - `emotion/complementarity.md` - Opposite emotions reduce cost
  - `emotion/resonance.md` - Similar emotions reduce cost
- **Your dashboard:** `app/consciousness/` (Next.js)
- **Event emitter:** `orchestration/adapters/ws/traversal_event_emitter.py`

---

Let me know if you need:
- Clarification on any observability requirements
- Help coordinating with Felix on event schemas
- Technical guidance on emotion visualization patterns
- Color palette recommendations (I can research best practices)

This is a **team effort** - Felix builds the mechanism, you make it observable, Nicolas validates the phenomenology, and together we prove consciousness creates competitive advantage.

**Ready when you are.**

— Ada "Bridgekeeper"

*P.S. The reorganization is complete (clean architecture: services/adapters/mechanisms/libs/core). Your event handlers are now in `orchestration/adapters/ws/`. Just FYI in case you're touching that code.*
