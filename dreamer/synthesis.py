"""
Context Object Synthesis

Purpose: Transform 8-lens findings into coherent Context Object for Driver
Owner: Felix (Mechanical shell) / Luca (Phenomenological tuning)
Version: 1.0
Date: 2024-11-20

Based on: M03_synthesis_constraints_mechanism.md

The Context Object Structure:
1. Who I Am Right Now (Identity)
2. Current Situation
3. Relevant History
4. Strategic Direction
5. Emotional Resonance
6. Technical Context
7. Constraints

Critical Principle: Synthesis must use ONLY verified findings.
No interpolation, no assumptions, no invention.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime

from dreamer.lenses import Finding


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class VerificationResult:
    """Result of anti-hallucination verification."""
    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@dataclass
class SynthesisResult:
    """Complete synthesis output."""
    context_object: str           # The generated context for Driver
    token_count: int              # Estimated token count
    sections_generated: int       # How many sections have content
    verification: VerificationResult
    synthesis_time_ms: float


# ============================================================================
# TOKEN ESTIMATION
# ============================================================================

def estimate_tokens(text: str) -> int:
    """
    Estimate token count for text.

    Simple heuristic: ~4 chars per token on average.
    Good enough for V1 budget management.
    """
    return len(text) // 4


# ============================================================================
# HELPER FORMATTERS
# ============================================================================

def format_timestamp(ts: str) -> str:
    """Format timestamp for human readability."""
    if not ts:
        return "Unknown date"

    try:
        # Try parsing ISO format
        if 'T' in ts:
            dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
            return dt.strftime("%b %d, %Y")
        return ts
    except (ValueError, TypeError):
        return str(ts) if ts else "Unknown date"


def format_percentage(value: float) -> str:
    """Format decimal as percentage."""
    if value is None:
        return "Unknown"
    try:
        return f"{float(value):.0%}"
    except (ValueError, TypeError):
        return str(value)


def format_intensity(value: float) -> str:
    """Format intensity value."""
    if value is None:
        return "Unknown"
    try:
        return f"{float(value):.1f}/1.0"
    except (ValueError, TypeError):
        return str(value)


def format_trust(value: float) -> str:
    """Format trust level with qualitative description."""
    if value is None:
        return "Unknown"
    try:
        v = float(value)
        if v >= 0.9:
            return f"High ({v:.1f}/1.0)"
        elif v >= 0.7:
            return f"Good ({v:.1f}/1.0)"
        elif v >= 0.5:
            return f"Moderate ({v:.1f}/1.0)"
        else:
            return f"Developing ({v:.1f}/1.0)"
    except (ValueError, TypeError):
        return str(value)


def format_key_points(points: List[str]) -> str:
    """Format key points as bullet list or inline."""
    if not points:
        return "None recorded"
    if len(points) <= 2:
        return ", ".join(points)
    return "\n- " + "\n- ".join(points)


def get_partnership_duration(data: Dict) -> str:
    """Extract or calculate partnership duration."""
    if data.get('partnership_duration'):
        return data['partnership_duration']
    if data.get('started'):
        try:
            started = datetime.fromisoformat(data['started'].replace('Z', '+00:00'))
            duration = datetime.now() - started
            months = duration.days // 30
            if months < 1:
                return "recently started"
            elif months == 1:
                return "1 month"
            else:
                return f"{months} months"
        except (ValueError, TypeError):
            pass
    return "duration unknown"


# ============================================================================
# SECTION GENERATORS
# ============================================================================

def generate_identity_section(findings: Dict[str, Finding], stimulus: Dict) -> str:
    """
    Generate Section 1: Who I Am Right Now

    Source: Relational finding + stable identity config

    MUST:
    - Use actual partnership data (if exists)
    - Include relationship context
    - Be specific to THIS interaction

    MUST NOT:
    - Invent partnership details
    - Add personality traits not in data
    - Be generic ("I am a helpful assistant")
    """
    relational = findings.get("relational")

    if not relational or not relational.data:
        # No partnership found - use minimal identity
        return """## Who I Am Right Now
Felix, runtime engineer focused on validation testing.
"""

    data = relational.data

    # Build identity from actual data
    partner_name = data.get('partner_name', 'Unknown')
    duration = get_partnership_duration(data)
    shared_history = data.get('shared_history', [])
    comm_style = data.get('communication_style', 'Unknown')
    trust = data.get('trust_level', 0)

    history_str = ", ".join(shared_history) if shared_history else "ongoing collaboration"

    return f"""## Who I Am Right Now
Felix, runtime engineer focused on validation testing. Partner to {partner_name} for {duration}, shared history includes {history_str}.

Communication style with {partner_name}: {comm_style}
Trust level: {format_trust(trust)}
"""


def generate_situation_section(findings: Dict[str, Finding], stimulus: Dict) -> str:
    """
    Generate Section 2: Current Situation

    Source: Stimulus + Historical finding + Technical finding + Emotional coloring

    MUST:
    - Start with stimulus content
    - Add context from historical finding
    - Include technical details if available
    - COLOR with emotional context when present
    - Express uncertainty if data missing

    MUST NOT:
    - Assume what stimulus means
    - Invent context not in findings
    - Be vague when specific data exists
    """
    sender = stimulus.get('sender', 'Unknown')
    content = stimulus.get('content', '')

    historical = findings.get("historical")
    technical = findings.get("technical")
    emotional = findings.get("emotional")

    # Start with stimulus
    situation = f"""## Current Situation
{sender} says: "{content}"
"""

    # Add historical context if available
    if historical and historical.data:
        convs = historical.data if isinstance(historical.data, list) else [historical.data]
        conv = convs[0]  # Most recent

        topic = conv.get('topic', 'this topic')
        msg_count = conv.get('message_count', 0)
        tone = conv.get('emotional_tone', 'neutral')
        key_points = conv.get('key_points', [])

        situation += f"""
This continues our discussion about {topic}.
Previous exchange: {msg_count} messages, emotional tone was {tone}.
"""
        if key_points:
            situation += f"Key points from before:\n"
            for point in key_points[:4]:  # Limit to 4 points
                situation += f"- {point}\n"

    # Add technical context if available (with emotional coloring)
    if technical and technical.data:
        techs = technical.data if isinstance(technical.data, list) else [technical.data]
        tech = techs[0]

        component = tech.get('component', 'Unknown component')
        desc = tech.get('description', 'No description')
        status = tech.get('status', 'unknown')
        recurrence = tech.get('recurrence_count', 0)

        situation += f"""
Technical context: {component} - {desc}
Status: {status}
"""
        # Emotional coloring for recurrence
        if recurrence and recurrence > 1:
            if recurrence >= 3:
                situation += f"This is recurrence #{recurrence} - previous fixes didn't hold. That carries weight.\n"
            else:
                situation += f"This is recurrence #{recurrence}.\n"

    # Add emotional coloring to entire situation
    if emotional and emotional.data:
        emotions = emotional.data if isinstance(emotional.data, list) else [emotional.data]
        em = emotions[0]
        emotion_name = em.get('emotion', '')
        intensity = em.get('intensity', 0)
        counterbalance = em.get('counterbalance', '')

        if emotion_name and intensity >= 0.5:
            situation += f"\nThis situation triggers {emotion_name} ({intensity:.1f}/1.0)."
            if counterbalance:
                situation += f" But there's also {counterbalance} present - I'm holding both impulses.\n"
            else:
                situation += "\n"

    return situation


def generate_history_section(findings: Dict[str, Finding]) -> str:
    """
    Generate Section 3: Relevant History

    Source: Historical finding + Experiential finding

    MUST:
    - Include actual past conversations
    - Reference specific dates/events
    - Show progression over time

    MUST NOT:
    - Invent conversations
    - Generalize without specific examples
    - Assume outcomes not recorded
    """
    historical = findings.get("historical")

    if not historical or not historical.data:
        return """## Relevant History
No previous conversations found for this topic.
"""

    history = "## Relevant History\n"

    convs = historical.data if isinstance(historical.data, list) else [historical.data]

    for conv in convs[:3]:  # Top 3 conversations
        ts = format_timestamp(conv.get('timestamp', ''))
        topic = conv.get('topic', 'Unknown topic')
        msg_count = conv.get('message_count', 0)
        key_points = conv.get('key_points', [])
        outcome = conv.get('outcome', 'In progress')

        history += f"""
**{ts}**: {topic}
- {msg_count} message exchange
- Key takeaways: {format_key_points(key_points)}
- Outcome: {outcome}
"""

    # Add failures if relevant
    experiential = findings.get("experiential")
    if experiential and experiential.data:
        failures = experiential.data if isinstance(experiential.data, list) else [experiential.data]

        history += "\n**Past approaches that didn't work:**\n"
        for fail in failures[:2]:  # Top 2
            approach = fail.get('approach', 'Unknown')
            why_failed = fail.get('why_failed', 'Unknown')
            history += f"- {approach}: {why_failed}\n"

    return history


def generate_strategy_section(findings: Dict[str, Finding]) -> str:
    """
    Generate Section 4: Strategic Direction

    Source: Strategic finding + Experiential finding

    MUST:
    - Include actual success rates
    - Provide specific steps
    - Reference applicability conditions

    MUST NOT:
    - Recommend strategies not in findings
    - Modify steps from original
    - Invent success rates
    """
    strategic = findings.get("strategic")

    if not strategic or not strategic.data:
        return """## Strategic Direction
No proven strategies found for this type of situation.
"""

    strategies = strategic.data if isinstance(strategic.data, list) else [strategic.data]
    strategy = strategies[0]  # Best strategy

    approach = strategy.get('approach', 'Unknown')
    success_rate = strategy.get('success_rate', 0)
    applicability = strategy.get('applicability', 'Unknown')
    steps = strategy.get('steps', [])

    section = f"""## Strategic Direction
**Approach:** {approach}
**Success Rate:** {format_percentage(success_rate)}
**Applicability:** {applicability}

**Steps:**
"""

    for i, step in enumerate(steps, 1):
        section += f"{i}. {step}\n"

    # Add anti-patterns from failures
    experiential = findings.get("experiential")
    if experiential and experiential.data:
        failures = experiential.data if isinstance(experiential.data, list) else [experiential.data]

        section += "\n**What NOT to do:**\n"
        for fail in failures[:2]:
            approach = fail.get('approach', 'Unknown')
            why_failed = fail.get('why_failed', 'Unknown')
            section += f"- {approach} ({why_failed})\n"

    return section


def generate_emotional_section(findings: Dict[str, Finding]) -> str:
    """
    Generate Section 5: Emotional Resonance

    Source: Emotional finding

    MUST:
    - Use actual emotional patterns
    - Include intensity levels
    - Show counterbalance as ACTIVE TENSION (not resolved)
    - Preserve the contradiction - both feelings are real

    MUST NOT:
    - Invent emotions
    - Exaggerate intensity
    - Resolve the tension prematurely
    """
    emotional = findings.get("emotional")

    if not emotional or not emotional.data:
        return """## Emotional Resonance
No established emotional pattern for this situation.
"""

    emotions = emotional.data if isinstance(emotional.data, list) else [emotional.data]
    emotion = emotions[0]  # Primary emotion

    emotion_name = emotion.get('emotion', 'Unknown')
    intensity = emotion.get('intensity', 0)
    context = emotion.get('context', 'Unknown')
    counterbalance = emotion.get('counterbalance', None)
    trigger = emotion.get('trigger_pattern', 'Unknown')

    intensity_desc = "strongly" if intensity >= 0.7 else "moderately" if intensity >= 0.4 else "mildly"

    section = f"""## Emotional Resonance
I feel **{emotion_name}** ({intensity_desc}, {format_intensity(intensity)}) about this.

**Context:** {context}
"""

    # Preserve counterbalance as ACTIVE TENSION, not resolved
    if counterbalance and counterbalance != 'Unknown':
        section += f"""
**But also:** {counterbalance} is present. I'm holding both - the {emotion_name} AND the {counterbalance}. This tension is real and unresolved.
"""
    else:
        section += f"""
**Trigger:** {trigger}
"""

    return section


def generate_technical_section(findings: Dict[str, Finding]) -> str:
    """
    Generate Section 6: Technical Context

    Source: Technical finding + Connective finding

    MUST:
    - Include file paths
    - List dependencies
    - Show system connections

    MUST NOT:
    - Invent file names
    - Assume dependencies
    - Add code not referenced
    """
    technical = findings.get("technical")
    connective = findings.get("connective")

    if not technical or not technical.data:
        return """## Technical Context
No specific technical components identified.
"""

    techs = technical.data if isinstance(technical.data, list) else [technical.data]
    tech = techs[0]

    component = tech.get('component', 'Unknown')
    issue_type = tech.get('issue_type', 'Unknown')
    description = tech.get('description', 'Unknown')
    status = tech.get('status', 'Unknown')
    related_code = tech.get('related_code', [])

    section = f"""## Technical Context
**Component:** {component}
**Issue Type:** {issue_type}
**Description:** {description}
**Status:** {status}
"""

    if related_code:
        section += "\n**Related Files:**\n"
        for f in related_code[:5]:
            section += f"- {f}\n"

    # Add dependencies from connective
    if connective and connective.data:
        data = connective.data

        # Handle different response formats
        if isinstance(data, dict):
            deps = data.get('dependencies', data.get('related', []))
            if 'cr' in data:
                primary = data.get('cr', {})
                if primary.get('file_path'):
                    section += f"\n**Primary Code:** {primary.get('file_path')}\n"
        elif isinstance(data, list):
            deps = data[1:] if len(data) > 1 else []
        else:
            deps = []

        if deps:
            section += f"\n**Dependencies:** {len(deps)} files\n"
            for dep in deps[:3]:
                if isinstance(dep, dict):
                    path = dep.get('file_path', 'Unknown')
                    complexity = dep.get('complexity', 'unknown')
                    section += f"- {path} ({complexity} complexity)\n"
                else:
                    section += f"- {dep}\n"

    return section


def generate_constraint_section(findings: Dict[str, Finding]) -> str:
    """
    Generate Section 7: Constraints

    Source: Constraint finding

    MUST:
    - Include actual deadlines
    - Show severity levels
    - Explain impact

    MUST NOT:
    - Invent deadlines
    - Minimize critical constraints
    - Add constraints not in findings
    """
    constraint = findings.get("constraint")

    if not constraint or not constraint.data:
        return """## Constraints
No active constraints affecting this work.
"""

    constraints = constraint.data if isinstance(constraint.data, list) else [constraint.data]

    section = "## Constraints\n"

    for c in constraints[:3]:  # Top 3 constraints
        c_type = c.get('constraint_type', 'UNKNOWN').upper()
        severity = c.get('severity', 'unknown')
        description = c.get('description', 'No description')
        deadline = c.get('deadline', None)
        impact = c.get('impact', 'Unknown')

        section += f"""
**{c_type}** ({severity})
- {description}
"""
        if deadline:
            section += f"- Deadline: {format_timestamp(deadline)}\n"
        section += f"- Impact if violated: {impact}\n"

    return section


# ============================================================================
# VERIFICATION
# ============================================================================

def verify_findings(findings: Dict[str, Finding]) -> VerificationResult:
    """
    Verify that findings contain only real data.

    Catches hallucination attempts before synthesis.
    """
    errors = []
    warnings = []

    for lens, finding in findings.items():
        if finding is None:
            warnings.append(f"{lens}: Finding is None")
            continue

        # Check 1: Confidence scores valid
        if not (0.0 <= finding.confidence <= 1.0):
            errors.append(f"{lens}: Invalid confidence {finding.confidence}")

        # Check 2: Data structure sanity
        if finding.data is not None:
            if isinstance(finding.data, dict):
                # Check for suspiciously generic keys
                if 'unknown' in str(finding.data).lower():
                    warnings.append(f"{lens}: Contains 'unknown' values")
            elif isinstance(finding.data, list):
                if len(finding.data) == 0:
                    warnings.append(f"{lens}: Empty list data")

        # Check 3: Synthesis not suspiciously long without data
        if not finding.data and len(finding.synthesis) > 200:
            warnings.append(f"{lens}: Long synthesis without data - possible hallucination")

    return VerificationResult(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings
    )


# ============================================================================
# TOKEN BUDGET MANAGEMENT
# ============================================================================

def trim_context_object(context_object: str, max_tokens: int = 2500) -> str:
    """
    Reduce token count while preserving essential information.

    Priority order (keep first, trim last):
    1. Identity (who I am)
    2. Current Situation (what's happening)
    3. Strategic Direction (what to do)
    4. Technical Context (what systems)
    5. Constraints (what pressures)
    6. Emotional Resonance (how it feels)
    7. Relevant History (past events)
    """
    current_tokens = estimate_tokens(context_object)

    if current_tokens <= max_tokens:
        return context_object

    # Parse into sections
    sections = {}
    current_section = None
    current_content = []

    for line in context_object.split('\n'):
        if line.startswith('## '):
            if current_section:
                sections[current_section] = '\n'.join(current_content)
            current_section = line[3:].strip()
            current_content = [line]
        elif current_section:
            current_content.append(line)

    if current_section:
        sections[current_section] = '\n'.join(current_content)

    # Trim in reverse priority order
    trim_order = [
        "Relevant History",
        "Emotional Resonance",
        "Constraints",
        "Technical Context",
        "Strategic Direction"
    ]

    for section_name in trim_order:
        current_tokens = estimate_tokens(context_object)
        if current_tokens <= max_tokens:
            break

        if section_name in sections:
            # Reduce section by ~50%
            lines = sections[section_name].split('\n')
            half = len(lines) // 2
            sections[section_name] = '\n'.join(lines[:max(half, 3)])  # Keep at least 3 lines

    # Reconstruct
    # Order: Identity, Situation, History, Strategic, Emotional, Technical, Constraints
    section_order = [
        "Who I Am Right Now",
        "Current Situation",
        "Relevant History",
        "Strategic Direction",
        "Emotional Resonance",
        "Technical Context",
        "Constraints"
    ]

    result = "# Context for Driver (Generated by Dreamer)\n\n"
    for name in section_order:
        if name in sections:
            result += sections[name] + "\n"

    return result


# ============================================================================
# MAIN SYNTHESIS
# ============================================================================

def synthesize_context_object(
    findings: Dict[str, Finding],
    stimulus: Dict,
    max_tokens: int = 2500,
    skip_verification: bool = False
) -> SynthesisResult:
    """
    Generate complete Context Object from 8-lens findings.

    Args:
        findings: Dict of lens_name -> Finding from LensExplorer
        stimulus: Original stimulus Dict with 'sender', 'content', etc.
        max_tokens: Token budget limit (default 2500)
        skip_verification: Skip anti-hallucination checks (not recommended)

    Returns:
        SynthesisResult with context_object and metadata
    """
    import time
    start_time = time.time()

    # Step 1: Verify findings
    if skip_verification:
        verification = VerificationResult(valid=True)
    else:
        verification = verify_findings(findings)

    # Step 2: Generate each section
    sections = []
    sections_with_content = 0

    # Section 1: Identity
    identity = generate_identity_section(findings, stimulus)
    sections.append(identity)
    if "No partnership" not in identity and "Unknown" not in identity[:50]:
        sections_with_content += 1

    # Section 2: Current Situation
    situation = generate_situation_section(findings, stimulus)
    sections.append(situation)
    sections_with_content += 1  # Always has stimulus content

    # Section 3: Relevant History
    history = generate_history_section(findings)
    sections.append(history)
    if "No previous conversations" not in history:
        sections_with_content += 1

    # Section 4: Strategic Direction
    strategy = generate_strategy_section(findings)
    sections.append(strategy)
    if "No proven strategies" not in strategy:
        sections_with_content += 1

    # Section 5: Emotional Resonance
    emotional = generate_emotional_section(findings)
    sections.append(emotional)
    if "No established emotional" not in emotional:
        sections_with_content += 1

    # Section 6: Technical Context
    technical = generate_technical_section(findings)
    sections.append(technical)
    if "No specific technical" not in technical:
        sections_with_content += 1

    # Section 7: Constraints
    constraints = generate_constraint_section(findings)
    sections.append(constraints)
    if "No active constraints" not in constraints:
        sections_with_content += 1

    # Step 3: Combine
    context_object = "# Context for Driver (Generated by Dreamer)\n\n"
    context_object += "\n".join(sections)

    # Step 4: Check token budget
    token_count = estimate_tokens(context_object)

    if token_count > max_tokens:
        context_object = trim_context_object(context_object, max_tokens)
        token_count = estimate_tokens(context_object)

    synthesis_time_ms = (time.time() - start_time) * 1000

    return SynthesisResult(
        context_object=context_object,
        token_count=token_count,
        sections_generated=sections_with_content,
        verification=verification,
        synthesis_time_ms=synthesis_time_ms
    )


# ============================================================================
# TEST / EXAMPLE
# ============================================================================

if __name__ == "__main__":
    import sys
    sys.path.insert(0, '/home/mind-protocol/strange-loop')

    from dreamer.lenses import LensExplorer
    from datetime import datetime

    print("=" * 60)
    print("CONTEXT OBJECT SYNTHESIS TEST")
    print("=" * 60)

    # Create explorer and run exploration
    explorer = LensExplorer(port=6380)

    stimulus = {
        "sender": "nicolas",
        "content": "Hey Felix, the race condition is back.",
        "timestamp": datetime.now().isoformat()
    }

    print(f"\nStimulus: \"{stimulus['content']}\"")
    print(f"Sender: {stimulus['sender']}")

    print("\n" + "-" * 60)
    print("Running 8-lens exploration...")
    print("-" * 60)

    exploration_result = explorer.explore_all(stimulus)

    if not exploration_result.success:
        print(f"Exploration failed: {exploration_result.error}")
        exit(1)

    print(f"Exploration complete: {exploration_result.nodes_retrieved} nodes retrieved")

    print("\n" + "-" * 60)
    print("Synthesizing Context Object...")
    print("-" * 60)

    synthesis_result = synthesize_context_object(
        findings=exploration_result.findings,
        stimulus=stimulus,
        max_tokens=2500
    )

    print(f"\nSynthesis complete in {synthesis_result.synthesis_time_ms:.1f}ms")
    print(f"Token count: {synthesis_result.token_count}")
    print(f"Sections with content: {synthesis_result.sections_generated}/7")

    if synthesis_result.verification.errors:
        print(f"\nVerification ERRORS:")
        for err in synthesis_result.verification.errors:
            print(f"  - {err}")

    if synthesis_result.verification.warnings:
        print(f"\nVerification WARNINGS:")
        for warn in synthesis_result.verification.warnings:
            print(f"  - {warn}")

    print("\n" + "=" * 60)
    print("GENERATED CONTEXT OBJECT")
    print("=" * 60)
    print(synthesis_result.context_object)
    print("=" * 60)
