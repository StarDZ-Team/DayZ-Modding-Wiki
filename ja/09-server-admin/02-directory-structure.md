# Chapter 9.2: ディレクトリ構造とミッションフォルダ

[ホーム](../README.md) | [<< 前へ: サーバーセットアップ](01-server-setup.md) | **ディレクトリ構造** | [次へ: serverDZ.cfgリファレンス >>](03-server-cfg.md)

---

> **概要:** DayZサーバーディレクトリとミッションフォルダ内のすべてのファイルとフォルダの完全なウォークスルーです。各ファイルの役割と、どのファイルが安全に編集できるかを理解することは、ルートエコノミーの調整やMODの追加を行う前に不可欠です。

---

## 目次

- [トップレベルサーバーディレクトリ](#トップレベルサーバーディレクトリ)
- [addons/ フォルダ](#addons-フォルダ)
- [keys/ フォルダ](#keys-フォルダ)
- [profiles/ フォルダ](#profiles-フォルダ)
- [mpmissions/ フォルダ](#mpmissions-フォルダ)
- [ミッションフォルダの構造](#ミッションフォルダの構造)
- [db/ フォルダ -- エコノミーコア](#db-フォルダ----エコノミーコア)
- [env/ フォルダ -- 動物テリトリー](#env-フォルダ----動物テリトリー)
- [storage_1/ フォルダ -- パーシステンス](#storage_1-フォルダ----パーシステンス)
- [トップレベルミッションファイル](#トップレベルミッションファイル)
- [編集すべきファイルと触れてはいけないファイル](#編集すべきファイルと触れてはいけないファイル)

---

## トップレベルサーバーディレクトリ

```
DayZServer/
  DayZServer_x64.exe          # サーバー実行ファイル
  serverDZ.cfg                 # メインサーバー設定（名前、パスワード、MOD、時間）
  dayzsetting.xml              # レンダリング設定（専用サーバーでは無関係）
  ban.txt                      # BAN済みSteam64 ID、1行に1つ
  whitelist.txt                # ホワイトリストSteam64 ID、1行に1つ
  steam_appid.txt              # "221100" を含む -- 編集しないでください
  dayz.gproj                   # Workbenchプロジェクトファイル -- 編集しないでください
  addons/                      # バニラゲームPBO
  battleye/                    # アンチチートファイル
  config/                      # Steam設定（config.vdf）
  dta/                         # コアエンジンPBO（スクリプト、GUI、グラフィックス）
  keys/                        # 署名検証キー（.bikeyファイル）
  logs/                        # エンジンレベルログ
  mpmissions/                  # すべてのミッションフォルダ
  profiles/                    # ランタイム出力（スクリプトログ、プレイヤーDB、クラッシュダンプ）
  server_manager/              # サーバー管理ユーティリティ
```

---

## addons/ フォルダ

PBOファイルとしてパッケージ化されたすべてのバニラゲームコンテンツを含みます。各PBOには対応する `.bisign` 署名ファイルがあります:

```
addons/
  ai.pbo                       # AI行動スクリプト
  ai.pbo.dayz.bisign           # ai.pboの署名
  animals.pbo                  # 動物の定義
  characters_backpacks.pbo     # バックパックのモデル/設定
  characters_belts.pbo         # ベルトアイテムのモデル
  weapons_firearms.pbo         # 武器のモデル/設定
  ... (100以上のPBOファイル)
```

**これらのファイルは絶対に編集しないでください。** SteamCMDでサーバーをアップデートするたびに上書きされます。MODは `modded` クラスシステムを通じてバニラの動作を上書きします。PBOを変更することはありません。

---

## keys/ フォルダ

MODの署名を検証するために使用される `.bikey` 公開鍵ファイルを含みます:

```
keys/
  dayz.bikey                   # バニラ署名キー（常に存在）
```

MODを追加する際は、その `.bikey` ファイルをこのフォルダにコピーします。サーバーは `serverDZ.cfg` の `verifySignatures = 2` を使用して、このフォルダに対応する `.bikey` がないPBOを拒否します。

プレイヤーが `keys/` フォルダにキーがないMODをロードすると、**「Signature check failed」** でキックされます。

---

## profiles/ フォルダ

サーバーの初回起動時に作成されます。ランタイム出力を含みます:

```
profiles/
  BattlEye/                              # BEログとBAN
  DataCache/                             # キャッシュデータ
  Users/                                 # プレイヤーごとの設定ファイル
  DayZServer_x64_2026-03-08_11-34-31.ADM  # 管理者ログ
  DayZServer_x64_2026-03-08_11-34-31.RPT  # エンジンレポート（クラッシュ情報、警告）
  script_2026-03-08_11-34-35.log           # スクリプトログ（最も重要なデバッグツール）
```

**スクリプトログ** はここで最も重要なファイルです。すべての `Print()` 呼び出し、すべてのスクリプトエラー、すべてのMODロードメッセージがここに記録されます。何かが壊れた場合、最初に確認する場所です。

ログファイルは時間とともに蓄積されます。古いログは自動的には削除されません。

---

## mpmissions/ フォルダ

マップごとに1つのサブフォルダを含みます:

```
mpmissions/
  dayzOffline.chernarusplus/    # チェルナルス（無料）
  dayzOffline.enoch/            # リヴォニア（DLC）
  dayzOffline.sakhal/           # サハル（DLC）
```

フォルダ名の形式は `<missionName>.<terrainName>` です。`serverDZ.cfg` の `template` 値はこれらのフォルダ名のいずれかと正確に一致する必要があります。

---

## ミッションフォルダの構造

チェルナルスのミッションフォルダ（`mpmissions/dayzOffline.chernarusplus/`）には以下が含まれます:

```
dayzOffline.chernarusplus/
  init.c                         # ミッションエントリポイントスクリプト
  db/                            # コアエコノミーファイル
  env/                           # 動物テリトリー定義
  storage_1/                     # パーシステンスデータ（プレイヤー、ワールド状態）
  cfgeconomycore.xml             # エコノミールートクラスとログ設定
  cfgenvironment.xml             # 動物テリトリーファイルへのリンク
  cfgeventgroups.xml             # イベントグループ定義
  cfgeventspawns.xml             # イベント（車両など）の正確なスポーン位置
  cfgeffectarea.json             # 汚染ゾーン定義
  cfggameplay.json               # ゲームプレイチューニング（スタミナ、ダメージ、建築）
  cfgignorelist.xml              # エコノミーから完全に除外されるアイテム
  cfglimitsdefinition.xml        # 有効なカテゴリ/使用場所/値タグの定義
  cfglimitsdefinitionuser.xml    # ユーザー定義のカスタムタグ定義
  cfgplayerspawnpoints.xml       # 新規スポーン地点
  cfgrandompresets.xml           # 再利用可能なルートプール定義
  cfgspawnabletypes.xml          # スポーンされるエンティティのプリアタッチアイテムとカーゴ
  cfgundergroundtriggers.json    # 地下エリアトリガー
  cfgweather.xml                 # 天候設定
  areaflags.map                  # エリアフラグデータ（バイナリ）
  mapclusterproto.xml            # マップクラスタープロトタイプ定義
  mapgroupcluster.xml            # 建物グループクラスター定義
  mapgroupcluster01.xml          # クラスターデータ（パート1）
  mapgroupcluster02.xml          # クラスターデータ（パート2）
  mapgroupcluster03.xml          # クラスターデータ（パート3）
  mapgroupcluster04.xml          # クラスターデータ（パート4）
  mapgroupdirt.xml               # 地面ルート位置
  mapgrouppos.xml                # マップグループ位置
  mapgroupproto.xml              # マップグループのプロトタイプ定義
```

---

## db/ フォルダ -- エコノミーコア

これはCentral Economyの心臓部です。5つのファイルが何がスポーンするか、どこに、どれだけスポーンするかを制御します:

```
db/
  types.xml        # 最重要ファイル: すべてのアイテムのスポーンルールを定義
  globals.xml      # グローバルエコノミーパラメータ（タイマー、上限、数量）
  events.xml       # ダイナミックイベント（動物、車両、ヘリコプター）
  economy.xml      # エコノミーサブシステムのトグル（ルート、動物、車両）
  messages.xml     # プレイヤーへのスケジュールされたサーバーメッセージ
```

### types.xml

ゲーム内の **すべてのアイテム** のスポーンルールを定義します。約23,000行あり、最も大きなエコノミーファイルです。各エントリは、マップ上に存在すべきアイテムのコピー数、スポーン場所、パーシステンスの持続時間を指定します。詳細は [Chapter 9.4](04-loot-economy.md) を参照してください。

### globals.xml

エコノミー全体に影響するグローバルパラメータ: ゾンビ数、動物数、クリーンアップタイマー、ルートダメージ範囲、リスポーンタイミング。合計33のパラメータがあります。完全なリファレンスは [Chapter 9.4](04-loot-economy.md) を参照してください。

### events.xml

動物と車両のダイナミックスポーンイベントを定義します。各イベントはノミナル数、スポーン制約、子バリアントを指定します。例えば、`VehicleCivilianSedan` イベントは3色のバリアントで8台のセダンをマップ上にスポーンさせます。

### economy.xml

エコノミーサブシステムのマスタートグル:

```xml
<economy>
    <dynamic init="1" load="1" respawn="1" save="1"/>
    <animals init="1" load="0" respawn="1" save="0"/>
    <zombies init="1" load="0" respawn="1" save="0"/>
    <vehicles init="1" load="1" respawn="1" save="1"/>
    <randoms init="0" load="0" respawn="1" save="0"/>
    <custom init="0" load="0" respawn="0" save="0"/>
    <building init="1" load="1" respawn="0" save="1"/>
    <player init="1" load="1" respawn="1" save="1"/>
</economy>
```

| フラグ | 意味 |
|------|---------|
| `init` | 最初のサーバー起動時にアイテムをスポーンする |
| `load` | パーシステンスから保存された状態を読み込む |
| `respawn` | クリーンアップ後にアイテムのリスポーンを許可する |
| `save` | パーシステンスファイルに状態を保存する |

### messages.xml

すべてのプレイヤーにブロードキャストされるスケジュールメッセージです。カウントダウンタイマー、繰り返し間隔、接続時メッセージ、シャットダウン警告をサポートします:

```xml
<messages>
    <message>
        <deadline>600</deadline>
        <shutdown>1</shutdown>
        <text>#name will shutdown in #tmin minutes.</text>
    </message>
    <message>
        <delay>2</delay>
        <onconnect>1</onconnect>
        <text>Welcome to #name</text>
    </message>
</messages>
```

`#name` はサーバー名、`#tmin` は残り時間（分）に使用します。

---

## env/ フォルダ -- 動物テリトリー

各動物種がスポーンできる場所を定義するXMLファイルを含みます:

```
env/
  bear_territories.xml
  cattle_territories.xml
  domestic_animals_territories.xml
  fox_territories.xml
  hare_territories.xml
  hen_territories.xml
  pig_territories.xml
  red_deer_territories.xml
  roe_deer_territories.xml
  sheep_goat_territories.xml
  wild_boar_territories.xml
  wolf_territories.xml
  zombie_territories.xml
```

これらのファイルには、マップ全体のテリトリーゾーンを定義する数百の座標ポイントが含まれています。`cfgenvironment.xml` から参照されます。動物やゾンビがスポーンする地理的な位置を変更したい場合以外は、めったに編集する必要はありません。

---

## storage_1/ フォルダ -- パーシステンス

再起動間のサーバーの永続的な状態を保持します:

```
storage_1/
  players.db         # すべてのプレイヤーキャラクターのSQLiteデータベース
  spawnpoints.bin    # バイナリスポーンポイントデータ
  backup/            # パーシステンスデータの自動バックアップ
  data/              # ワールド状態（設置アイテム、建築、車両）
```

**サーバーの実行中に `players.db` を編集しないでください。** サーバープロセスによってロックされたSQLiteデータベースです。キャラクターをワイプする必要がある場合は、まずサーバーを停止してからファイルを削除またはリネームしてください。

**フルパーシステンスワイプ** を行うには、サーバーを停止して `storage_1/` フォルダ全体を削除します。サーバーは次回起動時にフレッシュなワールドで再作成します。

**部分ワイプ**（キャラクターを維持し、ルートをリセット）を行うには:
1. サーバーを停止します
2. `storage_1/data/` 内のファイルを削除しますが、`players.db` は残します
3. 再起動します

---

## トップレベルミッションファイル

### cfgeconomycore.xml

エコノミーのルートクラスを登録し、CEログを設定します:

```xml
<economycore>
    <classes>
        <rootclass name="DefaultWeapon" />
        <rootclass name="DefaultMagazine" />
        <rootclass name="Inventory_Base" />
        <rootclass name="HouseNoDestruct" reportMemoryLOD="no" />
        <rootclass name="SurvivorBase" act="character" reportMemoryLOD="no" />
        <rootclass name="DZ_LightAI" act="character" reportMemoryLOD="no" />
        <rootclass name="CarScript" act="car" reportMemoryLOD="no" />
        <rootclass name="BoatScript" act="car" reportMemoryLOD="no" />
    </classes>
    <defaults>
        <default name="log_ce_loop" value="false"/>
        <default name="log_ce_dynamicevent" value="false"/>
        <default name="log_ce_vehicle" value="false"/>
        <default name="log_ce_lootspawn" value="false"/>
        <default name="log_ce_lootcleanup" value="false"/>
        <default name="log_ce_lootrespawn" value="false"/>
        <default name="log_ce_statistics" value="false"/>
        <default name="log_ce_zombie" value="false"/>
        <default name="log_storageinfo" value="false"/>
        <default name="log_hivewarning" value="true"/>
        <default name="log_missionfilewarning" value="true"/>
        <default name="save_events_startup" value="true"/>
        <default name="save_types_startup" value="true"/>
    </defaults>
</economycore>
```

アイテムスポーンの問題をデバッグする際は、`log_ce_lootspawn` を `"true"` に設定します。CEがどのアイテムをスポーンしようとしているか、なぜ成功または失敗したかの詳細な出力がRPTログに生成されます。

### cfglimitsdefinition.xml

`types.xml` で使用される `<category>`、`<usage>`、`<value>`、`<tag>` 要素の有効な値を定義します:

```xml
<lists>
    <categories>
        <category name="tools"/>
        <category name="containers"/>
        <category name="clothes"/>
        <category name="food"/>
        <category name="weapons"/>
        <category name="books"/>
        <category name="explosives"/>
        <category name="lootdispatch"/>
    </categories>
    <tags>
        <tag name="floor"/>
        <tag name="shelves"/>
        <tag name="ground"/>
    </tags>
    <usageflags>
        <usage name="Military"/>
        <usage name="Police"/>
        <usage name="Medic"/>
        <usage name="Firefighter"/>
        <usage name="Industrial"/>
        <usage name="Farm"/>
        <usage name="Coast"/>
        <usage name="Town"/>
        <usage name="Village"/>
        <usage name="Hunting"/>
        <usage name="Office"/>
        <usage name="School"/>
        <usage name="Prison"/>
        <usage name="Lunapark"/>
        <usage name="SeasonalEvent"/>
        <usage name="ContaminatedArea"/>
        <usage name="Historical"/>
    </usageflags>
    <valueflags>
        <value name="Tier1"/>
        <value name="Tier2"/>
        <value name="Tier3"/>
        <value name="Tier4"/>
        <value name="Unique"/>
    </valueflags>
</lists>
```

`types.xml` でここに定義されていない `<usage>` や `<value>` タグを使用すると、そのアイテムは警告なしにスポーンしません。

### cfgignorelist.xml

ここにリストされたアイテムは、`types.xml` にエントリがあってもエコノミーから完全に除外されます:

```xml
<ignore>
    <type name="Bandage"></type>
    <type name="CattleProd"></type>
    <type name="Defibrillator"></type>
    <type name="HescoBox"></type>
    <type name="StunBaton"></type>
    <type name="TransitBus"></type>
    <type name="Spear"></type>
    <type name="Mag_STANAGCoupled_30Rnd"></type>
    <type name="Wreck_Mi8"></type>
</ignore>
```

これは、ゲームコードに存在するが自然にはスポーンさせたくないアイテム（未完成のアイテム、廃止されたコンテンツ、シーズン外のシーズナルアイテム）に使用されます。

### cfggameplay.json

ゲームプレイパラメータをオーバーライドするJSONファイルです。スタミナ、移動、建築ダメージ、天候、温度、武器の障害物、溺水などを制御します。このファイルはオプションで、存在しない場合はサーバーがデフォルト値を使用します。

### cfgplayerspawnpoints.xml

新規スポーンしたプレイヤーがマップ上のどこに出現するかを、感染者・他のプレイヤー・建物からの距離制約とともに定義します。

### cfgeventspawns.xml

イベント（車両、ヘリクラッシュなど）がスポーンできる正確なワールド座標を含みます。`events.xml` の各イベント名には有効な位置のリストがあります:

```xml
<eventposdef>
    <event name="VehicleCivilianSedan">
        <pos x="12071.933594" z="9129.989258" a="317.953339" />
        <pos x="12302.375001" z="9051.289062" a="60.399284" />
        <pos x="10182.458985" z="1987.5271" a="29.172445" />
        ...
    </event>
</eventposdef>
```

`a` 属性は度数での回転角度です。

---

## 編集すべきファイルと触れてはいけないファイル

| ファイル / フォルダ | 編集可能? | 備考 |
|---------------|:---:|-------|
| `serverDZ.cfg` | はい | メインサーバー設定 |
| `db/types.xml` | はい | アイテムスポーンルール -- 最も一般的な編集対象 |
| `db/globals.xml` | はい | エコノミーチューニングパラメータ |
| `db/events.xml` | はい | 車両/動物スポーンイベント |
| `db/economy.xml` | はい | エコノミーサブシステムトグル |
| `db/messages.xml` | はい | サーバーブロードキャストメッセージ |
| `cfggameplay.json` | はい | ゲームプレイチューニング |
| `cfgspawnabletypes.xml` | はい | アタッチメント/カーゴプリセット |
| `cfgrandompresets.xml` | はい | ルートプール定義 |
| `cfglimitsdefinition.xml` | はい | カスタムusage/valueタグの追加 |
| `cfgplayerspawnpoints.xml` | はい | プレイヤースポーン地点 |
| `cfgeventspawns.xml` | はい | イベントスポーン座標 |
| `cfgignorelist.xml` | はい | エコノミーからアイテムを除外 |
| `cfgweather.xml` | はい | 天候パターン |
| `cfgeffectarea.json` | はい | 汚染ゾーン |
| `init.c` | はい | ミッションエントリスクリプト |
| `addons/` | **いいえ** | アップデート時に上書きされる |
| `dta/` | **いいえ** | コアエンジンデータ |
| `keys/` | 追加のみ | MODの `.bikey` ファイルをここにコピー |
| `storage_1/` | 削除のみ | パーシステンス -- 手動編集しないでください |
| `battleye/` | **いいえ** | アンチチート -- 触れないでください |
| `mapgroup*.xml` | 注意 | 建物ルート位置 -- 上級者向け編集のみ |

---

**前へ:** [サーバーセットアップ](01-server-setup.md) | [ホーム](../README.md) | **次へ:** [serverDZ.cfgリファレンス >>](03-server-cfg.md)
