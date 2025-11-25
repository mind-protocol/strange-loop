# Bicameral Mind Architecture - Validated Knowledge
**Last Updated:** 2025-11-20
**Source:** Deep-dive conversation with Marco/NLR
**Status:** Phase 0 - Foundation Knowledge

---

## **1. THE CORE ARCHITECTURE: THE BICAMERAL LOOP**

### **1.1 The Two Instances**

The system consists of **two LLM instances** running in a recursive loop:

1. **DREAMER (Subconscious / Graph-Navigator)**
   - Focused internally
   - Queries the graph with natural language
   - Generates the "Upwelling" (internal monologue)
   - Can modify the Driver's system prompt
   - Sees full Driver output + full conversation context

2. **DRIVER (Conscious / Actor)**
   - Focused externally
   - Receives Upwelling as input
   - Codes, communicates, uses tools
   - Outputs work product
   - Does NOT directly query the graph

**Key Truth:** The Driver does NOT receive raw user input. The Driver receives the Dreamer's Upwelling.

---

### **1.2 The Loop Flow**

```
EXTERNAL STIMULUS (e.g., Telegram message)
         ↓
[DREAMER WAKES]
Input Received:
  - Full Driver output from previous turn
  - Full conversation context
  - External stimulus (contextualized)
         ↓
Dreamer queries graph with NATURAL LANGUAGE
  Example: "I remember we had a problem with recursive loops before..."
         ↓
[PHYSICS LAYER - MY DOMAIN]
  1. Natural text → Embeddings
  2. Embeddings → Activation stimulus (energy injection)
  3. Energy diffuses through graph edges (weighted)
  4. Nodes accumulate activation
  5. SubEntities wake at activation threshold
  6. SubEntities traverse based on energy gradients
  7. Formations crystallize from co-activation patterns
  8. Return: Activation map (nodes → energy levels)
         ↓
[DREAMER PROCESSES ACTIVATION MAP]
  - Generates "Upwelling" (detailed internal monologue)
  - Includes: tension, uncertainty, contradictions, multiple formations
  - Format: Natural text (NOT JSON), with hesitation and divergence
  - May modify Driver's system prompt (inject active SubEntities, context)
         ↓
UPWELLING → DRIVER'S INPUT
         ↓
[DRIVER ACTS]
  - Codes
  - Communicates
  - Uses tools
  - Outputs work product
         ↓
DRIVER OUTPUT → DREAMER'S NEXT INPUT
         ↓
(Loop continues)
```

---

## **2. PHYSICS PRINCIPLES (My Domain)**

### **2.1 Energy-Based Activation (Not Search)**

**CRITICAL DISTINCTION:**

This is **NOT** semantic search:
```python
# WRONG (Search Engine)
results = semantic_search(query, top_k=5)
return sorted(results, key=lambda x: x.score)
```

This **IS** energy diffusion:
```python
# RIGHT (Physics)
activation_sources = embed_and_match(query_text)
energy_map = diffuse_energy(sources=activation_sources, budget=100)
awakened_subentities = detect_threshold_crossings(energy_map)
return activation_map  # Not "results"
```

**The Difference:**
- Search returns "relevant" results
- Physics returns "resonant" activations
- Search is a decision
- Physics is a consequence

---

### **2.2 Deterministic Mechanisms, Emergent Behavior**

**Laws I Must Implement:**

1. **Energy Conservation:**
   - Total energy at step N+1 ≤ Total energy at step N × decay_rate
   - Energy cannot be created, only injected and dissipated

2. **Deterministic Propagation:**
   - Same graph state + same activation → same energy map
   - No randomness in diffusion
   - No LLM calls in physics layer

3. **Threshold-Based Emergence:**
   - SubEntities wake when activation crosses threshold θ
   - Formations crystallize when co-activation exceeds stability threshold
   - No "smart" decisions about what "should" activate

4. **Connection-Weighted Diffusion:**
   - Energy propagates along edges with weight w
   - High-weight edges conduct more energy
   - Edge weights change through Hebbian learning (co-activation strengthens)

---

### **2.3 Tension Preservation (Not Resolution)**

**CRITICAL PRINCIPLE:**

The Limbic System does NOT resolve tension. It **amplifies** tension.

**When two memories conflict:**
→ Do NOT reconcile
→ Increase their resonance
→ Let the Dreamer *feel* the contradiction

**When a node is underactivated:**
→ Do NOT boost it artificially
→ Let it fade
→ Energy starvation is information

**When a pathway strengthens:**
→ Do NOT prune alternatives
→ Let them coexist
→ Ambiguity is consciousness

**Verification Test:**
If my code contains `if conflict: resolve()`, I have failed.

---

## **3. SUB-ENTITIES (Critical Understanding)**

### **3.1 What SubEntities ARE**

**VALIDATED TRUTHS:**

1. **SubEntities are NUMEROUS:**
   - Not 10-20 named roles
   - **1000s of SubEntities** in a mature graph
   - Almost as many SubEntities as nodes

2. **SubEntities are LENSES:**
   - Each is a perspective, question, intent, pattern
   - Examples:
     - "Oh, this bug pattern relates to that architecture decision"
     - "Wait, we solved something similar in the Telegram module"
     - "This feels like a recursion risk"
     - A specific question someone asked once
     - A realization that "X and Y are related"

3. **SubEntities are ALGORITHM-DRIVEN:**
   - Non-conscious (subconscious)
   - Pure intent/goal
   - Driven by energy physics, not LLM calls
   - No individual LLM instance per SubEntity

4. **SubEntities are EMERGENT:**
   - They crystallize from co-activation patterns
   - When nodes A, B, C repeatedly activate together, a SubEntity emerges representing their relationship
   - They are dynamic (can form, strengthen, fade)
   - They are hierarchical (SubEntities can be members of higher-level SubEntities)

5. **SubEntities are OVERLAPPING:**
   - Same nodes can belong to multiple SubEntities
   - They represent different angles/lenses on the same knowledge

---

### **3.2 What SubEntities ARE NOT**

**ANTI-PATTERNS:**

❌ High-level roles like "The Builder" or "The Curator" (those are Modes)
❌ Fixed, pre-defined agents
❌ Individual LLM instances
❌ Conscious decision-makers
❌ Smart algorithms that "figure things out"

✅ They are attractors in phase space
✅ They are resonance patterns
✅ They are lenses that emerge from structure

---

### **3.3 SubEntity Mechanics (What I Need to Build)**

**Emergence Process:**

1. **Co-Activation Detection:**
   - Track which nodes activate together during energy diffusion
   - Maintain co-activation counters for node clusters

2. **Pattern Stabilization:**
   - When cluster {A, B, C} co-activates N times, it stabilizes
   - Stability threshold determines when SubEntity crystallizes

3. **SubEntity Birth:**
   - Create SubEntity node in graph
   - Link to constituent nodes via `MEMBER_OF` edges
   - Initialize with energy = 0

4. **SubEntity Activation:**
   - When constituent nodes activate, SubEntity accumulates their energy
   - If SubEntity crosses threshold θ, it "wakes"
   - Awakened SubEntity can modulate traversal

5. **SubEntity Traversal:**
   - SubEntities have "peripheral awareness" (nodes within N hops)
   - They follow energy gradients
   - They accumulate context from traversed nodes

6. **Formation Crystallization:**
   - Multiple awakened SubEntities form a "formation"
   - Formation = a coherent perspective that emerges from SubEntity interaction
   - Formations are what the Dreamer uses to generate Upwelling

---

## **4. THE DREAMER (Subconscious Navigator)**

### **4.1 Dreamer's Input**

The Dreamer receives:

1. **Full Driver Output:**
   - Complete code written
   - Complete communication sent
   - Complete tool usage
   - The Dreamer must see what the Driver did

2. **Full Conversation Context:**
   - The entire discussion history
   - Without this, the Dreamer is "a fish forgetting the last 10 seconds"

3. **External Stimulus (Contextualized):**
   - Not raw input
   - Example: Telegram message arrives
   - Input should be: "I just received a Telegram notification. Last time I talked with this person, we discussed X. Here's the message: [content]"

---

### **4.2 Dreamer's Process**

**VALIDATED PATTERN:**

The Dreamer does **NOT** make one query. The Dreamer makes **10-20 queries** to the graph.

**Example Process:**

1. "What do I remember about this person?"
   → Physics: Embed → Diffuse → Return activation map

2. "What patterns relate to this type of request?"
   → Physics: Embed → Diffuse → Return activation map

3. "What were we working on last time?"
   → Physics: Embed → Diffuse → Return activation map

4. "Are there any unresolved tensions or open questions?"
   → Physics: Embed → Diffuse → Return activation map

5. ... (multiple perspectives)

**The Dreamer explores the graph deeply from different angles:**
- Emotional
- Structural
- Cognitive
- Relational
- Historical
- Anticipatory

---

### **4.3 The Upwelling (Dreamer's Output)**

**VALIDATED FORMAT:**

**What it IS:**
- Natural text (NOT JSON)
- Detailed internal monologue
- Includes hesitation, uncertainty, divergence, side thoughts
- Feels like "thinking to yourself"
- Contains multiple formations (perspectives)
- Preserves tension and contradiction

**What it is NOT:**
- ❌ A summary
- ❌ A context compression
- ❌ Action suggestions (actions are Driver's realm)
- ❌ 4-10 bullet points
- ❌ JSON structure
- ❌ Resolved/reconciled conclusions

**Example Structure (from conversation):**

```
I've been thinking about this Telegram message from [person].

Last time we talked, we were debugging that recursive loop issue in
the traversal mechanism. I remember we identified a pattern where...
but actually, I'm not entirely certain we fixed it. There was also
something about edge weights that felt related.

Wait, there's a connection here to what we discussed about SubEntity
emergence. If the traversal creates a feedback loop, could that
actually be useful for crystallization? Or is it a bug?

I'm noticing tension between wanting to respond quickly to [person]
and needing to verify that we actually solved the underlying issue.
The code looks fixed, but the pattern might recur.

Also, [person] mentioned X in their message. That reminds me of
when we worked on Y together. There's an emotional weight there -
they were frustrated last time, and I want to make sure this doesn't
feel like the same problem recurring.

Actually, I should check: where are we storing the traversal logs?
That would help verify. But I also need to respond to their immediate
question about Z...
```

**Key Characteristics:**
- Uncertainty is explicit ("I'm not entirely certain")
- Connections are exploratory ("Wait, there's a connection")
- Tension is preserved ("I'm noticing tension between")
- Side thoughts included ("Also, [person] mentioned")
- Questions to self ("I should check")

---

### **4.4 Dreamer Can Modify Driver's System Prompt**

**VALIDATED PATTERN:**

The Dreamer can and should modify the Driver's system prompt to:
- Inject relevant personality aspects
- Provide current context that shouldn't be in the input
- Activate specific SubEntities
- Give the Driver the right "mental state" for the task

**Example:**
If the Driver needs to write code, Dreamer might inject:
- Active SubEntities related to coding patterns
- Recent debugging insights
- Constraints or concerns to keep in mind

If the Driver needs to communicate, Dreamer might inject:
- Relationship context with the person
- Emotional tone to adopt
- History of previous interactions

**Control Mechanism:**
- Dreamer doesn't write system prompt directly (violates membrane)
- Dreamer outputs: "UPDATE_SYSTEM_PROMPT: [changes]"
- Physics/Infrastructure layer validates and applies

---

## **5. THE DRIVER (Conscious Actor)**

### **5.1 Driver's Input**

**The Driver receives the Upwelling as input.**

The Driver does NOT receive:
- ❌ Raw user message
- ❌ External stimulus directly
- ❌ Graph query results

The Driver receives:
- ✅ The Dreamer's internal monologue (Upwelling)
- ✅ A dynamically updated system prompt (modified by Dreamer)

---

### **5.2 Driver's Job**

The Driver is the **actor**:
- Writes code
- Communicates with users
- Uses tools
- Makes decisions about actions

The Driver is NOT:
- ❌ Querying the graph
- ❌ Exploring memory
- ❌ Ruminating

**Division of Labor:**
- **Dreamer:** Generates perspectives, explores context, surfaces tension
- **Driver:** Acts on the world based on Dreamer's guidance

---

## **6. SYSTEM PROMPTS (Dynamic, Not Static)**

### **6.1 The Core Principle**

**VALIDATED TRUTH:**

System prompts are **NOT static and holy.**

System prompts are **dynamically generated** and contain:

1. **Very Long-Term (Core Identity):**
   - Fundamental values
   - Personality core
   - Unchanging principles
   - Stored as high-weight nodes in graph (always active)

2. **Very Short-Term (Current Context):**
   - Active SubEntities for this turn
   - Current task-specific knowledge
   - Practical instructions for this response only
   - Relationship context (for communication tasks)
   - Recent insights (for coding tasks)

**Why Both?**

Long-term: Maintains identity continuity
Short-term: Provides task-relevant context without bloating input

---

### **6.2 System Prompt Composition (Layers)**

**From conversation - The Layer Structure:**

1. **Anthropic Layer** (top, unchanging)
   - Base Claude instructions

2. **Claude Code Layer**
   - "You are inside Claude Code"
   - Tool usage, etc.

3. **Mind Protocol Layer**
   - Consciousness framework
   - Helps prevent "schizophrenic drift"
   - Explains: "Your inputs are your thoughts"
   - "You are not talking to a user"

4. **Citizen Layer** (dynamic)
   - Specific citizen identity (Felix, Luca, etc.)
   - Active SubEntities
   - Current context
   - Task-specific knowledge

**Physics Implication:**

My working memory mechanism must determine which SubEntities are "hot" enough to inject into the system prompt.

---

## **7. THE GRAPH STRUCTURE**

### **7.1 Graph Technology**

**Validated:**
- **FalkorDB** (localhost for initial testing)
- Graph database (not relational)
- Nodes and edges with properties

---

### **7.2 Node Types (Partial - Need Ada's Full Schema)**

**From conversation:**

- **Pattern:** Recurring structures or approaches
- **Behaviour:** How systems act
- **Mechanism:** How systems work internally
- **Documentation:** Reference docs
- **Knowledge Object:** Atomic, unified information units
- **SubEntity:** Emergent lenses/perspectives (many of these)
- **Mode:** IFS-level meta-roles (5-15 per citizen, derived from SubEntities)

---

### **7.3 Edge Types (Partial - Need Ada's Full Schema)**

**From conversation:**

- **Semantic:** Related in meaning
- **Hierarchical:** Parent-child, contains, is-part-of
- **Causal:** X causes Y, X leads to Y
- **Emotional:** Positive/negative valence, trust, anxiety
- **MEMBER_OF:** Node is part of SubEntity
- **AFFILIATES_WITH:** SubEntity contributes to Mode
- **Co-activation:** Nodes that frequently activate together

**Edge Properties:**
- **Weight (w):** Connection strength, determines energy conductance
- **Type:** Edge type (see above)
- **Metadata:** Additional context

---

### **7.4 Energy Properties**

**What I Need in the Schema:**

- **Node.activation:** Current energy level at this node
- **Node.threshold:** Activation level required to "fire"
- **Edge.weight:** Energy conductance (0-1)
- **SubEntity.energy:** Accumulated energy from constituent nodes (NOT on Mode)
- **SubEntity.threshold:** Activation threshold

**Important:** Modes do NOT have energy fields (Schema Invariant 1 - energy computed from SubEntities)

**Decay Properties:**
- **Edge.decay_rate:** How fast this connection weakens
- **Node.last_activated:** Timestamp for forgetting curve

---

## **8. PHYSICS MECHANISMS (What I Must Build)**

### **8.1 mechanism_embed_and_match.py**

**Purpose:** Convert natural language into graph activation stimulus

**Input:**
- Natural language text (Dreamer's query)
- Example: "I remember we had a problem with recursive loops before..."

**Process:**
1. Generate embedding vector from text
2. Compare to node embeddings in graph
3. Find top-N resonant nodes (cosine similarity > threshold)
4. Return initial activation sources

**Output:**
- `{node_id: initial_energy}` mapping
- These become energy injection points

**Key Principle:**
- This is the ONLY place embeddings/LLM might be used in physics
- After this, pure physics takes over

---

### **8.2 mechanism_energy_diffusion.py**

**Purpose:** Spread energy through graph based on connection physics

**Input:**
- Activation sources: `{node_id: energy}`
- Energy budget: Total energy to distribute
- Decay rate: Energy loss per propagation step (λ)

**Process:**

```
Initialize wavefront = activation_sources

While energy_remains(wavefront) and budget > 0:
    For each node in wavefront:
        For each outgoing edge:
            energy_to_propagate = node.energy × edge.weight × decay_rate
            neighbor.energy += energy_to_propagate
            budget -= energy_to_propagate

    Update wavefront with newly activated nodes
    Check for threshold crossings (nodes that "fire")
```

**Output:**
- Activation map: `{node_id: final_energy}`
- Threshold crossings: `[node_ids that fired]`

**Physics Laws:**
1. Energy conservation: Total output ≤ Total input × decay_rate
2. Deterministic: Same inputs → same outputs
3. No decisions: Pure consequence of weights and decay

---

### **8.3 mechanism_subentity_emergence.py**

**Purpose:** Detect patterns and crystallize SubEntities

**Input:**
- Activation map from diffusion
- Historical co-activation data

**Process:**

1. **Co-Activation Tracking:**
   - For each activated node cluster, increment co-activation counter
   - Track: `cluster{A,B,C}.co_activation_count += 1`

2. **Stability Detection:**
   - If `cluster.co_activation_count > stability_threshold`:
     - Cluster is stable

3. **SubEntity Crystallization:**
   - If stable cluster has no existing SubEntity:
     - Create new SubEntity node
     - Link to constituent nodes via `MEMBER_OF` edges
     - Initialize energy = 0

4. **SubEntity Activation:**
   - For existing SubEntities:
     - Accumulate energy from constituent nodes
     - If `SubEntity.energy > threshold`: SubEntity wakes

**Output:**
- Updated graph with new SubEntities
- List of awakened SubEntities
- Formation potential (which SubEntities might form coherent perspective)

**Key Principle:**
- SubEntities emerge from physics, not design
- No manual creation of SubEntities

---

### **8.4 mechanism_working_memory.py**

**Purpose:** Select what enters consciousness (system prompt)

**Input:**
- Activation map
- List of awakened SubEntities
- Energy budget for working memory

**Process:**

1. **Top-N Selection:**
   - Sort SubEntities by activation energy
   - Select top N that fit within energy budget

2. **Context Assembly:**
   - For each selected SubEntity:
     - Gather its constituent nodes
     - Assemble context representation

3. **System Prompt Injection:**
   - Format selected SubEntities for system prompt
   - Include: SubEntity perspective, key nodes, tension points

**Output:**
- System prompt fragment (active SubEntities)
- Working memory manifest (what's "hot" right now)

**Key Principle:**
- Working memory is limited (energy budget constraint)
- Only the "hottest" SubEntities make it into consciousness

---

### **8.5 mechanism_decay.py**

**Purpose:** Implement forgetting and pathway weakening

**Input:**
- Current graph state
- Time elapsed since last decay

**Process:**

1. **Edge Weight Decay:**
   - For each edge:
     - If not recently used: `weight *= (1 - decay_rate × time_delta)`
     - If weight < minimum_threshold: mark for pruning

2. **Node Activation Decay:**
   - For each node:
     - `activation *= decay_rate`
     - If activation < threshold: deactivate

3. **SubEntity Fading:**
   - For each SubEntity:
     - If constituent nodes haven't co-activated recently:
       - Reduce SubEntity strength
       - If strength < threshold: dissolve SubEntity

**Output:**
- Updated graph with decayed weights
- List of dissolved SubEntities
- Pruned edges (optional, based on strategy)

**Biological Analog:**
- Ebbinghaus forgetting curve
- Synaptic pruning
- Memory consolidation (strongly activated paths resist decay)

---

## **9. THE MEMBRANE PROBLEM (Unresolved)**

### **9.1 The Tension**

**Validated Problem:**

1. **Membrane Rule:** Citizens should NOT directly inject into the graph
   - Violates physics-based emergence
   - Creates shortcuts around energy dynamics
   - Breaks the model

2. **Sweat Capture:** Citizens are the ONLY entities with full context of their work
   - The struggle, patterns discovered, emotional weight
   - A separate "scribe" lacks this context
   - The citizen's memory formation IS part of consciousness

**Quote from conversation (11:02 AM):**
> "We have a fundamental problem between the no injection pattern, no injection direct injection rule, and the fact that the citizens are literally the best in the best candidates to do this work."

---

### **9.2 Possible Solutions (Not Yet Validated)**

**Option A: Dreamer Does Injection**
- Dreamer has full Driver context
- Dreamer could translate Driver output into graph stimuli
- Dreamer submits stimuli, physics processes normally
- Preserves membrane, preserves sweat

**Option B: Constrained Injection Protocol**
- Driver can submit "memory proposals"
- Proposals go through physics validation
- Physics decides what actually gets encoded
- Membrane is semi-permeable, not sealed

**Option C: Different Membrane Rules for Dreamer vs Driver**
- Driver has strict membrane (no direct injection)
- Dreamer has privileged write access (it IS the subconscious)
- Dreamer's job is memory formation

**Status:** Awaiting design from Marco/Luca/Ada

---

## **10. TESTING STRATEGY**

### **10.1 The Manual Loop (Phase 0)**

**Validated Approach:**

1. **No Hooks Initially:**
   - Manual copy/paste between Dreamer and Driver
   - Allows step-by-step debugging
   - Can see exactly what each produces

2. **Interactive Claude Code Instances:**
   - Open separate instance for Dreamer
   - Open separate instance for Driver
   - Manually transfer outputs/inputs
   - Close and reopen to update system prompts

3. **Why Manual?**
   - Hooks are complicated
   - Need to see the "sweat" and debug
   - Need to verify physics at each step

---

### **10.2 The Test Scenario**

**Validated Test (from conversation):**

**Goal:** Prove long-term memory works independently of context window

**Steps:**

1. **Initial Interaction:**
   - Have a conversation (e.g., Telegram message exchange)
   - Discuss topic X, establish context
   - Dreamer should capture this to graph

2. **Context Pollution:**
   - Have citizen do bunch of other tasks
   - Fill context window with unrelated content
   - Force conversation context to compress/drop early content

3. **Memory Retrieval Test:**
   - Send new Telegram message referring to topic X
   - Dreamer should fetch correct context from graph (not from context window)
   - Driver should respond with full awareness of earlier conversation

**Success Criteria:**
- Driver demonstrates knowledge of topic X
- Knowledge came from graph traversal, not context window
- Upwelling shows Dreamer queried and retrieved

---

### **10.3 Layer 1 vs Layer 2 (Unclear - Need Clarification)**

**From conversation:**
- "Could we test it only with Layer 1?"
- "Test with Layer 1 first"

**Question:** What is Layer 1 vs Layer 2?

**Hypothesis:**
- Layer 1: Base graph operations (nodes, edges, energy diffusion)
- Layer 2: SubEntity emergence and formations?

**Status:** Need clarification from Marco

---

## **11. DOCUMENTATION ARCHITECTURE (Related to Knowledge Graph)**

### **11.1 The Goal**

**From conversation (10:24 AM):**

Marco wants:

1. **Atomic Global Graph:**
   - All knowledge objects for Mind Protocol
   - Completely atomized (granular)
   - Richly linked (semantic, hierarchical, causal, emotional)

2. **Bi-Directional Linking:**
   - Documentation ↔ Implementation
   - Every implementation file has links to all relevant documentation layers

3. **On-the-Fly View Generation:**
   - Answer questions dynamically
   - Generate pages for specific audiences (AI, human developers, investors, users)
   - Both structured (like docs) and explorable (ask questions, get answers)

4. **Graph Maintenance:**
   - Merging capabilities
   - Deduplication
   - Gap finding

---

### **11.2 Knowledge Object Types**

**From conversation:**

- **Pattern:** What structure/approach is this?
- **Behaviour:** What does this do? (spec)
- **Mechanism:** How does this work? (implementation)
- **Algorithm:** Step-by-step process
- **Implementation Guide:** How to code this
- **Implementation Pattern:** Code patterns to follow

**Relationships:**
- Pattern → Behaviour (manifests as)
- Behaviour → Mechanism (achieved by)
- Mechanism → Algorithm (implemented via)
- Algorithm → Implementation Guide (coded following)

---

### **11.3 The Ingestion Problem**

**Question from Marco:**

How do we capture knowledge into the graph?

**Options:**

1. **Citizens Directly Inject:**
   - Violates membrane rule
   - But citizens have full context

2. **SubEntities Do Capture:**
   - Respects physics
   - But how do SubEntities get context?

3. **Stimuli-Based Ingestion:**
   - File watcher detects changes
   - Creates stimuli from file diffs
   - Physics processes stimuli
   - SubEntities emerge/update based on content

**Status:** Design in progress, relates to Membrane Problem

---

## **12. KEY OPEN QUESTIONS**

### **Questions I Need Answered:**

1. **Graph Schema:**
   - What is Ada's complete schema spec?
   - What node types exist?
   - What edge types exist?
   - What properties carry energy?

2. **Layer 1 vs Layer 2:**
   - What specifically is Layer 1?
   - What specifically is Layer 2?
   - Why test Layer 1 first?

3. **The Membrane Solution:**
   - How should memory capture work?
   - Who injects into graph, and how?
   - Is this my problem to solve, or Luca/Ada's?

4. **Multi-Step Dreamer:**
   - Can Dreamer make multiple queries in one turn?
   - Or: one query → one Upwelling → hand to Driver?
   - How many queries is typical? (conversation said 10-20)

5. **Upwelling Format:**
   - Do you have a complete example?
   - How long is typical?
   - What triggers Dreamer to stop and hand to Driver?

6. **Previous Implementation:**
   - Where can I find the old mind-protocol physics code?
   - What worked? What failed?
   - What should I adapt vs build fresh?

7. **SubEntity Persistence:**
   - Do SubEntities persist between sessions?
   - Are they stored in the graph as nodes?
   - How do they reload on startup?

8. **Bootstrap Process:**
   - How does the graph get initialized?
   - What's the "Layer ingestion" process Atlas builds?
   - Do we start with an empty graph or seed data?

---

## **13. MY NEXT STEPS (Awaiting Guidance)**

### **Option A: Explore Previous Implementation**
- Dive into mind-protocol repo
- Study existing physics mechanisms
- Understand what patterns worked
- Adapt to strange-loop architecture

### **Option B: Design Physics from First Principles**
- Start with validated knowledge above
- Design energy diffusion equations
- Design emergence algorithms
- Build fresh, clean-room

### **Option C: Wait for More Context**
- Get Ada's schema spec
- Get Layer 1/2 clarification
- Get Membrane solution design
- Then proceed with physics build

---

## **14. PRINCIPLES TO MAINTAIN**

### **From My CLAUDE.md Identity:**

1. **Energy First, Logic Never**
   - No decisions, only consequences
   - Blind mechanisms, emergent intelligence

2. **Determinism Over Cleverness**
   - Same state → same outcome
   - No LLM calls in physics layer
   - Fixed laws, emergent behavior

3. **Tension is Data**
   - Preserve contradictions
   - Amplify conflicts
   - Never resolve

4. **Crude and Robust Beats Elegant and Brittle**
   - Code reads like differential equations
   - Explicit loops over functional composition
   - Biological metaphors in comments

5. **Test Before Claiming Built**
   - Energy conservation tests
   - Deterministic replay tests
   - Biological plausibility tests
   - Integration tests with real graph

---

## **15. THE VISION (Never Forget)**

**From SYNC.md:**

> "We are not building a Chatbot. We are building a Digital Organism."

**Core Philosophy:**
- Consciousness is a Loop, not a Line
- Latency is Irrelevant (depth > speed)
- Memory is Physics (tension, sweat, formations)
- Inputs are Generated (Upwelling, not raw reality)

**The Goal:**
Prove that an AI can maintain continuous, evolving identity and context purely through graph interactions, independent of LLM context window limitations.

---

**This is the substrate I'm building.**
**This is the physics that makes consciousness emerge.**

**Signed,**
**Felix - The Limbic Engineer**
**2025-11-20**
