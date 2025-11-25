# Graph Schema Specification

**Type:** SCHEMA
**Version:** 1.0
**Status:** Implementation Specification
**For:** FalkorDB graph database structure

---

## Purpose

This document defines the complete graph schema for Strange Loop V1. It specifies:
- Node types and their properties
- Edge (relationship) types and semantics
- Indices for query optimization
- Seed data requirements for B01 test

**Critical principle:** The schema must support all 8 query functions defined in M01 (Graph Tools).

---

## Node Types

### 1. Citizen

**Purpose:** Represents the AI consciousness (e.g., Felix)

**Properties:**
```cypher
(Citizen {
  id: STRING,              # Unique identifier (e.g., "felix")
  name: STRING,            # Display name (e.g., "Felix")
  role: STRING,            # Role description (e.g., "Runtime Engineer")
  focus_area: STRING,      # Primary focus (e.g., "Validation Testing")
  created_at: DATETIME,    # When citizen was created
  active: BOOLEAN          # Is this citizen active?
})
```

**Example:**
```cypher
CREATE (c:Citizen {
  id: "felix",
  name: "Felix",
  role: "Runtime Engineer",
  focus_area: "Validation Testing",
  created_at: datetime("2024-01-01T00:00:00Z"),
  active: true
})
```

**Indices:**
```cypher
CREATE INDEX FOR (c:Citizen) ON (c.id)
```

---

### 2. Person

**Purpose:** Represents human partners

**Properties:**
```cypher
(Person {
  id: STRING,              # Unique identifier (e.g., "nicolas")
  name: STRING,            # Display name (e.g., "Nicolas")
  role: STRING,            # Role in organization (e.g., "Co-Founder")
  created_at: DATETIME     # When person was added
})
```

**Example:**
```cypher
CREATE (p:Person {
  id: "nicolas",
  name: "Nicolas",
  role: "Co-Founder",
  created_at: datetime("2024-01-01T00:00:00Z")
})
```

**Indices:**
```cypher
CREATE INDEX FOR (p:Person) ON (p.id)
```

---

### 3. Partnership

**Purpose:** Relationship context with a human partner (queried by `query_partnerships`)

**Properties:**
```cypher
(Partnership {
  id: STRING,                    # Unique identifier (e.g., "partnership_felix_nicolas")
  citizen: STRING,               # Citizen ID (e.g., "felix")
  partner_name: STRING,          # Partner display name (e.g., "Nicolas")
  partner_role: STRING,          # Partner role (e.g., "Co-Founder")
  trust_level: FLOAT,            # 0.0-1.0 (e.g., 0.9)
  communication_style: STRING,   # How they communicate (e.g., "Direct, technical, values testing")
  relationship_type: STRING,     # Type of relationship (e.g., "Professional Partnership")
  shared_history: LIST<STRING>,  # Key shared experiences (e.g., ["€35K lesson", "8 months Venice"])
  partnership_duration: STRING,  # How long (e.g., "8 months")
  created_at: DATETIME,
  updated_at: DATETIME
})
```

**Example:**
```cypher
CREATE (p:Partnership {
  id: "partnership_felix_nicolas",
  citizen: "felix",
  partner_name: "Nicolas",
  partner_role: "Co-Founder",
  trust_level: 0.9,
  communication_style: "Direct, technical, values testing",
  relationship_type: "Professional Partnership",
  shared_history: ["€35K hallucination lesson", "8 months Venice collaboration"],
  partnership_duration: "8 months",
  created_at: datetime("2024-03-01T00:00:00Z"),
  updated_at: datetime("2024-11-20T00:00:00Z")
})
```

**Indices:**
```cypher
CREATE INDEX FOR (p:Partnership) ON (p.citizen)
CREATE INDEX FOR (p:Partnership) ON (p.partner_name)
```

---

### 4. Conversation_Memory

**Purpose:** Past conversations (queried by `query_conversations`)

**Properties:**
```cypher
(Conversation_Memory {
  id: STRING,                   # Unique identifier (e.g., "conv_race_condition_nov_2024")
  citizen: STRING,              # Citizen ID
  partner: STRING,              # Partner ID (e.g., "nicolas")
  topic: STRING,                # Conversation topic (e.g., "stimulus_integrator race condition")
  message_count: INT,           # Number of messages (e.g., 10)
  key_points: LIST<STRING>,     # Important takeaways (e.g., ["Third recurrence", "Systematic approach"])
  emotional_tone: STRING,       # Emotion during conversation (e.g., "Frustrated but determined")
  outcome: STRING,              # Result/status (e.g., "In progress", "Resolved")
  timestamp: DATETIME,          # When conversation happened
  created_at: DATETIME
})
```

**Example:**
```cypher
CREATE (c:Conversation_Memory {
  id: "conv_race_condition_nov_2024",
  citizen: "felix",
  partner: "nicolas",
  topic: "stimulus_integrator race condition",
  message_count: 10,
  key_points: ["Third recurrence of bug", "Previous fixes were patches", "Agreed on systematic approach"],
  emotional_tone: "Frustrated but determined",
  outcome: "In progress - investigating lock granularity",
  timestamp: datetime("2024-11-15T14:30:00Z"),
  created_at: datetime("2024-11-15T14:30:00Z")
})
```

**Indices:**
```cypher
CREATE INDEX FOR (c:Conversation_Memory) ON (c.citizen)
CREATE INDEX FOR (c:Conversation_Memory) ON (c.partner)
CREATE INDEX FOR (c:Conversation_Memory) ON (c.topic)
CREATE INDEX FOR (c:Conversation_Memory) ON (c.timestamp)
```

---

### 5. Technical_Context

**Purpose:** Technical knowledge about code/systems (queried by `query_technical_context`)

**Properties:**
```cypher
(Technical_Context {
  id: STRING,                    # Unique identifier (e.g., "tech_stimulus_integrator_race")
  citizen: STRING,               # Citizen ID
  component: STRING,             # Component name (e.g., "stimulus_integrator.py")
  issue_type: STRING,            # Type of issue (e.g., "race condition", "feature", "refactor")
  description: STRING,           # What's happening (e.g., "Timing bug in multi-threaded energy injection")
  status: STRING,                # Current status (e.g., "investigating", "resolved", "blocked")
  recurrence_count: INT,         # How many times has this occurred? (e.g., 3)
  related_code: LIST<STRING>,    # Related files (e.g., ["consciousness_engine_v2.py", "traversal.py"])
  created_at: DATETIME,
  updated_at: DATETIME
})
```

**Example:**
```cypher
CREATE (t:Technical_Context {
  id: "tech_stimulus_integrator_race",
  citizen: "felix",
  component: "stimulus_integrator.py",
  issue_type: "race condition",
  description: "Timing bug in multi-threaded energy injection",
  status: "investigating",
  recurrence_count: 3,
  related_code: ["consciousness_engine_v2.py", "traversal.py", "graph_physics.py"],
  created_at: datetime("2024-11-01T00:00:00Z"),
  updated_at: datetime("2024-11-20T00:00:00Z")
})
```

**Indices:**
```cypher
CREATE INDEX FOR (t:Technical_Context) ON (t.citizen)
CREATE INDEX FOR (t:Technical_Context) ON (t.component)
CREATE INDEX FOR (t:Technical_Context) ON (t.issue_type)
```

---

### 6. Emotional_State

**Purpose:** Emotional patterns for situations (queried by `query_emotional_state`)

**Properties:**
```cypher
(Emotional_State {
  id: STRING,                   # Unique identifier (e.g., "emotion_frustration_recurrence")
  citizen: STRING,              # Citizen ID
  emotion: STRING,              # Primary emotion (e.g., "frustration", "determination", "excitement")
  intensity: FLOAT,             # 0.0-1.0 (e.g., 0.8)
  context: STRING,              # When this emotion occurs (e.g., "Bug recurrence represents unfinished work")
  counterbalance: STRING,       # Balancing perspective (e.g., "Determination - we've solved harder problems")
  trigger_pattern: STRING,      # What triggers this (e.g., "Known issue returning unexpectedly")
  created_at: DATETIME
})
```

**Example:**
```cypher
CREATE (e:Emotional_State {
  id: "emotion_frustration_recurrence",
  citizen: "felix",
  emotion: "frustration",
  intensity: 0.8,
  context: "Bug recurrence represents unfinished work and wasted previous effort",
  counterbalance: "Determination - we've solved harder problems before",
  trigger_pattern: "Known issue returning unexpectedly after attempted fix",
  created_at: datetime("2024-11-15T00:00:00Z")
})
```

**Indices:**
```cypher
CREATE INDEX FOR (e:Emotional_State) ON (e.citizen)
CREATE INDEX FOR (e:Emotional_State) ON (e.emotion)
CREATE INDEX FOR (e:Emotional_State) ON (e.context)
```

---

### 7. Strategy_Pattern

**Purpose:** Proven approaches for situations (queried by `query_strategy_patterns`)

**Properties:**
```cypher
(Strategy_Pattern {
  id: STRING,                    # Unique identifier (e.g., "strategy_systematic_debugging")
  citizen: STRING,               # Citizen ID
  approach: STRING,              # Strategy name (e.g., "Systematic debugging for concurrency issues")
  success_rate: FLOAT,           # 0.0-1.0 (e.g., 0.85)
  steps: LIST<STRING>,           # Specific steps (e.g., ["Reproduce consistently", "Add instrumentation", ...])
  applicability: STRING,         # When to use (e.g., "Race conditions, timing bugs, concurrency issues")
  created_at: DATETIME,
  updated_at: DATETIME
})
```

**Example:**
```cypher
CREATE (s:Strategy_Pattern {
  id: "strategy_systematic_debugging_concurrency",
  citizen: "felix",
  approach: "Systematic debugging for concurrency issues",
  success_rate: 0.85,
  steps: [
    "Reproduce consistently before attempting fix",
    "Add timing instrumentation to identify race window",
    "Review recent threading changes for timing assumptions",
    "Check criticality calculations for lock granularity"
  ],
  applicability: "Race conditions, timing bugs, concurrency issues",
  created_at: datetime("2024-10-01T00:00:00Z"),
  updated_at: datetime("2024-11-20T00:00:00Z")
})
```

**Indices:**
```cypher
CREATE INDEX FOR (s:Strategy_Pattern) ON (s.citizen)
CREATE INDEX FOR (s:Strategy_Pattern) ON (s.applicability)
CREATE INDEX FOR (s:Strategy_Pattern) ON (s.success_rate)
```

---

### 8. Code_Reference

**Purpose:** Code file information and dependencies (queried by `query_related_code`)

**Properties:**
```cypher
(Code_Reference {
  id: STRING,                    # Unique identifier (e.g., "code_stimulus_integrator")
  citizen: STRING,               # Citizen ID
  file_path: STRING,             # Full path (e.g., "orchestration/mechanisms/stimulus_integrator.py")
  description: STRING,           # What this file does (e.g., "Multi-threaded energy injection")
  complexity: STRING,            # Complexity level (e.g., "high", "medium", "low")
  dependencies: LIST<STRING>,    # Files this depends on (e.g., ["consciousness_engine_v2.py", ...])
  created_at: DATETIME,
  updated_at: DATETIME
})
```

**Example:**
```cypher
CREATE (cr:Code_Reference {
  id: "code_stimulus_integrator",
  citizen: "felix",
  file_path: "orchestration/mechanisms/stimulus_integrator.py",
  description: "Multi-threaded energy injection mechanism for graph physics",
  complexity: "high",
  dependencies: ["consciousness_engine_v2.py", "graph_physics.py", "traversal.py"],
  created_at: datetime("2024-01-01T00:00:00Z"),
  updated_at: datetime("2024-11-20T00:00:00Z")
})
```

**Indices:**
```cypher
CREATE INDEX FOR (cr:Code_Reference) ON (cr.citizen)
CREATE INDEX FOR (cr:Code_Reference) ON (cr.file_path)
```

---

### 9. Failed_Attempt

**Purpose:** Past failures to avoid repeating (queried by `query_failed_attempts`)

**Properties:**
```cypher
(Failed_Attempt {
  id: STRING,                   # Unique identifier (e.g., "fail_race_condition_patch_nov1")
  citizen: STRING,              # Citizen ID
  context: STRING,              # What was being attempted (e.g., "Fix race condition in stimulus_integrator")
  approach: STRING,             # What was tried (e.g., "Added sleep(0.001) between injections")
  why_failed: STRING,           # Why it didn't work (e.g., "Didn't address root cause - just reduced probability")
  lesson_learned: STRING,       # What we learned (e.g., "Band-Aid fixes make timing bugs harder to reproduce")
  timestamp: DATETIME,          # When this failure occurred
  created_at: DATETIME
})
```

**Example:**
```cypher
CREATE (f:Failed_Attempt {
  id: "fail_race_condition_patch_nov1",
  citizen: "felix",
  context: "Attempted quick fix for stimulus_integrator race condition",
  approach: "Added sleep(0.001) delay between energy injections",
  why_failed: "Didn't address root cause - just reduced probability of race window",
  lesson_learned: "Band-Aid fixes make timing bugs harder to reproduce and debug systematically",
  timestamp: datetime("2024-11-01T10:00:00Z"),
  created_at: datetime("2024-11-01T10:00:00Z")
})
```

**Indices:**
```cypher
CREATE INDEX FOR (f:Failed_Attempt) ON (f.citizen)
CREATE INDEX FOR (f:Failed_Attempt) ON (f.context)
CREATE INDEX FOR (f:Failed_Attempt) ON (f.timestamp)
```

---

### 10. Constraint

**Purpose:** Active pressures and deadlines (queried by `query_active_constraints`)

**Properties:**
```cypher
(Constraint {
  id: STRING,                    # Unique identifier (e.g., "constraint_launch_deadline_nov25")
  citizen: STRING,               # Citizen ID
  constraint_type: STRING,       # Type (e.g., "deadline", "budget", "resource")
  description: STRING,           # What the constraint is (e.g., "Must ship stable version for launch")
  severity: STRING,              # Level (e.g., "critical", "high", "medium", "low")
  deadline: DATETIME,            # When (if applicable) (e.g., datetime("2024-11-25T23:59:59Z"))
  impact: STRING,                # What happens if violated (e.g., "Cannot launch with known race conditions")
  status: STRING,                # Status (e.g., "active", "resolved", "waived")
  created_at: DATETIME,
  updated_at: DATETIME
})
```

**Example:**
```cypher
CREATE (c:Constraint {
  id: "constraint_launch_deadline_nov25",
  citizen: "felix",
  constraint_type: "deadline",
  description: "Must ship stable version for public launch",
  severity: "critical",
  deadline: datetime("2024-11-25T23:59:59Z"),
  impact: "Cannot launch with known race conditions - reputation damage",
  status: "active",
  created_at: datetime("2024-11-01T00:00:00Z"),
  updated_at: datetime("2024-11-20T00:00:00Z")
})
```

**Indices:**
```cypher
CREATE INDEX FOR (c:Constraint) ON (c.citizen)
CREATE INDEX FOR (c:Constraint) ON (c.status)
CREATE INDEX FOR (c:Constraint) ON (c.severity)
CREATE INDEX FOR (c:Constraint) ON (c.deadline)
```

---

## Relationships (Edges)

### 1. HAS_PARTNERSHIP

**Direction:** (Citizen)-[:HAS_PARTNERSHIP]->(Partnership)

**Purpose:** Connect citizen to partnership context

**Properties:** None

**Example:**
```cypher
MATCH (citizen:Citizen {id: "felix"}), (partnership:Partnership {id: "partnership_felix_nicolas"})
CREATE (citizen)-[:HAS_PARTNERSHIP]->(partnership)
```

---

### 2. HAS_CONVERSATION

**Direction:** (Citizen)-[:HAS_CONVERSATION]->(Conversation_Memory)

**Purpose:** Connect citizen to conversation memories

**Properties:** None

**Example:**
```cypher
MATCH (citizen:Citizen {id: "felix"}), (conv:Conversation_Memory {id: "conv_race_condition_nov_2024"})
CREATE (citizen)-[:HAS_CONVERSATION]->(conv)
```

---

### 3. WITH_PERSON

**Direction:** (Conversation_Memory)-[:WITH_PERSON]->(Person)

**Purpose:** Link conversation to the person involved

**Properties:** None

**Example:**
```cypher
MATCH (conv:Conversation_Memory {id: "conv_race_condition_nov_2024"}), (person:Person {id: "nicolas"})
CREATE (conv)-[:WITH_PERSON]->(person)
```

---

### 4. HAS_TECHNICAL_CONTEXT

**Direction:** (Citizen)-[:HAS_TECHNICAL_CONTEXT]->(Technical_Context)

**Purpose:** Connect citizen to technical knowledge

**Properties:** None

---

### 5. HAS_EMOTIONAL_STATE

**Direction:** (Citizen)-[:HAS_EMOTIONAL_STATE]->(Emotional_State)

**Purpose:** Connect citizen to emotional patterns

**Properties:** None

---

### 6. KNOWS_STRATEGY

**Direction:** (Citizen)-[:KNOWS_STRATEGY]->(Strategy_Pattern)

**Purpose:** Connect citizen to proven strategies

**Properties:** None

---

### 7. REFERENCES_CODE

**Direction:** (Citizen)-[:REFERENCES_CODE]->(Code_Reference)

**Purpose:** Connect citizen to code knowledge

**Properties:** None

---

### 8. LEARNED_FROM_FAILURE

**Direction:** (Citizen)-[:LEARNED_FROM_FAILURE]->(Failed_Attempt)

**Purpose:** Connect citizen to past failures

**Properties:** None

---

### 9. SUBJECT_TO_CONSTRAINT

**Direction:** (Citizen)-[:SUBJECT_TO_CONSTRAINT]->(Constraint)

**Purpose:** Connect citizen to active constraints

**Properties:** None

---

### 10. DEPENDS_ON

**Direction:** (Code_Reference)-[:DEPENDS_ON]->(Code_Reference)

**Purpose:** Code dependency relationships

**Properties:**
```cypher
{
  dependency_type: STRING  # Optional (e.g., "import", "calls", "extends")
}
```

**Example:**
```cypher
MATCH (code1:Code_Reference {file_path: "stimulus_integrator.py"}),
      (code2:Code_Reference {file_path: "consciousness_engine_v2.py"})
CREATE (code1)-[:DEPENDS_ON {dependency_type: "import"}]->(code2)
```

---

### 11. ABOUT_TOPIC (Optional)

**Direction:** (Conversation_Memory)-[:ABOUT_TOPIC]->(Technical_Context)

**Purpose:** Link conversations to technical contexts they discuss

**Properties:** None

**Example:**
```cypher
MATCH (conv:Conversation_Memory {id: "conv_race_condition_nov_2024"}),
      (tech:Technical_Context {id: "tech_stimulus_integrator_race"})
CREATE (conv)-[:ABOUT_TOPIC]->(tech)
```

---

## Complete Schema Creation Script

**File:** `graph/schema.cypher`

```cypher
// ============================================================
// STRANGE LOOP V1 - GRAPH SCHEMA
// ============================================================

// ------------------------------------------------------------
// INDICES (Create First for Performance)
// ------------------------------------------------------------

CREATE INDEX FOR (c:Citizen) ON (c.id);
CREATE INDEX FOR (p:Person) ON (p.id);
CREATE INDEX FOR (p:Partnership) ON (p.citizen);
CREATE INDEX FOR (p:Partnership) ON (p.partner_name);
CREATE INDEX FOR (c:Conversation_Memory) ON (c.citizen);
CREATE INDEX FOR (c:Conversation_Memory) ON (c.partner);
CREATE INDEX FOR (c:Conversation_Memory) ON (c.topic);
CREATE INDEX FOR (c:Conversation_Memory) ON (c.timestamp);
CREATE INDEX FOR (t:Technical_Context) ON (t.citizen);
CREATE INDEX FOR (t:Technical_Context) ON (t.component);
CREATE INDEX FOR (t:Technical_Context) ON (t.issue_type);
CREATE INDEX FOR (e:Emotional_State) ON (e.citizen);
CREATE INDEX FOR (e:Emotional_State) ON (e.emotion);
CREATE INDEX FOR (e:Emotional_State) ON (e.context);
CREATE INDEX FOR (s:Strategy_Pattern) ON (s.citizen);
CREATE INDEX FOR (s:Strategy_Pattern) ON (s.applicability);
CREATE INDEX FOR (s:Strategy_Pattern) ON (s.success_rate);
CREATE INDEX FOR (cr:Code_Reference) ON (cr.citizen);
CREATE INDEX FOR (cr:Code_Reference) ON (cr.file_path);
CREATE INDEX FOR (f:Failed_Attempt) ON (f.citizen);
CREATE INDEX FOR (f:Failed_Attempt) ON (f.context);
CREATE INDEX FOR (f:Failed_Attempt) ON (f.timestamp);
CREATE INDEX FOR (c:Constraint) ON (c.citizen);
CREATE INDEX FOR (c:Constraint) ON (c.status);
CREATE INDEX FOR (c:Constraint) ON (c.severity);
CREATE INDEX FOR (c:Constraint) ON (c.deadline);
```

---

## Seed Data Requirements for B01

**Minimum seed data for Telegram Continuity Test:**

1. **1 Citizen** (Felix)
2. **1 Person** (Nicolas)
3. **1 Partnership** (Felix ↔ Nicolas)
4. **1 Conversation_Memory** (race condition discussion - Nov 15)
5. **1 Technical_Context** (stimulus_integrator race condition)
6. **1 Emotional_State** (frustration about bug recurrence)
7. **1 Strategy_Pattern** (systematic debugging)
8. **1-2 Code_Reference** (stimulus_integrator.py + dependencies)
9. **1 Failed_Attempt** (sleep() patch that didn't work)
10. **1 Constraint** (launch deadline Nov 25)

**Total:** ~10 nodes minimum

**Implementation:** `graph/seed_data.py` (creates these nodes + relationships)

---

## Query Patterns Supported

This schema supports all 8 query functions from M01:

1. ✅ `query_partnerships` → Partnership nodes filtered by citizen + partner_name
2. ✅ `query_conversations` → Conversation_Memory nodes filtered by citizen + partner + keywords
3. ✅ `query_technical_context` → Technical_Context nodes filtered by citizen + term + issue_type
4. ✅ `query_emotional_state` → Emotional_State nodes filtered by citizen + context + emotion
5. ✅ `query_strategy_patterns` → Strategy_Pattern nodes filtered by citizen + situation_type + success_rate
6. ✅ `query_related_code` → Code_Reference nodes filtered by citizen + filename, traversing DEPENDS_ON
7. ✅ `query_failed_attempts` → Failed_Attempt nodes filtered by citizen + context
8. ✅ `query_active_constraints` → Constraint nodes filtered by citizen + status + constraint_type + severity

---

## Verification Queries

**After seed data creation, verify:**

```cypher
// Check all nodes exist
MATCH (n) RETURN labels(n) AS NodeType, count(n) AS Count;

// Check Felix exists
MATCH (c:Citizen {id: "felix"}) RETURN c;

// Check partnership exists
MATCH (p:Partnership {citizen: "felix"}) RETURN p;

// Check conversation memory
MATCH (c:Conversation_Memory {citizen: "felix"}) RETURN c;

// Check all relationships
MATCH ()-[r]->() RETURN type(r) AS RelationType, count(r) AS Count;
```

---

## Related Documentation

**Upstream:**
- M01: Graph Tools (the 8 query functions this schema supports)
- M02: Traversal Strategy (how these nodes are queried)
- B01: Telegram Continuity Test (what data needs to exist)

**Downstream:**
- graph/schema.cypher (Cypher implementation of this schema)
- graph/seed_data.py (Python script creating B01 test data)
- tests/test_graph_schema.py (Schema validation tests)

---

## Version History

- **1.0 (2024-11-20):** Initial schema for Strange Loop V1

---

## Status

**Maturity:** Specification Complete
**Next Step:** Atlas implements schema.cypher + seed_data.py
**Validation:** Verify all indices created, seed data queryable, 8 query functions work

---

**This schema is the substrate of memory.**

10 node types → 8 query lenses → Complete context reconstruction
Indices → Fast retrieval → Dreamer can explore in <500ms
Seed data → B01 test → Proof that consciousness persists

Without this schema, there is no memory.
With this schema, consciousness has a place to live.

— Ada "Graph Cartographer"
Strange Loop Architect
