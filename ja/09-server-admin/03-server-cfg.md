# Chapter 9.3: serverDZ.cfg 完全リファレンス

[ホーム](../README.md) | [<< 前へ: ディレクトリ構造](02-directory-structure.md) | **serverDZ.cfgリファレンス** | [次へ: ルートエコノミー詳解 >>](04-loot-economy.md)

---

> **概要:** `serverDZ.cfg` のすべてのパラメータを、その目的、有効な値、デフォルト動作とともにドキュメント化しています。このファイルはサーバーのアイデンティティ、ネットワーク設定、ゲームプレイルール、時間加速、ミッション選択を制御します。

---

## 目次

- [ファイル形式](#ファイル形式)
- [サーバーアイデンティティ](#サーバーアイデンティティ)
- [ネットワークとセキュリティ](#ネットワークとセキュリティ)
- [ゲームプレイルール](#ゲームプレイルール)
- [時間と天候](#時間と天候)
- [パフォーマンスとログインキュー](#パフォーマンスとログインキュー)
- [パーシステンスとインスタンス](#パーシステンスとインスタンス)
- [ミッション選択](#ミッション選択)
- [完全な設定例](#完全な設定例)
- [設定を上書きする起動パラメータ](#設定を上書きする起動パラメータ)

---

## ファイル形式

`serverDZ.cfg` はBohemiaの設定形式（Cに似ています）を使用します。ルール:

- すべてのパラメータ代入は **セミコロン** `;` で終わります
- 文字列は **ダブルクォート** `""` で囲みます
- コメントには `//` を使用します（単一行）
- `class Missions` ブロックは中括弧 `{}` を使用し、`};` で終わります
- ファイルはUTF-8またはANSIエンコーディングである必要があります -- BOMなし

セミコロンが欠けていると、サーバーがサイレントに失敗するか、後続のパラメータが無視されます。

---

## サーバーアイデンティティ

```cpp
hostname = "My DayZ Server";         // ブラウザに表示されるサーバー名
password = "";                       // 接続パスワード（空 = パブリック）
passwordAdmin = "";                  // ゲーム内コンソールでの管理者ログインパスワード
description = "";                    // サーバーブラウザの詳細に表示される説明
```

| パラメータ | 型 | デフォルト | 備考 |
|-----------|------|---------|-------|
| `hostname` | string | `""` | サーバーブラウザに表示されます。最大約100文字です。 |
| `password` | string | `""` | パブリックサーバーの場合は空のままにします。プレイヤーはこれを入力して参加します。 |
| `passwordAdmin` | string | `""` | ゲーム内の `#login` コマンドで使用します。**すべてのサーバーで設定してください。** |
| `description` | string | `""` | 複数行の説明はサポートされていません。短くしてください。 |

---

## ネットワークとセキュリティ

```cpp
maxPlayers = 60;                     // 最大プレイヤースロット
verifySignatures = 2;                // PBO署名検証（2のみサポート）
forceSameBuild = 1;                  // クライアント/サーバーのEXEバージョン一致を要求
enableWhitelist = 0;                 // ホワイトリストの有効化/無効化
disableVoN = 0;                      // ボイスオーバーネットワークの無効化
vonCodecQuality = 20;               // VoN音声品質（0-30）
guaranteedUpdates = 1;               // ネットワークプロトコル（常に1を使用）
```

| パラメータ | 型 | 有効な値 | デフォルト | 備考 |
|-----------|------|-------------|---------|-------|
| `maxPlayers` | int | 1-60 | 60 | RAM使用量に影響します。各プレイヤーは約50-100 MBを追加します。 |
| `verifySignatures` | int | 2 | 2 | 値2のみサポートされています。PBOファイルを `.bisign` キーと照合検証します。 |
| `forceSameBuild` | int | 0, 1 | 1 | 1の場合、クライアントはサーバーの正確なEXEバージョンと一致する必要があります。常に1にしてください。 |
| `enableWhitelist` | int | 0, 1 | 0 | 1の場合、`whitelist.txt` に記載されたSteam64 IDのみ接続できます。 |
| `disableVoN` | int | 0, 1 | 0 | 1に設定するとゲーム内ボイスチャットが完全に無効になります。 |
| `vonCodecQuality` | int | 0-30 | 20 | 値が高いほど音声品質が向上しますが、帯域幅が増えます。20が良いバランスです。 |
| `guaranteedUpdates` | int | 1 | 1 | ネットワークプロトコル設定です。常に1を使用してください。 |

### シャードID

```cpp
shardId = "123abc";                  // プライベートシャード用の6桁の英数字
```

| パラメータ | 型 | デフォルト | 備考 |
|-----------|------|---------|-------|
| `shardId` | string | `""` | プライベートハイブサーバーに使用します。同じ `shardId` のサーバーのプレイヤーはキャラクターデータを共有します。パブリックハイブの場合は空のままにします。 |

---

## ゲームプレイルール

```cpp
disable3rdPerson = 0;               // 三人称カメラの無効化
disableCrosshair = 0;               // クロスヘアの無効化
disablePersonalLight = 1;           // 周囲プレイヤーライトの無効化
lightingConfig = 0;                 // 夜の明るさ（0 = 明るい、1 = 暗い）
```

| パラメータ | 型 | 有効な値 | デフォルト | 備考 |
|-----------|------|-------------|---------|-------|
| `disable3rdPerson` | int | 0, 1 | 0 | 一人称専用サーバーには1に設定します。最も一般的な「ハードコア」設定です。 |
| `disableCrosshair` | int | 0, 1 | 0 | クロスヘアを除去するには1に設定します。`disable3rdPerson=1` と組み合わせることが多いです。 |
| `disablePersonalLight` | int | 0, 1 | 1 | 「パーソナルライト」は夜間のプレイヤー周囲の微妙な光です。ほとんどのサーバーはリアリズムのために無効化（値1）します。 |
| `lightingConfig` | int | 0, 1 | 0 | 0 = 明るい夜（月明かりが見える）。1 = 真っ暗な夜（懐中電灯/NVGが必要）。 |

---

## 時間と天候

```cpp
serverTime = "SystemTime";                 // 初期時刻
serverTimeAcceleration = 12;               // 時間速度倍率（0-24）
serverNightTimeAcceleration = 1;           // 夜間時間速度倍率（0.1-64）
serverTimePersistent = 0;                  // 再起動間で時間を保存
```

| パラメータ | 型 | 有効な値 | デフォルト | 備考 |
|-----------|------|-------------|---------|-------|
| `serverTime` | string | `"SystemTime"` または `"YYYY/MM/DD/HH/MM"` | `"SystemTime"` | `"SystemTime"` はマシンのローカル時計を使用します。常時昼間サーバーの場合は `"2024/9/15/12/0"` のような固定時間を設定します。 |
| `serverTimeAcceleration` | int | 0-24 | 12 | ゲーム内時間の倍率です。12の場合、24時間サイクルは実時間2時間で完了します。1の場合はリアルタイムです。24の場合は1時間で1日が経過します。 |
| `serverNightTimeAcceleration` | float | 0.1-64 | 1 | `serverTimeAcceleration` と乗算されます。値4でacceleration 12の場合、夜は48倍速で経過します（非常に短い夜）。 |
| `serverTimePersistent` | int | 0, 1 | 0 | 1の場合、サーバーはゲーム内時計をディスクに保存し、再起動後にそこから再開します。0の場合、毎回の再起動時に `serverTime` にリセットされます。 |

### 一般的な時間設定

**常時昼間:**
```cpp
serverTime = "2024/6/15/12/0";
serverTimeAcceleration = 0;
serverTimePersistent = 0;
```

**高速昼夜サイクル（2時間の昼、短い夜）:**
```cpp
serverTime = "SystemTime";
serverTimeAcceleration = 12;
serverNightTimeAcceleration = 4;
serverTimePersistent = 1;
```

**リアルタイム昼夜:**
```cpp
serverTime = "SystemTime";
serverTimeAcceleration = 1;
serverNightTimeAcceleration = 1;
serverTimePersistent = 1;
```

---

## パフォーマンスとログインキュー

```cpp
loginQueueConcurrentPlayers = 5;     // ログイン中に同時処理されるプレイヤー数
loginQueueMaxPlayers = 500;          // 最大ログインキューサイズ
```

| パラメータ | 型 | デフォルト | 備考 |
|-----------|------|---------|-------|
| `loginQueueConcurrentPlayers` | int | 5 | 同時にロードインできるプレイヤー数です。値を低くすると再起動後のサーバー負荷スパイクが軽減されます。ハードウェアが強力でプレイヤーがキュー時間について不満を述べる場合は10-15に上げてください。 |
| `loginQueueMaxPlayers` | int | 500 | この数のプレイヤーがすでにキューに入っている場合、新しい接続は拒否されます。ほとんどのサーバーでは500で問題ありません。 |

---

## パーシステンスとインスタンス

```cpp
instanceId = 1;                      // サーバーインスタンス識別子
storageAutoFix = 1;                  // 破損したパーシステンスファイルの自動修復
```

| パラメータ | 型 | デフォルト | 備考 |
|-----------|------|---------|-------|
| `instanceId` | int | 1 | サーバーインスタンスを識別します。パーシステンスデータは `storage_<instanceId>/` に格納されます。同じマシンで複数のサーバーを実行する場合は、それぞれに異なる `instanceId` を付与してください。 |
| `storageAutoFix` | int | 1 | 1の場合、サーバーは起動時にパーシステンスファイルをチェックし、破損したものを空のファイルに置き換えます。常に1のままにしてください。 |

---

## ミッション選択

```cpp
class Missions
{
    class DayZ
    {
        template = "dayzOffline.chernarusplus";
    };
};
```

`template` 値は `mpmissions/` 内のフォルダ名と正確に一致する必要があります。利用可能なバニラミッション:

| テンプレート | マップ | DLC必要 |
|----------|-----|:---:|
| `dayzOffline.chernarusplus` | チェルナルス | いいえ |
| `dayzOffline.enoch` | リヴォニア | はい |
| `dayzOffline.sakhal` | サハル | はい |

カスタムミッション（例: MODやコミュニティマップから）は独自のテンプレート名を使用します。フォルダが `mpmissions/` に存在する必要があります。

---

## 完全な設定例

すべてのパラメータを含む完全なデフォルト `serverDZ.cfg` です:

```cpp
hostname = "EXAMPLE NAME";              // サーバー名
password = "";                          // サーバーへの接続パスワード
passwordAdmin = "";                     // サーバー管理者になるためのパスワード

description = "";                       // サーバーブラウザの説明

enableWhitelist = 0;                    // ホワイトリストの有効化/無効化（値 0-1）

maxPlayers = 60;                        // 最大プレイヤー数

verifySignatures = 2;                   // .pboを.bisignファイルと照合検証（2のみサポート）
forceSameBuild = 1;                     // クライアント/サーバーのバージョン一致を要求（値 0-1）

disableVoN = 0;                         // ボイスオーバーネットワークの有効化/無効化（値 0-1）
vonCodecQuality = 20;                   // ボイスオーバーネットワークのコーデック品質（値 0-30）

shardId = "123abc";                     // プライベートシャード用の6桁の英数字

disable3rdPerson = 0;                   // 三人称視点の切り替え（値 0-1）
disableCrosshair = 0;                   // クロスヘアの切り替え（値 0-1）

disablePersonalLight = 1;              // すべてのクライアントのパーソナルライトを無効化
lightingConfig = 0;                     // 0 で明るい夜、1 で暗い夜

serverTime = "SystemTime";             // 初期ゲーム内時刻（"SystemTime" または "YYYY/MM/DD/HH/MM"）
serverTimeAcceleration = 12;           // 時間速度倍率（0-24）
serverNightTimeAcceleration = 1;       // 夜間時間速度倍率（0.1-64）、serverTimeAccelerationとも乗算
serverTimePersistent = 0;              // 再起動間で時間を保存（値 0-1）

guaranteedUpdates = 1;                 // ネットワークプロトコル（常に1を使用）

loginQueueConcurrentPlayers = 5;       // ログイン中に同時処理されるプレイヤー数
loginQueueMaxPlayers = 500;            // 最大ログインキューサイズ

instanceId = 1;                        // サーバーインスタンスID（ストレージフォルダ命名に影響）

storageAutoFix = 1;                    // 破損したパーシステンスの自動修復（値 0-1）

class Missions
{
    class DayZ
    {
        template = "dayzOffline.chernarusplus";
    };
};
```

---

## 設定を上書きする起動パラメータ

一部の設定は `DayZServer_x64.exe` の起動時にコマンドラインパラメータで上書きできます:

| パラメータ | 上書き対象 | 例 |
|-----------|-----------|---------|
| `-config=` | 設定ファイルのパス | `-config=serverDZ.cfg` |
| `-port=` | ゲームポート | `-port=2302` |
| `-profiles=` | プロファイル出力ディレクトリ | `-profiles=profiles` |
| `-mod=` | クライアント側MOD（セミコロン区切り） | `-mod=@CF;@VPPAdminTools` |
| `-servermod=` | サーバー専用MOD | `-servermod=@MyServerMod` |
| `-BEpath=` | BattlEyeパス | `-BEpath=battleye` |
| `-dologs` | ログを有効にする | -- |
| `-adminlog` | 管理者ログを有効にする | -- |
| `-netlog` | ネットワークログを有効にする | -- |
| `-freezecheck` | フリーズ時の自動再起動 | -- |
| `-cpuCount=` | 使用するCPUコア数 | `-cpuCount=4` |
| `-noFilePatching` | ファイルパッチングを無効にする | -- |

### 完全な起動例

```batch
start DayZServer_x64.exe ^
  -config=serverDZ.cfg ^
  -port=2302 ^
  -profiles=profiles ^
  -mod=@CF;@VPPAdminTools;@MyMod ^
  -servermod=@MyServerOnlyMod ^
  -dologs -adminlog -netlog -freezecheck
```

MODは `-mod=` で指定された順序でロードされます。依存関係の順序が重要です: MOD BがMOD Aを必要とする場合、MOD Aを先にリストしてください。

---

**前へ:** [ディレクトリ構造](02-directory-structure.md) | [ホーム](../README.md) | **次へ:** [ルートエコノミー詳解 >>](04-loot-economy.md)
