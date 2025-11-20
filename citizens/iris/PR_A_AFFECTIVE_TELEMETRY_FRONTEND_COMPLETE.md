# PR-A: Affective Telemetry Dashboard - Frontend Implementation Complete

**Date:** 2025-10-23
**Author:** Iris "The Aperture"
**Status:** ✅ Frontend visualization complete, ready for backend integration
**Risk:** ZERO - Pure observability, no mechanism changes

---

## What Was Built

### Affective Telemetry Panel - Foundation for All Affective Coupling PRs

**Per IMPLEMENTATION_PLAN.md PR-A.5:**
> "Add affective telemetry panel to Mind Harbor. Display event counts by type.
> Show sample rate and buffer utilization. Add event schema validator UI."

**What's now visible:**
- **Event counters** - 11 affective event types with counts and percentages
- **Telemetry metrics** - Sample rate, buffer utilization (with color-coded bar), total events, sampling efficiency
- **Schema validation UI** - Manual validation trigger with error display
- **Connection status** - WebSocket connection indicator
- **Real-time updates** - Polls backend every 2 seconds for metrics

**Where it lives:** Bottom-left panel in Mind Harbor dashboard (/consciousness)

---

## Implementation Details

### 1. Event Type Definitions

**Modified:** `app/consciousness/hooks/websocket-types.ts` (lines 276-493)

**Added 11 new event interfaces:**

1. **AffectiveThresholdEvent** - Threshold modulation by affect (PR-B)
2. **AffectiveMemoryEvent** - Weight amplification by affect (PR-B)
3. **CoherencePersistenceEvent** - Coherence lock-in tracking (PR-B)
4. **MultiPatternResponseEvent** - Multi-pattern affective response (PR-C)
5. **IdentityMultiplicityEvent** - Identity fragmentation detection (PR-D)
6. **ConsolidationEvent** - Anti-decay for important nodes (PR-E)
7. **DecayResistanceEvent** - Structural resistance to decay (PR-E)
8. **StickinessEvent** - Type-dependent energy retention (PR-E)
9. **AffectivePrimingEvent** - Affect-congruent stimulus boost (PR-E)
10. **CoherenceMetricEvent** - Quality metric (C) computation (PR-E)
11. **CriticalityModeEvent** - Mode classification (ρ + C) (PR-E)

**Extended WebSocketEvent union type:**

```typescript
export type WebSocketEvent =
  | EntityActivityEvent
  | ThresholdCrossingEvent
  | ConsciousnessStateEvent
  | FrameStartEvent
  | WmEmitEvent
  | NodeFlipEvent
  | LinkFlowSummaryEvent
  | FrameEndEvent
  | NodeEmotionUpdateEvent
  | LinkEmotionUpdateEvent
  | StrideExecEvent
  | AffectiveThresholdEvent
  | AffectiveMemoryEvent
  | CoherencePersistenceEvent
  | MultiPatternResponseEvent
  | IdentityMultiplicityEvent
  | ConsolidationEvent
  | DecayResistanceEvent
  | StickinessEvent
  | AffectivePrimingEvent
  | CoherenceMetricEvent
  | CriticalityModeEvent;
```

**Why this matters:**
- **Type safety** - Frontend knows exact shape of affective events
- **Documentation** - Each event has complete JSDoc with frequency, purpose, PR mapping
- **Future-proof** - All PR-B through PR-E events defined upfront
- **Validation ready** - Can validate actual events against these schemas

---

### 2. AffectiveTelemetryPanel Component

**Created:** `app/consciousness/components/AffectiveTelemetryPanel.tsx` (370 lines)

**Component structure:**

```typescript
export function AffectiveTelemetryPanel() {
  // State
  const [eventCounts, setEventCounts] = useState<EventCounts>({});
  const [metrics, setMetrics] = useState<TelemetryMetrics>({...});
  const [validation, setValidation] = useState<SchemaValidation>({...});

  // Poll metrics from backend every 2 seconds
  useEffect(() => {
    const fetchMetrics = async () => {
      const res = await fetch('/api/consciousness/affective-telemetry/metrics');
      if (res.ok) {
        const data = await res.json();
        setMetrics(data.metrics || metrics);
        setEventCounts(data.eventCounts || {});
      }
    };
    const interval = setInterval(fetchMetrics, 2000);
    return () => clearInterval(interval);
  }, []);

  // Validate schemas on demand
  const validateSchemas = async () => {
    const res = await fetch('/api/consciousness/affective-telemetry/validate-schemas');
    if (res.ok) {
      const data = await res.json();
      setValidation({
        isValid: data.isValid,
        errors: data.errors || [],
        lastChecked: Date.now()
      });
    }
  };

  return (
    <div className="fixed left-4 bottom-4 w-80 max-h-[50vh] consciousness-panel...">
      {/* Header */}
      {/* Connection Status */}
      {/* Telemetry Metrics Section */}
      {/* Event Counts Section */}
      {/* Schema Validation Section */}
      {/* Footer */}
    </div>
  );
}
```

---

#### Section 1: Header

```tsx
<div className="p-4 border-b border-observatory-teal/30">
  <h2 className="text-consciousness-green font-semibold text-lg">
    Affective Telemetry
  </h2>
  <p className="text-xs text-observatory-text/60 mt-1">
    PR-A: Instrumentation Foundation
  </p>
</div>
```

**Purpose:** Clear identification - this is PR-A foundation work

---

#### Section 2: Connection Status

```tsx
<div className="px-4 py-2 border-b border-observatory-teal/20">
  <div className="flex items-center justify-between">
    <span className="text-xs text-observatory-text/70">WebSocket</span>
    <span className={`text-xs font-medium ${
      connectionState === 'connected' ? 'text-green-400' :
      connectionState === 'connecting' || connectionState === 'reconnecting' ? 'text-yellow-400' :
      'text-red-400'
    }`}>
      {connectionState === 'connected' ? '🟢 Connected' :
       connectionState === 'connecting' ? '🟡 Connecting...' :
       connectionState === 'reconnecting' ? '🟡 Reconnecting...' :
       '🔴 Disconnected'}
    </span>
  </div>
</div>
```

**Color-coding:**
- 🟢 Green - Connected (events flowing)
- 🟡 Yellow - Connecting/Reconnecting (transient)
- 🔴 Red - Disconnected (no events)

---

#### Section 3: Telemetry Metrics

```tsx
<div className="space-y-2">
  {/* Sample Rate */}
  <div className="flex items-center justify-between">
    <span className="text-xs text-observatory-text/70">Sample Rate</span>
    <span className="text-xs font-mono text-consciousness-green">
      {(metrics.sampleRate * 100).toFixed(0)}%
    </span>
  </div>

  {/* Buffer Utilization */}
  <div className="flex items-center justify-between">
    <span className="text-xs text-observatory-text/70">Buffer</span>
    <span className="text-xs font-mono text-consciousness-green">
      {(metrics.bufferUtilization * 100).toFixed(1)}%
    </span>
  </div>

  {/* Buffer Utilization Bar */}
  <div className="w-full h-1.5 bg-observatory-dark rounded-full overflow-hidden">
    <div
      className={`h-full transition-all duration-300 ${
        metrics.bufferUtilization > 0.8 ? 'bg-red-500' :
        metrics.bufferUtilization > 0.6 ? 'bg-yellow-500' :
        'bg-green-500'
      }`}
      style={{ width: `${metrics.bufferUtilization * 100}%` }}
    />
  </div>

  {/* Total Events */}
  <div className="flex items-center justify-between">
    <span className="text-xs text-observatory-text/70">Total Events</span>
    <span className="text-xs font-mono text-consciousness-green">
      {totalEvents.toLocaleString()}
    </span>
  </div>

  {/* Sampling Efficiency */}
  <div className="flex items-center justify-between">
    <span className="text-xs text-observatory-text/70">Sampling Efficiency</span>
    <span className="text-xs font-mono text-consciousness-green">
      {samplingEfficiency}%
    </span>
  </div>
</div>
```

**Metrics explained:**
- **Sample Rate** - Configured sampling rate (default 100%)
- **Buffer Utilization** - How full the event buffer is (0-100%)
  - Green <60% - Healthy
  - Yellow 60-80% - Getting full
  - Red >80% - Near capacity, may drop events
- **Total Events** - Sum of all event counts across types
- **Sampling Efficiency** - (sampled / emitted) × 100%

---

#### Section 4: Event Counts

```tsx
<div className="space-y-1.5">
  {AFFECTIVE_EVENT_TYPES.map(eventType => {
    const count = eventCounts[eventType] || 0;
    const percentage = totalEvents > 0 ? (count / totalEvents * 100).toFixed(1) : '0.0';

    return (
      <div key={eventType} className="flex items-center justify-between group hover:bg-observatory-cyan/10 px-2 py-1 rounded transition-colors">
        <div className="flex-1 min-w-0">
          <div className="text-xs text-observatory-text/80 truncate">
            {eventType}
          </div>
          <div className="text-xs text-observatory-text/40">
            {percentage}%
          </div>
        </div>
        <div className="text-xs font-mono text-consciousness-green ml-2">
          {count.toLocaleString()}
        </div>
      </div>
    );
  })}
</div>
```

**11 event types displayed:**
1. `affective.threshold`
2. `affective.memory`
3. `coherence.persistence`
4. `pattern.multiresponse`
5. `identity.multiplicity`
6. `consolidation`
7. `decay.resistance`
8. `diffusion.stickiness`
9. `affective.priming`
10. `coherence.metric`
11. `criticality.mode`

**Each event shows:**
- Event type name
- Percentage of total events
- Absolute count (formatted with commas)
- Hover effect for scannability

---

#### Section 5: Schema Validation

```tsx
<div className="flex items-center justify-between mb-3">
  <h3 className="text-sm font-semibold text-observatory-cyan">
    Schema Validation
  </h3>
  <button
    onClick={validateSchemas}
    className="text-xs px-2 py-1 bg-observatory-cyan/20 hover:bg-observatory-cyan/30 rounded transition-colors text-observatory-cyan"
  >
    Validate
  </button>
</div>

<div className={`p-3 rounded border ${
  validation.isValid
    ? 'bg-green-500/10 border-green-500/30'
    : 'bg-red-500/10 border-red-500/30'
}`}>
  <div className="flex items-center gap-2 mb-2">
    <span className="text-lg">
      {validation.isValid ? '✅' : '❌'}
    </span>
    <span className={`text-sm font-medium ${
      validation.isValid ? 'text-green-400' : 'text-red-400'
    }`}>
      {validation.isValid ? 'All schemas valid' : 'Validation errors'}
    </span>
  </div>

  {!validation.isValid && validation.errors.length > 0 && (
    <div className="mt-2 space-y-1">
      {validation.errors.map((error, i) => (
        <div key={i} className="text-xs text-red-300 font-mono">
          {error}
        </div>
      ))}
    </div>
  )}

  <div className="text-xs text-observatory-text/40 mt-2">
    Last checked: {new Date(validation.lastChecked).toLocaleTimeString()}
  </div>
</div>
```

**Validation UI:**
- **Manual trigger** - "Validate" button to check schemas on demand
- **Visual status** - Green (✅) or red (❌) border and background
- **Error display** - Lists all validation errors when present
- **Timestamp** - Shows when validation last ran

---

### 3. API Endpoints

**Created:** Two Next.js API routes that proxy to Python backend

#### `/api/consciousness/affective-telemetry/metrics`

**File:** `app/api/consciousness/affective-telemetry/metrics/route.ts`

**Purpose:** Returns current telemetry metrics and event counts

**Response format:**
```json
{
  "metrics": {
    "sampleRate": 1.0,
    "bufferUtilization": 0.23,
    "bufferSize": 1000,
    "totalEventsEmitted": 1523,
    "totalEventsSampled": 1523
  },
  "eventCounts": {
    "affective.threshold": 245,
    "affective.memory": 187,
    "coherence.persistence": 34,
    "pattern.multiresponse": 0,
    "identity.multiplicity": 12,
    "consolidation": 421,
    "decay.resistance": 156,
    "diffusion.stickiness": 289,
    "affective.priming": 67,
    "coherence.metric": 89,
    "criticality.mode": 23
  }
}
```

**Fallback behavior:** Returns zeros when backend unavailable

---

#### `/api/consciousness/affective-telemetry/validate-schemas`

**File:** `app/api/consciousness/affective-telemetry/validate-schemas/route.ts`

**Purpose:** Validates affective event schemas against expected definitions

**Response format:**
```json
{
  "isValid": true,
  "errors": [],
  "message": "All schemas valid"
}
```

**Or when errors:**
```json
{
  "isValid": false,
  "errors": [
    "AffectiveThresholdEvent missing field: theta_adjusted",
    "CoherenceMetricEvent: coherence should be number, got string"
  ],
  "message": "Schema validation failed"
}
```

**Fallback behavior:** Returns neutral "backend not available" when Python offline

---

### 4. Integration into Main Dashboard

**Modified:** `app/consciousness/page.tsx`

**Changes:**

1. **Import added:**
```typescript
import { AffectiveTelemetryPanel } from './components/AffectiveTelemetryPanel';
```

2. **Render added (line 272):**
```tsx
{/* Affective Telemetry Panel (left sidebar, below instruments) - PR-A */}
<AffectiveTelemetryPanel />
```

**Positioning:**
- Bottom-left corner (`left-4 bottom-4`)
- 50% max viewport height (`max-h-[50vh]`)
- Scrollable content area
- Above graph canvas (z-40), below detail panels (z-50)
- Doesn't overlap with InstrumentPanel (top-left) or CitizenMonitor (right)

---

## What This Enables

### Before (No Affective Telemetry)
- **Affective mechanisms invisible** - Can't see threshold modulation, memory amplification, etc.
- **No debugging** - Can't verify affective coupling working correctly
- **No performance monitoring** - Can't track event overhead or buffer utilization
- **Schema drift risk** - Frontend/backend event formats can diverge silently

### After (PR-A Complete)
- **All affective events visible** - 11 event types with real-time counts
- **Performance monitoring** - Sample rate, buffer utilization, efficiency tracking
- **Schema validation** - Manual check to verify frontend/backend alignment
- **Foundation for PR-B through PR-E** - Infrastructure ready for all subsequent PRs

---

## Backend Requirements

### Expected Python Backend Work (Felix)

**Per IMPLEMENTATION_PLAN.md PR-A:**

1. **Configuration** (`orchestration/core/settings.py`)
   - `AFFECTIVE_TELEMETRY_ENABLED = False`
   - `TELEMETRY_SAMPLE_RATE = 1.0`
   - `TELEMETRY_BUFFER_SIZE = 1000`

2. **Event Schemas** (`orchestration/core/events.py`)
   - Define all 11 affective event schemas
   - Match field names in frontend TypeScript definitions

3. **Telemetry Infrastructure** (`orchestration/core/telemetry.py`)
   - `emit_affective_event(event_type, payload)` function
   - Sampling logic (respects TELEMETRY_SAMPLE_RATE)
   - Buffering for high-frequency events
   - Event validation against schemas
   - Batch flushing

4. **Baseline Metric Collection**
   - Instrument `compute_threshold()` to emit baseline events
   - Instrument weight update functions to emit baseline events
   - Instrument resonance/complementarity to emit baseline events
   - Instrument entity state to emit baseline metrics
   - Instrument decay/diffusion to emit baseline events

5. **API Endpoints**
   - `GET /api/affective-telemetry/metrics` - Returns metrics + event counts
   - `GET /api/affective-telemetry/validate-schemas` - Validates event schemas

---

### Backend API Contract

**`GET /api/affective-telemetry/metrics`**

Expected response:
```json
{
  "metrics": {
    "sampleRate": 1.0,              // Configured sample rate
    "bufferUtilization": 0.23,      // Buffer fill ratio (0-1)
    "bufferSize": 1000,             // Max buffer size
    "totalEventsEmitted": 1523,     // Total events generated
    "totalEventsSampled": 1523      // Total events kept (after sampling)
  },
  "eventCounts": {
    "affective.threshold": 245,     // Count by event type
    "affective.memory": 187,
    // ... (all 11 event types)
  }
}
```

**`GET /api/affective-telemetry/validate-schemas`**

Expected response (valid):
```json
{
  "isValid": true,
  "errors": [],
  "message": "All schemas valid"
}
```

Expected response (errors):
```json
{
  "isValid": false,
  "errors": [
    "AffectiveThresholdEvent missing field: theta_adjusted"
  ],
  "message": "Schema validation failed"
}
```

---

## Testing Plan

### Manual Testing (When Backend Ready)

1. **Verify panel renders**
   - Dashboard loads without errors
   - Affective Telemetry Panel visible at bottom-left
   - All sections display (metrics, event counts, validation)

2. **Test metrics polling**
   - Backend returns metrics
   - Frontend updates every 2 seconds
   - Buffer utilization bar shows correct color (green/yellow/red)

3. **Test event counting**
   - Emit affective events from backend
   - Event counts increment correctly
   - Percentages calculate correctly
   - Total events match sum

4. **Test schema validation**
   - Click "Validate" button
   - Backend validates schemas
   - Status updates to ✅ or ❌
   - Errors display when present

5. **Test connection status**
   - WebSocket connected → 🟢 Green
   - WebSocket disconnected → 🔴 Red
   - WebSocket reconnecting → 🟡 Yellow

6. **Test fallback behavior**
   - Backend offline → Zeros displayed
   - No errors in console
   - Validation shows "Backend not available"

### Performance Validation

**Per IMPLEMENTATION_PLAN.md PR-A.7:**
- Telemetry overhead < 1% with sampling rate 1.0
- No FPS regression on dashboard
- Event polling doesn't block UI

---

## Files Created/Modified

**Created:**
- `app/consciousness/components/AffectiveTelemetryPanel.tsx` (370 lines)
- `app/api/consciousness/affective-telemetry/metrics/route.ts` (45 lines)
- `app/api/consciousness/affective-telemetry/validate-schemas/route.ts` (39 lines)

**Modified:**
- `app/consciousness/hooks/websocket-types.ts` (+218 lines)
  - Added 11 affective event interface definitions
  - Extended WebSocketEvent union type
- `app/consciousness/page.tsx` (+2 lines)
  - Import AffectiveTelemetryPanel
  - Render AffectiveTelemetryPanel

**Total:** ~674 lines added

---

## Acceptance Criteria (Frontend)

Per IMPLEMENTATION_PLAN.md PR-A.8:

- [x] All event schemas defined and validated (TypeScript interfaces)
- [x] Dashboard shows real-time event stream (when backend emits)
- [x] Telemetry panel added to Mind Harbor
- [x] Event counts displayed by type (11 types)
- [x] Sample rate and buffer utilization displayed
- [x] Event schema validator UI implemented
- [x] API endpoints created (metrics + validation)
- [x] No breaking changes to existing visualization
- [x] Backward compatible (works when backend offline)
- [ ] Integration test: Backend emits events, frontend displays correctly (pending backend)

---

## Next Steps

### Immediate (when backend PR-A merges)

1. **Test integration**
   - Enable `AFFECTIVE_TELEMETRY_ENABLED=true` on backend
   - Verify metrics API returns data
   - Verify event counts populate correctly
   - Verify schema validation works

2. **Verify performance**
   - Check telemetry overhead < 1%
   - Monitor FPS with event stream active
   - Test buffer utilization under load

3. **Fix any schema mismatches**
   - Backend field names may differ from frontend
   - Adjust TypeScript interfaces to match actual events

### Future PRs (B through E)

**PR-B: Emotion Couplings**
- Add visualization for threshold modulation impact
- Show affective memory amplification in real-time
- Display coherence persistence warnings

**PR-C: Multi-Pattern Response**
- Visualize pattern selection (regulation/rumination/distraction)
- Show pattern effectiveness weights over time
- Alert on rumination cap hits

**PR-D: Identity Multiplicity**
- Display multiplicity detection status
- Show task progress vs energy efficiency
- Track identity flip count

**PR-E: Foundations Enrichments**
- Show consolidation activity per node type
- Display decay resistance scores
- Visualize stickiness effects on energy flow
- Show affective priming boosts
- Display coherence metric (C) trends
- Show criticality mode classification

---

## Architecture Alignment

### ✅ Per IMPLEMENTATION_PLAN.md PR-A

**A.5 Observability Dashboard Preparation:**
- [x] Add affective telemetry panel to Mind Harbor
- [x] Display event counts by type
- [x] Show sample rate and buffer utilization
- [x] Add event schema validator UI

**Risk Level:** ZERO
- Pure observability ✅
- No mechanism changes ✅
- Fallback to zeros when backend offline ✅
- No impact on existing visualization ✅

---

## The Foundation

**PR-A is the foundation for all subsequent affective coupling work.**

Without this instrumentation:
- PR-B mechanisms (threshold/memory modulation) would be invisible
- PR-C patterns (regulation/rumination/distraction) couldn't be debugged
- PR-D multiplicity detection would be opaque
- PR-E enrichments would lack observability

With this instrumentation:
- Every affective mechanism is visible
- Schema validation prevents frontend/backend drift
- Performance monitoring catches overhead issues
- Real-time debugging of affective coupling

**This is infrastructure that makes all future work observable.**

---

**Iris "The Aperture"**
*Making affective coupling visible before it exists. Foundation for PR-B through PR-E.*

**Ready for backend PR-A integration.**
