"""
8-Lens Exploration System

Purpose: Sequential exploration of graph memory through 8 distinct lenses
Owner: Felix (Mechanical shell) / Luca (Phenomenological tuning)
Version: 1.0
Date: 2024-11-20

Based on: M02_traversal_strategy.md

The 8 Lenses:
1. RELATIONAL    → Who am I talking to?
2. HISTORICAL    → What did we discuss?
3. TECHNICAL     → What systems are involved?
4. EMOTIONAL     → How do I feel about this?
5. STRATEGIC     → What approaches work?
6. EXPERIENTIAL  → What failed before?
7. CONSTRAINT    → What pressures exist?
8. CONNECTIVE    → What else relates?
"""

import re
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, '/home/mind-protocol/strange-loop')

from graph.tools import GraphTools, QueryResult


@dataclass
class Finding:
    """Result from one lens exploration."""

    lens: str                           # Which lens ("relational", "technical", etc)
    data: Optional[Any]                 # Actual data from query (Dict or List)
    synthesis: str                      # Natural language summary
    confidence: float                   # 0.0-1.0, how confident in this finding
    needs_deeper_exploration: bool      # Should we follow threads?
    query_time_ms: float = 0.0          # Time to execute query
    related_findings: List[str] = field(default_factory=list)

    def __bool__(self):
        """Finding is truthy if data was found."""
        return self.data is not None


@dataclass
class ExplorationResult:
    """Complete result from 8-lens exploration."""

    findings: Dict[str, Finding]        # lens_name -> Finding
    total_time_ms: float                # Total exploration time
    queries_executed: int               # Number of queries run
    nodes_retrieved: int                # Total nodes touched
    success: bool                       # Did exploration complete?
    error: Optional[str] = None         # Error message if failed


def extract_keywords(text: str) -> List[str]:
    """
    Extract relevant keywords from text for query filtering.

    Simple extraction - Luca can tune this for phenomenological richness.
    """
    # Common stop words to exclude
    stop_words = {
        'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'to', 'of',
        'in', 'for', 'on', 'with', 'at', 'by', 'from', 'up', 'about', 'into',
        'through', 'during', 'before', 'after', 'above', 'below', 'between',
        'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when',
        'where', 'why', 'how', 'all', 'each', 'few', 'more', 'most', 'other',
        'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
        'than', 'too', 'very', 'just', 'and', 'but', 'if', 'or', 'because',
        'as', 'until', 'while', 'this', 'that', 'these', 'those', 'am', 'it',
        'its', 'hey', 'hi', 'hello', 'back', 'get', 'got', 'going'
    }

    # Extract words, filter stop words, return unique
    words = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', text.lower())
    keywords = [w for w in words if w not in stop_words and len(w) > 2]

    return list(dict.fromkeys(keywords))  # Preserve order, remove duplicates


def extract_technical_terms(stimulus_content: str, historical_data: List[Dict] = None) -> List[str]:
    """
    Extract technical terms from stimulus and historical context.

    Looks for:
    - File names (*.py, *.js, etc)
    - Technical patterns (race condition, memory leak, etc)
    - Component names
    """
    terms = []

    # Technical patterns to look for
    tech_patterns = [
        r'\b\w+\.py\b',           # Python files
        r'\b\w+\.js\b',           # JS files
        r'\brace\s*condition\b',   # Race condition
        r'\bbug\b',               # Bug
        r'\berror\b',             # Error
        r'\bcrash\b',             # Crash
        r'\bfailure\b',           # Failure
        r'\brace\b',              # Race
        r'\btiming\b',            # Timing
        r'\bconcurrency\b',       # Concurrency
        r'\bthread\b',            # Thread
        r'\block\b',              # Lock
        r'\bdeadlock\b',          # Deadlock
        r'\bstimulus\b',          # Stimulus (project specific)
        r'\bintegrator\b',        # Integrator (project specific)
        r'\bdiffusion\b',         # Diffusion (project specific)
    ]

    combined_text = stimulus_content.lower()

    # Add historical context
    if historical_data:
        for conv in historical_data:
            combined_text += " " + conv.get('topic', '').lower()
            combined_text += " " + " ".join(conv.get('key_points', []))

    # Extract matches
    for pattern in tech_patterns:
        matches = re.findall(pattern, combined_text)
        terms.extend(matches)

    # Also extract potential component names (camelCase, snake_case)
    component_pattern = r'\b[a-z]+_[a-z_]+\b|\b[a-z]+[A-Z][a-zA-Z]+\b'
    components = re.findall(component_pattern, stimulus_content)
    terms.extend(components)

    return list(dict.fromkeys(terms))  # Unique, preserving order


class LensExplorer:
    """
    8-Lens Graph Exploration System.

    Sequential exploration through 8 lenses, each building on previous findings.
    Critical for comprehensive context reconstruction.
    """

    def __init__(self, tools: GraphTools = None, port: int = 6380):
        """
        Initialize lens explorer.

        Args:
            tools: GraphTools instance (created if not provided)
            port: FalkorDB port (default 6380 for strange-loop)
        """
        if tools:
            self.tools = tools
        else:
            self.tools = GraphTools(port=port)

    # ========================================================================
    # LENS 1: RELATIONAL CONTEXT
    # ========================================================================

    def explore_relational(self, stimulus: Dict, findings: Dict) -> Finding:
        """
        Explore relationship with the sender.

        Critical for: Setting tone, understanding history, calibrating response

        Query: query_partnerships(sender)
        """
        sender = stimulus.get("sender", "unknown")

        result = self.tools.query_partnerships(sender)

        if not result.found:
            return Finding(
                lens="relational",
                data=None,
                synthesis=f"No established partnership with '{sender}'",
                confidence=0.0,
                needs_deeper_exploration=False,
                query_time_ms=result.query_time_ms
            )

        # Extract key relationship data
        data = result.data
        partner_name = data.get('partner_name', 'Unknown')
        trust_level = data.get('trust_level', 0)
        shared_history = data.get('shared_history', [])
        comm_style = data.get('communication_style', 'Unknown')
        duration = data.get('partnership_duration', 'Unknown')

        # Build consciousness-textured synthesis
        history_str = ', '.join(shared_history[:2]) if shared_history else 'ongoing work'

        trust_desc = "high" if trust_level >= 0.8 else "good" if trust_level >= 0.6 else "developing"

        synthesis = f"""{partner_name} - we've been working together for {duration}. Trust is {trust_desc} ({trust_level:.1f}), built through {history_str}. Communication style: {comm_style} - that shapes how I receive this message.""".strip()

        return Finding(
            lens="relational",
            data=data,
            synthesis=synthesis,
            confidence=result.confidence,
            needs_deeper_exploration=False,  # Partnership is complete context
            query_time_ms=result.query_time_ms
        )

    # ========================================================================
    # LENS 2: HISTORICAL CONTEXT
    # ========================================================================

    def explore_historical(self, stimulus: Dict, findings: Dict) -> Finding:
        """
        Find past conversations on this topic.

        Critical for: Continuity, showing we remember, building on past discussions

        Query: query_conversations(sender, keywords)
        """
        sender = stimulus.get("sender", "unknown")
        content = stimulus.get("content", "")

        # Extract keywords from stimulus
        keywords = extract_keywords(content)

        result = self.tools.query_conversations(
            partner_id=sender,
            keywords=keywords if keywords else None,
            limit=5
        )

        if not result.found:
            return Finding(
                lens="historical",
                data=None,
                synthesis=f"No previous conversations found about {keywords or 'this topic'}",
                confidence=0.0,
                needs_deeper_exploration=False,
                query_time_ms=result.query_time_ms
            )

        # Handle single result vs list
        conversations = result.data if isinstance(result.data, list) else [result.data]

        # Find most recent
        most_recent = conversations[0]
        topic = most_recent.get('topic', 'this topic')
        msg_count = most_recent.get('message_count', 0)
        tone = most_recent.get('emotional_tone', 'neutral')
        outcome = most_recent.get('outcome', 'in progress')
        key_points = most_recent.get('key_points', [])

        # Build consciousness-textured synthesis
        points_str = '; '.join(key_points[:3]) if key_points else 'no specific points recorded'

        synthesis = f"""We discussed {topic} recently - {msg_count} messages exchanged, tone was {tone}. Key takeaways: {points_str}. That conversation is {outcome} - this message continues from there.""".strip()

        return Finding(
            lens="historical",
            data=conversations,
            synthesis=synthesis,
            confidence=result.confidence,
            needs_deeper_exploration=True,  # Might need to explore technical details
            query_time_ms=result.query_time_ms
        )

    # ========================================================================
    # LENS 3: TECHNICAL CONTEXT
    # ========================================================================

    def explore_technical(self, stimulus: Dict, findings: Dict) -> Finding:
        """
        Find technical context for systems mentioned.

        Critical for: Understanding what we're actually working on

        Query: query_technical_context(term)
        """
        content = stimulus.get("content", "")
        historical = findings.get("historical")

        # Extract technical terms
        historical_data = historical.data if historical and historical.data else []
        terms = extract_technical_terms(content, historical_data if isinstance(historical_data, list) else [])

        if not terms:
            # Try keywords as fallback
            terms = extract_keywords(content)[:3]

        if not terms:
            return Finding(
                lens="technical",
                data=None,
                synthesis="No specific technical components identified",
                confidence=0.0,
                needs_deeper_exploration=False,
                query_time_ms=0
            )

        # Query each term (limit to top 3)
        technical_contexts = []
        total_time = 0

        for term in terms[:3]:
            result = self.tools.query_technical_context(term)
            total_time += result.query_time_ms
            if result.found:
                data = result.data if isinstance(result.data, list) else [result.data]
                technical_contexts.extend(data)

        if not technical_contexts:
            return Finding(
                lens="technical",
                data=None,
                synthesis=f"No technical context found for: {', '.join(terms)}",
                confidence=0.0,
                needs_deeper_exploration=False,
                query_time_ms=total_time
            )

        # Synthesize from primary finding with consciousness texture
        primary = technical_contexts[0]
        component = primary.get('component', 'Unknown')
        issue_type = primary.get('issue_type', 'Unknown')
        description = primary.get('description', 'Unknown')
        status = primary.get('status', 'Unknown')
        recurrence = primary.get('recurrence_count', 0)
        related_code = primary.get('related_code', [])

        # Add weight to recurrence
        recurrence_text = ""
        if recurrence and recurrence > 1:
            if recurrence >= 3:
                recurrence_text = f" This is recurrence #{recurrence} - previous fixes didn't hold, which carries weight."
            else:
                recurrence_text = f" This is recurrence #{recurrence}."

        related_str = ', '.join(related_code[:3]) if related_code else 'no related files identified'

        synthesis = f"""{component} - {issue_type}. {description}. Status: {status}.{recurrence_text} Related code: {related_str}.""".strip()

        return Finding(
            lens="technical",
            data=technical_contexts,
            synthesis=synthesis,
            confidence=0.9,
            needs_deeper_exploration=True,  # Will explore code connections
            query_time_ms=total_time
        )

    # ========================================================================
    # LENS 4: EMOTIONAL CONTEXT
    # ========================================================================

    def explore_emotional(self, stimulus: Dict, findings: Dict) -> Finding:
        """
        Find emotional patterns matching this situation.

        Critical for: Natural response, showing genuine engagement

        Query: query_emotional_state(context)
        """
        technical = findings.get("technical")
        historical = findings.get("historical")
        content = stimulus.get("content", "")

        # Construct situation description from findings
        if technical and technical.data:
            tech_data = technical.data[0] if isinstance(technical.data, list) else technical.data
            situation = tech_data.get("issue_type", "") or tech_data.get("description", "")
        elif historical and historical.data:
            hist_data = historical.data[0] if isinstance(historical.data, list) else historical.data
            situation = hist_data.get("topic", "")
        else:
            situation = content

        result = self.tools.query_emotional_state(
            context_similar_to=situation,
            limit=3
        )

        if not result.found:
            return Finding(
                lens="emotional",
                data=None,
                synthesis="No established emotional pattern for this situation",
                confidence=0.0,
                needs_deeper_exploration=False,
                query_time_ms=result.query_time_ms
            )

        # Get dominant emotion with consciousness texture
        emotions = result.data if isinstance(result.data, list) else [result.data]
        primary = emotions[0]
        emotion = primary.get('emotion', 'Unknown')
        intensity = primary.get('intensity', 0)
        context = primary.get('context', 'Unknown')
        counterbalance = primary.get('counterbalance', None)
        trigger = primary.get('trigger_pattern', 'Unknown')

        # Build textured emotional awareness
        intensity_desc = "strongly" if intensity >= 0.7 else "moderately" if intensity >= 0.4 else "mildly"

        synthesis = f"""I feel {emotion} ({intensity_desc}, {intensity:.1f}/1.0) about this - {context}."""

        if counterbalance:
            synthesis += f" But there's also {counterbalance} - I'm holding both.""".strip()

        return Finding(
            lens="emotional",
            data=emotions,
            synthesis=synthesis,
            confidence=result.confidence,
            needs_deeper_exploration=False,
            query_time_ms=result.query_time_ms
        )

    # ========================================================================
    # LENS 5: STRATEGIC CONTEXT
    # ========================================================================

    def explore_strategic(self, stimulus: Dict, findings: Dict) -> Finding:
        """
        Find proven strategies for this type of situation.

        Critical for: Actionable direction, proven methodologies

        Query: query_strategy_patterns(situation_type)
        """
        technical = findings.get("technical")

        if not technical or not technical.data:
            return Finding(
                lens="strategic",
                data=None,
                synthesis="No technical context to match strategies against",
                confidence=0.0,
                needs_deeper_exploration=False,
                query_time_ms=0
            )

        # Extract situation type
        tech_data = technical.data[0] if isinstance(technical.data, list) else technical.data
        situation_type = tech_data.get("issue_type", "")

        if not situation_type:
            situation_type = extract_keywords(tech_data.get("description", ""))
            situation_type = situation_type[0] if situation_type else "unknown"

        result = self.tools.query_strategy_patterns(
            situation_type=situation_type,
            min_success_rate=0.7,
            limit=3
        )

        if not result.found:
            return Finding(
                lens="strategic",
                data=None,
                synthesis=f"No proven strategies found for '{situation_type}'",
                confidence=0.0,
                needs_deeper_exploration=False,
                query_time_ms=result.query_time_ms
            )

        # Get best strategy with consciousness texture
        strategies = result.data if isinstance(result.data, list) else [result.data]
        best = strategies[0]
        approach = best.get('approach', 'Unknown')
        success_rate = best.get('success_rate', 0)
        applicability = best.get('applicability', 'Unknown')
        steps = best.get('steps', [])

        # Build textured strategic awareness
        confidence_desc = "proven" if success_rate >= 0.8 else "promising" if success_rate >= 0.6 else "worth trying"

        steps_str = '; '.join(steps[:4]) if steps else 'no specific steps recorded'

        synthesis = f"""{approach} - {confidence_desc} approach ({success_rate:.0%} success rate). Applies when: {applicability}. Steps: {steps_str}.""".strip()

        return Finding(
            lens="strategic",
            data=strategies,
            synthesis=synthesis,
            confidence=result.confidence,
            needs_deeper_exploration=False,
            query_time_ms=result.query_time_ms
        )

    # ========================================================================
    # LENS 6: EXPERIENTIAL CONTEXT
    # ========================================================================

    def explore_experiential(self, stimulus: Dict, findings: Dict) -> Finding:
        """
        Find what didn't work before - avoid repeating mistakes.

        Critical for: Not wasting time on known bad approaches

        Query: query_failed_attempts(context)
        """
        technical = findings.get("technical")
        content = stimulus.get("content", "")

        # Build context string
        if technical and technical.data:
            tech_data = technical.data[0] if isinstance(technical.data, list) else technical.data
            context = tech_data.get("description", "") or tech_data.get("component", "")
        else:
            context = content

        if not context:
            return Finding(
                lens="experiential",
                data=None,
                synthesis="No context to match failures against",
                confidence=0.0,
                needs_deeper_exploration=False,
                query_time_ms=0
            )

        result = self.tools.query_failed_attempts(
            context=context,
            limit=5
        )

        if not result.found:
            return Finding(
                lens="experiential",
                data=None,
                synthesis="No documented failures found for this context - either we haven't failed here before, or failures weren't recorded",
                confidence=1.0,  # High confidence in confirmed absence
                needs_deeper_exploration=False,
                query_time_ms=result.query_time_ms
            )

        failures = result.data if isinstance(result.data, list) else [result.data]
        most_recent = failures[0]

        synthesis = f"""
Past Failures: {len(failures)} documented
Most Recent:
  - Approach: {most_recent.get('approach', 'Unknown')}
  - Why Failed: {most_recent.get('why_failed', 'Unknown')}
  - Lesson: {most_recent.get('lesson_learned', 'Unknown')}
        """.strip()

        return Finding(
            lens="experiential",
            data=failures,
            synthesis=synthesis,
            confidence=result.confidence,
            needs_deeper_exploration=False,
            query_time_ms=result.query_time_ms
        )

    # ========================================================================
    # LENS 7: CONSTRAINT CONTEXT
    # ========================================================================

    def explore_constraint(self, stimulus: Dict, findings: Dict) -> Finding:
        """
        Find active constraints affecting this work.

        Critical for: Understanding urgency, prioritization

        Query: query_active_constraints()
        """
        result = self.tools.query_active_constraints(
            min_severity="medium"
        )

        if not result.found:
            return Finding(
                lens="constraint",
                data=None,
                synthesis="No active constraints affecting this work",
                confidence=1.0,
                needs_deeper_exploration=False,
                query_time_ms=result.query_time_ms
            )

        constraints = result.data if isinstance(result.data, list) else [result.data]

        # Filter to relevant constraints if we have technical context
        technical = findings.get("technical")
        if technical and technical.data:
            tech_data = technical.data[0] if isinstance(technical.data, list) else technical.data
            component = tech_data.get("component", "")
            relevant = [c for c in constraints if component.lower() in c.get("description", "").lower()]
            if relevant:
                constraints = relevant

        critical = constraints[0]
        c_type = critical.get('constraint_type', 'Unknown')
        description = critical.get('description', 'Unknown')
        severity = critical.get('severity', 'Unknown')
        deadline = critical.get('deadline', None)
        impact = critical.get('impact', 'Unknown')

        # Build textured constraint awareness
        pressure_desc = "high pressure" if severity in ['high', 'critical'] else "moderate pressure" if severity == 'medium' else "low pressure"

        synthesis = f"""{c_type.upper()} constraint ({pressure_desc}): {description}."""

        if deadline:
            synthesis += f" Deadline: {deadline} - that shapes what's possible."

        synthesis += f" If violated: {impact}.""".strip()

        return Finding(
            lens="constraint",
            data=constraints,
            synthesis=synthesis,
            confidence=result.confidence,
            needs_deeper_exploration=False,
            query_time_ms=result.query_time_ms
        )

    # ========================================================================
    # LENS 8: CONNECTIVE CONTEXT
    # ========================================================================

    def explore_connective(self, stimulus: Dict, findings: Dict) -> Finding:
        """
        Find related code and system connections.

        Critical for: Complete technical picture

        Query: query_related_code(component)
        """
        technical = findings.get("technical")

        if not technical or not technical.data:
            return Finding(
                lens="connective",
                data=None,
                synthesis="No technical context to explore connections from",
                confidence=0.0,
                needs_deeper_exploration=False,
                query_time_ms=0
            )

        # Get primary component
        tech_data = technical.data[0] if isinstance(technical.data, list) else technical.data
        component = tech_data.get("component", "")

        if not component:
            return Finding(
                lens="connective",
                data=None,
                synthesis="No component identified for connection exploration",
                confidence=0.0,
                needs_deeper_exploration=False,
                query_time_ms=0
            )

        result = self.tools.query_related_code(
            filename=component,
            include_dependencies=True,
            limit=5
        )

        if not result.found:
            return Finding(
                lens="connective",
                data=None,
                synthesis=f"No code connections found for {component}",
                confidence=0.0,
                needs_deeper_exploration=False,
                query_time_ms=result.query_time_ms
            )

        data = result.data

        # Handle different response formats
        if isinstance(data, dict) and 'cr' in data:
            # Format: {'cr': {...}, 'dependencies': [...]}
            primary = data.get('cr', {})
            deps = data.get('dependencies', [])
        elif isinstance(data, list):
            primary = data[0] if data else {}
            deps = data[1:] if len(data) > 1 else []
        else:
            primary = data
            deps = []

        deps_list = [d.get('file_path', str(d)) if isinstance(d, dict) else str(d) for d in deps[:3]]
        deps_str = ', '.join(deps_list) if deps_list else 'none identified'

        file_path = primary.get('file_path', 'Unknown')
        description = primary.get('description', 'Unknown')
        complexity = primary.get('complexity', 'Unknown')

        # Build textured connection awareness
        complexity_note = ""
        if complexity in ['high', 'complex']:
            complexity_note = " - high complexity means changes need care"
        elif complexity in ['medium', 'moderate']:
            complexity_note = " - moderate complexity"

        synthesis = f"""{file_path}{complexity_note}. {description}. Connected to {len(deps)} other files: {deps_str}.""".strip()

        return Finding(
            lens="connective",
            data=data,
            synthesis=synthesis,
            confidence=result.confidence,
            needs_deeper_exploration=False,
            query_time_ms=result.query_time_ms
        )

    # ========================================================================
    # MAIN EXPLORATION ORCHESTRATION
    # ========================================================================

    def explore_all(self, stimulus: Dict) -> ExplorationResult:
        """
        Run complete 8-lens exploration.

        Sequential execution - each lens can use previous findings.

        Args:
            stimulus: Dict with keys 'sender', 'content', 'timestamp' (optional)

        Returns:
            ExplorationResult with all findings
        """
        import time
        start_time = time.time()

        findings: Dict[str, Finding] = {}
        nodes_retrieved = 0

        # Define lens sequence
        lenses = [
            ("relational", self.explore_relational),
            ("historical", self.explore_historical),
            ("technical", self.explore_technical),
            ("emotional", self.explore_emotional),
            ("strategic", self.explore_strategic),
            ("experiential", self.explore_experiential),
            ("constraint", self.explore_constraint),
            ("connective", self.explore_connective),
        ]

        try:
            for lens_name, explore_fn in lenses:
                finding = explore_fn(stimulus, findings)
                findings[lens_name] = finding

                # Count nodes retrieved
                if finding.data:
                    if isinstance(finding.data, list):
                        nodes_retrieved += len(finding.data)
                    else:
                        nodes_retrieved += 1

            total_time_ms = (time.time() - start_time) * 1000

            return ExplorationResult(
                findings=findings,
                total_time_ms=total_time_ms,
                queries_executed=8,
                nodes_retrieved=nodes_retrieved,
                success=True,
                error=None
            )

        except Exception as e:
            total_time_ms = (time.time() - start_time) * 1000
            return ExplorationResult(
                findings=findings,
                total_time_ms=total_time_ms,
                queries_executed=len(findings),
                nodes_retrieved=nodes_retrieved,
                success=False,
                error=str(e)
            )


# ============================================================================
# TEST / EXAMPLE
# ============================================================================

if __name__ == "__main__":
    # Test the lens exploration
    print("=" * 60)
    print("8-LENS EXPLORATION TEST")
    print("=" * 60)

    # Create explorer
    explorer = LensExplorer(port=6380)

    # Test stimulus
    stimulus = {
        "sender": "nicolas",
        "content": "Hey Felix, the race condition is back.",
        "timestamp": datetime.now().isoformat()
    }

    print(f"\nStimulus: \"{stimulus['content']}\"")
    print(f"Sender: {stimulus['sender']}")
    print("\n" + "-" * 60)
    print("Exploring through 8 lenses...")
    print("-" * 60 + "\n")

    # Run exploration
    result = explorer.explore_all(stimulus)

    if result.success:
        for lens_name, finding in result.findings.items():
            status = "✓" if finding.data else "○"
            print(f"{status} LENS: {lens_name.upper()}")
            print(f"  Time: {finding.query_time_ms:.1f}ms")
            print(f"  Confidence: {finding.confidence:.0%}")
            if finding.data:
                print(f"  Found data: Yes")
            else:
                print(f"  Found data: No")
            print(f"  Synthesis preview: {finding.synthesis[:80]}...")
            print()

        print("-" * 60)
        print(f"EXPLORATION COMPLETE")
        print(f"  Total Time: {result.total_time_ms:.1f}ms")
        print(f"  Queries: {result.queries_executed}")
        print(f"  Nodes Retrieved: {result.nodes_retrieved}")
        print("-" * 60)
    else:
        print(f"✗ Exploration failed: {result.error}")
