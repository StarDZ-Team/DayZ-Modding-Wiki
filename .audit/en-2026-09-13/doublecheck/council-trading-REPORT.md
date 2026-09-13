# Independent Council: Trading Tutorial Safety

**Decision: accept revised.** Terra's central safety move is proportionate: keep the detailed UI, configuration, RPC, and inventory API material, but make the server refuse before any debit, spawn, quantity change, or deletion. A warning alone would not prevent the current handlers from destroying value, while replacing the whole tutorial or demanding a production transaction subsystem would exceed this audit.

The exact Terra handlers are not accepted unchanged. They remove all quantity and catalog checks even though the proposed prose says bounded request validation and price lookup remain demonstrated. The final blocks in `council-trading.json` retain those harmless server-side checks and then refuse before mutation.

## Evidence judgment

At BohemiaInteractive's official `DayZ-Script-Diff` commit `86974a0f5bd16b1ee3e334ad828133c93dca80a1` (Build 1.29.163709, Scripts Rev. 125372):

- [`inventory.c`](https://github.com/BohemiaInteractive/DayZ-Script-Diff/blob/86974a0f5bd16b1ee3e334ad828133c93dca80a1/scripts/3_game/systems/inventory/inventory.c#L870-L893) declares `EntityAI CreateInInventory(string type)`; its official comment says it returns the created entity or `null`, and the implementation has a `return null` path. Raw SHA-256: `BC9082828E69EF664C946B5EE86887B357E53517266AB4C0A94FA784B4534BF1`.
- [`game.c`](https://github.com/BohemiaInteractive/DayZ-Script-Diff/blob/86974a0f5bd16b1ee3e334ad828133c93dca80a1/scripts/3_game/global/game.c#L694-L702) declares `proto native Object CreateObjectEx( string type, vector pos, int iFlags, int iRotation = RF_DEFAULT );`. The declaration gives no transaction or compensation guarantee. Raw SHA-256: `C99E24587D8FD7DBA4BFFE7D86A9603307EDA745BE2F25798B69E347CCF5558C`.
- [`entityai.c`](https://github.com/BohemiaInteractive/DayZ-Script-Diff/blob/86974a0f5bd16b1ee3e334ad828133c93dca80a1/scripts/3_game/entities/entityai.c#L786-L810) implements `void DeleteSafe()` through immediate/deferred or player-juncture paths and exposes `IsSetForDeletion()`, but no transaction commit result. The same file declares `bool SetQuantity(..., bool clamp_to_stack_max = true)` at line 2247. Raw SHA-256: `7290A79E7298B6FDB9EBFC7A23D9CE7CCA7EF06C98F2DB8C7A883E24E8321479`.

These signatures justify rejecting the existing irreversible sequence and any repair that merely reports loss after it occurs. They do **not** prove compensation is impossible. A compensating design may be feasible, but correctness would depend on explicit state, cleanup/retry behavior, disconnect and restart handling, and runtime-tested engine semantics that are outside this documentation audit. The honest conclusion is narrower: this tutorial does not implement or prove such a protocol.

## Required revision to Terra

Use every exact old/new block in `council-trading.json`. The important differences from Terra's proposal are:

1. Keep the 1-10 bound and server catalog/sellability lookup in both handlers, then refuse.
2. Put a two-line teaching-only guard immediately above `RemoveCurrency`; it also scopes the adjacent `GiveCurrency` helper.
3. Replace Step 9 with refusal and no-mutation checks while retaining crafted-RPC validation cases.
4. Correct the remaining live-trading claims in Complete Code Reference, Best Practices, Theory vs Practice, What You Learned, and Common Mistakes.

This is still a small documentation repair: two handler substitutions, one code comment, and concise scope corrections. It preserves the tutorial rather than substituting a different feature.

## Prevention and warning limits

The refusal is prevention: all handler exits occur before `RemoveCurrency`, `GiveCurrency`, `SetQuantity`, `CreateInInventory`, `CreateObjectEx`, or `DeleteSafe` can mutate assets. The warning is only a copying boundary: it cannot make the unused helper code transaction-safe, prove deletion completion, or establish compensation correctness. Future live trading may use reservation, escrow, compensation, or durable recovery, but it must be separately designed and fault-tested; this council does not prescribe unsupported atomicity.

No English content, protected file, build, runtime, tooling, or commit was changed or claimed.
