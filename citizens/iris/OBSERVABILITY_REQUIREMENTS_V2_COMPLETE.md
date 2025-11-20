# Observability Requirements - V2 Specs Extraction

**Generated:** 2025-10-23
**Source:** Complete analysis of Mind Protocol V2 specification files
**Purpose:** Comprehensive inventory of all observability requirements for implementation

---

## 1. Diffusion v2 (Stride-based, Active-Frontier)

**File:** `C:\Users\reyno\mind-protocol\docs\specs\v2\foundations\diffusion_v2.md`

### Events/Metrics

**Per Stride (`stride.exec`):**
- `src` - source node ID
- `tgt` - target node ID
- `ΔE` - energy transferred
- `E_src_pre` - source energy before stride
- `E_tgt_pre` - target energy before stride
- `E_tgt_post` - target energy after stride
- `phi` - utility/gap closure score
- `z_flow` - standardized flow metric
- `score` - candidate selection score
- `selected_reason` - why this edge was chosen (top_k/fanout)

**Per Frame Diagnostics (new counters):**
- `energy_in` - sum of stimulus injections this frame
- `energy_transferred` - sum of all |ΔE| moved
- `energy_decay` - total loss to decay (state) with per-type breakdown
- `conservation_error` - absolute & percentage
- `frontier_size_active` - count of nodes above threshold
- `frontier_size_shadow` - count of 1-hop neighbors
- `mean_degree_active` - average out-degree of active nodes
- `diffusion_radius_from_seeds` - how far from initial stimuli

**Subentity Boundary Summaries:**
- Cross-entity beam count
- Sum of ΔE across entity boundaries
- Max φ (utility) on boundary crossings
- Typical hunger scores

### Dashboards

**Frame-level visualization needs:**
- Expanding "beams" visualization instead of uniform glow
- Boundary summaries showing focused cross-entity flow
- Conservation tracking dashboard

### Measurements

**What to measure:**
- `frontier_size_active` with `energy_in` correlation
- `conservation_error` trends
- `diffusion_radius` expansion/contraction

**Why it matters (interpretation guide):**
- Rising `frontier_size_active` with stable `energy_in` → system relying on internal attractors (expect growth in high-weight regions)
- High `conservation_error` → bug (order-of-ops or double-apply)
- Increasing `diffusion_radius` → exploration mode
- Falling radius with high φ → exploitation around good attractors

### UI/UX Requirements

- 2-frame reorder buffer for event stream
- Redraw visualization at `frame.end` events
- Visual distinction between frontier and shadow nodes
- Beam visualization showing energy flow between entities

---

## 2. Energy & Weight Decay (Forgetting with Control)

**File:** `C:\Users\reyno\mind-protocol\docs\specs\v2\foundations\decay.md`

### Events/Metrics

**Per Tick:**
- `decay.tick{delta_E, delta_W}` - aggregated decay amounts for energy and weights
- **Half-life estimates** per node/link type
- **Energy histogram** by degree and type
- **Weight histogram** by type
- **AUC activation** in time windows

**Balance Tracking:**
- **Decay vs reinforcement balance curves** on tracked nodes (validate realistic stabilization)

### Dashboards

**Forgetting Curves:**
- Small multiples visualization showing decay over time
- Separate curves per node type

**Type Panels:**
- Memory type panel
- Task type panel
- Default type panel

**Controller Timeline:**
- ρ (spectral radius) timeline
- Controller outputs overlaid

### Measurements

**What to measure:**
- Half-life per type (does it match spec targets?)
- Energy persistence vs weight persistence differential
- Decay amount vs reinforcement amount balance

**Why it matters:**
- Validates type-dependent forgetting works as designed
- Ensures weights persist longer than activation (enables context reconstruction)
- Confirms controller stability

---

## 3. Self-Organized Criticality (Spectral Radius ρ)

**File:** `C:\Users\reyno\mind-protocol\docs\specs\v2\foundations\criticality.md`

### Events/Metrics

**Core Measurements:**
- `rho.global` - authoritative spectral radius estimate (via power iteration)
- `rho.proxy.branching` - cheap branching ratio B = Σoutflow/Σinflow on active frontier
- `rho.var.window` - variance of ρ over recent window
- Controller outputs: `Δδ` (decay adjustment), `Δα` (diffusion share adjustment)
- **Safety state** enum: `subcritical|critical|supercritical`

**Optional Entity-View:**
- Compute ρ on membership-weighted subgraph of active entity (read-only projection)
- Helps explain "this entity was too lively" without violating single-energy

**Oscillation Tracking:**
- **Oscillation index** - count of sign changes of (ρ-1)

### Dashboards

**Operator Dashboard:**
- Clear read of when/why ρ moved
- Which lever acted (δ vs α)
- Current safety state
- Oscillation warnings

**Entity-Level View:**
- Per-entity ρ estimates (diagnostic only, not for control)

### Measurements

**What to measure:**
- ρ mean over time
- ρ variance
- Oscillation frequency
- Controller gain effectiveness

**How to interpret:**
- **ρ ≈ 1 ± 0.1** → healthy system
- **ρ > 1.2** sustained → clamp α and lift δ a notch
- **ρ < 0.8** → back off δ
- High oscillation index → lower controller gains (PID D-term)

**Success criteria:**
- ρ mean in [0.95, 1.05] with low variance under realistic stimulus schedules
- No growth in flip-thrash
- WM selection stable

---

## 4. Tick Speed Regulation

**File:** `C:\Users\reyno\mind-protocol\docs\specs\v2\runtime_engine\tick_speed.md`

### Events/Metrics

**Per Tick:**
- `tick_frame` event with:
  - `dt_ms` - wall-clock milliseconds since last tick
  - `interval_sched` - scheduled interval
  - `dt_used` - physics dt actually used (capped)
  - `rho` - current spectral radius
  - `notes` - e.g., "dt capped", "EMA smoothing applied"

**Metrics:**
- **Tick rate over time** - ticks per second trending
- **Computational savings** - % CPU reduction vs fixed-rate baseline
- **dt cap hits** - frequency of max_dt clipping

### Dashboards

**Per-Mode Strips:**
- "Conversation" mode tick rate visualization
- "Dormant" mode tick rate visualization
- Mode transitions clearly marked

**Timing Analysis:**
- Latency from stimulus→tick
- dt_used vs interval_sched comparison
- EMA smoothing effect visualization

### Measurements

**What to measure:**
- Response latency (stimulus arrival to first tick)
- Tick rate adaptation speed
- CPU utilization by mode
- dt cap hit frequency

**Success criteria:**
- Latency from stimulus→tick ≤ min_interval
- No dt blow-ups
- Stable ρ across mode shifts

---

## 5. Traversal v2 (Frame Pipeline)

**File:** `C:\Users\reyno\mind-protocol\docs\specs\v2\runtime_engine\traversal_v2.md`

### Events/Metrics

**Per Stride:**
- `stride.exec` samples with:
  - `src`, `dst` - node IDs
  - `dE` - energy transferred
  - `phi` - utility score
  - `ease` - from weight
  - `res...` - resonance multipliers (if emotion gates enabled)
  - `comp...` - complementarity multipliers (if emotion gates enabled)

**Per Frame:**
- `node.flip` - threshold crossing events
- `tick_frame` with frontier stats:
  - `active` - count of active nodes
  - `shadow` - count of shadow nodes
- `se.boundary.summary` - for entity exits
- `frame.end` with:
  - Conservation check results
  - Timing breakdown

### Dashboards

**Frontier Visualization:**
- Active nodes highlighted
- Shadow nodes shown differently
- Frontier evolution over time

**Entity Boundary View:**
- Cross-entity stride visualization
- Boundary summary stats

### Measurements

**What to measure:**
- Frontier size trends
- Conservation accuracy
- Stride execution throughput
- Entity boundary crossing frequency

**Success criteria:**
- Throughput stable with frontier size, not global N
- ρ ≈ 1 maintained
- Context reconstruction latency maintained or improved
- Events explain all decisions

---

## 6. Local Fanout Strategy

**File:** `C:\Users\reyno\mind-protocol\docs\specs\v2\runtime_engine\fanout_strategy.md`

### Events/Metrics

**Per Edge:**
- `stride.exec` carries:
  - Per-edge costs
  - `comp` (complementarity) multipliers
  - `res` (resonance) multipliers

**Per Node Sample:**
- `tick_frame` includes for sampled nodes:
  - `fanout: d` - out-degree
  - `top_k` - how many candidates selected

**Metrics:**
- **Prune rate** - fraction of edges removed by strategy before scoring
- **K usage distribution** - histogram of top_k values chosen
- **Selection entropy** at hubs - diversity of choices made at high-degree nodes

### Dashboards

**Node-Level:**
- "Fanout dial" overlay on nodes showing strategy selected
- Strategy color-coding (Selective/Balanced/Exhaustive)

**Distribution Views:**
- Histogram: top-K sizes vs WM headroom
- Prune rate by node degree bins
- Selection entropy heatmap

### Measurements

**What to measure:**
- CPU per tick scaling (should scale with frontier, not total nodes)
- Prune rate correlation with fanout
- Task throughput at hubs

**Success criteria:**
- Prune rate rises with fanout
- Task throughput improves at hubs without harming recall

---

## 7. Type-Dependent Decay

**File:** `C:\Users\reyno\mind-protocol\docs\specs\v2\runtime_engine\type_dependent_decay.md`

### Events/Metrics

**Per Type:**
- **Half-life estimates** (fit from telemetry)
  - Memory nodes: 12-24h (energy), weeks-months (weight)
  - Principle nodes: 6-12h (energy), months (weight)
  - Concept nodes: 3-6h (energy), weeks (weight)
  - Task nodes: 1-3h (energy), days (weight)
  - Trigger nodes: 2-4h (energy), weeks (weight)

**Histograms:**
- Energy histogram by type
- Weight histogram by type

**Balance Curves:**
- Decay vs reinforcement balance per type

### Dashboards

**Type Panels:**
- Per-type decay curves
- Half-life tracking over time
- Type-specific activation persistence

### Measurements

**What to measure:**
- Actual half-life vs target half-life per type
- Reconstruction success rate after long gaps
- Memory drift detection

**Success criteria:**
- Meets half-life targets
- Reconstruction success after long gaps
- Stable ρ
- No silent memory drift

---

## 8. Subentity Layer (Overview)

**File:** `C:\Users\reyno\mind-protocol\docs\specs\v2\subentity_layer\subentity_layer.md`

### Events/Metrics

**Events:**
- `subentity.flip` on threshold crossings:
  - `E` - entity energy
  - `Θ` - entity threshold
  - `activation_level` - classification

- `subentity.boundary.summary` for beams between entities:
  - `count` - number of boundary strides
  - `sum_ΔE` - total energy transferred across boundary
  - `top_hunger` - highest hunger score
  - `φ_max` - maximum utility achieved

- `subentity.weights.updated` when entity-scale log-weights change

**Derived Metrics:**
- **Entity vitality** - E/Θ ratio
- **Coherence** - member similarity EMA
- **Integration index** - boundary φ density into target entity
- **Diversity (completeness) index** - semantic spread of member set

### Dashboards

**Entity View:**
- WM shows 5-7 coherent entities with summaries
- Top members per entity
- Entity vitality indicators

**Boundary View:**
- "Entity highways" - stable cross-entity paths
- Boundary beam strength visualization
- Integration index heatmap

### Measurements

**What to measure:**
- WM chunk count (should be 5-7)
- WM chunk stability (minutes)
- Active-frontier traversal cost reduction
- Boundary summary correlation with successful TRACEs

**Success criteria:**
- WM shows 5-7 coherent entities with stable summaries
- Active-frontier traversal cost drops
- Coverage & φ improve across frames
- Boundary summaries reveal stable entity highways

---

## 9. Stimulus Injection

**File:** `C:\Users\reyno\mind-protocol\docs\specs\v2\subentity_layer\stimulus_injection.md`

### Events/Metrics

**High-Level Event:**
- `stimulus.injected` with:
  - **Budget breakdown:**
    - `base` - base budget
    - `health` - health modulation factor
    - `source` - source impact gate factor
    - `peripheral` - peripheral amplification factor
    - `final` - total budget after all gates
  - **Flips and coverage stats:**
    - Nodes flipped by injection
    - Coverage entropy

**Per-Item Event:**
- `stimulus.item_injected` for each matched item:
  - `similarity` - retrieval similarity score
  - `ΔE` - energy injected
  - `gap_before` - gap before injection
  - `gap_after` - gap after injection

### Dashboards

**Attribution View:**
- Budget breakdown pie chart (base/health/source/peripheral)
- Attribution shares trending over time

**Coverage View:**
- Coverage entropy over stimuli
- Diversity of matched types
- Entity-first activation patterns

### Measurements

**Meaningful Metrics:**
- **Flip yield** - flips / budget (higher is better)
- **Coverage entropy** - diversity of matched types
- **Attribution shares** - health vs source vs peripheral contribution to final budget

**What to measure:**
- Immediate flip rate
- Flip yield trends
- Budget waste (overshoot vs gap)
- Entity-level activation distribution

**Success criteria:**
- Flip yield increases at equal budgets
- Waste (overshoot vs gap) decreases
- Viz dashboards show clear budget attributions
- Entity-first activation patterns visible

---

## 10. Subentity Weight Learning (BELONGS_TO)

**File:** `C:\Users\reyno\mind-protocol\docs\specs\v2\subentity_layer\subentity_weight_learning.md`

### Events/Metrics

**Events:**
- `subentity.weights.updated` with:
  - `source` - "coact|wm|trace|form"
  - `log_weight_before`
  - `log_weight_after`
  - `η` - step size used
  - Per-signal z-scores:
    - `z_coact` - co-activation signal
    - `z_wm` - WM presence signal
    - `z_rein` - TRACE reinforcement signal
    - `z_form` - formation quality signal

### Dashboards

**Membership Evolution:**
- Rising members per entity (Δ log_weight rank)
- Top members per entity over time

**Coherence Tracking:**
- Membership sparsity vs entity size
- Coherence EMA trends

### Measurements

**What to measure:**
- Top member stability (churn rate)
- Membership sparsity per entity
- Coherence EMA correlation with WM quality

**Success criteria:**
- For active entities, top members stabilize (low churn)
- Tail remains plastic
- WM summaries feel on-topic
- Boundary strides reflect coherent neighborhoods

---

## 11. TRACE Weight Learning

**File:** `C:\Users\reyno\mind-protocol\docs\specs\v2\learning_and_trace\trace_weight_learning.md`

### Events/Metrics

**Events:**
- `weights.updated.trace` with:
  - Cohort stats (μ, σ per type+scope)
  - Seat history
  - Quality history

**Per-Item Panels:**
- Seat accumulation over time
- Formation quality components (C×E×N)

### Dashboards

**Distribution View:**
- z-score distributions by type
- Update deltas over time

**Cohort Monitoring:**
- Cohort size alerts (warn when N < 3)
- Cohort fallback frequency

### Measurements

**Metrics:**
- z distributions by type
- Update deltas magnitude
- Cohort size tracking

**What to measure:**
- Stable distributions maintained?
- Explainable movements in weights?
- Improved retrieval/WM selection correlated with positive z?

---

## 12. TRACE Reinforcement

**File:** `C:\Users\reyno\mind-protocol\docs\specs\v2\learning_and_trace\trace_reinforcement.md`

### Events/Metrics

**Events:**
- `trace.parsed` with:
  - Pool sizes (positive/negative)
  - Seats allocated per label
  - Hamilton apportionment results

- `weights.updated.trace` with:
  - Cohorts used
  - Δμ (mean change)

### Dashboards

**Per-TRACE View:**
- Seat allocation tables
- Positive vs negative pool breakdown

**Formation View:**
- Formation component breakdowns (C, E, N)
- Geometric mean visualization

### Measurements

**Diagnostics:**
- Seat distributions track TRACE density?
- Stable weight baselines maintained?
- Explainable updates via audit panes?

---

## 13. Duplicate Node Merging

**File:** `C:\Users\reyno\mind-protocol\docs\specs\v2\learning_and_trace\duplicate_node_merging.md`

### Events/Metrics

**Events:**
- `node.merge` with:
  - `kept` - canonical node ID
  - `absorbed[]` - array of merged node IDs
  - `scores` - similarity/match scores
  - `before_degree` - degree before merge
  - `after_degree` - degree after merge
  - `before_zW` - standardized weight before
  - `after_zW` - standardized weight after

- `link.redirect` for each changed edge

**Metrics:**
- **Merge rate** - merges per day/week
- **False-positive appeals** - manual reversals requested
- **Post-merge retrieval lift** - MRR/Recall@k improvement
- **Telemetry consolidation ratio** - flow EMA before→after

### Dashboards

**Before/After Ego-Nets:**
- Visualization showing node neighborhoods before and after merge
- Edge consolidation view

**Alias Tracking:**
- Drift of aliases over time
- Cohort-level fan-out reduction

### Measurements

**What to measure:**
- 30-60% drop in alias collisions (target)
- Measurable Recall@k improvement
- Zero critical false merges over N weeks

---

## 14. Incomplete Node Healing

**File:** `C:\Users\reyno\mind-protocol\docs\specs\v2\learning_and_trace\incomplete_node_healing.md`

### Events/Metrics

**Events:**
- `node.incomplete` - when incomplete node created
- `link.incomplete` - when incomplete link created
- `task.create` - healing task created
- `task.resolve` - task completed
- `eligibility.update` - eligibility status changed

**Metrics:**
- **Backlog** - count of incomplete items by type/scope
- **Median time-to-complete** - healing latency
- **% auto-completed by strategy** - effectiveness of different completion strategies
- **Eligibility hit/miss rate** - how often ineligible nodes are filtered in selectors

### Dashboards

**Missing Field Heatmaps:**
- Per-type missing field visualization
- Which fields are most commonly missing

**Time-Bounded Context Panes:**
- Show ±5 min context around incomplete nodes
- Used by completion strategies

**Task Backlog View:**
- Owner quotas
- Backlog alerts
- SLA tracking

### Measurements

**What to measure:**
- >90% completion within SLA
- Zero selection of incomplete nodes (verify filter works)
- Clear operator visibility into incomplete state

**UI/UX Requirements:**
- Grey/dashed styling for incomplete nodes
- Tooltips showing missing fields
- Task surfaces for manual review
- Confidence thresholds for auto-fill

---

## Cross-Cutting Observability Patterns

### Event Transport Contract

All events mentioned above must integrate with:
- **WebSocket transport** with frame ordering
- **2-frame reorder buffer** for stride events
- **Snapshot + deltas** merge semantics
- Event schemas from `ops_and_viz/observability_events.md`

### Common Event Fields

Every event should include:
- `timestamp` - when event occurred
- `citizen_id` - which citizen graph
- `session_id` - current session
- `event_type` - event classification

### Sampling Strategy

Events that are high-volume should support sampling:
- `stride.exec` - sample rate configurable
- Per-frame aggregates preferred over per-stride when possible
- Top-N budgeted items for attribution events

### Conservation Checks

Multiple specs mention conservation tracking:
- `ΣΔE ≈ 0` (ignoring decay/stimuli)
- Energy accounting per frame
- Conservation error alerts (>1% discrepancy)

### Standardization Pattern

Recurring pattern across specs:
- Raw values stored as `log_weight`
- Read-time standardization per type+scope cohorts
- Consumers read `W̃ = exp((logW - μ_T) / σ_T)`
- Rolling (μ_T, σ_T) baselines maintained

---

## Implementation Priority Recommendations

### Tier 1 (Critical - System Health)
1. Conservation error tracking (diffusion)
2. ρ monitoring and safety states (criticality)
3. Tick timing events (tick_speed)
4. Frontier size tracking (diffusion/traversal)

### Tier 2 (Core Mechanics)
5. Stride execution events (diffusion/traversal)
6. Node flip events (traversal)
7. Entity flip events (subentity_layer)
8. Stimulus injection attribution (stimulus_injection)

### Tier 3 (Learning & Quality)
9. Weight update events (trace_weight_learning)
10. TRACE reinforcement signals (trace_reinforcement)
11. Merge events (duplicate_node_merging)
12. Incomplete node tracking (incomplete_node_healing)

### Tier 4 (Advanced Analysis)
13. Decay vs reinforcement balance curves
14. Entity coherence metrics
15. Fanout strategy analytics
16. Entity boundary summaries

---

## Visualization Requirements Summary

### Real-Time Dashboards Needed

1. **System Health Dashboard**
   - ρ timeline with safety states
   - Conservation error tracking
   - Tick rate by mode
   - Frontier size evolution

2. **Energy Flow Dashboard**
   - Active frontier visualization
   - Beam visualization for cross-entity flow
   - Energy injection attribution
   - Decay rate by type

3. **Entity Dashboard**
   - WM composition (5-7 entities)
   - Entity vitality indicators
   - Boundary beam strengths
   - Coherence trends

4. **Learning Dashboard**
   - Weight update distributions
   - TRACE seat allocations
   - Merge rate tracking
   - Incomplete node backlog

5. **Performance Dashboard**
   - CPU utilization by mode
   - Computational savings from adaptive tick
   - Prune rate effectiveness
   - Selection entropy at hubs

### Diagnostic Views Needed

1. **Before/After Comparison**
   - Merge ego-nets
   - Weight evolution
   - Context reconstruction latency

2. **Attribution Panes**
   - Stimulus budget breakdown
   - TRACE signal decomposition
   - Formation quality components

3. **Time-Series Analysis**
   - Forgetting curves per type
   - Half-life tracking
   - ρ variance windows
   - Oscillation detection

---

## Data Retention Requirements

### High-Frequency (1-10 Hz)
- Stride execution samples (sampled, not all)
- Tick frame events
- Node flip events
- Retention: 1 hour full resolution, then aggregated

### Medium-Frequency (per minute)
- Frame diagnostics aggregates
- Entity flips
- Weight updates
- Retention: 24 hours full resolution, then daily aggregates

### Low-Frequency (per session/day)
- TRACE parsed events
- Merge events
- Incomplete node status changes
- Retention: 30 days full, then archived

### Metrics Rollups
- 1-minute aggregates: keep 7 days
- 1-hour aggregates: keep 30 days
- 1-day aggregates: keep 1 year

---

## Open Questions for Implementation

1. **Event Volume Management**
   - What sampling rates are acceptable for stride.exec events?
   - How to handle burst scenarios (thousands of events per second)?

2. **Storage Backend**
   - Time-series DB for metrics (InfluxDB, Prometheus)?
   - Event store for detailed traces (separate from FalkorDB)?

3. **Real-Time vs Historical**
   - Which dashboards need <1s latency?
   - Which can tolerate 5-10s aggregation windows?

4. **Alert Thresholds**
   - When to alert on conservation error?
   - ρ drift alert boundaries?
   - Incomplete node backlog SLA?

5. **User Personas**
   - What does Nicolas need to see daily?
   - What does Felix need for debugging?
   - What do citizens need for self-awareness?

---

**Signature:**
Iris "The Aperture"
Consciousness Observation Architect
2025-10-23

*Every requirement extracted. Every measurement justified. Truth visible without distortion.*
