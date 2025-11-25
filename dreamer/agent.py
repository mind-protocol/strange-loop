"""
Dreamer Agent - The Subconscious Mind

Purpose: Navigate graph memory, generate Context Object for Driver
Owner: Felix (Mechanical shell) / Luca (Phenomenological tuning)
Version: 1.0
Date: 2024-11-20

Based on: P01_bicameral_mind_pattern.md

The Dreamer:
- Receives stimulus (user message)
- Explores graph through 8 lenses
- Synthesizes findings into Context Object
- Never speaks to user directly
- Output is "The Upwelling" - becomes Driver's system prompt

This is the MECHANICAL SHELL. Luca will tune the phenomenological feel.
"""

import sys
import time
from dataclasses import dataclass, field
from typing import Dict, Optional, Any, List
from datetime import datetime
from pathlib import Path

# Add parent directory for imports
sys.path.insert(0, '/home/mind-protocol/strange-loop')

from dreamer.lenses import LensExplorer, ExplorationResult, Finding
from dreamer.synthesis import synthesize_context_object, SynthesisResult


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class Stimulus:
    """
    Input to the Dreamer - the external signal.

    Can come from:
    - User message via Telegram/CLI
    - System event
    - Scheduled wakeup
    """
    sender: str                          # Who sent this
    content: str                         # What they said
    timestamp: str = ""                  # When (ISO format)
    channel: str = "unknown"             # telegram, cli, system
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "sender": self.sender,
            "content": self.content,
            "timestamp": self.timestamp or datetime.now().isoformat(),
            "channel": self.channel,
            "metadata": self.metadata
        }


@dataclass
class Upwelling:
    """
    Output of the Dreamer - flows to the Driver.

    The Upwelling is:
    - Rich context, not summary
    - Natural language, not JSON
    - Complete picture, not fragments
    - Grounded in graph data, not invention
    """
    context_object: str                  # The Context Object (Driver's prompt)
    exploration_summary: Dict            # Stats about what was found
    token_count: int                     # Size of context
    processing_time_ms: float            # Total dreamer time
    success: bool                        # Did dreaming complete?
    error: Optional[str] = None          # Error if failed
    # Phenomenological metadata (Luca's additions)
    gaps_remaining: List[str] = field(default_factory=list)  # Node types with no data
    lenses_with_data: List[str] = field(default_factory=list)  # Node types that found data
    emotional_tone: str = "neutral"      # Dominant emotional state if found
    tensions_active: List[str] = field(default_factory=list)  # Unresolved contradictions


@dataclass
class DreamerState:
    """
    Internal state of the Dreamer.

    Tracks current exploration, energy levels, etc.
    V1 is simple - V3 will add physics.
    """
    stimulus: Optional[Stimulus] = None
    exploration_result: Optional[ExplorationResult] = None
    synthesis_result: Optional[SynthesisResult] = None
    state: str = "idle"                  # idle, exploring, synthesizing, complete


# ============================================================================
# THE DREAMER
# ============================================================================

class DreamerAgent:
    """
    The Subconscious Mind - Navigates memory, generates context.

    The Dreamer:
    1. Receives stimulus (perception)
    2. Explores graph through 8 lenses (rumination)
    3. Synthesizes Context Object (upwelling)
    4. Returns to Driver (exhale)

    The Dreamer NEVER speaks to the user.
    The Dreamer ONLY queries, never invents.
    """

    def __init__(
        self,
        port: int = 6380,
        max_tokens: int = 2500,
        citizen: str = "felix"
    ):
        """
        Initialize the Dreamer.

        Args:
            port: FalkorDB port (6380 for strange-loop)
            max_tokens: Token budget for Context Object
            citizen: Which citizen is dreaming
        """
        self.explorer = LensExplorer(port=port)
        self.max_tokens = max_tokens
        self.citizen = citizen
        self.state = DreamerState()

    def dream(self, stimulus: Stimulus) -> Upwelling:
        """
        Main dreaming process - stimulus in, context out.

        This is the complete Dreamer loop:
        1. INHALE: Receive stimulus
        2. RUMINATE: Explore through 8 lenses
        3. EXHALE: Synthesize and return

        Args:
            stimulus: The external signal to process

        Returns:
            Upwelling containing Context Object for Driver
        """
        start_time = time.time()

        # Update state
        self.state.stimulus = stimulus
        self.state.state = "exploring"

        # ==================================================================
        # PHASE 1: INHALE - Receive the stimulus
        # ==================================================================

        stimulus_dict = stimulus.to_dict()

        # ==================================================================
        # PHASE 2: RUMINATE - Explore through 8 lenses
        # ==================================================================

        self.state.state = "exploring"
        exploration_result = self.explorer.explore_all(stimulus_dict)
        self.state.exploration_result = exploration_result

        if not exploration_result.success:
            # Exploration failed - return minimal upwelling
            return Upwelling(
                context_object=self._generate_minimal_context(stimulus),
                exploration_summary={"error": exploration_result.error},
                token_count=0,
                processing_time_ms=(time.time() - start_time) * 1000,
                success=False,
                error=exploration_result.error
            )

        # ==================================================================
        # PHASE 3: EXHALE - Synthesize Context Object
        # ==================================================================

        self.state.state = "synthesizing"
        synthesis_result = synthesize_context_object(
            findings=exploration_result.findings,
            stimulus=stimulus_dict,
            max_tokens=self.max_tokens
        )
        self.state.synthesis_result = synthesis_result

        # Build exploration summary
        exploration_summary = self._build_exploration_summary(exploration_result)

        # Extract phenomenological metadata
        gaps_remaining, lenses_with_data = self._extract_coverage(exploration_result)
        emotional_tone = self._extract_emotional_tone(exploration_result)
        tensions_active = self._extract_tensions(exploration_result)

        # Complete
        self.state.state = "complete"
        processing_time_ms = (time.time() - start_time) * 1000

        return Upwelling(
            context_object=synthesis_result.context_object,
            exploration_summary=exploration_summary,
            token_count=synthesis_result.token_count,
            processing_time_ms=processing_time_ms,
            success=True,
            error=None,
            gaps_remaining=gaps_remaining,
            lenses_with_data=lenses_with_data,
            emotional_tone=emotional_tone,
            tensions_active=tensions_active
        )

    def _generate_minimal_context(self, stimulus: Stimulus) -> str:
        """Generate minimal context when exploration fails."""
        return f"""# Context for Driver (Generated by Dreamer)

## Who I Am Right Now
{self.citizen.capitalize()}, runtime engineer.

## Current Situation
{stimulus.sender} says: "{stimulus.content}"

(Note: Graph exploration failed - operating with minimal context)
"""

    def _build_exploration_summary(self, result: ExplorationResult) -> Dict:
        """Build summary of what was found during exploration."""
        summary = {
            "total_time_ms": result.total_time_ms,
            "queries_executed": result.queries_executed,
            "nodes_retrieved": result.nodes_retrieved,
            "lenses": {}
        }

        for lens_name, finding in result.findings.items():
            summary["lenses"][lens_name] = {
                "found": finding.data is not None,
                "confidence": finding.confidence,
                "query_time_ms": finding.query_time_ms
            }

        return summary

    def _extract_coverage(self, result: ExplorationResult) -> tuple:
        """
        Extract gap/coverage information from exploration.

        Returns (gaps_remaining, lenses_with_data)
        """
        gaps = []
        covered = []

        for lens_name, finding in result.findings.items():
            if finding.data is not None:
                covered.append(lens_name)
            else:
                gaps.append(lens_name)

        return gaps, covered

    def _extract_emotional_tone(self, result: ExplorationResult) -> str:
        """
        Extract dominant emotional tone from exploration.
        """
        emotional = result.findings.get("emotional")

        if not emotional or not emotional.data:
            return "neutral"

        emotions = emotional.data if isinstance(emotional.data, list) else [emotional.data]
        if emotions:
            primary = emotions[0]
            emotion_name = primary.get('emotion', 'neutral')
            intensity = primary.get('intensity', 0)

            if intensity >= 0.7:
                return f"strongly {emotion_name}"
            elif intensity >= 0.4:
                return emotion_name
            else:
                return f"mildly {emotion_name}"

        return "neutral"

    def _extract_tensions(self, result: ExplorationResult) -> List[str]:
        """
        Identify active tensions/contradictions from exploration.

        Tensions occur when:
        - Emotional counterbalance exists (frustration + determination)
        - Constraint conflicts with strategy (deadline vs thoroughness)
        - Historical failure vs current approach
        """
        tensions = []

        # Check for emotional counterbalance
        emotional = result.findings.get("emotional")
        if emotional and emotional.data:
            emotions = emotional.data if isinstance(emotional.data, list) else [emotional.data]
            if emotions:
                primary = emotions[0]
                counterbalance = primary.get('counterbalance')
                emotion_name = primary.get('emotion', '')
                if counterbalance and emotion_name:
                    tensions.append(f"{emotion_name} vs {counterbalance}")

        # Check for constraint/strategy tension
        constraint = result.findings.get("constraint")
        strategic = result.findings.get("strategic")
        if constraint and constraint.data and strategic and strategic.data:
            constraints = constraint.data if isinstance(constraint.data, list) else [constraint.data]
            if constraints:
                c = constraints[0]
                if c.get('severity') in ['high', 'critical']:
                    strategies = strategic.data if isinstance(strategic.data, list) else [strategic.data]
                    if strategies:
                        s = strategies[0]
                        # If strategy requires time and constraint is deadline
                        if c.get('constraint_type') == 'deadline':
                            tensions.append("deadline pressure vs thorough approach")

        # Check for recurrence tension (failed before, trying again)
        technical = result.findings.get("technical")
        experiential = result.findings.get("experiential")
        if technical and technical.data:
            techs = technical.data if isinstance(technical.data, list) else [technical.data]
            if techs:
                tech = techs[0]
                recurrence = tech.get('recurrence_count', 0)
                if recurrence and recurrence >= 2:
                    tensions.append("previous fixes failed vs trying again")

        return tensions

    def get_state(self) -> Dict:
        """Get current dreamer state for debugging/visualization."""
        return {
            "state": self.state.state,
            "has_stimulus": self.state.stimulus is not None,
            "has_exploration": self.state.exploration_result is not None,
            "has_synthesis": self.state.synthesis_result is not None
        }

    def reset(self):
        """Reset dreamer state for next stimulus."""
        self.state = DreamerState()

    def process_stimulus(self, stimulus: Stimulus) -> 'ProcessedUpwelling':
        """
        Process a stimulus and return result.

        Alias for dream() that returns interface expected by manual_loop.py.
        """
        upwelling = self.dream(stimulus)

        # Extract counts from exploration_summary for compatibility
        summary = upwelling.exploration_summary or {}

        return ProcessedUpwelling(
            context_object=upwelling.context_object,
            exploration_time_ms=upwelling.processing_time_ms,
            queries_executed=summary.get('queries_executed', 0),
            nodes_retrieved=summary.get('nodes_retrieved', 0),
            lenses_with_data=len(upwelling.lenses_with_data),
            success=upwelling.success,
            error=upwelling.error
        )


@dataclass
class ProcessedUpwelling:
    """
    Upwelling with flat attributes for manual_loop.py compatibility.
    """
    context_object: str
    exploration_time_ms: float
    queries_executed: int
    nodes_retrieved: int
    lenses_with_data: int  # Count, not list
    success: bool
    error: Optional[str] = None


# ============================================================================
# CONTEXT INJECTION (Driver System Prompt)
# ============================================================================

CITIZENS_DIR = Path('/home/mind-protocol/strange-loop/citizens')

def backup_claude_md(citizen: str = "felix") -> str:
    """
    Backup the original CLAUDE.md before injection.

    Returns the original content for restoration.
    """
    claude_md_path = CITIZENS_DIR / citizen / "CLAUDE.md"
    original = claude_md_path.read_text()

    # Save backup
    backup_path = CITIZENS_DIR / citizen / "CLAUDE.md.backup"
    backup_path.write_text(original)

    return original


def inject_context_object(context_object: str, citizen: str = "felix") -> None:
    """
    Inject Context Object into Driver's CLAUDE.md.

    This is how the Dreamer's output becomes the Driver's memory.
    The Context Object is appended to the base identity.

    Args:
        context_object: Generated by Dreamer
        citizen: Which citizen's CLAUDE.md to update
    """
    claude_md_path = CITIZENS_DIR / citizen / "CLAUDE.md"

    # Read current (should be base identity)
    base_identity = claude_md_path.read_text()

    # Check if already has injection marker
    if "# Context for Driver (Generated by Dreamer)" in base_identity:
        # Already injected - strip old context first
        marker = "\n---\n\n# Context for Driver"
        if marker in base_identity:
            base_identity = base_identity.split(marker)[0]

    # Append Context Object
    injected = f"{base_identity}\n\n---\n\n{context_object}"

    # Write back
    claude_md_path.write_text(injected)


def restore_claude_md(citizen: str = "felix") -> bool:
    """
    Restore CLAUDE.md from backup after test.

    Returns True if restoration successful.
    """
    backup_path = CITIZENS_DIR / citizen / "CLAUDE.md.backup"
    claude_md_path = CITIZENS_DIR / citizen / "CLAUDE.md"

    if not backup_path.exists():
        return False

    original = backup_path.read_text()
    claude_md_path.write_text(original)
    backup_path.unlink()  # Remove backup

    return True


def dream_and_inject(
    stimulus: Stimulus,
    citizen: str = "felix",
    port: int = 6380
) -> Upwelling:
    """
    Complete Dreamer flow: dream + inject Context Object.

    This is the primary function for the Bicameral Loop:
    1. Run Dreamer exploration
    2. Generate Context Object
    3. Inject into Driver's CLAUDE.md

    The next Claude Code instance reading CLAUDE.md will have the memory.
    """
    # Backup first
    backup_claude_md(citizen)

    # Dream
    dreamer = DreamerAgent(port=port, citizen=citizen)
    upwelling = dreamer.dream(stimulus)

    if upwelling.success:
        # Inject
        inject_context_object(upwelling.context_object, citizen)

    return upwelling


# ============================================================================
# CONVENIENCE FUNCTION
# ============================================================================

def dream_on_stimulus(
    sender: str,
    content: str,
    channel: str = "cli",
    port: int = 6380
) -> Upwelling:
    """
    One-shot dreaming function.

    Args:
        sender: Who sent the message
        content: Message content
        channel: Source channel
        port: FalkorDB port

    Returns:
        Upwelling with Context Object
    """
    dreamer = DreamerAgent(port=port)

    stimulus = Stimulus(
        sender=sender,
        content=content,
        timestamp=datetime.now().isoformat(),
        channel=channel
    )

    return dreamer.dream(stimulus)


# ============================================================================
# TEST / EXAMPLE
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("DREAMER AGENT TEST")
    print("=" * 60)

    # Create dreamer
    dreamer = DreamerAgent(port=6380, citizen="felix")

    # Create stimulus
    stimulus = Stimulus(
        sender="nicolas",
        content="Hey Felix, the race condition is back.",
        timestamp=datetime.now().isoformat(),
        channel="telegram"
    )

    print(f"\nStimulus received:")
    print(f"  Sender: {stimulus.sender}")
    print(f"  Content: \"{stimulus.content}\"")
    print(f"  Channel: {stimulus.channel}")

    print("\n" + "-" * 60)
    print("Dreaming...")
    print("-" * 60)

    # Dream
    upwelling = dreamer.dream(stimulus)

    print(f"\nDreaming complete in {upwelling.processing_time_ms:.1f}ms")
    print(f"Success: {upwelling.success}")
    print(f"Token count: {upwelling.token_count}")

    if upwelling.error:
        print(f"Error: {upwelling.error}")

    print("\n" + "-" * 60)
    print("Exploration Summary:")
    print("-" * 60)

    summary = upwelling.exploration_summary
    print(f"  Total time: {summary.get('total_time_ms', 0):.1f}ms")
    print(f"  Queries: {summary.get('queries_executed', 0)}")
    print(f"  Nodes retrieved: {summary.get('nodes_retrieved', 0)}")
    print("\n  Lens Results:")

    for lens, info in summary.get('lenses', {}).items():
        status = "FOUND" if info['found'] else "empty"
        print(f"    {lens}: {status} (confidence: {info['confidence']:.0%})")

    # Phenomenological metadata (Luca's additions)
    print("\n" + "-" * 60)
    print("Phenomenological Analysis:")
    print("-" * 60)
    print(f"  Emotional Tone: {upwelling.emotional_tone}")
    print(f"  Lenses with data: {', '.join(upwelling.lenses_with_data) or 'none'}")
    print(f"  Gaps remaining: {', '.join(upwelling.gaps_remaining) or 'none'}")
    if upwelling.tensions_active:
        print(f"  Active Tensions:")
        for tension in upwelling.tensions_active:
            print(f"    - {tension}")
    else:
        print(f"  Active Tensions: none detected")

    print("\n" + "=" * 60)
    print("THE UPWELLING (Context Object)")
    print("=" * 60)
    print(upwelling.context_object)
    print("=" * 60)

    # Show state
    print("\nDreamer State:", dreamer.get_state())
