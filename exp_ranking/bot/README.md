# MSU Ranking Bot

MSU のランキング API から **指定レベル以上**のキャラを全件取得し、SQLite に保存して `rankings.json` を出力します。

## 取得条件（既定・テスト）

| 設定 | 既定 | 説明 |
|------|------|------|
| `RANKING_MIN_LEVEL` | **225** | このレベル以上のキャラのみ保存 |
| `RANKING_MAX_PAGES` | 600 | 安全のための最大ページ数 |

API は総合順位順です。ページを進めるとレベルが下がるため、**そのページの最大レベルが `RANKING_MIN_LEVEL` 未満になった時点で取得を終了**します。

目安（2026-06 時点）:

| 最小レベル | おおよその人数 | ページ数 |
|------------|----------------|----------|
| 235+ | 約 950 人 | 約 95 ページ |
| 225+（既定） | 約 5500 人 | 約 550 ページ |

235+ のみにする場合は `.env` で `RANKING_MIN_LEVEL=235` に変更してください。

## データ保持

月間増加用に DB は直近 **35 ランキング日**のみ（`SNAPSHOT_RETENTION_DAYS`）。それより古い行は削除します。

ランキング日は **UTC 0:00（JST 9:00）** で切り替わります。スケジューラは **毎日 9:05 JST 以降** に 1 回実行を推奨します。

## Run

```powershell
cd exp_ranking\bot
pip install -r requirements.txt
copy .env.example .env
python main.py
```

| 用途 | bat |
|------|-----|
| データ取得 | `run_exp_ranking_fetch.bat` |
| Web | `run_exp_ranking_web.bat` |
| UIテスト用ダミー増加量 | `run_inject_dummy_gains.bat`（`rankings.json.bak` を作成） |
