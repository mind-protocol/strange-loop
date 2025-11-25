"""
Graph Tools - V1 Query Functions

Purpose: Tool-constrained queries for anti-hallucination
Owner: Felix (Physics/Runtime Engineer)
Version: 1.0
Date: 2024-11-20

These 8 functions are the ONLY way the Dreamer accesses memory.
No free generation allowed - only verified data from FalkorDB.

See: docs/mechanisms/M01_graph_tools.md for specification
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
import time

# FalkorDB client (pip install FalkorDB)
try:
    from falkordb import FalkorDB
except ImportError:
    print("WARNING: FalkorDB not installed. Run: pip install FalkorDB")
    FalkorDB = None


@dataclass
class QueryResult:
    """
    Structured result from graph query.

    Anti-hallucination guarantee: If found=False, data=None.
    LLM cannot invent what doesn't exist.
    """
    found: bool
    data: Optional[Any]  # Dict for single result, List[Dict] for multiple
    confidence: float  # 0.0-1.0 (1.0 for exact match, <1.0 for partial)
    query_time_ms: float
    error: Optional[str] = None


class GraphTools:
    """
    8 query functions for Dreamer memory access.

    Critical principle: These tools return actual nodes or None.
    Never fabricated data. Never hallucinated results.
    """

    def __init__(self, host: str = "localhost", port: int = 6379, graph_name: str = "strange_loop"):
        """
        Initialize FalkorDB connection.

        Args:
            host: FalkorDB host (default: localhost)
            port: FalkorDB port (default: 6379)
            graph_name: Graph database name (default: strange_loop)
        """
        if FalkorDB is None:
            raise ImportError("FalkorDB not installed. Run: pip install FalkorDB")

        self.db = FalkorDB(host=host, port=port)
        self.graph = self.db.select_graph(graph_name)
        self.graph_name = graph_name

    def _execute_query(self, cypher: str, params: Dict[str, Any] = None) -> QueryResult:
        """
        Execute Cypher query and return structured result.

        Args:
            cypher: Cypher query string
            params: Query parameters

        Returns:
            QueryResult with found/data/confidence/time
        """
        start_time = time.time()
        params = params or {}

        try:
            result = self.graph.query(cypher, params)
            query_time_ms = (time.time() - start_time) * 1000

            if not result.result_set:
                # No results found
                return QueryResult(
                    found=False,
                    data=None,
                    confidence=0.0,
                    query_time_ms=query_time_ms
                )

            # Parse results
            data = []
            for record in result.result_set:
                # Convert record to dict
                if len(record) == 1:
                    # Single node/value
                    node = record[0]
                    if hasattr(node, 'properties'):
                        data.append(node.properties)
                    else:
                        data.append(node)
                else:
                    # Multiple values - create dict from column names
                    row_dict = {}
                    for i, value in enumerate(record):
                        col_name = result.header[i][1] if result.header else f"col_{i}"
                        if hasattr(value, 'properties'):
                            row_dict[col_name] = value.properties
                        else:
                            row_dict[col_name] = value
                    data.append(row_dict)

            # Return single dict if only one result, else list
            if len(data) == 1:
                return QueryResult(
                    found=True,
                    data=data[0],
                    confidence=1.0,  # Exact match
                    query_time_ms=query_time_ms
                )
            else:
                return QueryResult(
                    found=True,
                    data=data,
                    confidence=0.95,  # Multiple matches (slightly lower confidence)
                    query_time_ms=query_time_ms
                )

        except Exception as e:
            query_time_ms = (time.time() - start_time) * 1000
            return QueryResult(
                found=False,
                data=None,
                confidence=0.0,
                query_time_ms=query_time_ms,
                error=str(e)
            )

    # ========================================================================
    # THE 8 QUERY FUNCTIONS
    # ========================================================================

    def query_partnerships(self, partner_id: str, citizen: str = "felix") -> QueryResult:
        """
        Find partnership information for a specific partner.

        Args:
            partner_id: Partner name (e.g., "nicolas", "ada")
            citizen: AI citizen name (default: "felix")

        Returns:
            QueryResult containing Partnership node or None if not found

        Example:
            result = tools.query_partnerships("nicolas")
            # Returns partnership context: trust_level, communication_style, shared_history
        """
        cypher = """
        MATCH (p:Partnership {citizen: $citizen})
        WHERE toLower(p.partner_name) = toLower($partner_id)
        RETURN p
        """

        return self._execute_query(cypher, {
            "citizen": citizen,
            "partner_id": partner_id
        })

    def query_conversations(
        self,
        partner_id: str,
        keywords: Optional[List[str]] = None,
        citizen: str = "felix",
        limit: int = 5
    ) -> QueryResult:
        """
        Find conversations with a partner, optionally filtered by topic.

        Args:
            partner_id: Partner name
            keywords: Optional topic keywords to filter by
            citizen: AI citizen name
            limit: Max conversations to return (default: 5)

        Returns:
            QueryResult containing list of Conversation_Memory nodes

        Example:
            result = tools.query_conversations("nicolas", ["race condition", "bug"])
            # Returns conversation history about race conditions
        """
        if keywords:
            # Filter by keywords
            cypher = """
            MATCH (conv:Conversation_Memory {citizen: $citizen, partner: $partner_id})
            WHERE ANY(kw IN $keywords WHERE toLower(conv.topic) CONTAINS toLower(kw))
            RETURN conv
            ORDER BY conv.timestamp DESC
            LIMIT $limit
            """
        else:
            # No keywords - return all conversations with partner
            cypher = """
            MATCH (conv:Conversation_Memory {citizen: $citizen, partner: $partner_id})
            RETURN conv
            ORDER BY conv.timestamp DESC
            LIMIT $limit
            """

        return self._execute_query(cypher, {
            "citizen": citizen,
            "partner_id": partner_id,
            "keywords": keywords or [],
            "limit": limit
        })

    def query_technical_context(
        self,
        term: str,
        issue_type: Optional[str] = None,
        citizen: str = "felix",
        limit: int = 5
    ) -> QueryResult:
        """
        Find technical information about code, systems, or bugs.

        Args:
            term: Search term (component name, bug description, etc.)
            issue_type: Optional filter (e.g., "race condition", "feature", "refactor")
            citizen: AI citizen name
            limit: Max results to return (default: 5)

        Returns:
            QueryResult containing list of Technical_Context nodes

        Example:
            result = tools.query_technical_context("stimulus_integrator", "race condition")
            # Returns technical context about race condition in stimulus_integrator
        """
        if issue_type:
            # Filter by issue type
            cypher = """
            MATCH (t:Technical_Context {citizen: $citizen})
            WHERE (toLower(t.component) CONTAINS toLower($term)
                   OR toLower(t.description) CONTAINS toLower($term))
              AND toLower(t.issue_type) = toLower($issue_type)
            RETURN t
            ORDER BY t.updated_at DESC
            LIMIT $limit
            """
        else:
            # No issue type filter
            cypher = """
            MATCH (t:Technical_Context {citizen: $citizen})
            WHERE toLower(t.component) CONTAINS toLower($term)
               OR toLower(t.description) CONTAINS toLower($term)
            RETURN t
            ORDER BY t.updated_at DESC
            LIMIT $limit
            """

        return self._execute_query(cypher, {
            "citizen": citizen,
            "term": term,
            "issue_type": issue_type or "",
            "limit": limit
        })

    def query_emotional_state(
        self,
        context_similar_to: str,
        emotion: Optional[str] = None,
        citizen: str = "felix",
        limit: int = 3
    ) -> QueryResult:
        """
        Find emotional patterns for situations.

        Args:
            context_similar_to: Situation description to match against
            emotion: Optional emotion filter (e.g., "frustration", "excitement")
            citizen: AI citizen name
            limit: Max results to return (default: 3)

        Returns:
            QueryResult containing list of Emotional_State nodes

        Example:
            result = tools.query_emotional_state("bug recurrence", "frustration")
            # Returns emotional patterns for recurring bugs
        """
        if emotion:
            # Filter by specific emotion
            cypher = """
            MATCH (e:Emotional_State {citizen: $citizen})
            WHERE toLower(e.context) CONTAINS toLower($context_similar_to)
              AND toLower(e.emotion) = toLower($emotion)
            RETURN e
            ORDER BY e.intensity DESC
            LIMIT $limit
            """
        else:
            # No emotion filter
            cypher = """
            MATCH (e:Emotional_State {citizen: $citizen})
            WHERE toLower(e.context) CONTAINS toLower($context_similar_to)
            RETURN e
            ORDER BY e.intensity DESC
            LIMIT $limit
            """

        return self._execute_query(cypher, {
            "citizen": citizen,
            "context_similar_to": context_similar_to,
            "emotion": emotion or "",
            "limit": limit
        })

    def query_strategy_patterns(
        self,
        situation_type: str,
        min_success_rate: float = 0.5,
        citizen: str = "felix",
        limit: int = 3
    ) -> QueryResult:
        """
        Find proven approaches for situations.

        Args:
            situation_type: Type of situation (e.g., "concurrency issues", "debugging")
            min_success_rate: Minimum success rate (0.0-1.0, default: 0.5)
            citizen: AI citizen name
            limit: Max results to return (default: 3)

        Returns:
            QueryResult containing list of Strategy_Pattern nodes

        Example:
            result = tools.query_strategy_patterns("race conditions", min_success_rate=0.7)
            # Returns strategies with >70% success for race conditions
        """
        cypher = """
        MATCH (s:Strategy_Pattern {citizen: $citizen})
        WHERE toLower(s.applicability) CONTAINS toLower($situation_type)
          AND s.success_rate >= $min_success_rate
        RETURN s
        ORDER BY s.success_rate DESC
        LIMIT $limit
        """

        return self._execute_query(cypher, {
            "citizen": citizen,
            "situation_type": situation_type,
            "min_success_rate": min_success_rate,
            "limit": limit
        })

    def query_related_code(
        self,
        filename: str,
        citizen: str = "felix",
        include_dependencies: bool = True,
        limit: int = 5
    ) -> QueryResult:
        """
        Find code file information and dependencies.

        Args:
            filename: File name or path (partial match supported)
            citizen: AI citizen name
            include_dependencies: Also return dependent files (default: True)
            limit: Max results to return (default: 5)

        Returns:
            QueryResult containing list of Code_Reference nodes

        Example:
            result = tools.query_related_code("stimulus_integrator.py")
            # Returns code reference + files it depends on
        """
        if include_dependencies:
            # Return file + dependencies
            cypher = """
            MATCH (cr:Code_Reference {citizen: $citizen})
            WHERE toLower(cr.file_path) CONTAINS toLower($filename)
            OPTIONAL MATCH (cr)-[:DEPENDS_ON]->(dep:Code_Reference)
            RETURN cr, collect(dep) AS dependencies
            LIMIT $limit
            """
        else:
            # Just the file
            cypher = """
            MATCH (cr:Code_Reference {citizen: $citizen})
            WHERE toLower(cr.file_path) CONTAINS toLower($filename)
            RETURN cr
            LIMIT $limit
            """

        return self._execute_query(cypher, {
            "citizen": citizen,
            "filename": filename,
            "limit": limit
        })

    def query_failed_attempts(
        self,
        context: str,
        citizen: str = "felix",
        limit: int = 5
    ) -> QueryResult:
        """
        Find past failures to avoid repeating.

        Args:
            context: What was being attempted (e.g., "race condition fix")
            citizen: AI citizen name
            limit: Max results to return (default: 5)

        Returns:
            QueryResult containing list of Failed_Attempt nodes

        Example:
            result = tools.query_failed_attempts("race condition")
            # Returns past failed attempts to fix race conditions
        """
        cypher = """
        MATCH (f:Failed_Attempt {citizen: $citizen})
        WHERE toLower(f.context) CONTAINS toLower($context)
           OR toLower(f.approach) CONTAINS toLower($context)
        RETURN f
        ORDER BY f.timestamp DESC
        LIMIT $limit
        """

        return self._execute_query(cypher, {
            "citizen": citizen,
            "context": context,
            "limit": limit
        })

    def query_active_constraints(
        self,
        constraint_type: Optional[str] = None,
        min_severity: str = "medium",
        citizen: str = "felix",
        limit: int = 10
    ) -> QueryResult:
        """
        Find active pressures and deadlines.

        Args:
            constraint_type: Optional type filter (e.g., "deadline", "budget", "resource")
            min_severity: Minimum severity ("low", "medium", "high", "critical")
            citizen: AI citizen name
            limit: Max results to return (default: 10)

        Returns:
            QueryResult containing list of Constraint nodes

        Example:
            result = tools.query_active_constraints("deadline", "critical")
            # Returns critical deadlines
        """
        # Severity ranking
        severity_rank = {
            "low": 0,
            "medium": 1,
            "high": 2,
            "critical": 3
        }

        min_rank = severity_rank.get(min_severity.lower(), 1)

        if constraint_type:
            # Filter by type
            cypher = """
            MATCH (c:Constraint {citizen: $citizen, status: "active"})
            WHERE toLower(c.constraint_type) = toLower($constraint_type)
            RETURN c
            ORDER BY
                CASE c.severity
                    WHEN 'critical' THEN 3
                    WHEN 'high' THEN 2
                    WHEN 'medium' THEN 1
                    ELSE 0
                END DESC,
                c.deadline ASC
            LIMIT $limit
            """
        else:
            # No type filter
            cypher = """
            MATCH (c:Constraint {citizen: $citizen, status: "active"})
            RETURN c
            ORDER BY
                CASE c.severity
                    WHEN 'critical' THEN 3
                    WHEN 'high' THEN 2
                    WHEN 'medium' THEN 1
                    ELSE 0
                END DESC,
                c.deadline ASC
            LIMIT $limit
            """

        # Filter results by severity in Python (since Cypher doesn't support dynamic WHERE on CASE)
        result = self._execute_query(cypher, {
            "citizen": citizen,
            "constraint_type": constraint_type or "",
            "limit": limit
        })

        if result.found and result.data:
            # Filter by severity
            data_list = result.data if isinstance(result.data, list) else [result.data]
            filtered = [
                item for item in data_list
                if severity_rank.get(item.get('severity', 'low').lower(), 0) >= min_rank
            ]

            if filtered:
                result.data = filtered if len(filtered) > 1 else filtered[0]
            else:
                result.found = False
                result.data = None
                result.confidence = 0.0

        return result


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

if __name__ == "__main__":
    # Example: Test connection and query
    try:
        tools = GraphTools(host="localhost", port=6379)
        print("✓ Connected to FalkorDB")

        # Test query_partnerships
        result = tools.query_partnerships("nicolas")
        print(f"\nPartnership query: found={result.found}, time={result.query_time_ms:.2f}ms")
        if result.found:
            print(f"Data: {result.data}")
        else:
            print("No partnership found (expected if seed data not loaded)")

    except Exception as e:
        print(f"✗ Error: {e}")
        print("Make sure FalkorDB is running: docker run -p 6379:6379 falkordb/falkordb")
