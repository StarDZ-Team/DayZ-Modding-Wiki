# Chapter 9.5: 車両とダイナミックイベントスポーン

[ホーム](../README.md) | [<< 前へ: ルートエコノミー](04-loot-economy.md) | [次へ: プレイヤースポーン >>](06-player-spawning.md)

---

> **概要:** 車両とダイナミックイベント（ヘリクラッシュ、護送車列、パトカー）は `types.xml` を使用 **しません**。3つのファイルからなる個別のシステムを使用します: `events.xml` が何をいくつスポーンするかを定義し、`cfgeventspawns.xml` がどこにスポーンするかを定義し、`cfgeventgroups.xml` がグループ化されたフォーメーションを定義します。この章では3つのファイルすべてをバニラの実際の値で解説します。

---

## 目次

- [車両スポーンの仕組み](#車両スポーンの仕組み)
- [events.xmlの車両エントリ](#eventsxmlの車両エントリ)
- [車両イベントフィールドリファレンス](#車両イベントフィールドリファレンス)
- [cfgeventspawns.xml -- スポーン位置](#cfgeventspawnsxml----スポーン位置)
- [ヘリクラッシュイベント](#ヘリクラッシュイベント)
- [軍事護送車列](#軍事護送車列)
- [パトカー](#パトカー)
- [cfgeventgroups.xml -- グループスポーン](#cfgeventgroupsxml----グループスポーン)
- [cfgeconomycore.xmlの車両ルートクラス](#cfgeconomycorexmlの車両ルートクラス)
- [よくある間違い](#よくある間違い)

---

## 車両スポーンの仕組み

車両は `types.xml` では定義 **されません**。車両クラスを `types.xml` に追加しても、スポーンしません。車両は専用の3ファイルパイプラインを使用します:

1. **`events.xml`** -- 各車両イベントを定義します: マップ上に存在すべき数（nominal）、スポーン可能なバリアント（children）、ライフタイムやセーフ半径などの動作フラグ。

2. **`cfgeventspawns.xml`** -- 車両イベントがエンティティを配置できる物理的なワールド位置を定義します。各イベント名はx, z座標と角度を持つ `<pos>` エントリのリストにマッピングされます。

3. **`cfgeventgroups.xml`** -- 複数のオブジェクトが相対的な位置オフセットで一緒にスポーンするグループスポーンを定義します（例: 列車の残骸）。

CEは `events.xml` を読み取り、スポーンが必要なイベントを選択し、`cfgeventspawns.xml` で一致する位置を検索し、`saferadius` と `distanceradius` の制約を満たすものをランダムに選択し、その位置にランダムに選択された子エンティティをスポーンさせます。

3つのファイルはすべて `mpmissions/<your_mission>/db/` にあります。

---

## events.xmlの車両エントリ

すべてのバニラ車両タイプにはそれぞれのイベントエントリがあります。以下は実際の値を含むすべてのエントリです:

### シビリアンセダン

```xml
<event name="VehicleCivilianSedan">
    <nominal>8</nominal>
    <min>5</min>
    <max>11</max>
    <lifetime>300</lifetime>
    <restock>0</restock>
    <saferadius>500</saferadius>
    <distanceradius>500</distanceradius>
    <cleanupradius>200</cleanupradius>
    <flags deletable="0" init_random="0" remove_damaged="1"/>
    <position>fixed</position>
    <limit>mixed</limit>
    <active>1</active>
    <children>
        <child lootmax="0" lootmin="0" max="5" min="3" type="CivilianSedan"/>
        <child lootmax="0" lootmin="0" max="5" min="3" type="CivilianSedan_Black"/>
        <child lootmax="0" lootmin="0" max="5" min="3" type="CivilianSedan_Wine"/>
    </children>
</event>
```

### すべてのバニラ車両イベント

すべての車両イベントは上記のセダンと同じ構造を使用します。値のみ異なります:

| イベント名 | Nominal | Min | Max | Lifetime | 子要素（バリアント） |
|------------|---------|-----|-----|----------|---------------------|
| `VehicleCivilianSedan` | 8 | 5 | 11 | 300 | `CivilianSedan`, `_Black`, `_Wine` |
| `VehicleOffroadHatchback` | 8 | 5 | 11 | 300 | `OffroadHatchback`, `_Blue`, `_White` |
| `VehicleHatchback02` | 8 | 5 | 11 | 300 | Hatchback02バリアント |
| `VehicleSedan02` | 8 | 5 | 11 | 300 | Sedan02バリアント |
| `VehicleTruck01` | 8 | 5 | 11 | 300 | V3Sトラックバリアント |
| `VehicleOffroad02` | 3 | 2 | 3 | 300 | Gunter -- スポーン数が少ない |
| `VehicleBoat` | 22 | 18 | 24 | 600 | ボート -- 最多数、長いライフタイム |

`VehicleOffroad02` は他の陸上車両（8）よりも低いnominal（3）を持っています。`VehicleBoat` は最高のnominal（22）と長いライフタイム（600 vs 300）の両方を持っています。

---

## 車両イベントフィールドリファレンス

### イベントレベルのフィールド

| フィールド | 型 | 説明 |
|-------|------|-------------|
| `name` | string | イベント識別子です。`position="fixed"` の場合、`cfgeventspawns.xml` のエントリと一致する必要があります。 |
| `nominal` | int | マップ上のこのイベントのアクティブインスタンスのターゲット数です。 |
| `min` | int | カウントがこれを下回った時、CEはさらにスポーンを試みます。 |
| `max` | int | ハード上限です。CEはこのカウントを超えません。 |
| `lifetime` | int | リスポーンチェック間の秒数です。車両の場合、これは車両のパーシステンスライフタイムではなく、CEが生成またはクリーンアップするかどうかを再評価する間隔です。 |
| `restock` | int | リスポーン試行間の最小秒数です。0 = 次のサイクル。 |
| `saferadius` | int | イベントがスポーンするためのプレイヤーからの最小距離（メートル）です。プレイヤーの前に車両が出現するのを防ぎます。 |
| `distanceradius` | int | 同じイベントの2つのインスタンス間の最小距離（メートル）です。2台のセダンが隣り合ってスポーンするのを防ぎます。 |
| `cleanupradius` | int | プレイヤーがこの距離（メートル）以内にいる場合、イベントエンティティはクリーンアップから保護されます。 |

### フラグ

| フラグ | 値 | 説明 |
|------|--------|-------------|
| `deletable` | 0, 1 | CEがこのイベントエンティティを削除できるかどうかです。車両は0（CEによる削除不可）を使用します。 |
| `init_random` | 0, 1 | 初回スポーン時に初期位置をランダマイズします。0 = `cfgeventspawns.xml` の固定位置を使用。 |
| `remove_damaged` | 0, 1 | エンティティが破壊された時に削除します。**車両には重要です** -- [よくある間違い](#よくある間違い) を参照してください。 |

### その他のフィールド

| フィールド | 値 | 説明 |
|-------|--------|-------------|
| `position` | `fixed`, `player` | `fixed` = `cfgeventspawns.xml` の位置にスポーン。`player` = プレイヤーの位置に対してスポーン。 |
| `limit` | `child`, `mixed`, `custom` | `child` = 子タイプごとにmin/maxを適用。`mixed` = すべての子にわたってmin/maxを共有。`custom` = エンジン固有の動作。 |
| `active` | 0, 1 | このイベントを有効または無効にします。0 = イベントは完全にスキップされます。 |

### 子要素のフィールド

| 属性 | 説明 |
|-----------|-------------|
| `type` | スポーンするエンティティのクラス名です。 |
| `min` | このバリアントの最小インスタンス数です。 |
| `max` | このバリアントの最大インスタンス数です。 |
| `lootmin` | エンティティ内/周囲にスポーンされるルートアイテムの最小数です。車両は0（パーツは `cfgspawnabletypes.xml` から来ます）。 |
| `lootmax` | ルートアイテムの最大数です。ヘリクラッシュやダイナミックイベントで使用され、車両では使用されません。 |

---

## cfgeventspawns.xml -- スポーン位置

このファイルはイベント名をワールド座標にマッピングします。各 `<event>` ブロックには、そのイベントタイプの有効なスポーン位置のリストが含まれます。CEが車両をスポーンする必要がある場合、このリストから `saferadius` と `distanceradius` の制約を満たすランダムな位置を選択します。

```xml
<event name="VehicleCivilianSedan">
    <pos x="4509.1" z="9321.5" a="172"/>
    <pos x="6283.7" z="2468.3" a="90"/>
    <pos x="11447.2" z="11203.8" a="45"/>
    <pos x="2961.4" z="5107.6" a="0"/>
    <!-- ... さらに多くの位置 ... -->
</event>
```

各 `<pos>` には3つの属性があります:

| 属性 | 説明 |
|-----------|-------------|
| `x` | ワールドX座標（マップ上の東西位置）です。 |
| `z` | ワールドZ座標（マップ上の南北位置）です。 |
| `a` | 度数での角度（0-360）です。スポーン時の車両の向きです。 |

**重要なルール:**

- イベントに `cfgeventspawns.xml` で一致する `<event>` ブロックがない場合、`events.xml` の設定に関係なく **スポーンしません**。
- `nominal` 値以上の `<pos>` エントリが必要です。`nominal=8` に設定しても3つの位置しかない場合、3台しかスポーンできません。
- 位置は道路または平坦な地面上にあるべきです。建物内や急な地形上の位置は、車両が埋まったり転覆したりしてスポーンする原因になります。
- `a`（角度）値は車両の向きを決定します。自然に見えるスポーンのために道路の方向と合わせてください。

---

## ヘリクラッシュイベント

ヘリコプタークラッシュは、軍事ルートと周囲の感染者を伴う残骸をスポーンするダイナミックイベントです。`<secondary>` タグを使用してクラッシュサイト周辺のゾンビスポーンを定義します。

```xml
<event name="StaticHeliCrash">
    <nominal>3</nominal>
    <min>1</min>
    <max>3</max>
    <lifetime>2100</lifetime>
    <restock>0</restock>
    <saferadius>1000</saferadius>
    <distanceradius>500</distanceradius>
    <cleanupradius>200</cleanupradius>
    <secondary>InfectedArmy</secondary>
    <flags deletable="1" init_random="0" remove_damaged="0"/>
    <position>fixed</position>
    <limit>mixed</limit>
    <active>1</active>
    <children>
        <child lootmax="15" lootmin="10" max="3" min="1" type="Wreck_UH1Y"/>
    </children>
</event>
```

### 車両イベントとの主な違い

- **`<secondary>InfectedArmy</secondary>`** -- クラッシュサイト周辺に軍事ゾンビをスポーンさせます。このタグはCEが周辺に配置する感染者スポーングループを参照します。
- **`lootmin="10"` / `lootmax="15"`** -- 残骸は10-15個のダイナミックイベントルートアイテムと共にスポーンします。これらは `types.xml` で `deloot="1"` フラグが付いたアイテム（軍事装備、レア武器）です。
- **`lifetime=2100`** -- クラッシュは35分間持続した後、CEがクリーンアップして別の場所に新しいものをスポーンします。
- **`saferadius=1000`** -- クラッシュはプレイヤーから1 km以内には出現しません。
- **`remove_damaged=0`** -- 残骸は定義上すでに「損傷」しているため、これは0でなければなりません。そうでないと即座にクリーンアップされます。

---

## 軍事護送車列

軍事護送車列は、軍事ルートと感染者の護衛と共にスポーンする静的な破壊された車両グループです。

```xml
<event name="StaticMilitaryConvoy">
    <nominal>5</nominal>
    <min>3</min>
    <max>5</max>
    <lifetime>1800</lifetime>
    <restock>0</restock>
    <saferadius>1000</saferadius>
    <distanceradius>500</distanceradius>
    <cleanupradius>200</cleanupradius>
    <secondary>InfectedArmy</secondary>
    <flags deletable="1" init_random="0" remove_damaged="0"/>
    <position>fixed</position>
    <limit>mixed</limit>
    <active>1</active>
    <children>
        <child lootmax="10" lootmin="5" max="5" min="3" type="Wreck_V3S"/>
    </children>
</event>
```

護送車列はヘリクラッシュと同一の動作をします: `<secondary>` タグがサイト周辺に `InfectedArmy` をスポーンし、`deloot="1"` のルートアイテムが残骸上に出現します。`nominal=5` で、マップ上に最大5つの護送車列サイトが同時に存在します。各サイトは1800秒（30分）持続した後、新しい場所にサイクルします。

---

## パトカー

パトカーイベントは、近くに警察タイプの感染者を伴う破壊された警察車両をスポーンします。**デフォルトでは無効になっています。**

```xml
<event name="StaticPoliceCar">
    <nominal>10</nominal>
    <min>5</min>
    <max>10</max>
    <lifetime>2500</lifetime>
    <restock>0</restock>
    <saferadius>500</saferadius>
    <distanceradius>200</distanceradius>
    <cleanupradius>100</cleanupradius>
    <secondary>InfectedPoliceHard</secondary>
    <flags deletable="1" init_random="0" remove_damaged="0"/>
    <position>fixed</position>
    <limit>mixed</limit>
    <active>0</active>
    <children>
        <child lootmax="5" lootmin="3" max="10" min="5" type="Wreck_PoliceCar"/>
    </children>
</event>
```

**`active=0`** はこのイベントがデフォルトで無効であることを意味します -- 有効にするには `1` に変更してください。`<secondary>InfectedPoliceHard</secondary>` タグはハードバリアントの警察ゾンビ（通常の感染者より強い）をスポーンします。`nominal=10` と `saferadius=500` で、パトカーはヘリクラッシュよりも多数ですが価値は低いです。

---

## cfgeventgroups.xml -- グループスポーン

このファイルは、複数のオブジェクトが相対的な位置オフセットで一緒にスポーンするイベントを定義します。最も一般的な使用例は放棄された列車です。

```xml
<event name="Train_Abandoned_Cherno">
    <children>
        <child type="Land_Train_Wagon_Tanker_Blue" x="0" z="0" a="0"/>
        <child type="Land_Train_Wagon_Box_Brown" x="0" z="15" a="0"/>
        <child type="Land_Train_Wagon_Flatbed_Green" x="0" z="30" a="0"/>
        <child type="Land_Train_Engine_Blue" x="0" z="45" a="0"/>
    </children>
</event>
```

最初の子要素は `cfgeventspawns.xml` の位置に配置されます。以降の子要素はその原点からの `x`、`z`、`a` 値でオフセットされます。この例では、列車の車両がz軸に沿って15メートル間隔で配置されています。

グループ内の各 `<child>` には以下があります:

| 属性 | 説明 |
|-----------|-------------|
| `type` | スポーンするオブジェクトのクラス名です。 |
| `x` | グループ原点からのXオフセット（メートル）です。 |
| `z` | グループ原点からのZオフセット（メートル）です。 |
| `a` | グループ原点からの角度オフセット（度）です。 |

グループイベント自体も、nominal数、ライフタイム、アクティブ状態を制御する `events.xml` の対応するエントリが必要です。

---

## cfgeconomycore.xmlの車両ルートクラス

CEが車両を追跡可能なエンティティとして認識するためには、`cfgeconomycore.xml` にルートクラス宣言が必要です:

```xml
<economycore>
    <classes>
        <rootclass name="CarScript" act="car"/>
        <rootclass name="BoatScript" act="car"/>
    </classes>
</economycore>
```

- **`CarScript`** はDayZのすべての陸上車両の基底クラスです。
- **`BoatScript`** はすべてのボートの基底クラスです。
- `act="car"` 属性は、これらのエンティティを車両固有の動作（パーシステンス、イベントベースのスポーン）で扱うようCEに指示します。

これらのルートクラスエントリがなければ、CEは車両インスタンスを追跡または管理しません。別の基底クラスを継承するMOD車両を追加する場合、ここにそのルートクラスを追加する必要がある場合があります。

---

## よくある間違い

これらはサーバー管理者が最も頻繁に遭遇する車両スポーンの問題です。

### types.xmlに車両を入れる

**問題:** `CivilianSedan` を `types.xml` にnominal 10で追加します。セダンはスポーンしません。

**対処法:** `types.xml` から車両を削除します。`events.xml` で適切な子要素を持つ車両イベントを追加または編集し、`cfgeventspawns.xml` に一致するスポーン位置が存在することを確認します。車両はアイテムスポーンシステムではなくイベントシステムを使用します。

### cfgeventspawns.xmlに一致するスポーン位置がない

**問題:** `events.xml` に新しい車両イベントを作成しますが、車両が出現しません。

**対処法:** `cfgeventspawns.xml` に十分な `<pos>` エントリを持つ一致する `<event name="YourEventName">` ブロックを追加します。両方のファイルのイベント `name` は正確に一致する必要があります。`nominal` 値以上の位置が必要です。

### 走行可能な車両にremove_damaged=0を設定する

**問題:** 車両イベントに `remove_damaged="0"` を設定します。時間が経つと、サーバーは決してデスポーンしない破壊された車両で溢れ、スポーン位置をブロックしパフォーマンスが低下します。

**対処法:** すべての走行可能な車両（セダン、トラック、ハッチバック、ボート）では `remove_damaged="1"` を維持してください。これにより、車両が破壊された時にCEがそれを削除し、新しいものをスポーンさせます。`remove_damaged="0"` は、設計上すでに損傷している残骸オブジェクト（ヘリクラッシュ、護送車列）にのみ設定してください。

### active=1の設定を忘れる

**問題:** 車両イベントを設定しますがスポーンしません。

**対処法:** `<active>` タグを確認してください。`0` に設定されている場合、イベントは無効です。`StaticPoliceCar` のような一部のバニライベントは `active=0` で出荷されています。スポーンを有効にするには `1` に設定してください。

### nominal数に対してスポーン位置が不足

**問題:** 車両イベントに `nominal=15` を設定しますが、`cfgeventspawns.xml` に6つの位置しかありません。6台の車両しかスポーンしません。

**対処法:** さらに `<pos>` エントリを追加します。原則として、CEが `saferadius` と `distanceradius` の制約を満たすための十分なオプションを持てるように、nominal値の少なくとも2-3倍の位置を含めてください。

### 車両が建物の中や地下にスポーンする

**問題:** 車両が建物にクリッピングしたり、地形に埋まってスポーンします。

**対処法:** `cfgeventspawns.xml` の `<pos>` 座標を確認してください。ファイルに追加する前に、管理者テレポートを使用してゲーム内で位置をテストしてください。位置は平坦な道路や開けた地面上にあるべきで、角度（`a`）は道路の方向と合わせてください。

---

[ホーム](../README.md) | [<< 前へ: ルートエコノミー](04-loot-economy.md) | [次へ: プレイヤースポーン >>](06-player-spawning.md)
