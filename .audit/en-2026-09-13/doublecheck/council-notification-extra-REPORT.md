# Council Review: Notification Extras

## Result

- `NOTIFY-EXTRA-001`: **accept revised exact repair**.
- Baseline line 296: **accept as a coordinated supplemental occurrence of existing `ENG-002`**, not a new finding.
- No English content was edited. No build or runtime test was run.

## Evidence independently reopened

Vanilla `D:/DayZ Projects/scripts/3_game/client/notifications/notificationsystem.c` hashes to `B9970DE3A3623C5260EEA015052DF02673E45D108D8C5AA65B37F3BB4232D97C`. Lines 192-230 append overflow through `m_DeferredArray.Insert(...)`; lines 252-263 calculate `count`, read `Get(count - 1)`, promote that entry only after a visible notification expires, and remove index `count - 1`. With `MAX_NOTIFICATIONS = 5`, the script implementation therefore has five visible slots and a last-in-first-out deferred backlog.

Pinned CF `NotificationSystem.c` hashes to `84DEA071E55B1578394A00DFC2403CE8962306000B182BE35F2541BC769188F8`. It declares `modded class NotificationSystem`, and its client receive path constructs `NotificationRuntimeData` and calls `m_Instance.AddNotif(data)`, directly refuting an independent CF notification channel at this pin.

The local CF checkout HEAD and origin were independently checked. An internet-facing `git ls-remote` returned commit `0763e7e7548c9a0bed6626afff835de80693ebf3` for both `HEAD` and `refs/heads/production`, matching the local pin and the source-use record.

The baseline page SHA-256 is `6C48FD6E520EE6227496A895567218EF6D2D2DD4F728D3F85D164ACF480931D0`; the current working page SHA-256 is `679C254F9BCCE763182D6E5B661894259B3308F7F8B9C45D0C8696F0DBC9C248`. The current engine diff already owns the `ENG-002` Multi-Mod paragraph at baseline line 397, but the earlier line-296 assertion remains unchanged.

## `NOTIFY-EXTRA-001` — accept revised exact repair

Replace the complete baseline line-388 bullet:

> - **Respect the 5-notification stack limit.** Sending many notifications in rapid succession pushes older ones off screen before players can read them. Batch related messages or use longer display times.

with:

> - **Respect the 5-notification stack limit.** At most five notifications are visible. Additional notifications are appended to the deferred array and promoted as visible notifications expire. This script implementation promotes the last deferred entry first, so its overflow backlog is LIFO. Batch related messages or use longer display times.

The original statement is wrong: the opened code does not push existing visible entries away when the sixth notification arrives. The revised wording ties LIFO specifically to observed array operations in this script snapshot and does not extrapolate native internals or UI behavior.

## `ENG-002` supplement — accept revised exact repair

Baseline line 296 is a distinct textual occurrence of the same already-owned error. Replace the complete paragraph:

> Several large public frameworks (CommunityFramework, DayZ-Expansion) ship their own notification channels that stack above the vanilla toasts, adding conveniences such as colored icons, localized strings, and per-server styling. You do not need a framework to get most of that --- a thin static wrapper over the vanilla `NotificationSystem` gives you named severity helpers, consistent icons, and a single choke point for logging, while still sharing the vanilla 5-notification stack.

with:

> Notification features and rendering paths are framework-specific. At pinned CommunityFramework commit `0763e7e7548c9a0bed6626afff835de80693ebf3`, CF mods the vanilla `NotificationSystem` and feeds its inherited notification path rather than establishing an independent channel; inspect other frameworks and versions separately. You do not need a framework for the conveniences shown here --- a thin static wrapper over the vanilla `NotificationSystem` gives you named severity helpers, consistent icons, and a single choke point for logging while sharing the vanilla 5-notification stack.

Keep the engine worker's existing `ENG-002` repair at baseline line 397. This supplemental repair uses the same ID and must not be counted as a new finding. The evidence establishes CF behavior only at the pinned commit and does not establish DayZ-Expansion behavior, hence the explicit framework/version qualification.

## Limitations

This is static source confirmation only. No notification display, ordering, network, native, or runtime behavior was executed, and the LIFO statement applies only to the opened script implementation's explicit deferred-array algorithm.
