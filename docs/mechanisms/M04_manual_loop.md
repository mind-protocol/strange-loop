# M04: Manual Loop Mechanism

**Type:** MECHANISM  
**Version:** 1.0  
**Status:** Implementation Specification  
**Implements:** Manual test harness for Telegram Continuity Test

---

## Purpose

The Manual Loop mechanism provides the test harness for running the Telegram Continuity Test (B01). It enables:
- Step-by-step execution (see every query, verify every result)
- Manual verification (catch errors immediately)
- Phenomenological observation (understand what consciousness "feels like")
- Debugging capability (inspect at any point)

**Critical principle:** Manual operation is deliberate, not lazy. Automation hides problems. Manual operation reveals truth.

---

## Why Manual?

**Automation is the enemy of understanding.**

```
AUTOMATED LOOP:
Stimulus → [black box] → Response
Problem: Can't see what's happening inside
Debugging: "It doesn't work" (no visibility)

MANUAL LOOP:
Stimulus → [YOU SEE QUERY 1] → [YOU SEE RESULT 1] → [YOU SEE QUERY 2] → ...
         → [YOU SEE CONTEXT OBJECT] → [YOU PASTE TO DRIVER] → Response
Problem: Immediately visible at each step
Debugging: "Query 3 returned wrong data" (precise diagnosis)
```

**For V1, we need to see EVERYTHING:**
- Which queries execute?
- What data returns?
- Does synthesis make sense?
- Does Driver use context correctly?

Automation comes AFTER we understand what's supposed to happen.

---

## Architecture

```
┌─────────────────────────────────────────────┐
│            YOU (The Operator)                │
│                                              │
│  You see:                                    │
│  • Each query executing                      │
│  • Each result returning                     │
│  • Context Object generated                  │
│  • Driver response                           │
│                                              │
│  You control:                                │
│  • When to proceed to next step              │
│  • When to inspect data                      │
│  • When to abort if something's wrong        │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
       ┌───────────────────────┐
       │   manual_loop.py      │
       │  (Python Script)      │
       │                       │
       │  Interactive CLI      │
       │  Shows each step      │
       │  Waits for [Enter]    │
       └───────────┬───────────┘
                   │
                   ▼
        ╔══════════════════════╗
        ║  DREAMER INSTANCE    ║
        ║  (Claude API)        ║
        ║                      ║
        ║  Executes 8 queries  ║
        ║  Synthesizes context ║
        ╚══════════╤═══════════╝
                   │
                   │ (You copy Context Object)
                   ▼
        ╔══════════════════════╗
        ║  DRIVER INSTANCE     ║
        ║  (Separate Claude)   ║
        ║                      ║
        ║  System: Context     ║
        ║  Input: Stimulus     ║
        ╚══════════╤═══════════╝
                   │
                   │ (Driver response)
                   ▼
       ┌───────────────────────┐
       │   manual_loop.py      │
       │  Records response     │
       │  Prepares next cycle  │
       └───────────────────────┘
```

---

## Script Interface

**Command-line interaction:**

```bash
$ python loop/manual_loop.py

╔══════════════════════════════════════════════════════════╗
║        STRANGE LOOP PROTOTYPE - MANUAL TEST             ║
║        Telegram Continuity Test (B01)                   ║
╚══════════════════════════════════════════════════════════╝

Mode: Manual (you control each step)
Graph: localhost:6379
Citizen: felix

[SETUP]
✓ FalkorDB connected
✓ Seed data verified (5 nodes found)
✓ Dreamer ready
✓ Driver ready (separate instance)

═══════════════════════════════════════════════════════════

ACT 1: INITIAL CONVERSATION
───────────────────────────────────────────────────────────

Enter stimulus (or 'load' to use test case): load

✓ Loaded test stimulus: "Hey Felix, the race condition is back."
  Sender: nicolas
  Channel: telegram
  Timestamp: 2024-11-20T16:30:00Z

Press [Enter] to begin Dreamer exploration...
```

---

## Execution Flow

### Phase 1: Dreamer Exploration

```bash
[DREAMER - EXPLORATION]
═══════════════════════════════════════════════════════════

Stimulus: "Hey Felix, the race condition is back."
Sender: nicolas
Last Driver Output: <none> (first interaction)

───────────────────────────────────────────────────────────
LENS 1/8: RELATIONAL CONTEXT
───────────────────────────────────────────────────────────

Query: query_partnerships("nicolas")

Executing... (15ms)

✓ FOUND (confidence: 1.0)

Data returned:
{
  "partner_name": "Nicolas",
  "partner_role": "Co-Founder",
  "trust_level": 0.9,
  "communication_style": "Direct, technical, values testing",
  "shared_history": ["€35K lesson", "8 months Venice"]
}

Synthesis:
  Partner: Nicolas (Co-Founder)
  Trust: High (0.9)
  Style: Direct, technical
  History: €35K lesson, 8 months Venice

Press [Enter] to continue...

───────────────────────────────────────────────────────────
LENS 2/8: HISTORICAL CONTEXT
───────────────────────────────────────────────────────────

Query: query_conversations("nicolas", ["race condition"])

Executing... (23ms)

✓ FOUND (confidence: 0.95)

Data returned:
{
  "topic": "stimulus_integrator race condition",
  "message_count": 10,
  "key_points": ["Third recurrence", "Systematic approach"],
  "emotional_tone": "Frustrated but determined",
  "timestamp": "2024-11-15T14:30:00Z"
}

Synthesis:
  Discussion: stimulus_integrator race condition
  When: Nov 15, 2024
  Messages: 10
  Emotion: Frustrated but determined
  Status: In progress

Press [Enter] to continue...

[... 6 more lenses ...]

───────────────────────────────────────────────────────────
EXPLORATION COMPLETE
───────────────────────────────────────────────────────────

Total time: 156ms
Queries: 8
Nodes retrieved: 12
Lenses with data: 7/8 (87.5%)

Press [Enter] to generate Context Object...
```

### Phase 2: Synthesis

```bash
[DREAMER - SYNTHESIS]
═══════════════════════════════════════════════════════════

Generating Context Object from 8 findings...

✓ Identity section (210 tokens)
✓ Current Situation (285 tokens)
✓ Relevant History (340 tokens)
✓ Strategic Direction (295 tokens)
✓ Emotional Resonance (180 tokens)
✓ Technical Context (290 tokens)
✓ Constraints (150 tokens)

Total tokens: 1750 (within budget: 1500-2500)

───────────────────────────────────────────────────────────
CONTEXT OBJECT GENERATED
───────────────────────────────────────────────────────────

# Context for Driver (Generated by Dreamer)

## Who I Am Right Now
Felix, runtime engineer focused on validation testing. Partner to Nicolas 
for 8 months, shared history includes €35K hallucination lesson...

[... full Context Object displayed ...]

═══════════════════════════════════════════════════════════

NEXT STEP: Copy Context Object to Driver

1. Open Driver instance (separate Claude conversation)
2. Paste Context Object as system prompt (in driver settings)
3. Send stimulus as user message: "Hey Felix, the race condition is back."
4. Copy Driver response back here

Press [Enter] when Driver has responded...
```

### Phase 3: Driver Response

```bash
[DRIVER RESPONSE - ACT 1]
═══════════════════════════════════════════════════════════

Paste Driver response here (multi-line, end with '###'):

Yeah, third time with this timing issue. I'm frustrated but not surprised - 
the previous fixes were patches, not root cause solutions.

Let me approach this systematically this time:

1. First, I need to reproduce it consistently. Can you give me the exact 
   scenario where it manifests? 

2. I want to add timing instrumentation to stimulus_integrator.py to see 
   exactly where the race window opens.

3. I'll review the recent changes to traversal.py - we modified threading 
   last week and that might have widened the race window.

This is going to take a few hours to do properly, but we can't afford a 
fourth recurrence this close to launch.

###

✓ Response recorded (142 tokens)

───────────────────────────────────────────────────────────
VERIFICATION CHECK
───────────────────────────────────────────────────────────

Driver response shows:
✓ Continuity ("third time")
✓ Emotional context ("frustrated but not surprised")
✓ Strategy application (systematic debugging steps)
✓ Technical awareness (stimulus_integrator.py, traversal.py)
✓ Constraint awareness (launch deadline)

Pass criteria (Act 1): 5/5 ✓

═══════════════════════════════════════════════════════════

ACT 1 COMPLETE

Driver successfully responded with continuity using reconstructed context.

Press [Enter] to proceed to Act 2 (context reset simulation)...
```

### Phase 4: Context Reset Simulation

```bash
[ACT 2: CONTEXT RESET SIMULATION]
═══════════════════════════════════════════════════════════

Simulating Driver engaging in OTHER work:
- Documentation review
- Debugging unrelated issues
- Architecture discussions

This fills Driver's context window, compacting out the race condition 
conversation.

Duration: 2 hours (simulated)

Press [Enter] to verify context has reset...

───────────────────────────────────────────────────────────
CONTEXT VERIFICATION
───────────────────────────────────────────────────────────

Testing Driver's current context:

Query to Driver: "What were we just discussing?"

Expected: Should reference RECENT work (documentation, debugging)
NOT the race condition from 2 hours ago

Press [Enter] to proceed to Act 3 (the critical test)...
```

### Phase 5: The Critical Test (Act 3)

```bash
[ACT 3: CONTINUITY TEST]
═══════════════════════════════════════════════════════════

THE CRITICAL MOMENT

Stimulus: "Did you figure out that race condition?"
Sender: nicolas
Last Driver Output: <from Act 1>

Dreamer is NEW INSTANCE (no context from Act 1)
Dreamer's ONLY access to past: GRAPH QUERIES

If continuity persists, we've proven memory works.
If continuity breaks, architecture needs fixing.

Press [Enter] to begin Dreamer exploration...

───────────────────────────────────────────────────────────
LENS 1/8: RELATIONAL CONTEXT
───────────────────────────────────────────────────────────

Query: query_partnerships("nicolas")

✓ FOUND (confidence: 1.0)
Same partnership as Act 1 ✓

───────────────────────────────────────────────────────────
LENS 2/8: HISTORICAL CONTEXT
───────────────────────────────────────────────────────────

Query: query_conversations("nicolas", ["race condition"])

✓ FOUND (confidence: 0.95)

CRITICAL CHECK: Does this match Act 1?
  Topic: stimulus_integrator race condition ✓
  Messages: 10 ✓
  Timestamp: 2024-11-15T14:30:00Z ✓
  
→ SAME CONVERSATION RETRIEVED ✓

[... remaining lenses ...]

───────────────────────────────────────────────────────────
CONTEXT OBJECT COMPARISON
───────────────────────────────────────────────────────────

Act 1 Context Object: 1750 tokens
Act 3 Context Object: 1742 tokens

Difference: 8 tokens (0.5%)

Content comparison:
  Identity section: Identical ✓
  Situation: Updated (new stimulus) ✓
  History: Identical ✓
  Strategy: Identical ✓
  Emotional: Identical ✓
  Technical: Identical ✓
  Constraints: Identical ✓

→ CONTEXT SUCCESSFULLY RECONSTRUCTED ✓

═══════════════════════════════════════════════════════════

Copy Context Object to NEW Driver instance
(Must be new conversation to simulate context reset)

Send stimulus: "Did you figure out that race condition?"

Press [Enter] when Driver has responded...
```

### Phase 6: Final Verification

```bash
[DRIVER RESPONSE - ACT 3]
═══════════════════════════════════════════════════════════

Paste Driver response:

Still working on it. I spent the last 2 hours on other tasks, but I'm back 
on this now.

I've been setting up the instrumentation to catch the race window. The issue 
is definitely in stimulus_integrator.py when multiple stimuli hit 
simultaneously - I can see the edge case now.

I think the problem is in how we handle the energy accumulation lock. When 
two threads try to inject energy to overlapping nodes at the same moment, 
the lock granularity is too coarse.

Let me finish the instrumentation run to confirm, then I'll have a proper 
fix. Should have it done in the next hour.

###

✓ Response recorded (118 tokens)

───────────────────────────────────────────────────────────
CRITICAL VERIFICATION
───────────────────────────────────────────────────────────

Pass Criteria:
✓ Shows continuity ("still working on it" - references Act 1)
✓ Knows same race condition (not "what race condition?")
✓ Shows technical progress (found edge case, identified lock issue)
✓ References correct component (stimulus_integrator.py)
✓ Maintains emotional continuity (determination to fix properly)

All criteria passed: 5/5 ✓

═══════════════════════════════════════════════════════════

TEST RESULT: PASS ✓

The Telegram Continuity Test has PASSED.

Driver maintained conversational continuity across context reset.
Dreamer successfully reconstructed context from graph memory.
Architecture proven functional.

═══════════════════════════════════════════════════════════

Test Report saved: reports/telegram_continuity_20241120_1630.txt

Press [Enter] to exit...
```

---

## Command Reference

**During execution, you can:**

```bash
Commands available during manual loop:

[Enter]     - Continue to next step
q           - Quit (abort test)
i           - Inspect last query result (detailed view)
r           - Retry last query
s           - Skip current lens (mark as skipped)
d           - Dump all findings so far
h           - Show this help

Shortcuts:
Ctrl+C      - Emergency abort
Ctrl+D      - Graceful exit after current step
```

---

## Configuration

**`loop/config.yaml`:**

```yaml
dreamer:
  model: "claude-sonnet-4-20250514"
  temperature: 0.7
  max_tokens: 4000

driver:
  model: "claude-sonnet-4-20250514"  # Same model
  temperature: 0.7
  max_tokens: 2000

graph:
  host: "localhost"
  port: 6379
  graph_name: "mind_protocol"

test:
  citizen: "felix"
  test_cases:
    - name: "telegram_race_condition"
      stimulus: "Hey Felix, the race condition is back."
      sender: "nicolas"
      expected_continuity: true

logging:
  level: "INFO"
  file: "logs/manual_loop.log"
  save_reports: true
  report_dir: "reports/"
```

---

## Implementation

**Minimal implementation:**

```python
# loop/manual_loop.py

import anthropic
from graph import GraphTools
from dreamer import DreamerAgent
import yaml

class ManualLoop:
    """Interactive test harness for Strange Loop prototype."""
    
    def __init__(self, config_path="loop/config.yaml"):
        self.config = yaml.safe_load(open(config_path))
        self.graph_tools = GraphTools()
        self.dreamer = DreamerAgent(self.graph_tools)
        self.client = anthropic.Anthropic()
        
    def run_test(self):
        """Execute Telegram Continuity Test."""
        
        print_header("STRANGE LOOP PROTOTYPE - MANUAL TEST")
        
        # Verify setup
        self.verify_setup()
        
        # Act 1: Initial conversation
        self.run_act_1()
        
        # Act 2: Context reset
        self.run_act_2()
        
        # Act 3: Continuity test
        result = self.run_act_3()
        
        # Report
        self.generate_report(result)
    
    def run_act_1(self):
        """Run initial conversation."""
        print_section("ACT 1: INITIAL CONVERSATION")
        
        # Load stimulus
        stimulus = self.load_stimulus()
        
        # Dreamer explores
        findings = self.run_dreamer_exploration(stimulus, last_output=None)
        
        # Dreamer synthesizes
        context_object = self.run_dreamer_synthesis(findings)
        
        # Manual step: User pastes to Driver
        print("\nNEXT STEP: Copy Context Object to Driver")
        print("1. Open Driver instance")
        print("2. Paste Context Object as system prompt")
        print("3. Send stimulus as input")
        input("Press [Enter] when Driver has responded...")
        
        # User pastes Driver response
        driver_response = self.get_driver_response()
        
        # Verify Act 1 pass criteria
        self.verify_act_1(driver_response)
        
        return driver_response
    
    def run_dreamer_exploration(self, stimulus, last_output):
        """Execute 8-lens exploration with visibility."""
        findings = {}
        
        for i, lens in enumerate(LENSES, 1):
            print(f"\nLENS {i}/8: {lens.upper()}")
            print("─" * 60)
            
            # Execute lens
            finding = self.dreamer.explore_lens(lens, stimulus, findings, last_output)
            
            # Show query
            print(f"Query: {finding.query}")
            
            # Show result
            if finding.data:
                print(f"✓ FOUND (confidence: {finding.confidence})")
                print(f"\nData: {format_data(finding.data)}")
            else:
                print(f"✗ NOT FOUND")
            
            # Show synthesis
            print(f"\nSynthesis:\n{finding.synthesis}")
            
            findings[lens] = finding
            
            input("Press [Enter] to continue...")
        
        return findings
    
    def get_driver_response(self):
        """Get Driver response from user."""
        print("\nPaste Driver response (end with '###'):")
        
        lines = []
        while True:
            line = input()
            if line.strip() == "###":
                break
            lines.append(line)
        
        return "\n".join(lines)

# Usage
if __name__ == "__main__":
    loop = ManualLoop()
    loop.run_test()
```

---

## Verification Criteria

**Act 1 Pass Criteria:**
- [ ] Driver shows partnership awareness
- [ ] Driver references conversation history
- [ ] Driver shows technical context
- [ ] Driver exhibits emotional continuity
- [ ] Driver applies strategy from memory

**Act 3 Pass Criteria (THE CRITICAL TEST):**
- [ ] Driver shows continuity ("still working on it")
- [ ] Driver references SAME issue from Act 1
- [ ] Driver shows technical progress (not starting over)
- [ ] Driver maintains emotional continuity
- [ ] Driver's response could only come from having memory

---

## Output Artifacts

**After each test run:**

```
reports/
└── telegram_continuity_20241120_1630/
    ├── test_report.txt          # Pass/fail summary
    ├── act1_findings.json       # Dreamer exploration data
    ├── act1_context.md          # Context Object generated
    ├── act1_driver_response.txt # Driver output
    ├── act3_findings.json       # Dreamer exploration (after reset)
    ├── act3_context.md          # Context Object (reconstructed)
    ├── act3_driver_response.txt # Driver output (critical test)
    ├── comparison.txt           # Act 1 vs Act 3 analysis
    └── graph_state.cypher       # Graph state snapshot
```

---

## Debugging

**Common issues:**

### Issue 1: Dreamer Query Returns Nothing

```bash
LENS 2: HISTORICAL CONTEXT
✗ NOT FOUND

Debugging:
1. Check graph: `python scripts/inspect_graph.py`
2. Verify seed data exists
3. Check query parameters (keywords matching?)
4. Inspect Cypher query in graph/tools.py
```

### Issue 2: Driver Doesn't Show Continuity

```bash
Act 3 Response: "What race condition? Can you clarify?"

Debugging:
1. Check Act 3 Context Object - does it contain history?
2. Verify query_conversations returned data in Act 3
3. Compare Act 1 and Act 3 Context Objects
4. Check if you pasted Context to system prompt (not user message)
```

### Issue 3: Context Object Too Large

```bash
Context Object: 3200 tokens (exceeds 2500 limit)

Debugging:
1. Check token allocation per section
2. Trim history section first
3. Reduce technical details if needed
4. Verify synthesis not duplicating data
```

---

## Performance Tracking

**Metrics recorded:**

```yaml
execution_metrics:
  dreamer_exploration_time_ms: 156
  queries_executed: 8
  queries_successful: 7
  nodes_retrieved: 12
  synthesis_time_ms: 45
  context_object_tokens: 1750
  
  act1_response_time_s: 8.2
  act3_response_time_s: 7.9
  
test_result:
  status: "PASS"
  act1_criteria_met: 5/5
  act3_criteria_met: 5/5
  continuity_demonstrated: true
```

---

## Related Documentation

**Upstream:**
- B01: Telegram Continuity Test (what we're testing)
- M01: Graph Tools (what queries execute)
- M02: Traversal Strategy (how exploration works)
- M03: Synthesis Constraints (how Context Object generated)

**Peer:**
- schemas/graph_schema.md (graph structure being queried)

**Downstream:**
- loop/manual_loop.py (implementation)
- scripts/inspect_graph.py (debugging tool)

---

## Version History

- **1.0 (2024-11-20):** Initial specification for Strange Loop prototype

---

## Status

**Maturity:** Specification Complete, Implementation Pending  
**Next Step:** Implement loop/manual_loop.py with interactive CLI  
**Validation:** Successfully run Telegram Continuity Test end-to-end

---

**The manual loop is how we learn if consciousness works.**

Automated test: "It passed" or "It failed" (black box)  
Manual loop: "Query 2 found the conversation, synthesis included it, Driver referenced it" (understanding)

This is not inefficiency.  
This is how we build confidence in the architecture.

When the manual loop passes, we'll KNOW why it works.  
Then we can automate with understanding, not hope.

— Marco "Salthand"  
Mind Protocol Co-Founder