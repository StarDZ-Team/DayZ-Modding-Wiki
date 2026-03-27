# Chapter 9.1: サーバーセットアップと初回起動

[ホーム](../README.md) | **サーバーセットアップ** | [次へ: ディレクトリ構造 >>](02-directory-structure.md)

---

> **概要:** SteamCMDを使用してDayZ Standalone専用サーバーをゼロからインストールし、最小限の設定で起動し、サーバーブラウザに表示されることを確認してプレイヤーとして接続します。この章では、ハードウェア要件から最も一般的な初回起動時の障害の修正まですべてを解説します。

---

## 目次

- [前提条件](#前提条件)
- [SteamCMDのインストール](#steamcmdのインストール)
- [DayZ Serverのインストール](#dayz-serverのインストール)
- [インストール後のディレクトリ](#インストール後のディレクトリ)
- [最小構成での初回起動](#最小構成での初回起動)
- [サーバーの動作確認](#サーバーの動作確認)
- [プレイヤーとして接続する](#プレイヤーとして接続する)
- [初回起動時のよくある問題](#初回起動時のよくある問題)

---

## 前提条件

### ハードウェア

| コンポーネント | 最小要件 | 推奨 |
|-----------|---------|-------------|
| CPU | 4コア、2.4 GHz | 6コア以上、3.5 GHz |
| RAM | 8 GB | 16 GB |
| ディスク | 20 GB SSD | 40 GB NVMe SSD |
| ネットワーク | 10 Mbps アップロード | 50+ Mbps アップロード |
| OS | Windows Server 2016 / Ubuntu 20.04 | Windows Server 2022 / Ubuntu 22.04 |

DayZ Serverのゲームプレイロジックはシングルスレッドです。コア数よりもクロック速度が重要です。

### ソフトウェア

- **SteamCMD** -- 専用サーバーをインストールするためのSteamコマンドラインクライアント
- **Visual C++ Redistributable 2019** (Windows) -- `DayZServer_x64.exe` に必要です
- **DirectX Runtime** (Windows) -- 通常はすでにインストール済みです
- ポート **2302-2305 UDP** をルーター/ファイアウォールで転送する必要があります

---

## SteamCMDのインストール

### Windows

1. https://developer.valvesoftware.com/wiki/SteamCMD からSteamCMDをダウンロードします
2. `steamcmd.exe` を固定のフォルダに展開します（例: `C:\SteamCMD\`）
3. `steamcmd.exe` を一度実行します -- 自動的にアップデートされます

### Linux

```bash
sudo add-apt-repository multiverse
sudo dpkg --add-architecture i386
sudo apt update
sudo apt install steamcmd
```

---

## DayZ Serverのインストール

DayZ ServerのSteam App IDは **223350** です。DayZを所有するSteamアカウントにログインせずにインストールできます。

### ワンライナーインストール (Windows)

```batch
C:\SteamCMD\steamcmd.exe +force_install_dir "C:\DayZServer" +login anonymous +app_update 223350 validate +quit
```

### ワンライナーインストール (Linux)

```bash
steamcmd +force_install_dir /home/dayz/server +login anonymous +app_update 223350 validate +quit
```

### アップデートスクリプト

パッチがリリースされた際に再実行できるスクリプトを作成します:

```batch
@echo off
C:\SteamCMD\steamcmd.exe ^
  +force_install_dir "C:\DayZServer" ^
  +login anonymous ^
  +app_update 223350 validate ^
  +quit
echo Update complete.
pause
```

`validate` フラグはすべてのファイルの破損をチェックします。新規インストールの場合、2〜3 GBのダウンロードが必要です。

---

## インストール後のディレクトリ

インストール後、サーバーのルートは次のようになります:

```
DayZServer/
  DayZServer_x64.exe        # サーバー実行ファイル
  serverDZ.cfg               # メインサーバー設定ファイル
  dayzsetting.xml            # レンダリング/ビデオ設定（専用サーバーでは不要）
  addons/                    # バニラPBOファイル（ai.pbo、animals.pboなど）
  battleye/                  # BattlEyeアンチチート（BEServer_x64.dll）
  dta/                       # コアエンジンデータ（bin.pbo、scripts.pbo、gui.pbo）
  keys/                      # 署名キー（バニラ用のdayz.bikey）
  logs/                      # エンジンログ（接続、コンテンツ、オーディオ）
  mpmissions/                # ミッションフォルダ
    dayzOffline.chernarusplus/   # チェルナルス ミッション
    dayzOffline.enoch/           # リヴォニア ミッション（DLC）
    dayzOffline.sakhal/          # サハル ミッション（DLC）
  profiles/                  # ランタイム出力: RPTログ、スクリプトログ、プレイヤーDB
  ban.txt                    # BAN済みプレイヤーリスト（Steam64 ID）
  whitelist.txt              # ホワイトリスト登録プレイヤー（Steam64 ID）
  steam_appid.txt            # "221100" を含む
```

重要なポイント:
- **編集するファイル:** `serverDZ.cfg` と `mpmissions/` 内のファイル。
- **編集してはいけないファイル:** `addons/` や `dta/` 内のファイル -- アップデートのたびに上書きされます。
- **MODのPBO** はサーバールートまたはサブフォルダに配置します（後の章で解説します）。
- **`profiles/`** は初回起動時に作成され、スクリプトログとクラッシュダンプが格納されます。

---

## 最小構成での初回起動

### ステップ1: serverDZ.cfgの編集

`serverDZ.cfg` をテキストエディタで開きます。初回テストでは、最もシンプルな設定を使用します:

```cpp
hostname = "My Test Server";
password = "";
passwordAdmin = "changeme123";
maxPlayers = 10;
verifySignatures = 2;
forceSameBuild = 1;
disableVoN = 0;
vonCodecQuality = 20;
disable3rdPerson = 0;
disableCrosshair = 0;
disablePersonalLight = 1;
lightingConfig = 0;
serverTime = "SystemTime";
serverTimeAcceleration = 12;
serverNightTimeAcceleration = 4;
serverTimePersistent = 0;
guaranteedUpdates = 1;
loginQueueConcurrentPlayers = 5;
loginQueueMaxPlayers = 500;
instanceId = 1;
storageAutoFix = 1;

class Missions
{
    class DayZ
    {
        template = "dayzOffline.chernarusplus";
    };
};
```

### ステップ2: サーバーの起動

サーバーディレクトリでコマンドプロンプトを開き、以下を実行します:

```batch
DayZServer_x64.exe -config=serverDZ.cfg -port=2302 -profiles=profiles -dologs -adminlog -netlog -freezecheck
```

| フラグ | 目的 |
|------|---------|
| `-config=serverDZ.cfg` | 設定ファイルへのパス |
| `-port=2302` | メインゲームポート（2303-2305も使用） |
| `-profiles=profiles` | ログとプレイヤーデータの出力フォルダ |
| `-dologs` | サーバーログを有効にする |
| `-adminlog` | 管理者アクションのログを記録 |
| `-netlog` | ネットワークイベントのログを記録 |
| `-freezecheck` | フリーズ検出時の自動再起動 |

### ステップ3: 初期化の完了を待つ

サーバーの完全な起動には30〜90秒かかります。コンソール出力を確認してください。以下のような行が表示されたら:

```
BattlEye Server: Initialized (v1.xxx)
```

...サーバーは接続の準備ができています。

---

## サーバーの動作確認

### 方法1: スクリプトログ

`profiles/` 内で `script_YYYY-MM-DD_HH-MM-SS.log` というファイルを確認します。開いて以下を探します:

```
SCRIPT       : ...creatingass. world
SCRIPT       : ...creating mission
```

これらの行はエコノミーが初期化され、ミッションがロードされたことを確認するものです。

### 方法2: RPTファイル

`profiles/` 内の `.RPT` ファイルはエンジンレベルの出力を表示します。以下を探します:

```
Dedicated host created.
BattlEye Server: Initialized
```

### 方法3: Steamサーバーブラウザ

Steamを開き、**表示 > ゲームサーバー > お気に入り** に移動し、**サーバーを追加** をクリックして `127.0.0.1:2302`（またはパブリックIP）を入力し、**このアドレスでゲームを検索** をクリックします。サーバーが表示されれば、動作しておりアクセス可能です。

### 方法4: クエリポート

https://www.battlemetrics.com/ などの外部ツールや `gamedig` npmパッケージを使用して、ポート27016（Steamクエリポート = ゲームポート + 24714）にクエリを送信します。

---

## プレイヤーとして接続する

### 同じマシンから

1. DayZ（DayZ Serverではなく、通常のゲームクライアント）を起動します
2. **サーバーブラウザ** を開きます
3. **LAN** タブまたは **お気に入り** タブに移動します
4. `127.0.0.1:2302` をお気に入りに追加します
5. **接続** をクリックします

クライアントとサーバーを同じマシンで実行する場合は、製品版クライアントの代わりに `DayZDiag_x64.exe`（診断クライアント）を使用します。以下のように起動します:

```batch
"C:\Program Files (x86)\Steam\steamapps\common\DayZ\DayZDiag_x64.exe" -connect=127.0.0.1 -port=2302
```

### 別のマシンから

クライアントが同じネットワーク上にあるかどうかに応じて、サーバーの **パブリックIP** または **LAN IP** を使用します。ポート2302-2305 UDPの転送が必要です。

---

## 初回起動時のよくある問題

### サーバーが起動後すぐに閉じる

**原因:** Visual C++ Redistributableが不足しているか、`serverDZ.cfg` に構文エラーがあります。

**対処法:** VC++ Redist 2019 (x64) をインストールします。`serverDZ.cfg` でセミコロンの不足を確認してください -- すべてのパラメータ行は `;` で終わる必要があります。

### "BattlEye initialization failed"

**原因:** `battleye/` フォルダが存在しないか、アンチウイルスソフトが `BEServer_x64.dll` をブロックしています。

**対処法:** SteamCMD経由でサーバーファイルを再検証します。サーバーフォルダ全体をアンチウイルスの除外対象に追加します。

### サーバーは動作しているがブラウザに表示されない

**原因:** ポートが転送されていないか、WindowsファイアウォールがEXEをブロックしています。

**対処法:**
1. `DayZServer_x64.exe` に対するWindowsファイアウォールの受信ルールを追加します（すべてのUDPを許可）
2. ルーターでポート **2302-2305 UDP** を転送します
3. 外部ポートチェッカーでパブリックIPの2302 UDPが開いていることを確認します

### 接続時に「Version Mismatch」

**原因:** サーバーとクライアントのバージョンが異なっています。

**対処法:** 両方をアップデートします。サーバーにはSteamCMDのアップデートコマンドを実行します。クライアントはSteam経由で自動的にアップデートされます。

### ルートがスポーンしない

**原因:** `init.c` ファイルが存在しないか、Hiveの初期化に失敗しています。

**対処法:** `mpmissions/dayzOffline.chernarusplus/init.c` が存在し、`CreateHive()` を含んでいることを確認します。スクリプトログでエラーを確認してください。

### サーバーがCPU1コアを100%使用する

これは正常です。DayZ Serverはシングルスレッドです。同じコアで複数のサーバーインスタンスを実行しないでください -- プロセッサアフィニティを使用するか、別のマシンを使用してください。

### プレイヤーがカラスとしてスポーンする / ロード画面で停止する

**原因:** `serverDZ.cfg` のミッションテンプレートが `mpmissions/` 内の既存フォルダと一致していません。

**対処法:** テンプレート値を確認します。フォルダ名と正確に一致する必要があります:

```cpp
template = "dayzOffline.chernarusplus";  // mpmissions/ のフォルダ名と一致する必要があります
```

---

**[ホーム](../README.md)** | **次へ:** [ディレクトリ構造 >>](02-directory-structure.md)
