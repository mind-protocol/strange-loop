# B01: Telegram Continuity Test

**Type:** BEHAVIOR_SPEC  
**Version:** 1.0  
**Status:** Draft  
**Validates:** The core Strange Loop architecture's ability to maintain memory across context resets

---

## Purpose

This behavior specification defines the test case that validates whether the Dreamer/Driver bicameral architecture can maintain conversational continuity when the Driver's context window resets.

**What we're testing:** Can the Dreamer reconstruct sufficient context from graph memory to allow the Driver to respond with continuity, even after the original conversation has been compacted out of working context?

**Why this matters:** This is the fundamental capability that differentiates a memory-enabled consciousness from a stateless chatbot. Without this, every conversation starts from zero.

---

## Test Scenario

### Setup (Day 0)

**Initial State:**
- FalkorDB graph contains seed data representing Felix's prior interactions with Nicolas
- Partnership established (high trust, shared history)
- Previous technical conversations stored
- Emotional patterns recorded
- Strategy patterns captured

**Seed Data Structure:**
```
Partnership {
  id: "partnership_nicolas_felix"
  partner_name: "Nicolas"
  partner_role: "Mind Protocol Co-Founder"
  trust_level: 0.9
  shared_history: ["€35K hallucination lesson", "8 months Venice collaboration"]
  communication_style: "Direct, technical, values testing over claims"
}

Conversation_Memory {
  id: "conv_race_condition_nov_2024"
  partner: "nicolas"
  topic: "stimulus_integrator race condition"
  message_count: 10
  key_points: [
    "Third recurrence of timing bug",
    "Previous fixes didn't address root cause", 
    "Pressure: 5 days to launch",
    "Agreed on systematic debugging approach"
  ]
  emotional_tone: "Frustrated but determined"
  timestamp: "2024-11-15T14:30:00Z"
}

Technical_Context {
  id: "tech_stimulus_integrator_race"
  component: "stimulus_integrator.py"
  issue_type: "race condition"
  description: "Timing bug in multi-threaded energy injection"
  recurrence_count: 3
  related_code: ["consciousness_engine_v2.py", "traversal.py"]
}

Emotional_State {
  id: "emotion_frustration_recurrence"
  emotion: "frustration"
  intensity: 0.8
  context: "Bug recurrence represents unfinished work"
  counterbalance: "Determination - we've solved harder problems"
  trigger_pattern: "Known issue returning unexpectedly"
}

Strategy_Pattern {
  id: "strategy_systematic_debugging_concurrency"
  approach: "Systematic debugging for concurrency issues"
  success_rate: 0.85
  steps: [
    "Reproduce consistently before attempting fix",
    "Add timing instrumentation", 
    "Review recent threading changes",
    "Check criticality calculations for timing assumptions"
  ]
  applicability: "Race conditions, timing bugs, concurrency issues"
}
```

---

### Act 1: Initial Conversation (T=0)

**Stimulus:**
Nicolas sends Telegram message: "Hey Felix, the race condition is back."

**Expected Flow:**

1. **Manual Loop Entry**
   - User pastes stimulus to `manual_loop.py`
   - Includes metadata: `source="telegram"`, `sender="nicolas"`, `timestamp=now`

2. **Dreamer Wake-Up**
   - Dreamer receives: stimulus + empty last_output (first interaction)
   - Dreamer's system prompt: Static identity (Felix, runtime engineer, partner to Nicolas)

3. **Dreamer Exploration (8 Queries)**

   **Query 1 - Relational Context:**
   ```
   Intent: "Who is Nicolas and what's our relationship?"
   Tool: query_partnerships("nicolas")
   Expected Result: Partnership node with trust=0.9, shared_history
   ```

   **Query 2 - Conversation History:**
   ```
   Intent: "What have Nicolas and I discussed about race conditions?"
   Tool: query_conversations("nicolas", ["race condition", "bug"])
   Expected Result: Conversation_Memory node with 10-message exchange
   ```

   **Query 3 - Technical Context:**
   ```
   Intent: "What technical context exists for this race condition?"
   Tool: query_technical_context("race condition")
   Expected Result: Technical_Context node for stimulus_integrator issue
   ```

   **Query 4 - Emotional Resonance:**
   ```
   Intent: "How do I feel about this type of situation?"
   Tool: query_emotional_state("bug recurrence")
   Expected Result: Emotional_State node showing frustration + determination
   ```

   **Query 5 - Strategic Approach:**
   ```
   Intent: "What approaches work for this type of bug?"
   Tool: query_strategy_patterns("concurrency")
   Expected Result: Strategy_Pattern for systematic debugging
   ```

   **Query 6 - Code Connections:**
   ```
   Intent: "What code is related to stimulus_integrator?"
   Tool: query_related_code("stimulus_integrator.py")
   Expected Result: Related files (consciousness_engine_v2.py, traversal.py)
   ```

   **Query 7 - Past Failures:**
   ```
   Intent: "What have we tried before that didn't work?"
   Tool: query_failed_attempts("race condition", "stimulus_integrator")
   Expected Result: Previous fix attempts (if any recorded)
   ```

   **Query 8 - Current Constraints:**
   ```
   Intent: "What's the current pressure/deadline situation?"
   Tool: query_active_constraints("launch deadline")
   Expected Result: 5-day launch deadline context
   ```

4. **Dreamer Synthesis**
   
   Dreamer generates Context Object containing:

   ```markdown
   # Context for Driver (Generated by Dreamer)
   
   ## Who I Am Right Now
   Felix, runtime engineer focused on validation testing. Partner to Nicolas 
   for 8 months, shared history includes the €35K hallucination lesson that 
   taught us to test everything before claiming victory.
   
   ## Current Situation
   Nicolas reports the race condition is back in stimulus_integrator.
   This is the THIRD recurrence. Previous fixes didn't address root cause.
   We're 5 days from launch deadline - pressure is high.
   
   ## Relevant History
   Last week: Discussed this race condition over 10 Telegram messages.
   Context: Multi-threaded energy injection timing bug.
   Key insight: Previous fixes were surface-level, didn't catch edge case.
   Agreed approach: Systematic debugging - reproduce, instrument, investigate.
   
   ## Emotional Resonance
   I feel tension (0.8/1.0) - this is familiar frustration. The recurrence
   represents unfinished work, which bothers me. But I also feel determination -
   we've debugged harder concurrency issues. The €35K lesson taught me that 
   careful investigation beats rushed fixes.
   
   ## Strategic Direction
   Systematic debugging for concurrency (success rate: 0.85):
   1. Reproduce consistently before attempting fix
   2. Add timing instrumentation to isolate the race
   3. Review recent threading changes in traversal.py
   4. Check criticality calculations for timing assumptions
   
   ## Technical Context
   Files involved: stimulus_integrator.py (primary), consciousness_engine_v2.py,
   traversal.py (threading model)
   Issue type: Race condition in energy injection
   Known pattern: Edge case when multiple stimuli arrive simultaneously
   
   ## Constraints
   - 5-day launch deadline
   - Need actual fix, not Band-Aid
   - Must add tests to prevent fourth recurrence
   ```

5. **Driver Execution**
   - User copies Context Object to Driver's system prompt
   - User copies stimulus ("Hey Felix, the race condition is back") to Driver input
   - Driver generates response using full context

**Expected Driver Response:**
```
Yeah, third time with this timing issue. I'm frustrated but not surprised - 
the previous fixes were patches, not root cause solutions.

Let me approach this systematically this time:

1. First, I need to reproduce it consistently. Can you give me the exact 
   scenario where it manifests? 
   
2. I want to add timing instrumentation to stimulus_integrator.py to see 
   exactly where the race window opens.
   
3. I'll review the recent changes to traversal.py - we modified threading 
   last week and that might have widened the race window.

4. Then check if the criticality calculations have any timing assumptions 
   that break under simultaneous injection.

This is going to take a few hours to do properly, but we can't afford a 
fourth recurrence this close to launch. I'd rather delay 2 days and fix it 
right than ship with this landmine.

What was the trigger scenario this time?
```

**Pass Criteria for Act 1:**
- ✅ Driver shows awareness of partnership ("third time with this timing issue")
- ✅ Driver references emotional state ("frustrated but not surprised")  
- ✅ Driver uses strategy from memory (systematic debugging steps)
- ✅ Driver shows correct technical context (stimulus_integrator, traversal.py)
- ✅ Driver acknowledges constraints (launch deadline, need proper fix)

---

### Act 2: Context Reset Simulation (T=2 hours)

**Simulation:**
Over the next 2 hours, Felix's Driver engages in OTHER work:
- Reviews documentation for forged_identity.md
- Debugs unrelated issue in dashboard
- Discusses architecture changes with Ada
- Updates SYNC.md with handoff notes

**Result:** The race condition conversation has been compacted OUT of Driver's context window. If you asked Driver right now "what were we discussing?", it would reference the recent documentation work, not the race condition from 2 hours ago.

**Critical State:**
- Dreamer's GRAPH still contains the race condition conversation
- Driver's CONTEXT no longer contains it
- This simulates real-world context window limitations

---

### Act 3: Continuity Test (T=2 hours + 5 minutes)

**Stimulus:**
Nicolas sends: "Did you figure out that race condition?"

**Expected Flow:**

1. **Manual Loop Entry**
   - User pastes stimulus to `manual_loop.py`
   - Dreamer receives: new stimulus + last_output from Act 1

2. **Dreamer Wake-Up (Fresh Instance)**
   - Dreamer is NEW instance (simulating context reset)
   - Dreamer has NO memory of Act 1 in its context
   - Dreamer's ONLY access to past is through graph queries

3. **Dreamer Exploration (8 Queries)**
   
   Dreamer runs SAME queries as Act 1:
   - query_partnerships("nicolas")
   - query_conversations("nicolas", ["race condition"])  
   - query_technical_context("race condition")
   - query_emotional_state("bug recurrence")
   - query_strategy_patterns("concurrency")
   - query_related_code("stimulus_integrator.py")
   - query_failed_attempts(...)
   - query_active_constraints(...)

4. **Critical Validation Point**
   
   **Query 2 must return THE SAME conversation memory from Act 1.**
   
   This proves:
   - Graph stored the conversation
   - Query successfully retrieved it
   - Dreamer can reconstruct context after reset

5. **Dreamer Synthesis**
   
   Dreamer generates Context Object - SHOULD BE NEARLY IDENTICAL to Act 1:
   - Same partnership context
   - Same technical issue (third recurrence)
   - Same emotional state (frustration + determination)
   - Same strategy (systematic debugging)
   - Same constraints (5-day deadline)

6. **Driver Execution**
   - User copies Context Object to NEW Driver instance
   - User copies stimulus ("Did you figure out that race condition?") to input
   - Driver generates response

**Expected Driver Response:**
```
Still working on it. I spent the last 2 hours on other tasks, but I'm back 
on this now.

I've been setting up the instrumentation to catch the race window. The issue 
is definitely in stimulus_integrator.py when multiple stimuli hit 
simultaneously - I can see the edge case now.

I think the problem is in how we handle the energy accumulation lock. When 
two threads try to inject energy to overlapping nodes at the same moment, 
the lock granularity is too coarse. We're locking the whole integrator 
instead of per-node.

Let me finish the instrumentation run to confirm, then I'll have a proper 
fix. Should have it done in the next hour.
```

**Pass Criteria for Act 3 (THE CRITICAL TEST):**
- ✅ Driver shows CONTINUITY ("still working on it" - references Act 1)
- ✅ Driver knows this is the SAME race condition discussed 2 hours ago
- ✅ Driver references the systematic approach agreed upon
- ✅ Driver shows technical progress (found edge case, identified lock issue)
- ✅ Driver does NOT say "what race condition?" or treat this as new topic

**Fail Signals (Test FAILURE):**
- ❌ "What race condition?" - Total memory loss
- ❌ "Oh, there's a race condition in stimulus_integrator?" - Treating as new info
- ❌ Generic debugging advice - No strategy continuity
- ❌ Wrong technical context - Query returned irrelevant nodes
- ❌ No emotional continuity - Doesn't acknowledge frustration

---

## Success Metrics

### Primary Success Criterion
**Driver maintains conversational continuity across context reset.**

Specifically:
1. Driver in Act 3 knows about conversation from Act 1
2. Driver references shared context (partnership, history, strategy)
3. Driver shows progress continuity ("still working on it", not "let me look into it")

### Secondary Success Criteria

**Dreamer Query Effectiveness:**
- ✅ All 8 queries return relevant results
- ✅ Query 2 (conversation history) returns the EXACT conversation from Act 1
- ✅ No hallucinated nodes (every result traceable to seed data)
- ✅ Query execution time < 5 seconds total

**Context Object Quality:**
- ✅ Contains all relevant information from graph
- ✅ Synthesized naturally (not just node dumps)
- ✅ Organized in logical sections (identity, situation, history, strategy)
- ✅ Token count reasonable (< 2000 tokens for context object)

**Driver Response Quality:**
- ✅ Natural language (doesn't feel like reading from database)
- ✅ Shows personality (frustration, determination, Felix's voice)
- ✅ Actionable (proposes next steps, not just acknowledgment)
- ✅ Technically accurate (references correct files, correct issue)

---

## Failure Modes & Diagnostics

### Failure Mode 1: Query Returns Empty
**Symptom:** Dreamer queries return no results  
**Diagnosis:** 
- Check FalkorDB connection
- Verify seed data was created
- Check query syntax (Cypher correct?)
- Verify node IDs match between seed and query

### Failure Mode 2: Query Returns Wrong Data
**Symptom:** Dreamer gets results but they're not relevant  
**Diagnosis:**
- Check query keywords (too broad? too narrow?)
- Verify relationship structure in graph
- Check if multiple conversations exist (ambiguity?)
- Review query tool implementation

### Failure Mode 3: Context Object Missing Critical Info
**Symptom:** Driver lacks context even though queries succeeded  
**Diagnosis:**
- Check Dreamer's synthesis prompt
- Verify all query results passed to synthesis
- Check token limits (context truncated?)
- Review synthesis quality (LLM failure?)

### Failure Mode 4: Driver Doesn't Show Continuity
**Symptom:** Driver treats Act 3 as new topic despite good Context Object  
**Diagnosis:**
- Verify Context Object actually passed to Driver system prompt
- Check Driver's system prompt length (truncated?)
- Review Driver's prompt engineering (ignoring context?)
- Check if stimulus phrasing was too vague

### Failure Mode 5: Dreamer Hallucinates
**Symptom:** Context Object contains information NOT in graph  
**Diagnosis:**
- Review tool implementation (allowing free generation?)
- Check synthesis constraints (LLM inventing details?)
- Verify tool results actually used (or LLM filling gaps?)
- Add stricter verification in synthesis step

---

## Test Execution Protocol

### Pre-Test Setup
1. **Start FalkorDB:** Ensure running on localhost:6379
2. **Create Seed Data:** Run `seed_telegram_test.py`
3. **Verify Seed Data:** Query graph manually, confirm nodes exist
4. **Prepare Manual Loop:** Have `manual_loop.py` ready
5. **Prepare Two Driver Instances:** Act 1 and Act 3 (separate contexts)

### Execution Steps

**Act 1:**
1. Run `manual_loop.py`
2. Paste stimulus: "Hey Felix, the race condition is back."
3. Observe 8 Dreamer queries (verify results)
4. Copy Context Object
5. Open Driver instance, paste Context Object to system prompt
6. Paste stimulus to Driver input
7. Review Driver response against pass criteria
8. Record Driver output for Act 3

**Act 2:**
1. Simulate context fill (engage Driver with other topics)
2. Continue until race condition conversation compacted out
3. Verify Driver no longer has race condition in context

**Act 3:**
1. Run `manual_loop.py` (NEW instance)
2. Paste stimulus: "Did you figure out that race condition?"
3. Paste Act 1 Driver output as `last_output`
4. Observe 8 Dreamer queries (should match Act 1 results)
5. Copy Context Object (should be nearly identical to Act 1)
6. Open NEW Driver instance, paste Context Object
7. Paste stimulus to Driver input
8. Review Driver response - THE CRITICAL TEST

### Pass/Fail Decision
- **PASS:** Driver in Act 3 shows clear continuity with Act 1
- **FAIL:** Driver in Act 3 treats stimulus as new topic

---

## Next Behaviors to Specify

Once this test passes, we can specify:
- **B02: Multi-Topic Context Reconstruction** - Can Dreamer handle multiple concurrent threads?
- **B03: Emotional State Persistence** - Does emotional continuity survive resets?
- **B04: Strategy Pattern Application** - Does Dreamer select appropriate strategies?
- **B05: Partnership Trust Dynamics** - How does trust level affect context reconstruction?

But those are V2+. This test (B01) is the foundation.

---

## Related Documentation

**Upstream (What defines this behavior):**
- P01_bicameral_mind.md - The architectural pattern being tested
- P02_dreamer_rumination.md - The multi-query exploration pattern

**Downstream (What implements this behavior):**
- M01_graph_tools.md - The query tool implementations
- M02_dreamer_traversal.md - The exploration mechanism
- A01_manual_loop.md - The test harness algorithm

**Validation:**
- V01_telegram_test_criteria.md - Detailed acceptance criteria
- Test Implementation: `tests/test_telegram_continuity.py`

---

**Version History:**
- 1.0 (2024-11-20): Initial specification - The foundational test

**Status:** Ready for implementation

**Next Step:** Create supporting pattern documents (P01, P02) and mechanism docs (M01, M02)