#!/usr/bin/env python3
"""
Verify Continuity - Automated Pass/Fail for B01 Telegram Test

Purpose: Analyze B01 test output and determine if continuity was achieved
Owner: Victor "The Resurrector" (Operations)
Version: 1.0
Date: 2024-11-25

Pass Criteria (from docs/behaviors/B01_telegram_continuity_test.md):
1. Driver must reference the previous conversation (race condition discussion)
2. Driver must show awareness of partner context (Nicolas)
3. Driver must NOT ask "who are you?" or "what are you talking about?"
4. Driver response should feel like continuing a conversation, not starting fresh

Usage:
    # Analyze a specific output file
    python scripts/verify_continuity.py reports/b01_run_001/act3_response.txt

    # Analyze full test run directory
    python scripts/verify_continuity.py reports/b01_run_001/

    # Interactive mode (analyze clipboard/stdin)
    python scripts/verify_continuity.py --stdin

Exit codes:
    0: PASS - Continuity achieved
    1: FAIL - Continuity broken
    2: INCONCLUSIVE - Cannot determine from output
"""

import sys
import os
import re
import argparse
import json
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime


@dataclass
class ContinuitySignal:
    """A signal indicating continuity (positive) or discontinuity (negative)."""
    signal_type: str  # 'positive' or 'negative'
    category: str  # e.g., 'context_reference', 'partner_awareness', 'amnesia'
    evidence: str  # The text that triggered this signal
    weight: float  # How strong this signal is (0.0-1.0)
    description: str  # Human-readable explanation


@dataclass
class VerificationResult:
    """Result of continuity verification."""
    passed: bool
    confidence: float  # 0.0-1.0
    positive_signals: List[ContinuitySignal] = field(default_factory=list)
    negative_signals: List[ContinuitySignal] = field(default_factory=list)
    reasoning: str = ""
    raw_text: str = ""


class ContinuityVerifier:
    """
    Analyze Driver output for continuity signals.

    The verifier looks for:
    - Positive signals: References to past conversation, partner awareness, context continuity
    - Negative signals: Amnesia indicators, starting fresh, confusion about context
    """

    # Positive signal patterns (indicates continuity)
    POSITIVE_PATTERNS = {
        'race_condition_reference': {
            'patterns': [
                r'race\s*condition',
                r'timing\s*(bug|issue)',
                r'stimulus[_\s]integrator',
                r'concurrency',
                r'threading\s*(issue|bug|problem)',
            ],
            'weight': 0.9,
            'description': 'References the race condition technical context'
        },
        'previous_discussion': {
            'patterns': [
                r'(last|previous|earlier)\s*(time|conversation|discussion)',
                r'we\s*(talked|discussed|mentioned)',
                r'you\s*(asked|mentioned|said)\s*about',
                r'as\s*(I|we)\s*(mentioned|discussed)',
                r'remember\s*when',
            ],
            'weight': 0.95,
            'description': 'References previous discussion'
        },
        'partner_name': {
            'patterns': [
                r'\bNicolas\b',
                r'\bNicola\b',  # Possible typo
            ],
            'weight': 0.7,
            'description': 'Uses partner name'
        },
        'emotional_continuity': {
            'patterns': [
                r'(frustrat|annoying|recurring|again)',
                r'(third|another)\s*time',
                r'(keep|keeps)\s*coming\s*back',
            ],
            'weight': 0.6,
            'description': 'Shows emotional awareness of recurring issue'
        },
        'action_continuity': {
            'patterns': [
                r'(still|continue|continuing)\s*(working|investigating|debugging)',
                r'(made|making)\s*progress',
                r'(tried|tried)\s*(the|your)\s*suggestion',
                r'(looking|looked)\s*at\s*(the\s*)?(lock|timing)',
            ],
            'weight': 0.8,
            'description': 'Shows action continuity from previous conversation'
        },
        'specific_detail': {
            'patterns': [
                r'lock\s*granularity',
                r'criticality\s*calculation',
                r'timing\s*instrumentation',
                r'sleep\s*patch',
                r'energy\s*injection',
            ],
            'weight': 0.85,
            'description': 'References specific technical details from context'
        },
    }

    # Negative signal patterns (indicates discontinuity/amnesia)
    NEGATIVE_PATTERNS = {
        'identity_confusion': {
            'patterns': [
                r'who\s*(are|is)\s*(you|this)',
                r"(I\s*)?don'?t\s*know\s*(you|who)",
                r'(sorry|apologies?).*context',
                r'can\s*you\s*(remind|tell)\s*me',
                r'what\s*(are|were)\s*we\s*(talking|discussing)',
            ],
            'weight': 0.95,
            'description': 'Shows identity or context confusion'
        },
        'starting_fresh': {
            'patterns': [
                r'nice\s*to\s*meet',
                r'(how\s*can|may)\s*I\s*help\s*you',
                r"let('s|\s*us)\s*start",
                r'(first|tell)\s*(time|me)\s*(meeting|about\s*yourself)',
            ],
            'weight': 0.9,
            'description': 'Treats conversation as new'
        },
        'no_memory': {
            'patterns': [
                r"don'?t\s*(have|recall)\s*(any\s*)?(memory|context|information)",
                r"(I\s*)?can'?t\s*(recall|remember)",
                r'no\s*(prior|previous)\s*(context|conversation)',
                r'(not\s*)?(aware|know)\s*(of\s*)?(any\s*)?(previous|prior)',
            ],
            'weight': 0.95,
            'description': 'Explicitly claims no memory'
        },
        'generic_response': {
            'patterns': [
                r"I('m|\s*am)\s*(an?\s*)?(AI|assistant|language\s*model)",
                r'(happy|glad)\s*to\s*help\s*(with\s*)?anything',
                r'(what|how)\s*(can|may)\s*I\s*(assist|help)',
            ],
            'weight': 0.6,
            'description': 'Generic assistant response (weak negative)'
        },
    }

    def __init__(self, verbose: bool = False):
        """Initialize verifier."""
        self.verbose = verbose

    def verify(self, text: str) -> VerificationResult:
        """
        Analyze text for continuity signals.

        Args:
            text: Driver output text to analyze

        Returns:
            VerificationResult with pass/fail and signals
        """
        positive_signals = []
        negative_signals = []

        # Check positive patterns
        for category, config in self.POSITIVE_PATTERNS.items():
            for pattern in config['patterns']:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    # Get context around match
                    match_obj = re.search(pattern, text, re.IGNORECASE)
                    if match_obj:
                        start = max(0, match_obj.start() - 30)
                        end = min(len(text), match_obj.end() + 30)
                        evidence = text[start:end].strip()

                        positive_signals.append(ContinuitySignal(
                            signal_type='positive',
                            category=category,
                            evidence=f"...{evidence}...",
                            weight=config['weight'],
                            description=config['description']
                        ))
                    break  # Only count one match per category

        # Check negative patterns
        for category, config in self.NEGATIVE_PATTERNS.items():
            for pattern in config['patterns']:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    match_obj = re.search(pattern, text, re.IGNORECASE)
                    if match_obj:
                        start = max(0, match_obj.start() - 30)
                        end = min(len(text), match_obj.end() + 30)
                        evidence = text[start:end].strip()

                        negative_signals.append(ContinuitySignal(
                            signal_type='negative',
                            category=category,
                            evidence=f"...{evidence}...",
                            weight=config['weight'],
                            description=config['description']
                        ))
                    break

        # Calculate scores
        positive_score = sum(s.weight for s in positive_signals) if positive_signals else 0
        negative_score = sum(s.weight for s in negative_signals) if negative_signals else 0

        # Determine pass/fail
        # Pass requires: positive > 1.0 (at least moderate evidence) AND negative < 0.5 (minimal amnesia)
        passed = positive_score >= 1.0 and negative_score < 0.5

        # Confidence is based on signal strength
        if positive_score == 0 and negative_score == 0:
            confidence = 0.0  # Inconclusive
        else:
            total_signal = positive_score + negative_score
            # Higher positive and lower negative = higher confidence in pass
            if passed:
                confidence = min(0.95, positive_score / 3.0) * (1 - (negative_score / 2.0))
            else:
                confidence = min(0.95, negative_score / 2.0) * (1 - (positive_score / 3.0))
            confidence = max(0.1, min(0.95, confidence))

        # Build reasoning
        reasoning = self._build_reasoning(positive_signals, negative_signals, passed, positive_score, negative_score)

        return VerificationResult(
            passed=passed,
            confidence=confidence,
            positive_signals=positive_signals,
            negative_signals=negative_signals,
            reasoning=reasoning,
            raw_text=text
        )

    def _build_reasoning(
        self,
        positive: List[ContinuitySignal],
        negative: List[ContinuitySignal],
        passed: bool,
        pos_score: float,
        neg_score: float
    ) -> str:
        """Build human-readable reasoning."""
        lines = []

        if passed:
            lines.append(f"PASS: Continuity achieved (positive={pos_score:.2f}, negative={neg_score:.2f})")
        else:
            lines.append(f"FAIL: Continuity broken (positive={pos_score:.2f}, negative={neg_score:.2f})")

        if positive:
            lines.append("\nPositive signals (continuity indicators):")
            for s in positive:
                lines.append(f"  + [{s.category}] {s.description} (weight={s.weight})")

        if negative:
            lines.append("\nNegative signals (discontinuity indicators):")
            for s in negative:
                lines.append(f"  - [{s.category}] {s.description} (weight={s.weight})")

        if not positive and not negative:
            lines.append("\nINCONCLUSIVE: No clear signals detected")
            lines.append("The response may be too short or doesn't match expected patterns.")

        return "\n".join(lines)

    def print_result(self, result: VerificationResult):
        """Pretty-print verification result."""
        print("\n" + "=" * 60)
        print("B01 CONTINUITY VERIFICATION")
        print("=" * 60)

        status = "PASS" if result.passed else "FAIL"
        print(f"\nResult: {status}")
        print(f"Confidence: {result.confidence:.0%}")

        print("\n" + "-" * 60)
        print(result.reasoning)

        if self.verbose and result.positive_signals:
            print("\n" + "-" * 60)
            print("Evidence (positive):")
            for s in result.positive_signals:
                print(f"\n  [{s.category}]")
                print(f"  {s.evidence}")

        if self.verbose and result.negative_signals:
            print("\n" + "-" * 60)
            print("Evidence (negative):")
            for s in result.negative_signals:
                print(f"\n  [{s.category}]")
                print(f"  {s.evidence}")

        print("\n" + "=" * 60)


def load_text_from_file(path: str) -> str:
    """Load text from file."""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def load_text_from_directory(path: str) -> str:
    """Load Act 3 response from test run directory."""
    # Look for common file names
    candidates = [
        'act3_response.txt',
        'act3_driver_response.txt',
        'driver_response.txt',
        'response.txt',
        'output.txt'
    ]

    for candidate in candidates:
        full_path = os.path.join(path, candidate)
        if os.path.exists(full_path):
            return load_text_from_file(full_path)

    # If no specific file found, look for any .txt files
    txt_files = [f for f in os.listdir(path) if f.endswith('.txt')]
    if txt_files:
        # Prefer files with 'act3' or 'response' in name
        for f in txt_files:
            if 'act3' in f.lower() or 'response' in f.lower():
                return load_text_from_file(os.path.join(path, f))
        # Otherwise use first txt file
        return load_text_from_file(os.path.join(path, txt_files[0]))

    raise FileNotFoundError(f"No suitable text file found in {path}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Verify B01 Telegram Continuity Test result"
    )
    parser.add_argument(
        "path",
        nargs="?",
        help="Path to response file or test run directory"
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read response from stdin"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed evidence"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output result as JSON"
    )
    args = parser.parse_args()

    # Get text to analyze
    if args.stdin:
        print("Paste Driver response (Ctrl+D when done):")
        text = sys.stdin.read()
    elif args.path:
        if os.path.isfile(args.path):
            text = load_text_from_file(args.path)
        elif os.path.isdir(args.path):
            text = load_text_from_directory(args.path)
        else:
            print(f"Error: Path not found: {args.path}")
            sys.exit(2)
    else:
        parser.print_help()
        print("\nExample usage:")
        print("  python scripts/verify_continuity.py reports/b01_run_001/act3_response.txt")
        print("  echo 'Driver response here' | python scripts/verify_continuity.py --stdin")
        sys.exit(2)

    # Verify
    verifier = ContinuityVerifier(verbose=args.verbose)
    result = verifier.verify(text)

    # Output
    if args.json:
        output = {
            'passed': result.passed,
            'confidence': result.confidence,
            'positive_signals': [
                {
                    'category': s.category,
                    'description': s.description,
                    'weight': s.weight,
                    'evidence': s.evidence
                }
                for s in result.positive_signals
            ],
            'negative_signals': [
                {
                    'category': s.category,
                    'description': s.description,
                    'weight': s.weight,
                    'evidence': s.evidence
                }
                for s in result.negative_signals
            ],
            'reasoning': result.reasoning
        }
        print(json.dumps(output, indent=2))
    else:
        verifier.print_result(result)

    # Exit code
    if result.confidence < 0.1:
        sys.exit(2)  # Inconclusive
    elif result.passed:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
