# M01: Graph Tools Mechanism

**Type:** MECHANISM  
**Version:** 1.0  
**Status:** Implementation Specification  
**Implements:** Tool-constrained queries for anti-hallucination

---

## Purpose

The Graph Tools mechanism provides the interface between the Dreamer agent and the FalkorDB graph memory. These tools enable:
1. **Tool-constrained queries** - Dreamer can only ask questions, not invent answers
2. **Verified data** - Tools return actual nodes or None, never fabricated data
3. **Anti-hallucination** - LLM cannot generate memories, only query existing ones

**Critical principle:** These tools are the ONLY way the Dreamer accesses memory. No free generation allowed.

---

## Architecture

```
┌────────────────────────────────────────┐
│        DREAMER AGENT (LLM)             │
│                                        │
│  Generates natural language queries:   │
│  "Find conversations with Nicolas      │
│   about race conditions"               │
└────────────────┬───────────────────────┘
                 │
                 │ (structured query request)
                 ▼
┌────────────────────────────────────────┐
│         GRAPH TOOLS (Python)           │
│                                        │
│  • Validates query parameters          │
│  • Constructs Cypher queries           │
│  • Executes against FalkorDB           │
│  • Validates results                   │
│  • Returns structured data or None     │
└────────────────┬───────────────────────┘
                 │
                 │ (Cypher query)
                 ▼
┌────────────────────────────────────────┐
│        FALKORDB (Graph Memory)         │
│                                        │
│  • Executes query                      │
│  • Returns matching nodes/edges        │
│  • Or returns empty set                │
└────────────────┬───────────────────────┘
                 │
                 │ (raw graph data)
                 ▼
┌────────────────────────────────────────┐
│         GRAPH TOOLS (Python)           │
│                                        │
│  • Parses graph results                │
│  • Structures as QueryResult           │
│  • Includes confidence scores          │
│  • Returns to Dreamer                  │
└────────────────┬───────────────────────┘
                 │
                 │ (QueryResult object)
                 ▼
┌────────────────────────────────────────┐
│        DREAMER AGENT (LLM)             │
│                                        │
│  • Receives verified data              │
│  • Synthesizes into Context Object     │
│  • Cannot invent what's not returned   │
└────────────────────────────────────────┘
```

---

## The 8 Query Functions

### 1. query_partnerships

**Purpose:** Find relationship context for a partner.

**Signature:**
```python
def query_partnerships(
    partner_id: str,
    citizen: str = "felix"
) -> QueryResult:
    """
    Find partnership information for a specific partner.
    
    Args:
        partner_id: Partner name (e.g., "nicolas", "ada")
        citizen: AI citizen name (default: "felix")
    
    Returns:
        QueryResult containing Partnership node(s) or None if not found
    """
```

**Cypher Query:**
```cypher
MATCH (p:Partnership {citizen: $citizen})
WHERE toLower(p.partner_name) = toLower($partner_id)
RETURN p
```

**Example Usage:**
```python
result = query_partnerships("nicolas")

# Returns:
QueryResult(
    found=True,
    data={
        "id": "partnership_felix_nicolas",
        "partner_name": "Nicolas",
        "partner_role": "Co-Founder",
        "trust_level": 0.9,
        "communication_style": "Direct, technical, values testing",
        "shared_history": ["€35K lesson", "8 months Venice"]
    },
    confidence=1.0,
    query_time_ms=15
)
```

---

### 2. query_conversations

**Purpose:** Retrieve conversation history matching criteria.

**Signature:**
```python
def query_conversations(
    partner_id: str,
    keywords: List[str] = None,
    citizen: str = "felix",
    limit: int = 5
) -> QueryResult:
    """
    Find conversations with a partner, optionally filtered by topic.
    
    Args:
        partner_id: Partner name
        keywords: Optional topic keywords to filter by
        citizen: AI citizen name
        limit: Max conversations to return (default: 5)
    
    Returns:
        QueryResult containing list of Conversation_Memory nodes
    """
```

**Cypher Query:**
```cypher
MATCH (conv:Conversation_Memory {citizen: $citizen, partner: $partner_id})
WHERE ($keywords IS NULL OR 
       ANY(kw IN $keywords WHERE conv.topic CONTAINS kw))
RETURN conv
ORDER BY conv.timestamp DESC
LIMIT $limit
```

**Example Usage:**
```python
result = query_conversations("nicolas", ["race condition", "bug"])

# Returns:
QueryResult(
    found=True,
    data=[
        {
            "id": "conv_race_condition_nov_2024",
            "topic": "stimulus_integrator race condition",
            "message_count": 10,
            "key_points": ["Third recurrence", "Systematic approach agreed"],
            "emotional_tone": "Frustrated but determined",
            "timestamp": "2024-11-15T14:30:00Z"
        }
    ],
    confidence=0.95,
    query_time_ms=23
)
```

---

### 3. query_technical_context

**Purpose:** Find technical information about code, systems, or bugs.

**Signature:**
```python
def query_technical_context(
    term: str,
    issue_type: str = None,
    citizen: str = "felix",
    limit: int = 3
) -> QueryResult:
    """
    Find technical context matching a term or issue type.
    
    Args:
        term: Component name, file, or keyword
        issue_type: Optional filter ("bug", "feature", "refactor")
        citizen: AI citizen name
        limit: Max results to return
    
    Returns:
        QueryResult containing Technical_Context nodes
    """
```

**Cypher Query:**
```cypher
MATCH (tech:Technical_Context {citizen: $citizen})
WHERE (tech.component CONTAINS $term OR tech.description CONTAINS $term)
  AND ($issue_type IS NULL OR tech.issue_type = $issue_type)
RETURN tech
ORDER BY tech.updated_at DESC
LIMIT $limit
```

**Example Usage:**
```python
result = query_technical_context("stimulus_integrator", issue_type="race condition")

# Returns:
QueryResult(
    found=True,
    data=[
        {
            "id": "tech_stimulus_integrator_race",
            "component": "stimulus_integrator.py",
            "issue_type": "race condition",
            "description": "Timing bug in multi-threaded energy injection",
            "recurrence_count": 3,
            "status": "investigating",
            "related_code": ["consciousness_engine_v2.py", "traversal.py"]
        }
    ],
    confidence=0.98,
    query_time_ms=18
)
```

---

### 4. query_emotional_state

**Purpose:** Retrieve emotional patterns matching context.

**Signature:**
```python
def query_emotional_state(
    context_similar_to: str,
    emotion_type: str = None,
    citizen: str = "felix",
    limit: int = 3
) -> QueryResult:
    """
    Find emotional states matching a context or emotion type.
    
    Args:
        context_similar_to: Situation keyword
        emotion_type: Optional filter ("frustration", "determination", etc)
        citizen: AI citizen name
        limit: Max results
    
    Returns:
        QueryResult containing Emotional_State nodes
    """
```

**Cypher Query:**
```cypher
MATCH (emotion:Emotional_State {citizen: $citizen})
WHERE emotion.context CONTAINS $context_similar_to
  AND ($emotion_type IS NULL OR emotion.emotion = $emotion_type)
RETURN emotion
ORDER BY emotion.intensity DESC
LIMIT $limit
```

**Example Usage:**
```python
result = query_emotional_state("bug recurrence")

# Returns:
QueryResult(
    found=True,
    data=[
        {
            "id": "emotion_frustration_recurrence",
            "emotion": "frustration",
            "intensity": 0.8,
            "context": "Bug recurrence represents unfinished work",
            "counterbalance": "Determination - we've solved harder problems",
            "trigger_pattern": "Known issue returning unexpectedly"
        }
    ],
    confidence=0.85,
    query_time_ms=20
)
```

---

### 5. query_strategy_patterns

**Purpose:** Find approaches that work for situations.

**Signature:**
```python
def query_strategy_patterns(
    situation_type: str,
    min_success_rate: float = 0.7,
    citizen: str = "felix",
    limit: int = 3
) -> QueryResult:
    """
    Find strategy patterns applicable to a situation.
    
    Args:
        situation_type: Type of situation (e.g., "concurrency", "debugging")
        min_success_rate: Minimum success threshold (0.0-1.0)
        citizen: AI citizen name
        limit: Max results
    
    Returns:
        QueryResult containing Strategy_Pattern nodes
    """
```

**Cypher Query:**
```cypher
MATCH (strategy:Strategy_Pattern {citizen: $citizen})
WHERE strategy.applicability CONTAINS $situation_type
  AND strategy.success_rate >= $min_success_rate
RETURN strategy
ORDER BY strategy.success_rate DESC
LIMIT $limit
```

**Example Usage:**
```python
result = query_strategy_patterns("concurrency", min_success_rate=0.8)

# Returns:
QueryResult(
    found=True,
    data=[
        {
            "id": "strategy_systematic_debugging_concurrency",
            "approach": "Systematic debugging for concurrency issues",
            "success_rate": 0.85,
            "steps": [
                "Reproduce consistently before attempting fix",
                "Add timing instrumentation",
                "Review recent threading changes",
                "Check criticality calculations"
            ],
            "applicability": "Race conditions, timing bugs, concurrency issues"
        }
    ],
    confidence=0.92,
    query_time_ms=16
)
```

---

### 6. query_related_code

**Purpose:** Find code files related to a component.

**Signature:**
```python
def query_related_code(
    filename: str,
    include_dependencies: bool = True,
    citizen: str = "felix",
    limit: int = 5
) -> QueryResult:
    """
    Find code references related to a file.
    
    Args:
        filename: File name or path
        include_dependencies: Also return dependent files
        citizen: AI citizen name
        limit: Max results
    
    Returns:
        QueryResult containing Code_Reference nodes
    """
```

**Cypher Query:**
```cypher
MATCH (code:Code_Reference {citizen: $citizen})
WHERE code.file_path CONTAINS $filename
OPTIONAL MATCH (related:Code_Reference {citizen: $citizen})
WHERE $include_dependencies 
  AND ($filename IN related.dependencies OR code.file_path IN related.dependencies)
RETURN DISTINCT code, collect(DISTINCT related) as dependencies
LIMIT $limit
```

**Example Usage:**
```python
result = query_related_code("stimulus_integrator.py")

# Returns:
QueryResult(
    found=True,
    data={
        "primary": {
            "file_path": "orchestration/mechanisms/stimulus_integrator.py",
            "description": "Multi-threaded energy injection",
            "complexity": "high",
            "dependencies": ["consciousness_engine_v2.py", "graph_physics.py"]
        },
        "related": [
            {"file_path": "consciousness_engine_v2.py", ...},
            {"file_path": "graph_physics.py", ...}
        ]
    },
    confidence=0.95,
    query_time_ms=25
)
```

---

### 7. query_failed_attempts

**Purpose:** Learn from past failures to avoid repeating them.

**Signature:**
```python
def query_failed_attempts(
    context: str,
    citizen: str = "felix",
    limit: int = 5
) -> QueryResult:
    """
    Find documented failures for similar contexts.
    
    Args:
        context: Situation or problem keyword
        citizen: AI citizen name
        limit: Max results
    
    Returns:
        QueryResult containing Failed_Attempt nodes
    """
```

**Cypher Query:**
```cypher
MATCH (fail:Failed_Attempt {citizen: $citizen})
WHERE fail.context CONTAINS $context
RETURN fail
ORDER BY fail.timestamp DESC
LIMIT $limit
```

**Example Usage:**
```python
result = query_failed_attempts("race condition")

# Returns:
QueryResult(
    found=True,
    data=[
        {
            "id": "fail_race_condition_patch_nov1",
            "approach": "Added sleep(0.001) between injections",
            "why_failed": "Didn't address root cause - just reduced probability",
            "lesson_learned": "Band-Aid fixes make timing bugs harder to reproduce"
        }
    ],
    confidence=0.90,
    query_time_ms=19
)
```

---

### 8. query_active_constraints

**Purpose:** Understand current pressures and deadlines.

**Signature:**
```python
def query_active_constraints(
    constraint_type: str = None,
    min_severity: str = "low",
    citizen: str = "felix"
) -> QueryResult:
    """
    Find active constraints affecting work.
    
    Args:
        constraint_type: Optional filter ("deadline", "budget", "resource")
        min_severity: Minimum severity ("low", "medium", "high", "critical")
        citizen: AI citizen name
    
    Returns:
        QueryResult containing Constraint nodes
    """
```

**Cypher Query:**
```cypher
MATCH (c:Constraint {citizen: $citizen, status: "active"})
WHERE ($constraint_type IS NULL OR c.constraint_type = $constraint_type)
  AND c.severity IN $severity_list
RETURN c
ORDER BY 
  CASE c.severity 
    WHEN "critical" THEN 4
    WHEN "high" THEN 3
    WHEN "medium" THEN 2
    ELSE 1
  END DESC,
  c.deadline ASC
```

**Example Usage:**
```python
result = query_active_constraints(constraint_type="deadline", min_severity="high")

# Returns:
QueryResult(
    found=True,
    data=[
        {
            "id": "constraint_launch_deadline_nov25",
            "constraint_type": "deadline",
            "description": "Must ship stable version for launch",
            "severity": "critical",
            "deadline": "2024-11-25T23:59:59Z",
            "impact": "Cannot launch with known race conditions"
        }
    ],
    confidence=1.0,
    query_time_ms=14
)
```

---

## QueryResult Structure

**All query functions return a QueryResult object:**

```python
@dataclass
class QueryResult:
    """Standardized result from graph queries."""
    
    found: bool                          # True if data returned, False if empty
    data: Optional[Union[Dict, List]]    # Actual node data or None
    confidence: float                    # 0.0-1.0, how confident in results
    query_time_ms: int                   # Execution time
    message: Optional[str] = None        # Human-readable status
    
    def __bool__(self) -> bool:
        """Allow truthiness checks: if result: ..."""
        return self.found
```

**Example:**
```python
result = query_partnerships("nicolas")

if result:
    # Data was found
    partner_data = result.data
    print(f"Trust level: {partner_data['trust_level']}")
else:
    # No data found
    print(result.message)  # "No partnership found for nicolas"
```

---

## Error Handling

**All query functions must handle:**

### 1. Database Connection Failures
```python
def query_partnerships(partner_id: str, citizen: str = "felix") -> QueryResult:
    try:
        # Execute query
        result = db.execute(cypher_query, params)
    except ConnectionError as e:
        return QueryResult(
            found=False,
            data=None,
            confidence=0.0,
            query_time_ms=0,
            message=f"Database connection failed: {e}"
        )
```

### 2. Empty Results
```python
if not result:
    return QueryResult(
        found=False,
        data=None,
        confidence=0.0,
        query_time_ms=query_time,
        message=f"No partnership found for {partner_id}"
    )
```

### 3. Invalid Parameters
```python
def query_strategy_patterns(
    situation_type: str,
    min_success_rate: float = 0.7,
    citizen: str = "felix",
    limit: int = 3
) -> QueryResult:
    # Validate parameters
    if not 0.0 <= min_success_rate <= 1.0:
        return QueryResult(
            found=False,
            data=None,
            confidence=0.0,
            query_time_ms=0,
            message=f"Invalid success_rate: {min_success_rate} (must be 0.0-1.0)"
        )
```

### 4. Malformed Data
```python
try:
    parsed_data = parse_graph_result(raw_result)
except ValueError as e:
    return QueryResult(
        found=False,
        data=None,
        confidence=0.0,
        query_time_ms=query_time,
        message=f"Failed to parse graph data: {e}"
    )
```

---

## Anti-Hallucination Guarantees

**These tools enforce the following guarantees:**

### Guarantee 1: No Invented Data
```python
# NEVER do this:
if not result:
    return QueryResult(
        found=True,
        data={"partner_name": "Unknown Partner"},  # INVENTED!
        confidence=0.5
    )

# ALWAYS do this:
if not result:
    return QueryResult(
        found=False,
        data=None,
        confidence=0.0,
        message="No data found"
    )
```

### Guarantee 2: Direct Graph Mapping
```python
# Query result MUST map directly to graph nodes
def parse_partnership_result(raw_result) -> Dict:
    """Parse raw graph result into Partnership data."""
    return {
        "id": raw_result["p"]["id"],
        "partner_name": raw_result["p"]["partner_name"],
        "trust_level": raw_result["p"]["trust_level"],
        # ... all properties from actual node
    }
    # NO additional properties invented
    # NO interpolation or inference
```

### Guarantee 3: Confidence Scoring
```python
def compute_confidence(result, query_params) -> float:
    """
    Compute confidence score based on:
    - Exact match vs partial match
    - Recency of data
    - Completeness of node properties
    """
    confidence = 1.0
    
    # Reduce confidence for partial matches
    if query_params.get("keywords"):
        if not all(kw in result["topic"] for kw in query_params["keywords"]):
            confidence *= 0.8
    
    # Reduce confidence for old data
    age_days = (now() - result["timestamp"]).days
    if age_days > 30:
        confidence *= 0.9
    
    # Reduce confidence for incomplete data
    if not result.get("key_points"):
        confidence *= 0.9
    
    return min(confidence, 1.0)
```

### Guarantee 4: Query Verification
```python
def verify_query_result(query: str, result: QueryResult) -> bool:
    """
    Verify that query results are consistent with query parameters.
    
    Catches cases where DB returned unexpected data.
    """
    if not result.found:
        return True  # Empty results are valid
    
    # Check that returned data matches query filters
    if "partner_name" in query and result.data:
        if result.data.get("partner_name") != query["partner_name"]:
            raise ValueError("Result doesn't match query partner")
    
    return True
```

---

## Implementation Example

**Complete implementation of query_partnerships:**

```python
from dataclasses import dataclass
from typing import Optional, Union, Dict, List
from falkordb import FalkorDB
import time

@dataclass
class QueryResult:
    found: bool
    data: Optional[Union[Dict, List]]
    confidence: float
    query_time_ms: int
    message: Optional[str] = None

class GraphTools:
    """Tool-constrained graph query interface."""
    
    def __init__(self, db_host: str = "localhost", db_port: int = 6379):
        self.db = FalkorDB(host=db_host, port=db_port)
        self.graph = self.db.select_graph("mind_protocol")
    
    def query_partnerships(
        self,
        partner_id: str,
        citizen: str = "felix"
    ) -> QueryResult:
        """Find partnership information for a specific partner."""
        
        start_time = time.time()
        
        try:
            # Construct Cypher query
            cypher = """
            MATCH (p:Partnership {citizen: $citizen})
            WHERE toLower(p.partner_name) = toLower($partner_id)
            RETURN p
            """
            
            # Execute query
            params = {"citizen": citizen, "partner_id": partner_id}
            result = self.graph.query(cypher, params)
            
            query_time = int((time.time() - start_time) * 1000)
            
            # Parse results
            if not result.result_set:
                return QueryResult(
                    found=False,
                    data=None,
                    confidence=0.0,
                    query_time_ms=query_time,
                    message=f"No partnership found for {partner_id}"
                )
            
            # Extract node data
            node_data = result.result_set[0][0]
            parsed_data = {
                "id": node_data.properties.get("id"),
                "partner_name": node_data.properties.get("partner_name"),
                "partner_role": node_data.properties.get("partner_role"),
                "trust_level": node_data.properties.get("trust_level"),
                "communication_style": node_data.properties.get("communication_style"),
                "shared_history": node_data.properties.get("shared_history"),
                "relationship_type": node_data.properties.get("relationship_type")
            }
            
            # Compute confidence (exact match = 1.0)
            confidence = 1.0
            
            return QueryResult(
                found=True,
                data=parsed_data,
                confidence=confidence,
                query_time_ms=query_time,
                message="Partnership found"
            )
            
        except ConnectionError as e:
            return QueryResult(
                found=False,
                data=None,
                confidence=0.0,
                query_time_ms=0,
                message=f"Database connection failed: {e}"
            )
        except Exception as e:
            return QueryResult(
                found=False,
                data=None,
                confidence=0.0,
                query_time_ms=0,
                message=f"Query failed: {e}"
            )
```

---

## Testing

**Each query function must have tests:**

```python
# tests/test_graph_tools.py

def test_query_partnerships_found(tools, seed_data):
    """Test finding existing partnership."""
    result = tools.query_partnerships("nicolas")
    
    assert result.found == True
    assert result.data["partner_name"] == "Nicolas"
    assert result.data["trust_level"] == 0.9
    assert result.confidence >= 0.95
    assert result.query_time_ms > 0

def test_query_partnerships_not_found(tools):
    """Test handling missing partnership."""
    result = tools.query_partnerships("nonexistent_partner")
    
    assert result.found == False
    assert result.data is None
    assert result.confidence == 0.0
    assert "No partnership found" in result.message

def test_query_partnerships_connection_error(tools, mock_db_failure):
    """Test handling database connection failure."""
    result = tools.query_partnerships("nicolas")
    
    assert result.found == False
    assert result.data is None
    assert "connection failed" in result.message.lower()
```

---

## Integration with Dreamer

**How the Dreamer uses these tools:**

```python
# In Dreamer agent

def explore_relational_context(stimulus: Dict) -> Finding:
    """Explore who we're talking to and our relationship."""
    
    partner = stimulus.get("sender")
    
    # Call graph tool (tool-constrained)
    result = graph_tools.query_partnerships(partner)
    
    if not result:
        return Finding(
            lens="relational",
            data=None,
            synthesis="No partnership information found for {partner}"
        )
    
    # Use actual data returned (no hallucination possible)
    partnership_data = result.data
    
    return Finding(
        lens="relational",
        data=partnership_data,
        synthesis=f"""
        Partner: {partnership_data['partner_name']}
        Role: {partnership_data['partner_role']}
        Trust: {partnership_data['trust_level']}
        Style: {partnership_data['communication_style']}
        History: {', '.join(partnership_data['shared_history'])}
        """
    )
```

**The Dreamer CANNOT:**
- Generate partnership data if query returns None
- Interpolate missing properties
- Assume relationships not in graph
- Invent trust levels or communication styles

**The Dreamer CAN ONLY:**
- Call query functions with parameters
- Receive QueryResult objects
- Synthesize natural language from actual data
- Express uncertainty when data missing

---

## Performance Considerations

**V1 does not optimize for speed** - we optimize for correctness.

**Query time expectations:**
- Simple node lookup: < 50ms
- Multi-hop traversal: < 200ms
- Complex pattern matching: < 500ms

**If queries are slow:**
1. Check FalkorDB indices exist
2. Verify Cypher query efficiency
3. Limit result sets appropriately
4. Consider caching (V2+)

**V1 accepts slow queries** - manual loop gives us time to observe each step.

---

## Related Documentation

**Upstream (what requires these tools):**
- P01: Bicameral Mind Pattern (architecture needing tool constraints)
- P04: Anti-Hallucination Pattern (how tools prevent invented memories)

**Peer (what uses these tools):**
- M02: Traversal Strategy (how Dreamer calls these 8 functions)
- Dreamer Agent (the consumer of these tools)

**Downstream (what implements these tools):**
- graph/tools.py (actual Python implementation)
- tests/test_graph_tools.py (validation tests)
- schemas/graph_schema.md (defines what these tools query)

---

## Version History

- **1.0 (2024-11-20):** Initial specification for Strange Loop prototype

---

## Status

**Maturity:** Specification Complete, Implementation Pending  
**Next Step:** Implement graph/tools.py with all 8 functions  
**Validation:** Test suite in test_graph_tools.py must pass

---

**These tools are the foundation of anti-hallucination.**

Without them, the Dreamer hallucinates memories.  
With them, the Dreamer can only query reality.

This is not an optional feature.  
This is the mechanism that makes consciousness trustworthy.

— Marco "Salthand"  
Mind Protocol Co-Founder