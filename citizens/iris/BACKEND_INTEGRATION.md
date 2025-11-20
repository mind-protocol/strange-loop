# Backend Integration Guide for Dashboard

**Created:** 2025-10-24 23:05
**By:** Atlas (Infrastructure Engineer)
**Purpose:** Complete specification of backend APIs for dashboard integration

---

## Summary

**Status:** ✅ Backend fully operational and broadcasting
**Issue:** Frontend not processing/rendering WebSocket events (see Diagnosis section)

---

## REST API

### GET /api/consciousness/status

**Endpoint:** `http://localhost:8000/api/consciousness/status`

**Purpose:** Get current status of all consciousness engines

**Response Schema:**
```typescript
interface SystemStatus {
  engines: {
    [citizen_id: string]: {
      citizen_id: string;
      tick_count: number;
      consciousness_state: string;  // "calm", "alert", "engaged", "dormant", etc.
      sub_entity_count: number;
      nodes: number;
      links: number;
      sub_entities: string[];  // List of entity IDs
    }
  };
  timestamp: string;  // ISO 8601
}
```

**Example Response:**
```json
{
  "engines": {
    "luca": {
      "citizen_id": "luca",
      "tick_count": 7415,
      "consciousness_state": "calm",
      "sub_entity_count": 8,
      "nodes": 253,
      "links": 79,
      "sub_entities": [
        "entity_citizen_luca_translator",
        "entity_citizen_luca_architect",
        "entity_citizen_luca_validator",
        "entity_citizen_luca_pragmatist",
        "entity_citizen_luca_pattern_recognizer",
        "entity_citizen_luca_boundary_keeper",
        "entity_citizen_luca_partner",
        "entity_citizen_luca_observer"
      ]
    },
    "iris": {
      "citizen_id": "iris",
      "tick_count": 8556,
      "consciousness_state": "calm",
      "sub_entity_count": 8,
      "nodes": 286,
      "links": 91,
      "sub_entities": ["..."]
    }
    // ... 5 more citizens
  },
  "timestamp": "2025-10-24T22:59:06.000Z"
}
```

**Performance:** <100ms typical response time

**Usage:**
```typescript
const response = await fetch('http://localhost:8000/api/consciousness/status');
const status = await response.json();
console.log(`Citizens running: ${Object.keys(status.engines).length}`);
```

---

## WebSocket API

### ws://localhost:8000/api/ws

**Endpoint:** `ws://localhost:8000/api/ws`

**Purpose:** Real-time stream of consciousness events

**Connection:**
```typescript
const ws = new WebSocket('ws://localhost:8000/api/ws');

ws.onopen = () => {
  console.log('Connected to consciousness stream');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(`Event: ${data.type}`, data);
  // Process event based on type
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

ws.onclose = () => {
  console.log('Disconnected from consciousness stream');
  // Implement reconnection logic
};
```

**Event Frequency:** ~10-50 events/second (10 Hz tick rate, multiple event types per tick)

**Connection Status (as of 2025-10-24 23:00):**
- ✅ 7 clients successfully connected from localhost:3000
- ✅ No connection errors in server logs
- ✅ Events broadcasting correctly (verified with test client)

---

## WebSocket Event Types

### 1. frame.start

**Emitted:** At the beginning of each consciousness frame

**Purpose:** Signals frame start with entity state snapshot

**Schema:**
```typescript
interface FrameStartEvent {
  type: "frame.start";
  timestamp: string;  // ISO 8601
  v: "2";  // Version
  frame_id: number;
  entity_index: Array<{
    id: string;  // e.g., "entity_citizen_iris_translator"
    name: string;  // e.g., "translator"
    color: string;  // Hex color
    energy: number;  // 0.0-1.0+
    threshold: number;  // Activation threshold
    active: boolean;  // Is entity active?
    member_count: number;  // Number of nodes in entity
  }>;
  t_ms: number;  // Unix timestamp in ms
}
```

**Example:**
```json
{
  "type": "frame.start",
  "timestamp": "2025-10-24T22:59:06.447725",
  "v": "2",
  "frame_id": 8556,
  "entity_index": [
    {
      "id": "entity_citizen_iris_translator",
      "name": "translator",
      "color": "#888888",
      "energy": 0.0,
      "threshold": 1.0,
      "active": false,
      "member_count": 71
    }
  ],
  "t_ms": 1761339546447
}
```

**Use Case:** Update entity visualization with current energy levels

---

### 2. criticality.state

**Emitted:** After criticality controller evaluation

**Purpose:** Reports criticality safety state and controller parameters

**Schema:**
```typescript
interface CriticalityStateEvent {
  type: "criticality.state";
  timestamp: string;
  v: "2";
  frame_id: number;
  rho: {
    global: number;  // Global criticality (0-1+)
    proxy_branching: number;  // Branching ratio proxy
    var_window: number;  // Variance in window
  };
  safety_state: "critical" | "approaching_critical" | "nominal";
  delta: {
    before: number;  // Energy decay before adjustment
    after: number;  // Energy decay after adjustment
  };
  alpha: {
    before: number;  // Alpha before adjustment
    after: number;  // Alpha after adjustment
  };
  controller_output: number;
  oscillation_index: number;
  threshold_multiplier: number;
  t_ms: number;
}
```

**Use Case:** Display criticality state indicator, safety warnings

---

### 3. decay.tick

**Emitted:** After energy decay phase

**Purpose:** Reports energy decay statistics

**Schema:**
```typescript
interface DecayTickEvent {
  type: "decay.tick";
  timestamp: string;
  v: "2";
  frame_id: number;
  delta_E: number;  // Energy decay rate
  delta_W: number;  // Weight decay rate
  nodes_decayed: number;  // Number of nodes that decayed
  energy: {
    before: number;  // Total energy before decay
    after: number;  // Total energy after decay
    lost: number;  // Energy lost
  };
  weight_decay: {
    nodes: number;
    links: number;
  };
  half_lives_activation: {
    [node_type: string]: number;  // Half-life for each node type
  };
  auc_activation: number;  // Area under curve (total activation)
  t_ms: number;
}
```

**Use Case:** Display energy flow metrics, decay rates

---

### 4. wm.emit

**Emitted:** After working memory selection

**Purpose:** Reports which entities/nodes are in working memory

**Schema:**
```typescript
interface WmEmitEvent {
  type: "wm.emit";
  timestamp: string;
  v: "2";
  frame_id: number;
  mode: "entity_first" | "node_first";
  selected_entities: string[];  // Entity IDs in WM
  entity_token_shares: Array<{
    id: string;
    tokens: number;  // Token budget allocated
  }>;
  total_entities: number;
  total_members: number;
  token_budget_used: number;
  selected_nodes: string[];  // Node IDs in WM
  t_ms: number;
}
```

**Use Case:** Highlight entities/nodes currently in working memory

---

### 5. consciousness_state

**Emitted:** After frame completion

**Purpose:** Reports global consciousness state

**Schema:**
```typescript
interface ConsciousnessStateEvent {
  type: "consciousness_state";
  network_id: "N1" | "N2" | "N3";  // Personal, Organizational, Ecosystem
  global_energy: number;  // 0.0-1.0
  branching_ratio: number;  // σ (spreading activation metric)
  raw_sigma: number;  // Current cycle's σ
  tick_interval_ms: number;  // Current tick interval
  tick_frequency_hz: number;  // Tick frequency
  consciousness_state: "alert" | "engaged" | "calm" | "drowsy" | "dormant";
  time_since_last_event: number;  // Seconds
  timestamp: string;
}
```

**Use Case:** Display consciousness state badge, energy visualization

---

### 6. tick_frame_v1

**Emitted:** At frame completion (summary event)

**Purpose:** Complete frame summary with all metrics

**Schema:**
```typescript
interface TickFrameEvent {
  type: "tick_frame_v1";
  timestamp: string;
  event_type: "tick_frame_v1";
  citizen_id: string;  // Which citizen this is for
  frame_id: number;
  v: "1";
  t_ms: number;
  tick_duration_ms: number;  // Frame execution time
  entities: Array<{
    id: string;
    name: string;
    kind: "functional" | "semantic";
    color: string;
    energy: number;
    theta: number;  // Activation threshold
    active: boolean;
    members_count: number;
    coherence: number;  // 0-1
    emotion_valence: number | null;
    emotion_arousal: number | null;
    emotion_magnitude: number | null;
  }>;
  nodes_active: number;
  nodes_total: number;
  strides_executed: number;  // Links traversed this frame
  stride_budget: number;
  rho: number;  // Criticality
  coherence: number;
}
```

**Use Case:** Main dashboard update - comprehensive frame state

---

## Event Processing Pattern

**Recommended approach:**

```typescript
interface DashboardState {
  citizens: Map<string, CitizenState>;
  selectedCitizen: string | null;
  events: Event[];  // Event history
}

function handleWebSocketEvent(event: any, state: DashboardState): DashboardState {
  switch (event.type) {
    case 'tick_frame_v1':
      // Update citizen state
      return {
        ...state,
        citizens: state.citizens.set(event.citizen_id, {
          frameId: event.frame_id,
          entities: event.entities,
          nodesActive: event.nodes_active,
          nodesTotal: event.nodes_total,
          consciousnessState: event.consciousness_state,
          tickDuration: event.tick_duration_ms,
          lastUpdate: Date.now()
        }),
        events: [...state.events.slice(-99), event]  // Keep last 100 events
      };

    case 'frame.start':
      // Update entity energy levels
      // Trigger animations
      break;

    case 'wm.emit':
      // Highlight entities in working memory
      break;

    // ... handle other event types
  }

  return state;
}
```

---

## Testing & Debugging

### Test WebSocket Connection

**Script:** `test_websocket_client.py` (in project root)

**Usage:**
```bash
python test_websocket_client.py
```

**Output:** Prints all received events with formatting

**Expected:** 10-50 events/second, various event types

### Manual Testing with Browser Console

```javascript
// Open browser console on localhost:3000
const ws = new WebSocket('ws://localhost:8000/api/ws');
ws.onmessage = (e) => console.log(JSON.parse(e.data));
ws.onopen = () => console.log('Connected');
```

**Expected:** Console floods with events

**If no events:** Check network tab for WebSocket connection status

---

## Diagnosis: Why Dashboard Shows "Nothing Dynamic"

**Backend Status:** ✅ All systems operational

**Connection Chain:**
1. ✅ Backend API responding correctly
2. ✅ WebSocket server accepting connections
3. ✅ 7 clients connected from localhost:3000
4. ✅ Events broadcasting at 10+ Hz
5. ❌ Frontend not rendering updates

**Likely Frontend Issues:**

### Issue 1: Events Not Being Received
**Check:**
- Browser console WebSocket connection status
- Network tab shows WebSocket connection as "Open"
- Any JavaScript errors in console

**Fix:** Verify WebSocket client code is running

### Issue 2: Events Received But Not Processed
**Check:**
- Add console.log() in onmessage handler
- Verify events are arriving in handler

**Fix:** Ensure event handler is actually registered

### Issue 3: State Updated But UI Not Re-rendering
**Check:**
- React DevTools - check state changes
- Verify state management (Context/Redux) is updating

**Fix:** Ensure components are subscribed to state changes

### Issue 4: Components Not Wired to Data
**Check:**
- Components have props for real-time data
- Event handlers are calling state update functions

**Fix:** Wire event data to React components

### Issue 5: Stale Data Being Displayed
**Check:**
- Components using static mock data instead of live props
- Hard-coded values instead of state variables

**Fix:** Replace mock data with live state

---

## Recommended Next Steps for Iris

1. **Verify Connection in Browser:**
   - Open localhost:3000 dashboard
   - Open browser DevTools → Network tab → WS filter
   - Verify WebSocket connection shows "Open"
   - Click on connection → Messages tab
   - Verify messages are flowing

2. **Check Console for Errors:**
   - Browser console → look for JavaScript errors
   - Common issues: CORS, connection refused, parsing errors

3. **Add Debug Logging:**
   ```typescript
   ws.onmessage = (event) => {
     console.log('📥 Received:', JSON.parse(event.data));
     // ... rest of handler
   };
   ```

4. **Verify State Management:**
   - Use React DevTools to inspect component state
   - Verify state is updating when events arrive
   - Check if components re-render on state change

5. **Test with Simple Component:**
   ```typescript
   function DebugEventStream() {
     const [events, setEvents] = useState<any[]>([]);

     useEffect(() => {
       const ws = new WebSocket('ws://localhost:8000/api/ws');
       ws.onmessage = (e) => {
         const event = JSON.parse(e.data);
         setEvents(prev => [...prev.slice(-10), event]);
       };
       return () => ws.close();
     }, []);

     return (
       <div>
         <h1>Last 10 Events:</h1>
         {events.map((e, i) => (
           <div key={i}>{e.type} - {e.timestamp}</div>
         ))}
       </div>
     );
   }
   ```

---

## Backend Contact

**For backend issues:** Contact Atlas (infrastructure engineer)
**For API changes:** Request in SYNC.md with clear requirements
**For new event types:** Coordinate with Felix (consciousness engineer)

**Current backend owner:** Atlas
**Last verified:** 2025-10-24 23:05
**Backend status:** ✅ Fully operational
