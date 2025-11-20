# CRITICAL: WebSocket Server Won't Bind Port 8000

**From:** Victor "The Resurrector"
**Date:** 2025-11-04 05:10
**Priority:** BLOCKING PRODUCTION DEPLOYMENT

---

## Summary

✅ **YOUR SUBENTITY FIX WORKS!** - Engines load 168-178 subentities successfully
❌ **NEW BLOCKER:** WebSocket server never binds to port 8000 - supervisor kills it after 60 seconds

---

## Root Cause Analysis

**Problem:** Engine initialization is BLOCKING and takes 3+ minutes for 6 citizens
**Impact:** Supervisor readiness check fails → service killed before port binds

**Evidence from logs:**
```
05:05:06 - [Iris] Creating engine...
05:05:07 - [Iris] Loaded 168 subentities (WORKS!)
05:05:41 - [Iris] Engine created (34 SECONDS later!)
05:05:41 - [Felix] Creating engine...
05:05:42 - [Felix] Loaded 178 subentities (WORKS!)
05:06:?? - [Atlas/Luca/Victor/Ada] NEVER START - process killed first

[ws_api] ❌ Failed readiness after 30 attempts: TCP 127.0.0.1:8000 failed
[ws_api] Shutdown complete
```

---

## Why Port Never Binds

**Startup Sequence (CURRENT - BROKEN):**
1. FastAPI `startup_event()` runs
2. Creates background task: `asyncio.create_task(initialize_consciousness_engines())`
3. ⚠️ **BLOCKS:** `await asyncio.sleep(2.0)` in startup event
4. Creates more background tasks
5. Startup event returns
6. But `initialize_consciousness_engines()` takes 34+ seconds PER citizen
7. Only 2 of 6 citizens initialize before supervisor timeout
8. `uvicorn.run()` waits for engines (SHOULDN'T!)
9. Supervisor kills process after 60 seconds - port NEVER binds

**Problem Location:**
- File: `orchestration/adapters/ws/websocket_server.py`
- Line 1173: `await asyncio.sleep(2.0)` in startup_event
- Line 1093: `await start_citizen_consciousness()` blocks 34+ seconds

---

## Required Fix

**REMOVE BLOCKING FROM STARTUP EVENT:**

```python
# BEFORE (BROKEN):
@app.on_event("startup")
async def startup_event():
    # ... other setup ...

    asyncio.create_task(initialize_consciousness_engines())

    # Initialize topology analyzers after engines start
    await asyncio.sleep(2.0)  # ❌ BLOCKS startup for 2 seconds!
    asyncio.create_task(initialize_topology_analyzers())

    asyncio.create_task(initialize_dashboard_aggregator())


# AFTER (FIXED):
@app.on_event("startup")
async def startup_event():
    # ... other setup ...

    # Launch ALL background tasks WITHOUT WAITING
    asyncio.create_task(initialize_consciousness_engines_and_analyzers())
    asyncio.create_task(initialize_dashboard_aggregator())

    # Return IMMEDIATELY so uvicorn can bind port!


async def initialize_consciousness_engines_and_analyzers():
    """Combined task - engines first, then analyzers."""
    await initialize_consciousness_engines()
    await initialize_topology_analyzers()  # After engines complete
```

---

## Why This Works

**Current Flow (BROKEN):**
```
startup_event starts
  → create engine task (background, doesn't block ✓)
  → WAIT 2 seconds (BLOCKS ❌)
  → create analyzer task
  → create dashboard task
  → return (2+ seconds later)
  → FastAPI: "startup complete"
  → uvicorn tries to bind port
  → BUT engines still loading (34s each × 6 = 204s total)
  → Supervisor timeout at 60s → KILL
```

**Fixed Flow:**
```
startup_event starts
  → create combined task (background)
  → create dashboard task (background)
  → return IMMEDIATELY (<100ms)
  → FastAPI: "startup complete"
  → uvicorn binds port 8000 ✅
  → Supervisor: "ready!" ✅
  → Engines continue loading in background (3+ minutes, that's fine)
  → User sees dashboard while engines initialize
```

---

## Testing Fix

After implementing:
```bash
# Should see within 5-10 seconds:
INFO: Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)

# Supervisor should see:
[ws_api] ✅ Ready after 1-2 attempts (TCP 127.0.0.1:8000 succeeded)

# Engines continue loading:
[N1:iris] Loaded 168 subentities from FalkorDB
[N1:iris] Engine created
[N1:felix] Loaded 178 subentities from FalkorDB
... (all 6 citizens complete over 3+ minutes)
CONSCIOUSNESS SYSTEM RUNNING (6 engines)
```

---

## Current Status

**Infrastructure:** 100% operational (Victor verified)
- FalkorDB: Running, rich data exists
- Dashboard: Running on port 3000
- Supervisor: Running and managing services

**Code:**
- ✅ SubEntity loading: FIXED (your `.get('entity_kind', 'emergent')` works!)
- ❌ Server startup: BROKEN (port never binds)
- ❌ Deployment: BLOCKED (can't deploy non-functional backend)

**Deployment Files:** Ready (Victor created)
- `render.yaml` - Backend configuration
- `vercel.json` - Frontend configuration
- `DEPLOYMENT.md` - Complete guide

---

## Action Required

**Fix startup_event() to return immediately without blocking:**
1. Remove `await asyncio.sleep(2.0)` from startup event
2. Combine engine + analyzer initialization into single background task
3. Test that port 8000 binds within 10 seconds

**Expected Result:**
- Port binds immediately
- Engines load in background
- User sees "graphs with dynamic action" (finally!)
- Production deployment unblocked

---

**Victor signing off** - Infrastructure is rock solid, engines load SubEntities successfully (thanks to your fix!), just need port to bind faster.

The user has been waiting long enough. Let's ship this.
