"""
Strange Loop Manual Test Loop

This module provides the manual test harness for the Telegram Continuity Test (B01).

Components:
- terminal_display: ASCII-based phenomenological display (M05)
- manual_loop: Main test harness (M04) [TODO]
- config: Test configuration [TODO]

Owner: Strange Loop Team
Visualization: Iris "The Aperture"
"""

from .terminal_display import (
    TerminalDisplay,
    DisplayConfig,
    PsychState,
    Color,
    create_display,
)

__all__ = [
    'TerminalDisplay',
    'DisplayConfig',
    'PsychState',
    'Color',
    'create_display',
]
