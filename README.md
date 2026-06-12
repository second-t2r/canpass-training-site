# canpass-training-site

CanPass の研修・運用資料（Web版スライド）。

- `index.html` … 入口（PWゲート＋一覧）
- `worker.html` … ① CanPass はたらき方研修（ワーカー向け・全31枚）
- `admin.html` … ② CanPass 運用ガイド（PM/運用向け・L2・全33枚）
- `assets/{worker,admin}/*.jpg` … スライド画像（自己完結・外部依存なし）
- 操作 … 矢印キー/スペース/クリックで送り。`noindex` 付与。
- 再生成 … `python3 build.py`（`~/work/cancer/intermediate/qa/*.pdf` から画像化）

## 取り扱い注意（重要）

- 本資料は **L2機密・関係者限定**。いずれも最終版ではなく **敲き**（今後、研修ごとの筆記テスト・実地訓練のプログラム化/資料化を進める）。
- 公開方法は **GitHub Pages の限定URL運用＋PWゲート（"CanPass"）**。**いずれも真のアクセス制御ではない**（限定URLは推測されにくいだけ、PWはクライアント側JS＝ソースを見れば回避可能）。社外秘の確実な保護にはならない点に留意。
- **医療系の生データ・実名・診断名・録画・原本は本リポジトリに一切含めない**（`.gitignore` でガード）。スライド内も符号（worker-A / client-X）運用。
- 運用ガイドの配布判断は **PM→代表**。経営マター（事業計画・出資・送金）は本資料の対象外。
- 社外提示・対外/医療表現は、配布前に **久保監修＋代表承認** を通す。

## 出典

CanPass 運用ルール整備（2026-06）。正本：`~/work/cancer/ops/rules/`（workspace_logging_spec / distribution_rules / naming_conventions）。
