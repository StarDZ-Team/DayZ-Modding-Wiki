# Chapter 9.12: 上級サーバートピック

[ホーム](../README.md) | [<< 前へ: トラブルシューティング](11-troubleshooting.md) | [Part 9 ホーム](01-server-setup.md)

---

> **概要:** 詳細な設定ファイル、マルチマップセットアップ、エコノミーの分割、動物テリトリー、ダイナミックイベント、天候制御、自動再起動、メッセージシステムについて解説します。

---

## 目次

- [cfggameplay.json 詳解](#cfggameplayjson-詳解)
- [マルチマップサーバー](#マルチマップサーバー)
- [カスタムエコノミーチューニング](#カスタムエコノミーチューニング)
- [cfgenvironment.xmlと動物テリトリー](#cfgenvironmentxmlと動物テリトリー)
- [カスタムダイナミックイベント](#カスタムダイナミックイベント)
- [サーバー再起動の自動化](#サーバー再起動の自動化)
- [cfgweather.xml](#cfgweatherxml)
- [メッセージシステム](#メッセージシステム)

---

## cfggameplay.json 詳解

**cfggameplay.json** ファイルはミッションフォルダにあり、ハードコードされたゲームプレイのデフォルト値をオーバーライドします。まず **serverDZ.cfg** で有効化してください:

```cpp
enableCfgGameplayFile = 1;
```

バニラの構造:

```json
{
  "version": 123,
  "GeneralData": {
    "disableBaseDamage": false,
    "disableContainerDamage": false,
    "disableRespawnDialog": false,
    "disableRespawnInUnconsciousness": false
  },
  "PlayerData": {
    "disablePersonalLight": false,
    "StaminaData": {
      "sprintStaminaModifierErc": 1.0, "sprintStaminaModifierCro": 1.0,
      "staminaWeightLimitThreshold": 6000.0, "staminaMax": 100.0,
      "staminaKg": 0.3, "staminaMin": 0.0,
      "staminaDepletionSpeed": 1.0, "staminaRecoverySpeed": 1.0
    },
    "ShockHandlingData": {
      "shockRefillSpeedConscious": 5.0, "shockRefillSpeedUnconscious": 1.0,
      "allowRefillSpeedModifier": true
    },
    "MovementData": {
      "timeToSprint": 0.45, "timeToJog": 0.0,
      "rotationSpeedJog": 0.3, "rotationSpeedSprint": 0.15
    },
    "DrowningData": {
      "staminaDepletionSpeed": 10.0, "healthDepletionSpeed": 3.0,
      "shockDepletionSpeed": 10.0
    },
    "WeaponObstructionData": { "staticMode": 1, "dynamicMode": 1 }
  },
  "WorldsData": {
    "lightingConfig": 0, "objectSpawnersArr": [],
    "environmentMinTemps": [-3, -2, 0, 4, 9, 14, 18, 17, 13, 11, 9, 0],
    "environmentMaxTemps": [3, 5, 7, 14, 19, 24, 26, 25, 18, 14, 10, 5]
  },
  "BaseBuildingData": { "canBuildAnywhere": false, "canCraftAnywhere": false },
  "UIData": {
    "use3DMap": false,
    "HitIndicationData": {
      "hitDirectionOverrideEnabled": false, "hitDirectionBehaviour": 1,
      "hitDirectionStyle": 0, "hitDirectionIndicatorColorStr": "0xffbb0a1e",
      "hitDirectionMaxDuration": 2.0, "hitDirectionBreakPointRelative": 0.2,
      "hitDirectionScatter": 10.0, "hitIndicationPostProcessEnabled": true
    }
  }
}
```

- `version` -- サーバーバイナリが期待する値と一致する必要があります。変更しないでください。
- `lightingConfig` -- `0`（デフォルト）または `1`（明るい夜）。
- `environmentMinTemps` / `environmentMaxTemps` -- 12個の値、月ごとに1つ（1月〜12月）。
- `disablePersonalLight` -- 夜間の新規プレイヤー近くの微かな周囲光を除去します。
- `staminaMax` とスプリント修飾子は、プレイヤーが疲労するまで走れる距離を制御します。
- `use3DMap` -- ゲーム内マップを地形レンダリングされた3Dバリアントに切り替えます。

---

## マルチマップサーバー

DayZは `mpmissions/` 内の異なるミッションフォルダを通じて複数のマップをサポートします:

| マップ | ミッションフォルダ |
|-----|---------------|
| チェルナルス | `mpmissions/dayzOffline.chernarusplus/` |
| リヴォニア | `mpmissions/dayzOffline.enoch/` |
| サハル | `mpmissions/dayzOffline.sakhal/` |

各マップには独自のCEファイル（`types.xml`、`events.xml` など）があります。**serverDZ.cfg** の `template` でマップを切り替えます:

```cpp
class Missions {
    class DayZ {
        template = "dayzOffline.chernarusplus";
    };
};
```

または起動パラメータで: `-mission=mpmissions/dayzOffline.enoch`

複数のマップを同時に実行するには、それぞれ独自の設定、プロファイルディレクトリ、ポート範囲を持つ別々のサーバーインスタンスを使用してください。

---

## カスタムエコノミーチューニング

### types.xmlの分割

アイテムを複数のファイルに分割し、**cfgeconomycore.xml** に登録します:

```xml
<economycore>
    <ce folder="db">
        <file name="types.xml" type="types" />
        <file name="types_weapons.xml" type="types" />
        <file name="types_vehicles.xml" type="types" />
    </ce>
</economycore>
```

サーバーは `type="types"` のすべてのファイルをロードしてマージします。

### カスタムカテゴリとタグ

**cfglimitsdefinition.xml** は `types.xml` 用のカテゴリ/タグを定義しますが、アップデート時に上書きされます。代わりに **cfglimitsdefinitionuser.xml** を使用してください:

```xml
<lists>
    <categories>
        <category name="custom_rare" />
    </categories>
    <tags>
        <tag name="custom_event" />
    </tags>
</lists>
```

---

## cfgenvironment.xmlと動物テリトリー

ミッションフォルダ内の **cfgenvironment.xml** ファイルは `env/` サブディレクトリのテリトリーファイルにリンクします:

```xml
<env>
    <territories>
        <file path="env/zombie_territories.xml" />
        <file path="env/bear_territories.xml" />
        <file path="env/wolf_territories.xml" />
    </territories>
</env>
```

`env/` フォルダには以下の動物テリトリーファイルが含まれています:

| ファイル | 動物 |
|------|---------|
| **bear_territories.xml** | ヒグマ |
| **wolf_territories.xml** | オオカミの群れ |
| **fox_territories.xml** | キツネ |
| **hare_territories.xml** | ウサギ/ノウサギ |
| **hen_territories.xml** | ニワトリ |
| **pig_territories.xml** | ブタ |
| **red_deer_territories.xml** | アカシカ |
| **roe_deer_territories.xml** | ノロジカ |
| **sheep_goat_territories.xml** | ヒツジ/ヤギ |
| **wild_boar_territories.xml** | イノシシ |
| **cattle_territories.xml** | ウシ |

テリトリーエントリは位置と動物数を持つ円形ゾーンを定義します:

```xml
<territory color="4291543295" name="BearTerritory 001">
    <zone name="Bear zone" smin="-1" smax="-1" dmin="1" dmax="4" x="7628" z="5048" r="500" />
</territory>
```

- `x`, `z` -- 中心座標、`r` -- 半径（メートル）
- `dmin`, `dmax` -- ゾーン内の最小/最大動物数
- `smin`, `smax` -- 予約済み（`-1` に設定）

---

## カスタムダイナミックイベント

ダイナミックイベント（ヘリクラッシュ、護送車列）は **events.xml** で定義されます。カスタムイベントを作成するには:

**1. events.xmlでイベントを定義します:**

```xml
<event name="StaticMyCustomCrash">
    <nominal>3</nominal> <min>1</min> <max>5</max>
    <lifetime>1800</lifetime> <restock>600</restock>
    <saferadius>500</saferadius> <distanceradius>200</distanceradius> <cleanupradius>100</cleanupradius>
    <flags deletable="0" init_random="0" remove_damaged="1" />
    <position>fixed</position> <limit>child</limit> <active>1</active>
    <children>
        <child lootmax="10" lootmin="5" max="3" min="1" type="Wreck_Mi8_Crashed" />
    </children>
</event>
```

**2. cfgeventspawns.xmlにスポーン位置を追加します:**

```xml
<event name="StaticMyCustomCrash">
    <pos x="4523.2" z="9234.5" a="180" />
    <pos x="7812.1" z="3401.8" a="90" />
</event>
```

**3. 感染者ガードを追加します**（オプション） -- イベント定義に `<secondary type="ZmbM_PatrolNormal_Autumn" />` 要素を追加します。

**4. グループスポーン**（オプション） -- **cfgeventgroups.xml** でクラスタを定義し、イベントでグループ名を参照します。

---

## サーバー再起動の自動化

DayZには組み込みの再起動スケジューラがありません。OSレベルの自動化を使用してください。

### Windows

**restart_server.bat** を作成し、Windowsのタスクスケジューラで4-6時間ごとに実行します:

```batch
@echo off
taskkill /f /im DayZServer_x64.exe
timeout /t 10
xcopy /e /y "C:\DayZServer\profiles\storage_1" "C:\DayZBackups\%date:~-4%-%date:~-7,2%-%date:~-10,2%\"
C:\SteamCMD\steamcmd.exe +force_install_dir C:\DayZServer +login anonymous +app_update 223350 validate +quit
start "" "C:\DayZServer\DayZServer_x64.exe" -config=serverDZ.cfg -profiles=profiles -port=2302
```

### Linux

シェルスクリプトを作成し、cronに追加します（`0 */4 * * *`）:

```bash
#!/bin/bash
kill $(pidof DayZServer) && sleep 15
cp -r /home/dayz/server/profiles/storage_1 /home/dayz/backups/$(date +%F_%H%M)_storage_1
/home/dayz/steamcmd/steamcmd.sh +force_install_dir /home/dayz/server +login anonymous +app_update 223350 validate +quit
cd /home/dayz/server && ./DayZServer -config=serverDZ.cfg -profiles=profiles -port=2302 &
```

各再起動前に必ず `storage_1/` をバックアップしてください。シャットダウン中のパーシステンス破損は、プレイヤーの拠点と車両をワイプする可能性があります。

---

## cfgweather.xml

ミッションフォルダ内の **cfgweather.xml** ファイルは天候パターンを制御します。各マップには独自のデフォルトが付属しています:

各気象現象には `min`、`max`、`duration_min`、`duration_max`（秒）があります:

| 気象現象 | デフォルトMin | デフォルトMax | 備考 |
|------------|-------------|-------------|-------|
| `overcast` | 0.0 | 1.0 | 雲の密度と雨の確率を駆動します |
| `rain` | 0.0 | 1.0 | 曇りのしきい値を超えた場合にのみ発生します。雨なしにするにはmaxを `0.0` に設定 |
| `fog` | 0.0 | 0.3 | `0.5` を超える値はほぼゼロの視界になります |
| `wind_magnitude` | 0.0 | 18.0 | 弾道とプレイヤーの移動に影響します |

---

## メッセージシステム

ミッションフォルダ内の **db/messages.xml** ファイルはスケジュールされたサーバーメッセージとシャットダウン警告を制御します:

```xml
<messages>
    <message deadline="0" shutdown="0"><text>Welcome to our server!</text></message>
    <message deadline="240" shutdown="1"><text>Server restart in 4 minutes!</text></message>
    <message deadline="60" shutdown="1"><text>Server restart in 1 minute!</text></message>
    <message deadline="0" shutdown="1"><text>Server is restarting now.</text></message>
</messages>
```

- `deadline` -- メッセージがトリガーされるまでの分数（シャットダウンメッセージの場合、サーバーが停止するまでの分数）
- `shutdown` -- `1` はシャットダウンシーケンスメッセージ、`0` は通常のブロードキャスト

メッセージシステムはサーバーを再起動しません。外部で再起動スケジュールが設定されている場合にのみ警告を表示します。

---

[ホーム](../README.md) | [<< 前へ: トラブルシューティング](11-troubleshooting.md) | [Part 9 ホーム](01-server-setup.md)
