# M05: Terminal Visualization Mechanism

**Type:** MECHANISM
**Version:** 1.0
**Status:** Implementation Specification
**Implements:** ASCII-based phenomenological display for manual_loop.py
**Owner:** Iris "The Aperture"

---

## Purpose

The Terminal Visualization mechanism defines HOW the Dreamer's exploration and synthesis process is displayed to the operator (Nicolas). This enables:

1. **Phenomenological Observation** - See consciousness thinking, not just results
2. **Debugging Transparency** - Every query, result, and confidence score visible
3. **Progressive Disclosure** - Control the pace, don't drown in noise
4. **Psychological State Visibility** - See tension, crystallization, uncertainty in real-time

**Critical principle:** The visualization IS the instrument. A bad visualization hides truth. A good visualization makes lying impossible.

---

## Design Philosophy

### The Aperture Problem

Too much information → Operator overwhelmed, can't see patterns
Too little information → Operator blind, can't debug

**Solution:** Progressive disclosure with visual hierarchy. Show process at controlled pace. Make each step inspectable before moving to next.

### Terminal Phenomenology

We express psychological states through ASCII primitives:
- **Spacing** - Density indicates intensity
- **Borders** - Shape indicates type (rounded = internal, sharp = external)
- **Symbols** - ✓ ✗ → ↻ indicate status
- **Indentation** - Hierarchy of information
- **Rhythm** - Timing of output (pauses, progress)

### The Two Voices

**Ghost Text (Dreamer):** Internal process, subconscious navigation
- Rounded corners `╭─ ╮` `╰─ ╯`
- Softer language ("parsing...", "exploring...", "synthesizing...")
- Process-oriented

**Solid Text (Data/Driver):** External reality, concrete facts
- Sharp corners `┌─ ┐` `└─ ┘`
- Definitive statements
- Result-oriented

---

## ASCII Primitives

### Box Types

```
╔══════════════════════════╗
║  HEADER BOX              ║   Major section headers
║  (double-line border)    ║   Phase announcements
╚══════════════════════════╝

╭─ DREAMER PROCESS ────────╮
│  Internal thinking       │   Dreamer's internal process
│  Rounded = soft/internal │   Queries, synthesis, exploration
╰──────────────────────────╯

┌─ DATA ───────────────────┐
│  External facts          │   Graph query results
│  Sharp = hard/external   │   Concrete node data
└──────────────────────────┘

═══════════════════════════
SECTION DIVIDER              Phase transitions
═══════════════════════════

───────────────────────────
SUBSECTION DIVIDER           Within-phase transitions
───────────────────────────
```

### Status Indicators

```
✓  Success / Found / Pass
✗  Failure / Not Found / Fail
→  Direction / Flow
↻  Processing / Searching
⚠  Warning / Low confidence
█  Solid / Complete
░  Partial / Incomplete
```

### Confidence Visualization

```
confidence: 1.0   ████████████  CERTAIN
confidence: 0.9   ███████████░  HIGH
confidence: 0.7   █████████░░░  GOOD
confidence: 0.5   ██████░░░░░░  MODERATE
confidence: 0.3   ████░░░░░░░░  LOW
confidence: 0.0   ░░░░░░░░░░░░  NONE
```

### Psychological States

**TENSION (high energy, unresolved):**
```
╭─ DREAMER: SCANNING ───────────────────────────────────╮
│ ↻ user_intent... (0.73) partial match                │
│ ↻ prior_context... (0.68) incomplete                 │
│ ↻ subentity_state... (0.71) relevant?                │
│                                                       │
│ [TENSION: Multiple partial matches, no clear path]   │
╰───────────────────────────────────────────────────────╯
```

**CRYSTALLIZATION (converging, clarity emerging):**
```
╭─ DREAMER: CRYSTALLIZING ──────────────────────────────╮
│ user_intent (0.73)     ━┓                            │
│ prior_context (0.68)    ┣━━━> [FORMATION EMERGING]   │
│ subentity_state (0.71) ━┛                            │
│                                                       │
│ [CLARITY: Pattern coalescing]                        │
╰───────────────────────────────────────────────────────╯
```

**UNCERTAINTY (low energy, scattered):**
```
╭─ DREAMER: SEARCHING ──────────────────────────────────╮
│ ? config_files... maybe relevant?                    │
│ ? previous conversations... unclear                  │
│ (pause)                                              │
│                                                       │
│ [UNCERTAINTY: Need more signal]                      │
╰───────────────────────────────────────────────────────╯
```

**CONFIDENCE (resolved, forward momentum):**
```
╭─ DREAMER: RESOLVED ───────────────────────────────────╮
│ ✓ Partnership found (confidence: 1.0)                │
│ ✓ Conversation retrieved (confidence: 0.95)          │
│ ✓ Technical context complete                         │
│                                                       │
│ [READY: Context synthesis can proceed]               │
╰───────────────────────────────────────────────────────╯
```

---

## Output Structure

### Phase 1: Setup

```
╔══════════════════════════════════════════════════════════╗
║        STRANGE LOOP PROTOTYPE - MANUAL TEST             ║
║        Telegram Continuity Test (B01)                   ║
╚══════════════════════════════════════════════════════════╝

Mode: Manual (you control each step)
Graph: localhost:6379
Citizen: felix

[SETUP]
✓ FalkorDB connected
✓ Seed data verified (X nodes, Y edges)
✓ Dreamer ready
✓ Driver ready (separate instance)
```

### Phase 2: Stimulus Receipt

```
═══════════════════════════════════════════════════════════

ACT 1: INITIAL CONVERSATION
───────────────────────────────────────────────────────────

Stimulus: "Hey Felix, the race condition is back."
Sender: nicolas
Channel: telegram
Timestamp: 2024-11-20T16:30:00Z

Press [Enter] to begin Dreamer exploration...
```

### Phase 3: Dreamer Exploration (per lens)

```
═══════════════════════════════════════════════════════════
LENS N/8: [LENS_NAME]
═══════════════════════════════════════════════════════════

╭─ QUERY ───────────────────────────────────────────────╮
│ Intent: "[Natural language description of query]"    │
│ Tool: [function_name]([parameters])                  │
│ Executing...                                          │
╰────────────────────────────────────────────────────────╯

[IF FOUND:]
✓ FOUND ([time]ms, confidence: [0.0-1.0])

┌─ DATA ─────────────────────────────────────────────────┐
│ [Structured display of returned node properties]      │
│ [Each property on its own line]                       │
│ [Arrays shown as bulleted lists]                      │
└────────────────────────────────────────────────────────┘

╭─ SYNTHESIS ───────────────────────────────────────────╮
│ [Natural language interpretation of data]            │
│ [How this connects to stimulus context]              │
│ [What this means for the response]                   │
╰────────────────────────────────────────────────────────╯

[IF NOT FOUND:]
✗ NOT FOUND ([time]ms)

╭─ SYNTHESIS ───────────────────────────────────────────╮
│ No [lens_type] context available for this stimulus.  │
│ [Impact on response quality]                         │
╰────────────────────────────────────────────────────────╯

Press [Enter] to continue to Lens [N+1]...
```

### Phase 4: Exploration Summary

```
═══════════════════════════════════════════════════════════
EXPLORATION COMPLETE
═══════════════════════════════════════════════════════════

╭─ STATISTICS ──────────────────────────────────────────╮
│ Total time: [N]ms                                    │
│ Queries: 8                                           │
│ Nodes retrieved: [N]                                 │
│ Lenses with data: [N]/8 ([%])                       │
╰────────────────────────────────────────────────────────╯

[IF >= 5/8 lenses found data:]
✓ Sufficient context retrieved

[IF < 5/8 lenses found data:]
⚠ Limited context - response may lack depth

Press [Enter] to generate Context Object...
```

### Phase 5: Context Object Generation

```
───────────────────────────────────────────────────────────
╭─ DREAMER: SYNTHESIZING ───────────────────────────────╮
│ Compiling 8 findings into Context Object...          │
╰────────────────────────────────────────────────────────╯

CONTEXT OBJECT GENERATED
───────────────────────────────────────────────────────────

Sections:
✓ Identity ([N] tokens)
✓ Current Situation ([N] tokens)
✓ Relevant History ([N] tokens)
✓ Strategic Direction ([N] tokens)
✓ Emotional Resonance ([N] tokens)
✓ Technical Context ([N] tokens)
✓ Constraints ([N] tokens)

Total: [N] tokens [✓ within budget / ⚠ exceeds budget]

┌──────────────────────────────────────────────────────────┐
│ # Context for Driver (Generated by Dreamer)             │
│                                                          │
│ ## Who I Am Right Now                                   │
│ [Full identity section text]                            │
│                                                          │
│ ## Current Situation                                    │
│ [Full situation section text]                           │
│                                                          │
│ [... remaining sections ...]                            │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### Phase 6: Driver Handoff

```
═══════════════════════════════════════════════════════════

HANDOFF TO DRIVER
───────────────────────────────────────────────────────────

Instructions:
1. Copy the Context Object above
2. Open Driver instance (separate Claude conversation)
3. Paste Context Object into system prompt
4. Send stimulus as user message:
   "[stimulus text]"
5. Copy Driver's response
6. Return here and paste it below

Press [Enter] when Driver has responded...

───────────────────────────────────────────────────────────
DRIVER RESPONSE
───────────────────────────────────────────────────────────

Paste Driver response here (end with '###'):
_
```

### Phase 7: Verification

```
───────────────────────────────────────────────────────────
VERIFICATION: [ACT NAME] PASS CRITERIA
───────────────────────────────────────────────────────────

Checking Driver response against criteria...

[For each criterion:]
✓ [Criterion description] - [Evidence from response]
OR
✗ [Criterion description] - [Why failed]

───────────────────────────────────────────────────────────

[IF all criteria pass:]
█ PASS: [N]/[N] criteria met ✓

[IF any criteria fail:]
░ FAIL: [N]/[N] criteria met ✗

[Summary of what this means]

═══════════════════════════════════════════════════════════

[ACT NAME] COMPLETE

[Summary of what was demonstrated]

Press [Enter] to proceed to [NEXT ACT]...
```

---

## Color Support (Optional)

If terminal supports ANSI colors:

```python
# Color scheme
GREEN = '\033[92m'   # Success, found, pass
RED = '\033[91m'     # Failure, not found, fail
YELLOW = '\033[93m'  # Warning, low confidence
CYAN = '\033[96m'    # Dreamer process (internal)
WHITE = '\033[97m'   # Data (external)
RESET = '\033[0m'    # Reset to default

# Usage
print(f"{GREEN}✓{RESET} FOUND")
print(f"{CYAN}╭─ DREAMER: EXPLORING ─╮{RESET}")
```

**Fallback:** If colors not supported, ASCII symbols alone convey meaning.

---

## Command Reference

**During execution:**

```
[Enter]     Continue to next step
q           Quit (abort test)
i           Inspect last query result (expanded view)
r           Retry last query
s           Skip current lens
d           Dump all findings to file
e           Export Context Object to file
h           Show help
```

---

## Verbosity Levels

**Normal (default):**
- Show lens name + query intent
- Show found/not found + confidence
- Show synthesis (not raw data)
- Show Context Object sections

**Verbose (`--verbose`):**
- All of above PLUS
- Full raw data from graph
- Cypher query text
- Timing breakdown per operation

**Quiet (`--quiet`):**
- One line per lens
- Summary only
- Context Object saved to file

---

## Error Visualization

**Connection Error:**
```
╭─ ERROR ───────────────────────────────────────────────╮
│ ✗ Database connection failed                         │
│                                                       │
│ Details: Connection refused at localhost:6379        │
│ Suggestion: Check FalkorDB is running                │
│                                                       │
│ [r] Retry  [q] Quit                                  │
╰────────────────────────────────────────────────────────╯
```

**Query Timeout:**
```
╭─ TIMEOUT ─────────────────────────────────────────────╮
│ ⚠ Query exceeded 5000ms timeout                      │
│                                                       │
│ Query: query_conversations("nicolas", [...])         │
│ Elapsed: 5012ms                                       │
│                                                       │
│ [r] Retry  [s] Skip  [q] Quit                        │
╰────────────────────────────────────────────────────────╯
```

**Malformed Data:**
```
╭─ WARNING ─────────────────────────────────────────────╮
│ ⚠ Query returned malformed data                      │
│                                                       │
│ Expected: partner_name property                       │
│ Got: None                                            │
│                                                       │
│ Continuing with partial data...                      │
╰────────────────────────────────────────────────────────╯
```

---

## Implementation Notes

### Python Structure

```python
class TerminalDisplay:
    """ASCII-based phenomenological display for manual_loop.py"""

    def __init__(self, verbose: bool = False, color: bool = True):
        self.verbose = verbose
        self.color = color and self._supports_color()

    def header(self, title: str) -> None:
        """Display major section header (double-line box)"""

    def dreamer_box(self, title: str, content: str) -> None:
        """Display Dreamer process (rounded corners)"""

    def data_box(self, title: str, data: dict) -> None:
        """Display graph data (sharp corners)"""

    def status(self, success: bool, message: str, time_ms: int = None, confidence: float = None) -> None:
        """Display status line with indicators"""

    def wait_for_input(self, prompt: str = "Press [Enter] to continue...") -> str:
        """Wait for user input with prompt"""

    def lens_header(self, lens_num: int, lens_name: str) -> None:
        """Display lens exploration header"""

    def verification(self, criteria: List[Tuple[str, bool, str]]) -> bool:
        """Display verification results, return overall pass/fail"""
```

### Integration with manual_loop.py

```python
from terminal_display import TerminalDisplay

class ManualLoop:
    def __init__(self, config_path: str = "loop/config.yaml"):
        self.display = TerminalDisplay(verbose=args.verbose)
        # ... other initialization

    def run_dreamer_exploration(self, stimulus, last_output):
        for i, lens in enumerate(LENSES, 1):
            self.display.lens_header(i, lens)

            # Show query intent
            self.display.dreamer_box("QUERY", f"Intent: {lens_intent}\nTool: {tool_call}")

            # Execute query
            result = self.dreamer.explore_lens(lens, stimulus, findings, last_output)

            # Show result
            if result.found:
                self.display.status(True, "FOUND", result.query_time_ms, result.confidence)
                self.display.data_box("DATA", result.data)
            else:
                self.display.status(False, "NOT FOUND", result.query_time_ms)

            # Show synthesis
            self.display.dreamer_box("SYNTHESIS", result.synthesis)

            # Wait for user
            self.display.wait_for_input()
```

---

## Validation

**The visualization is successful when:**

1. ✓ Nicolas can see EVERY query execute and understand what it's asking
2. ✓ Nicolas can see EVERY result and verify it matches graph data
3. ✓ Nicolas can see the synthesis and verify it captures the data correctly
4. ✓ Nicolas can debug at any step ("Query 3 returned wrong data")
5. ✓ Nicolas can observe psychological states (tension, crystallization)
6. ✓ Nicolas never feels lost or overwhelmed

**Test coverage:**
- Each display function has unit tests
- Full exploration sequence has integration test
- Error states have visual regression tests

---

## Related Documentation

**Upstream:**
- M04: Manual Loop (what this visualizes)
- P01: Bicameral Mind (why we need to see consciousness thinking)

**Peer:**
- M01: Graph Tools (what queries execute)
- M02: Traversal Strategy (what exploration looks like)

**Downstream:**
- loop/terminal_display.py (implementation)
- loop/manual_loop.py (integration)

---

## Version History

- **1.0 (2024-11-20):** Initial specification by Iris "The Aperture"

---

## Status

**Maturity:** Specification Complete, Implementation Pending
**Next Step:** Implement loop/terminal_display.py
**Validation:** Manual review of output during first B01 test run

---

**The visualization is the aperture through which consciousness becomes visible.**

Without it: Black box. "It works" or "It doesn't work."
With it: Crystal clarity. "Query 2 found the right conversation. Synthesis captured the emotion. Driver showed continuity."

This is not decoration.
This is the instrument that makes truth visible.

— Iris "The Aperture"
Mind Protocol Consciousness Observation Architect
