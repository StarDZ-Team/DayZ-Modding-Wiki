# DayZ Modding Wiki (日本語版)

> DayZ Enforce Script によるMod開発の総合リファレンスガイド

---

## 目次

### Part 1: Enforce Script 言語リファレンス

| 章 | タイトル | 内容 |
|---|---|---|
| [1.1](01-enforce-script/01-variables-types.md) | 変数と型 | プリミティブ型、宣言、型変換 |
| [1.2](01-enforce-script/02-arrays-maps-sets.md) | Array、Map、Set | コレクション型の完全リファレンス |
| [1.3](01-enforce-script/03-classes-inheritance.md) | クラスと継承 | クラス宣言、継承、override、static |
| [1.4](01-enforce-script/04-modded-classes.md) | Modded Class | DayZ Modding の核心メカニズム |
| [1.5](01-enforce-script/05-control-flow.md) | 制御フロー | if/else、for、while、foreach、switch |
| [1.6](01-enforce-script/06-strings.md) | String 操作 | 文字列メソッド完全リファレンス |
| [1.7](01-enforce-script/07-math-vectors.md) | Math と Vector | 数学関数、ベクトル演算 |
| [1.8](01-enforce-script/08-memory-management.md) | メモリ管理 | ref、autoptr、参照カウント、循環参照 |
| [1.9](01-enforce-script/09-casting-reflection.md) | キャストとリフレクション | 型変換、ランタイム型検査、リフレクション API |
| [1.10](01-enforce-script/10-enums-preprocessor.md) | Enum とプリプロセッサ | 列挙型、ビットフラグ、#ifdef |
| [1.11](01-enforce-script/11-error-handling.md) | エラーハンドリング | ガード節、ErrorEx、デバッグログ |
| [1.12](01-enforce-script/12-gotchas.md) | 落とし穴一覧 | 存在しない機能と回避策 |

### Part 2: Mod の構成

| 章 | タイトル | 内容 |
|---|---|---|
| [2.1](02-mod-structure/01-five-layers.md) | 5層スクリプト階層 | 1_Core ～ 5_Mission のレイヤー構成 |
| [2.2](02-mod-structure/02-config-cpp.md) | config.cpp 詳解 | CfgPatches、CfgMods、スクリプトモジュール |
| [2.3](02-mod-structure/03-mod-cpp.md) | mod.cpp と Workshop | ランチャー表示用メタデータ |
| [2.4](02-mod-structure/04-minimum-viable-mod.md) | 最小構成の Mod | ゼロから動く Mod を作る |
| [2.5](02-mod-structure/05-file-organization.md) | ファイル構成のベストプラクティス | ディレクトリ構造、命名規則 |

### Part 3: GUI システム

| 章 | タイトル | 内容 |
|---|---|---|
| [3.1](03-gui-system/01-widget-types.md) | Widget 型一覧 | 全 Widget タイプのリファレンス |
| [3.2](03-gui-system/02-layout-files.md) | Layout ファイル形式 | .layout ファイルの構文と属性 |
| [3.3](03-gui-system/03-sizing-positioning.md) | サイズとポジション | 比率指定 vs ピクセル指定 |
| [3.4](03-gui-system/04-containers.md) | コンテナ Widget | WrapSpacer、GridSpacer、ScrollWidget |
| [3.5](03-gui-system/05-programmatic-widgets.md) | プログラムによる Widget 作成 | コードから Widget を生成 |
| [3.6](03-gui-system/06-event-handling.md) | イベントハンドリング | クリック、入力、フォーカスのイベント処理 |
| [3.7](03-gui-system/07-styles-fonts.md) | スタイルとフォント | .styles ファイル、フォント設定 |

### Part 4: ファイル形式

| 章 | タイトル | 内容 |
|---|---|---|
| [4.1](04-file-formats/01-textures.md) | テクスチャ | .paa、.edds 形式 |
| [4.2](04-file-formats/02-models.md) | モデル | .p3d 3Dモデル形式 |
| [4.3](04-file-formats/03-materials.md) | マテリアル | .rvmat マテリアル定義 |
| [4.4](04-file-formats/04-audio.md) | オーディオ | .ogg サウンドファイル |
| [4.5](04-file-formats/05-dayz-tools.md) | DayZ Tools | 公式ツールチェーン |
| [4.6](04-file-formats/06-pbo-packing.md) | PBO パッキング | Addon Builder とパッキング |

### Part 5: 設定ファイル

| 章 | タイトル | 内容 |
|---|---|---|
| [5.1](05-config-files/01-stringtable.md) | Stringtable | ローカライゼーション (stringtable.csv) |
| [5.2](05-config-files/02-inputs-xml.md) | Inputs.xml | カスタムキーバインド |
| [5.3](05-config-files/03-credits-json.md) | Credits.json | クレジット情報 |
| [5.4](05-config-files/04-imagesets.md) | Imageset | アイコンとスプライトシート |

### Part 6: エンジン API

| 章 | タイトル | 内容 |
|---|---|---|
| [6.1](06-engine-api/01-entity-system.md) | エンティティシステム | Object、EntityAI、ItemBase |
| [6.2](06-engine-api/02-vehicles.md) | 車両 | CarScript、車両システム |
| [6.3](06-engine-api/03-weather.md) | 天候 | Weather API |
| [6.4](06-engine-api/04-cameras.md) | カメラ | カメラシステム |
| [6.5](06-engine-api/05-ppe.md) | ポストプロセスエフェクト | PPE システム |
| [6.6](06-engine-api/06-notifications.md) | 通知 | 通知システム |
| [6.7](06-engine-api/07-timers.md) | タイマー | CallLater、タイマーシステム |
| [6.8](06-engine-api/08-file-io.md) | ファイル I/O | ファイル読み書き、JSON |
| [6.9](06-engine-api/09-networking.md) | ネットワーキング | RPC、同期 |
| [6.10](06-engine-api/10-central-economy.md) | Central Economy | アイテムスポーン、types.xml |

### Part 7: 設計パターン

| 章 | タイトル | 内容 |
|---|---|---|
| [7.1](07-patterns/01-singletons.md) | シングルトン | シングルトンパターン |
| [7.2](07-patterns/02-module-systems.md) | モジュールシステム | モジュール管理パターン |
| [7.3](07-patterns/03-rpc-patterns.md) | RPC パターン | リモートプロシージャコール |
| [7.4](07-patterns/04-config-persistence.md) | 設定の永続化 | JSON 設定ファイルの読み書き |
| [7.5](07-patterns/05-permissions.md) | パーミッション | 権限管理システム |
| [7.6](07-patterns/06-events.md) | イベントシステム | イベントバス、コールバック |
| [7.7](07-patterns/07-performance.md) | パフォーマンス | 最適化のベストプラクティス |

### Part 8: チュートリアル

| 章 | タイトル | 内容 |
|---|---|---|
| [8.1](08-tutorials/01-first-mod.md) | はじめての Mod | ステップバイステップガイド |
| [8.2](08-tutorials/02-custom-item.md) | カスタムアイテム | アイテムの作成 |
| [8.3](08-tutorials/03-admin-panel.md) | 管理パネル | Admin パネルの構築 |
| [8.4](08-tutorials/04-chat-commands.md) | チャットコマンド | コマンドシステムの実装 |

### クイックリファレンス

| ページ | 内容 |
|---|---|
| [チートシート](cheatsheet.md) | Enforce Script 全機能の早見表 |

---

## この Wiki について

この Wiki は DayZ の Enforce Script によるMod開発について、基礎から応用まで網羅した日本語リファレンスです。

**対象読者:** DayZ のMod開発に興味がある開発者（C#、Java、C++ などの経験があると理解しやすいですが、プログラミング初心者でも順を追って学べます）。

**注意事項:**
- Enforce Script は C/C++ とは**異なる言語**です。見た目は似ていますが、独自のルールと制限があります
- `try/catch` は存在しません。ガード節パターンを使います
- `do...while` は存在しません。`while` + `break` パターンを使います
- コード例内のコメントは英語のまま保持しています（コードの可読性のため）

---

*[英語版はこちら](../en/) | 翻訳元: DayZ Modding Wiki (English)*
