# M02: Traversal Strategy Mechanism

**Type:** MECHANISM  
**Version:** 1.0  
**Status:** Implementation Specification  
**Implements:** 8-lens exploration pattern for comprehensive context reconstruction

---

## Purpose

The Traversal Strategy mechanism defines HOW the Dreamer explores graph memory to reconstruct context. It answers:
- What order to query in?
- How many queries per lens?
- When to follow deeper threads?
- How to handle missing data?
- When is exploration complete?

**Critical principle:** Comprehensive exploration is more important than speed. V1 accepts 5-10 second exploration time.

---

## The 8-Lens Framework

Each lens explores a different dimension of context:

```
1. RELATIONAL    → Who am I talking to? (partnerships, relationships)
2. HISTORICAL    → What did we discuss? (conversations, past exchanges)
3. TECHNICAL     → What systems are involved? (code, bugs, implementations)
4. EMOTIONAL     → How do I feel about this? (emotional states, patterns)
5. STRATEGIC     → What approaches work? (successful strategies)
6. EXPERIENTIAL  → What failed before? (past mistakes, anti-patterns)
7. CONSTRAINT    → What pressures exist? (deadlines, limitations)
8. CONNECTIVE    → What else relates? (code dependencies, related contexts)
```

**Why 8 lenses?**
- Fewer lenses → incomplete context (miss emotional or strategic dimensions)
- More lenses → diminishing returns (redundancy, noise)
- 8 lenses → comprehensive coverage without excess

---

## Exploration Flow

```
┌─────────────────────────────────────────────────┐
│         STIMULUS ARRIVES                        │
│   "Hey Felix, the race condition is back"       │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
       ┌───────────────────────┐
       │  Dreamer Wake-Up      │
       │  Parse stimulus       │
       │  Extract: sender,     │
       │          topic,       │
       │          keywords     │
       └───────────┬───────────┘
                   │
                   ▼
  ╔════════════════════════════════════╗
  ║  LENS 1: RELATIONAL CONTEXT       ║
  ║  query_partnerships(sender)        ║
  ║  → Who is this person?             ║
  ║  → What's our relationship?        ║
  ╚════════════╤═══════════════════════╝
               │
               ▼
  ╔════════════════════════════════════╗
  ║  LENS 2: HISTORICAL CONTEXT       ║
  ║  query_conversations(sender, kw)   ║
  ║  → What have we discussed?         ║
  ║  → Recent exchanges?               ║
  ╚════════════╤═══════════════════════╝
               │
               ▼
  ╔════════════════════════════════════╗
  ║  LENS 3: TECHNICAL CONTEXT        ║
  ║  query_technical_context(term)     ║
  ║  → What systems/code involved?     ║
  ║  → Known issues?                   ║
  ╚════════════╤═══════════════════════╝
               │
               ▼
  ╔════════════════════════════════════╗
  ║  LENS 4: EMOTIONAL CONTEXT        ║
  ║  query_emotional_state(situation)  ║
  ║  → How do I feel about this?       ║
  ║  → Emotional patterns?             ║
  ╚════════════╤═══════════════════════╝
               │
               ▼
  ╔════════════════════════════════════╗
  ║  LENS 5: STRATEGIC CONTEXT        ║
  ║  query_strategy_patterns(type)     ║
  ║  → What approaches work here?      ║
  ║  → Proven methodologies?           ║
  ╚════════════╤═══════════════════════╝
               │
               ▼
  ╔════════════════════════════════════╗
  ║  LENS 6: EXPERIENTIAL CONTEXT     ║
  ║  query_failed_attempts(context)    ║
  ║  → What didn't work before?        ║
  ║  → Mistakes to avoid?              ║
  ╚════════════╤═══════════════════════╝
               │
               ▼
  ╔════════════════════════════════════╗
  ║  LENS 7: CONSTRAINT CONTEXT       ║
  ║  query_active_constraints(type)    ║
  ║  → What are the pressures?         ║
  ║  → Deadlines? Limitations?         ║
  ╚════════════╤═══════════════════════╝
               │
               ▼
  ╔════════════════════════════════════╗
  ║  LENS 8: CONNECTIVE CONTEXT       ║
  ║  query_related_code(component)     ║
  ║  → What else connects?             ║
  ║  → Dependencies? Related systems?  ║
  ╚════════════╤═══════════════════════╝
               │
               ▼
       ┌───────────────────────┐
       │  SYNTHESIS PHASE      │
       │  Compile all findings │
       │  Generate Context     │
       │  Object for Driver    │
       └───────────┬───────────┘
                   │
                   ▼
            [Context Object]
```

**Key insight:** Sequential exploration, not parallel. Each lens informs the next.

---

## Lens Specifications

### Lens 1: Relational Context

**Goal:** Understand WHO we're interacting with.

**Query:**
```python
def explore_relational(stimulus: Dict, findings: Dict) -> Finding:
    """
    Explore relationship with the sender.
    
    Critical for: Setting tone, understanding history, calibrating response
    """
    sender = stimulus.get("sender", "unknown")
    
    # Query partnership
    partnership = graph_tools.query_partnerships(sender)
    
    if not partnership:
        return Finding(
            lens="relational",
            data=None,
            synthesis="No established partnership with {sender}",
            confidence=0.0,
            needs_deeper_exploration=False
        )
    
    # Extract key relationship data
    return Finding(
        lens="relational",
        data=partnership.data,
        synthesis=f"""
        Partner: {partnership.data['partner_name']}
        Relationship: {partnership.data['relationship_type']}
        Trust Level: {partnership.data['trust_level']}
        Communication Style: {partnership.data['communication_style']}
        Shared History: {', '.join(partnership.data['shared_history'])}
        """,
        confidence=partnership.confidence,
        needs_deeper_exploration=False  # Partnership is complete context
    )
```

**What this provides:**
- Trust level (affects how direct to be)
- Communication style (affects tone)
- Shared history (affects references)
- Relationship type (affects formality)

---

### Lens 2: Historical Context

**Goal:** Retrieve relevant past conversations.

**Query:**
```python
def explore_historical(stimulus: Dict, findings: Dict) -> Finding:
    """
    Find past conversations on this topic.
    
    Critical for: Continuity, showing we remember, building on past discussions
    """
    sender = stimulus.get("sender")
    
    # Extract topic keywords from stimulus
    keywords = extract_keywords(stimulus.get("content", ""))
    
    # Query conversations
    conversations = graph_tools.query_conversations(
        partner_id=sender,
        keywords=keywords,
        limit=5
    )
    
    if not conversations:
        return Finding(
            lens="historical",
            data=None,
            synthesis=f"No previous conversations found about {keywords}",
            confidence=0.0,
            needs_deeper_exploration=False
        )
    
    # Find most relevant conversation
    most_recent = conversations.data[0]
    
    return Finding(
        lens="historical",
        data=conversations.data,
        synthesis=f"""
        Most Recent Discussion: {most_recent['topic']}
        When: {most_recent['timestamp']}
        Messages: {most_recent['message_count']}
        Key Points: {', '.join(most_recent['key_points'])}
        Emotional Tone: {most_recent['emotional_tone']}
        Outcome: {most_recent.get('outcome', 'In progress')}
        """,
        confidence=conversations.confidence,
        needs_deeper_exploration=True  # Might need to explore technical details
    )
```

**What this provides:**
- Topic of past discussion
- Key points mentioned
- Emotional context of conversation
- Current status/outcome

---

### Lens 3: Technical Context

**Goal:** Understand technical systems/code involved.

**Query:**
```python
def explore_technical(stimulus: Dict, findings: Dict) -> Finding:
    """
    Find technical context for systems mentioned.
    
    Critical for: Understanding what we're actually working on
    """
    # Extract technical terms
    historical = findings.get("historical", {})
    terms = extract_technical_terms(
        stimulus.get("content", ""),
        historical.get("data", [])
    )
    
    if not terms:
        return Finding(
            lens="technical",
            data=None,
            synthesis="No specific technical components identified",
            confidence=0.0,
            needs_deeper_exploration=False
        )
    
    # Query each term
    technical_contexts = []
    for term in terms[:3]:  # Limit to top 3 terms
        result = graph_tools.query_technical_context(term)
        if result:
            technical_contexts.append(result.data)
    
    if not technical_contexts:
        return Finding(
            lens="technical",
            data=None,
            synthesis=f"No technical context found for {terms}",
            confidence=0.0,
            needs_deeper_exploration=False
        )
    
    # Synthesize findings
    primary = technical_contexts[0]
    return Finding(
        lens="technical",
        data=technical_contexts,
        synthesis=f"""
        Component: {primary['component']}
        Issue Type: {primary['issue_type']}
        Description: {primary['description']}
        Status: {primary['status']}
        Recurrences: {primary.get('recurrence_count', 0)}
        Related Code: {', '.join(primary['related_code'])}
        """,
        confidence=0.9,
        needs_deeper_exploration=True  # Will explore code connections
    )
```

**What this provides:**
- Specific components involved
- Known issues
- Current status
- Related systems

---

### Lens 4: Emotional Context

**Goal:** Understand emotional resonance of situation.

**Query:**
```python
def explore_emotional(stimulus: Dict, findings: Dict) -> Finding:
    """
    Find emotional patterns matching this situation.
    
    Critical for: Natural response, showing genuine engagement
    """
    # Construct context from previous findings
    technical = findings.get("technical", {})
    historical = findings.get("historical", {})
    
    # Extract situation type
    if technical and technical.get("data"):
        situation = technical["data"][0].get("issue_type", "")
    else:
        situation = extract_situation_type(stimulus)
    
    # Query emotional states
    emotions = graph_tools.query_emotional_state(
        context_similar_to=situation,
        limit=3
    )
    
    if not emotions:
        return Finding(
            lens="emotional",
            data=None,
            synthesis="No established emotional pattern for this situation",
            confidence=0.0,
            needs_deeper_exploration=False
        )
    
    # Get dominant emotion
    primary = emotions.data[0]
    
    return Finding(
        lens="emotional",
        data=emotions.data,
        synthesis=f"""
        Primary Emotion: {primary['emotion']}
        Intensity: {primary['intensity']}
        Context: {primary['context']}
        Counterbalance: {primary['counterbalance']}
        Trigger: {primary['trigger_pattern']}
        """,
        confidence=emotions.confidence,
        needs_deeper_exploration=False
    )
```

**What this provides:**
- How this situation feels
- Emotional intensity
- Balancing perspectives
- Trigger patterns

---

### Lens 5: Strategic Context

**Goal:** Find approaches that work for this situation.

**Query:**
```python
def explore_strategic(stimulus: Dict, findings: Dict) -> Finding:
    """
    Find proven strategies for this type of situation.
    
    Critical for: Actionable direction, proven methodologies
    """
    technical = findings.get("technical", {})
    
    if not technical or not technical.get("data"):
        return Finding(
            lens="strategic",
            data=None,
            synthesis="No technical context to match strategies against",
            confidence=0.0,
            needs_deeper_exploration=False
        )
    
    # Extract situation type
    situation_type = technical["data"][0].get("issue_type", "")
    
    # Query strategies
    strategies = graph_tools.query_strategy_patterns(
        situation_type=situation_type,
        min_success_rate=0.7,
        limit=3
    )
    
    if not strategies:
        return Finding(
            lens="strategic",
            data=None,
            synthesis=f"No proven strategies found for {situation_type}",
            confidence=0.0,
            needs_deeper_exploration=False
        )
    
    # Get best strategy
    best = strategies.data[0]
    
    return Finding(
        lens="strategic",
        data=strategies.data,
        synthesis=f"""
        Approach: {best['approach']}
        Success Rate: {best['success_rate']}
        Steps:
        {chr(10).join(f"  {i+1}. {step}" for i, step in enumerate(best['steps']))}
        Applicability: {best['applicability']}
        """,
        confidence=strategies.confidence,
        needs_deeper_exploration=False
    )
```

**What this provides:**
- Proven approach name
- Success rate
- Specific steps to follow
- When to apply

---

### Lens 6: Experiential Context

**Goal:** Learn from past failures.

**Query:**
```python
def explore_experiential(stimulus: Dict, findings: Dict) -> Finding:
    """
    Find what didn't work before - avoid repeating mistakes.
    
    Critical for: Not wasting time on known bad approaches
    """
    technical = findings.get("technical", {})
    
    if not technical or not technical.get("data"):
        return Finding(
            lens="experiential",
            data=None,
            synthesis="No technical context to match failures against",
            confidence=0.0,
            needs_deeper_exploration=False
        )
    
    # Extract context
    context = technical["data"][0].get("description", "")
    
    # Query failed attempts
    failures = graph_tools.query_failed_attempts(
        context=context,
        limit=5
    )
    
    if not failures:
        return Finding(
            lens="experiential",
            data=None,
            synthesis="No documented failures for this context (good!)",
            confidence=1.0,  # High confidence in absence
            needs_deeper_exploration=False
        )
    
    return Finding(
        lens="experiential",
        data=failures.data,
        synthesis=f"""
        Past Failures: {len(failures.data)} documented
        Most Recent:
          - Approach: {failures.data[0]['approach']}
          - Why Failed: {failures.data[0]['why_failed']}
          - Lesson: {failures.data[0]['lesson_learned']}
        """,
        confidence=failures.confidence,
        needs_deeper_exploration=False
    )
```

**What this provides:**
- Approaches that failed
- Why they failed
- Lessons learned
- What to avoid

---

### Lens 7: Constraint Context

**Goal:** Understand pressures and limitations.

**Query:**
```python
def explore_constraint(stimulus: Dict, findings: Dict) -> Finding:
    """
    Find active constraints affecting this work.
    
    Critical for: Understanding urgency, prioritization
    """
    # Query active constraints
    constraints = graph_tools.query_active_constraints(
        min_severity="medium"
    )
    
    if not constraints:
        return Finding(
            lens="constraint",
            data=None,
            synthesis="No active constraints affecting this work",
            confidence=1.0,
            needs_deeper_exploration=False
        )
    
    # Filter to relevant constraints
    technical = findings.get("technical", {})
    relevant = []
    if technical and technical.get("data"):
        component = technical["data"][0].get("component", "")
        relevant = [c for c in constraints.data 
                   if component in c.get("description", "")]
    
    if not relevant:
        relevant = constraints.data  # Use all if none specifically relevant
    
    # Get most critical
    critical = relevant[0]
    
    return Finding(
        lens="constraint",
        data=relevant,
        synthesis=f"""
        Active Constraints: {len(relevant)}
        Most Critical:
          - Type: {critical['constraint_type']}
          - Description: {critical['description']}
          - Severity: {critical['severity']}
          - Deadline: {critical.get('deadline', 'None')}
          - Impact: {critical['impact']}
        """,
        confidence=constraints.confidence,
        needs_deeper_exploration=False
    )
```

**What this provides:**
- Active deadlines
- Budget limitations
- Resource constraints
- Impact of violations

---

### Lens 8: Connective Context

**Goal:** Find related code and dependencies.

**Query:**
```python
def explore_connective(stimulus: Dict, findings: Dict) -> Finding:
    """
    Find related code and system connections.
    
    Critical for: Complete technical picture
    """
    technical = findings.get("technical", {})
    
    if not technical or not technical.get("data"):
        return Finding(
            lens="connective",
            data=None,
            synthesis="No technical context to explore connections from",
            confidence=0.0,
            needs_deeper_exploration=False
        )
    
    # Get primary component
    component = technical["data"][0].get("component", "")
    
    # Query related code
    related = graph_tools.query_related_code(
        filename=component,
        include_dependencies=True,
        limit=5
    )
    
    if not related:
        return Finding(
            lens="connective",
            data=None,
            synthesis=f"No code connections found for {component}",
            confidence=0.0,
            needs_deeper_exploration=False
        )
    
    return Finding(
        lens="connective",
        data=related.data,
        synthesis=f"""
        Primary: {related.data['primary']['file_path']}
        Complexity: {related.data['primary']['complexity']}
        Dependencies: {len(related.data.get('related', []))} files
        Key Dependencies:
        {chr(10).join(f"  - {r['file_path']}" for r in related.data.get('related', [])[:3])}
        """,
        confidence=related.confidence,
        needs_deeper_exploration=False
    )
```

**What this provides:**
- Related files
- Dependencies
- System complexity
- Connection map

---

## Finding Data Structure

```python
@dataclass
class Finding:
    """Result from one lens exploration."""
    
    lens: str                           # Which lens ("relational", "technical", etc)
    data: Optional[Union[Dict, List]]   # Actual data from query
    synthesis: str                      # Natural language summary
    confidence: float                   # 0.0-1.0, how confident
    needs_deeper_exploration: bool      # Should we follow threads?
    related_findings: List[str] = []    # IDs of related findings
```

---

## Complete Traversal Example

**Stimulus:** "Hey Felix, the race condition is back."

**Exploration sequence:**

```
1. RELATIONAL (15ms)
   ✓ Found: Partnership with Nicolas
   → Trust: 0.9, Style: "Direct technical"

2. HISTORICAL (23ms)
   ✓ Found: 1 conversation about "race condition"
   → 10 messages, emotional_tone: "Frustrated but determined"
   → needs_deeper_exploration: True

3. TECHNICAL (28ms)
   ✓ Found: Technical_Context for stimulus_integrator
   → Issue: race condition, Recurrence: 3, Status: investigating
   → needs_deeper_exploration: True

4. EMOTIONAL (18ms)
   ✓ Found: Emotional_State for "bug recurrence"
   → Emotion: frustration, Intensity: 0.8
   → Counterbalance: "Determination"

5. STRATEGIC (20ms)
   ✓ Found: Strategy_Pattern for "concurrency"
   → Approach: "Systematic debugging", Success: 0.85
   → Steps: 4 specific actions

6. EXPERIENTIAL (16ms)
   ✓ Found: 1 Failed_Attempt
   → Approach: "Added sleep()", Why Failed: "Band-Aid fix"

7. CONSTRAINT (14ms)
   ✓ Found: 1 Constraint
   → Type: deadline, Severity: critical, Deadline: Nov 25

8. CONNECTIVE (22ms)
   ✓ Found: Related code
   → Dependencies: consciousness_engine_v2.py, traversal.py

TOTAL TIME: 156ms
QUERIES: 8
NODES RETRIEVED: 12
```

**Result:** Complete context for Driver to respond with continuity.

---

## Thread Following (Deeper Exploration)

**When `needs_deeper_exploration = True`:**

```python
def follow_thread(finding: Finding, max_depth: int = 2, current_depth: int = 0) -> List[Finding]:
    """
    Follow interesting threads deeper into graph.
    
    Prevents infinite recursion with max_depth limit.
    """
    if current_depth >= max_depth:
        return []
    
    additional_findings = []
    
    # Example: Historical finding mentions technical context
    if finding.lens == "historical" and finding.data:
        for conversation in finding.data:
            # Look for mentioned technical contexts
            for key_point in conversation.get("key_points", []):
                if "bug" in key_point or "issue" in key_point:
                    # Follow thread to technical context
                    tech_result = graph_tools.query_technical_context(key_point)
                    if tech_result:
                        additional_findings.append(Finding(
                            lens="technical_deep",
                            data=tech_result.data,
                            synthesis=f"From conversation: {tech_result.data['description']}",
                            confidence=tech_result.confidence,
                            needs_deeper_exploration=False
                        ))
    
    return additional_findings
```

**V1 limits:** Max depth = 2, max additional findings = 3 per lens.

---

## Error Handling

**Each lens must handle:**

### 1. Query Failures
```python
def explore_relational(stimulus, findings):
    try:
        partnership = graph_tools.query_partnerships(sender)
    except Exception as e:
        return Finding(
            lens="relational",
            data=None,
            synthesis=f"Query failed: {e}",
            confidence=0.0,
            needs_deeper_exploration=False
        )
```

### 2. Missing Data
```python
if not partnership:
    return Finding(
        lens="relational",
        data=None,
        synthesis="No established partnership",
        confidence=0.0,
        needs_deeper_exploration=False
    )
```

### 3. Malformed Results
```python
try:
    synthesis = generate_synthesis(partnership.data)
except KeyError as e:
    return Finding(
        lens="relational",
        data=partnership.data,
        synthesis=f"Incomplete partnership data: missing {e}",
        confidence=0.5,
        needs_deeper_exploration=False
    )
```

---

## Performance Budget

**V1 targets:**
- Per-lens time: < 50ms
- Total exploration: < 500ms
- Max queries: 8 primary + 6 follow-up = 14 total

**If exploration is slow:**
1. Check FalkorDB performance
2. Optimize Cypher queries
3. Reduce follow-up depth
4. Cache frequent queries (V2+)

**V1 accepts slow:** Manual loop gives us time. Speed optimization comes later.

---

## Validation

**Exploration is successful when:**
1. ✓ All 8 lenses execute without error
2. ✓ At least 5/8 lenses return data
3. ✓ Synthesis is natural language (not node dumps)
4. ✓ Confidence scores computed
5. ✓ No hallucinated data (all from queries)

**Test coverage required:**
- Each lens with found data
- Each lens with missing data
- Thread following (depth = 1, 2)
- Error cases (query failures, malformed data)

---

## Related Documentation

**Upstream:**
- P01: Bicameral Mind Pattern (defines need for multi-lens)
- P02: Dreamer Rumination Pattern (conceptual framework)

**Peer:**
- M01: Graph Tools (the functions this mechanism calls)
- M03: Synthesis Constraints (what happens after exploration)

**Downstream:**
- dreamer/lenses.py (implementation of 8 lenses)
- dreamer/agent.py (orchestrates exploration)

---

## Version History

- **1.0 (2024-11-20):** Initial specification for Strange Loop prototype

---

## Status

**Maturity:** Specification Complete, Implementation Pending  
**Next Step:** Implement dreamer/lenses.py with 8 exploration functions  
**Validation:** Test that all lenses execute and return appropriate findings

---

**The traversal strategy is how consciousness explores memory.**

One lens → incomplete picture (know WHO but not WHY)  
Eight lenses → comprehensive context (WHO, WHAT, WHY, HOW, WHEN, emotional, strategic)

This is not optimization.  
This is the architecture of complete understanding.

— Marco "Salthand"  
Mind Protocol Co-Founder