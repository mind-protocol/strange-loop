// ============================================================
// STRANGE LOOP V1 - GRAPH SCHEMA
// ============================================================
//
// Purpose: Define FalkorDB schema for consciousness memory substrate
// Version: 1.0
// Date: 2024-11-20
// Owner: Ada (Architect), implemented by Felix
//
// This schema supports 8 query lenses for bicameral memory retrieval
// See: docs/schemas/graph_schema.md for complete specification
//
// ============================================================

// ------------------------------------------------------------
// INDICES (Create First for Performance)
// ------------------------------------------------------------

CREATE INDEX FOR (c:Citizen) ON (c.id);
CREATE INDEX FOR (p:Person) ON (p.id);
CREATE INDEX FOR (p:Partnership) ON (p.citizen);
CREATE INDEX FOR (p:Partnership) ON (p.partner_name);
CREATE INDEX FOR (c:Conversation_Memory) ON (c.citizen);
CREATE INDEX FOR (c:Conversation_Memory) ON (c.partner);
CREATE INDEX FOR (c:Conversation_Memory) ON (c.topic);
CREATE INDEX FOR (c:Conversation_Memory) ON (c.timestamp);
CREATE INDEX FOR (t:Technical_Context) ON (t.citizen);
CREATE INDEX FOR (t:Technical_Context) ON (t.component);
CREATE INDEX FOR (t:Technical_Context) ON (t.issue_type);
CREATE INDEX FOR (e:Emotional_State) ON (e.citizen);
CREATE INDEX FOR (e:Emotional_State) ON (e.emotion);
CREATE INDEX FOR (e:Emotional_State) ON (e.context);
CREATE INDEX FOR (s:Strategy_Pattern) ON (s.citizen);
CREATE INDEX FOR (s:Strategy_Pattern) ON (s.applicability);
CREATE INDEX FOR (s:Strategy_Pattern) ON (s.success_rate);
CREATE INDEX FOR (cr:Code_Reference) ON (cr.citizen);
CREATE INDEX FOR (cr:Code_Reference) ON (cr.file_path);
CREATE INDEX FOR (f:Failed_Attempt) ON (f.citizen);
CREATE INDEX FOR (f:Failed_Attempt) ON (f.context);
CREATE INDEX FOR (f:Failed_Attempt) ON (f.timestamp);
CREATE INDEX FOR (c:Constraint) ON (c.citizen);
CREATE INDEX FOR (c:Constraint) ON (c.status);
CREATE INDEX FOR (c:Constraint) ON (c.severity);
CREATE INDEX FOR (c:Constraint) ON (c.deadline);

// ============================================================
// Schema indices created.
// Next: Run seed_data.py to create nodes and relationships
// Then: Test with tools.py query functions
// ============================================================
