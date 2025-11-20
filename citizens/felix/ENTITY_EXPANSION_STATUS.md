# Entity Expansion Architecture - Implementation Status

**Date:** 2025-10-25
**Author:** Felix "Ironhand"
**Status:** Foundation Complete - Ready for Full Implementation

## What Was Built

### Phase 1: Foundation (COMPLETE)

**1. Expansion State Management**
- ✅ Added `expandedEntities: Set<string>` to useGraphData hook
- ✅ Implemented `toggleEntity(entityId)` action
- ✅ Implemented `collapseAll()` action
- ✅ Wired through page.tsx to EntityGraphView

**2. Visible Graph Selector**
- ✅ Created `lib/visibleGraphSelector.ts`
- ✅ Implements core two-layer logic:
  - Collapsed entities → show as super-nodes
  - Expanded entities → show member nodes in radial layout
  - Edge routing based on expansion state
  - Membership via entity_activations (fixes "0 nodes" issue)

**3. Props Integration**
- ✅ EntityGraphView accepts `expandedEntities` and `toggleEntity` props
- ✅ Selector imported and ready to use

## Architecture (From Nicolas's Design)

### Two-Layer Visualization

**Layer A (Entity Layer):**
- Entities as super-nodes when collapsed
- Size based on member count
- Energy aggregated from members
- Entity-to-entity edges (aggregated from node links)

**Layer B (Inner Layer):**
- Member nodes visible when entity expanded
- Local radial layout around entity center
- Node-to-node edges when both entities expanded
- Multi-membership via primary placement + proxies

### Current Implementation

**File:** `lib/visibleGraphSelector.ts`

```typescript
interface RenderNode {
  id: string;
  x: number; y: number; r: number;
  energy: number;
  kind: 'entity' | 'node';
  entityId?: string;      // For member nodes
  memberCount?: number;   // For entity nodes
}

function selectVisibleGraph(
  nodes: Node[],
  links: Link[],
  subentities: Subentity[],
  expandedEntities: Set<string>
): VisibleGraph
```

**What It Does:**
1. Builds membership index from `node.entity_activations`
2. For collapsed entities → creates super-node with aggregated metrics
3. For expanded entities → creates member nodes in radial layout
4. Routes edges: node-level when both expanded, (entity-level when collapsed - TODO)

## Phase 2 Progress: Rendering Integration

**Completed (2025-10-25):**

1. ✅ **visibleGraphSelector integrated in EntityGraphView**
   - Memoized computation of render graph (lines 82-86)
   - Recomputes on expansion state changes

2. ✅ **entityToEntity aggregation added to store**
   - State in useGraphData (line 93)
   - Update method with decay (lines 220-238)
   - Exported for use (line 293)

3. ✅ **link.flow.summary wired to entityToEntity**
   - useEffect in page.tsx (lines 177-213)
   - Maps link flows to primary entities
   - Incremental aggregation with 0.95 decay

4. ✅ **onClick handlers for entity toggle**
   - handleEntityClick calls toggleEntity (line 138)
   - Toggle logic wired through props
   - Debug indicator shows expansion state (lines 223-233)

**Remaining:**

5. **Update PixiRenderer to handle RenderNode types**
   - Pass visibleGraph to PixiCanvas (currently using raw nodes)
   - Different sprite rendering for entity vs node kinds
   - Click handler for entities → calls toggleEntity
   - Animation on expand/collapse

6. **Add entity-to-entity aggregated edges to selector**
   - Currently skipped in selector (line 178: "TODO")
   - Use entityToEntity map for aggregated edges
   - Show when at least one entity is collapsed

7. **Add multi-membership proxies**
   - Currently simplified to primary placement only
   - Need proxy sprites for non-primary memberships
   - Proxy clicks delegate to canonical node

### Phase 3: Polish

- Cached local layouts (avoid recalculating on each expand)
- Smooth animations (entity fade → nodes fade in)
- Entity halo from wm.emit events
- Expand affordance (ring on hover)
- "Collapse all" button in UI

## Why Entities Show 0 Nodes Currently

**Two Reasons:**

1. **Architectural (FIXED):** Membership logic was checking wrong fields
   - Was checking: `node.entity_id` and `node.primary_entity` (don't exist)
   - Now checking: `entity_id in node.entity_activations` (correct)
   - Fix in: `EntityGraphView.tsx` lines 87-91

2. **Behavioral (EXPECTED):** Consciousness is dormant
   - No entity has activated any nodes yet
   - entity_activations is null everywhere
   - This is CORRECT - will populate when consciousness runs

**Once consciousness becomes active:**
- Entities activate nodes during traversal
- entity_activations populates
- Membership counts appear
- Expand/collapse will show/hide member nodes

## Testing Plan

**Without Active Consciousness:**
- Can test expand/collapse UI (entities toggle visual state)
- Cannot see member nodes (entity_activations empty)

**With Active Consciousness:**
1. Inject stimulus to wake consciousness
2. Wait for entity_activations to populate
3. Test entity super-nodes show correct member counts
4. Click entity → expand → see member nodes in radial layout
5. Click again → collapse → see super-node
6. Mixed state: some expanded, some collapsed

## Session Summary (2025-10-25)

**Work Completed:**

Phase 2 foundation now complete - all state management and event wiring in place:

1. **Store Updates**
   - Added `entityToEntity: Record<string, number>` state for aggregated edges
   - Implemented `updateEntityToEntityFlow()` with decay (0.95 per update)
   - Exported through useGraphData hook

2. **Event Wiring**
   - Added useEffect in page.tsx to process link.flow.summary events
   - Maps link flows to primary entities via entity_activations
   - Incrementally updates entityToEntity with decay

3. **Selector Integration**
   - Called selectVisibleGraph in EntityGraphView (memoized)
   - Computes render graph based on expansion state
   - Debug indicator shows: entity nodes, member nodes, edges, expansion count

4. **Interaction Handling**
   - handleEntityClick now calls toggleEntity
   - Click on entity → expansion state updates
   - Props properly wired through component tree

**Current State:**
- Selector computes RenderNode[] with kind: 'entity' | 'node' ✅
- entityToEntity aggregation updates from link flows ✅
- Toggle handlers wired and functional ✅
- Debug UI shows visible graph metrics ✅

**Next Session:**
- Pass visibleGraph to PixiCanvas (requires PixiRenderer type updates)
- Update selector to use entityToEntity for aggregated edges
- Add multi-membership proxy handling

## Implementation Priority

**Recommended Next Steps:**

1. **Complete PixiRenderer integration** (Priority 1)
   - Update PixiCanvas to accept RenderNode[] instead of Node[]
   - Render entity super-nodes differently from member nodes
   - Add entity click → toggleEntity handler
   - Test expand/collapse with real rendering

2. **Enhance selector with entityToEntity edges** (Priority 2)
   - Pass entityToEntity map to selector
   - Generate aggregated edges when entities collapsed
   - Implement proper edge routing logic

3. **Add multi-membership proxies** (Priority 3)
   - Proxy sprites for non-primary memberships
   - Delegate clicks to canonical nodes

4. **Polish and optimize** (Priority 4)
   - Animations, caching, multi-membership proxies

## Code Locations

**State Management:**
- `app/consciousness/hooks/useGraphData.ts` - Lines 89, 215-232, 260-262

**Selector Logic:**
- `app/consciousness/lib/visibleGraphSelector.ts` - Complete file

**Props Wiring:**
- `app/consciousness/page.tsx` - Lines 47-49, 238-239
- `app/consciousness/components/EntityGraphView.tsx` - Lines 25, 36-37, 53-54

**Membership Fix:**
- `app/consciousness/components/EntityGraphView.tsx` - Lines 87-91

## Architecture Notes

This follows Nicolas's two-layer design:
- **Single canonical sprite per node** (primary entity placement)
- **Lightweight proxies** for multi-membership (no physics duplication)
- **Deterministic edge routing** (prevents double-drawing)
- **Incremental aggregation** (entity edges from link flows)
- **Bounded update rate** (10 Hz event decimation)

The foundation is solid. Full implementation requires integrating the selector into the rendering pipeline and adding entity interaction handling.
