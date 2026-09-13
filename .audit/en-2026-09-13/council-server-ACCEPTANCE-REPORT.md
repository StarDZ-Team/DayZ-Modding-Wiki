# Server repair acceptance

**Verdict: approved.** CS13-1 through CS13-4 resolve; approval binds the twelve child pages and reports below. Integration remains with the coordinator and committer.

Main observed HEAD: `9c3f2b0d6406dcdccf5f6f7487a2c18391c08fe6`; previous council HEAD: `d19ede0eb2d7419abde1bfa6bd328ac12a8142e6`; child HEAD: `42b5f2c5c8c862ea1d94224763b7eef0e4c95785`. Main advanced through unrelated changes; its twelve server pages are clean and match the prior council main bytes. All twelve differ from the reviewed child.

## Bounded evidence

- CS13-1: Chapter 04:629/631/634 now says summarized and requires all multi-element/flags elements for both types and events, matching cached mission-files lines 38-44. Adjacent messages, group replacement, spawnabletypes, globals/economy and event children rules remain intact.
- CS13-2: Chapter 03:91 uses bool / false,true / false and explicitly leaves parser equivalence unverified, matching cached Server Configuration lines 22-23. Identifier caveat and access-control link are retained.
- CS13-3: Chapter 04:437/534 removes the speculative numerical models and states multiple-item and empty-selection semantics are unverified. No assertion of independent probability addition remains; engine semantics are not inferred.
- CS13-4: Chapter 04:71 matches custom-terrain cache line 92 for mapgroupdirt purpose; :73 links to the existing chapter 12 territory heading and discussion; :67 points below to Tags. Independently counted 22 data rows at :52-73 with all ten additions retained; both third-revision reports now state 22, with no other report changes.

All 11 UTF-8 replacements reversed in memory to the prior council raw/LF hashes: exactly two pages and two reports changed. Ten other pages and seven historical reports remain byte-identical. Both fourth-revision output checksums pass. The eight resolved third findings (MAT-1, MAT-3, MAT-4, MAT-5, OPT-1, OPT-3, OPT-5, OPT-7) and all 21 historical dispositions are preserved, including withdrawn requests and the later MAT-1/MAT-5 closures; this is not a fresh whole-domain audit.

The three primary-source caches were actually reopened and rehashed. No live retrieval, runtime/parser test, build, source edits, integration or commit occurred. Native probability semantics remain unverified.

## Source bindings

- [DayZ:Central_Economy_mission_files_modding?action=raw](https://community.bistudio.com/wiki/DayZ:Central_Economy_mission_files_modding?action=raw): `C:/Users/LEONAR~1/AppData/Local/Temp/wiki-audit-20260911/BIKI-CE-mission-files-council-20260913.txt`; raw/LF `4940eb16d5002a08da0563f27d9e69d3a5e6b4956d083a381bf269c8578ae645`.
- [DayZ:Central_Economy_setup_for_custom_terrains?action=raw](https://community.bistudio.com/wiki/DayZ:Central_Economy_setup_for_custom_terrains?action=raw): `C:/Users/LEONAR~1/AppData/Local/Temp/wiki-audit-20260911/BIKI-CE-terrains-council-20260913.txt`; raw/LF `099cb40823d2ed9f2d601a9e936c648fdf9db799bd3a0c0ca9662532b05b1078`.
- [DayZ:Server_Configuration?action=raw](https://community.bistudio.com/wiki/DayZ:Server_Configuration?action=raw): `C:/Users/LEONAR~1/AppData/Local/Temp/wiki-audit-20260911/BIKI-Server-council-20260913.txt`; raw/LF `b2d11b4cd7d973ff65fd9804406e02d4c091176f9926ee1af1f04142fe4142f7`.

## Exact child page hashes

Raw SHA256 hashes exact bytes; LF SHA256 converts CRLF to LF only. Main comparison hashes are recorded per page in JSON.

| Path | Raw SHA256 | LF SHA256 |
|---|---|---|
| en/09-server-admin/01-server-setup.md | `9eb7b685512839a6840248e9c91b76db6af22d273ca461d910ea2fb217d4fec0` | `3ff2c03476ac5bdd83d48d57cfd4dfe41afa402575fda775cc92c77d32518338` |
| en/09-server-admin/02-directory-structure.md | `b5d33f4e7ad7d7264822e0e7a04a06544f4586013b699fba411f8e2f8b09a19f` | `2347bb40d55151dfa30bfc5dced1b5f1cac6d581240aa4b44c5536f36b8f7ae4` |
| en/09-server-admin/03-server-cfg.md | `0d3bd14292727a7752d5175466d0cfbeb9485b54e4024876957fb0c821678996` | `405dde26d9a61b970503a9056b0873e4b2d3bfac4fbf462a8d478d793b4f6ec4` |
| en/09-server-admin/04-loot-economy.md | `7ffe958e13891ddaca32409f8912840fd8228d834527a3ef3b0f9d2ac981e830` | `84e40672a7b6f1fe38b8f8f4b76be785efcfb95c2cba6991b3c3146a427bc0c4` |
| en/09-server-admin/05-vehicle-spawning.md | `04f8ce76802d350a8779ed669663b77e489e8b9b99b7a6a7b5a3fb0c4a3f7efc` | `e7bb44a9f777767fc1f7c00f2615b04c203a85053df39695cdc6cf8f50717335` |
| en/09-server-admin/06-player-spawning.md | `d4772ffed9ed1549ef2226a34ee162fd028453d660db48a90925710db60322cd` | `7dca57d6da99730d41b8ba7c20760fc94e8ee13c6ab42ed61b9d1063be5a91af` |
| en/09-server-admin/07-persistence.md | `a7b4de6249d00e6af6485f294b7869d44ea3541de8fae7b3c1be8c01bffcfc01` | `fccd97afb70830ec1b48bfa10cf2552258cd7efd7561bc9683c29a3141315a4c` |
| en/09-server-admin/08-performance.md | `24e8aaf097cb30d312f0c4b37afce2c82b3a549388d6c75f82ad7d9e8d444cef` | `95c3952f5311aebbe3fd35e04bc8830d4e002ebc295badf47cc513cb77596e5f` |
| en/09-server-admin/09-access-control.md | `aac968e574f7cc6da5c4c9351771abfcb33c456bc474b1d05fb193d96dff0bd0` | `4ae065361d1eefdda15197f9d8d08bc53c7a59b3c2a2a613ca9d951d530715fd` |
| en/09-server-admin/10-mod-management.md | `9fbe9d3fbdb79d5257429f13fa153e74717fec3b64e00c567240d38f0c13b143` | `b18e5116b9df930324be026d1d7bb6650fb1e90a098770e853cffdeb3b64bffe` |
| en/09-server-admin/11-troubleshooting.md | `378a8e849b9300c4f21933c40d762f8bbcf5d1440a3a02324602f524cd5afaa5` | `c64aa9877fdae952860ec896e329ec2ff634b1a305b960e6c4be7dda59ec127a` |
| en/09-server-admin/12-advanced.md | `8605a3aa971410c3d1a297d8e8697eb727fa6398ccce206eed8317635cc0ef7f` | `f7794cedbe560e4f3dbb7856453a5fc38cf5230e000e9eac466f532a6d0c1bc8` |

## Exact report hashes

Roots refer to the main and child paths in JSON. Historical reports retain their historical status; fourth revision and this acceptance supersede the four bounded requests.

| Root / path | Raw SHA256 | LF SHA256 |
|---|---|---|
| child: .audit/en-2026-09-11/server-COUNCIL-REVISION.json | `6d0df34ede1820533799a3e498b6e5b4f076eec7663bcacab5608edd284a9644` | `6d0df34ede1820533799a3e498b6e5b4f076eec7663bcacab5608edd284a9644` |
| child: .audit/en-2026-09-11/server-COUNCIL-REVISION.md | `8b053c5d2378837d858f767cf134e74f213b17abe2294276f66f240ef0c50076` | `8b053c5d2378837d858f767cf134e74f213b17abe2294276f66f240ef0c50076` |
| child: .audit/en-2026-09-11/server-findings.json | `4fe2e56528e7286e01055beb1e1ad3a30cf99cf41ee5727785458cd015bb9a8e` | `4fe2e56528e7286e01055beb1e1ad3a30cf99cf41ee5727785458cd015bb9a8e` |
| child: .audit/en-2026-09-11/server-REPORT.md | `83f79cea3ee8b8abc0040feffd2b8a96e1e7733c3ddafbedaa9cb1f42930ef99` | `067f3bf22632715ee9412f5661379d0377df2b8967d7a59c89f3d1a1903e844e` |
| child: .audit/en-2026-09-11/server-REVISION.md | `8ea14f3378c7f81a6ff1f076fda254af6dd90aac6b77de016b018deeaa610268` | `7e6ed1ade302e67eaf6eaed4e1bfc074d2422301f324b5e0ef11b39826d13662` |
| child: .audit/en-2026-09-11/server-SECOND-REVISION.json | `84c219bc5e60a17de680b664aca8b5c36a96db6a3ad701770dd4d2d1d5af675c` | `84c219bc5e60a17de680b664aca8b5c36a96db6a3ad701770dd4d2d1d5af675c` |
| child: .audit/en-2026-09-11/server-SECOND-REVISION.md | `95c8ed6aa5abb0f54f46193b7c4cb84b16bd39f4e3700646a694f076f280eb08` | `b7b66ecf0a9480503580ced221d1ffa0a7e538ac06df5fab6b258d0d849face3` |
| child: .audit/en-2026-09-11/server-THIRD-REVISION.json | `40588451247cccfe510d46437041e23cf3d9a71520a2fda13b0527b95f568446` | `40588451247cccfe510d46437041e23cf3d9a71520a2fda13b0527b95f568446` |
| child: .audit/en-2026-09-11/server-THIRD-REVISION.md | `e02c5f55a537e6eacfc5d324ae173436aae64070b7f01b2c9d15054d0b231d14` | `e02c5f55a537e6eacfc5d324ae173436aae64070b7f01b2c9d15054d0b231d14` |
| child: .audit/en-2026-09-13/server-FOURTH-REVISION.json | `ed9dd3e4072d7444ff71df69521f889ade7cb77705c838e55f6d480263c8ec01` | `e8ecf0fd10ae2d3f13ee02e907e1e44f6a757b1a0300691a6007cdbf63a4f301` |
| child: .audit/en-2026-09-13/server-FOURTH-REVISION-REPORT.md | `ebf65ecfd20d0fbf046fc9baaf52feb1803c24e71e9a74786694b239eb332c3f` | `1782b4d414fc99315df6f931866827299730ceaec421b2889b6a5feec08d4d6e` |
| child: .audit/en-2026-09-13/server-FOURTH-REVISION-SHA256.json | `137b5a142ff6b567d49ab1f217239d424f1881fb0c4a17a5970838d678bdc88d` | `6fea8b8ac803ac89354a4f1c49b739768dead358732ccb6cccdef038c5cf5856` |
| main: .audit/en-2026-09-13/council-server.json | `66328542fe1ebe3e0137645fbb7037eba99f8cfcda15228bdbe378e7742793a4` | `a84ca26f961b90cd23f6000ff5496fe425c937b6b284a41ce23ab74e6f86a647` |
| main: .audit/en-2026-09-13/council-server-REPORT.md | `2373c2cc4327c4ed0a3802b187c78e82f62f7450c194e948d6e1bfbc42939fe3` | `6a939fd938583ef59d6dd8081a40e1730841b4992a1ac6c8bfcdcba23c586955` |
| main: .audit/en-2026-09-13/council-server-ACCEPTANCE.json | `389f2d6813cc439f447b0e179b2569d3222e88b2955276e4266548b26a5621a4` | `389f2d6813cc439f447b0e179b2569d3222e88b2955276e4266548b26a5621a4` |

This Markdown report excludes its own hash to avoid self-reference. Remaining: route approved child bytes to the committer and recheck these hashes and current main server state before integration.
