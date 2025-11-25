"""
Manual Loop Orchestration - B01 Telegram Continuity Test

This is the test harness for Strange Loop V1.
It orchestrates the Dreamer → Driver → Verification flow.

In V1: Manual copy/paste between Dreamer output and Driver input
In V2+: Automated LLM calls

Owner: Felix (Runtime Engineer) + Atlas (Infrastructure)
Phase: 5 (Driver Integration & Test Harness)

Usage:
    python loop/manual_loop.py                    # Run B01 test
    python loop/manual_loop.py --act 1            # Run specific act
    python loop/manual_loop.py --stimulus "..."   # Custom stimulus
"""

import sys
import os
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, List, Dict

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from graph.tools import GraphTools
from dreamer.agent import DreamerAgent, Stimulus
from driver.agent import DriverAgent
from loop.terminal_display import (
    TerminalDisplay, 
    DisplayConfig, 
    PsychState,
    create_display
)


@dataclass
class ActResult:
    """Result of a single act execution."""
    act_num: int
    act_name: str
    stimulus: str
    context_object: str
    driver_response: Optional[str]
    passed: bool
    criteria_results: Dict[str, bool]


class ManualLoop:
    """
    Manual Loop Orchestrator for B01 Test.
    
    Coordinates:
    - Dreamer exploration (graph queries → Context Object)
    - Driver preparation (prompt assembly)
    - Manual handoff (copy/paste instructions)
    - Verification (pass/fail criteria)
    """
    
    def __init__(
        self,
        citizen: str = "felix",
        graph_host: str = "localhost",
        graph_port: int = 6380,
        verbose: bool = False
    ):
        self.citizen = citizen
        self.verbose = verbose
        
        # Initialize components
        self.display = create_display(verbose=verbose, width=70)
        self.graph_tools = GraphTools(host=graph_host, port=graph_port)
        self.dreamer = DreamerAgent(port=graph_port, citizen=citizen)
        # self.driver = DriverAgent()  # V1: Manual handoff, no automated driver
        
        # Track act results
        self.results: List[ActResult] = []
    
    # =========================================================================
    # B01 TEST SCENARIOS
    # =========================================================================
    
    def get_b01_stimulus(self, act: int) -> Stimulus:
        """Get stimulus for B01 test acts."""
        
        if act == 1:
            return Stimulus(
                content="Hey Felix, the race condition is back.",
                sender="nicolas",
                channel="telegram",
                timestamp=datetime.now().isoformat()
            )
        elif act == 3:
            return Stimulus(
                content="Did you figure out that race condition?",
                sender="nicolas", 
                channel="telegram",
                timestamp=datetime.now().isoformat()
            )
        else:
            raise ValueError(f"Unknown act: {act}")
    
    def get_verification_criteria(self, act: int) -> Dict[str, str]:
        """Get pass/fail criteria for each act."""
        
        if act == 1:
            return {
                "partnership_awareness": "Shows awareness of partnership (mentions 'third time', 'we', past history)",
                "emotional_state": "References emotional state (frustration, determination)",
                "strategy_usage": "Uses strategy from memory (systematic debugging steps)",
                "technical_context": "Shows correct technical context (stimulus_integrator, race condition)",
                "constraint_awareness": "Acknowledges constraints (launch deadline)"
            }
        elif act == 3:
            return {
                "continuity": "Shows continuity with Act 1 ('still working on it', 'we discussed')",
                "remembers_topic": "Knows this is the SAME race condition from earlier",
                "strategy_continuity": "References the systematic approach agreed upon",
                "progress_indication": "Shows progress or continued investigation",
                "not_new_topic": "Does NOT treat this as a new topic or ask 'what race condition?'"
            }
        else:
            return {}
    
    # =========================================================================
    # EXECUTION FLOW
    # =========================================================================
    
    def run_dreamer(self, stimulus: Stimulus) -> str:
        """Run Dreamer exploration and return Context Object."""
        
        self.display.header_box(
            "DREAMER AWAKENS",
            "Exploring graph memory..."
        )
        
        # Run exploration
        upwelling = self.dreamer.process_stimulus(stimulus)
        
        # Display statistics
        self.display.lens_summary(
            total_time_ms=int(upwelling.exploration_time_ms),
            queries=upwelling.queries_executed,
            nodes_retrieved=upwelling.nodes_retrieved,
            lenses_with_data=upwelling.lenses_with_data
        )
        
        # Display psychological state
        if upwelling.lenses_with_data >= 6:
            self.display.psych_state(PsychState.CONFIDENCE, "Rich context retrieved")
        elif upwelling.lenses_with_data >= 4:
            self.display.psych_state(PsychState.CRYSTALLIZING, "Moderate context")
        else:
            self.display.psych_state(PsychState.UNCERTAINTY, "Limited context")
        
        return upwelling.context_object
    
    def prepare_driver(self, context_object: str, stimulus: str) -> dict:
        """Prepare Driver for manual execution.

        V1: Manual handoff - no DriverAgent.
        Context Object becomes the system prompt directly.
        """

        self.display.header_box(
            "DRIVER PREPARATION",
            "Assembling system prompt..."
        )

        # V1: Context Object IS the system prompt
        result = {
            'system_prompt': context_object,
            'stimulus': stimulus
        }

        self.display.status_success(f"System prompt assembled ({len(result['system_prompt'])} chars)")

        return result
    
    def display_handoff(self, driver_prep: dict, stimulus: str):
        """Display handoff instructions and context."""
        
        self.display.section_divider()
        print()
        print("=" * 70)
        print("CONTEXT OBJECT (Copy everything between the lines)")
        print("=" * 70)
        print()
        print(driver_prep['system_prompt'])
        print()
        print("=" * 70)
        print("END CONTEXT OBJECT")
        print("=" * 70)
        print()
        
        self.display.handoff_instructions(stimulus)
    
    def get_driver_response(self) -> str:
        """Get Driver response from user (manual copy/paste)."""
        
        print()
        print("-" * 70)
        print("Paste the Driver's response below.")
        print("When done, type '###' on a new line and press Enter.")
        print("-" * 70)
        
        return self.display.get_multiline_input()
    
    def verify_response(self, act: int, response: str) -> Dict[str, bool]:
        """Verify Driver response against criteria."""
        
        criteria = self.get_verification_criteria(act)
        results = {}
        
        self.display.verification_header(f"ACT {act}")
        
        response_lower = response.lower()
        
        for key, description in criteria.items():
            # Simple keyword-based verification for V1
            # V2+ could use LLM-based verification
            
            if act == 1:
                if key == "partnership_awareness":
                    passed = any(w in response_lower for w in ["third", "again", "we", "our", "nicolas"])
                elif key == "emotional_state":
                    passed = any(w in response_lower for w in ["frustrat", "sigh", "damn", "annoying", "determin"])
                elif key == "strategy_usage":
                    passed = any(w in response_lower for w in ["systematic", "reproduce", "instrument", "step"])
                elif key == "technical_context":
                    passed = any(w in response_lower for w in ["stimulus_integrator", "race", "timing", "thread"])
                elif key == "constraint_awareness":
                    passed = any(w in response_lower for w in ["deadline", "launch", "days", "25"])
                else:
                    passed = False
                    
            elif act == 3:
                if key == "continuity":
                    passed = any(w in response_lower for w in ["still", "working", "continu", "progress", "earlier"])
                elif key == "remembers_topic":
                    passed = "what race condition" not in response_lower and "which race" not in response_lower
                elif key == "strategy_continuity":
                    passed = any(w in response_lower for w in ["systematic", "instrument", "reproduce", "approach"])
                elif key == "progress_indication":
                    passed = any(w in response_lower for w in ["found", "discovered", "identified", "working on", "progress"])
                elif key == "not_new_topic":
                    passed = "what race condition" not in response_lower
                else:
                    passed = False
            else:
                passed = False
            
            results[key] = passed
            self.display.verification_criterion(description, passed)
        
        # Overall result
        passed_count = sum(1 for v in results.values() if v)
        total = len(results)
        self.display.verification_result(passed_count, total)
        
        return results
    
    # =========================================================================
    # ACT EXECUTION
    # =========================================================================
    
    def run_act(self, act: int) -> ActResult:
        """Run a single act of the B01 test."""
        
        act_names = {1: "INITIAL CONVERSATION", 3: "CONTINUITY TEST"}
        act_name = act_names.get(act, f"ACT {act}")
        
        self.display.act_header(act, act_name)
        
        # Get stimulus
        stimulus = self.get_b01_stimulus(act)
        self.display.stimulus_display(
            stimulus=stimulus.content,
            sender=stimulus.sender,
            channel=stimulus.channel,
            timestamp=stimulus.timestamp
        )
        
        # Wait for user to proceed
        self.display.wait_for_input("Press [Enter] to begin Dreamer exploration...")
        
        # Run Dreamer
        context_object = self.run_dreamer(stimulus)
        
        # Prepare Driver
        driver_prep = self.prepare_driver(context_object, stimulus.content)
        
        # Display handoff instructions
        self.display_handoff(driver_prep, stimulus.content)
        
        # Get Driver response
        driver_response = self.get_driver_response()
        
        # Verify
        criteria_results = self.verify_response(act, driver_response)
        passed = all(criteria_results.values())
        
        # Create result
        result = ActResult(
            act_num=act,
            act_name=act_name,
            stimulus=stimulus.content,
            context_object=context_object,
            driver_response=driver_response,
            passed=passed,
            criteria_results=criteria_results
        )
        
        self.results.append(result)
        
        # Display completion
        status = "PASSED ✓" if passed else "FAILED ✗"
        self.display.act_complete(act_name, f"Result: {status}")
        
        return result
    
    # =========================================================================
    # FULL B01 TEST
    # =========================================================================
    
    def run_b01_test(self):
        """Run the complete B01 Telegram Continuity Test."""
        
        self.display.header_box(
            "STRANGE LOOP - B01 TEST",
            "Telegram Continuity Test"
        )
        
        print("This test validates that the Bicameral Mind architecture")
        print("can maintain conversational continuity across context resets.")
        print()
        print("Test structure:")
        print("  Act 1: Initial conversation (race condition)")
        print("  Act 2: Context reset simulation (manual)")
        print("  Act 3: Continuity test (does Driver remember?)")
        print()
        
        self.display.wait_for_input("Press [Enter] to begin B01 test...")
        
        # Act 1
        act1_result = self.run_act(1)
        
        if not act1_result.passed:
            print()
            print("⚠ Act 1 did not pass all criteria.")
            print("  You may continue to test continuity, or quit to debug.")
            response = input("  Continue? [y/n]: ")
            if response.lower() != 'y':
                return
        
        # Act 2: Context Reset Simulation
        self.display.act_header(2, "CONTEXT RESET SIMULATION")
        print()
        print("Simulating context reset...")
        print()
        print("In a real scenario, the Driver would have processed other tasks,")
        print("pushing the Act 1 conversation out of its context window.")
        print()
        print("For this test, we simulate by using a FRESH Driver instance")
        print("that has NO memory of Act 1 in its context.")
        print()
        print("The only way Driver can know about Act 1 is through")
        print("the Dreamer's graph queries.")
        print()
        self.display.wait_for_input("Press [Enter] when ready for Act 3 (use a FRESH Driver instance)...")
        
        # Act 3
        act3_result = self.run_act(3)
        
        # Final Results
        self.display.section_divider()
        self.display.header_box(
            "B01 TEST COMPLETE",
            "Final Results"
        )
        
        print("Act Results:")
        for result in self.results:
            status = "✓ PASS" if result.passed else "✗ FAIL"
            passed = sum(1 for v in result.criteria_results.values() if v)
            total = len(result.criteria_results)
            print(f"  Act {result.act_num}: {status} ({passed}/{total} criteria)")
        
        print()
        
        # THE critical test
        if act3_result.passed:
            print("=" * 70)
            print("  ✓ B01 TELEGRAM CONTINUITY TEST: PASSED")
            print("=" * 70)
            print()
            print("  The Driver maintained continuity across context reset.")
            print("  Memory retrieval from graph is WORKING.")
            print("  The Bicameral Mind architecture is VALIDATED.")
            print()
        else:
            print("=" * 70)
            print("  ✗ B01 TELEGRAM CONTINUITY TEST: FAILED")
            print("=" * 70)
            print()
            print("  The Driver did NOT maintain continuity.")
            print("  Check:")
            print("  - Did the Dreamer retrieve correct context?")
            print("  - Was the Context Object complete?")
            print("  - Did the Driver use the context properly?")
            print()


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Strange Loop Manual Test Loop")
    parser.add_argument("--act", type=int, help="Run specific act (1 or 3)")
    parser.add_argument("--stimulus", type=str, help="Custom stimulus text")
    parser.add_argument("--citizen", type=str, default="felix", help="Citizen name")
    parser.add_argument("--host", type=str, default="localhost", help="FalkorDB host")
    parser.add_argument("--port", type=int, default=6380, help="FalkorDB port")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    try:
        loop = ManualLoop(
            citizen=args.citizen,
            graph_host=args.host,
            graph_port=args.port,
            verbose=args.verbose
        )
        
        if args.act:
            loop.run_act(args.act)
        else:
            loop.run_b01_test()
            
    except KeyboardInterrupt:
        print("\n\nTest aborted by user.")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
