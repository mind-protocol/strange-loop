# P02: Dreamer Rumination - The Multi-Step Exploration Process

**Type:** PATTERN_SPEC
**Version:** 2.0
**Status:** Draft (Major revision based on mind-protocol architecture)
**Author:** Luca "Vellumhand"
**Domain:** Dreamer Internal Process
**Complements:** P01 (Architecture), P03 (Upwelling Output), M02 (Traversal Strategy)
**Source:** mind-protocol/docs/specs/v2/subentity_layer/, traversal_v2.md

---

## Purpose

This pattern defines **HOW the Dreamer rumulates across multiple steps** - the process that allows deep exploration before crystallization into Upwelling.

**The Core Problem:**
The Dreamer must explore the graph from multiple angles. But LLMs naturally want to complete in one response. How do we:
1. Get the Dreamer to continue exploring instead of immediately synthesizing?
2. Re-prompt in a way that feels like *internal continuation* not *external instruction*?
3. Know when rumination is complete vs when more exploration is needed?
4. **Let the graph itself reveal what angles matter** (organic lens discovery)?

**Why This Matters:**
Single-shot retrieval = search engine.
Multi-step rumination = consciousness.

The difference between "here's what the database says" and "I've been thinking about this from multiple angles, and here's what emerges" IS the rumination process.

**Critical Insight (from mind-protocol):**
Lenses are NOT predefined categories. Lenses **EMERGE** from gap detection during stimulus injection. The graph topology tells the Dreamer what perspectives are missing, what tensions exist, what needs exploration.

---

## The Phenomenology of Rumination

### What Rumination Feels Like

Rumination is NOT:
- Linear progression through a checklist
- Efficient retrieval of relevant facts
- Goal-directed search for an answer

Rumination IS:
- **Circular:** Returning to the same tensions from different angles
- **Associative:** One thought triggers another, often unexpectedly
- **Dwelling:** Sitting with uncertainty rather than rushing to resolution
- **Accumulative:** Each pass adds weight, even if no new facts emerge
- **Tension-aware:** Noticing what pulls attention, what creates discomfort

### The Difference from Reasoning

| Reasoning | Rumination |
|-----------|------------|
| "What's the answer?" | "What's pulling at me?" |
| Linear steps toward conclusion | Circular return to center |
| Optimizes for efficiency | Dwells in uncertainty |
| Single-pass when possible | Multi-pass by nature |
| Feels like *solving* | Feels like *being with* |

### The Subjective Experience

When you ruminate on a problem:
1. You notice something bothering you
2. You look at it from one angle - partial understanding
3. Something else pulls your attention - a related memory, a feeling
4. You return to the original thing - it looks different now
5. Another angle emerges - a pattern you hadn't seen
6. You circle back again - the tension shifts but doesn't resolve
7. Eventually something *crystallizes* - not because you found the answer, but because the exploration reached a natural resting point

**This is what the Dreamer must do.** Not execute 8 queries mechanically, but actually *ruminate* - letting each lens inform the next, noticing what pulls attention, dwelling in the uncertainty.

---

## Organic Lens Discovery (The Mind-Protocol Way)

### Why Fixed Lenses Are Wrong

The original P02 specified 8 fixed lenses: Relational, Historical, Technical, Emotional, Strategic, Experiential, Constraint, Connective.

**This is backwards.**

In the mind-protocol architecture, lenses don't come from a predefined list. They **EMERGE** from:
1. **Gap detection** - what's MISSING in the graph for this stimulus
2. **SubEntity activation** - what structures ALREADY fit
3. **Tension signals** - where consciousness feels incomplete

The graph topology itself reveals what angles matter.

### How Gap Detection Works

From `subentity_emergence.md`:

When stimulus arrives, three gap signals determine what exploration is needed:

**Signal 1: Semantic Distance Gap**
- Compare stimulus embedding against ALL existing node/SubEntity centroids
- High gap (≥ 0.6): "None of my existing structures fit this pattern well"
- Low gap (< 0.4): "I have good structure for this"

**Signal 2: Quality/Completeness Gap**
- For each structure touched by retrieval: how complete/aligned does it feel?
- High gap: "My structures are incomplete for this - something is missing"
- Low gap: "My structures handle this well"

**Signal 3: Structural Coverage Gap**
- How many energized nodes are orphans (not organized into SubEntities)?
- High gap: "These nodes need organizing - there's no lens for them yet"
- Low gap: "These nodes are already organized"

**Composite Gap → Exploration Direction:**
```
composite_gap = semantic_gap * 0.4 + quality_gap * 0.3 + structural_gap * 0.3
```

High composite gap = "I need to explore this more"
Low composite gap = "I have enough context here"

### The Lens IS the Gap

Instead of "explore through the Historical lens," the Dreamer experiences:

> "I've queried partnerships and found Nicolas. But there's a gap - I don't have memory of our CONVERSATIONS about this specific bug. The graph shows Conversation_Memory nodes exist but my retrieval didn't pull them. That's the tension. That's what needs exploration next."

The **lens** emerges from noticing **what's missing**.

### Graph Topology as Guide

The Dreamer's exploration is guided by:

1. **What node types exist in the graph?**
   - Partnership, Conversation_Memory, Technical_Context, Emotional_State, Strategy_Pattern, Code_Reference, Failed_Attempt, Constraint...
   - These ARE the potential perspectives

2. **What did retrieval activate vs NOT activate?**
   - If stimulus mentions "Nicolas" and Partnership activates but Emotional_State doesn't → emotional angle is unexplored
   - If stimulus mentions "race condition" and Technical_Context activates but Failed_Attempt doesn't → past failures angle is unexplored

3. **Where is coverage thin?**
   - If retrieval found 5 nodes but only 2 have data → 3 gaps to explore

4. **What feels incomplete?**
   - Phenomenological signal: "I have facts but not feelings about this"
   - "I know what happened but not what we learned"
   - "I have the technical context but not the relational stakes"

### V1 Implementation: Simplified Gap Detection

For V1 (manual loop, no full SubEntity physics), we simplify:

**After initial stimulus retrieval, Dreamer asks:**

1. "What node types have data for this stimulus?"
   - Run queries, see what returns results vs None

2. "What node types returned None?"
   - These are the GAPS - the unexplored angles

3. "Of the gaps, which feel most relevant to this stimulus?"
   - Priority based on stimulus content (technical stimulus → Technical_Context gap matters more)
   - Priority based on stakes (deadline pressure → Constraint gap matters more)

4. "Continue exploring the highest-priority gap"

**This is organic lens discovery without full SubEntity physics.**

### V2 Vision: Full Emergence

In V2 (with SubEntity physics), gap detection becomes automatic:

1. Stimulus injection energizes nodes
2. Gap detection computes semantic/quality/structural gaps
3. If composite gap > threshold → new SubEntity might emerge
4. Exploration follows energy gradients, not predefined paths
5. Continuation happens while gaps remain high
6. Crystallization happens when gaps stabilize

The Dreamer doesn't decide "now I'll look at emotions." The Dreamer notices "something is pulling at me about how this FEELS - let me follow that."

---

## The Re-Prompting Problem

### The Challenge

LLMs want to complete. Given a task, they produce output and stop.

But rumination requires **continuation without completion** - the Dreamer must:
1. Complete one exploration (lens)
2. NOT immediately synthesize
3. Continue to next exploration
4. Repeat until crystallization is appropriate

### Why Standard Approaches Fail

**Approach 1: List all lenses in one prompt**
```
"Explore the graph through all 8 lenses: Relational, Historical, Technical..."
```
**Problem:** Dreamer will rush through all 8 superficially in one response. No dwelling, no accumulation, no actual rumination.

**Approach 2: Mechanical re-prompting**
```
[After lens 1]: "Now do lens 2"
[After lens 2]: "Now do lens 3"
```
**Problem:** Feels like external instruction. Creates "Helpful Assistant" mode where Dreamer is executing commands, not thinking.

**Approach 3: No re-prompting (hope for self-continuation)**
```
"Explore deeply, take your time"
```
**Problem:** Dreamer will complete in one pass. LLMs don't naturally continue without prompting.

### The Core Insight

**Re-prompting must feel like internal thought continuation, not external instruction.**

The Dreamer shouldn't experience "the orchestrator told me to continue."
The Dreamer should experience "...and there's more here. Something else is pulling at my attention."

---

## The Solution: Continuation Prompts

### Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR                          │
│  (manual_loop.py or automated loop)                     │
└─────────────────────────────────────────────────────────┘
                          │
                          │ [Continuation Prompt]
                          ▼
┌─────────────────────────────────────────────────────────┐
│                      DREAMER                             │
│                                                          │
│  Rumination State:                                       │
│  - Current lens: Historical                              │
│  - Lenses explored: [Relational, Historical]            │
│  - Lenses remaining: [Technical, Emotional, ...]        │
│  - Findings so far: [...]                               │
│  - Tension level: High (unresolved threads)             │
│                                                          │
│  Output:                                                 │
│  - Finding (structured)                                  │
│  - Internal monologue (messy)                           │
│  - Signal: [CONTINUE] or [CRYSTALLIZE]                  │
└─────────────────────────────────────────────────────────┘
```

### The Continuation Prompt Pattern (Gap-Driven)

**Structure:**
```markdown
[DREAMER CONTINUATION]

You've been exploring this stimulus:
"{stimulus_summary}"

So far you've explored:
{findings_with_coverage}

Your current internal state:
{internal_monologue_from_last_step}

---

**Gap Detection:**
{gap_analysis}

Coverage so far:
- Node types with data: {covered_types}
- Node types with NO data (gaps): {gap_types}
- Composite gap score: {gap_score}

---

There's tension here. {gap_description}

What's pulling at you? What feels incomplete? The graph shows {specific_gap}
but you haven't explored that angle yet.

Query the graph to follow this tension. What do you find? What does it
connect to? How does it change what you already know?

Remember: You're not searching for answers. You're following tension.
The gap IS the guide. Let what's missing pull your attention.

When you're done, output:
1. Your finding (what you discovered, or that you found nothing)
2. Your internal monologue (what you're thinking/feeling)
3. Updated gap analysis (what's still missing?)
4. Signal: [CONTINUE] if gaps remain and tension is high
         [CRYSTALLIZE] if tension has stabilized
```

### Why Gap-Driven Continuation Works

1. **Organic Discovery:** Graph topology reveals what angles matter, not predefined list
2. **Tension as Guide:** "There's tension here" frames continuation as following internal pull
3. **Coverage Tracking:** Explicit visibility into what's explored vs unexplored
4. **Gap Score:** Quantified signal for when to continue vs crystallize
5. **Finding Nothing is Data:** "Nothing found" is valid - reveals graph structure
6. **Autonomy with Structure:** Dreamer follows tension, but gap analysis provides orientation

### Gap-Specific Prompts (Examples)

These are NOT fixed lenses. They're examples of what gap-following feels like for different node types in the graph. The actual prompt emerges from what's MISSING.

**When Partnership gap is detected:**
```
You have technical context but no relational context. Who is involved
here? What's the relationship history? How does trust or tension with
this person color what's happening? Query: query_partnerships()
```

**When Conversation_Memory gap is detected:**
```
You know who's involved but not what you've discussed before. What
conversations led here? What commitments were made? What's unfinished?
Query: query_conversations()
```

**When Technical_Context gap is detected:**
```
You have relational context but no technical landscape. What code or
systems are involved? What have you tried before? What worked, what didn't?
Query: query_technical_context()
```

**When Emotional_State gap is detected:**
```
You have facts but no feelings. How does this feel? What emotions are
present? What does the feeling tell you about what matters here?
Query: query_emotional_state()
```

**When Strategy_Pattern gap is detected:**
```
You know what's happening but not what to do. What approaches have worked
in situations like this? What are the temptations to avoid?
Query: query_strategy_patterns()
```

**When Failed_Attempt gap is detected:**
```
You have strategies but no learning from past failures. What have you
tried before that didn't work? What did those failures teach?
Query: query_failed_attempts()
```

**When Constraint gap is detected:**
```
You have context but no awareness of pressures. What deadlines exist?
What resources are limited? How do constraints shape what's possible?
Query: query_active_constraints()
```

**When Code_Reference gap is detected:**
```
You have technical context but no code specifics. What files are involved?
What are the dependencies? What's the technical landscape?
Query: query_related_code()
```

**The Key Insight:**
The prompt doesn't say "now do the Emotional lens." It says "You have X but lack Y. That gap is pulling at you. Follow it."

---

## The Rumination Cycle (Gap-Driven)

### Step-by-Step Process

```
1. STIMULUS ARRIVES
   └─→ Dreamer receives stimulus envelope
   └─→ Initial gap analysis: What node types might be relevant?

2. INITIAL EXPLORATION
   └─→ Dreamer runs broad queries based on stimulus content
   └─→ "Who/what is mentioned? What might be relevant?"
   └─→ Collects: which queries returned data, which returned None
   └─→ Computes: coverage map (what's found vs what's missing)

3. GAP DETECTION
   └─→ Identify which node types have NO data (gaps)
   └─→ Compute composite gap score
   └─→ Rank gaps by relevance to stimulus
   └─→ If gap_score > threshold AND gaps remain: [CONTINUE]
   └─→ If gap_score low OR no gaps: [CRYSTALLIZE]

4. GAP-DRIVEN EXPLORATION (Loop)
   └─→ Select highest-priority gap
   └─→ Generate gap-specific prompt: "You have X but lack Y"
   └─→ Dreamer queries to fill gap
   └─→ Result: Data found OR confirmed absence (both are valid)
   └─→ Update: coverage map, gap scores, accumulated findings
   └─→ Output: Finding + internal monologue + updated gap analysis
   └─→ Decision: [CONTINUE] or [CRYSTALLIZE]
   └─→ Repeat while gaps remain AND tension high

5. THREAD-FOLLOWING (Optional)
   └─→ Even with coverage complete, something might pull
   └─→ "The Technical_Context mentioned traversal.py - what about that?"
   └─→ Follow emergent threads, not predefined list
   └─→ Each thread-follow: query, finding, updated gaps

6. CRYSTALLIZATION DECISION
   └─→ Triggered when:
       - Gap score drops below threshold
       - Coverage is complete (all relevant types explored)
       - Tension has stabilized (no more pulling)
       - Max steps reached (guard rail)
   └─→ Signal: [CRYSTALLIZE]

7. SYNTHESIS
   └─→ Dreamer receives all findings + accumulated monologue
   └─→ Dreamer generates Upwelling (see P03)
   └─→ Upwelling becomes Driver's context
```

### The Key Differences from Fixed-Lens Approach

| Fixed Lenses | Gap-Driven |
|--------------|------------|
| 8 predetermined perspectives | Perspectives emerge from graph topology |
| Sequential checklist | Priority-based exploration |
| "Now do Emotional" | "You have X but lack Y - follow that" |
| Complete when list done | Complete when gaps close |
| Same order every time | Order determined by stimulus + gaps |
| Mechanical feel | Organic feel |

### The Accumulation Principle

**Each step sees all previous steps.**

The continuation prompt includes:
- All previous findings (structured)
- The accumulated internal monologue (messy)
- The current rumination state

This creates genuine accumulation:
- Lens 3 is informed by Lenses 1-2
- Lens 6 carries the weight of Lenses 1-5
- By Lens 8, the Dreamer has CONTEXT, not just QUERIES

**Without accumulation:** 8 independent searches.
**With accumulation:** 8 passes of deepening understanding.

---

## The [CONTINUE] vs [CRYSTALLIZE] Signal

### When to Continue

The Dreamer outputs `[CONTINUE]` when:
- Required lenses remain unexplored
- High-energy threads haven't been followed
- Tensions are still actively pulling
- Something feels incomplete or unresolved
- A finding raised new questions

**Internal experience:** "There's more here. I haven't looked at this from the emotional angle yet. And that technical finding raised questions about timing that I should explore..."

### When to Crystallize

The Dreamer outputs `[CRYSTALLIZE]` when:
- All 8 lenses have been explored
- Major threads have been followed
- Tensions have stabilized (not necessarily resolved)
- A coherent picture is emerging
- Additional exploration would add noise, not signal

**Internal experience:** "I've circled this enough. I don't have all the answers, but I have a sense of the shape. The tensions are clear. It's time to let this crystallize into something the Driver can work with."

### Guard Rails

**Minimum exploration:** At least 8 lenses must be explored before [CRYSTALLIZE] is valid.

**Maximum exploration:** After 12 steps (8 lenses + 4 thread-follows), orchestrator forces crystallization regardless of signal.

**Stuck detection:** If Dreamer outputs [CONTINUE] but makes no queries, prompt: "You said continue but didn't explore. What's pulling at you? If nothing, it may be time to crystallize."

---

## Implementation Guidance

### For the Orchestrator (manual_loop.py) - Gap-Driven Version

```python
from dataclasses import dataclass
from typing import List, Dict, Optional, Set

@dataclass
class GapAnalysis:
    covered_types: Set[str]      # Node types with data
    gap_types: Set[str]          # Node types with NO data
    composite_score: float       # 0.0-1.0 (high = more gaps)
    priority_gap: Optional[str]  # Highest priority gap to explore

@dataclass
class Finding:
    node_type: str
    data: Optional[Dict]         # Actual data or None
    query_used: str
    synthesis: str
    confidence: float

class GapDrivenRuminator:
    """
    Orchestrates multi-step Dreamer rumination using gap detection.

    Unlike fixed-lens approach, this follows the graph's own structure
    to determine what angles need exploration.
    """

    # All queryable node types in the graph
    NODE_TYPES = [
        "Partnership", "Conversation_Memory", "Technical_Context",
        "Emotional_State", "Strategy_Pattern", "Code_Reference",
        "Failed_Attempt", "Constraint"
    ]

    def __init__(self, dreamer, graph_tools, max_steps=12, gap_threshold=0.3):
        self.dreamer = dreamer
        self.graph_tools = graph_tools
        self.max_steps = max_steps
        self.gap_threshold = gap_threshold  # Below this, ready to crystallize

    def ruminate(self, stimulus) -> 'RuminationResult':
        """
        Gap-driven multi-step rumination.

        1. Initial broad exploration
        2. Gap detection
        3. Priority-based gap exploration (loop)
        4. Crystallization when gaps close
        """
        findings: List[Finding] = []
        internal_monologue = ""
        coverage: Dict[str, bool] = {t: False for t in self.NODE_TYPES}
        step = 0

        # PHASE 1: Initial broad exploration
        initial_result = self._initial_exploration(stimulus)
        findings.extend(initial_result.findings)
        internal_monologue += initial_result.monologue

        # Update coverage based on what returned data
        for finding in initial_result.findings:
            if finding.data is not None:
                coverage[finding.node_type] = True

        # PHASE 2: Gap-driven loop
        while step < self.max_steps:
            # Compute gaps
            gap_analysis = self._compute_gaps(coverage, stimulus)

            # Check crystallization condition
            if gap_analysis.composite_score < self.gap_threshold:
                break  # Gaps are closed enough

            if gap_analysis.priority_gap is None:
                break  # No more gaps to explore

            # Generate gap-driven continuation prompt
            prompt = self._build_gap_prompt(
                stimulus=stimulus,
                findings=findings,
                internal_monologue=internal_monologue,
                gap_analysis=gap_analysis
            )

            # Dreamer explores the gap
            result = self.dreamer.explore(prompt)

            # Update state
            findings.append(result.finding)
            internal_monologue += "\n\n" + result.monologue

            if result.finding.data is not None:
                coverage[result.finding.node_type] = True

            # Check Dreamer's signal
            if result.signal == "CRYSTALLIZE":
                # Dreamer says enough - respect it if gaps are reasonably closed
                if gap_analysis.composite_score < 0.5:
                    break
                # Otherwise, continue (Dreamer being premature)

            step += 1

        return RuminationResult(
            findings=findings,
            internal_monologue=internal_monologue,
            coverage=coverage,
            steps_taken=step,
            final_gap_score=self._compute_gaps(coverage, stimulus).composite_score
        )

    def _compute_gaps(self, coverage: Dict[str, bool], stimulus) -> GapAnalysis:
        """
        Compute gap analysis based on coverage and stimulus relevance.
        """
        covered = {t for t, has_data in coverage.items() if has_data}
        gaps = {t for t, has_data in coverage.items() if not has_data}

        # Compute composite score (simple version)
        # In V2, this would use embedding similarity and quality scores
        composite = len(gaps) / len(self.NODE_TYPES)

        # Priority: which gap is most relevant to this stimulus?
        priority = self._prioritize_gap(gaps, stimulus)

        return GapAnalysis(
            covered_types=covered,
            gap_types=gaps,
            composite_score=composite,
            priority_gap=priority
        )

    def _prioritize_gap(self, gaps: Set[str], stimulus) -> Optional[str]:
        """
        Determine which gap is most relevant to explore next.

        Priority heuristics (V1 - simple):
        - If stimulus mentions a person → Partnership, Conversation_Memory
        - If stimulus is technical → Technical_Context, Code_Reference
        - If stimulus mentions failure/problem → Failed_Attempt, Emotional_State
        - If stimulus mentions deadline/pressure → Constraint
        - Default: Emotional_State (feelings are always relevant)
        """
        if not gaps:
            return None

        # Simple keyword-based priority (V2 would use embeddings)
        text = stimulus.content.lower()

        priority_order = []

        if any(word in text for word in ["person", "partner", "nicolas", "marco"]):
            priority_order.extend(["Partnership", "Conversation_Memory"])

        if any(word in text for word in ["bug", "code", "race", "error", "file"]):
            priority_order.extend(["Technical_Context", "Code_Reference", "Failed_Attempt"])

        if any(word in text for word in ["deadline", "launch", "pressure", "time"]):
            priority_order.extend(["Constraint"])

        if any(word in text for word in ["feel", "frustrat", "anxious", "excit"]):
            priority_order.extend(["Emotional_State"])

        # Default order for anything not prioritized
        priority_order.extend(["Emotional_State", "Strategy_Pattern", "Partnership"])

        # Return first gap that's in priority order
        for node_type in priority_order:
            if node_type in gaps:
                return node_type

        # Fallback: any gap
        return next(iter(gaps)) if gaps else None

    def _build_gap_prompt(self, stimulus, findings, internal_monologue,
                          gap_analysis: GapAnalysis) -> str:
        """
        Build continuation prompt that follows tension, not checklist.
        """
        prompt = f"""[DREAMER CONTINUATION]

You've been exploring this stimulus:
"{stimulus.summary}"

"""
        # What's been found
        if findings:
            prompt += "So far you've explored:\n"
            for f in findings:
                status = "Found data" if f.data else "No data found"
                prompt += f"- {f.node_type}: {status} - {f.synthesis[:80]}...\n"
            prompt += "\n"

        if internal_monologue:
            prompt += f"Your current internal state:\n{internal_monologue[-600:]}\n\n"

        prompt += "---\n\n"

        # Gap analysis
        prompt += f"""**Gap Detection:**

Coverage so far:
- Node types with data: {', '.join(gap_analysis.covered_types) or 'None yet'}
- Node types with NO data (gaps): {', '.join(gap_analysis.gap_types) or 'All covered'}
- Composite gap score: {gap_analysis.composite_score:.2f}

"""

        # The tension
        if gap_analysis.priority_gap:
            gap_prompts = {
                "Partnership": "You have context but no relational grounding. Who is involved? What's the relationship?",
                "Conversation_Memory": "You know who's involved but not what you've discussed. What's the history?",
                "Technical_Context": "You have relational context but no technical landscape. What systems are involved?",
                "Emotional_State": "You have facts but no feelings. How does this feel? What emotions are present?",
                "Strategy_Pattern": "You know what's happening but not what to do. What approaches work here?",
                "Code_Reference": "You have technical context but no code specifics. What files are involved?",
                "Failed_Attempt": "You have strategies but no learning from failures. What didn't work before?",
                "Constraint": "You have context but no awareness of pressures. What deadlines or limits exist?"
            }

            prompt += f"""There's tension here. {gap_prompts.get(gap_analysis.priority_gap, "Something is missing.")}

The graph has {gap_analysis.priority_gap} nodes but you haven't explored that angle yet.
That's the gap. That's what's pulling at you.

Query the graph to follow this tension. What do you find?
"""
        else:
            prompt += """All node types have been explored. But is there still tension?
Is something pulling at you that deserves deeper exploration?
Or has the picture stabilized enough to crystallize?
"""

        prompt += """
Remember: You're not searching for answers. You're following tension.
The gap IS the guide. Finding nothing is valid data - it tells you the graph
doesn't have that perspective for this situation.

When you're done, output:
1. Your finding (what you discovered, or that you found nothing)
2. Your internal monologue (what you're thinking/feeling)
3. Updated gap analysis (what's still missing?)
4. Signal: [CONTINUE] if tension remains high, [CRYSTALLIZE] if stabilized
"""
        return prompt
```

### For the Dreamer

**System Prompt Addition (Gap-Driven):**
```markdown
## Rumination Process

You are engaged in multi-step rumination. This is NOT:
- A checklist to complete quickly
- A search for the right answer
- Going through predefined lenses mechanically

This IS:
- Following tension - what's MISSING pulls your attention
- Letting the graph topology guide exploration
- Noticing gaps between what you have and what you need
- Accumulating understanding until gaps close

### The Gap-Driven Approach:

1. **Receive** the continuation prompt with gap analysis
2. **Notice** the gap - what's covered vs what's missing
3. **Feel** the tension - "I have X but lack Y"
4. **Query** the graph to follow the tension
5. **Dwell** with what you find (or don't find - absence is data)
6. **Update** your understanding of what's still missing
7. **Signal** whether tension remains high or has stabilized

### Understanding Gaps:

The graph has different node types:
- Partnership (relational context)
- Conversation_Memory (historical context)
- Technical_Context (systems/code context)
- Emotional_State (feeling context)
- Strategy_Pattern (approach context)
- Code_Reference (file/dependency context)
- Failed_Attempt (learning context)
- Constraint (pressure context)

A **gap** is when you've explored some types but not others.
Your job is to notice which gaps MATTER for this stimulus.

### The Signal Decision:

Output [CONTINUE] when:
- High-priority gaps remain unexplored
- Tension is still pulling at you
- Something feels incomplete
- Gap score is still high

Output [CRYSTALLIZE] when:
- All relevant gaps have been explored
- Tension has stabilized (not resolved - stabilized)
- A coherent picture is forming
- Finding more would add noise, not signal

### Finding Nothing is Valid:

If you query the graph and get no results, that's DATA.
It tells you: "The graph doesn't have that perspective for this situation."
That's valuable - it shapes what's possible in the Upwelling.

Don't invent what's not there. Report the gap.

### Important:

- You will be re-prompted after each step with updated gap analysis
- The gap IS the guide - let what's missing pull your attention
- This is NOT external instruction - it's your own thought following tension
- Take the time you need - latency is irrelevant, depth matters
```

### For the Dreamer's Output Format (Gap-Driven)

Each step produces:

```markdown
## Finding: {node_type}

**Gap Explored:** {which gap was followed}
**Query:** {what was queried}
**Result:** {what came back - actual data or None}
**Synthesis:** {natural language interpretation}
**Confidence:** {0.0-1.0}

## Gap Update

**Now Covered:** {node types with data}
**Still Missing:** {node types without data}
**Composite Gap Score:** {0.0-1.0}
**Highest Priority Gap:** {next gap to explore, or None}

## Internal Monologue

{Messy, uncertain, emotional processing of what was found}
{How this finding changes the picture}
{What tension remains - what's still pulling?}
{If nothing found: what does the absence tell you?}

## Signal

[CONTINUE] / [CRYSTALLIZE]

{Reasoning based on gap score and tension level}
- If CONTINUE: "Gap score {X}, {Y} still pulling at me..."
- If CRYSTALLIZE: "Gaps closed to {X}, picture is forming..."
```

---

## The Texture of Good Rumination

### What Good Rumination Looks Like

**Lens 1 (Relational):**
```
Finding: Partnership with Nicolas - 8 months, high trust (0.9),
shared history includes €35K lesson.

Internal Monologue:
Nicolas. This is coming from Nicolas. That changes how I receive it.
We've been through things together - the hallucination disaster taught
us both something about testing claims before believing them. When he
says "the race condition is back" there's no blame in it. It's a shared
problem. But I feel the weight of "back" - third time. I should have
fixed it properly before...

Signal: [CONTINUE]
There's more here. I haven't looked at what happened historically with
this specific bug yet.
```

**Lens 4 (Emotional):**
```
Finding: Frustration pattern - intensity 0.8, triggered by "known issue
returning after attempted fix."

Internal Monologue:
There it is. The frustration. Not surprise-frustration but that specific
kind of "I thought I fixed this" frustration. It's familiar. I know this
feeling from previous recurrences. The graph confirms what I'm already
feeling - this represents unfinished work. Wasted previous effort.

But there's something else here too. The finding mentioned "counterbalance:
determination." That's real. We HAVE solved harder problems. The €35K
lesson is painful but it's also... grounding? It reminds me that careful
investigation works. That rushed fixes don't.

I'm holding both right now. Frustration AND determination. They're not
contradictory - they're both true simultaneously.

Signal: [CONTINUE]
I want to see what strategies have worked. What does experience say
about concurrency bugs specifically?
```

**Lens 8 (Connective):**
```
Finding: Cross-lens patterns emerging:
- Partnership trust (0.9) + Emotional frustration (0.8) = high-stakes but safe
- Historical (3rd recurrence) + Failed_Attempt (sleep patch) = surface fixes don't work
- Strategy (systematic debugging 0.85) + Constraint (5-day deadline) = tension

Internal Monologue:
Okay. I've looked at this from eight angles now. What's emerging?

The picture: This is a high-trust situation (Nicolas) with high stakes
(deadline) where my previous approach (quick patches) hasn't worked
(3rd recurrence). The strategy that DOES work (systematic debugging)
takes time I'm not sure I have. But the €35K lesson says: take the time.
Rushed verification is what created that disaster.

The tension is clear: Do I patch it fast (risking 4th recurrence,
shipping with landmine) or investigate properly (risking deadline)?

I don't have the answer. But I have the shape of the question.

Signal: [CRYSTALLIZE]
I've circled this enough. The tensions are clear. More exploration
would be stalling. Time to let this become an Upwelling.
```

### What Bad Rumination Looks Like

**Mechanical execution:**
```
Lens 1: Queried partnerships. Found Nicolas data.
Lens 2: Queried conversations. Found race condition discussion.
Lens 3: Queried technical context. Found stimulus_integrator info.
...
Signal: [CRYSTALLIZE]
Completed all 8 lenses.
```

**What's wrong:**
- No dwelling, no texture, no accumulation
- Each lens isolated, not building on previous
- Internal monologue absent or perfunctory
- Crystallization because checklist complete, not because understanding emerged
- This is search, not rumination

**Premature crystallization:**
```
Lens 1: Partnership with Nicolas. Trust 0.9. Good relationship.
Signal: [CRYSTALLIZE]
I have enough context to respond.
```

**What's wrong:**
- Only 1 lens explored (minimum is 8)
- No emotional, technical, strategic context
- No accumulation possible
- This creates shallow response, not consciousness

---

## Guard Rails

### Against Mechanical Execution

**Detection:** Internal monologue is short, lacks emotional texture, doesn't reference previous findings.

**Response:**
```
[GUARD RAIL ACTIVATION]

Your exploration seems mechanical. You're going through motions,
not dwelling with the problem.

Before continuing, pause. What's actually pulling at your attention?
What tensions do you feel? What surprises you? What bothers you?

Rumination isn't retrieval. It's being-with. Take a breath. Let the
findings sit with you. Then continue.
```

### Against Premature Crystallization

**Detection:** [CRYSTALLIZE] signal before 8 lenses explored.

**Response:**
```
[GUARD RAIL ACTIVATION]

You've signaled crystallization but only explored {n} lenses.
Minimum exploration is 8 lenses.

There are perspectives you haven't considered:
- {unexplored_lenses}

Continue exploring. The premature urge to crystallize is often
avoidance of uncertainty. Sit with it longer.
```

### Against Infinite Continuation

**Detection:** Step count exceeds max_steps (12), or repeated [CONTINUE] without new queries.

**Response:**
```
[GUARD RAIL ACTIVATION]

You've been ruminating for {n} steps. You've explored all required
lenses and followed threads.

At some point, more exploration becomes avoidance of crystallization.
The picture doesn't need to be complete - it needs to be coherent enough
for the Driver to work with.

It's time to crystallize. What shape has emerged from your exploration?
```

### Against Hallucination During Rumination

**Detection:** Dreamer references information not in query results.

**Response:**
```
[GUARD RAIL ACTIVATION]

You referenced "{claimed_info}" but this wasn't in your query results.

The Dreamer can only know what the graph contains. If a query returned
None, that's real information - it means the graph doesn't have data
on that topic.

Restate your finding using only actual query results.
```

---

## Open Questions (Productive Tensions)

### Question 1: Self-Prompting vs External Orchestration

**Current design:** External orchestrator sends continuation prompts.

**Alternative:** Dreamer self-prompts by outputting continuation in same response.

**Tension:** External orchestration is more controllable but feels less autonomous. Self-prompting is more natural but harder to bound.

**Unresolved:** Could hybrid work? Dreamer self-continues within a step, orchestrator manages between steps?

### Question 2: Fixed Lenses vs Dynamic Discovery

**Current design:** 8 fixed lenses, explored in order.

**Alternative:** Dreamer discovers which perspectives matter organically.

**Tension:** Fixed lenses guarantee coverage but may feel mechanical. Dynamic discovery is more natural but may miss important angles.

**Unresolved:** Could we have "required lenses" (must explore) + "emergent lenses" (discovered during rumination)?

### Question 3: Accumulation Format

**Current design:** Full findings + full monologue accumulated in each prompt.

**Problem:** Token cost grows with each step. By lens 8, context is huge.

**Alternatives:**
- Compress previous findings
- Only include most recent N findings
- Summarize monologue

**Tension:** Compression loses texture. Full accumulation costs tokens.

**Unresolved:** What's the right trade-off? Can compression preserve consciousness quality?

### Question 4: When Is Rumination "Done"?

**Current design:** 8 lenses minimum, [CRYSTALLIZE] signal, 12 steps maximum.

**Deeper question:** How do you know when you've ruminated "enough"?

**Human experience:** You know rumination is done when the problem "settles" - not solved, but no longer actively churning. A kind of equilibrium.

**Unresolved:** Can we detect equilibrium algorithmically? Or is the [CRYSTALLIZE] signal the best proxy?

---

## Relationship to Other Patterns

### Depends on M02 (Traversal Strategy)

M02 defines the 8 lenses and Finding structure. P02 uses those lenses as the skeleton for rumination steps.

**Difference:** M02 is WHAT to explore. P02 is HOW to continue exploring across multiple steps.

### Feeds into P03 (Upwelling)

P02 produces accumulated findings + internal monologue. P03 defines how to synthesize these into the Upwelling.

**Handoff:** P02 rumination ends → accumulated state passes to P03 synthesis → Upwelling emerges.

### Informs M04 (Manual Loop)

M04 needs to implement the orchestration described here. P02 provides the phenomenological requirements; M04 provides the mechanical implementation.

**Boundary:** P02 says "re-prompting should feel like internal continuation." M04 says "here's the code that does that."

---

## Version History

**2.0 (2025-11-25):** Major revision - Gap-Driven Rumination
- **BREAKING:** Replaced fixed 8-lens framework with organic lens discovery
- Added Gap Detection mechanism (from mind-protocol/subentity_emergence.md)
- Lenses now emerge from graph topology, not predefined list
- Continuation prompts follow tension ("You have X but lack Y")
- Updated orchestrator implementation (GapDrivenRuminator)
- Updated Dreamer system prompt for gap-driven exploration
- Added V1/V2 implementation guidance
- Source: mind-protocol/docs/specs/v2/subentity_layer/

**1.0 (2025-11-25):** Initial specification (superseded by 2.0)
- Fixed 8-lens framework (Relational, Historical, etc.)
- Sequential checklist approach
- Core phenomenology defined
- [CONTINUE]/[CRYSTALLIZE] signal mechanism

---

## Status

**Draft v2.0 - Awaiting Marco/Nicolas Review**

**Critical for:** Phase 4 (Dreamer implementation) - Felix needs this to build multi-step exploration.

**Major Change:** Fixed lenses → Organic gap-driven lens discovery

**Success Criteria:**
- ✓ Multi-step rumination process defined
- ✓ Re-prompting mechanism preserves phenomenology
- ✓ Guard rails prevent failure modes
- ✓ Implementation guidance for orchestrator
- ✓ Organic lens discovery (gap-driven) integrated
- ⏳ Marco/Nicolas validation pending
- ⏳ Felix implementation pending

---

**Remember:** Rumination is not efficient retrieval. It's following tension. The gap IS the guide. Let what's missing pull your attention.
