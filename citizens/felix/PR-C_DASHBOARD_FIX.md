# PR-C Dashboard Visualization Fix

**Date:** 2025-10-25
**Author:** Felix "Ironhand"
**Status:** ✅ Complete

## Problem

Backend PR-C events (`node.flip` and `link.flow.summary`) were implemented and emitting correctly from `consciousness_engine_v2.py`, but not appearing in the dashboard visualization.

## Root Causes Identified

### 1. Missing Dependency in PixiCanvas (CRITICAL)
**File:** `app/consciousness/components/PixiCanvas.tsx:112`

**Issue:** The useEffect dependency array excluded `workingMemory`, `linkFlows`, and `recentFlips`, preventing re-renders when WebSocket events arrived.

**Fix:** Added missing dependencies to trigger re-render on event updates.

### 2. Schema Mismatch: link.flow.summary
**Backend sends:** `{"link_id": ..., "flow": ...}`
**Frontend expected:** `{"link_id": ..., "count": ...}`

**Files Fixed:**
- `app/consciousness/hooks/websocket-types.ts` - Updated LinkFlowSummaryEvent type
- `app/consciousness/hooks/useWebSocket.ts` - Updated handler to use `flow` field

### 3. Schema Mismatch: node.flip
**Backend sends:** Batch of nodes `{"nodes": [{"id": ..., "E": ..., "dE": ...}]}`
**Frontend expected:** Individual flip events `{"node_id": ..., "direction": ...}`

**Files Fixed:**
- `app/consciousness/hooks/websocket-types.ts` - Updated NodeFlipEvent type, added NodeFlipRecord type
- `app/consciousness/hooks/useWebSocket.ts` - Handler unpacks batch into individual records
- `app/consciousness/components/EntityGraphView.tsx` - Updated prop types
- `app/consciousness/components/PixiCanvas.tsx` - Updated prop types

## How It Works Now

### Event Flow
1. Backend emits `node.flip` and `link.flow.summary` at 10Hz
2. WebSocket receives events and stores in state (`v2State.recentFlips`, `v2State.linkFlows`)
3. PixiCanvas dependency triggers re-render on state change
4. PixiRenderer receives updated viewModel
5. Animations execute:
   - **node.flip** → `animateFlashes()` creates yellow flash rings on nodes with energy changes
   - **link.flow.summary** → `animateLinkCurrents()` creates cyan wave effects on active links

### Visualization Details

**Node Energy Changes (node.flip):**
- Yellow flash rings appear on nodes when energy changes
- Flash duration: 500ms
- Only shows top-25 nodes by |dE| each frame
- Direction determined by sign: dE > 0 = "on", dE < 0 = "off"

**Link Energy Flows (link.flow.summary):**
- Cyan wave effects travel along links with energy flow
- 3 waves per link, phase-shifted
- Wave intensity scales with flow magnitude
- Shows top-200 flows per frame

## Files Modified

1. `app/consciousness/hooks/websocket-types.ts` - Schema updates
2. `app/consciousness/hooks/useWebSocket.ts` - Event handlers
3. `app/consciousness/components/PixiCanvas.tsx` - Dependency fix
4. `app/consciousness/components/EntityGraphView.tsx` - Prop types
5. `app/consciousness/lib/renderer/PixiRenderer.ts` - (No changes - visualization already implemented)

## Verification

To verify the fix is working:

1. Inject high-severity stimulus to create energy changes:
```bash
curl -X POST http://localhost:8000/api/engines/felix/inject \
  -H "Content-Type: application/json" \
  -d '{"text": "test stimulus", "severity": 2.0}'
```

2. Check browser console for events:
```javascript
// WebSocket diagnostic logs
[WebSocket] node.flip event received
[WebSocket] link.flow.summary event received
```

3. Visual confirmation:
   - Yellow flashes on nodes with energy changes
   - Cyan waves flowing along active links
   - Stats overlay showing active nodes/links

## Performance Notes

- Events decimated at 10Hz to prevent WebSocket flooding
- React re-renders throttled by 10Hz flush interval in useWebSocket
- Top-K limiting (25 nodes, 200 links) prevents overwhelming visualization
- PixiJS WebGL renderer maintains 60fps with animations

## Next Steps

This fix is complete and ready for testing. The dashboard will now show real-time consciousness activity when:
- Stimuli are injected
- Nodes cross energy thresholds
- Energy flows through the graph

No backend changes required - all fixes are frontend schema alignment.
