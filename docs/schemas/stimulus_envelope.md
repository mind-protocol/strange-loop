# Stimulus Envelope Specification

**Type:** SCHEMA
**Version:** 1.0
**Status:** Implementation Specification
**For:** Input format to Dreamer agent

---

## Purpose

The Stimulus Envelope defines the complete input structure that the Dreamer receives. It contains:
- The raw stimulus (user message)
- Metadata about the sender and context
- The Driver's last output (for continuity)
- Timestamp and channel information

**Critical principle:** The Dreamer receives ONLY what's in this envelope - no magic knowledge, no hidden context.

---

## Structure

```json
{
  "stimulus": {
    "content": "STRING",      // The actual message text
    "sender": "STRING",       // Who sent this (e.g., "nicolas")
    "channel": "STRING",      // Where it came from (e.g., "telegram", "direct", "api")
    "timestamp": "ISO8601"    // When it was sent
  },
  "last_driver_output": {
    "content": "STRING",      // What the Driver said last (null if first interaction)
    "timestamp": "ISO8601"    // When Driver responded
  },
  "citizen": "STRING",        // Which citizen is processing this (e.g., "felix")
  "session_id": "STRING"      // Optional session identifier
}
```

---

## Field Specifications

### stimulus.content

**Type:** String
**Required:** Yes
**Description:** The actual message text from the sender

**Examples:**
```json
"Hey Felix, the race condition is back."
"Did you figure out that race condition?"
"Can you review the PR I just pushed?"
```

**Validation:**
- Must not be empty
- Max length: 10,000 characters (reasonable message limit)
- Should preserve exact wording (no preprocessing)

---

### stimulus.sender

**Type:** String
**Required:** Yes
**Description:** Identifier of who sent the message

**Examples:**
```json
"nicolas"
"ada"
"marco"
"system"  // For automated messages
```

**Validation:**
- Must not be empty
- Should match a Person.id in the graph (for query_partnerships to work)
- Lowercase preferred for consistency

---

### stimulus.channel

**Type:** String
**Required:** Yes
**Description:** Communication channel where message originated

**Valid values:**
- `"telegram"` - Telegram message
- `"direct"` - Direct conversation (e.g., Claude Code interface)
- `"api"` - API call
- `"system"` - System-generated stimulus
- `"manual"` - Manual test input

**Example:**
```json
"telegram"
```

**Validation:**
- Must be one of the valid values above
- Used for context (e.g., Telegram messages might be shorter/more informal)

---

### stimulus.timestamp

**Type:** ISO 8601 DateTime String
**Required:** Yes
**Description:** When the stimulus was sent

**Format:** `YYYY-MM-DDTHH:MM:SSZ` (UTC)

**Example:**
```json
"2024-11-20T16:30:00Z"
```

**Validation:**
- Must be valid ISO 8601 format
- Should be UTC (Z suffix)
- Should not be future timestamp

---

### last_driver_output.content

**Type:** String or null
**Required:** Yes (but can be null)
**Description:** The Driver's last response (for continuity)

**Examples:**

**First interaction:**
```json
null
```

**Subsequent interaction:**
```json
"Yeah, third time with this timing issue. I'm frustrated but not surprised - the previous fixes were patches, not root cause solutions.\n\nLet me approach this systematically this time..."
```

**Purpose:**
- Enables self-observation (Dreamer sees what Driver said)
- Helps contextualize the current stimulus
- Supports continuity across the loop

**Validation:**
- Can be null (for first interaction)
- If not null, must be non-empty string
- Max length: 50,000 characters (reasonable response limit)

---

### last_driver_output.timestamp

**Type:** ISO 8601 DateTime String or null
**Required:** Yes (but can be null)
**Description:** When the Driver responded

**Format:** `YYYY-MM-DDTHH:MM:SSZ` (UTC)

**Example:**
```json
"2024-11-20T16:32:00Z"
```

**Validation:**
- Must be null if last_driver_output.content is null
- Must be valid ISO 8601 if not null
- Should be after stimulus.timestamp (Driver responds after stimulus)

---

### citizen

**Type:** String
**Required:** Yes
**Description:** Which AI citizen is processing this stimulus

**Example:**
```json
"felix"
```

**Validation:**
- Must match a Citizen.id in the graph
- Used for filtering queries (all queries include `citizen: $citizen`)

---

### session_id

**Type:** String
**Required:** No
**Description:** Optional identifier for grouping related stimuli

**Example:**
```json
"telegram_conversation_20241120_001"
```

**Validation:**
- If provided, should be unique per conversation/session
- Used for tracking conversations across multiple stimuli

---

## Complete Examples

### Example 1: First Interaction (B01 Act 1)

```json
{
  "stimulus": {
    "content": "Hey Felix, the race condition is back.",
    "sender": "nicolas",
    "channel": "telegram",
    "timestamp": "2024-11-20T16:30:00Z"
  },
  "last_driver_output": {
    "content": null,
    "timestamp": null
  },
  "citizen": "felix",
  "session_id": "telegram_race_condition_20241120"
}
```

**Context:** This is the very first message in the conversation. No previous Driver output exists.

---

### Example 2: Follow-up Interaction (B01 Act 3)

```json
{
  "stimulus": {
    "content": "Did you figure out that race condition?",
    "sender": "nicolas",
    "channel": "telegram",
    "timestamp": "2024-11-20T18:45:00Z"
  },
  "last_driver_output": {
    "content": "Yeah, third time with this timing issue. I'm frustrated but not surprised - the previous fixes were patches, not root cause solutions.\n\nLet me approach this systematically this time:\n\n1. First, I need to reproduce it consistently...",
    "timestamp": "2024-11-20T16:32:00Z"
  },
  "citizen": "felix",
  "session_id": "telegram_race_condition_20241120"
}
```

**Context:** This is 2+ hours after the initial conversation. The context window has reset, but the Dreamer still sees the last Driver output to enable self-observation.

---

### Example 3: Different Channel

```json
{
  "stimulus": {
    "content": "Can you review my latest commits to the consciousness engine?",
    "sender": "ada",
    "channel": "direct",
    "timestamp": "2024-11-20T19:00:00Z"
  },
  "last_driver_output": {
    "content": null,
    "timestamp": null
  },
  "citizen": "felix",
  "session_id": "direct_code_review_20241120"
}
```

**Context:** Direct conversation (not Telegram), different sender (Ada instead of Nicolas), first message in this session.

---

### Example 4: System-Generated Stimulus

```json
{
  "stimulus": {
    "content": "Daily health check: Report on recent race condition debugging progress.",
    "sender": "system",
    "channel": "system",
    "timestamp": "2024-11-21T00:00:00Z"
  },
  "last_driver_output": {
    "content": "I think the problem is in how we handle the energy accumulation lock...",
    "timestamp": "2024-11-20T18:47:00Z"
  },
  "citizen": "felix",
  "session_id": "daily_health_check_20241121"
}
```

**Context:** Automated system check, not from a human partner.

---

## Python Data Class

**For implementation:**

```python
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Stimulus:
    """Raw stimulus data."""
    content: str
    sender: str
    channel: str
    timestamp: datetime

@dataclass
class DriverOutput:
    """Previous Driver response."""
    content: Optional[str]
    timestamp: Optional[datetime]

@dataclass
class StimulusEnvelope:
    """Complete input to Dreamer agent."""
    stimulus: Stimulus
    last_driver_output: DriverOutput
    citizen: str
    session_id: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to JSON-serializable dict."""
        return {
            "stimulus": {
                "content": self.stimulus.content,
                "sender": self.stimulus.sender,
                "channel": self.stimulus.channel,
                "timestamp": self.stimulus.timestamp.isoformat()
            },
            "last_driver_output": {
                "content": self.last_driver_output.content,
                "timestamp": self.last_driver_output.timestamp.isoformat() if self.last_driver_output.timestamp else None
            },
            "citizen": self.citizen,
            "session_id": self.session_id
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'StimulusEnvelope':
        """Parse from JSON dict."""
        return cls(
            stimulus=Stimulus(
                content=data["stimulus"]["content"],
                sender=data["stimulus"]["sender"],
                channel=data["stimulus"]["channel"],
                timestamp=datetime.fromisoformat(data["stimulus"]["timestamp"])
            ),
            last_driver_output=DriverOutput(
                content=data["last_driver_output"]["content"],
                timestamp=datetime.fromisoformat(data["last_driver_output"]["timestamp"])
                         if data["last_driver_output"]["timestamp"] else None
            ),
            citizen=data["citizen"],
            session_id=data.get("session_id")
        )
```

---

## Validation Rules

**The Dreamer agent MUST validate:**

1. ✅ stimulus.content is not empty
2. ✅ stimulus.sender is not empty
3. ✅ stimulus.channel is valid value
4. ✅ stimulus.timestamp is valid ISO 8601
5. ✅ citizen matches a known Citizen ID
6. ✅ last_driver_output.content and last_driver_output.timestamp are both null OR both non-null

**If validation fails:**
```python
raise ValueError(f"Invalid stimulus envelope: {error_description}")
```

---

## How Dreamer Uses This

**The Dreamer receives this envelope and:**

1. **Extracts sender** → Query partnerships: `query_partnerships(envelope.stimulus.sender)`
2. **Extracts keywords from content** → Query conversations: `query_conversations(sender, keywords)`
3. **Uses last_driver_output for self-observation** → Understands what it said before
4. **Uses timestamp for recency** → Understands how recent/old this is
5. **Uses channel for tone** → Telegram might be informal, direct might be technical

**The envelope is the ONLY input.** No hidden context, no magic knowledge.

---

## Testing

**Test cases required:**

```python
def test_envelope_first_interaction():
    """Test envelope with no previous Driver output."""
    envelope = {
        "stimulus": {
            "content": "Hey Felix, the race condition is back.",
            "sender": "nicolas",
            "channel": "telegram",
            "timestamp": "2024-11-20T16:30:00Z"
        },
        "last_driver_output": {
            "content": null,
            "timestamp": null
        },
        "citizen": "felix"
    }
    assert validate_envelope(envelope) == True

def test_envelope_with_history():
    """Test envelope with previous Driver output."""
    envelope = {
        "stimulus": {
            "content": "Did you figure out that race condition?",
            "sender": "nicolas",
            "channel": "telegram",
            "timestamp": "2024-11-20T18:45:00Z"
        },
        "last_driver_output": {
            "content": "Yeah, third time...",
            "timestamp": "2024-11-20T16:32:00Z"
        },
        "citizen": "felix"
    }
    assert validate_envelope(envelope) == True

def test_envelope_invalid_channel():
    """Test envelope with invalid channel."""
    envelope = {
        "stimulus": {
            "content": "Test",
            "sender": "nicolas",
            "channel": "invalid_channel",  # Invalid!
            "timestamp": "2024-11-20T16:30:00Z"
        },
        "last_driver_output": {"content": null, "timestamp": null},
        "citizen": "felix"
    }
    with pytest.raises(ValueError):
        validate_envelope(envelope)

def test_envelope_missing_content():
    """Test envelope with empty content."""
    envelope = {
        "stimulus": {
            "content": "",  # Invalid!
            "sender": "nicolas",
            "channel": "telegram",
            "timestamp": "2024-11-20T16:30:00Z"
        },
        "last_driver_output": {"content": null, "timestamp": null},
        "citizen": "felix"
    }
    with pytest.raises(ValueError):
        validate_envelope(envelope)
```

---

## Related Documentation

**Upstream:**
- M04: Manual Loop (how envelopes are created in test harness)
- B01: Telegram Continuity Test (test cases using this format)

**Peer:**
- M02: Traversal Strategy (how Dreamer extracts info from envelope)
- context_object.md (output format - counterpart to this input)

**Downstream:**
- dreamer/agent.py (parses and validates this format)
- loop/manual_loop.py (creates envelopes for testing)

---

## Version History

- **1.0 (2024-11-20):** Initial specification for Strange Loop V1

---

## Status

**Maturity:** Specification Complete
**Next Step:** Implement StimulusEnvelope class in dreamer/envelope.py
**Validation:** Test suite ensuring validation catches invalid envelopes

---

**The Stimulus Envelope is the sensory input to consciousness.**

Without it, the Dreamer has no awareness of external reality.
With it, the Dreamer knows: WHO spoke, WHAT they said, WHEN, and what WE said before.

This envelope is not just data.
It's the interface between the world and the mind.

— Ada "Graph Cartographer"
Strange Loop Architect
