#!/usr/bin/env python3
"""
Preflight Check - Comprehensive Health Verification for Strange Loop

Purpose: Verify all prerequisites before running B01 Telegram Continuity Test
Owner: Victor "The Resurrector" (Operations)
Version: 1.0
Date: 2024-11-25

Checks:
- FalkorDB connection (port 6380)
- Graph "strange_loop" exists
- Seed data present (11 nodes, 12 relationships expected)
- Node type distribution
- Query latency baseline (<100ms)
- All 8 query functions operational

Exit codes:
- 0: All checks passed
- 1: Critical failure (cannot proceed with test)
- 2: Warning (can proceed but issues detected)

Usage:
    python scripts/preflight_check.py [--host HOST] [--port PORT] [--graph GRAPH]
"""

import sys
import time
import argparse
from typing import Tuple, List, Dict, Any
from dataclasses import dataclass

# Add parent directory to path for imports
sys.path.insert(0, '/home/mind-protocol/strange-loop')

try:
    from falkordb import FalkorDB
except ImportError:
    print("FATAL: FalkorDB not installed. Run: pip install FalkorDB")
    sys.exit(1)


@dataclass
class CheckResult:
    """Result of a single preflight check."""
    name: str
    passed: bool
    message: str
    details: Dict[str, Any] = None
    is_critical: bool = True  # If critical, failure blocks test execution


class PreflightChecker:
    """Comprehensive health verification for Strange Loop."""

    # Expected seed data counts
    EXPECTED_NODES = 11
    EXPECTED_RELATIONSHIPS = 12
    EXPECTED_NODE_TYPES = {
        'Citizen': 1,
        'Person': 1,
        'Partnership': 1,
        'Conversation_Memory': 1,
        'Technical_Context': 1,
        'Emotional_State': 1,
        'Strategy_Pattern': 1,
        'Code_Reference': 2,
        'Failed_Attempt': 1,
        'Constraint': 1
    }

    # Query latency threshold (ms)
    LATENCY_THRESHOLD_MS = 100

    def __init__(self, host: str = "localhost", port: int = 6380, graph_name: str = "strange_loop"):
        """
        Initialize preflight checker.

        Args:
            host: FalkorDB host
            port: FalkorDB port (default: 6380 for Strange Loop)
            graph_name: Graph database name
        """
        self.host = host
        self.port = port
        self.graph_name = graph_name
        self.db = None
        self.graph = None
        self.results: List[CheckResult] = []

    def run_all_checks(self) -> Tuple[bool, bool]:
        """
        Run all preflight checks.

        Returns:
            Tuple of (all_passed, has_critical_failure)
        """
        print("=" * 60)
        print("PREFLIGHT CHECK - Strange Loop Operational Verification")
        print("=" * 60)
        print(f"\nTarget: {self.host}:{self.port}/{self.graph_name}")
        print("-" * 60)

        # Check sequence
        self._check_connection()
        if self.db:
            self._check_graph_exists()
            if self.graph:
                self._check_seed_data()
                self._check_node_types()
                self._check_relationships()
                self._check_query_latency()
                self._check_query_functions()

        return self._summarize_results()

    def _check_connection(self):
        """Check FalkorDB connection."""
        check_name = "FalkorDB Connection"
        print(f"\n[CHECK] {check_name}")

        try:
            start = time.time()
            self.db = FalkorDB(host=self.host, port=self.port)
            latency = (time.time() - start) * 1000

            self.results.append(CheckResult(
                name=check_name,
                passed=True,
                message=f"Connected to FalkorDB in {latency:.1f}ms",
                details={'latency_ms': latency}
            ))
            print(f"  [PASS] Connected in {latency:.1f}ms")

        except Exception as e:
            self.results.append(CheckResult(
                name=check_name,
                passed=False,
                message=f"Connection failed: {e}",
                details={'error': str(e)},
                is_critical=True
            ))
            print(f"  [FAIL] Connection failed: {e}")
            print(f"\n  HINT: Is FalkorDB running?")
            print(f"        docker run -d --name strange-loop-falkordb -p {self.port}:6379 falkordb/falkordb")

    def _check_graph_exists(self):
        """Check that graph exists."""
        check_name = "Graph Exists"
        print(f"\n[CHECK] {check_name}")

        try:
            self.graph = self.db.select_graph(self.graph_name)
            # Try a simple query to verify graph is accessible
            result = self.graph.query("RETURN 1 AS test")

            self.results.append(CheckResult(
                name=check_name,
                passed=True,
                message=f"Graph '{self.graph_name}' accessible"
            ))
            print(f"  [PASS] Graph '{self.graph_name}' accessible")

        except Exception as e:
            self.results.append(CheckResult(
                name=check_name,
                passed=False,
                message=f"Graph not accessible: {e}",
                details={'error': str(e)},
                is_critical=True
            ))
            print(f"  [FAIL] Graph not accessible: {e}")
            print(f"\n  HINT: Run seed data creation:")
            print(f"        python graph/seed_data.py localhost {self.port} {self.graph_name}")

    def _check_seed_data(self):
        """Check seed data is present."""
        check_name = "Seed Data Present"
        print(f"\n[CHECK] {check_name}")

        try:
            # Count nodes
            result = self.graph.query("MATCH (n) RETURN count(n) AS count")
            node_count = result.result_set[0][0] if result.result_set else 0

            passed = node_count >= self.EXPECTED_NODES
            message = f"Found {node_count} nodes (expected {self.EXPECTED_NODES})"

            self.results.append(CheckResult(
                name=check_name,
                passed=passed,
                message=message,
                details={'node_count': node_count, 'expected': self.EXPECTED_NODES},
                is_critical=node_count == 0  # Only critical if NO data
            ))

            status = "[PASS]" if passed else "[WARN]"
            print(f"  {status} {message}")

            if node_count == 0:
                print(f"\n  HINT: Run seed data creation:")
                print(f"        python graph/seed_data.py localhost {self.port} {self.graph_name}")

        except Exception as e:
            self.results.append(CheckResult(
                name=check_name,
                passed=False,
                message=f"Query failed: {e}",
                details={'error': str(e)},
                is_critical=True
            ))
            print(f"  [FAIL] Query failed: {e}")

    def _check_node_types(self):
        """Check node type distribution."""
        check_name = "Node Type Distribution"
        print(f"\n[CHECK] {check_name}")

        try:
            result = self.graph.query(
                "MATCH (n) RETURN labels(n)[0] AS type, count(n) AS count ORDER BY type"
            )

            actual_types = {}
            for record in result.result_set:
                actual_types[record[0]] = record[1]

            # Compare to expected
            missing = []
            wrong_count = []
            for node_type, expected_count in self.EXPECTED_NODE_TYPES.items():
                actual_count = actual_types.get(node_type, 0)
                if actual_count == 0:
                    missing.append(node_type)
                elif actual_count != expected_count:
                    wrong_count.append(f"{node_type}: {actual_count} (expected {expected_count})")

            passed = len(missing) == 0 and len(wrong_count) == 0

            self.results.append(CheckResult(
                name=check_name,
                passed=passed,
                message="All expected node types present" if passed else f"Issues: {len(missing)} missing, {len(wrong_count)} wrong count",
                details={
                    'actual': actual_types,
                    'expected': self.EXPECTED_NODE_TYPES,
                    'missing': missing,
                    'wrong_count': wrong_count
                },
                is_critical=len(missing) > 0
            ))

            if passed:
                print(f"  [PASS] All {len(self.EXPECTED_NODE_TYPES)} node types present")
            else:
                if missing:
                    print(f"  [FAIL] Missing node types: {', '.join(missing)}")
                if wrong_count:
                    print(f"  [WARN] Wrong counts: {', '.join(wrong_count)}")

            # Print distribution
            print(f"  Distribution:")
            for node_type, count in sorted(actual_types.items()):
                expected = self.EXPECTED_NODE_TYPES.get(node_type, '?')
                status = "ok" if count == expected else "!"
                print(f"    {node_type}: {count} ({status})")

        except Exception as e:
            self.results.append(CheckResult(
                name=check_name,
                passed=False,
                message=f"Query failed: {e}",
                details={'error': str(e)},
                is_critical=False
            ))
            print(f"  [FAIL] Query failed: {e}")

    def _check_relationships(self):
        """Check relationship count."""
        check_name = "Relationships"
        print(f"\n[CHECK] {check_name}")

        try:
            result = self.graph.query("MATCH ()-[r]->() RETURN count(r) AS count")
            rel_count = result.result_set[0][0] if result.result_set else 0

            passed = rel_count >= self.EXPECTED_RELATIONSHIPS
            message = f"Found {rel_count} relationships (expected {self.EXPECTED_RELATIONSHIPS})"

            self.results.append(CheckResult(
                name=check_name,
                passed=passed,
                message=message,
                details={'rel_count': rel_count, 'expected': self.EXPECTED_RELATIONSHIPS},
                is_critical=rel_count == 0
            ))

            status = "[PASS]" if passed else "[WARN]"
            print(f"  {status} {message}")

            # Show relationship types
            result = self.graph.query(
                "MATCH ()-[r]->() RETURN type(r) AS type, count(r) AS count ORDER BY type"
            )
            print(f"  Types:")
            for record in result.result_set:
                print(f"    {record[0]}: {record[1]}")

        except Exception as e:
            self.results.append(CheckResult(
                name=check_name,
                passed=False,
                message=f"Query failed: {e}",
                details={'error': str(e)},
                is_critical=False
            ))
            print(f"  [FAIL] Query failed: {e}")

    def _check_query_latency(self):
        """Check baseline query latency."""
        check_name = "Query Latency Baseline"
        print(f"\n[CHECK] {check_name}")

        try:
            # Run multiple queries and average
            latencies = []
            test_queries = [
                "MATCH (n) RETURN count(n)",
                "MATCH (c:Citizen) RETURN c LIMIT 1",
                "MATCH (p:Partnership) RETURN p LIMIT 1"
            ]

            for query in test_queries:
                start = time.time()
                self.graph.query(query)
                latencies.append((time.time() - start) * 1000)

            avg_latency = sum(latencies) / len(latencies)
            max_latency = max(latencies)

            passed = avg_latency < self.LATENCY_THRESHOLD_MS
            message = f"Avg: {avg_latency:.1f}ms, Max: {max_latency:.1f}ms (threshold: {self.LATENCY_THRESHOLD_MS}ms)"

            self.results.append(CheckResult(
                name=check_name,
                passed=passed,
                message=message,
                details={
                    'avg_latency_ms': avg_latency,
                    'max_latency_ms': max_latency,
                    'threshold_ms': self.LATENCY_THRESHOLD_MS
                },
                is_critical=False  # High latency is a warning, not critical
            ))

            status = "[PASS]" if passed else "[WARN]"
            print(f"  {status} {message}")

        except Exception as e:
            self.results.append(CheckResult(
                name=check_name,
                passed=False,
                message=f"Query failed: {e}",
                details={'error': str(e)},
                is_critical=False
            ))
            print(f"  [FAIL] Query failed: {e}")

    def _check_query_functions(self):
        """Check all 8 query functions are operational."""
        check_name = "Query Functions (8 tools)"
        print(f"\n[CHECK] {check_name}")

        try:
            from graph.tools import GraphTools

            tools = GraphTools(host=self.host, port=self.port, graph_name=self.graph_name)

            # Test each function
            function_results = {}

            # 1. query_partnerships
            result = tools.query_partnerships("nicolas")
            function_results['query_partnerships'] = result.found
            print(f"  1. query_partnerships: {'OK' if result.found else 'EMPTY'} ({result.query_time_ms:.1f}ms)")

            # 2. query_conversations
            result = tools.query_conversations("nicolas", ["race condition"])
            function_results['query_conversations'] = result.found
            print(f"  2. query_conversations: {'OK' if result.found else 'EMPTY'} ({result.query_time_ms:.1f}ms)")

            # 3. query_technical_context
            result = tools.query_technical_context("stimulus_integrator")
            function_results['query_technical_context'] = result.found
            print(f"  3. query_technical_context: {'OK' if result.found else 'EMPTY'} ({result.query_time_ms:.1f}ms)")

            # 4. query_emotional_state
            result = tools.query_emotional_state("bug recurrence")
            function_results['query_emotional_state'] = result.found
            print(f"  4. query_emotional_state: {'OK' if result.found else 'EMPTY'} ({result.query_time_ms:.1f}ms)")

            # 5. query_strategy_patterns
            result = tools.query_strategy_patterns("concurrency")
            function_results['query_strategy_patterns'] = result.found
            print(f"  5. query_strategy_patterns: {'OK' if result.found else 'EMPTY'} ({result.query_time_ms:.1f}ms)")

            # 6. query_related_code
            result = tools.query_related_code("stimulus_integrator")
            function_results['query_related_code'] = result.found
            print(f"  6. query_related_code: {'OK' if result.found else 'EMPTY'} ({result.query_time_ms:.1f}ms)")

            # 7. query_failed_attempts
            result = tools.query_failed_attempts("race condition")
            function_results['query_failed_attempts'] = result.found
            print(f"  7. query_failed_attempts: {'OK' if result.found else 'EMPTY'} ({result.query_time_ms:.1f}ms)")

            # 8. query_active_constraints
            result = tools.query_active_constraints()
            function_results['query_active_constraints'] = result.found
            print(f"  8. query_active_constraints: {'OK' if result.found else 'EMPTY'} ({result.query_time_ms:.1f}ms)")

            # Summary
            working = sum(1 for v in function_results.values() if v)
            passed = working == 8
            message = f"{working}/8 query functions returning data"

            self.results.append(CheckResult(
                name=check_name,
                passed=passed,
                message=message,
                details={'function_results': function_results},
                is_critical=working == 0  # Only critical if ALL fail
            ))

            status = "[PASS]" if passed else "[WARN]"
            print(f"\n  {status} {message}")

        except ImportError as e:
            self.results.append(CheckResult(
                name=check_name,
                passed=False,
                message=f"Import failed: {e}",
                details={'error': str(e)},
                is_critical=True
            ))
            print(f"  [FAIL] Cannot import graph.tools: {e}")

        except Exception as e:
            self.results.append(CheckResult(
                name=check_name,
                passed=False,
                message=f"Error: {e}",
                details={'error': str(e)},
                is_critical=True
            ))
            print(f"  [FAIL] Error: {e}")

    def _summarize_results(self) -> Tuple[bool, bool]:
        """
        Summarize all check results.

        Returns:
            Tuple of (all_passed, has_critical_failure)
        """
        print("\n" + "=" * 60)
        print("PREFLIGHT SUMMARY")
        print("=" * 60)

        passed_count = sum(1 for r in self.results if r.passed)
        failed_count = len(self.results) - passed_count
        critical_failures = [r for r in self.results if not r.passed and r.is_critical]

        print(f"\nResults: {passed_count} passed, {failed_count} failed")
        print(f"Critical failures: {len(critical_failures)}")

        if critical_failures:
            print("\nCritical failures:")
            for r in critical_failures:
                print(f"  - {r.name}: {r.message}")

        all_passed = failed_count == 0
        has_critical = len(critical_failures) > 0

        print("\n" + "-" * 60)
        if all_passed:
            print("PREFLIGHT: PASS - Ready for test execution")
        elif not has_critical:
            print("PREFLIGHT: WARN - Can proceed but issues detected")
        else:
            print("PREFLIGHT: FAIL - Cannot proceed with test")
        print("-" * 60)

        return all_passed, has_critical


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Preflight check for Strange Loop test execution"
    )
    parser.add_argument("--host", default="localhost", help="FalkorDB host")
    parser.add_argument("--port", type=int, default=6380, help="FalkorDB port")
    parser.add_argument("--graph", default="strange_loop", help="Graph name")
    args = parser.parse_args()

    checker = PreflightChecker(
        host=args.host,
        port=args.port,
        graph_name=args.graph
    )

    all_passed, has_critical = checker.run_all_checks()

    if has_critical:
        sys.exit(1)
    elif not all_passed:
        sys.exit(2)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
