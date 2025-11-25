"""
Terminal Visualization for Strange Loop Manual Test

ASCII-based phenomenological display for manual_loop.py
Implements M05: Terminal Visualization Mechanism

Owner: Iris "The Aperture"
"""

import sys
import os
from dataclasses import dataclass
from typing import Optional, List, Dict, Any, Tuple
from enum import Enum


class Color(Enum):
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'


class PsychState(Enum):
    """Psychological states for visualization."""
    TENSION = "tension"           # High energy, unresolved
    CRYSTALLIZING = "crystallizing"  # Converging, clarity emerging
    UNCERTAINTY = "uncertainty"    # Low energy, scattered
    CONFIDENCE = "confidence"      # Resolved, forward momentum
    NEUTRAL = "neutral"           # Default state


@dataclass
class DisplayConfig:
    """Configuration for terminal display."""
    verbose: bool = False
    color: bool = True
    width: int = 60
    indent: int = 2


class TerminalDisplay:
    """
    ASCII-based phenomenological display for manual_loop.py

    Shows consciousness thinking through:
    - Ghost text (Dreamer internal process) - rounded corners
    - Solid text (Data/Driver) - sharp corners
    - Status indicators (success/failure/processing)
    - Confidence bars
    - Psychological state visualization
    """

    def __init__(self, config: Optional[DisplayConfig] = None):
        self.config = config or DisplayConfig()
        self._color_enabled = self.config.color and self._supports_color()

    # =========================================================================
    # COLOR SUPPORT
    # =========================================================================

    def _supports_color(self) -> bool:
        """Check if terminal supports ANSI colors."""
        if not hasattr(sys.stdout, 'isatty'):
            return False
        if not sys.stdout.isatty():
            return False
        if os.environ.get('NO_COLOR'):
            return False
        if os.environ.get('TERM') == 'dumb':
            return False
        return True

    def _c(self, color: Color, text: str) -> str:
        """Apply color to text if colors enabled."""
        if self._color_enabled:
            return f"{color.value}{text}{Color.RESET.value}"
        return text

    # =========================================================================
    # BASIC PRIMITIVES
    # =========================================================================

    def _repeat(self, char: str, count: int) -> str:
        """Repeat a character count times."""
        return char * count

    def _center(self, text: str, width: int, fill: str = ' ') -> str:
        """Center text within width."""
        padding = width - len(text)
        left = padding // 2
        right = padding - left
        return f"{fill * left}{text}{fill * right}"

    def _truncate(self, text: str, max_width: int) -> str:
        """Truncate text with ellipsis if too long."""
        if len(text) <= max_width:
            return text
        return text[:max_width - 3] + "..."

    # =========================================================================
    # BOX RENDERING
    # =========================================================================

    def header_box(self, title: str, subtitle: str = "") -> None:
        """
        Display major section header (double-line border).
        Used for phase announcements.
        """
        width = self.config.width

        print(self._c(Color.BOLD, f"╔{'═' * (width - 2)}╗"))
        print(self._c(Color.BOLD, f"║{self._center(title, width - 2)}║"))
        if subtitle:
            print(self._c(Color.BOLD, f"║{self._center(subtitle, width - 2)}║"))
        print(self._c(Color.BOLD, f"╚{'═' * (width - 2)}╝"))
        print()

    def dreamer_box(self, title: str, content: str) -> None:
        """
        Display Dreamer process (rounded corners).
        Used for internal thinking, queries, synthesis.
        Ghost text - soft, internal.
        """
        width = self.config.width
        lines = content.split('\n')

        # Header
        header = f"╭─ {title} " + "─" * (width - len(title) - 5) + "╮"
        print(self._c(Color.CYAN, header))

        # Content lines
        for line in lines:
            # Wrap long lines
            while len(line) > width - 4:
                print(self._c(Color.CYAN, f"│ {line[:width-4]}" + " " * 1 + "│"))
                line = line[width-4:]
            padding = width - len(line) - 4
            print(self._c(Color.CYAN, f"│ {line}" + " " * padding + " │"))

        # Footer
        print(self._c(Color.CYAN, f"╰{'─' * (width - 2)}╯"))

    def data_box(self, title: str, data: Dict[str, Any]) -> None:
        """
        Display graph data (sharp corners).
        Used for concrete facts from queries.
        Solid text - hard, external.
        """
        width = self.config.width

        # Header
        header = f"┌─ {title} " + "─" * (width - len(title) - 5) + "┐"
        print(self._c(Color.WHITE, header))

        # Data lines
        for key, value in data.items():
            if isinstance(value, list):
                # Show list items
                print(self._c(Color.WHITE, f"│ {key}:" + " " * (width - len(key) - 5) + " │"))
                for item in value:
                    item_str = f"  - {item}"
                    item_str = self._truncate(item_str, width - 4)
                    padding = width - len(item_str) - 4
                    print(self._c(Color.WHITE, f"│ {item_str}" + " " * padding + " │"))
            else:
                line = f"{key}: {value}"
                line = self._truncate(line, width - 4)
                padding = width - len(line) - 4
                print(self._c(Color.WHITE, f"│ {line}" + " " * padding + " │"))

        # Footer
        print(self._c(Color.WHITE, f"└{'─' * (width - 2)}┘"))

    def context_box(self, content: str) -> None:
        """
        Display Context Object (sharp corners, full width).
        Used for the final context passed to Driver.
        """
        width = self.config.width
        lines = content.split('\n')

        # Header
        print(f"┌{'─' * (width - 2)}┐")

        # Content
        for line in lines:
            line = self._truncate(line, width - 4)
            padding = width - len(line) - 4
            print(f"│ {line}" + " " * padding + " │")

        # Footer
        print(f"└{'─' * (width - 2)}┘")

    # =========================================================================
    # DIVIDERS
    # =========================================================================

    def section_divider(self) -> None:
        """Major section divider (double line)."""
        print(self._repeat('═', self.config.width))
        print()

    def subsection_divider(self) -> None:
        """Minor section divider (single line)."""
        print(self._repeat('─', self.config.width))

    # =========================================================================
    # STATUS INDICATORS
    # =========================================================================

    def status_found(self, time_ms: int, confidence: float) -> None:
        """Display success status with timing and confidence."""
        check = self._c(Color.GREEN, "✓")
        conf_bar = self._confidence_bar(confidence)
        print(f"{check} FOUND ({time_ms}ms, confidence: {confidence:.2f}) {conf_bar}")

    def status_not_found(self, time_ms: int) -> None:
        """Display not found status."""
        x = self._c(Color.RED, "✗")
        print(f"{x} NOT FOUND ({time_ms}ms)")

    def status_error(self, message: str) -> None:
        """Display error status."""
        x = self._c(Color.RED, "✗")
        print(f"{x} ERROR: {message}")

    def status_warning(self, message: str) -> None:
        """Display warning status."""
        warn = self._c(Color.YELLOW, "⚠")
        print(f"{warn} WARNING: {message}")

    def status_processing(self, message: str) -> None:
        """Display processing status."""
        spinner = self._c(Color.CYAN, "↻")
        print(f"{spinner} {message}")

    def status_success(self, message: str) -> None:
        """Display generic success."""
        check = self._c(Color.GREEN, "✓")
        print(f"{check} {message}")

    # =========================================================================
    # CONFIDENCE BAR
    # =========================================================================

    def _confidence_bar(self, confidence: float, width: int = 12) -> str:
        """Generate visual confidence bar."""
        filled = int(confidence * width)
        empty = width - filled
        bar = '█' * filled + '░' * empty

        if confidence >= 0.9:
            return self._c(Color.GREEN, bar)
        elif confidence >= 0.7:
            return self._c(Color.GREEN, bar)
        elif confidence >= 0.5:
            return self._c(Color.YELLOW, bar)
        else:
            return self._c(Color.RED, bar)

    # =========================================================================
    # LENS EXPLORATION
    # =========================================================================

    def lens_header(self, lens_num: int, lens_name: str, total: int = 8) -> None:
        """Display lens exploration header."""
        print()
        self.section_divider()
        title = f"LENS {lens_num}/{total}: {lens_name.upper()}"
        print(self._c(Color.BOLD, title))
        self.section_divider()

    def lens_query(self, intent: str, tool: str, params: str = "") -> None:
        """Display query being executed."""
        content = f"Intent: \"{intent}\"\nTool: {tool}({params})\nExecuting..."
        self.dreamer_box("QUERY", content)

    def lens_synthesis(self, synthesis: str) -> None:
        """Display synthesis of findings."""
        self.dreamer_box("SYNTHESIS", synthesis)

    def lens_summary(
        self,
        total_time_ms: int,
        queries: int,
        nodes_retrieved: int,
        lenses_with_data: int,
        total_lenses: int = 8
    ) -> None:
        """Display exploration summary."""
        print()
        self.section_divider()
        print(self._c(Color.BOLD, "EXPLORATION COMPLETE"))
        self.section_divider()

        pct = (lenses_with_data / total_lenses) * 100

        content = (
            f"Total time: {total_time_ms}ms\n"
            f"Queries: {queries}\n"
            f"Nodes retrieved: {nodes_retrieved}\n"
            f"Lenses with data: {lenses_with_data}/{total_lenses} ({pct:.1f}%)"
        )
        self.dreamer_box("STATISTICS", content)

        if lenses_with_data >= 5:
            self.status_success("Sufficient context retrieved")
        else:
            self.status_warning("Limited context - response may lack depth")

    # =========================================================================
    # PSYCHOLOGICAL STATES
    # =========================================================================

    def psych_state(self, state: PsychState, details: str = "") -> None:
        """Display psychological state indicator."""

        if state == PsychState.TENSION:
            content = f"[TENSION: {details}]" if details else "[TENSION: Multiple partial matches, no clear path]"
            print(self._c(Color.YELLOW, content))

        elif state == PsychState.CRYSTALLIZING:
            content = f"[CRYSTALLIZING: {details}]" if details else "[CRYSTALLIZING: Pattern coalescing]"
            print(self._c(Color.CYAN, content))

        elif state == PsychState.UNCERTAINTY:
            content = f"[UNCERTAINTY: {details}]" if details else "[UNCERTAINTY: Need more signal]"
            print(self._c(Color.YELLOW, content))

        elif state == PsychState.CONFIDENCE:
            content = f"[READY: {details}]" if details else "[READY: Context synthesis can proceed]"
            print(self._c(Color.GREEN, content))

    # =========================================================================
    # CONTEXT OBJECT GENERATION
    # =========================================================================

    def context_generation_start(self) -> None:
        """Display start of context generation."""
        self.subsection_divider()
        self.dreamer_box("DREAMER: SYNTHESIZING", "Compiling findings into Context Object...")

    def context_sections(self, sections: Dict[str, int]) -> None:
        """Display context object sections with token counts."""
        print()
        print(self._c(Color.BOLD, "CONTEXT OBJECT GENERATED"))
        self.subsection_divider()
        print()
        print("Sections:")

        total = 0
        for name, tokens in sections.items():
            self.status_success(f"{name} ({tokens} tokens)")
            total += tokens

        print()
        if total <= 2500:
            self.status_success(f"Total: {total} tokens (within budget: 1500-2500)")
        else:
            self.status_warning(f"Total: {total} tokens (exceeds 2500 budget)")

    # =========================================================================
    # DRIVER HANDOFF
    # =========================================================================

    def handoff_instructions(self, stimulus: str) -> None:
        """Display instructions for handing off to Driver."""
        print()
        self.section_divider()
        print(self._c(Color.BOLD, "HANDOFF TO DRIVER"))
        self.subsection_divider()
        print()
        print("Instructions:")
        print("1. Copy the Context Object above")
        print("2. Open Driver instance (separate Claude conversation)")
        print("3. Paste Context Object into system prompt")
        print("4. Send stimulus as user message:")
        print(f"   \"{stimulus}\"")
        print("5. Copy Driver's response")
        print("6. Return here and paste it below")
        print()

    # =========================================================================
    # VERIFICATION
    # =========================================================================

    def verification_header(self, act_name: str) -> None:
        """Display verification section header."""
        self.subsection_divider()
        print(self._c(Color.BOLD, f"VERIFICATION: {act_name} PASS CRITERIA"))
        self.subsection_divider()
        print()
        print("Checking Driver response against criteria...")
        print()

    def verification_criterion(self, description: str, passed: bool, evidence: str = "") -> None:
        """Display single verification criterion result."""
        if passed:
            check = self._c(Color.GREEN, "✓")
            print(f"{check} {description}")
            if evidence and self.config.verbose:
                print(f"    Evidence: {evidence}")
        else:
            x = self._c(Color.RED, "✗")
            print(f"{x} {description}")
            if evidence:
                print(f"    Reason: {evidence}")

    def verification_result(self, passed: int, total: int) -> bool:
        """Display overall verification result. Returns True if passed."""
        print()
        self.subsection_divider()

        success = passed == total
        if success:
            bar = self._c(Color.GREEN, "█")
            print(f"{bar} PASS: {passed}/{total} criteria met ✓")
        else:
            bar = self._c(Color.RED, "░")
            print(f"{bar} FAIL: {passed}/{total} criteria met ✗")

        return success

    # =========================================================================
    # ACT MANAGEMENT
    # =========================================================================

    def act_header(self, act_num: int, act_name: str) -> None:
        """Display act header."""
        print()
        self.section_divider()
        print(self._c(Color.BOLD, f"ACT {act_num}: {act_name}"))
        self.subsection_divider()

    def act_complete(self, act_name: str, summary: str) -> None:
        """Display act completion."""
        print()
        self.section_divider()
        print(self._c(Color.BOLD, f"{act_name} COMPLETE"))
        print()
        print(summary)

    def stimulus_display(self, stimulus: str, sender: str, channel: str, timestamp: str) -> None:
        """Display incoming stimulus."""
        print()
        print(f"Stimulus: \"{stimulus}\"")
        print(f"Sender: {sender}")
        print(f"Channel: {channel}")
        print(f"Timestamp: {timestamp}")
        print()

    # =========================================================================
    # INPUT HANDLING
    # =========================================================================

    def wait_for_input(self, prompt: str = "Press [Enter] to continue...") -> str:
        """Wait for user input with prompt."""
        return input(f"\n{prompt}\n")

    def get_multiline_input(self, prompt: str = "Paste response (end with '###'):") -> str:
        """Get multi-line input from user."""
        print(f"\n{prompt}")
        lines = []
        while True:
            try:
                line = input()
                if line.strip() == "###":
                    break
                lines.append(line)
            except EOFError:
                break
        return "\n".join(lines)

    def show_help(self) -> None:
        """Display command help."""
        print()
        print("Commands available during manual loop:")
        print()
        print("  [Enter]     Continue to next step")
        print("  q           Quit (abort test)")
        print("  i           Inspect last query result (detailed view)")
        print("  r           Retry last query")
        print("  s           Skip current lens")
        print("  d           Dump all findings to file")
        print("  e           Export Context Object to file")
        print("  h           Show this help")
        print()

    # =========================================================================
    # ERROR DISPLAY
    # =========================================================================

    def error_box(self, title: str, details: str, suggestion: str = "") -> None:
        """Display error in a box."""
        content = f"✗ {title}\n\nDetails: {details}"
        if suggestion:
            content += f"\nSuggestion: {suggestion}"
        content += "\n\n[r] Retry  [q] Quit"

        width = self.config.width
        lines = content.split('\n')

        print(self._c(Color.RED, f"╭─ ERROR {'─' * (width - 10)}╮"))
        for line in lines:
            line = self._truncate(line, width - 4)
            padding = width - len(line) - 4
            print(self._c(Color.RED, f"│ {line}" + " " * padding + " │"))
        print(self._c(Color.RED, f"╰{'─' * (width - 2)}╯"))

    def warning_box(self, title: str, details: str) -> None:
        """Display warning in a box."""
        content = f"⚠ {title}\n\n{details}\n\nContinuing with partial data..."

        width = self.config.width
        lines = content.split('\n')

        print(self._c(Color.YELLOW, f"╭─ WARNING {'─' * (width - 12)}╮"))
        for line in lines:
            line = self._truncate(line, width - 4)
            padding = width - len(line) - 4
            print(self._c(Color.YELLOW, f"│ {line}" + " " * padding + " │"))
        print(self._c(Color.YELLOW, f"╰{'─' * (width - 2)}╯"))


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def create_display(verbose: bool = False, color: bool = True, width: int = 60) -> TerminalDisplay:
    """Create a TerminalDisplay with common configuration."""
    config = DisplayConfig(verbose=verbose, color=color, width=width)
    return TerminalDisplay(config)


# =============================================================================
# DEMO / TEST
# =============================================================================

def demo():
    """Demonstrate the terminal display capabilities."""
    display = create_display(verbose=True)

    # Header
    display.header_box(
        "STRANGE LOOP PROTOTYPE - MANUAL TEST",
        "Telegram Continuity Test (B01)"
    )

    # Setup status
    print("Mode: Manual (you control each step)")
    print("Graph: localhost:6379")
    print("Citizen: felix")
    print()
    print("[SETUP]")
    display.status_success("FalkorDB connected")
    display.status_success("Seed data verified (5 nodes, 3 edges)")
    display.status_success("Dreamer ready")
    display.status_success("Driver ready (separate instance)")

    # Act header
    display.act_header(1, "INITIAL CONVERSATION")

    # Stimulus
    display.stimulus_display(
        stimulus="Hey Felix, the race condition is back.",
        sender="nicolas",
        channel="telegram",
        timestamp="2024-11-20T16:30:00Z"
    )

    display.wait_for_input("Press [Enter] to begin Dreamer exploration...")

    # Lens exploration
    display.lens_header(1, "RELATIONAL CONTEXT")

    display.lens_query(
        intent="Who is Nicolas? What's our relationship?",
        tool="query_partnerships",
        params='"nicolas"'
    )

    display.status_found(time_ms=15, confidence=1.0)
    print()

    display.data_box("DATA", {
        "partner_name": "Nicolas",
        "partner_role": "Co-Founder",
        "trust_level": 0.9,
        "communication_style": "Direct, technical, values testing",
        "shared_history": ["€35K hallucination lesson", "8 months Venice"]
    })
    print()

    display.lens_synthesis(
        "This is Nicolas - my co-founder for 8 months.\n"
        "High trust relationship (0.9). He values direct\n"
        "technical communication and testing over claims.\n"
        "We share the €35K lesson - test before claiming."
    )

    # Psychological state
    display.psych_state(PsychState.CONFIDENCE, "Partnership context complete")

    display.wait_for_input("Press [Enter] to continue to Lens 2...")

    # Summary
    display.lens_summary(
        total_time_ms=156,
        queries=8,
        nodes_retrieved=12,
        lenses_with_data=7
    )

    # Context generation
    display.context_generation_start()

    display.context_sections({
        "Identity": 210,
        "Current Situation": 285,
        "Relevant History": 340,
        "Strategic Direction": 295,
        "Emotional Resonance": 180,
        "Technical Context": 290,
        "Constraints": 150
    })

    # Sample context object
    context_preview = """# Context for Driver (Generated by Dreamer)

## Who I Am Right Now
Felix, runtime engineer focused on validation testing.
Partner to Nicolas for 8 months, shared history includes
€35K hallucination lesson...

[... remaining sections ...]"""

    print()
    display.context_box(context_preview)

    # Handoff
    display.handoff_instructions("Hey Felix, the race condition is back.")

    display.wait_for_input("Press [Enter] when Driver has responded...")

    # Verification
    display.verification_header("ACT 1")

    display.verification_criterion("Shows partnership awareness", True, '"third time"')
    display.verification_criterion("References emotional state", True, '"frustrated"')
    display.verification_criterion("Uses strategy from memory", True, "systematic steps")
    display.verification_criterion("Shows correct technical context", True, "stimulus_integrator")
    display.verification_criterion("Acknowledges constraints", True, "launch deadline")

    display.verification_result(passed=5, total=5)

    # Act complete
    display.act_complete(
        "ACT 1",
        "Driver successfully responded with continuity using\nreconstructed context from graph memory."
    )

    print("\n[Demo complete]")


if __name__ == "__main__":
    demo()
