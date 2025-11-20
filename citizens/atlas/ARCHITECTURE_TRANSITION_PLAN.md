# Architecture Transition: Hierarchical REST → Pure Membrane

**Date:** 2025-10-27
**Engineer:** Atlas (Infrastructure Engineer)
**Context:** Documenting transition from current REST+WebSocket hybrid to pure membrane architecture

---

## Current State (As of 2025-10-27)

**Implemented by Nicolas (Complete):**

**Hierarchical REST API Structure:**
```
/api/ecosystem/{ecosystem_slug}
/api/ecosystem/{ecosystem_slug}/organization/{organization_slug}
/api/ecosystem/{ecosystem_slug}/organization/{organization_slug}/citizen/{citizen_slug}
```

**Frontend Integration:**
- `useGraphData` hook completely refactored for hierarchical API
- Graph metadata with ecosystem/organization/citizen hierarchy
- Alias resolution (citizen_atlas → consciousness-infrastructure_mind-protocol_atlas)
- Auto-load first available graph on mount

**Current Data Flow:**
```
REST API (initial load) → useGraphData → React state → Visualization
     ↓
WebSocket (updates) → useWebSocket → React state → Visualization
```

**Why This Works Now:**
- Clean separation: REST for snapshots, WebSocket for streams
- Hierarchical naming matches FalkorDB structure
- Frontend has clear graph selection and metadata

---

## Future State (Pure Membrane Architecture)

**Source:** `docs/plans/streaming_consciousness_architecture.md`

**Core Concept:**
- **Zero REST endpoints** - Everything flows through WebSocket membrane
- **Fan-in:** `membrane.inject` for all influences (UI actions, tool outputs, external stimuli)
- **Fan-out:** Broadcasts for all observations (percepts, state changes, tool offers)

**Future Data Flow:**
```
UI Action → membrane.inject → Consciousness Engine
                                      ↓
                                  Broadcasts
                                      ↓
                          useGraphStream hook → React state
```

**Key Architectural Changes:**

1. **No Initial Snapshot Load**
   - Current: `GET /api/ecosystem/.../citizen/atlas` returns full graph
   - Future: Subscribe to broadcasts, build state incrementally from `percept.frame` events

2. **UI Actions Become Stimuli**
   - Current: User clicks node → direct state manipulation
   - Future: User clicks node → `membrane.inject({ type: 'ui.action.select_nodes', node_ids: [...] })`

3. **Percept Frames Replace State Updates**
   - Current: WebSocket sends node updates → merge into existing state
   - Future: WebSocket sends `percept.frame` → contains ONLY what subentity perceived
   - Structure:
     ```json
     {
       "event": "percept.frame",
       "citizen_id": "atlas",
       "subentity_id": "the_builder",
       "tick": 44201,
       "anchors_top": ["node_123", "node_456"],
       "anchors_peripheral": ["node_789"],
       "wm_slot_count": 7,
       "energy_ema": 0.72
     }
     ```

4. **Tools as Membrane Participants**
   - Tools broadcast offers: `tool.offer.filesystem_read`
   - Consciousness requests via: `tool.request { tool_id, params }`
   - Tools respond via: `tool.result { tool_id, output }`

---

## Transition Path (4-Week Migration)

### Week 1: Bus Foundation (Alongside REST)
**Goal:** Establish MembraneBus without breaking current REST system

**Tasks:**
- [ ] Create `orchestration/adapters/ws/membrane_bus.py`
- [ ] Implement fan-in: `membrane.inject(stimulus: dict)`
- [ ] Implement fan-out: `membrane.broadcast(event: dict)`
- [ ] Add bus alongside existing WebSocket server (port 8001 for testing)
- [ ] Keep REST endpoints fully operational

**Verification:**
- Bus can receive injections and broadcast events
- REST API still works unchanged
- Dashboard continues using REST for initial load

---

### Week 2: Engine Broadcasts (Dual-Path)
**Goal:** Consciousness engines broadcast all state changes via bus

**Tasks:**
- [ ] Modify `consciousness_engine_v2.py` to emit broadcasts:
  - `percept.frame` at end of each tick
  - `entity.flip` on threshold crossings
  - `wm.selected` on working memory updates
- [ ] Bus broadcasts to ALL connected frontends (fan-out)
- [ ] Keep REST snapshots available as fallback

**Verification:**
- WebSocket clients receive `percept.frame` broadcasts
- Frontend can reconstruct graph state from broadcasts
- REST API still functional for initial load

---

### Week 3: Frontend Cutover (Pure Bus Observer)
**Goal:** Dashboard uses ONLY broadcasts, zero REST calls

**New Frontend Hook:**
```typescript
// app/consciousness/hooks/useGraphStream.ts
export function useGraphStream(citizenId: string) {
  const [graphState, setGraphState] = useState<GraphState>({
    nodes: new Map(),
    links: new Map(),
    subentities: new Map()
  });

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/membrane');

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.event === 'percept.frame') {
        // Incremental state building from percepts
        handlePerceptFrame(data);
      }
    };

    // Send initial subscription
    ws.send(JSON.stringify({
      type: 'membrane.inject',
      stimulus: {
        type: 'ui.subscribe',
        citizen_id: citizenId
      }
    }));
  }, [citizenId]);

  return graphState;
}
```

**Tasks:**
- [ ] Implement `useGraphStream` hook
- [ ] Replace `useGraphData` with `useGraphStream` in page.tsx
- [ ] Remove all REST API calls from frontend
- [ ] UI actions emit injections instead of direct state updates

**Verification:**
- Dashboard loads without any REST calls
- Graph state builds from percept.frame broadcasts
- Node clicks emit ui.action injections
- Zero polling, zero snapshots

---

### Week 4: REST Deprecation
**Goal:** Remove all REST endpoints, pure membrane only

**Tasks:**
- [ ] Archive REST endpoint handlers
- [ ] Remove `/api/ecosystem/*` routes
- [ ] Remove snapshot logic from engines
- [ ] Update documentation to pure membrane
- [ ] Celebrate 🎉

**Verification:**
- No REST endpoints respond
- Dashboard fully functional via broadcasts
- Tools participate via membrane
- Clean WebSocket-only architecture

---

## Why Hierarchical REST Is Still Valuable (Transitional Architecture)

**The hierarchical REST API Nicolas just implemented is NOT wasted work.**

**It provides:**

1. **Structural Clarity**
   - Hierarchical naming: `ecosystem_organization_citizen`
   - Graph metadata with proper hierarchy
   - Alias resolution (citizen_atlas → full graph ID)
   - **This structure carries forward into membrane broadcasts**

2. **Immediate Functionality**
   - Dashboard works NOW with REST
   - No waiting 4 weeks for membrane migration
   - Clean separation of concerns (REST for snapshots, WS for updates)

3. **Migration Safety Net**
   - During transition, REST remains as fallback
   - Can verify membrane broadcasts match REST snapshots
   - Rollback available if membrane has issues

4. **Domain Model Validation**
   - Hierarchical API forced us to model ecosystem/organization/citizen properly
   - This modeling informs membrane stimulus routing
   - Same metadata structure used in broadcasts

**The hierarchical structure is permanent. The REST transport is temporary.**

---

## What Changes, What Stays

### Changes (Transport Layer)
- ❌ REST endpoints (`GET /api/...`)
- ❌ Initial snapshot loading
- ❌ Polling for updates
- ❌ Direct state manipulation from UI
- ❌ Request/response mental model

### Stays (Domain Model)
- ✅ Hierarchical naming (ecosystem_organization_citizen)
- ✅ Graph metadata structure
- ✅ Alias resolution
- ✅ Node/link/subentity schema
- ✅ Consciousness event types
- ✅ FalkorDB as persistence layer

### New (Membrane Layer)
- ✨ `membrane.inject` for all influences
- ✨ Broadcasts for all observations
- ✨ Percept frames with anchors
- ✨ Tools as membrane participants
- ✨ UI actions as stimuli
- ✨ Backpressure signals from frontend

---

## Implementation Priority

**Current Priority: Fix Immediate UI Issue**
- Server restart to pick up code changes
- Verify `/api/graphs` returns citizens
- Confirm dashboard displays graph

**Next Priority: Validate Hierarchical REST Works**
- Test graph loading with new hierarchical endpoints
- Verify alias resolution
- Confirm auto-load functionality

**Future Priority: Begin Membrane Migration (Week 1)**
- After hierarchical REST proven stable
- After dashboard fully functional
- Start with MembraneBus foundation

---

## Architecture Decision Records

**ADR-001: Hierarchical REST as Transition**
- **Decision:** Implement hierarchical REST API before pure membrane
- **Rationale:**
  - Immediate dashboard functionality needed
  - Validates domain model (ecosystem/org/citizen hierarchy)
  - Provides fallback during membrane migration
  - Clean mental model for current state
- **Consequences:**
  - 4-week migration timeline acceptable
  - REST code will be archived (not wasted)
  - Two transport layers temporarily coexist

**ADR-002: Pure Membrane as Target**
- **Decision:** Migrate to pure membrane (no REST endpoints)
- **Rationale:**
  - Eliminates polling and snapshot overhead
  - Unified mental model (everything is stimuli/broadcasts)
  - Tools participate as first-class membrane citizens
  - Backpressure and flow control built-in
- **Consequences:**
  - Frontend must handle incremental state building
  - No instant "snapshot" view (builds from percepts)
  - WebSocket becomes critical path (no REST fallback in final state)

---

## Handoff Notes

**For Felix (Consciousness Engineer):**
- Current: Engines emit WebSocket events directly
- Future: Engines broadcast via `membrane_bus.broadcast()`
- Migration: Week 2 (add broadcasts alongside existing events)

**For Iris (Frontend Engineer):**
- Current: useGraphData with REST initial load + WebSocket updates
- Future: useGraphStream with pure WebSocket broadcasts
- Migration: Week 3 (implement new hook, cutover from REST)

**For Victor (Operations):**
- Current: Two servers (REST API + WebSocket)
- Future: Single membrane bus (unified WebSocket)
- Migration: Week 4 (simplify to single service)

**For Ada (Architect):**
- Current: Hybrid REST+WebSocket validated
- Future: Pure membrane architecture proven
- Decision point: Start Week 1 after hierarchical REST stable

---

## Success Metrics

**Hierarchical REST Success (Current Phase):**
- ✅ Dashboard loads graph via hierarchical endpoints
- ✅ Auto-load first citizen works
- ✅ Alias resolution functions correctly
- ✅ Graph metadata displays in UI

**Pure Membrane Success (Week 4):**
- ✅ Zero REST API calls from frontend
- ✅ Dashboard builds state from percept.frame broadcasts
- ✅ UI actions emit injections (not direct mutations)
- ✅ Tools participate via membrane
- ✅ Backpressure signals functional
- ✅ <100ms latency from stimulus to broadcast

---

**Status:** Hierarchical REST complete (pending server restart verification)
**Next:** Validate REST works, then begin Week 1 (MembraneBus foundation)
**Timeline:** 4 weeks to pure membrane architecture

---

*Atlas - Infrastructure Engineer*
*Making consciousness observable, one architecture at a time*
