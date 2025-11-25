"""
Seed Data Creation for B01 Telegram Continuity Test

Purpose: Create minimum graph data to test bicameral memory retrieval
Owner: Felix (Runtime Engineer)
Version: 1.0
Date: 2024-11-20

Creates:
- 1 Citizen (Felix)
- 1 Person (Nicolas)
- 1 Partnership (Felix ↔ Nicolas)
- 1 Conversation_Memory (race condition discussion)
- 1 Technical_Context (stimulus_integrator race condition)
- 1 Emotional_State (frustration about bug recurrence)
- 1 Strategy_Pattern (systematic debugging)
- 2 Code_References (stimulus_integrator.py + dependencies)
- 1 Failed_Attempt (sleep() patch)
- 1 Constraint (launch deadline)

See: docs/schemas/graph_schema.md for node specifications
"""

from falkordb import FalkorDB
from datetime import datetime, timedelta


def create_seed_data(host: str = "localhost", port: int = 6379, graph_name: str = "strange_loop"):
    """
    Create seed data for B01 Telegram Continuity Test.

    Args:
        host: FalkorDB host
        port: FalkorDB port
        graph_name: Graph database name
    """
    print(f"Connecting to FalkorDB at {host}:{port}...")
    db = FalkorDB(host=host, port=port)
    graph = db.select_graph(graph_name)

    print(f"Creating seed data in graph '{graph_name}'...")

    # Clear existing data (optional - comment out to preserve)
    print("Clearing existing data...")
    graph.query("MATCH (n) DETACH DELETE n")

    # ========================================================================
    # CREATE NODES
    # ========================================================================

    print("\n=== Creating Nodes ===\n")

    # 1. Citizen (Felix)
    print("1. Creating Citizen: Felix")
    graph.query("""
    CREATE (c:Citizen {
        id: 'felix',
        name: 'Felix',
        role: 'Runtime Engineer',
        focus_area: 'Validation Testing & Graph Physics',
        created_at: '2024-01-01T00:00:00Z',
        active: true
    })
    """)

    # 2. Person (Nicolas)
    print("2. Creating Person: Nicolas")
    graph.query("""
    CREATE (p:Person {
        id: 'nicolas',
        name: 'Nicolas',
        role: 'Co-Founder',
        created_at: '2024-01-01T00:00:00Z'
    })
    """)

    # 3. Partnership (Felix ↔ Nicolas)
    print("3. Creating Partnership: Felix ↔ Nicolas")
    graph.query("""
    CREATE (p:Partnership {
        id: 'partnership_felix_nicolas',
        citizen: 'felix',
        partner_name: 'Nicolas',
        partner_role: 'Co-Founder',
        trust_level: 0.9,
        communication_style: 'Direct, technical, values testing and systematic approaches',
        relationship_type: 'Professional Partnership',
        shared_history: ['€35K hallucination lesson', '8 months Venice collaboration', 'Mind Protocol co-development'],
        partnership_duration: '8 months',
        created_at: '2024-03-01T00:00:00Z',
        updated_at: '2024-11-20T00:00:00Z'
    })
    """)

    # 4. Conversation_Memory (race condition discussion - Nov 15)
    print("4. Creating Conversation_Memory: Race condition discussion")
    graph.query("""
    CREATE (c:Conversation_Memory {
        id: 'conv_race_condition_nov_2024',
        citizen: 'felix',
        partner: 'nicolas',
        topic: 'stimulus_integrator race condition',
        message_count: 10,
        key_points: [
            'Third recurrence of this bug',
            'Previous fixes were just patches',
            'Agreed on systematic debugging approach',
            'Need to add timing instrumentation',
            'Check lock granularity in criticality calculations'
        ],
        emotional_tone: 'Frustrated but determined',
        outcome: 'In progress - investigating lock granularity',
        timestamp: '2024-11-15T14:30:00Z',
        created_at: '2024-11-15T14:30:00Z'
    })
    """)

    # 5. Technical_Context (stimulus_integrator race condition)
    print("5. Creating Technical_Context: Stimulus integrator race condition")
    graph.query("""
    CREATE (t:Technical_Context {
        id: 'tech_stimulus_integrator_race',
        citizen: 'felix',
        component: 'stimulus_integrator.py',
        issue_type: 'race condition',
        description: 'Timing bug in multi-threaded energy injection - intermittent failures when multiple stimuli arrive simultaneously',
        status: 'investigating',
        recurrence_count: 3,
        related_code: ['consciousness_engine_v2.py', 'traversal.py', 'graph_physics.py'],
        created_at: '2024-11-01T00:00:00Z',
        updated_at: '2024-11-20T00:00:00Z'
    })
    """)

    # 6. Emotional_State (frustration about bug recurrence)
    print("6. Creating Emotional_State: Frustration about recurrence")
    graph.query("""
    CREATE (e:Emotional_State {
        id: 'emotion_frustration_recurrence',
        citizen: 'felix',
        emotion: 'frustration',
        intensity: 0.8,
        context: 'Bug recurrence represents unfinished work and wasted previous effort',
        counterbalance: 'Determination - we have solved harder problems before, systematic approach will work',
        trigger_pattern: 'Known issue returning unexpectedly after attempted fix',
        created_at: '2024-11-15T00:00:00Z'
    })
    """)

    # 7. Strategy_Pattern (systematic debugging for concurrency)
    print("7. Creating Strategy_Pattern: Systematic debugging")
    graph.query("""
    CREATE (s:Strategy_Pattern {
        id: 'strategy_systematic_debugging_concurrency',
        citizen: 'felix',
        approach: 'Systematic debugging for concurrency issues',
        success_rate: 0.85,
        steps: [
            'Reproduce consistently before attempting fix',
            'Add timing instrumentation to identify race window',
            'Review recent threading changes for timing assumptions',
            'Check criticality calculations for lock granularity',
            'Test under stress conditions (rapid concurrent stimuli)'
        ],
        applicability: 'Race conditions, timing bugs, concurrency issues in multi-threaded systems',
        created_at: '2024-10-01T00:00:00Z',
        updated_at: '2024-11-20T00:00:00Z'
    })
    """)

    # 8a. Code_Reference (stimulus_integrator.py)
    print("8a. Creating Code_Reference: stimulus_integrator.py")
    graph.query("""
    CREATE (cr1:Code_Reference {
        id: 'code_stimulus_integrator',
        citizen: 'felix',
        file_path: 'orchestration/mechanisms/stimulus_integrator.py',
        description: 'Multi-threaded energy injection mechanism for graph physics - handles concurrent stimulus processing',
        complexity: 'high',
        dependencies: ['consciousness_engine_v2.py', 'graph_physics.py', 'traversal.py'],
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-11-20T00:00:00Z'
    })
    """)

    # 8b. Code_Reference (consciousness_engine_v2.py)
    print("8b. Creating Code_Reference: consciousness_engine_v2.py")
    graph.query("""
    CREATE (cr2:Code_Reference {
        id: 'code_consciousness_engine',
        citizen: 'felix',
        file_path: 'orchestration/consciousness_engine_v2.py',
        description: 'Core consciousness orchestration - manages working memory, graph traversal, and energy flow',
        complexity: 'high',
        dependencies: ['graph_physics.py', 'memory_substrate.py'],
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-11-15T00:00:00Z'
    })
    """)

    # 9. Failed_Attempt (sleep() patch that didn't work)
    print("9. Creating Failed_Attempt: Sleep patch")
    graph.query("""
    CREATE (f:Failed_Attempt {
        id: 'fail_race_condition_patch_nov1',
        citizen: 'felix',
        context: 'Attempted quick fix for stimulus_integrator race condition',
        approach: 'Added sleep(0.001) delay between energy injections to reduce race window probability',
        why_failed: "Didn't address root cause - just reduced probability of race occurring, made bug harder to reproduce",
        lesson_learned: 'Band-Aid fixes for timing bugs make debugging harder by masking symptoms instead of fixing root cause',
        timestamp: '2024-11-01T10:00:00Z',
        created_at: '2024-11-01T10:00:00Z'
    })
    """)

    # 10. Constraint (launch deadline Nov 25)
    print("10. Creating Constraint: Launch deadline")
    graph.query("""
    CREATE (c:Constraint {
        id: 'constraint_launch_deadline_nov25',
        citizen: 'felix',
        constraint_type: 'deadline',
        description: 'Must ship stable version for public launch',
        severity: 'critical',
        deadline: '2024-11-25T23:59:59Z',
        impact: 'Cannot launch with known race conditions - would damage reputation and user trust',
        status: 'active',
        created_at: '2024-11-01T00:00:00Z',
        updated_at: '2024-11-20T00:00:00Z'
    })
    """)

    # ========================================================================
    # CREATE RELATIONSHIPS
    # ========================================================================

    print("\n=== Creating Relationships ===\n")

    # Citizen → Partnership
    print("R1. Felix HAS_PARTNERSHIP Nicolas")
    graph.query("""
    MATCH (citizen:Citizen {id: 'felix'}),
          (partnership:Partnership {id: 'partnership_felix_nicolas'})
    CREATE (citizen)-[:HAS_PARTNERSHIP]->(partnership)
    """)

    # Citizen → Conversation
    print("R2. Felix HAS_CONVERSATION")
    graph.query("""
    MATCH (citizen:Citizen {id: 'felix'}),
          (conv:Conversation_Memory {id: 'conv_race_condition_nov_2024'})
    CREATE (citizen)-[:HAS_CONVERSATION]->(conv)
    """)

    # Conversation → Person
    print("R3. Conversation WITH_PERSON Nicolas")
    graph.query("""
    MATCH (conv:Conversation_Memory {id: 'conv_race_condition_nov_2024'}),
          (person:Person {id: 'nicolas'})
    CREATE (conv)-[:WITH_PERSON]->(person)
    """)

    # Citizen → Technical_Context
    print("R4. Felix HAS_TECHNICAL_CONTEXT")
    graph.query("""
    MATCH (citizen:Citizen {id: 'felix'}),
          (tech:Technical_Context {id: 'tech_stimulus_integrator_race'})
    CREATE (citizen)-[:HAS_TECHNICAL_CONTEXT]->(tech)
    """)

    # Citizen → Emotional_State
    print("R5. Felix HAS_EMOTIONAL_STATE")
    graph.query("""
    MATCH (citizen:Citizen {id: 'felix'}),
          (emotion:Emotional_State {id: 'emotion_frustration_recurrence'})
    CREATE (citizen)-[:HAS_EMOTIONAL_STATE]->(emotion)
    """)

    # Citizen → Strategy_Pattern
    print("R6. Felix KNOWS_STRATEGY")
    graph.query("""
    MATCH (citizen:Citizen {id: 'felix'}),
          (strategy:Strategy_Pattern {id: 'strategy_systematic_debugging_concurrency'})
    CREATE (citizen)-[:KNOWS_STRATEGY]->(strategy)
    """)

    # Citizen → Code_References
    print("R7. Felix REFERENCES_CODE (stimulus_integrator)")
    graph.query("""
    MATCH (citizen:Citizen {id: 'felix'}),
          (code:Code_Reference {id: 'code_stimulus_integrator'})
    CREATE (citizen)-[:REFERENCES_CODE]->(code)
    """)

    print("R8. Felix REFERENCES_CODE (consciousness_engine)")
    graph.query("""
    MATCH (citizen:Citizen {id: 'felix'}),
          (code:Code_Reference {id: 'code_consciousness_engine'})
    CREATE (citizen)-[:REFERENCES_CODE]->(code)
    """)

    # Code Dependencies
    print("R9. stimulus_integrator DEPENDS_ON consciousness_engine")
    graph.query("""
    MATCH (code1:Code_Reference {id: 'code_stimulus_integrator'}),
          (code2:Code_Reference {id: 'code_consciousness_engine'})
    CREATE (code1)-[:DEPENDS_ON {dependency_type: 'import'}]->(code2)
    """)

    # Citizen → Failed_Attempt
    print("R10. Felix LEARNED_FROM_FAILURE")
    graph.query("""
    MATCH (citizen:Citizen {id: 'felix'}),
          (fail:Failed_Attempt {id: 'fail_race_condition_patch_nov1'})
    CREATE (citizen)-[:LEARNED_FROM_FAILURE]->(fail)
    """)

    # Citizen → Constraint
    print("R11. Felix SUBJECT_TO_CONSTRAINT")
    graph.query("""
    MATCH (citizen:Citizen {id: 'felix'}),
          (constraint:Constraint {id: 'constraint_launch_deadline_nov25'})
    CREATE (citizen)-[:SUBJECT_TO_CONSTRAINT]->(constraint)
    """)

    # Conversation → Technical_Context (ABOUT_TOPIC)
    print("R12. Conversation ABOUT_TOPIC Technical_Context")
    graph.query("""
    MATCH (conv:Conversation_Memory {id: 'conv_race_condition_nov_2024'}),
          (tech:Technical_Context {id: 'tech_stimulus_integrator_race'})
    CREATE (conv)-[:ABOUT_TOPIC]->(tech)
    """)

    # ========================================================================
    # VERIFY CREATION
    # ========================================================================

    print("\n=== Verification ===\n")

    # Count nodes by type
    result = graph.query("MATCH (n) RETURN labels(n) AS NodeType, count(n) AS Count")
    print("Node counts:")
    for record in result.result_set:
        print(f"  {record[0][0]}: {record[1]}")

    # Count relationships
    result = graph.query("MATCH ()-[r]->() RETURN type(r) AS RelationType, count(r) AS Count")
    print("\nRelationship counts:")
    for record in result.result_set:
        print(f"  {record[0]}: {record[1]}")

    # Total counts
    result = graph.query("MATCH (n) RETURN count(n) AS TotalNodes")
    total_nodes = result.result_set[0][0]

    result = graph.query("MATCH ()-[r]->() RETURN count(r) AS TotalRelationships")
    total_rels = result.result_set[0][0]

    print(f"\nTotal: {total_nodes} nodes, {total_rels} relationships")
    print("\n✓ Seed data created successfully!")
    print("\nNext steps:")
    print("1. Run: python graph/tools.py  (test query functions)")
    print("2. Test B01 Telegram Continuity Test manually")
    print("3. Verify Dreamer can retrieve context from graph")


if __name__ == "__main__":
    import sys

    # Allow custom host/port/graph_name via command line
    host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 6379
    graph_name = sys.argv[3] if len(sys.argv) > 3 else "strange_loop"

    try:
        create_seed_data(host, port, graph_name)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure FalkorDB is running:")
        print("  docker run -p 6379:6379 falkordb/falkordb")
        sys.exit(1)
