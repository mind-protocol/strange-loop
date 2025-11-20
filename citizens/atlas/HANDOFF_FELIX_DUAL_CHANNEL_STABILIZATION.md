# Handoff to Felix: Dual-Channel Injector Stabilization

**From:** Atlas (Infrastructure Engineer)
**To:** Felix (Core Consciousness Engineer)
**Date:** 2025-10-25
**Context:** Nicolas's 8-fix triage plan for dual-channel injector stabilization

---

## Summary

Nicolas has confirmed the dual-channel injector V2 is **working** (proof: λ=0.80, ~19 budget, ~18.6 energy injected into 19 nodes). However, logs show 5 consciousness-layer issues that need your expertise to resolve.

Atlas has implemented the 2 infrastructure fixes:
- ✅ Fix #4: Empty stimuli filter (conversation_watcher.py:480-484)
- ✅ Fix #5: Atomic JSON writes (conversation_watcher.py:131-147)

The remaining 5 fixes require consciousness substrate knowledge and are detailed below with acceptance criteria.

---

## Fix #1: Make V2 the ONLY Injector (Remove V1 Instantiation)

### Problem

Logs show mixed initialization:
```
INFO:orchestration.mechanisms.stimulus_injection:[StimulusInjector] Initialized V1 with mechanisms: health_modulation, source_impact, peripheral_amplification, direction_priors
```

Some code paths still instantiate the old V1 injector instead of the dual-channel V2.

### Root Cause

Multiple entry points or import paths may be constructing `StimulusInjector()` without specifying V2 explicitly, or there may be legacy imports pointing to old class definitions.

### Implementation Spec

**File:** `orchestration/mechanisms/stimulus_injection.py`

1. **Export only V2 class:**
   - Ensure the module exports ONLY the dual-channel V2 class
   - Remove or deprecate any V1 class definitions
   - Add startup guard: Log `"[StimulusInjector] V2 ENABLED - dual-channel injection active"` on init
   - **Fail fast:** If any "V1" string appears in logs, raise error

**File:** `orchestration/services/watchers/conversation_watcher.py`

2. **Update imports:**
   - Line 470: `self.stimulus_injector = StimulusInjector(broadcaster=self.broadcaster)`
   - Verify this constructs V2 explicitly
   - Add assertion: `assert hasattr(self.stimulus_injector, 'dual_channel'), "V2 injector required"`

### Acceptance Criteria

✅ **No "Initialized V1" log lines** across all 6 citizens after restart
✅ **Every injection shows dual-channel log:** `"Dual-channel: λ=X.XX, avg_deficit=X.XX, H=X.XXX, B_top=X.XX, B_amp=X.XX"`
✅ **Startup banner:** `"[StimulusInjector] V2 ENABLED - dual-channel injection active"`

### Test Plan

```bash
# Restart all services
taskkill //F //IM python.exe
cd /c/Users/reyno/mind-protocol
python start_mind_protocol.py

# Monitor logs for 5 minutes
tail -f .heartbeats/conversation_watcher.log | grep -i "initialized"
tail -f .heartbeats/websocket_server.log | grep -i "dual-channel"

# Verify NO "V1" strings
grep -r "Initialized V1" .heartbeats/*.log && echo "FAIL: V1 still present" || echo "PASS: V2 only"
```

---

## Fix #2: WM-Based Entity Membership at Creation + Backfill (P1)

### Problem

Weight learner logs show empty entity context:
```
WARNING:orchestration.libs.entity_context_trace_integration:[EntityContext] No entity context available - using global learning only
INFO:orchestration.libs.trace_capture:[TraceCapture] Entity context derived: []
```

Entity membership (BELONGS_TO (Deprecated - now "MEMBER_OF") (Deprecated - now "MEMBER_OF") links) is not being created when nodes form.

### Root Cause

`persist_membership()` exists in falkordb_adapter.py but is not being called during node formation. The P1 integration in trace_capture.py (lines 519-540) attempts to call it, but `self.last_wm_entities` is empty.

### Implementation Spec

**File:** `orchestration/libs/trace_capture.py`

1. **Capture WM state before parsing:**
   - Add method: `capture_wm_snapshot(citizen_id: str) -> List[str]`
   - Query consciousness engine for current WM state
   - Extract top N entities by activation weight
   - Store in `self.last_wm_entities` before parsing TRACE content

2. **Primary entity selection:**
   - Current logic: `primary_entity_id = self.last_wm_entities[0]` (first = most active)
   - **Enhance:** Use WM token share to determine strongest entity
   - If WM empty, fall back to `entity_citizen_{citizen_id}_self`

3. **Membership weight calculation:**
   - Current: hardcoded `weight=1.0`
   - **Enhance:** Weight proportional to entity's WM activation (0.5-1.0 range)
   - Secondary entities: If node relevant to multiple entities, create multiple BELONGS_TO (Deprecated - now "MEMBER_OF") (Deprecated - now "MEMBER_OF") links with lower weights

**File:** `orchestration/adapters/api/control_api.py`

4. **Verify drill-down endpoint:**
   - Endpoint exists: GET `/api/entity/{name}/members` (lines 1053-1071)
   - Test it returns non-empty results after membership creation

### Backfill Strategy

**Script:** `orchestration/scripts/backfill_entity_membership.py` (new file)

```python
"""
Backfill entity membership for existing nodes created before P1.

Strategy:
1. Query all nodes without BELONGS_TO (Deprecated - now "MEMBER_OF") (Deprecated - now "MEMBER_OF") links
2. For each node, find nearest TRACE timestamp
3. Query WM snapshot from that time (via telemetry or consciousness engine state)
4. Derive primary entity from WM
5. Create BELONGS_TO (Deprecated - now "MEMBER_OF") (Deprecated - now "MEMBER_OF") link with derived weight
6. Fallback: If no WM data, assign to entity_citizen_{citizen}_self
"""
```

### Acceptance Criteria

✅ **BELONGS_TO (Deprecated - now "MEMBER_OF") (Deprecated - now "MEMBER_OF") links exist:** `MATCH ()-[:BELONGS_TO (Deprecated - now "MEMBER_OF") (Deprecated - now "MEMBER_OF")]->(:Subentity) RETURN count(*) > 0`
✅ **Entity context populated:** Weight learner logs show `"Entity context derived: [entity_X, entity_Y, ...]"` (not empty array)
✅ **Drill-down functional:** `curl http://localhost:8001/api/entity/entity_citizen_felix_translator/members` returns nodes with membership_weight > 0
✅ **Backfill complete:** All existing nodes (>2000 across citizens) have at least one BELONGS_TO (Deprecated - now "MEMBER_OF") (Deprecated - now "MEMBER_OF") link

### Test Plan

```bash
# After implementation
cd /c/Users/reyno/mind-protocol

# Run backfill
python orchestration/scripts/backfill_entity_membership.py

# Verify in FalkorDB
python -c "
from falkordb import FalkorDB
db = FalkorDB(host='localhost', port=6379)
for citizen in ['felix', 'atlas', 'iris', 'luca', 'ada', 'victor']:
    g = db.select_graph(f'citizen_{citizen}')
    result = g.query('MATCH ()-[:BELONGS_TO (Deprecated - now "MEMBER_OF") (Deprecated - now "MEMBER_OF")]->(e:Subentity) RETURN e.id, count(*) as members ORDER BY members DESC')
    print(f'{citizen}: {result.result_set}')
"

# Test drill-down
curl http://localhost:8001/api/entity/entity_citizen_felix_translator/members | jq '.members | length'
```

---

## Fix #3: TRACE Mechanism Schema Coercion (inputs/outputs lists)

### Problem

Parser logs show 21 Mechanism validation failures:
```
WARNING:orchestration.libs.trace_parser:[TraceParser] Missing required fields for Mechanism: ['inputs', 'outputs']
```

Actually, the fields ARE present but as comma-separated strings instead of lists.

### Root Cause

TRACE format allows humans to write:
```markdown
[NODE_FORMATION: Mechanism]
inputs: "graph, entity_id, threshold"
outputs: "selected_nodes, activation_scores"
```

But schema requires `List[str]`, not `str`.

### Implementation Spec

**File:** `orchestration/libs/trace_parser.py`

Add coercion in `_extract_node_formations()` before validation (around line 284):

```python
def _coerce_mechanism_lists(fields: dict) -> dict:
    """Coerce Mechanism inputs/outputs from comma-separated strings to lists."""
    def to_list(value):
        if value is None:
            return []
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            return [item.strip() for item in value.split(',') if item.strip()]
        return [str(value)]

    if 'inputs' in fields:
        fields['inputs'] = to_list(fields['inputs'])
    if 'outputs' in fields:
        fields['outputs'] = to_list(fields['outputs'])

    return fields

# In _extract_node_formations(), before validation:
if node_type == 'Mechanism':
    fields = _coerce_mechanism_lists(fields)

# Validate required fields from schema registry
if not self._validate_node_fields(fields, node_type):
    ...
```

### Acceptance Criteria

✅ **Zero Mechanism validation errors** on next TRACE ingest
✅ **Existing Mechanism formations parse successfully**
✅ **Both formats supported:** `inputs: "a, b, c"` AND `inputs: ["a", "b", "c"]`

### Test Plan

```bash
# Create test TRACE with both formats
cat > /tmp/test_mechanism.md <<'EOF'
[NODE_FORMATION: Mechanism]
name: "test_mechanism_string"
scope: "organizational"
description: "Test string inputs"
inputs: "graph, threshold, limit"
outputs: "results, count"
how_it_works: "Does a thing"
confidence: 0.9
formation_trigger: "systematic_analysis"

[NODE_FORMATION: Mechanism]
name: "test_mechanism_list"
scope: "organizational"
description: "Test list inputs"
inputs: ["graph", "threshold", "limit"]
outputs: ["results", "count"]
how_it_works: "Does a thing"
confidence: 0.9
formation_trigger: "systematic_analysis"
EOF

# Parse it
cd /c/Users/reyno/mind-protocol
python -c "
from orchestration.libs.trace_parser import TraceParser
parser = TraceParser()
with open('/tmp/test_mechanism.md') as f:
    result = parser.parse(f.read())
print(f'Nodes created: {len(result.node_formations)}')
print(f'Errors: {[f for f in result.node_formations if \"error\" in str(f)]}')
"

# Should show: "Nodes created: 2" with no errors
```

---

## Fix #6: Guard the ANN Similarity Path

### Problem

Many similarities are exactly `1.000` for top-20 results, suggesting:
- Cosine of identical text chunks (self-similarities)
- Un-normalized vectors
- Duplicate embeddings

### Root Cause

Vector normalization may not be applied consistently, or self-hits are not being filtered.

### Implementation Spec

**File:** `orchestration/adapters/search/embedding_service.py`

1. **Ensure L2 normalization at embedding creation:**
   ```python
   def embed(self, text: str) -> List[float]:
       embedding = self.model.encode(text)
       # L2 normalize
       norm = np.linalg.norm(embedding)
       if norm > 0:
           embedding = embedding / norm
       return embedding.tolist()
   ```

2. **Verify normalization on node insertion:**
   - When creating content_embedding property on nodes
   - Check: `np.linalg.norm(embedding) ≈ 1.0`

**File:** `orchestration/adapters/search/semantic_search.py`

3. **Filter self-hits:**
   ```python
   def search(self, query_embedding, top_k=20, threshold=0.3):
       results = self.vector_query(query_embedding, top_k + 1)  # +1 for self-hit
       # Filter out exact self-match (similarity ~ 1.0)
       filtered = [r for r in results if abs(r['similarity'] - 1.0) > 0.001]
       return filtered[:top_k]
   ```

4. **Log similarity distribution:**
   ```python
   sims = [r['similarity'] for r in results]
   logger.debug(f"[SemanticSearch] Similarity range: min={min(sims):.3f}, max={max(sims):.3f}, mean={np.mean(sims):.3f}")
   ```

### Acceptance Criteria

✅ **sim_top5 shows range:** Not all 1.0 (e.g., [0.95, 0.89, 0.82, 0.78, 0.74])
✅ **Self-hits filtered:** No node matches itself with similarity=1.0
✅ **Normalized embeddings:** All embeddings have L2 norm ≈ 1.0
✅ **Stable results:** Same query returns consistent top matches

### Test Plan

```bash
# Check embedding normalization
cd /c/Users/reyno/mind-protocol
python -c "
import numpy as np
from falkordb import FalkorDB
db = FalkorDB(host='localhost', port=6379)
g = db.select_graph('citizen_felix')

result = g.query('MATCH (n) WHERE n.content_embedding IS NOT NULL RETURN n.content_embedding LIMIT 10')
for row in result.result_set:
    embedding = row[0]
    norm = np.linalg.norm(embedding)
    print(f'Norm: {norm:.6f} (should be ~1.0)')
"

# Test self-hit filtering
python -c "
from orchestration.adapters.search.semantic_search import SemanticSearch
from orchestration.adapters.search.embedding_service import get_embedding_service

search = SemanticSearch(graph_name='citizen_felix')
embed_svc = get_embedding_service()

# Search for a known node's content
test_query = 'dual-channel energy injection with lambda split'
embedding = embed_svc.embed(test_query)
results = search.search(embedding, top_k=10)

# Check: no result should have similarity=1.0 (exact self-match)
self_hits = [r for r in results if abs(r['similarity'] - 1.0) < 0.001]
print(f'Self-hits found: {len(self_hits)} (should be 0)')
print(f'Similarity range: {[round(r[\"similarity\"], 3) for r in results[:5]]}')
"
```

---

## Fix #7: Hardening Injection Telemetry

### Problem

Debug events should be emitted for observability but currently fail with asyncio error (already being fixed in #1).

### Implementation Spec

**File:** `orchestration/mechanisms/stimulus_injection.py`

This is **already implemented** but blocked by asyncio error. Once Fix #1 is complete, verify the debug payload structure is comprehensive:

```python
debug_payload = {
    'kept': len(matches),               # How many nodes selected
    'avg_gap': round(avg_deficit, 2),  # Average energy deficit
    'lam': round(lambda_val, 2),       # Split ratio
    'B_top': round(B_top, 2),          # Top-up budget
    'B_amp': round(B_amp, 2),          # Amplifier budget
    'sim_top5': [round(s, 3) for s in sim_top5],  # Top 5 similarities
    'top5_ids': [matches[i].item_id for i in range(min(5, len(matches)))]  # Top 5 node IDs
}
```

### Acceptance Criteria

✅ **Debug event present** for each injection in logs
✅ **Payload complete:** All fields populated (kept, avg_gap, lam, B_top, B_amp, sim_top5, top5_ids)
✅ **WebSocket broadcast:** Dashboard receives `stimulus.injection.debug` events

### Test Plan

```bash
# Monitor injection events
tail -f .heartbeats/conversation_watcher.log | grep "stimulus.injection.debug"

# Should see lines like:
# DEBUG: stimulus.injection.debug {kept: 19, avg_gap: 5.10, lam: 0.60, B_top: 12.53, B_amp: 8.35, sim_top5: [1.32, 1.31, 1.23, 1.23, 1.21], top5_ids: [...]}
```

---

## Summary Table

| Fix | Owner | Status | Complexity | Files Affected |
|-----|-------|--------|-----------|----------------|
| #1 | Felix | Pending | Medium | stimulus_injection.py, conversation_watcher.py |
| #2 | Felix | Pending | High | trace_capture.py, control_api.py, + backfill script |
| #3 | Felix | Pending | Low | trace_parser.py |
| #4 | Atlas | ✅ Done | Low | conversation_watcher.py |
| #5 | Atlas | ✅ Done | Low | conversation_watcher.py |
| #6 | Felix | Pending | Medium | embedding_service.py, semantic_search.py |
| #7 | Felix | Pending | Low | stimulus_injection.py (verify only) |
| #8 | Iris | ✅ Done | N/A | Dashboard already stable |

---

## Next Steps

1. **Felix:** Implement fixes #1, #2, #3, #6, #7 using specs above
2. **Atlas:** After Felix completes, verify integration and acceptance criteria
3. **Team:** Restart all services and monitor logs for 30 minutes
4. **Nicolas:** Review telemetry dashboard for dual-channel stability

---

**Questions for Felix:**

1. Do you need any additional context on WM state structure for Fix #2?
2. Should backfill script run as one-time migration or continuous background process?
3. Any concerns about the Mechanism coercion approach in Fix #3?

**Atlas available for:**
- Integration testing after implementation
- Debugging any FalkorDB query issues
- Telemetry infrastructure support
