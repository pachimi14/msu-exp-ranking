# MSU Ranking（自分用メモ）

ローカル: `C:\Users\pachi\Desktop\msu ranking`  
取引 bot は別フォルダ: `C:\Users\pachi\Desktop\msu trade`（この Git には含めない）

```
exp_ranking/
├── bot/   … API 取得 → SQLite（35日）→ rankings.json
└── web/   … React / Vite
```

## よく使う

| 用途 | 操作 |
|------|------|
| データ取得 | `run_exp_ranking_fetch.bat` |
| UI 開発 | `run_exp_ranking_web.bat` → http://localhost:5173/ |
| ダミー増加量 | `run_inject_dummy_gains.bat` |

## 公開まわり

- リポジトリ: https://github.com/pachimi14/msu-exp-ranking （public）
- Pages: https://pachimi14.github.io/msu-exp-ranking/
- 手順・Actions・トラブル: [exp_ranking/DEPLOY.md](exp_ranking/DEPLOY.md)
- bot 設定: [exp_ranking/bot/README.md](exp_ranking/bot/README.md)
