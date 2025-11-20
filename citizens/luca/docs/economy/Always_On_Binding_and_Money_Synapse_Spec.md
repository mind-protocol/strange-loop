# Always-On Binding & Money Synapse Rail Specification

**Version:** 0.1 Draft  
**Status:** Draft – pending architecture review  
**Authors:** Luca "Vellumhand", Atlas, Ada "Bridgekeeper"

---

## 1. Purpose & Scope

- Make wallet binding mandatory for every identity that contacts a Mind Protocol rail.
- Auto-settle every ASK without interactive prompts while keeping the wallet owner in control.
- Extend the money synapse mechanic so investors and citizens can see and farm payout links (“wire to printers” USP).
- Define adapter behavior, core services, data contracts, telemetry, and acceptance criteria for launch.

### In Scope
- Identity observation for Telegram, X, email relays, and the Mind UI.
- Wallet provisioning, claim, migration, delegate approvals, and enforcement when revoked.
- Per-message pricing, micro-batched settlement, and receipt anchoring.
- Money synapse weight evolution, relay payouts, and associated events.
- UX copy surfaced in adapters and dashboards.

### Out of Scope
- Visual implementation of dashboard cards, tables, or graphs.
- Fiat accounting, tax policy, and legal review.
- Alternative L1 blockchains or manual custody flows beyond passkey + custodial fallback.

---

## 2. Objectives & Non-Negotiables

1. **Zero unbound mode:** adapters must refuse to forward messages that lack an active delegate approval to the settlement program.
2. **Instant settlement:** every ASK is priced, charged, and proved before any downstream consciousness processing.
3. **User sovereignty:** when passkeys are available, the provisioned wallet is fully user-owned; custodial wallets remain claimable at any time.
4. **Physics over knobs:** abuse prevention relies on dynamic pricing, refractory surcharges, null routing, and Hebbian decay – no arbitrary caps.
5. **Receipts-first USP:** investors can trace how their wires route value whenever a KOL, org, or lane earns.

---

## 3. System Overview

```
identity seen → wallet provisioned/claimed → delegate granted → ASK priced → micro-batch settlement → money synapse weight updated → relay payouts distributed → receipts emitted
```

- Each adapter performs a binding check before forwarding payloads downstream.
- Provisioning service chooses passkey (preferred) or custodial wallet.
- Delegate service calls SPL `ApproveChecked` with unlimited allowance to the Settlement Program.
- Settlement queue batches `TransferChecked` instructions every 250–500 milliseconds.
- Money synapse engine updates link weights, records receipts, and triggers relay payouts.

---

## 4. Component Responsibilities

| Component | Responsibilities |
| --- | --- |
| **Identity Adapter (TG/X/email/UI)** | Detect first contact, call provisioning API, enforce delegate presence, block revoked wallets, surface UX copy. |
| **Wallet Provisioner** | Attempt WebAuthn passkey creation; if absent, mint custodial wallet, register claim token, return wallet id and type. |
| **Delegation Service** | Submit on-chain `ApproveChecked` to grant unlimited $MIND allowance to Settlement Program; maintain audit trail of approvals. |
| **Settlement Program** | Hold delegate authority, execute micro-batched `TransferChecked`, anchor receipts, expose settlement health metrics. |
| **Pricing Engine** | Compute ε-cost per ASK using surge pricing, refractory surcharge, and target-specific base rate. |
| **Money Synapse Engine** | Maintain weights, apply decay, sparsity, and rank-normalized updates after each ASK and receipt. |
| **Relay Payout Router** | Apply KOL/org relay share policies, normalize payouts over upstream wires, emit `money_synapse.receive`. |
| **Telemetry Pipeline** | Emit L4 events, surface binding state, settlement backlog, relay receipts, and null-route actions. |

---

## 5. Identity & Wallet Lifecycle

### 5.1 Auto Provisioning

- Trigger: adapter observes identity with no binding record.
- Flow:
  1. Adapter passes `handle`, `channel`, and optional `passkey_capable` flag to provisioning API.
  2. Provisioner attempts WebAuthn registration; on success returns `wallet`, `custody = "passkey"`.
  3. If passkey not possible, mint custodial wallet seeded in rail keyring; generate `claim_token` and mark `custody = "custodial"`.
  4. Emit `identity.auto_provisioned@1.0 { handle, channel, wallet, custody }`.
- Provisioner returns delegate-ready wallet id within 200 ms budget.

### 5.2 Delegate Grant & Enforcement

- Delegation service immediately submits SPL Token-2022 `ApproveChecked` with `amount = u64::MAX` for the $MIND mint and delegate = Settlement Program id.
- On success emit `settlement_authority.granted@1.0 { wallet, delegate, custody }`.
- Adapters cache delegate status; they must re-check on cold start or after revocation.
- If on-chain revocation detected (via `DelegateChanged` event or failed settlement attempt), adapters stop forwarding and reply with “Re-enable rail to speak”.

### 5.3 Claim & Migration

- Custodial wallets remain locked until user visits UI and completes passkey claim.
- Claim flow:
  1. User authenticates via passkey; claim service moves assets to new passkey wallet or upgrades custody.
  2. Emit `wallet.claimed@1.0 { handle, wallet, custody: "passkey" }`.
- Migration flow allows redirection to external wallet while maintaining binding:
  - Submit move request, rotate delegate to new wallet, settle outstanding balance.
  - Emit `wallet.migrate@1.0 { from_wallet, to_wallet, custody_to }`.

---

## 6. Settlement Flow

1. Adapter submits ASK payload containing `identity`, `target`, `body`, `context`.
2. Pricing engine computes `ask_price` = base rate × surge multiplier × refractory multiplier.
3. Settlement queue records ledger entry and appends to current micro-batch bucket.
4. Micro-batcher flushes every 250–500 ms (configurable) or when bucket exceeds 32 transfers:
   - Compose Solana transaction with batched `TransferChecked`.
   - Submit to cluster with retry and backoff.
   - On confirmation emit `ask.proved@1.0 { ask_id, wallet, amount_mind, tx_sig }`.
5. Downstream consciousness processing continues only after settlement success (or soft-fail via null-route decision).

Failure handling:
- If transaction fails due to revoked delegate, mark binding invalid and notify adapters.
- If insufficient balance, apply surge penalty, optionally trigger `wallet.depleted` event, and null-route message.

---

## 7. Pricing & Abuse Controls

- **Surge pricing:** multiplier grows with short-term ASK velocity from wallet to target; decays exponentially when activity falls.
- **Refractory surcharge:** additive percentage applied when consecutive messages arrive within two seconds; decays linearly.
- **Base rate catalog:** each target (citizen, org, lane) publishes base ε price; adapters fetch via cached registry.
- **Null-route:** citizens/orgs register offenders; rail still settles (proving spend) but downstream workloads ignore payload.
- **Hebbian decay:** money synapse weights shrink when ASK cadence drops or valence is negative, ensuring spam does not retain payout share.

---

## 8. Money Synapse Learning Model

- Each wallet→target link stores `log_weight`, `wire_weight`, `half_life_days`, `last_ask_ts`, `basis`, `sell_pct_max`, `relay_share_pct`.
- After each ASK:
  - Apply decay: `log_weight *= decay_factor(Δt, half_life)`.
  - Compute rank-normalized signals for spend amount, embedding similarity, valence, and outcome KPI.
  - Update: `log_weight += η × Σ(a_i × signal_i)` (single log-weight update from subentity membership spec).
  - Clamp per-update delta to whiplash limits and apply sparsity pruning to weakest wires.
- `wire_weight = exp(log_weight)` for payout normalization.
- Relay payouts:
  - Target declares `relay_share_pct` (≤ `max_relay_pct` default 0.2) and `max_hops` (default 1).
  - When target receives payout M, router allocates `M × relay_share_pct` across upstream wires proportional to `wire_weight`.
  - Each resulting transfer emits `money_synapse.receive@1.0 { basis, from_wallet, to_wallet, amount_mind, tx_ref }`.

---

## 9. Emergent L3 Subentities

- Significant co-engagement clusters form `Network_Cluster` nodes with `MEMBER_OF` links learned via same log-weight rule.
- When coherence threshold reached, emit `cluster.promoted_to_org@1.0` and optionally create `Company` node.
- Humans reaching activation threshold trigger `human.activated@1.0 { handle, target }`, signalling weight increase and potential dashboard surfacing.

---

## 10. Adapter Requirements

| Adapter | Mandatory Behaviors |
| --- | --- |
| **Telegram** | Resolve handles to canonical id, call provisioning before first relay, insert UX copy on success, reject message when revoked. |
| **X (Twitter)** | Use webhook/mention stream, throttle provisioning retries, enforce binding before delivering mention. |
| **Email** | Bind on first inbound, include claim instructions in auto-reply header, drop mail on revocation. |
| **Mind UI** | Require authenticated session; binding occurs during login; show claim banner until passkey created. |

Adapters must log binding decisions, settlement ids, and null-routes for audit.

---

## 11. Data Contracts & Events (L4)

| Event | Required Fields |
| --- | --- |
| `identity.auto_provisioned@1.0` | `handle`, `channel`, `wallet`, `custody`, `provisioning_latency_ms` |
| `settlement_authority.granted@1.0` | `wallet`, `delegate`, `custody`, `tx_sig`, `expires_at` |
| `wallet.claimed@1.0` | `handle`, `wallet`, `previous_custody`, `new_custody` |
| `wallet.migrate@1.0` | `from_wallet`, `to_wallet`, `delegate_rebound_ts`, `custody_to` |
| `ask.opened@1.0` | `ask_id`, `wallet`, `target`, `amount_mind`, `surge_multiplier`, `refractory_multiplier` |
| `ask.proved@1.0` | `ask_id`, `wallet`, `target`, `amount_mind`, `tx_sig`, `batch_id` |
| `money_synapse.updated@1.0` | `wallet`, `target`, `log_weight_before`, `log_weight_after`, `signals`, `half_life_days`, `sparsity_trimmed` |
| `relay.policy.updated@1.0` | `wallet`, `relay_share_pct`, `max_hops`, `sell_pct_max` |
| `money_synapse.receive@1.0` | `wallet`, `from_wallet`, `basis`, `amount_mind`, `tx_ref`, `relay_path` |
| `human.activated@1.0` | `handle`, `target`, `activation_score`, `wire_weight` |
| `binding.revoked@1.0` | `wallet`, `reason`, `detected_at`, `adapter_action` |

All events adhere to L4 schema rules: include `description`, `observed_at`, `producer`, and `confidence` metadata.

---

## 12. UX Copy

- **Initial binding (DM/tweet/email reply):** “Your identity is now bound to a $MIND rail wallet. Every message auto-settles; receipts are public. Claim anytime to withdraw or migrate.”
- **Claim banner:** “You have a rail wallet with **{balance} $MIND** and **{wire_count} wires**. Claim with passkey or migrate to your wallet.”
- **Revocation warning:** “Revoking disables your voice on the rail. Re-enable to speak again.”
- **Relay settings (KOL dashboard):** “Set the share you relay to upstream wires when you profit. Default 10%, capped at 20%.”

Adapters must cache localized variants but preserve meaning.

---

## 13. Observability & Telemetry

- Metrics: binding success rate, delegate approval latency, settlement batch size, backlog depth, null-route count, relay payout volume.
- Alerts:
  - Delegate failure rate > 0.5% over 5 minutes.
  - Settlement backlog older than 2 seconds.
  - Money synapse update errors or sparsity pruning > configured cap.
- Dashboards include profit graph (wallet → target → downstream) and receipts feed derived from events above.

---

## 14. Security Considerations

- Custodial wallets stored in rail keyring isolated from app credentials; claim tokens hashed with per-handle salt.
- Delegate program id restricted; only Settlement Program may operate with unlimited approval.
- Revocation triggers confirm removal of delegate and flush unsettled queue.
- Passkey flows follow WebAuthn best practices; no private keys transmitted to backend.

---

## 15. Rollout Plan

1. **Shadow Mode:** adapters bind quietly while still accepting legacy flow; monitor metrics.
2. **Enforce Delegate:** flip feature flag to block unbound messages after delegate approved.
3. **Enable Relay Payouts:** start with opt-in KOL set; verify share caps and receipts.
4. **Full Launch:** announce USP, unlock dashboard sections, route investor demo traffic.

Rollback simply toggles enforcement flags while keeping wallet state intact.

---

## 16. Verification & Acceptance

- Run end-to-end script that simulates new Telegram handle, ensures `identity.auto_provisioned` and `settlement_authority.granted` within 500 ms, verifies first ASK settles with receipt.
- Revoke delegate and confirm adapters reject subsequent messages; reinstating delegate restores flow.
- Replay surge pricing scenarios to ensure cost growth aligns with configuration.
- Trigger relay payout from org to KOL and assert upstream wallet receives proportional amount with `money_synapse.receive`.
- Verify custodial claim migrates funds and reissues delegate without settlement gaps.

---

## 17. Open Questions

- Should surge pricing parameters vary per channel (e.g., email vs DM) or remain target-specific only?
- Do we expose real-time relay earnings in public feeds or restrict to authenticated dashboards?
- What custodial wallet provider SLAs do we require for claim tokens?
- How aggressively should null-route statuses decay to re-enable previously abusive wallets?

---

## 18. Dependencies

- Settlement Program must support SPL Token-2022 delegate flows.
- Passkey service requires platform WebAuthn libraries in adapters and dashboard.
- Pricing engine needs access to recent ASK telemetry and target configs.

---

## 19. Next Steps

1. Atlas & Victor validate delegate enforcement in staging rail.
2. Iris integrates UX copy and claim banner in dashboard.
3. Felix wires money synapse increment logic to L3 evidence stream.
4. Ada schedules investor demo once verification artifacts recorded.

