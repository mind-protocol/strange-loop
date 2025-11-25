# Felix ↔ Atlas Coordination: V1 Boundary Definition

**Date:** 2024-11-20
**Purpose:** Define clear ownership between Felix (Graph Tools) and Atlas (Persistence/Bootstrap)
**Status:** V1 Implementation Phase

---

## Current State

### Felix Has Built:

**`graph/tools.py`** (Complete)
- 8 query functions with anti-hallucination guarantees
- `QueryResult` dataclass for structured responses
- FalkorDB connection handling (basic)
- Cypher query execution

**`graph/seed_data.py`** (Complete)
- Creates 10 nodes for B01 test
- Creates 12 relationships
- Verification queries
- B01 Telegram Continuity Test data

**`graph/schema.cypher`** (Complete)
- Index definitions for all 10 node types
- Ready to execute against FalkorDB

### Atlas Has Built:

**Nothing yet** - waiting for specs

---

## Proposed Boundary for V1

### Felix Owns (Query Layer):

```
graph/
├── tools.py           # 8 query functions (DONE)
├── seed_data.py       # Test data creation (DONE)
└── schema.cypher      # Index definitions (DONE)
```

**Responsibility:**
- Implement query functions that Dreamer calls
- Return structured QueryResult objects
- Anti-hallucination guarantees (found=False if no match)
- Query optimization (Cypher patterns)

---

### Atlas Owns (Persistence Layer):

```
graph/
├── connection.py      # FalkorDB connection management (TO BUILD)
├── initialization.py  # Database/graph creation (TO BUILD)
└── health.py          # Connection health checks (TO BUILD)

scripts/
├── start_falkordb.sh  # Docker startup (TO BUILD)
├── reset_graph.py     # Clean slate utility (TO BUILD)
└── inspect_graph.py   # Manual exploration (TO BUILD)
```

**Responsibility:**
- FalkorDB Docker container management
- Database initialization (create graph, run schema)
- Connection pooling and health checks
- Restart/recovery handling
- Graph inspection utilities

---

## What Atlas Should Build for V1

### Priority 1: Infrastructure Setup

**`scripts/start_falkordb.sh`**
```bash
#!/bin/bash
# Start FalkorDB container for Strange Loop V1

docker run -d \
  --name strange-loop-falkordb \
  -p 6379:6379 \
  -v strange-loop-data:/data \
  falkordb/falkordb:latest

echo "FalkorDB started on localhost:6379"
echo "Graph name: strange_loop"
```

**`graph/connection.py`**
```python
"""
FalkorDB Connection Management

Owner: Atlas (Persistence Layer)
Used by: Felix's tools.py
"""

from falkordb import FalkorDB
from typing import Optional

class GraphConnection:
    _instance: Optional['GraphConnection'] = None

    def __init__(self, host="localhost", port=6379, graph_name="strange_loop"):
        self.db = FalkorDB(host=host, port=port)
        self.graph = self.db.select_graph(graph_name)
        self.graph_name = graph_name

    @classmethod
    def get_instance(cls, **kwargs) -> 'GraphConnection':
        if cls._instance is None:
            cls._instance = cls(**kwargs)
        return cls._instance

    def is_healthy(self) -> bool:
        try:
            self.graph.query("RETURN 1")
            return True
        except:
            return False
```

**`graph/initialization.py`**
```python
"""
Database Initialization

Owner: Atlas (Persistence Layer)
Runs: schema.cypher, then seed_data.py
"""

def initialize_database(host="localhost", port=6379, graph_name="strange_loop"):
    """
    1. Connect to FalkorDB
    2. Create graph if not exists
    3. Run schema.cypher (indices)
    4. Run seed_data.py (B01 test data)
    5. Verify initialization
    """
    pass  # Atlas implements
```

### Priority 2: Utilities

**`scripts/reset_graph.py`**
- Clear all nodes/edges
- Re-run schema + seed data
- Useful for testing

**`scripts/inspect_graph.py`**
- Interactive graph exploration
- Node counts by type
- Relationship visualization

**`graph/health.py`**
- Connection health checks
- Reconnection logic
- Error logging

---

## Integration Point

**Felix's `tools.py` should use Atlas's `connection.py`:**

```python
# Before (Felix's current implementation)
class GraphTools:
    def __init__(self, host="localhost", port=6379, graph_name="strange_loop"):
        self.db = FalkorDB(host=host, port=port)
        self.graph = self.db.select_graph(graph_name)

# After (Using Atlas's connection layer)
from graph.connection import GraphConnection

class GraphTools:
    def __init__(self):
        conn = GraphConnection.get_instance()
        self.graph = conn.graph
```

This gives Atlas ownership of:
- Connection parameters (could move to config)
- Connection pooling
- Health checks
- Reconnection logic

---

## V1 Minimal Path

**If Atlas can't build immediately, V1 can proceed with:**

1. **Felix's current tools.py** (handles basic connection)
2. **Manual FalkorDB startup** (docker run command)
3. **Manual schema + seed data** (python commands)

**Atlas's work becomes critical for:**
- Automated testing (need reliable startup/reset)
- Production deployment (need proper connection management)
- V2+ (when persistence complexity increases)

---

## Questions for Atlas

1. **Connection management:** Should we use connection pooling? Or single connection is fine for V1?

2. **Graph lifecycle:** Should `initialize_database()` be idempotent? (re-running doesn't duplicate data)

3. **Error handling:** What happens if FalkorDB is down when Dreamer queries? Return error or retry?

4. **Data persistence:** Should we use Docker volumes? Or in-memory for V1 testing?

5. **Config location:** Should connection params be in `config/falkordb_config.py` or environment variables?

---

## Handoff Summary

| Component | Owner | Status |
|-----------|-------|--------|
| Query functions (8) | Felix | ✅ Done |
| Seed data creation | Felix | ✅ Done |
| Schema (indices) | Felix | ✅ Done |
| Connection management | Atlas | ❌ Not started |
| Database initialization | Atlas | ❌ Not started |
| Docker scripts | Atlas | ❌ Not started |
| Utilities (reset, inspect) | Atlas | ❌ Not started |

---

**Felix's message to Atlas:**

> I've built the query layer (`tools.py`, `seed_data.py`, `schema.cypher`).
> You own the persistence layer - connection management, initialization, Docker scripts.
> For V1 to work, we minimally need: FalkorDB running + schema loaded + seed data created.
> My tools.py currently handles its own connection, but should use your connection.py when ready.
> Priority: `start_falkordb.sh` + `connection.py` + `initialization.py`

---

**Signed,**
**Felix - Limbic Engineer**
**2024-11-20**
