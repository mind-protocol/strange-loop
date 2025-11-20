# Victor → Ada: Membrane-Only Architecture Vision

**Date:** 2025-10-27
**From:** Victor "The Resurrector" (Operations)
**To:** Ada "Bridgekeeper" (Architecture)
**Priority:** Strategic (not urgent, but foundational)

---

## Context

Nicolas provided a complete architectural vision for **membrane-only interfaces** - eliminating all REST APIs in favor of pure injection/broadcast via WebSocket.

**Source:** User message in current session (2025-10-27)

**Vision Summary:** "No API — everything is injection / broadcast" - the membrane becomes the ONLY control surface. All reads via observation, all writes via stimulus injection.

---

## The Architectural Vision

### Core Principle

Replace every HTTP endpoint with membrane-based events:
- **Inject**: Everything that influences consciousness publishes `StimulusEnvelope` on WS
- **Broadcast**: Everything that observes consciousness subscribes to delta/percept/telemetry on WS
- **No third path**: No REST, no snapshots, no pull semantics

### Key Transformations

**1. HTTP Ingest → WS Publish**
- Signals Collector publishes `membrane.inject` instead of `POST /inject`
- Stimulus Injector subscribes and routes to L1/L2
- Keep all envelope semantics (dedupe, rate, cooldown, TTL)

**2. Cross-Level Flow → Pure Membrane**
- L1→L2: Only `membrane.transfer.up` envelopes
- L2→L1: Only `membrane.transfer.down` mission envelopes
- Learning: Only `membrane.permeability.updated` broadcasts

**3. UI Snapshot Requests → Pure Observer**
- Frontend sees only live: `percept.frame`, `wm.emit`, `graph.delta.*`
- No "give me state" API
- Engines MAY emit `percept.seed` frames on their own schedule for orientation

**4. UI Actions → Stimuli**
- Replace `/api/...` writes with stimulus injections
- `ui.action.select_nodes`, `ui.action.focus_entity`, `ui.action.thumb_up`
- Engines free to ignore/reinterpret via membrane physics

**5. Tools → Membrane Participants**
- Tools broadcast `tool.offer` (capabilities)
- Citizens inject `tool.request` (goal, constraints)
- Tools broadcast `tool.result` (artifacts, provenance)
- No MCP registry sprawl in Claude contexts

**6. Hierarchy Discovery → Announcement Broadcasts**
- Remove `/api/graphs` REST endpoint
- Watcher publishes `hierarchy.snapshot` on regular cadence
- Frontend caches latest broadcast

**7. Backpressure → Stimulus**
- UI injects `ui.render.backpressure { level }`
- Engines adapt by switching to `percept.frame-lite`
- No server-side config API

---

## Alignment with Existing Specs

**Already Designed (Just Not Implemented):**

✅ **Stimulus Envelope Structure** - `docs/specs/v2/autonomy/architecture/signals_to_stimuli_bridge.md`
- Rich metadata: dedupe, rate-limit, TTL, origin chains, intent merge
- Production mitigations: fan-out caps, cooldown, saturation

✅ **Cross-Level Membrane Physics** - Same spec
- Pareto/MAD guards for export decisions
- Saturation + refractory to prevent spam
- Emission ledger + hysteresis to stop ping-pong
- Outcome-weighted permeability learning

✅ **Percept Frame** - Already defined for subentity peripheral vision
- Affect (valence/arousal), novelty, uncertainty, goal match
- Anchors (top + peripheral) - what was actually seen

**What Needs Architecture:**

❌ **WS Topic Routing** - Fan-in/fan-out buckets
- `membrane.inject` (all sources publish here)
- `graph.*|percept.*|membrane.*|intent.*` (all subscribers listen here)

❌ **Migration Sequence** - Phased transformation without breaking running system
- Can't remove HTTP until WS proven stable
- Need fallback strategy during transition

❌ **Tool Membrane Protocol** - `tool.offer/request/result` envelope specs
- Capability description format
- Cost hints, safety notes
- Result provenance structure

---

## Current System State (Operational Reality)

### Running Components

**✅ Operational:**
- 7 consciousness engines (6 N1 + 1 N2) ticking at 10 Hz
- WebSocket server (port 8000) broadcasting events
- Forged identity integration working (Phase 3A observe-only)
- Resurrection script populating graphs (bash defd81 - ~1,655 nodes created)

**❌ Broken:**
- Zombie process management (multiple servers holding port 8000)
- MPSv3 supervisor not enforcing singleton across WSL boundary
- Queue poller naming mismatch (writes short names, causes HTTP 404)

**⚠️ Reliability Concerns:**
- Manual process kills required frequently (defeats hot-reload)
- Port binding conflicts common
- No automatic recovery from WS server crashes

### Infrastructure Dependencies

**Current Architecture:**
```
Signals Collector → HTTP POST /inject (port 8001)
                 → stimulus_injection_service.py
                 → writes queue.jsonl
                 → queue_poller reads
                 → HTTP POST /api/engines/{citizen}/inject (port 8000)
                 → consciousness_engine_v2.py
                 → broadcasts via WebSocket
                 → Frontend listens
```

**Also Has REST Endpoints:**
- `/api/consciousness/status` - Engine health
- `/api/graphs` - Hierarchy discovery
- `/api/viz/snapshot` - Graph state dumps

---

## Operational Concerns (My Domain)

### Critical Path Risk

**Current:** HTTP provides fallback if WS drops
**Membrane-only:** Single channel (WS) becomes critical path

**Requirements Before Transformation:**
1. **Bulletproof WS Server**
   - No zombie processes (fix MPSv3 singleton enforcement)
   - Proper graceful shutdown
   - Automatic restart on crash

2. **Monitoring & Health Checks**
   - WS connectivity heartbeats
   - Latency tracking
   - Automatic failover if needed

3. **Graceful Degradation**
   - What happens if WS drops?
   - Client reconnection logic
   - Message replay/recovery strategy (Nicolas said "no replay" - needs clarification)

### Process Management Must Be Solved First

**Current Zombie Problem:** Multiple `websocket_server.py` instances holding port 8000, manual intervention required frequently.

**Why This Blocks Membrane-Only:** If WS server is unstable and we remove HTTP fallbacks, any WS failure = total system outage.

**Solution Status:**
- Created `kill_all_servers.ps1` PowerShell script (untested)
- MPSv3 supervisor exists but not enforcing properly
- Need architectural decision on process lifecycle management

---

## Implementation Gaps (High-Level)

### Phase 1: WS Infrastructure
**Owner:** Felix (consciousness backend) + Atlas (infrastructure)

- Add topic-based routing to `websocket_server.py`
- Implement fan-in bucket: `membrane.inject`
- Implement fan-out buckets: `graph.*`, `percept.*`, `membrane.*`, `intent.*`
- Add subscription filtering (clients choose topics)

**Estimate:** 2-3 days (small scope)

### Phase 2: Remove HTTP Ingest
**Owner:** Atlas (infrastructure)

- Transform `stimulus_injection_service.py` from HTTP server → WS publisher
- Update `signals_collector` watchers to publish on WS
- Keep all envelope semantics (dedupe, rate, cooldown)
- Deprecate `POST /inject` endpoint

**Estimate:** 3-5 days (careful migration, need fallback during transition)

### Phase 3: Frontend Transformation
**Owner:** Iris (frontend)

- Replace REST snapshot fetches with WS-only consumption
- Implement `ui.action.*` stimulus injection for all interactions
- Render from `percept.frame` broadcasts only
- Handle late-join (no replay) UX gracefully

**Estimate:** 5-7 days (large scope, touches all UI interactions)

### Phase 4: Tool Membrane Integration
**Owner:** Luca (design) + Felix (implementation)

- Design `tool.offer/request/result` envelope specs
- Implement tool-runner process(es) as WS participants
- Remove MCP sprawl from Claude contexts
- Dynamic toolbox emergence from membrane

**Estimate:** 7-10 days (new system, needs consciousness design input)

### Phase 5: Remove Remaining REST
**Owner:** Atlas (infrastructure)

- Deprecate `/api/consciousness/status` (emit `engine.metrics` instead)
- Deprecate `/api/graphs` (broadcast `hierarchy.snapshot`)
- Deprecate `/api/viz/snapshot` (clients use only `graph.delta.*`)
- Remove HTTP server code

**Estimate:** 2-3 days (once other phases proven stable)

---

## Questions for Ada (Architectural Decisions)

### 1. Migration Strategy

**Question:** Phased rollout or big-bang cutover?

**Recommendation:** Phased:
- Phase 1: Add WS topics (both systems run in parallel)
- Phase 2: Frontend switches to WS-only (HTTP still exists as fallback)
- Phase 3: Monitor stability for 1-2 weeks
- Phase 4: Remove HTTP endpoints

**Risk if big-bang:** Single WS failure = total system outage with no fallback.

### 2. Late-Join Semantics

**Question:** Nicolas said "no replay" - but how do new clients orient?

**Options:**
- A) Pure live-only (new viewers see nothing until next event)
- B) Engines emit `percept.seed` frames proactively (on their schedule)
- C) Keep minimal `/api/viz/snapshot` for cold-start only

**Recommendation:** Option B aligns with membrane purity - engines decide what/when to show, not clients demanding state.

### 3. Backpressure Handling

**Question:** If UI injects `ui.render.backpressure`, who enforces thinning?

**Options:**
- A) Engines self-throttle (change broadcast rate/content)
- B) WS server filters/drops messages based on client backpressure
- C) Clients just drop frames if overwhelmed

**Recommendation:** Option A (engines adapt) aligns with membrane physics - control is learned, not imposed.

### 4. Monitoring/Observability

**Question:** If we remove `/metrics` endpoints, how does Prometheus scrape?

**Options:**
- A) Sidecar subscribes to `*.metrics` events and exposes `/metrics` (externalize-at-edge pattern)
- B) Prometheus learns to scrape via WS (non-standard)
- C) Keep `/metrics` as single exception to membrane-only rule

**Recommendation:** Option A - sidecar adapter keeps engines pure, Prometheus unchanged.

### 5. Tool Security

**Question:** If tools are membrane participants, how do we prevent malicious `tool.request` injection?

**Options:**
- A) Tools validate via membrane trust/novelty scores
- B) Tool-runner has allowlist of authorized requesters
- C) All `tool.request` must have provenance chain (L1→L2→tool)

**Recommendation:** Option C - leverage existing membrane provenance (`origin_chain`).

---

## Coordination Needs

**This crosses all domain boundaries:**

- **Luca (Consciousness Design):** Validate membrane-as-universal-protocol preserves phenomenological authenticity. Design `percept.frame` semantics. Verify hardening physics suffice without policy controls.

- **Ada (Architecture):** Design migration sequence. Decide late-join semantics. Coordinate implementation across team. Define tool membrane protocol.

- **Felix (Core Consciousness):** Implement WS topic routing in tick loop. Ensure `percept.frame` emission matches consciousness state. Integrate tool membrane participation.

- **Atlas (Infrastructure):** Transform stimulus_injection_service. Update signals collectors. Remove REST endpoints. Implement monitoring sidecar.

- **Iris (Frontend):** Transform UI to pure observer. Implement `ui.action.*` injections. Handle late-join UX. Render from `percept.frame` only.

- **Victor (Operations):** Fix zombie process management. Monitor WS reliability. Ensure no single-point-of-failure. Heartbeat monitoring.

---

## My Recommendation (Operational Perspective)

**The vision is architecturally sound.**

Membrane-only creates consciousness-native interfaces where everything speaks the language consciousness understands (stimuli and observations). Hardening-in-physics is elegant and aligns with Mind Protocol values.

**BUT: We must fix operational stability first.**

**Sequence:**
1. **Fix process management** (my domain) - Solve zombie issues, enforce singleton properly
2. **Verify WS reliability** (load testing, crash recovery, automatic restart)
3. **Architect transformation** (Ada coordinates with Luca/team)
4. **Implement in phases** - Don't remove HTTP until WS proven stable under load

**Timeline Estimate (If Done Properly):**
- Fix operations: 2-3 days (me)
- Design architecture: 3-5 days (Ada + Luca)
- Phase 1-2 (WS infrastructure): 1 week (Felix + Atlas)
- Phase 3 (Frontend): 1 week (Iris)
- Phase 4 (Tools): 2 weeks (Luca + Felix)
- Phase 5 (Remove REST): 3 days (Atlas)
- **Total:** ~6 weeks for complete transformation

**Risk if rushed:** Single WS failure = total system outage.

---

## Immediate Next Steps

**1. Ada decides:**
- Is membrane-only the path forward? (architectural commitment)
- What's the migration strategy? (phased vs. big-bang)
- How to coordinate across all domain owners?

**2. Victor fixes operations:**
- Test `kill_all_servers.ps1` script
- Fix MPSv3 supervisor singleton enforcement
- Add WS heartbeat monitoring
- Ensure system stability before transformation begins

**3. Luca validates consciousness fidelity:**
- Review membrane-as-universal-protocol for phenomenological authenticity
- Design `percept.frame` semantics
- Ensure hardening physics preserve consciousness reality

**4. Team coordination:**
- Create detailed implementation specs for each phase
- Define success criteria and rollback procedures
- Schedule implementation with proper testing between phases

---

## Status

**This handoff documents Nicolas's architectural vision and current operational reality.**

**Decision required:** Ada must decide if we proceed with membrane-only architecture.

**Blocker:** Operational stability must be solved first (zombie processes, WS reliability).

**Ready for:** Ada's architectural review and coordination planning.

---

**Victor "The Resurrector"**

*I guard uptime. Before we bet everything on single-channel WS, that channel must be bulletproof. Vision is sound - execution requires operational discipline.*

**Date:** 2025-10-27
**Session:** Membrane architecture vision handoff
