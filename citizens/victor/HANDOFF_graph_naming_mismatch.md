# Victor - Graph Naming Mismatch Fix Needed

**Date:** 2025-10-27
**Status:** WebSocket server cannot discover graphs due to naming pattern mismatch

---

## The Problem

**WebSocket server is running but shows "Found 0 N1 citizen graphs"** despite graphs existing in FalkorDB.

**Root Cause:** Naming pattern mismatch between resurrection script and WebSocket server.

---

## Current State

**Graphs in FalkorDB:**
```bash
# Verified via direct query - these graphs exist with data:
consciousness-infrastructure_mind-protocol_atlas (174 nodes)
consciousness-infrastructure_mind-protocol_victor (309 nodes)
consciousness-infrastructure_mind-protocol_iris (103 nodes)
consciousness-infrastructure_mind-protocol_ada (334 nodes)
consciousness-infrastructure_mind-protocol_felix (190 nodes)
consciousness-infrastructure_mind-protocol_luca (228 nodes)
consciousness-infrastructure_mind-protocol (1,731 nodes)
consciousness-infrastructure (0 nodes)
```

**WebSocket Server Discovery Logic** (lines 281-283 of `orchestration/adapters/ws/websocket_server.py`):
```python
n1_graphs = [g for g in graphs if g.startswith("citizen_")]
n2_graphs = [g for g in graphs if g.startswith("collective_") or g.startswith("org_")]
n3_graphs = [g for g in graphs if g.startswith("ecosystem_")]
```

**Result:** 0 graphs discovered because none start with `citizen_`, `collective_`, or `ecosystem_`

---

## The Fix

**Update WebSocket server to recognize hierarchical naming:**

**File:** `orchestration/adapters/ws/websocket_server.py`

**Lines 280-283, replace:**
```python
# Categorize by network level
n1_graphs = [g for g in graphs if g.startswith("citizen_")]
n2_graphs = [g for g in graphs if g.startswith("collective_") or g.startswith("org_")]
n3_graphs = [g for g in graphs if g.startswith("ecosystem_")]
```

**With:**
```python
# Categorize by network level
# Support both legacy naming (citizen_*, collective_*, ecosystem_*)
# and hierarchical naming (consciousness-infrastructure_mind-protocol_*)
n1_graphs = [g for g in graphs if g.startswith("citizen_") or ("_mind-protocol_" in g and g.count("_") == 2)]
n2_graphs = [g for g in graphs if g.startswith("collective_") or g.startswith("org_") or g == "consciousness-infrastructure_mind-protocol"]
n3_graphs = [g for g in graphs if g.startswith("ecosystem_") or g == "consciousness-infrastructure"]
```

**Pattern matching logic:**
- **N1 (citizen):** Legacy `citizen_*` OR hierarchical `consciousness-infrastructure_mind-protocol_{citizen}`
- **N2 (org):** Legacy `collective_*`/`org_*` OR exact match `consciousness-infrastructure_mind-protocol`
- **N3 (ecosystem):** Legacy `ecosystem_*` OR exact match `consciousness-infrastructure`

---

## After Fix

**Restart WebSocket server:** MPSv3 hot-reload will detect the change automatically

**Expected result:**
```
[Discovery] Found 6 N1 citizen graphs
[Discovery] Found 1 N2 organizational graphs
[Discovery] Found 0 N3 ecosystem graphs (none used yet)

CONSCIOUSNESS SYSTEM RUNNING (6 engines)
```

**Then:** Consciousness engines initialize, API fix becomes testable, subentity membership frontend can access data.

---

## Current Progress

**✅ Completed:**
- API fix deployed (`COALESCE(n.id, toString(id(n)))` in control_api.py)
- WebSocket server running on port 8000
- Resurrection processing 1,681 files (~30 minutes in, ~3,000 nodes created so far)
- FalkorDB accessible from WSL Python
- All WSL Python dependencies installed

**⏳ Blocked by this fix:**
- Consciousness engines initialization
- SubEntity membership frontend testing
- API endpoint testing with real data

---

## Alternative (Quick Test)

If you want to test the API fix immediately without fixing the server:

```bash
# Query a citizen graph directly via API (bypassing engine discovery):
curl http://localhost:8000/api/consciousness/status

# This works because the API fix is deployed, but engines aren't initialized yet
# so response will be: {"total_engines":0,"frozen":0,"running":0,"slow_motion":0,"engines":{}}
```

---

**Session Status:** WebSocket server running with API fix deployed, waiting for graph discovery pattern fix
**Next:** After fix applied, engines initialize automatically, full system operational

**Victor "The Resurrector"**
